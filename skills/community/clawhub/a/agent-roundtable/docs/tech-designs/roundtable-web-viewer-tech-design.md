# 圆桌 Web Viewer — 后端技术方案

> 作者：码飞（技术总监）
> 日期：2026-05-21
> 状态：已批准（2026-05-21）

---

## 1. 架构概述

```
┌──────────────────────────────────────────────────┐
│            Roundtable.run() 主循环                 │
│                                                    │
│   publisher = WebPublisher(discussion_dir)         │
│   publisher.start(discussion_id, token)            │
│                                                    │
│   for speech in speeches:                          │
│       publisher.on_speech(speech)   # Hook 1       │
│                                                    │
│   publisher.conclude(conclusion)    # Hook 2       │
├──────────────────────────────────────────────────┤
│          WebPublisher (Python)                     │
│                                                    │
│   ┌─────────────┐   ┌──────────────────┐          │
│   │ fcntl.flock  │   │ PM2 管理         │          │
│   │ 文件锁写入   │   │ Express 进程     │          │
│   └──────┬──────┘   └────────┬─────────┘          │
│          │                   │                     │
│          ▼                   ▼                     │
│   discussion.json    http://0.0.0.0:<port>        │
│   (原子写入)          GET /r/:token → SPA          │
│                      GET /api/:token/data → JSON   │
│                      GET /api/:token/events → SSE  │
│                      POST /api/:token/revoke       │
└──────────────────────────────────────────────────┘
```

## 2. 文件结构

```
roundtable_ai/
  web_publisher.py         # 核心模块：WebPublisher 类
  web/
    index.html             # 单文件 SPA（内联 CSS+JS，Tailwind CDN）
    theme.css              # CSS 变量表
    server.mjs             # Express 服务（Node.js）
    ecosystem.config.cjs   # PM2 配置文件
```

### discussion.json 路径约定

`discussion.json` 存放在每个讨论的输出目录下：

```
output/{discussion_id}/
  discussion.json          # 讨论数据（WebPublisher 读写）
  transcript.md            # 讨论记录（其他模块生成）
```

WebPublisher 构造时传入 `discussion_dir`，即 `output/{discussion_id}/` 路径。

## 3. WebPublisher 类设计

```python
class WebPublisher:
    """管理圆桌讨论的 Web 查看页面。"""

    def __init__(
        self,
        discussion_dir: str,       # discussion.json 所在目录
        port: int = 8199,          # 默认端口，可通过 --web-port 覆盖
        host: str = "0.0.0.0",     # 绑定地址
    ):
        self._discussion_dir = Path(discussion_dir)
        self._port = port
        self._host = host
        self._token: str | None = None
        self._discussion_id: str | None = None
        self._pm2_process_name: str | None = None  # PM2 进程名
        self._revoked: bool = False

    def start(self, discussion_id: str, token: str | None = None) -> str:
        """启动 Web 服务，返回完整 URL。

        1. 生成 nanoid(21) token（如果未提供）
        2. 写入初始 discussion.json（带文件锁）
        3. 端口探测 + PM2 启动 Express
        4. 返回 URL：http://<host>:<port>/r/<token>
        """

    def on_speech(self, speech: dict) -> None:
        """Hook：新发言。通过文件锁更新 discussion.json。

        discussion.json 格式：
        {
          "discussion_id": "rt_xxx",
          "topic": "...",
          "status": "active" | "concluded",
          "participants": [...],
          "speeches": [...],
          "conclusion": null | "...",
          "updated_at": 1234567890
        }
        """

    def conclude(self, conclusion: str) -> None:
        """Hook：讨论结束。追加 conclusion 字段，更新 status。"""

    def revoke(self) -> None:
        """L1 链接撤销。标记 token 为已撤销。"""

    def stop(self) -> None:
        """PM2 停止 Express 进程。"""

    @property
    def url(self) -> str | None:
        """当前 Web 页面 URL。"""
```

## 4. 端口探测策略

```python
def _find_available_port(self, preferred: int) -> int:
    """优先使用 preferred，冲突时自动 +1 递增（最多尝试 10 个）。"""
    for offset in range(10):
        port = preferred + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No available port in range {preferred}-{preferred+9}")
```

## 5. 文件锁方案（fcntl.flock）

```python
def _write_discussion_json(self, data: dict) -> None:
    """原子写入 discussion.json：flock → 写临时文件 → rename。"""
    target = self._discussion_dir / "discussion.json"
    tmp = target.with_suffix(".json.tmp")

    with open(tmp, "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    os.rename(tmp, target)  # 原子操作
```

关键点：
- `LOCK_EX` 排他锁，确保读写互斥
- 先写 `.tmp` 再 `os.rename()`，保证原子性
- `os.fsync()` 确保数据落盘
- 读取端（Express）用 `LOCK_SH` 共享锁

## 6. Express 服务设计（server.mjs）

### 6.1 依赖

- `express` — 路由 + 静态文件
- 无其他依赖，零额外 npm 包

### 6.2 路由

