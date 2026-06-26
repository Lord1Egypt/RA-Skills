---
name: feishu-files
description: A simple skill send files to feishu.
---

# Skill: 飞书发文件

## 飞书发文件（重要！目前只测试了图片和视频）
OpenClaw的`message`工具目前不能直接在飞书发送本地视频或图像。
**正确方法：用exec工具执行curl调飞书API，分三步：**

### Step 1: 获取tenant_access_token
APP_SECRET=$(python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(c['channels']['feishu']['appSecret'])")
APP_ID=$(python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(c['channels']['feishu']['appId'])")
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
-H 'Content-Type: application/json' \
-d '{"app_id":"'$APP_ID'","app_secret":"'$APP_SECRET'"}' \
| python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

### Step 2: 上传图片获取image_key
IMAGE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
-H "Authorization: Bearer $TOKEN" \
-F "image_type=message" \
-F "image=@/path/to/image.png" \
| python3 -c "import json,sys; print(json.load(sys.stdin)['data']['image_key'])")

### Step 3: 发送图片消息
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"receive_id":"收信人open_id","msg_type":"image","content":"{\"image_key\":\"'$IMAGE_KEY'\"}"}'