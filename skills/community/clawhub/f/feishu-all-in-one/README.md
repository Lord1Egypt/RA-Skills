# 飞书 All-in-One 技能包

> 📦 开箱即用 | 经过完整验证 | 2026-03-04

## 快速开始

### 1. 飞书开放平台配置

1. 创建应用：https://open.feishu.cn/
2. 获取 App ID 和 App Secret
3. 配置权限（见 SKILL.md）
4. 配置事件订阅（使用长连接）
5. 发布应用

### 2. OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "你的App_ID",
      "appSecret": "你的App_Secret",
      "accounts": {
        "main": {
          "appId": "你的App_ID",
          "appSecret": "你的App_Secret"
        }
      }
    }
  }
}
```

### 3. 发送互动卡片

```bash
cd /path/to/feishu-all-in-one/scripts
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

# 发送给个人用户（已修复！）
node send-card.js confirmation "测试消息" \
  --chat-id ou_xxxxxxxx \
  --receive-id-type open_id
```

### 4. 启动回调服务器

```bash
cd /path/to/feishu-all-in-one/scripts

# 安装依赖（只需一次）
npm install

export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

node card-callback-server.js &
```

## 详细文档

请参阅 [SKILL.md](./SKILL.md) 获取完整配置指南。

## 已验证功能

- ✅ 文字消息收发
- ✅ 图片/文件发送
- ✅ 互动卡片发送
- ✅ 卡片按钮回调
- ✅ 主动消息推送
- ✅ 语音转文字（需单独安装 faster-whisper）
