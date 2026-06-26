---
name: dingtalk-connector-guide
version: 1.0.0
description: 钉钉机器人接入指南 - OpenClaw 连接钉钉完整教程。适合：中国企业用户、钉钉开发者。
metadata:
  openclaw:
    emoji: "📌"
    requires:
      bins: []
---

# 钉钉机器人接入指南

让 AI 助手连接钉钉，自动处理群消息。

## 前置条件

1. 钉钉企业账号（管理员权限）
2. OpenClaw 已安装
3. 公网可访问的服务器（或内网穿透）

## 步骤 1：创建钉钉应用

1. 登录 [钉钉开放平台](https://open.dingtalk.com)
2. 进入「应用开发」→「企业内部开发」
3. 点击「创建应用」
4. 填写应用信息：
   - 应用名称：AI 助手
   - 应用描述：OpenClaw AI 助手
   - 应用 Logo：上传图标

## 步骤 2：获取凭证

创建完成后，记录以下信息：

```
AppKey（Client ID）：dingxxxxxxxxxxxxxxx
AppSecret（Client Secret）：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## 步骤 3：配置机器人

1. 进入应用 →「机器人与消息推送」
2. 点击「添加机器人」
3. 配置机器人：
   - 机器人名称：AI 助手
   - 机器人图标：上传
   - 消息接收地址：`https://your-server.com/webhook/dingtalk`

## 步骤 4：权限配置

在「权限管理」中开通：

- ✅ 企业会话消息读权限
- ✅ 企业会话消息写权限
- ✅ 通讯录只读权限
- ✅ 成员信息读权限

## 步骤 5：配置 OpenClaw

```bash
# 设置钉钉连接
openclaw connect dingtalk

# 输入凭证
Client ID: dingxxxxxxxxxxxxxxx
Client Secret: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# 启动服务
openclaw start
```

## 步骤 6：测试机器人

在钉钉群中 @机器人 发送消息：

```
@AI助手 你好
```

机器人应该回复：

```
你好！我是 AI 助手，有什么可以帮助你的？
```

## 常见问题

### Q: 消息接收地址填什么？

需要是公网可访问的 HTTPS 地址。如果没有公网服务器：

```bash
# 使用 ngrok 内网穿透
ngrok http 3000
# 将生成的 https://xxx.ngrok.io 填入
```

### Q: 机器人不回复？

检查清单：
1. 权限是否开通
2. 服务是否启动
3. 网络是否可达
4. 日志是否有错误

```bash
# 查看日志
openclaw logs -f
```

### Q: 如何支持图片消息？

需要在钉钉开放平台开通「图片消息」权限，并在 OpenClaw 配置中启用。

## 高级配置

### 多群支持

机器人默认支持所有群，可以通过配置限制：

```yaml
# ~/.openclaw/config.yaml
dingtalk:
  allowed_chats:
    - chat_id_1
    - chat_id_2
```

### 自定义欢迎语

```yaml
dingtalk:
  welcome_message: |
    欢迎加入！我是 AI 助手。
    有问题随时 @我
```

### 工作时间限制

```yaml
dingtalk:
  work_hours:
    start: "09:00"
    end: "18:00"
    timezone: "Asia/Shanghai"
```

## 需要帮助？

- 📖 完整文档：https://docs.openclaw.ai
- 💬 技术支持：
  - 基础接入：¥99
  - 高级配置：¥299
  - 企业定制：¥999

联系：微信 yang1002378395 或 Telegram @yangster151
