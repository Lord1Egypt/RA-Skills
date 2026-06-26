---
name: agentic-engineering/composing
description: Agentic Engineering 分支：创作。DeepSeek thinker → MiniMax maker 双模型管线。触发：歌曲创作、文案生成、需要深度推理+多媒体输出的一切任务。
---
---

# DeepSeek-MiniMax 双模型协作团队

**架构：** DeepSeek_V4_Flash（思想空间构建）→ MiniMax_M2.7（具体实现）

## AutoGen Studio 团队

| 属性 | 值 |
|------|-----|
| 团队ID | 30 |
| 名称 | `DeepSeek_MiniMax_Duo` |
| 类型 | SelectorGroupChat |
| 数据库 | `/home/hongliang/.autogenstudio/*.db` |
| MCP脚本 | `/home/hongliang/.openclaw/workspace/autogen/mcp_autogen_studio_v2.py` |

## 两个 Agent

### DeepSeek_Thinker（思想空间构建）
- **模型：** DeepSeek V4 Flash（`deepseek-v4-flash`）
- **API 格式：** Anthropic 兼容端点 `https://api.deepseek.com/anthropic`
- **API Key：** `sk-a94a…8ce3`
- **职责：** 深层推理、构建思想框架和逻辑链条
- **系统提示：** 只负责"想"，输出推理链和结论，不执行具体操作

### MiniMax_Maker（具体实现）
- **模型：** MiniMax-M2.7-highspeed
- **API 格式：** Anthropic 兼容端点 `https://api.minimaxi.com/anthropic`
- **API Key：** `sk-cp-…I35Y`
- **职责：** 接收推理结果，生成文本/图片/音乐等多媒体输出
- **系统提示：** 关注"实现"，不代替 DeepSeek_Thinker 推理

## 调用方式

### 通过 MCP 工具（OpenClaw 内）
```python
# 启动团队
autogen-studio__chat_start(team_id=30, message="你的问题")

# 查询结果
autogen-studio__chat_result(task_id="xxx")

# 需要用户输入时
autogen-studio__send_input(task_id="xxx", response="你的回答")
```

### 直接通过 API（Python）
```python
import asyncio, httpx, json, websockets

TOKEN = "eyJhbG…tpzo"  # AutoGen Studio JWT
UID = "205283334"
h = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}

async with httpx.AsyncClient() as c:
    # 创建 session & run
    r = await c.post("http://localhost:8081/api/sessions/", headers=h,
        json={"user_id": UID, "team_id": 30, "name": "session_name"})
    sid = r.json()["data"]["id"]
    r = await c.post("http://localhost:8081/api/runs/", headers=h,
        json={"session_id": sid, "user_id": UID})
    rid = r.json()["data"]["run_id"]

    # 获取团队配置
    r = await c.get("http://localhost:8081/api/teams/30", headers=h,
        params={"user_id": UID})
    comp = r.json()["data"]["component"]

    # WebSocket 连接并启动
    ws_url = f"ws://localhost:8081/api/ws/runs/{rid}?token={TOKEN}"
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        await ws.send(json.dumps({
            "type": "start", "task": "你的问题",
            "files": [], "team_config": comp
        }))
        # 接收消息...
```

## 关键配置

### DeepSeek API 端点（OpenClaw Provider）
```json
{
  "provider": "deepseek-official",
  "baseUrl": "https://api.deepseek.com",
  "apiKey": "sk-a94…8ce3",
  "api": "openai-completions",
  "models": [
    {"id": "deepseek-v4-flash", "name": "DeepSeek V4 Flash", ...},
    {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro", ...}
  ]
}
```

### AutoGen Studio 启动
```bash
autogenstudio ui --port 8081 --host 0.0.0.0 \
  --auth-config /home/hongliang/.autogenstudio/config/auth.yaml
```

## 已知问题

1. **Gateway 重启会杀掉 autogenstudio** — 需要用 `setsid` 独立启动
2. **MCP server 在 gateway 重启后自动拉起** — 但 autogenstudio 需要手动重启
3. **DeepSeek API 需要 Anthropic 格式** — OpenAI 格式下 `content` 为空字符串
4. **团队配置在 DB 中** — 修改后用 `UPDATE team SET component=? WHERE id=30`
5. **Auth 配置** — 在 `/home/hongliang/.autogenstudio/config/auth.yaml`
