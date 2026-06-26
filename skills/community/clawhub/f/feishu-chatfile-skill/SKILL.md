---
name: feishu-send-file
description: 飞书发送本地图片和文件技能。支持向飞书私聊（ou_）和群聊（oc_）发送图片（JPEG/PNG/WEBP 等）及文件（PDF/HTML/ZIP 等）。采用官方推荐的两步法（上传获取 key -> 发送消息），确保内容在飞书客户端正常显示并获得最佳体验。
---

# 飞书发图片 & 文件 Skill

## 强制规则（Feishu channel）

- 任务产出了图片，必须**主动**发送到当前会话，不等用户催促。
- 用户说"发给我/群里看图"时，**必须走脚本**，不能只返回本地路径。
- 发送后记录 `code`、`msg`、`message_id` 用于排查。

## 关键：receive_id 前缀判断

| 前缀 | receive_id_type | 场景 |
|------|-----------------|------|
| `ou_...` | `open_id` | 私聊（单人） |
| `oc_...` | `chat_id` | 群聊 |

**脚本已自动判断，不需要手动传 type。**

## 获取凭据

从 OpenClaw 配置读取 app_id / app_secret：

```bash
grep -A 2 '"feishu"' /root/.openclaw/openclaw.json | grep -E '(appId|appSecret)'
```

从 context inbound_meta 获取 receive_id（去掉 `user:` 前缀保留 `ou_...` 部分）。

## 发送图片

### 方式一：用脚本（推荐）

```bash
python3 skills/feishu-send-file/scripts/send_image.py <image_path> <receive_id> <app_id> <app_secret> [domain]
```

**参数说明：**
- `image_path`：要发送的图片路径（JPEG/PNG/WEBP/GIF/TIFF/BMP/ICO）
- `receive_id`：接收者 ID，支持 `ou_...`（私聊）或 `oc_...`（群聊），脚本自动判断类型
- `app_id`：飞书应用 ID（从 `openclaw.json` 的 `channels.feishu.appId` 读取）
- `app_secret`：飞书应用密钥（从 `openclaw.json` 的 `channels.feishu.appSecret` 读取）
- `domain`：可选，默认 `feishu`；国际版 Lark 传 `lark`

**示例：**

```bash
# 发个人（ou_...）
python3 skills/feishu-send-file/scripts/send_image.py ./chart.png ou_xxx $APP_ID $APP_SECRET

# 发群（oc_...）
python3 skills/feishu-send-file/scripts/send_image.py ./chart.png oc_xxx $APP_ID $APP_SECRET

# 国际版 Lark
python3 skills/feishu-send-file/scripts/send_image.py ./chart.png ou_xxx $APP_ID $APP_SECRET lark
```

**完整路径示例：**

```bash
python3 /root/.openclaw/workspace/skills/feishu-send-file/scripts/send_image.py \
  /root/myfiles/generated-images/demo.png \
  <USER_RECEIVE_ID> \
  <YOUR_APP_ID> \
  <YOUR_APP_SECRET>
```

## 发送文件

### 方式一：用脚本（推荐）

```bash
python3 skills/feishu-send-file/scripts/send_file.py <file_path> <receive_id> <app_id> <app_secret> [file_name]
```

**参数说明：**
- `file_path`：要发送的文件路径（HTML/PDF/ZIP/代码文件等）
- `receive_id`：接收者 ID，支持 `ou_...`（私聊）或 `oc_...`（群聊），脚本自动判断类型
- `app_id`：飞书应用 ID（从 `openclaw.json` 的 `channels.feishu.appId` 读取）
- `app_secret`：飞书应用密钥（从 `openclaw.json` 的 `channels.feishu.appSecret` 读取）
- `file_name`：可选，自定义文件名（不填则用原文件名）

**示例：**

```bash
# 发个人
python3 skills/feishu-send-file/scripts/send_file.py ./report.pdf ou_xxx $APP_ID $APP_SECRET

# 发群
python3 skills/feishu-send-file/scripts/send_file.py ./report.pdf oc_xxx $APP_ID $APP_SECRET
```

**完整路径示例：**

```bash
python3 /root/.openclaw/workspace/skills/feishu-send-file/scripts/send_file.py \
  /root/myfiles/report.html \
  <USER_RECEIVE_ID> \
  <YOUR_APP_ID> \
  <YOUR_APP_SECRET> \
  report.html
```

### 方式二：手动两步

**Step 1 - 上传文件：**
```bash
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=<文件名>" \
  -F "file=@<文件路径>" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")
```

**Step 2 - 发送消息：**
```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"<OPEN_ID>\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## 脚本底层逻辑说明

### 发送原理

飞书消息链路中，发送文件或图片的最佳方式是采用“两步法”：
1. **先上传**：将本地文件上传到 `im/v1/files` 或 `im/v1/images`，获取持久化的 `file_key` 或 `image_key`。
2. **后发送**：调用 `im/v1/messages` 接口，指定 `msg_type` 为 `file` 或 `image` 并携带对应的 Key。

直接传递本地路径字符串到消息接口通常会导致客户端只显示路径文本。本脚本通过自动化这两步流程，确保用户在飞书里实际看到图片本体或可预览的文件。

### 普通文件 vs 图片的链路区别

- **普通文件**：`im/v1/files` -> `file_key` -> `msg_type=file`
- **图片**：`im/v1/images` -> `image_key` -> `msg_type=image`

脚本会自动处理这些差异。

## 排查

- 发送失败先看 `code` / `msg`
- 群发失败检查：机器人已入群 + send_message 权限 + 使用正确的 `oc_` chat_id
- `oc_...` 误当 `open_id` 发必定报错
- **不要把本地路径回显误判为发送成功**
- 飞书 file_type 用 `stream` 适用于所有普通文件类型