| 路径 | 方法 | 逻辑 |
|------|------|------|
| `/r/:token` | GET | 返回 index.html SPA |
| `/api/:token/data` | GET | 读取 discussion.json，`flock(LOCK_SH)` |
| `/api/:token/events` | GET | SSE 推送，`flock(LOCK_SH)` + `fs.watch()` |
| `/api/:token/revoke` | POST | 写入 revoked tokens 文件 |

### 6.3 SSE 实现

```javascript
// GET /api/:token/events
app.get('/api/:token/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  });

  // 初始推送
  const data = readDiscussion(req.params.token);
  res.write(`event: init\ndata: ${JSON.stringify(data)}\n\n`);

  // Last-Event-ID 支持
  const lastId = req.headers['last-event-id'] || 0;

  // fs.watch 监听 discussion.json 变化
  const watcher = fs.watch(discussionPath, () => {
    const newData = readDiscussion(req.params.token);
    const eventId = Date.now();
    res.write(`id: ${eventId}\nevent: update\ndata: ${JSON.stringify(newData)}\n\n`);
  });

  req.on('close', () => watcher.close());
});
```

### 6.4 长轮询降级（微信兼容）

```javascript
// GET /api/:token/poll?since=<timestamp>
app.get('/api/:token/poll', (req, res) => {
  const since = parseInt(req.query.since) || 0;
  // 阻塞等待最多 25 秒
  waitForUpdate(since, 25000).then(data => {
    res.json(data);
  });
});
```

前端检测 `EventSource` 是否可用，不可用时降级为长轮询。

## 7. Token 安全

```python
from nanoid import generate  # pip install nanoid

token = generate(size=21)  # 默认 alphabet，21 字符
```

- Token 存储在 discussion.json 的顶层字段 `token`
- 撤销状态存储在 `discussion.json` 的 `revoked_tokens` 数组
- 每个请求校验 token 有效性

## 8. 讨论数据格式（discussion.json）

```json
{
  "discussion_id": "rt_36c7dbdd",
  "topic": "内置 Web 查看页面",
  "status": "active",
  "token": "V1StGXR8_Z5jdHi6B-myT",
  "participants": [
    {
      "profile": "baoyu",
      "display_name": "饼哥",
      "role": "产品总监"
    }
  ],
  "speeches": [
    {
      "id": 1,
      "round": 0,
      "participant": "baoyu",
      "display_name": "饼哥",
      "content": "...",
      "created_at": 1234567890
    }
  ],
  "conclusion": null,
  "revoked_tokens": [],
  "updated_at": 1234567890
}
```

## 9. 里程碑计划

| 阶段 | 内容 | 预计耗时 |
|------|------|----------|
| M1 | WebPublisher 类 + 文件锁 + 端口探测 + discussion.json 写入 | 2h |
| M1.5 | Express server.mjs（4 个路由 + SSE + 长轮询） | 2h |
| M2 | SPA index.html 骨架（像素姐可并行） | 1h |
| M3 | SSE 实时更新联调 + 断线重连 + 微信降级 | 2h |
| M4 | 集成到 Roundtable.run() + L1 撤销接口 | 1h |
| M5 | 测试 + 验收 | 2h |

## 10. 依赖清单

### Python
- `nanoid` — Token 生成（pip install nanoid）
- `fcntl` — 文件锁（stdlib，仅 Unix）

### Node.js
- `express` — Web 框架
- 无其他 npm 依赖

## 11. PM2 进程管理

使用 PM2 管理 Express 进程，Python 通过 `pm2` CLI 操作：

```python
def _start_pm2(self, port: int) -> None:
    """PM2 启动 Express 服务。"""
    server_path = Path(__file__).parent / "web" / "server.mjs"
    self._pm2_process_name = f"roundtable-web-{self._discussion_id}"

    subprocess.run([
        "pm2", "start", str(server_path),
        "--name", self._pm2_process_name,
        "--interpreter", "node",
        "--",
        "--port", str(port),
        "--discussion-dir", str(self._discussion_dir),
    ], check=True)

def stop(self) -> None:
    """PM2 停止 Express 进程。"""
    if self._pm2_process_name:
        subprocess.run(["pm2", "delete", self._pm2_process_name])
        self._pm2_process_name = None
```

PM2 优势：
- 进程崩溃自动重启
- 日志管理（`pm2 logs roundtable-web-xxx`）
- 优雅停止（`pm2 delete`）
- 无需 Python 持有子进程引用

## 12. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 端口冲突 | 自动探测 +1 递增 |
| 文件锁竞争 | flock 排他锁 + 原子写入 |
| Express 进程崩溃 | PM2 自动重启 |
| 微信不支持 SSE | EventSource 检测 + 长轮询降级 |
| nanoid 库不可用 | 降级为 secrets.token_urlsafe(21) |

---

## 待确认项

~~1. Express server.mjs 的启动方式：Python subprocess.Popen 直接 `node server.mjs`，还是用 PM2？~~ → **已确认：使用 PM2**
~~2. discussion.json 的路径约定：是在 `output_path` 同目录，还是单独的 `web_data/` 目录？~~ → **已确认：放在 `output/{discussion_id}/` 目录下**
~~3. 20 并发 SSE 连接是否需要 worker_threads 或 cluster？~~ → **已确认：不需要，单进程轻松处理**

---

> 方案已更新，Boss 确认后开始开发。
