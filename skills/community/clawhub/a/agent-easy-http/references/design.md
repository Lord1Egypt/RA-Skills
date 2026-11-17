# agent-easy-http 设计文档

## 目录
1. 架构概述
2. 与 skill-to-http 对比
3. 关键设计决策
4. 扩展路径

---

## 1. 架构概述

```
外部系统
    │ POST /skills/{name}/run
    ▼
agent-easy-http (FastAPI, ~300行)
    │
    ├─ 1. 生成 job_id，注册 asyncio.Event
    ├─ 2. sessions_send → Agent 主会话
    │       prompt 包含：Skill名、SKILL.md内容、message、params、callback_url
    │
    │  [Agent 收到后]
    │  └─ sessions_spawn → sub-agent 执行 Skill
    │       ↓ 完成
    │       POST /callback/{job_id} {result: "..."}
    │
    ├─ 3. Event.set() 解锁同步等待
    └─ 4. 返回结果给调用方
```

### 数据流时序

```
t=0ms    调用方 POST /skills/work-summary/run
t=1ms    生成 job_id，注册 Event，发 sessions_send
t=~50ms  Agent 主会话收到消息
t=~100ms Agent sessions_spawn sub-agent
t=~4s    sub-agent 启动完毕，开始执行
t=~20s   sub-agent 完成 → POST /callback/{job_id}
t=~20s   Event.set() → 返回结果给调用方
```

---

## 2. 与 skill-to-http 对比

| 维度 | agent-easy-http | skill-to-http |
|------|----------------|---------------|
| **代码量** | ~300行 | ~7000行 |
| **执行引擎** | Agent 自身 | skill_runner（5种executor） |
| **并发** | ✅（每个请求独立sub-agent） | ✅（线程池） |
| **执行器降级** | ❌ 绑定 OpenClaw | ✅ CC/Codex/LLM 降级 |
| **极速模式** | ❌ 每次冷启动 ~4s | ✅ 复用已有 Agent |
| **依赖 Agent 在线** | ✅ 必须 | ❌ 独立进程 |
| **管理控制台** | ❌ 无 | ✅ Web UI |
| **历史记录** | ❌ 内存 TTL 1h | ✅ SQLite 持久化 |
| **运维复杂度** | ✅ 低 | ❌ 高 |
| **适用场景** | 开发/内部工具 | 生产/多环境 |

---

## 3. 关键设计决策

### 3.1 回调方式：webhook vs sessions_send

选择 **webhook 回调**，原因：

- sessions_send 是阻塞调用，长任务会占用 HTTP 连接
- webhook 使同步和异步接口实现都自然
- 超时语义清晰（job TTL 独立控制）
- 同机部署时回调地址 = 127.0.0.1:PORT，无网络问题

### 3.2 Job 存储：内存 vs SQLite

当前：**内存 + TTL 1h**

- 轻量，无额外依赖
- 服务重启后 job 丢失（acceptable，异步场景需注意）
- 未来可选：接入 history_store.py（复用 skill-to-http 实现）

### 3.3 Skill 发现：静态扫描

启动时一次性扫描所有已安装 Skill，通过 `/admin/reload` 手动刷新。

不做动态监听（inotify），避免额外依赖。

---

## 4. 扩展路径

### v1.1：通用 /run 入口

```python
@app.post("/run")
async def run_any(req: GeneralRunRequest):
    # message 直接透传给 Agent，不注入 SKILL.md
    # Agent 自己判断用什么工具/Skill
```

### v1.2：SQLite 历史记录

复用 skill-to-http 的 history_store.py。

### v1.3：Server-Sent Events 进度推送

```
GET /jobs/{job_id}/stream → EventSource
Agent 执行中可推送进度：data: {"status": "running", "progress": "..."}
```

### v2：支持非 Skill 任务

```
POST /run {"message": "查一下本月各BU费用，发给财务组"}
→ Agent 自行决策：调 SQL → 整理 → 发 Hi 消息
```
