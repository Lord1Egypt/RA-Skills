# feishu-send-image

在飞书聊天中发送原生图片消息的 OpenClaw 技能。

## 解决什么问题

OpenClaw 内置的 `message` 工具在飞书中发送图片时，无论使用 `filePath`、`media` 还是 `buffer` 参数，都只会生成文件附件，而非可直接预览的图片消息。

本技能通过直接调用飞书 Bot API，实现真正的图片消息发送。

## 使用场景

- 发送 AI 生成的图表（股票走势、数据分析图等）
- 发送截图、处理后的图片
- 任何需要在飞书对话中直接展示图片的场景

## 工作原理

三步完成图片发送：
1. 获取飞书 `tenant_access_token`
2. 上传图片获取 `image_key`
3. 发送 `image` 类型消息

## 使用方法

```bash
bash scripts/feishu_send_image.sh <图片路径> <接收者ID> <app_id> <app_secret> [id类型]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `图片路径` | 本地图片文件路径，支持 png/jpg/gif/webp |
| `接收者ID` | 飞书用户的 `open_id` 或群聊的 `chat_id` |
| `app_id` | 飞书应用 App ID |
| `app_secret` | 飞书应用 App Secret |
| `id类型` | 可选，`open_id`（默认）或 `chat_id` |

### 示例

```bash
# 发送图片给用户
bash scripts/feishu_send_image.sh /tmp/chart.png ou_xxxxx cli_xxxxx secret_xxxxx

# 发送图片到群聊
bash scripts/feishu_send_image.sh /tmp/chart.png oc_xxxxx cli_xxxxx secret_xxxxx chat_id
```

## 凭证获取

App ID 和 App Secret 可从 OpenClaw 配置文件中获取：

```
~/.openclaw/openclaw.json → channels.feishu.accounts.default.appId / appSecret
```

接收者 `open_id` 来自飞书消息的 `sender_id` 字段。

## 前置条件

- 飞书自建应用已创建并启用机器人能力
- 应用已获取 `im:message:send_as_bot`（发送消息）和 `im:resource`（上传图片）权限
- 系统已安装 `curl` 和 `python3`

## 安装

```bash
openclaw skill install feishu-send-image.skill
```

或手动将 `feishu-send-image/` 目录放入 `~/.openclaw/workspace/skills/` 下。
