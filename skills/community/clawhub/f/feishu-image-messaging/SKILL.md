---
name: feishu-image-messaging
description: 飞书图片消息收发助手 - 通过飞书 API 发送和接收图片消息，支持本地文件、远程 URL、图文混排。解决飞书官方 API 只提供底层接口、开发者需要自行封装图片上传和消息发送流程的痛点。适用于需要自动化发送图片到飞书群聊或私聊的场景，如：每日简报配图、监控系统截图报警、报表自动推送等。
---

# Feishu Image Messaging / 飞书图片消息助手

## 功能特性 / Features

- 📤 **发送图片** - 支持本地文件、远程 URL
- 📝 **图文混排** - 图片配文字，丰富消息内容
- 🎯 **多场景支持** - 单聊、群聊均可
- 🔧 **简单易用** - 一行命令完成图片发送

## 解决的问题 / Problem Solved

飞书开放平台官方只提供底层 API：
- 需要先调用 `im/v1/images` 上传图片获取 `image_key`
- 再调用 `im/v1/messages` 发送消息，拼接复杂的富文本 JSON

**本 Skill 帮你封装好整个流程**，只需一行命令即可发送图片。

## 使用场景 / Use Cases

- 📊 **每日简报** - 早报自动配图发送到群聊
- 🚨 **监控报警** - 系统异常截图自动推送
- 📈 **报表推送** - 定时发送数据可视化图表
- 🤖 **机器人消息** - 智能助手发送图片回复

## 安装 / Installation

```bash
# 从 ClawHub 安装
clawhub install feishu-image-messaging

# 或本地安装
clawhub install ./feishu-image-messaging.skill
```

## 配置 / Configuration

设置环境变量：

```bash
export FEISHU_APP_ID="cli_xxxxxx"
export FEISHU_APP_SECRET="xxxxxx"
```

> 💡 获取方式：飞书开放平台 → 开发者后台 → 创建应用 → 查看凭证

## 使用方法 / Usage

### 快速发送（推荐）

```bash
# 发送本地图片
./scripts/send_image.sh -r "ou_xxx" -i "/path/to/image.jpg"

# 发送远程图片 + 配文
./scripts/send_image.sh -r "oc_xxx" -i "https://example.com/img.png" -t "每日数据报表"
```

参数说明：
- `-r`: 接收者 ID（open_id / user_id / chat_id）
- `-i`: 图片路径（本地文件）或 URL（远程图片）
- `-t`: 可选， accompanying text

### 分步调用（高级）

```bash
# 1. 获取 token
TOKEN=$(./scripts/get_token.sh)

# 2. 上传图片
IMAGE_KEY=$(./scripts/upload_image.sh -f "image.jpg" -t "$TOKEN")

# 3. 发送消息
./scripts/send_message.sh -r "ou_xxx" -k "$IMAGE_KEY" -t "Hello" -a "$TOKEN"
```

## API 文档 / API Reference

详见 `references/api.md`：
- 图片上传 API
- 图片下载 API
- 消息发送 API
- 认证 API

## 文件结构 / File Structure

```
feishu-image-messaging/
├── SKILL.md              # 本文件
├── scripts/
│   ├── config.sh         # 配置（从环境变量读取）
│   ├── get_token.sh      # 获取 access token
│   ├── upload_image.sh   # 上传图片
│   ├── send_message.sh   # 发送消息
│   └── send_image.sh     # 一键发送（整合以上）
└── references/
    └── api.md            # API 文档
```

## 技术栈 / Tech Stack

- Shell / Bash
- curl（HTTP 请求）
- jq（JSON 处理）
- 飞书开放平台 API

## 注意事项 / Notes

- ⚠️ 请妥善保管 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`，不要提交到代码仓库
- 🔄 Access token 有效期为 2 小时，脚本会自动处理获取
- 📤 图片上传后获得的 `image_key` 有效期为 1 年
- 🎯 `image_key` 可以重复使用，建议缓存以减少上传次数

## 问题排查 / Troubleshooting

| 错误码 | 含义 | 解决 |
|--------|------|------|
| `99992402` | 缺少必填字段 | 检查 `receive_id_type` 参数 |
| `230001` | 消息内容格式错误 | 检查 JSON 格式和转义 |
| `11200` | Access token 无效 | 重新获取 token |

## 更新日志 / Changelog

### v1.0.0 (2025-03-11)
- ✨ 初始版本
- 📤 支持本地图片上传
- 🌐 支持远程图片 URL
- 📝 支持图文混排
- 🎯 支持单聊和群聊

## 作者 / Author

Created by OpenClaw AI Assistant for Hivemoon Inc.

## 许可证 / License

MIT License

---

**Enjoy sending images with Feishu! 🚀**
