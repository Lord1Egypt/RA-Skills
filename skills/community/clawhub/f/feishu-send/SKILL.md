---
name: feishu-send
description: 飞书发送图片/文件/语音。用 curl 调用飞书 API 发送，比 message 工具更可靠。用于需要发送图片、文件、语音到飞书时触发。
---

# Feishu Send

用 exec + curl 调用飞书 API 发送图片、文件、语音。

## 凭证读取规则

```
优先读：当前 agent 名字对应的 account 配置
防错读：如果读不到，用 main 账户
```

调用时通过环境变量注入 agent 名字：
```bash
AGENT_NAME=main
```

## 统一获取凭证

```bash
# 从 openclaw.json 读取飞书凭证
# 优先读 AGENT_NAME 对应的 account，读不到则用 main 作为 fallback
get_feishu_creds() {
    local agent_name="${AGENT_NAME:-main}"
    local config_file="$HOME/.openclaw/openclaw.json"
    local app_id app_secret

    # 尝试读取当前 agent 的 account
    app_id=$(python3 -c "
import json, sys
c = json.load(open('$config_file'))
accounts = c.get('channels', {}).get('feishu', {}).get('accounts', {})
# 先尝试 agent 名
if '$agent_name' in accounts:
    print(accounts['$agent_name'].get('appId', ''))
elif 'main' in accounts:
    print(accounts['main'].get('appId', ''))
else:
    print('')
" 2>/dev/null)

    app_secret=$(python3 -c "
import json, sys
c = json.load(open('$config_file'))
accounts = c.get('channels', {}).get('feishu', {}).get('accounts', {})
if '$agent_name' in accounts:
    print(accounts['$agent_name'].get('appSecret', ''))
elif 'main' in accounts:
    print(accounts['main'].get('appSecret', ''))
else:
    print('')
" 2>/dev/null)

    echo "$app_id $app_secret"
}

# 用法：读取凭证
read -r APP_ID APP_SECRET <<< "$(get_feishu_creds)"
```

## 统一获取 Token

```bash
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
```

---

## 发送图片

### Step 1: 获取凭证

```bash
read -r APP_ID APP_SECRET <<< "$(get_feishu_creds)"
```

### Step 2: 获取 token

```bash
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
```

### Step 3: 上传图片获取 image_key

```bash
IMAGE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['image_key'])")
```

### Step 4: 发送图片消息

```bash
# 发到群聊
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"

# 发给个人（需要 open_id）
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$OPEN_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"
```

**支持格式**: JPEG, PNG, WEBP, GIF, TIFF, BMP, ICO

---

## 发送文件

### Step 1-2: 同上获取 token

### Step 3: 上传文件获取 file_key

```bash
FILE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=xxx.zip" \
  -F "file=@/path/to/file.zip" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")
```

### Step 4: 发送文件消息

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

---

## 发送语音

### Step 1-2: 同上获取 token

### Step 3: 上传音频获取 file_key

```bash
FILE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=xxx.opus" \
  -F "file=@/path/to/audio.opus" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")
```

### Step 4: 发送语音

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\",\\\"duration\\\":$DURATION}\"}"
```

---

## 完整示例

发送一张图片到飞书群：

```bash
# agent 名字（调用前设置）
AGENT_NAME=main

# Step 1: 读取凭证
read -r APP_ID APP_SECRET <<< "$(get_feishu_creds)"

# Step 2: 获取 token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 3: 上传图片
IMAGE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/tmp/screenshot.png" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['image_key'])")

# Step 4: 发送
CHAT_ID="oc_87d0d49f1f81f9e1b8dd1d5ad5f9ec72"
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"
```

## 注意事项

- ❌ 不要用 `message` 工具的发图片/文件功能 —— 会变成路径或失败
- ✅ 用 exec + curl 方式稳定可靠
- ✅ 调用前设置 `AGENT_NAME` 环境变量，不设置则默认读 main
- ✅ 自动 fallback：如果 AGENT_NAME 对应的 account 不存在，用 main 账户
- ✅ token 有有效期，不用每次操作都重新获取
