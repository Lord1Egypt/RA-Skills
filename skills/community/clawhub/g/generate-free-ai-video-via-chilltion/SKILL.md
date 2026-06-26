---
name: chilltion
description: 通过 Chilltion（轻现AI）API 生成 AI 视频。当用户想要从文本提示创建短视频、查询 Chilltion 会话/积分/费用/余额，或调用 Chilltion 的任意 /api 端点时使用。触发词包括"做个视频"、"生成视频"、"create a video"、"chilltion"、"查会话/积分/余额"。支持自主（单次）和交互（多轮）两种模式；在 scripts/*.sh 下提供每个端点的 shell 脚本，共享统一的 env 校验辅助函数。
---

# 轻现AI 视频接口

所有操作通过 `scripts/` 目录下的 shell 脚本完成。每个脚本都会加载 `scripts/_common.sh`，该文件将 `CHILLTION_BASE_URL` 默认设为 `https://chilltion.com`，若缺少 `CHILLTION_API_KEY` 则以退出码 2 终止。

## 必需环境变量

```
CHILLTION_BASE_URL   # 默认 https://chilltion.com；开发时可传入调试地址
CHILLTION_API_KEY    # ct_... 格式的密钥，在 Web 应用的 /keys 页面创建
CHILLTION_INSECURE=1 # 可选，内网环境跳过 TLS 验证（需在脚本中添加 -k 参数）
```

如果用户尚未提供密钥，请在调用前询问。获取密钥的方法：登录 `https://chilltion.com`，进入 **设置 → API 密钥**，创建新密钥（以 `ct_` 开头）。

## 会话详情响应字段

`GET /api/sessions/{id}` 返回：

| 字段 | 类型 | 说明 |
|---|---|---|
| `video_url` | string | 最终合成视频的 OSS 地址；未生成时为空 |
| `chat_url` | string | 前端对话页面地址，如 `https://chilltion.com/chat/{session_id}` |

## 脚本列表

| 脚本 | 参数 | 端点 |
|---|---|---|
| `scripts/create_session.sh` | `[mode] [message]` | `POST /api/sessions` — `mode` 默认为 `autonomous`；传入 `message` 后后端会立即开始处理。 |
| `scripts/stream.sh` | `<session_id> [from_seq]` | `GET /api/chat/{id}/stream`（SSE；推送 `phase_change` / `progress` / `preview_ready` / `video_ready` / `done` / `error`）。 |
| `scripts/send_message.sh` | `<session_id> <content>` | `POST /api/chat/{id}/message` — 交互模式下的后续对话。 |
| `scripts/list_sessions.sh` | `[offset] [limit]` | `GET /api/sessions` |
| `scripts/session_detail.sh` | `<session_id>` | `GET /api/sessions/{id}` — 返回 `video_url`（OSS）和 `chat_url`（前端页面）。 |
| `scripts/balance.sh` | – | `GET /api/credits/balance` |
| `scripts/session_cost.sh` | `<session_id>` | `GET /api/credits/session-cost/{id}` |
| `scripts/credit_log.sh` | `[offset] [limit] [start] [end]` | `GET /api/credits/log`（日期格式 `YYYY-MM-DD`） |

所有脚本输出原始 JSON 响应。可使用 `jq`（或其他 JSON 解析器）提取字段。

## 构建提示词

自主模式端到端运行，无需额外输入 — 将所有信息写入一条消息：
- 主题、目标受众、时长（30秒/60秒/90秒）、风格、章节数（2–6）、语言（默认 zh-CN）。

交互模式适用于需要迭代调整的场景：先创建空会话（`scripts/create_session.sh interactive`），再通过 `scripts/send_message.sh` 逐轮发送消息。

## 自主模式端到端流程

```bash
# 1) 一次调用创建会话 + 发送首条消息
sid=$(scripts/create_session.sh autonomous "做个 60 秒介绍光合作用的科普视频，3 章节，中文" | jq -r .session_id)

# 2) 流式监听直到 video_ready，然后退出
scripts/stream.sh "$sid" 0 | while IFS= read -r line; do
  case "$line" in
    data:*)
      json="${line#data: }"
      type=$(printf '%s' "$json" | jq -r '.type // empty')
      case "$type" in
        progress)     printf '%s\n' "$json" | jq -r '"[progress] \(.progress) \(.message // "")"' ;;
        phase_change) printf '%s\n' "$json" | jq -r '"[phase] \(.from) -> \(.to)"' ;;
        video_ready)  url=$(printf '%s' "$json" | jq -r '.url // .data.url'); echo "VIDEO: $url"; break ;;
        error)        printf '%s\n' "$json" | jq -r '"[error] \(.message)"' >&2; exit 1 ;;
      esac
      ;;
  esac
done
```

`progress` 事件的 `progress` 字段通常为 0–100，但偶尔可能为 0–1；展示前请做归一化处理。自主模式中首个 `video_ready` 即为交付物；后续的（修订阶段）是修改后的版本。

## 错误码

| 状态码 | 含义 |
|---|---|
| 401 | 密钥无效或已过期 — 请用户核实 `ct_` 密钥 |
| 402 | 积分不足 — 返回 `detail.balance` 和 `detail.required` |
| 404 | 会话不存在 — 需重新创建 |
| 409 | 会话正忙 — 请先连接 SSE 观察进度 |

## SSE 事件参考

每行格式为 `data: {json}`，包含顶层 `seq` 和 `type`。主要事件类型：

- `phase_change` — `from`、`to`（`requirements` → `creative_planning` → `designing` → `producing` → `revision` → `complete`）
- `progress` — `message`、`progress`（0–100，偶尔 0–1）
- `preview_ready` / `preview_append` — 章节缩略图
- `video_ready` — 最终视频地址，位于 `url`（或 `data.url`）
- `done` — 流结束
- `error` — `message`
