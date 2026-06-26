# DeepSeek V3.2 API 集成文档

> 为 DeepSeek V4 切换做准备 · 2026-04-14

---

## 1. 概述

### 1.1 什么是 DeepSeek V3.2

DeepSeek V3.2 是国产大模型 DeepSeek 的最新版本，通过 **OpenAI 兼容 API** 提供服务。与 V3.1 相比，V3.2 主要升级：

| 特性 | V3.1 | V3.2 |
|------|------|------|
| 模型 ID | `deepseek-chat` | `deepseek-chat`（底层升级） |
| 推理模型 ID | `deepseek-reasoner` | `deepseek-reasoner`（底层升级） |
| 上下文窗口 | 128K | 128K |
| `reasoning_content` 暴露 | ✅ | ✅（增强） |
| JSON Mode | ✅ | ✅ |
| Function Calling | ✅ | ✅ |
| Beta 端点 8K max_tokens | ✅ | ✅ |
| FIM Completion | ✅ | ✅（Beta） |
| Chat Prefix Completion | ✅ | ✅（Beta） |
| Context Caching | ❌ | ✅（降成本） |

> **V4 预告**：DeepSeek V4 预计 2026 年 4 月下旬发布，届时只需修改 `model` 参数为 `deepseek-chat-v4` 或 `deepseek-reasoner-v4`，无需改动代码。

### 1.2 两个模型的区别

| 模型 ID | 模式 | 适用场景 | 特点 |
|---------|------|----------|------|
| `deepseek-chat` | 非思考模式 | 通用对话、代码生成、快速问答 | 响应快、成本低 |
| `deepseek-reasoner` | 思考模式 | 数学推理、复杂分析、代码调试 | 内置思维链（CoT），返回 `reasoning_content` |

两者底层共享 V3.2 架构，API 格式完全一致，**仅切换 `model` 参数即可切换模式**。

---

## 2. 快速开始

### 2.1 安装依赖

```bash
pip install httpx       # 推荐（已在 agent-cluster 间接依赖）
pip install openai      # 可选，OpenAI SDK 方式调用时使用
```

### 2.2 获取 API Key

1. 访问 [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. 创建新 API Key（格式：`dsk-xxx`）
3. 将 Key 存入环境变量（**不要硬编码**）

```bash
# Linux / macOS
export DEEPSEEK_API_KEY="dsk-your-key-here"

# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="dsk-your-key-here"
```

### 2.3 Python 快速调用

#### 方式一：直接使用 httpx（推荐用于 agent-cluster）

```python
import httpx
import os

client = httpx.AsyncClient(timeout=120.0)
response = await client.post(
    "https://api.deepseek.com/chat/completions",
    json={
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in one sentence."},
        ],
        "max_tokens": 500,
        "temperature": 0.3,
    },
    headers={
        "Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json",
    },
)
data = response.json()
print(data["choices"][0]["message"]["content"])
```

#### 方式二：OpenAI SDK 兼容调用

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",  # 或 "https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)
print(response.choices[0].message.content)
```

#### 方式三：cURL 快速测试

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 500,
    "temperature": 0.3,
    "stream": false
  }'
```

---

## 3. 引擎集成架构

### 3.1 在 agent-cluster 中使用

```python
from execution.deepseek_engine import DeepSeekEngine

# 初始化引擎
engine = DeepSeekEngine({
    "api_key": os.environ["DEEPSEEK_API_KEY"],
    "model": "deepseek-chat",       # 或 "deepseek-reasoner"
    "max_tokens": 4096,
    "temperature": 0.3,
    "json_mode": False,
})

# 执行任务
result = await engine.execute(
    task="查询今日库存情况",
    context={
        "user_id": "u001",
        "user_role": "admin",
        "intent_type": "stock_query",
    },
)

print(result.output["content"])
print(f"Tokens: {result.tokens_used}, Latency: {result.latency_ms}ms")
```

### 3.2 通过 EngineRouter 自动路由

DeepSeek 引擎已注册到 `EngineRouter`，以下场景会自动路由到 DeepSeek：

