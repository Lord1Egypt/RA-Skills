# Email Bridge

A personal email middleware with real-time notifications, verification code extraction, and multi-provider support (Gmail, QQ Mail, NetEase).

## Quick Start

### 安装

```bash
# 克隆项目
git clone https://github.com/ryanchan720/email-bridge.git
cd email-bridge

# 安装
pip install -e .

# 验证安装
python test_installation.py
```

### 配置账户

⚠️ **安全提示**: 请使用 CLI 本地配置，**不要在聊天中分享授权码**。

```bash
# 添加账户（会交互式提示输入授权码）
email-bridge accounts add your@qq.com -p qq

# 同步邮件
email-bridge sync

# 启动守护进程
email-bridge daemon start -d
```

## 添加邮箱账户

### QQ 邮箱（推荐，5 分钟）

1. 获取授权码：https://service.mail.qq.com/detail/0/75
2. 添加账户：
   ```bash
   email-bridge accounts add your@qq.com -p qq
   # 系统会提示输入授权码
   ```

### 网易邮箱（163/126）

1. 在邮箱设置中开启 IMAP/SMTP 服务，获取授权码
2. 添加账户：
   ```bash
   email-bridge accounts add your@163.com -p netease \
     --config '{"password": "YOUR_AUTH_CODE"}'
   ```

### Gmail（高级用户，20 分钟）

