# 频道参数映射表

Phase 1.8 中，识别用户填写的频道类型后，从此文件读取对应的参数模板，
动态展示给用户填写。

---

## 使用方式

1. 从用户填写的频道名称匹配下方对应的频道条目
2. 将该频道的「用户需提供的参数」整理成问卷展示给用户
3. 收集完成后，按「openclaw 配置写法」构造 `openclaw channels add` 命令

如果用户填写的频道不在此列表中，执行：
```bash
openclaw channels list --json
```
查看已配置的频道，并提示用户参考 OpenClaw 官方文档获取参数说明：
https://docs.openclaw.ai/channels

---

## 各频道参数详情

---

### Telegram

**难度**：⭐ 最简单，推荐新手首选

**用户需提供的参数：**
```
Bot Token（从 @BotFather 获取）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw 配置写法：**
```yaml
channels:
  telegram:
    token: <BOT_TOKEN>
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel telegram --account <accountId> --token <BOT_TOKEN>
```

**获取 Token 方法：**
1. 在 Telegram 中找到 @BotFather
2. 发送 `/newbot`，按提示操作
3. 获得形如 `123456789:ABCdefGHI...` 的 token

---

### Discord

**难度**：⭐⭐ 较简单

**用户需提供的参数：**
```
Bot Token（从 Discord Developer Portal 获取）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw 配置写法：**
```yaml
channels:
  discord:
    token: <BOT_TOKEN>
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel discord --account <accountId> --token <BOT_TOKEN>
```

**获取 Token 方法：**
1. 访问 https://discord.com/developers/applications
2. 新建 Application → Bot → Reset Token
3. 复制 Token

---

### Slack

**难度**：⭐⭐⭐ 中等

**用户需提供的参数：**
```
Bot Token（xoxb- 开头）：___________
App Token（xapp- 开头，Socket Mode 用）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw 配置写法：**
```yaml
channels:
  slack:
    botToken: <BOT_TOKEN>
    appToken: <APP_TOKEN>
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel slack --account <accountId> \
  --bot-token <BOT_TOKEN> --app-token <APP_TOKEN>
```

**获取 Token 方法：**
1. 访问 https://api.slack.com/apps → Create New App
2. 开启 Socket Mode，生成 App Token（xapp-）
3. OAuth & Permissions → Bot Token（xoxb-）

---

### WhatsApp

**难度**：⭐⭐⭐ 中等（需 QR 扫码配对）

**用户需提供的参数：**
```
Account ID（账号别名，默认 default）：___________（可留空）
手机号（用于识别，如 +8613812345678）：___________（可选）
```

**注意**：WhatsApp 使用 Baileys（Web 协议），无需 API Token，
但需要扫描 QR 码完成配对，这一步必须由用户手动完成。

**openclaw channels add 命令：**
```bash
openclaw channels add --channel whatsapp --account <accountId>
# 执行后会显示 QR 码，用 WhatsApp 手机扫描完成配对
```

**用户操作清单补充：**
> ⚠️ WhatsApp 需要手动扫码，创建完成后请运行：
> `openclaw channels login --channel whatsapp --account <accountId>`
> 用手机 WhatsApp 扫描显示的 QR 码完成配对。

---

### 飞书（Feishu / Lark）

**难度**：⭐⭐⭐⭐ 较复杂（需插件安装 + 企业应用配置）

**前置条件**：需先安装飞书插件
```bash
openclaw plugin add feishu
```

**用户需提供的参数：**
```
App ID（飞书开放平台的应用 ID，格式 cli_xxxx）：___________
App Secret（飞书开放平台的应用密钥）：___________
Verification Token（事件订阅的验证 Token）：___________
Encrypt Key（加密密钥，可选但推荐）：___________（可留空）
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw 配置写法：**
```yaml
channels:
  feishu:
    appId: <APP_ID>
    appSecret: <APP_SECRET>
    verificationToken: <VERIFICATION_TOKEN>
    encryptKey: <ENCRYPT_KEY>
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel feishu --account <accountId> \
  --app-id <APP_ID> \
  --app-secret <APP_SECRET> \
  --verification-token <VERIFICATION_TOKEN> \
  --encrypt-key <ENCRYPT_KEY>
```