```python
from execution.engine_router import EngineRouter, RoutingContext

router = EngineRouter()

ctx = RoutingContext(
    task="需要使用国产合规方案",
    intent_type="compliance",
    user_role="admin",
    scene="compliance",
    entities={},
)
# → 自动路由到 domestic-deepseek-chat
```

### 3.3 配置项说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | env: `DEEPSEEK_API_KEY` | API Key，优先级：config > env |
| `model` | str | `deepseek-chat` | 模型 ID：`deepseek-chat` / `deepseek-reasoner` |
| `base_url` | str | `https://api.deepseek.com` | API 端点 |
| `max_tokens` | int | 4096 | 最大输出 token（Beta 端点上限 8K） |
| `temperature` | float | 0.3 | 采样温度（0~1） |
| `reasoning_effort` | float | 0.5 | 思维链努力程度（0~1，仅 R1 生效） |
| `timeout` | float | 120.0 | 请求超时秒数 |
| `json_mode` | bool | False | 强制 JSON 输出 |
| `use_beta` | bool | False | 使用 Beta 端点（8K max_tokens / FIM / Prefix Completion） |

---

## 4. V3.2 高级特性

### 4.1 reasoning_content（推理思维链）

**仅 `deepseek-reasoner` 模式有效**

```python
result = await engine.execute(
    task="求 x³ - 6x² + 11x - 6 = 0 的解",
    context=build_context(intent_type="analysis"),
)

# 最终答案
print(result.output["content"])

# 推理过程（V3.2 新增增强）
if result.output.get("reasoning_content"):
    print("=== 推理过程 ===")
    print(result.output["reasoning_content"])
```

**输出结构：**
```json
{
  "choices": [{
    "message": {
      "content": "答案是 42",           // 最终答案
      "reasoning_content": "逐步推理..." // 思维链（reasoner 模式）
    }
  }]
}
```

### 4.2 JSON Mode（结构化输出）

适用于需要程序化解析结果的场景：

```python
engine = DeepSeekEngine({
    "api_key": api_key,
    "json_mode": True,
})

result = await engine.execute(
    task='返回一个 JSON：{"name": str, "age": int, "skills": list[str]}',
    context=build_context(),
)

import json
data = json.loads(result.output["content"])
print(data["name"])
```

### 4.3 多轮对话（带历史）

```python
result = await engine.execute(
    task="继续",
    context={
        **build_context(),
        "history": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮你的？"},
        ],
    },
)
```

### 4.4 流式输出（SSE）

```python
async for chunk in engine.stream("写一篇短文", build_context()):
    if chunk.done:
        print("\n[流式输出完成]")
    else:
        print(chunk.content, end="", flush=True)
```

> ⚠️ **注意**：`deepseek-reasoner` 模式暂不支持 SSE 流式输出，引擎会自动降级为阻塞调用后分词流式展示。

### 4.5 Beta 端点（8K max_tokens / FIM / Prefix Completion）

```python
engine = DeepSeekEngine({
    "api_key": api_key,
    "use_beta": True,        # 切换到 /beta 端点
    "max_tokens": 8192,      # 自动限制到 8K
})
```

Beta 端点额外支持：
- **FIM Completion**：代码中间补全（`POST /completions`）
- **Chat Prefix Completion**：续写指定前缀

### 4.6 Context Caching（降低长上下文成本）

将长文档作为 context 复用时，DeepSeek V3.2 支持上下文缓存：

```python
# 目前通过 system prompt 注入长文档（未来版本将支持专用 cache API）
messages = [
    {"role": "system", "content": "参考文档：\n" + long_document},
    {"role": "user", "content": "基于上述文档回答：..."},
]
```

---

## 5. 错误处理

### 5.1 错误码对照表

| HTTP 状态码 | error_code | 含义 | 处理建议 |
|-------------|-----------|------|----------|
| 401 | `invalid_api_key` | API Key 无效 | 检查 `DEEPSEEK_API_KEY` 配置 |
| 403 | `forbidden` | 无访问权限 | 检查账户余额和权限 |
| 429 | `rate_limit_exceeded` | 请求频率超限 | 添加重试延迟（指数退避） |
| 500 | `internal_server_error` | DeepSeek 服务器错误 | 稍后重试 |
| 503 | `service_unavailable` | 服务不可用 | 降级到其他引擎 |

