# Discord 渠道配置指南

## 概述
本指南将帮助您配置 OpenClaw 的 Discord 渠道，以便在 Discord 社区推广 feishu-team-manager 技能。

## 配置前提
- 拥有 Discord 账号
- 拥有或可以创建一个 Discord 服务器
- 能够访问 Discord 开发者门户 (https://discord.com/developers/applications)

## 配置步骤

### 第1步：创建 Discord 应用和机器人

1. **访问 Discord 开发者门户**
   - 打开 https://discord.com/developers/applications
   - 登录您的 Discord 账号

2. **创建新应用**
   - 点击右上角 "New Application"
   - 应用名称: "OpenClaw" (或您喜欢的名称)
   - 点击 "Create"

3. **创建机器人**
   - 在左侧菜单点击 "Bot"
   - 点击 "Add Bot"
   - 确认创建

4. **配置机器人设置**
   - **Username**: OpenClaw (或您喜欢的名称)
   - **Icon**: 可上传头像 (可选)
   - **Public Bot**: 保持关闭 (仅限您的服务器使用)

5. **启用特权网关意图 (Privileged Gateway Intents)**
   在 Bot 页面下方找到 "Privileged Gateway Intents"，启用：
   - ✅ **Message Content Intent** (必需)
   - ✅ **Server Members Intent** (推荐，用于权限管理)
   - ✅ **Presence Intent** (可选)

### 第2步：获取机器人令牌 (Bot Token)

1. **重置/获取令牌**
   - 在 Bot 页面找到 "Token" 部分
   - 点击 "Reset Token"
   - 确认操作
   - **复制生成的令牌并妥善保存** (这是敏感信息，不要分享)

   > ⚠ **重要**: 令牌相当于机器人的密码，泄露后他人可以控制您的机器人。

2. **令牌格式示例**
   ```
   MTAxODIzOTAyNjExNDE4MjQ4Mg.G1L6cC.abcdefghijklmnopqrstuvwxyz123456
   ```

### 第3步：生成邀请链接并添加机器人到服务器

1. **配置 OAuth2**
   - 左侧菜单点击 "OAuth2" → "URL Generator"
   - 在 "Scopes" 部分勾选：
     - ✅ `bot`
     - ✅ `applications.commands`

2. **设置机器人权限**
   在 "Bot Permissions" 部分勾选以下权限：
   - ✅ View Channels (查看频道)
   - ✅ Send Messages (发送消息)
   - ✅ Read Message History (读取消息历史)
   - ✅ Embed Links (嵌入链接)
   - ✅ Attach Files (附加文件)
   - ✅ Add Reactions (添加反应，可选)

3. **生成邀请链接**
   - 页面底部会生成一个 URL
   - 复制该 URL
   - 在浏览器中打开该 URL
   - 选择您的 Discord 服务器
   - 点击 "Authorize"

### 第4步：获取必要的 ID

1. **启用开发者模式**
   - 打开 Discord 客户端
   - 用户设置 (齿轮图标) → 高级 → 启用 "开发者模式"

2. **获取服务器 ID**
   - 右键点击服务器图标
   - 选择 "复制服务器 ID"

3. **获取用户 ID**
   - 右键点击您的头像
   - 选择 "复制用户 ID"

4. **保存 ID**
   - 服务器 ID: `123456789012345678` (示例)
   - 用户 ID: `987654321098765432` (示例)

### 第5步：允许机器人发送私信

1. **服务器隐私设置**
   - 右键点击服务器图标
   - 选择 "隐私设置"
   - 启用 "允许服务器成员发送私信"

### 第6步：配置 OpenClaw

#### 方法A：使用环境变量 (推荐)

1. **设置环境变量**
   ```bash
   # 设置 Discord 机器人令牌
   export DISCORD_BOT_TOKEN="您的机器人令牌"
   
   # 设置用户ID和服务器ID (可选，用于配对)
   export DISCORD_USER_ID="您的用户ID"
   export DISCORD_SERVER_ID="您的服务器ID"
   ```

2. **验证环境变量**
   ```bash
   echo $DISCORD_BOT_TOKEN
   ```

#### 方法B：直接修改 openclaw.json

1. **备份当前配置**
   ```bash
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **添加 Discord 配置**
   在 `channels` 部分添加以下配置：

   ```json
   "discord": {
     "enabled": true,
     "token": {
       "source": "env",
       "provider": "default",
       "id": "DISCORD_BOT_TOKEN"
     },
     "accounts": {
       "default": {
         "dmPolicy": "open",
         "allowFrom": ["*"]
       }
     },
     "streaming": true,
     "footer": {
       "elapsed": true,
       "status": true
     }
   }
   ```

3. **完整配置示例**
   ```json
   {
     "channels": {
       "feishu": { ... },
       "qqbot": { ... },
       "discord": {
         "enabled": true,
         "token": {
           "source": "env",
           "provider": "default",
           "id": "DISCORD_BOT_TOKEN"
         },
         "accounts": {
           "default": {
             "dmPolicy": "open",
             "allowFrom": ["*"]
           }
         },
         "streaming": true,
         "footer": {
           "elapsed": true,
           "status": true
         }
       }
     }
   }
   ```

### 第7步：重启 OpenClaw Gateway

1. **重启服务**
   ```bash
   openclaw gateway restart
   ```

2. **检查状态**
   ```bash
   openclaw gateway status
   ```

3. **查看日志**
   ```bash
   journalctl -u openclaw -f
   ```

### 第8步：配对机器人

1. **发送配对指令**
   在 Discord 中向您的机器人发送：
   ```
   /pair
   ```

2. **或通过其他渠道配对**
   如果您有其他已配置的渠道 (如飞书)，可以发送：
   ```
   "我已经设置了 Discord 机器人令牌。请完成 Discord 设置，用户ID是 <您的用户ID>，服务器ID是 <您的服务器ID>。"
   ```

### 第9步：验证配置

1. **检查连接状态**
   - Discord 机器人应该显示为在线
   - 可以 @机器人 或发送消息测试

2. **测试功能**
   ```bash
   # 测试消息发送
   openclaw message --channel discord --action send --message "测试消息"
   ```

## 故障排除

### 常见问题1：机器人不在线
- **原因**: 令牌错误或配置不正确
- **解决**: 检查令牌是否正确，环境变量是否设置

### 常见问题2：无法发送消息
- **原因**: 权限不足
- **解决**: 确保机器人有 "Send Messages" 权限

### 常见问题3：无法读取消息
- **原因**: 未启用 Message Content Intent
- **解决**: 在开发者门户重新启用 Message Content Intent

### 常见问题4：私信无法工作
- **原因**: 服务器隐私设置未允许私信
- **解决**: 启用 "允许服务器成员发送私信"

## 安全建议

1. **令牌安全**
   - 不要将令牌提交到版本控制系统
   - 不要通过聊天分享令牌
   - 定期轮换令牌

2. **权限最小化**
   - 只授予必要的权限
   - 在生产环境使用限制性更强的权限

3. **环境隔离**
   - 开发和生产环境使用不同的机器人
   - 使用不同的令牌

## 推广使用

配置完成后，您可以使用以下命令在 Discord 推广 feishu-team-manager：

```bash
# 发送推广消息
openclaw message --channel discord --action send --message "🎉 新技能发布：feishu-team-manager (HR大姐头) v2.3.1 ..."
```

## 获取帮助

如果遇到问题：
1. 查看 OpenClaw Discord 文档: `/usr/lib/node_modules/openclaw/docs/channels/discord.md`
2. 检查日志: `journalctl -u openclaw -f`
3. 在 OpenClaw Discord 社区寻求帮助

---
**指南版本**: 1.0.0  
**最后更新**: 2026-04-23  
**适用 OpenClaw 版本**: 2026.3.28+