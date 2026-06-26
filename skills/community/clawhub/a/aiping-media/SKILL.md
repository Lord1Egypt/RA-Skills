---
name: aiping-media
description: AIPing 媒体生成技能，支持图片生成和视频生成。生成后自动下载到本地，优先通过飞书发送原生图片/视频消息，CDN 链接作为备选。当用户要求生成图片、生成视频、图片生成、视频制作、AI绘图、文生图、文生视频时自动触发。
primaryEnv: AIPING_API_KEY
requires:
  env:
    - AIPING_API_KEY
    - FEISHU_APP_ID
    - FEISHU_APP_SECRET
---

# AIPing Media Skill

通过 AIPing API 生成图片和视频，完整流程：**生成 → 本地下载 → 飞书原生发送**，CDN 链接作为备选。

## 完整工作流

```
生成图片/视频 → 自动下载到本地 (/tmp/) → 上传飞书 → 发送原生消息
                                              ↓ 失败
                                         返回 CDN 链接
```

---

## 快速上手（新用户从零到跑通）

### 第一步：安装技能

```bash
clawhub install aiping-media
```

### 第二步：配置环境变量

在 `~/.openclaw/openclaw.json` 的 `env` 块中添加三个变量。推荐用 CLI 写入，避免手动编辑 JSON：

```bash
openclaw config set env.AIPING_API_KEY   "你的AIPing Key"
openclaw config set env.FEISHU_APP_ID    "cli_xxxxxxxxxxxxxxxx"
openclaw config set env.FEISHU_APP_SECRET "你的飞书AppSecret"
```

> **获取飞书 AppID / AppSecret**：飞书开放平台 → 你的应用 → 凭证与基础信息

验证写入成功：

```bash
openclaw config get env.AIPING_API_KEY
openclaw config get env.FEISHU_APP_ID
```

### 第三步：重启 Gateway（让 env 变量生效）

```bash
openclaw gateway restart
```

### 第四步：获取自己的飞书 open_id

以下命令自动用配置中的 AppID/Secret 获取 token，再查询你自己的 open_id（把 `你的手机号或邮箱` 替换成实际值）：

```bash
# 获取 token
TOKEN=$(python3 -c "
import requests, json
with open('$(echo ~/.openclaw/openclaw.json)') as f:
    cfg = json.load(f)
env = cfg['env']
r = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': env['FEISHU_APP_ID'], 'app_secret': env['FEISHU_APP_SECRET']})
print(r.json()['tenant_access_token'])
")

# 按手机号查 open_id（换成你的手机号，含国家码如 +8613800138000）
curl -s "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mobiles": ["你的手机号"]}' | python3 -m json.tool
```

记下 `open_id`（格式如 `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`），后续测试用。

### 第五步：一键测试（图片生成 + 飞书发送）

```bash
SKILL_DIR=~/.openclaw/workspace/skills/aiping-media

# 生成图片（默认模型 Doubao-Seedream-5.0-lite，~5秒）
IMG_JSON=$(python3 $SKILL_DIR/scripts/generate_image.py "赛博朋克城市夜景，霓虹灯，超写实")
LOCAL_PATH=$(echo $IMG_JSON | python3 -c "import sys,json; print(json.load(sys.stdin)['local_path'])")
echo "图片已下载到: $LOCAL_PATH"

# 发送到飞书（替换 open_id）
python3 $SKILL_DIR/scripts/send_feishu.py image ou_你的open_id $LOCAL_PATH
```

输出 `"success": true` 即代表完整链路跑通。

### 第六步：测试视频生成

```bash
SKILL_DIR=~/.openclaw/workspace/skills/aiping-media

# 提交任务（视频生成通常需要 1~3 分钟）
TASK_JSON=$(python3 $SKILL_DIR/scripts/generate_video.py submit Kling-V3-Omni "一只橘猫在草地上打滚，阳光明媚" 5 pro 16:9)
TASK_ID=$(echo $TASK_JSON | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task ID: $TASK_ID"

# 等待完成并自动下载（轮询，最长等 5 分钟）
VIDEO_JSON=$(python3 $SKILL_DIR/scripts/generate_video.py wait $TASK_ID)
VIDEO_PATH=$(echo $VIDEO_JSON | python3 -c "import sys,json; print(json.load(sys.stdin).get('local_path',''))")
echo "视频已下载到: $VIDEO_PATH"

# 发送到飞书（群聊用 chat_id）
python3 $SKILL_DIR/scripts/send_feishu.py video oc_群聊ID $VIDEO_PATH chat_id
```

