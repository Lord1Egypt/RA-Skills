# feishu-axiang-send-image

🦞 飞书图片发送技能 - 使用自有飞书应用配置发送图片到飞书聊天

## 功能特点

- ✅ 支持发送 PNG/JPG/GIF/WEBP 格式图片
- ✅ 两步流程：上传图片获取 image_key → 发送图片消息
- ✅ 支持个人聊天和群聊
- ✅ 开箱即用，无需配置环境变量

## 安装

```bash
clawhub install feishu-axiang-send-image
```

## 使用前配置

**⚠️ 重要：使用前必须配置飞书应用信息！**

1. 编辑 `scripts/send.py`，修改以下配置：

```python
APP_CONFIG = {
    "app_id": "cli_XXX",  # 替换为你的飞书应用 AppID
    "app_secret": "XXX",  # 替换为你的飞书应用 AppSecret
    "default_target": "ou_XXX",  # 替换为默认发送目标用户的 open_id
    "account_name": "your_account"  # 你的账号名称
}
```

2. （可选）创建允许发送的用户列表文件

## 使用方法

### 命令行调用

```bash
# 发送到默认用户
python scripts/send.py --file-path "C:\path\to\image.png"

# 发送到指定用户
python scripts/send.py --file-path "image.png" --target "ou_xxxxx"

# 发送到群聊
python scripts/send.py --file-path "image.png" --target "oc_xxxxx" --target-type chat_id
```

### Python API 调用

```python
from scripts.send import send_image_to_feishu

# 发送到默认用户
result = send_image_to_feishu("image.png")
print(f"Message ID: {result['message_id']}")

# 发送到指定用户
result = send_image_to_feishu(
    "image.png",
    target="ou_xxxxx",
    target_type="open_id"
)
```

## 完整文档

详细文档请查看 `SKILL.md` 文件。

## 安全提示

- ⚠️ 不要将包含真实 AppID/AppSecret 的脚本上传到公开仓库
- ⚠️ 生产环境建议使用环境变量或配置文件管理敏感信息
- ⚠️ 定期检查允许发送的用户列表

## 版本

v1.0 - 初始版本

## 许可证

MIT
