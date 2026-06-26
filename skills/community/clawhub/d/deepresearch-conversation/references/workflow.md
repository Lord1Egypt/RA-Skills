# DeepResearch 完整调用工作流

> 本文是 `scripts/deepresearch.py` 背后的实现细节文档。脚本已经封装了 SSE 解析、HTTP 长连接、interrupt_id 嵌套解析等所有底层逻辑；只有当你需要自行实现客户端、调试异常或做并发压测时才需要查阅本文。

## 目录
1. [完整流程图](#完整流程图)
2. [SSE 流解析要点](#sse-流解析要点)
3. [HTTP 客户端注意事项](#http-客户端注意事项)
4. [单阶段自动执行模式](#单阶段自动执行模式)
5. [Python 实现示例](#python-实现示例)
6. [Go 实现要点](#go-实现要点)
7. [并发压测模式](#并发压测模式)
8. [常见问题排查](#常见问题排查)

---

## 完整流程图

```
用户输入研究问题
       ↓
═══════════════════════════════════════
  单阶段自动流程 (脚本 run 子命令)
═══════════════════════════════════════
       ↓
[Step 1] POST /create → 获取 conversation_id
         Body: { version } 或 { agent_id }（都可选，同时提供时以 agent_id 为准，都不提供默认 version=lite）
       ↓
[Step 2] POST /run (初始 query + version/agent_id) → 读 SSE 流
       ↓
  是否有澄清事件？
  (role=assistant + event.name="/chat/chat_agent")
  ┌──── 是 ────────────────────┐
  ↓                            ↓
[Step 3a]                   [Step 3b]
等待 ≥10s 后                 直接进入 Step 4
POST /run (query="跳过")
→ 读 SSE 流
  └───────────────────────────┘
       ↓
[Step 4] 从 SSE 事件中提取：
  - interrupt_id
  - structured_outline
       ↓
[Step 5] 自动确认大纲
  POST /run (query="确认" +
   interrupt_id +
   structured_outline)
  → 读 SSE 流
       ↓
  收到 .html 文件事件
       ↓
  stdout 输出结果 JSON → 流程结束
```

---

## SSE 流解析要点

### 流结束信号（满足任一即可停止读取）

- `status == "interrupt"` — 大纲 / 澄清阶段结束，等待下一步指令
- `event.is_end == true && event.is_stop == true` — 整个流程结束
- `content.type == "files"` 且 `filename` 以 `.html` 结尾 — 报告已生成完成

### 关键事件识别

| 阶段 | 识别字段 |
|------|----------|
| 需求澄清 | `role=assistant`, `event.name="/chat/chat_agent"` |
| 大纲生成 | `event.name="/toolcall/structured_outline"`, `status=interrupt` |
| 中断等待 | `status="interrupt"`, `event.name="/toolcall/interrupt"` |
| 文件生成 | `content.type="files"`, `filename` 以 `.md` 或 `.html` 结尾 |

### interrupt_id 提取（注意嵌套 JSON）

`content.text` 是 `{ "data": "<JSON字符串>" }` 结构，需做 **两次 JSON 解析**：

```python
raw = json.loads(content["text"])          # 得到 {"data": "..."}
interrupt_data = json.loads(raw["data"])   # 得到 {"interrupt_id": "...", ...}
interrupt_id = interrupt_data["interrupt_id"]
```

`structured_outline` 也是相同的双层 JSON 结构，解析方式一致。

---

## HTTP 客户端注意事项

- **禁止设置整体超时**：SSE 是长连接，应使用空闲超时（推荐 10 分钟无数据则断开）。
- **禁用 gzip 压缩**：发送 `Accept-Encoding: identity` 或不发该头，避免流式数据被压缩缓冲。
- **禁用 HTTP/2**：强制使用 HTTP/1.1，与 curl 默认行为一致，避免某些代理对 HTTP/2 流的提前关闭。
- **Authorization 头格式**：`Bearer {api_key}`。

---

## 单阶段自动执行模式

脚本设计为单个 `run` 子命令，全程无需用户交互，自动完成澄清跳过和大纲确认：

```bash
python3 scripts/deepresearch.py run \
  --query "研究问题" \
  --api-key "bce-v3/ALTAK-..." \
  --version lite
```

stdout 输出（一行 JSON）：
```json
{
  "conversation_id": "de65bd4c-...",
  "outline": {"title": "...", "description": "...", "sub_chapters": [...]},
  "outline_preview": "标题：...\n描述：...\n\n章节结构：\n  1. ...",
  "files": {
    "md": {"filename": "report_xxx.md", "download_url": "https://..."},
    "html": {"filename": "report_xxx.html", "download_url": "https://..."}
  }
}
```

---

## Python 实现示例

```python
import json
import requests
import time

BASE_URL = "https://qianfan.baidubce.com/v2"
API_KEY = "your-api-key"
VERSION = "lite"  # lite（默认，轻量版）| standard（标准版）| pro（高级版）

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept-Encoding": "identity",  # 禁用 gzip，确保 SSE 正常接收
}

IDLE_TIMEOUT = 600  # 10 分钟空闲超时


def create_conversation():
    """Step 1: 创建会话，获取 conversation_id"""
    resp = requests.post(
        f"{BASE_URL}/agent/deepresearch/create",
        headers=HEADERS,
        json={"version": VERSION},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["result"]["conversation_id"]


def stream_sse(payload, early_stop=None):
    """
    发送 POST /run 并读取 SSE 流，返回所有事件列表。
    early_stop: callable(event) -> bool，返回 True 时提前退出
    """
    events = []
    with requests.post(
        f"{BASE_URL}/agent/deepresearch/run",
        headers=HEADERS,
        json=payload,
        stream=True,
        timeout=None,  # 不设整体超时，用空闲超时控制
    ) as resp:
        resp.raise_for_status()
        last_data_time = time.time()

        for line in resp.iter_lines(decode_unicode=True):
            if time.time() - last_data_time > IDLE_TIMEOUT:
                raise TimeoutError("SSE idle timeout (10 min)")

            if not line:
                continue

            last_data_time = time.time()

            if line.startswith("data:"):
                raw = line[5:].strip()
            elif line.startswith("data:{"):
                raw = line[4:].strip()
            else:
                continue

            if raw == "[DONE]":
                break

            try:
                event = json.loads(raw)
            except json.JSONDecodeError:
                continue

            events.append(event)

            if event.get("status") == "interrupt":
                break

            for content in event.get("content", []):
                ev_info = content.get("event") or {}
                if ev_info.get("is_end") and ev_info.get("is_stop"):
                    return events

            if early_stop and early_stop(event):
                break

    return events


def has_clarification(events):
    """判断是否有需求澄清事件"""
    for event in events:
        if event.get("role") == "assistant":
            for content in event.get("content", []):
                ev_info = content.get("event") or {}
                if ev_info.get("name") == "/chat/chat_agent":
                    return True
    return False


def extract_interrupt_id(events):
    """从事件流中提取 interrupt_id（注意嵌套JSON）"""
    for event in events:
        if event.get("status") == "interrupt":
            for content in event.get("content", []):
                if content.get("type") == "json":
                    ev_info = content.get("event") or {}
                    if ev_info.get("name") == "/toolcall/interrupt":
                        text = content.get("text", {})
                        if "data" in text:
                            inner = json.loads(text["data"])
                            if inner.get("interrupt_id"):
                                return inner["interrupt_id"]
    return None


def extract_structured_outline(events):
    """从事件流中提取 structured_outline（注意嵌套JSON）"""
    for event in events:
        for content in event.get("content", []):
            if content.get("type") == "json":
                ev_info = content.get("event") or {}
                if ev_info.get("name") == "/toolcall/structured_outline":
                    text = content.get("text", {})
                    if "data" in text:
                        outline = json.loads(text["data"])
                        if outline.get("title"):
                            return outline
    return None


def extract_files(events):
    """从事件流中提取生成的文件信息"""
    files = {}
    for event in events:
        for content in event.get("content", []):
            if content.get("type") == "files":
                text = content.get("text", {})
                filename = text.get("filename", "")
                if filename.endswith(".md") and "md" not in files:
                    files["md"] = text
                elif filename.endswith(".html") and "html" not in files:
                    files["html"] = text
    return files


def format_outline_preview(outline):
    """格式化大纲预览内容"""
    lines = []
    lines.append(f"标题：{outline.get('title', '')}")
    lines.append(f"描述：{outline.get('description', '')}")
    lines.append("")
    lines.append("章节结构：")
    for i, ch in enumerate(outline.get("sub_chapters", []), 1):
        lines.append(f"  {i}. {ch.get('title', '')}")
        for sub in ch.get("sub_chapters", []):
            lines.append(f"     - {sub.get('title', '')}")
    return "\n".join(lines)


def run_full(query):
    """单阶段自动执行：查询 → 大纲 → 自动确认 → 报告"""
    # Step 1
    conversation_id = create_conversation()

    # Step 2
    events = stream_sse({
        "query": query,
        "version": VERSION,
        "conversation_id": conversation_id,
    })

    # Step 3: 自动跳过澄清
    if has_clarification(events):
        time.sleep(10)
        events = stream_sse({
            "query": "跳过",
            "version": VERSION,
            "conversation_id": conversation_id,
        })

    # Step 4: 提取大纲
    interrupt_id = extract_interrupt_id(events)
    outline = extract_structured_outline(events)
    if not interrupt_id or not outline:
        raise ValueError("未能提取 interrupt_id 或 structured_outline")

    # Step 5: 自动确认大纲，生成报告
    def is_html_file(event):
        for content in event.get("content", []):
            if content.get("type") == "files":
                filename = content.get("text", {}).get("filename", "")
                if filename.endswith(".html"):
                    return True
        return False

    report_events = stream_sse({
        "query": "确认",
        "version": VERSION,
        "conversation_id": conversation_id,
        "interrupt_id": interrupt_id,
        "structured_outline": outline,
    }, early_stop=is_html_file)

    files = extract_files(report_events)

    return {
        "conversation_id": conversation_id,
        "outline": outline,
        "outline_preview": format_outline_preview(outline),
        "files": files,
    }


# 使用示例
if __name__ == "__main__":
    result = run_full("研究2025年全球AI市场规模与发展趋势")
    print(f"大纲: {result['outline_preview']}")
    if result["files"]:
        print(f"MD: {result['files'].get('md', {}).get('download_url')}")
        print(f"HTML: {result['files'].get('html', {}).get('download_url')}")
```

---

## Go 实现要点

参考压测代码（`main.go`）的关键设计：

### HTTP Client 配置
```go
client := &http.Client{
    // 不设 Timeout！SSE 长连接下会被提前关闭
    Transport: &http.Transport{
        DisableCompression: true,  // 禁用 gzip，与 curl 行为一致
        ForceAttemptHTTP2:  false, // 强制 HTTP/1.1
        TLSNextProto:       make(map[string]func(authority string, c *tls.Conn) http.RoundTripper),
        DialContext: (&net.Dialer{
            Timeout:   30 * time.Second,
            KeepAlive: 30 * time.Second,
        }).DialContext,
    },
}
```

### SSE 空闲超时控制
```go
const idleTimeout = 10 * time.Minute
idleTimer := time.AfterFunc(idleTimeout, func() { cancel() })
defer idleTimer.Stop()

// 收到任意数据时重置计时器
idleTimer.Reset(idleTimeout)
```

### SSE 行读取（兼容两种格式）
```go
scanner := bufio.NewScanner(resp.Body)
scanner.Buffer(make([]byte, 10*1024*1024), 10*1024*1024) // 10MB buffer
for scanner.Scan() {
    line := scanner.Text()
    var raw string
    if strings.HasPrefix(line, "data: ") {
        raw = strings.TrimPrefix(line, "data: ")
    } else if strings.HasPrefix(line, "data:{") {
        raw = strings.TrimPrefix(line, "data:")
    } else {
        continue
    }
    if raw == "[DONE]" { break }
    // 解析 JSON...
}
```

---

## 并发压测模式

参考 `main.go` 的并发控制设计：

```python
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_benchmark(queries, concurrency=5, total_requests=10):
    """并发压测"""
    results = []
    counter = 0
    lock = threading.Lock()

    def worker(idx):
        nonlocal counter
        query = queries[idx % len(queries)]

        with lock:
            nonlocal counter
            counter += 1
            n = counter
        if n > 1:
            time.sleep(0.1)

        start = time.time()
        try:
            result = run_full(query)
            duration = time.time() - start
            return {"success": True, "duration": duration, "files": result["files"], "query": query}
        except Exception as e:
            duration = time.time() - start
            return {"success": False, "error": str(e), "duration": duration, "query": query}

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(worker, i) for i in range(total_requests)]
        for future in as_completed(futures):
            results.append(future.result())

    success = [r for r in results if r["success"]]
    print(f"总请求: {total_requests}, 成功: {len(success)}, 失败: {total_requests - len(success)}")
    if success:
        durations = [r["duration"] for r in success]
        print(f"平均耗时: {sum(durations)/len(durations):.1f}s")
        print(f"P99耗时: {sorted(durations)[int(len(durations)*0.99)]:.1f}s")
    return results
```

### 并发配置建议

| 场景 | concurrency | request_interval_ms |
|------|-------------|---------------------|
| 功能测试 | 1 | 0 |
| 轻度压测 | 3-5 | 100 |
| 中度压测 | 10 | 200 |
| 高并发压测 | 20+ | 500 |

---

## 常见问题排查

### 1. SSE 流提前断开（context canceled）
- **原因**: 设置了整体 HTTP 超时或代理的连接超时
- **解决**: 使用空闲超时代替整体超时，超时时间 ≥ 10 分钟

### 2. 找不到 interrupt_id
- **原因**: 大纲阶段的 `text` 字段是嵌套 JSON 字符串，未做二次解析
- **解决**: 先解析 `text.data` 字段（字符串），再解析其中的 JSON

### 3. 报告生成超时（耗时 >10 分钟）
- **原因**: 深度研究任务耗时较长，服务端长时间未推送数据（已知问题）
- **解决**: 增大空闲超时时间，或监控报告生成任务状态

### 4. 澄清阶段发送"跳过"后无响应
- **原因**: 澄清阶段需等待 Agent 完成澄清对话后再发送，过早发送会被忽略
- **解决**: 确认收到 `status=interrupt` 事件后再发送跳过请求，建议等待 ≥10 秒

### 5. HTTP 400 / 401 错误
- **401**: API Key 无效或格式错误，检查 `Authorization: Bearer {api_key}` 格式
- **400**: 请求参数错误，常见原因：`version` 值无效或 `interrupt_id` 不匹配

### 6. 脚本在 Agent 环境中无法交互
- **原因**: Agent 通过 run_command 执行脚本，没有 stdin
- **解决**: 使用单阶段自动模式（run 子命令），全程无需用户交互