---

## 在 Agent 代码中调用

### 图片生成 + 飞书发送

```python
from scripts.generate_image import generate_image
from scripts.send_feishu import send_image

# 1. 生成（自动下载到本地）
img = generate_image(
    model="Kling-V1",
    prompt="未来城市夜景，赛博朋克风格",
    negative_prompt="低质量，模糊"
)
local_path = img.get("local_path")  # 自动下载路径

# 2. 发送飞书
if local_path:
    # 发送给用户（默认 open_id）
    result = send_image(token=None, receive_id="ou_xxx", source=local_path)
    # 或发送到群聊（指定 chat_id）
    result = send_image(token=None, receive_id="oc_xxx", source=local_path, receive_id_type="chat_id")
    if result.get("success"):
        print(f"飞书 image_key: {result.get('image_key')}")
    else:
        print(f"失败: {result.get('error')}")
        print(f"CDN链接: {result.get('cdn_url')}")
```

### 视频生成 + 飞书发送

```python
from scripts.generate_video import generate_video, wait_for_video
from scripts.send_feishu import send_video

# 1. 提交任务
video = generate_video(
    model="Kling-V3-Omni",
    prompt="一只猫咪在草地上玩耍",
    seconds=5,
    mode="pro",
    aspect_ratio="1:1"
)
task_id = video["id"]

# 2. 等待完成（自动下载）
result = wait_for_video(task_id)
local_path = result.get("local_path")

# 3. 发送到群聊
if local_path:
    result = send_video(token=None, receive_id="oc_xxx", source=local_path, receive_id_type="chat_id")
```

---

## 推荐模型

### 图片
| 模型 | 说明 |
|------|------|
| `Doubao-Seedream-5.0-lite` | 通用文生图，支持垫图（默认） |
| `Kling-V1` | 高质量，速度快 |
| `HunyuanImage-3.0` | 腾讯混元 |

### 视频
| 模型 | mode | aspect_ratio | 说明 |
|------|------|---------------|------|
| `Kling-V3-Omni` | pro/std | 16:9, 9:16, 1:1 | 最新全能版，推荐 |
| `Kling-V2.6` | std | 16:9, 9:16, 1:1 | 稳定版 |

---

## 脚本命令行用法

### generate_image.py
```bash
python3 scripts/generate_image.py <prompt> [model] [negative_prompt] [image_url] [aspect_ratio] [nodownload]
```

### generate_video.py
```bash
# 提交任务
python3 scripts/generate_video.py submit <model> <prompt> [seconds] [mode] [aspect_ratio]
# 等待完成（自动下载）
python3 scripts/generate_video.py wait <task_id>
# 查询状态
python3 scripts/generate_video.py query <task_id>
```

### send_feishu.py
```bash
# 图片（本地文件或 CDN URL）
python3 scripts/send_feishu.py image <receive_id> <file_or_url> [receive_id_type]
# 视频（本地文件或 CDN URL）
python3 scripts/send_feishu.py video <receive_id> <file_or_url> [receive_id_type]
```

**关键参数 `receive_id_type`**（默认 `open_id`，易踩坑！）：

| receive_id_type | 适用场景 | receive_id 示例 |
|-----------------|---------|----------------|
| `open_id` | 发送给**单个用户** | `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `chat_id` | 发送到**群聊** | `oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

> ⚠️ **群聊必须用 `chat_id`**，不能拿用户的 open_id 发到群里，否则返回 `400 Bad Request`

**示例：**
```bash
# 发送给用户（默认 open_id）
python3 scripts/send_feishu.py image ou_xxxxxxxx /tmp/a.jpg

# 发送到群聊（指定 chat_id）
python3 scripts/send_feishu.py image oc_xxxxxxxx /tmp/a.jpg chat_id
```

---

## 飞书上传接口详解（踩坑经验汇总）

### 图片上传 vs 视频上传（对比）