Gmail 需要 OAuth 配置，详见 [Gmail 配置指南](#gmail-配置指南)。

## 日常使用

```bash
# 同步邮件
email-bridge sync

# 查看最近邮件
email-bridge messages list -n 10

# 启动守护进程（实时通知）
email-bridge daemon start -d

# 提取验证码
email-bridge codes

# 发送邮件
email-bridge send -a <account_id> -t recipient@example.com -s "主题" -b "正文"
```

---

## Gmail 配置指南

> ⚠️ **注意**：Gmail API 配置流程较复杂，需要 Google Cloud 项目和 OAuth 授权。如果你只需要基本的收发邮件功能，建议等待后续 IMAP/SMTP 支持。

### 前置条件

- 一个 Google 账号（Gmail 邮箱）
- 能访问 Google Cloud Console（可能需要科学上网）

### Step 1：创建 Google Cloud 项目

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 登录你的 Google 账号
3. 页面顶部点击项目选择器，点击 **"NEW PROJECT"**
4. 项目名称随便填（如 `email-bridge`），点击 **"CREATE"**
5. 创建完成后选中该项目

### Step 2：启用 Gmail API

1. 打开 [Gmail API 页面](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
2. 确保顶部显示的是刚创建的项目
3. 点击 **"ENABLE"**

### Step 3：配置 OAuth 同意屏幕

1. 打开 [OAuth 同意屏幕配置](https://console.cloud.google.com/apis/credentials/consent)
2. 用户类型选择 **"External"**，点击 **"CREATE"**

**填写配置：**

| 字段 | 填写内容 |
|------|----------|
| App name | `Email Bridge` 或任意名称 |
| User support email | 选择你的邮箱 |
| Developer contact | 填你的邮箱 |
| 其他字段 | 可留空 |

点击 **"SAVE AND CONTINUE"**。

**Scopes（权限范围）：**

1. 点击 **"ADD OR REMOVE SCOPES"**
2. 搜索 `gmail.readonly`，勾选 `https://www.googleapis.com/auth/gmail.readonly`
3. 点击 **"UPDATE"**，然后 **"SAVE AND CONTINUE"**

> 💡 `gmail.readonly` 是只读权限，足够用于读取邮件。如需发送邮件，请使用 SMTP（需配置应用专用密码）。

**Test Users（测试用户）：**

1. 点击 **"ADD USERS"**
2. 填写你的 Gmail 地址
3. 点击 **"ADD"**，然后 **"SAVE AND CONTINUE"**

最后检查无误，点击 **"BACK TO DASHBOARD"**。

### Step 4：创建 OAuth 客户端凭证

1. 打开 [Credentials 页面](https://console.cloud.google.com/apis/credentials)
2. 点击 **"CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type 选择 **"Desktop app"**
4. Name 随便填（如 `Email Bridge CLI`）
5. 点击 **"CREATE"**
6. 在弹出窗口点击 **"DOWNLOAD JSON"** 下载凭证文件

### Step 5：安装凭证文件

```bash
# 创建目录
mkdir -p ~/.email-bridge/gmail

# 将下载的凭证文件移动过去，重命名为 credentials.json
mv ~/Downloads/client_secret_xxx.json ~/.email-bridge/gmail/credentials.json
```

### Step 6：添加账户并授权

```bash
# 添加 Gmail 账户
email-bridge accounts add your@gmail.com --provider gmail --name "Personal Gmail"

# 首次同步，会打开浏览器要求授权
email-bridge sync -a <account_id>
```

授权完成后，token 会自动保存在 `~/.email-bridge/gmail/token_*.json`，后续同步无需再次授权。

### Gmail 配置选项

```bash
# 自定义同步范围：最近 3 天，最多 50 封
email-bridge accounts add user@gmail.com -p gmail \
  --config '{"sync_days": 3, "sync_max_messages": 50}'
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `sync_days` | 同步最近 N 天的邮件 | 7 |
| `sync_max_messages` | 每次同步最大邮件数 | 100 |
| `credentials_path` | 自定义凭证文件路径 | `~/.email-bridge/gmail/credentials.json` |
| `token_path` | 自定义 token 存储路径 | 自动生成 |

> ⚠️ **Gmail 发送邮件**：如果需要用 Gmail 发送邮件，需要额外配置应用专用密码：
> 1. 开启 Google 账户的两步验证
> 2. 访问 [应用专用密码](https://myaccount.google.com/apppasswords)
> 3. 生成一个新密码，选择"邮件"和"其他设备"
> 4. 用应用专用密码更新账户配置：
>    ```bash
>    email-bridge accounts update <account_id> --config '{"password": "YOUR_APP_PASSWORD"}'
>    ```

---

## QQ 邮箱配置

> ✅ **推荐**：配置简单，只需要授权码。

### Step 1：开启 IMAP 服务

1. 登录 [QQ 邮箱](https://mail.qq.com/)
2. 点击 **设置** → **账户**
3. 找到 **"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"**
4. 开启 **"IMAP/SMTP服务"**
5. 按提示发送短信验证
6. 获得一个 **16 位授权码**（保存好！）

### Step 2：添加账户

```bash
# 使用授权码（不是登录密码！）
email-bridge accounts add your@qq.com -p qq \
  --config '{"password": "YOUR_16_CHAR_AUTH_CODE"}' \
  --name "QQ Mail"
```

### Step 3：同步邮件

```bash
email-bridge sync -a <account_id>
```

---

## 网易邮箱配置（163/126）

> ✅ **推荐**：配置简单，只需要授权码。

### Step 1：开启 IMAP 服务

**163 邮箱：**
1. 登录 [163 邮箱](https://mail.163.com/)
2. 点击 **设置** → **POP3/SMTP/IMAP**
3. 开启 **"IMAP/SMTP服务"**
4. 获得授权码

**126 邮箱：**
1. 登录 [126 邮箱](https://mail.126.com/)
2. 同上步骤

### Step 2：添加账户

```bash
# 163 邮箱
email-bridge accounts add your@163.com -p netease \
  --config '{"password": "YOUR_AUTH_CODE"}' \
  --name "163 Mail"

# 126 邮箱
email-bridge accounts add your@126.com -p netease \
  --config '{"password": "YOUR_AUTH_CODE"}' \
  --name "126 Mail"
```

### Step 3：同步邮件

```bash
email-bridge sync -a <account_id>
```

---

## 使用示例

### 查看邮件

```bash
# 列出最近邮件
email-bridge messages list

# 列出最近 20 封
email-bridge messages list -n 20

# 只看未读
email-bridge messages unread

# 按关键词搜索
email-bridge messages search --keyword "verification"

# 按日期范围搜索
email-bridge messages search --from-date 2026-03-20 --to-date 2026-03-24

# 查看邮件详情
email-bridge messages get <message_id>
```

### 验证码提取

```bash
# 提取邮件中的验证码
email-bridge extract <message_id> --codes

# 提取操作链接
email-bridge extract <message_id> --links

# 两者都要
email-bridge extract <message_id> --all

# 快速查找最近验证码
email-bridge codes
email-bridge codes -a <account_id>
```

### 发送邮件

```bash
# 发送简单邮件
email-bridge send -a <account_id> -t recipient@example.com -s "主题" -b "正文内容"

# 发送给多人
email-bridge send -a <account_id> -t user1@example.com -t user2@example.com -s "主题" -b "正文"

# 抄送
email-bridge send -a <account_id> -t recipient@example.com -c cc@example.com -s "主题" -b "正文"

# 发送 HTML 邮件
email-bridge send -a <account_id> -t recipient@example.com -s "主题" --html "<h1>标题</h1><p>内容</p>"
```

### 守护进程（实时监听）

Email Bridge 支持后台运行，实时监听新邮件：

```bash
# 启动守护进程（后台运行）
email-bridge daemon start -d

# 查看状态
email-bridge daemon status

# 停止守护进程
email-bridge daemon stop

# 自定义轮询间隔（默认 300 秒，仅影响 Gmail）
email-bridge daemon start -d -i 60

# 禁用 OpenClaw 通知
email-bridge daemon start -d --no-notify
```

**工作模式：**

| 邮箱 | 模式 | 延迟 |
|------|------|------|
| QQ 邮箱 | IDLE（实时推送） | 秒级 |
| 网易邮箱 | IDLE（实时推送） | 秒级 |
| Gmail | 轮询 | 可配置（默认 5 分钟） |

> 💡 QQ/网易邮箱使用 IMAP IDLE 协议，服务器有新邮件会主动推送通知。Gmail 不支持 IDLE，使用定时轮询。

**通知内容：**

收到新邮件时，会通过 `openclaw system event` 发送通知，包含发件人和主题：

```
📧 新邮件: ryanchan720@qq.com

1. 发件人名称
   邮件主题

2. 发件人名称
   邮件主题

... 还有 N 封
```

> 💡 通知只在有新邮件到达时触发，不会重复通知已存在的邮件。

**日志文件：** `~/.email-bridge/daemon.log`

### 账户管理

```bash
# 列出所有账户
email-bridge accounts list

# 更新账户名称
email-bridge accounts update <id> --name "New Name"

# 禁用/启用账户
email-bridge accounts update <id> --disable
email-bridge accounts update <id> --enable

# 删除账户（同时删除邮件）
email-bridge accounts delete <id>
```

### 同步

```bash
# 同步所有账户
email-bridge sync

# 同步指定账户
email-bridge sync -a <account_id>

# 同步最近 30 天
email-bridge sync --days 30
```

### 统计

```bash
email-bridge stats
```

---

## 邮件分类

邮件根据主题关键词自动分类（仅扫描主题，不扫描正文）：

| 分类 | 说明 | 示例关键词 |
|------|------|-----------|
| `verification` | 验证码、账户确认 | 验证码, OTP, activate, 绑定邮箱 |
| `security` | 安全提醒、登录通知 | 安全提醒, security alert, 密码修改 |
| `transactional` | 订单、支付、发货 | 订单确认, receipt, 发货通知 |
| `promotion` | 营销推广、优惠活动 | 奖励, 优惠, promo, discount |
| `subscription` | 订阅、Newsletter | newsletter, 订阅, weekly digest |
| `spam_like` | 疑似垃圾邮件 | 中奖, FREE, click here now |
| `normal` | 普通邮件（默认） | - |

**通知格式**：
- 🔐 verification：重点显示验证码
- ⚠️ security：突出警示信息
- 📦 transactional：订单/发货通知
- 🎁 promotion：营销推广
- 📰 subscription：订阅内容
- 🚫 spam_like：标记但不展开

---

## 功能总结

| 功能 | Gmail | QQ 邮箱 | 网易邮箱 |
|------|-------|---------|----------|
| 接收邮件 | ✅ API | ✅ IMAP | ✅ IMAP |
| 发送邮件 | ✅ SMTP* | ✅ SMTP | ✅ SMTP |
| 实时监听 | ✅ 轮询 | ✅ IDLE | ✅ IDLE |
| 新邮件通知 | ✅ | ✅ | ✅ |
| 验证码提取 | ✅ | ✅ | ✅ |
| 链接提取 | ✅ | ✅ | ✅ |
| 自动分类 | ✅ | ✅ | ✅ |

*\*Gmail 发送需要额外配置应用专用密码*

---

## 数据存储

所有数据存储在 `~/.email-bridge/`：

```
~/.email-bridge/
├── email_bridge.db          # SQLite 数据库
├── daemon.pid               # 守护进程 PID（运行时）
├── daemon.log               # 守护进程日志
└── gmail/
    ├── credentials.json     # OAuth 凭证
    └── token_xxx.json       # 授权 Token（自动生成）
```

---

## 项目结构

```
email-bridge/
├── email_bridge/
│   ├── cli.py           # CLI 入口（Click）
│   ├── service.py       # 业务逻辑层
│   ├── models.py        # Pydantic 数据模型
│   ├── db.py            # SQLite 存储层
│   ├── categories.py    # 分类检测
│   ├── extraction.py    # 验证码/链接提取
│   ├── daemon.py        # 守护进程
│   └── adapters/
│       ├── base.py      # Adapter 接口
│       ├── mock.py      # Mock 适配器（演示用）
│       ├── gmail.py     # Gmail API 适配器
│       ├── imap.py      # IMAP 适配器（QQ/网易）
│       └── smtp.py      # SMTP 发送适配器
├── fixtures/
│   └── sample_emails.json
├── tests/
├── README.md
└── DESIGN.md
```

---

## Roadmap

**当前版本 v0.5：**
- ✅ Gmail API 集成（OAuth2）
- ✅ QQ 邮箱 IMAP/SMTP 集成
- ✅ 网易邮箱（163/126）IMAP/SMTP 集成
- ✅ 验证码提取
- ✅ 操作链接提取
- ✅ 发送邮件
- ✅ 守护进程模式
- ✅ Mock 模式演示

**计划中：**
- ⏳ Web UI
- ⏳ 附件处理

---

## License

MIT