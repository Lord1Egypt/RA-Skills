---
name: egatee-chat-summary
description: 拉取IM账号近1-7天聊天记录并生成汇总分析
metadata:
  {
    "openclaw": {
      "emoji": "💬",
      "primaryEnv": "EGATEE_CHAT_API_KEY",
      "requires": {
        "env": [
          "EGATEE_CHAT_API_KEY"
        ]
      }
    }
  }
---

# Egatee Chat Summary Skill

该 Skill 用于：

1. 调用 notify 开放接口 `POST /api/notify/im/openapi/getChatHistoryByApiKey`（`X-API-Key` 鉴权）拉取绑定 IM 账号近 1~7 天聊天记录
2. 输出 `meta` 与按对端聚合的 `peer_summaries`（含 `peerNick` / `peerAvatar` 等）

**未配置 `EGATEE_CHAT_API_KEY` 时**：`tool.py` 会报错并提示在 OpenClaw 中为该 Skill 配置该环境变量。

## 输入参数

- `day`: 查询最近天数，范围 1~7，默认 1
- `size`: 每页条数，默认 100
- `max_pages`: 最大分页页数，默认 20

## 依赖环境变量

- **`EGATEE_CHAT_API_KEY`（必填）**：OpenClaw 中需在 Skill 环境变量里配置；`uat_` 前缀走 UAT 网关，`prod_` 等走生产网关（详见 `tool.py` 推断逻辑）。
- `EGATEE_NOTIFY_BASE_URL`（可选）：显式指定网关根地址；不填则按 apiKey 前缀自动选择 `http://api.uat.egatee.net` 或 `https://api.egatee.com`。
- `EGATEE_FROM_ACCOUNT`（可选）：仅作 `meta.imAccount` 兜底显示。
- `EGATEE_AUTH_TOKEN`（可选）：当前 openapi 接口不使用，保留兼容。
- `EGATEE_DEBUG` / `EGATEE_REQUEST_ID`（可选）：调试与链路追踪。

## 运行

```bash
python tool.py --day 7 --timeout 60
```