### 5.2 引擎内错误处理

```python
from execution.deepseek_engine import DeepSeekEngine, DeepSeekAPIError

engine = DeepSeekEngine({"api_key": api_key})

try:
    result = await engine.execute(task, context)
    if not result.success:
        logger.error(f"DeepSeek 执行失败: {result.error}")
        # → 触发 EngineRouter 降级
except DeepSeekAPIError as e:
    if e.status_code == 429:
        await asyncio.sleep(5)  # 退避重试
        ...
```

### 5.3 降级策略

在 `engines.yaml` 中配置：

```yaml
fallback:
  order:
    - local-self-built      # DeepSeek 失败 → 本地引擎
    - claude-managed-agents # 本地也失败 → Claude MA
  conditions:
    timeout_seconds: 60
    max_retries: 1
    retry_on_error: true
```

---

## 6. V4 切换指南

V4 发布后，切换步骤：

### 步骤 1：更新配置

**`config/engines.yaml`**：
```yaml
engines:
  deepseek:
    model: "deepseek-chat-v4"      # V4 模型 ID（TBD，以官方公告为准）
    # deepseek-reasoner-v4
```

或通过环境变量：
```bash
export DEEPSEEK_MODEL="deepseek-chat-v4"
```

### 步骤 2：运行回归测试

```bash
DEEPSEEK_API_KEY=sk-xxx pytest agent-cluster/tests/test_deepseek_engine.py -v
```

### 步骤 3：验证生产场景

重点验证：
- [ ] 基础对话（deepseek-chat-v4）
- [ ] 复杂推理（deepseek-reasoner-v4）
- [ ] JSON Mode 输出格式
- [ ] Function Calling（Agent 场景）
- [ ] 响应延迟和 Token 消耗对比

### 步骤 4：监控指标

```python
# 切换后监控指标
- result.latency_ms（延迟）
- result.tokens_used（Token 消耗）
- result.success（成功率）
- error rate（按错误码分类）
```

---

## 7. 安全注意事项

1. **API Key 安全存储**
   - ✅ 使用环境变量或 `.env` 文件
   - ❌ 禁止硬编码在代码中
   - ❌ 禁止提交到 Git（已在 `.gitignore` 中排除 `.env`）

2. **生产环境白名单**
   ```python
   # 生产环境建议启用 httpx 白名单
   export DEEPSEEK_WHITELIST_ENABLED="true"
   # 域名 api.deepseek.com 已在白名单中
   ```

3. **日志脱敏**
   - API Key 在日志中显示为 `dsk-xxx***`
   - 请求内容不记录 Token 字段

---

## 8. 性能基准参考

> 以下为参考值，实际性能取决于网络和任务复杂度。

| 模型 | 场景 | 预期延迟 | Token 消耗 |
|------|------|----------|------------|
| `deepseek-chat` | 简单对话（100字） | 0.5~2s | ~200 tokens |
| `deepseek-chat` | 代码生成（200字） | 1~3s | ~400 tokens |
| `deepseek-reasoner` | 数学推理（中等） | 3~8s | ~800 tokens（含 CoT） |
| `deepseek-reasoner` | 复杂分析（长） | 8~15s | ~1500 tokens（含 CoT） |

---

## 9. 参考资源

| 资源 | 地址 |
|------|------|
| DeepSeek 官方文档 | https://api-docs.deepseek.com/ |
| DeepSeek 控制台（API Key 管理） | https://platform.deepseek.com/api_keys |
| V3.2 模型说明 | https://platform.deepseek.com/docs |
| DeepSeek V4 发布公告 | 待更新（预计 2026-04 下旬） |

---

## Change Log

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-04-14 | v0.1 | 初始文档，V3.2 API 集成测试版本 |
| 2026-04-（待更新） | v0.2 | V4 切换记录 |