**获取参数方法：**
1. 访问飞书开放平台：https://open.feishu.cn/app
2. 创建企业自建应用
3. 「凭证与基础信息」页面获取 App ID 和 App Secret
4. 「事件订阅」页面获取 Verification Token 和 Encrypt Key
5. 配置回调地址：`https://<你的服务器>/feishu/webhook`

**用户操作清单补充：**
> ⚠️ 飞书需要在开放平台配置 Webhook 回调地址，服务器需对外可访问。
> 确保 openclaw gateway 已启动并可从公网访问。

---

### Microsoft Teams

**难度**：⭐⭐⭐⭐ 较复杂

**用户需提供的参数：**
```
Bot ID（Azure Bot 的 App ID）：___________
Bot Password（Azure Bot 的 App Password / Client Secret）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw 配置写法：**
```yaml
channels:
  msteams:
    botId: <BOT_ID>
    botPassword: <BOT_PASSWORD>
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel msteams --account <accountId> \
  --bot-id <BOT_ID> \
  --bot-password <BOT_PASSWORD>
```

---

### Google Chat

**难度**：⭐⭐⭐ 中等（需 Google Cloud 项目配置）

**用户需提供的参数：**
```
Service Account JSON 路径（或 JSON 内容）：___________
Project Number：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel googlechat --account <accountId> \
  --service-account <PATH_TO_JSON> \
  --project-number <PROJECT_NUMBER>
```

---

### Signal

**难度**：⭐⭐⭐⭐ 较复杂（需 signal-cli 环境）

**前置条件**：需先安装 signal-cli
```bash
# 参考：https://github.com/AsamK/signal-cli
```

**用户需提供的参数：**
```
注册的手机号（如 +8613812345678）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel signal --account <accountId> \
  --phone-number <PHONE_NUMBER>
```

---

### Matrix

**难度**：⭐⭐⭐ 中等

**用户需提供的参数：**
```
Homeserver URL（如 https://matrix.org）：___________
Access Token：___________
User ID（如 @bot:matrix.org）：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel matrix --account <accountId> \
  --homeserver <HOMESERVER_URL> \
  --access-token <ACCESS_TOKEN> \
  --user-id <USER_ID>
```

---

### LINE

**难度**：⭐⭐⭐ 中等（需插件安装）

**前置条件**：
```bash
openclaw plugin add line
```

**用户需提供的参数：**
```
Channel Access Token（长期 Token）：___________
Channel Secret：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel line --account <accountId> \
  --channel-token <ACCESS_TOKEN> \
  --channel-secret <CHANNEL_SECRET>
```

---

### Zalo

**难度**：⭐⭐⭐⭐ 较复杂（需插件安装）

**前置条件**：
```bash
openclaw plugin add zalo
```

**用户需提供的参数：**
```
App ID：___________
Secret Key：___________
Refresh Token：___________
Account ID（账号别名，默认 default）：___________（可留空）
```

**openclaw channels add 命令：**
```bash
openclaw channels add --channel zalo --account <accountId> \
  --app-id <APP_ID> \
  --secret-key <SECRET_KEY> \
  --refresh-token <REFRESH_TOKEN>
```

---

## 频道特殊说明汇总

| 频道 | 需要插件 | 需要 QR 扫码 | 需要公网访问 | 鉴权类型 |
|------|---------|------------|------------|---------|
| Telegram | 否 | 否 | 否（长轮询）| Bot Token |
| Discord | 否 | 否 | 否 | Bot Token |
| Slack | 否 | 否 | 否（Socket Mode）| Bot Token + App Token |
| WhatsApp | 否 | **是** | 否 | QR 配对 |
| 飞书 | **是** | 否 | **是** | App ID + Secret + Token |
| Teams | 否 | 否 | **是** | Bot ID + Password |
| Google Chat | 否 | 否 | **是** | Service Account |
| Signal | 否（需 signal-cli）| 否 | 否 | 手机号 |
| Matrix | 否 | 否 | 否 | Access Token |
| LINE | **是** | 否 | **是** | Channel Token + Secret |
| Zalo | **是** | 否 | 否 | App ID + Secret + Refresh Token |

---

## 未知频道处理

如用户提供的频道不在上表中：

```
⚠️ 频道「<CHANNEL>」暂无内置参数模板。

请提供以下信息：
  1. 该频道的鉴权参数（Token、Key 等，请参考 OpenClaw 官方文档）
  2. 频道是否需要先安装插件（openclaw plugin add <channel>）

参考文档：https://docs.openclaw.ai/channels
```
