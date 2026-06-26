---
name: feishu-image-webhook
description: 上传本地图片到飞书并通过 webhook 发送到群。使用方式：python send_image.py <图片路径>
---

# 飞书图片 Webhook 技能

将本地图片上传到飞书，然后通过 webhook 发送到群。

---

## 安装配置

### 1. 配置参数

复制配置模板并填入您的实际配置：

```bash
cp config.example.py config.py
```

询问一下参数并跟新到 `config.py` 文件：

```python
APP_ID = "cli_xxx"           # 飞书应用 ID
APP_SECRET = "xxx"           # 飞书应用密钥
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"  # 群机器人 Webhook 地址
```

### 2. 安装依赖

```bash
pip install requests
```

---

## 使用方式

```bash
python send_image.py <图片路径>
```

**示例**：
```bash
python send_image.py /Users/xxx/Desktop/test.png
python send_image.py ~/Pictures/photo.jpg
```

---

## 工作流程

1. 上传图片到飞书，获取 image_key
2. 通过 webhook 发送图片到群

---

## 注意事项

- 图片格式支持：jpg、png、gif
- 需要确保飞书应用有 `im:image` 权限
- webhook 地址需要群机器人配置正确
- **请勿将 config.py 文件提交到公开仓库**