| | 图片 | 视频 |
|--|------|------|
| **上传接口** | `POST /im/v1/images` | `POST /im/v1/files` |
| **参数传递方式** | `multipart/form-data`（`-F`） | `multipart/form-data`（`-F`） |
| **必需参数** | `image_type=message` | `file_type=mp4` + `file_name=xxx.mp4` |
| **返回值 key** | `image_key` | `file_key` |
| **发送时 msg_type** | `image` | `media` |
| **content 格式** | `{"image_key": "xxx"}` | `{"file_key": "xxx", "type": "video"}` |

### 完整 curl 示例（图片）

```bash
# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['tenant_access_token'])")

# 2. 上传图片
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/tmp/image.jpg" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['image_key'])")

# 3. 发送图片
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\": \"oc_xxx\", \"msg_type\": \"image\", \"content\": \"{\\"image_key\\": \\"$IMAGE_KEY\\"}\"}"
```

### 完整 curl 示例（视频）

```bash
# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['tenant_access_token'])")

# 2. 上传视频（注意：file_type 必须是 "mp4"，不是 "video/mp4"！）
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=mp4" \
  -F "file_name=video.mp4" \
  -F "file=@/tmp/video.mp4" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['file_key'])")

# 3. 发送视频（msg_type 是 "media"，content 里 type 是 "video"）
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\": \"oc_xxx\", \"msg_type\": \"media\", \"content\": \"{\\"file_key\\": \\"$FILE_KEY\\", \\"type\\": \\"video\\"}\"}"
```

### 飞书上传最容易踩的坑

| 错误写法 | 正确写法 | 说明 |
|---------|---------|------|
| 上传图片设 `Content-Type: application/json` | 不要设 Content-Type，让 curl 自动生成 | multipart/form-data 不能手动设 Content-Type |
| `file_type=video/mp4` | `file_type=mp4` | 文件类型是枚举值，不是 MIME type！ |
| 上传视频缺少 `file_name` | 必须加 `file_name=xxx.mp4` | 否则报 234001 参数错误 |
| 视频发送用 `msg_type=video` | 用 `msg_type=media` | 视频/音频/文件都是 media 类型 |
| `content: {"video_key": "xxx"}` | `content: {"file_key": "xxx", "type": "video"}` | 字段名是 `file_key`，不是 `video_key` |

---

## 注意事项

1. **env 变量必须配置**：技能脚本从 `AIPING_API_KEY` / `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 读取凭证，未配置时调用函数会抛 `EnvironmentError`
2. **重启 gateway 后才生效**：修改 `openclaw.json` 的 env 块后必须 `openclaw gateway restart`
3. **本地文件限制 /tmp/**：`send_feishu.py` 只允许读取 `/tmp/` 下的本地文件，生成脚本默认也写入 `/tmp/`
4. **自动 MIME 检测**：根据文件扩展名自动识别 PNG/JPEG/GIF/MP4
5. **视频生成需要耐心**：视频任务提交后 status 为 `queued`，需要等待 1~3 分钟才能完成，用 `wait` 命令轮询查询
6. **上传接口不能混用**：图片必须用 `/im/v1/images`，视频必须用 `/im/v1/files`，两者接口不同

## 常见错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `400 Bad Request /im/v1/messages` | `receive_id_type` 与 `receive_id` 不匹配（如群聊用了 open_id） | 群聊传 `chat_id` + `receive_id_type="chat_id"`，个人用 `open_id` |
| `飞书错误码 234001` | 参数错误，上传接口参数格式不对 | 对照上方「最容易踩的坑」检查：file_type 枚举值、file_name 是否传入、Content-Type 是否误设 |
| `飞书错误码 230001` | 缺少 `im:resource` 权限 | 飞书开放平台 → 权限管理 → 开通 `im:resource` → 重新发布 |
| `飞书错误码 99991663` | `tenant_access_token` 过期 | token 会自动续期，若仍失败重启 gateway |
| `本地文件路径必须在 /tmp/` | 读取了 `/tmp/` 以外的文件 | 只传 `/tmp/` 下的文件路径 |
| `image_key / file_key 无效` | 图片上传和发送用了不同的 token 或应用 | 确保同一应用内完成上传和发送 |
| 视频发送成功但群里看不到 | `file_key` 与 `file_name` 来自不同文件 | 每次发送都要重新上传，获取新的 file_key |
| AIPing 返回 `503 暂无可用服务商` | 视频生成模型不支持 chat/completions 接口 | 视频生成必须用 `/api/v1/videos` 端点，不是 `/chat/completions` |
