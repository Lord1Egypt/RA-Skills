# feishu-axiang-send-image - 飞书图片发送技能

## 技能说明

飞书图片发送技能，使用自有飞书应用配置发送图片到飞书聊天（个人或群聊）。

**特点：**
- 🦞 专属配置 - 使用自有的飞书应用配置
- ⚡ 开箱即用 - 无需配置环境变量
- 🎯 简化调用 - 只需提供图片路径和目标用户

## 核心配置

**飞书应用信息（硬编码在脚本中）：**
```json
{
  "appId": "cli_XXX",
  "appSecret": "XXX",
  "accountId": "XXX"
}
```

**允许发送的用户：**
- 在 `feishu-axiang-allowFrom.json` 中配置允许的用户列表

## 触发词

- 发送图片到飞书
- 发图给我
- axiang send image

## 核心原理

**两步法：**
1. 调用 `im/v1/images` API 上传图片到飞书 → 获取 `image_key`
2. 调用 `im/v1/messages` API 发送图片消息 → 获取 `message_id`

## 使用方法

### 方法 1：命令行调用

```bash
# 发送图片到个人（默认）
python scripts/send.py --file-path "C:\path\to\image.png"

# 发送到指定用户
python scripts/send.py --file-path "C:\path\to\image.png" --target "ou_xxxxx"

# 发送到群聊
python scripts/send.py --file-path "C:\path\to\image.png" --target "oc_xxxxx" --target-type chat_id
```

### 方法 2：Python API 调用

```python
from scripts.send import send_image_to_feishu

# 发送到默认用户
result = send_image_to_feishu("image.png")

# 发送到指定用户
result = send_image_to_feishu("image.png", target="ou_xxxxx", target_type="open_id")
```

## 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--file-path` | ✅ | - | 本地图片文件路径 |
| `--target` | ❌ | 配置中的默认值 | 目标用户 open_id 或群聊 chat_id |
| `--target-type` | ❌ | `open_id` | 目标类型（open_id/chat_id） |

## 输出示例

```
Image Sender
   File: C:\Users\your_username\.openclaw\workspace\image.png
   Target: ou_xxxxx (open_id)
   App: cli_XXX (accountId)

Step 1: Get tenant_access_token
   OK Token obtained

Step 2: Upload image to Feishu
   OK Upload success, image_key: img_v3_xxx

Step 3: Send image message
   OK Send success, message_id: om_xxx

Image sent successfully!
```

## 支持格式

| 格式 | 支持 | 说明 |
|------|------|------|
| PNG | ✅ | 推荐格式 |
| JPG/JPEG | ✅ | 支持 |
| GIF | ✅ | 支持（会自动转换） |
| WEBP | ✅ | 支持 |

## 限制

- 单张图片最大 20MB
- 仅支持配置允许的用户
- 需要网络连接

## 故障排查

### 错误：open_id cross app

**原因：** 目标用户不在允许列表中

**解决：** 
1. 检查目标 open_id 是否正确
2. 在 `feishu-axiang-allowFrom.json` 中添加用户

### 错误：file not found

**原因：** 图片路径不存在

**解决：** 检查文件路径是否正确，使用绝对路径

### 错误：tenant_access_token 获取失败

**原因：** AppID 或 AppSecret 错误

**解决：** 检查脚本中的配置是否正确

## 相关文件

- `scripts/send.py` - 主发送脚本
- `feishu-axiang-allowFrom.json` - 允许发送的用户列表（需自行配置）

## 版本历史

- **v1.0** - 初始版本，专属配置

## 安装后配置

1. 编辑 `scripts/send.py`，填入你自己的飞书应用配置：
   - `app_id`: 你的飞书应用 AppID
   - `app_secret`: 你的飞书应用 AppSecret
   - `default_target`: 默认发送目标用户

2. 创建 `feishu-axiang-allowFrom.json` 文件，配置允许发送的用户列表

## 注意事项

⚠️ **安全提示：**
- 不要将包含真实 AppID/AppSecret 的脚本上传到公开仓库
- 生产环境建议使用环境变量或配置文件管理敏感信息
- 定期检查允许发送的用户列表
