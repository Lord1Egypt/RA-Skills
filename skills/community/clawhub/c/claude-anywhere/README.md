# Claude Anywhere

![Claude Anywhere](https://img.shields.io/badge/Claude-Anywhere-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.6.1-brightgreen?style=for-the-badge)

**Claude Anywhere Pro — 龙虾与Claude Code的完美结合**
**Claude Anywhere Pro — OpenClaw meets Claude Code, anywhere.**

> 不是聊天机器人。是你口袋里的 AI 员工。
> Not a chatbot. Your AI engineer, in your pocket.

Claude Anywhere 让你通过 Telegram、企业微信、QQ 随时随地：

- 📂 读写文件 / Read/write files remotely
- ⚡ 执行命令 / Execute commands on your server
- 📷 分析图片 / Analyze images — just send a screenshot
- 📄 文件分析 / Analyze files — PDF, Excel, CSV, code
- 🔄 会话恢复 / Resume sessions across any device
- ⏰ 定时任务 / Schedule cron tasks

在手机上也能做到电脑上的一切。摆脱终端束缚。
Everything you can do on desktop, now in your pocket. No terminal needed.

---

## 3步上手 / 3 Steps to Start

### Telegram
1. 在 Telegram 搜索 @BotFather，发 /newbot，复制 Token
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 Token → `npm run telegram` → 完成 ✅

### 企业微信 WeChat Work
1. 登录 work.weixin.qq.com → 应用管理 → AI助手 → 创建机器人，记录 Bot ID 和 Secret
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 Bot ID + Secret → `npm run wecom` → 完成 ✅

### QQ
1. 打开 https://q.qq.com/qqbot/openclaw/index.html → 扫码 → 创建机器人 → 获取 AppID + AppSecret
2. `git clone https://github.com/yizhao1978/claude-anywhere.git && cd claude-anywhere && npm install && cp .env.example .env`
3. 填入 AppID + AppSecret → `npm run qq` → 完成 ✅

### 三平台一键启动
配好所有 Token → `npm start` → 自动启动已配置的平台

---

## 🔄 随时接续，永不中断 / Resume Anywhere, Never Lose Progress

Claude Anywhere 最强大的功能之一：你可以在任何设备、任何平台上接续之前的对话。

One of Claude Anywhere's most powerful features: resume any conversation, on any device, any platform.

在地铁上开始调试代码，到办公室打开电脑继续——`/sessions` 列出所有会话，`/resume` 一键接续。你的工作进度，永远不会丢失。

Start debugging on the subway, continue at your desk — `/sessions` to list all sessions, `/resume` to pick up where you left off. Your work, always saved.

---

## 免费版 vs Pro 版 / Free vs Pro

| 功能 / Feature | 免费 Free | Pro |
|---|---|---|
| 每日消息数 / Messages/day | 5 条 | 无限 Unlimited |
| 试用期 / Trial period | 7 天 | — |
| 多轮对话 / Multi-turn chat | ✗ | ✓ |
| 图片分析 / Image analysis | ✗ | ✓ |
| 文件分析 / File analysis | ✗ | ✓ |
| 企业微信 / WeChat Work | 有限 Limited | 完整 Full |
| 广告 / Ads | ✓ | ✗ |
| 会话历史 / Session history | ✗ | ✓ |

**升级 Pro → [claudeanywhere.gumroad.com/l/claude-anywhere](https://claudeanywhere.gumroad.com/l/claude-anywhere)（$5.99/月）**

---

## 前置要求 / Prerequisites

在开始之前，请确认以下每一项都已准备好。
Before starting, make sure all of the following are ready.

### 1. Node.js 18 或更高版本 / Node.js 18+

**检查是否已安装 / Check if installed：**
```bash
node --version
```

**预期输出 / Expected output：**
```
v20.11.0
```
看到 `v18.x.x` 或更高版本即可。显示 `command not found` 说明未安装。

**如未安装 / If not installed：**
```bash
# Ubuntu / Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS（需要先安装 Homebrew / requires Homebrew）
brew install node

# 验证安装 / Verify
node --version
npm --version
```

**常见报错 / Common errors：**
- `Permission denied`：在命令前加 `sudo`
- `curl: command not found`：先运行 `sudo apt install curl`

---

### 2. Claude Code CLI

**检查是否已安装 / Check if installed：**
```bash
claude --version
```

**预期输出 / Expected output：**
```
1.x.x
```

**如未安装 / If not installed：**
```bash
npm install -g @anthropic-ai/claude-code
```

**预期输出 / Expected output：**
```
added 1 package in 3s
```

安装后需要完成一次登录（After install, complete login once）：
```bash
claude
# 按提示登录 Anthropic 账号 / Follow prompts to log in to Anthropic account
# 登录后按 Ctrl+C 退出即可 / Press Ctrl+C to exit after login
```

**常见报错 / Common errors：**
- `EACCES: permission denied`：运行 `sudo npm install -g @anthropic-ai/claude-code`
- 登录后 `claude --version` 仍报错：重新开一个终端窗口再试

---

### 3. 平台 Token / Platform Tokens

各平台的 Token 获取方式见上方"3步上手"部分。
See the "3 Steps to Start" section above for token setup.

---

## 详细安装 / Detailed Installation

### 第 1 步：下载代码 / Step 1: Clone the repository

```bash
git clone https://github.com/yizhao1978/claude-anywhere.git
cd claude-anywhere
```

---

### 第 2 步：安装依赖 / Step 2: Install dependencies

```bash
npm install
```

**常见报错 / Common errors：**
- `npm: command not found`：Node.js 未正确安装，回到前置要求第 1 步
- `EACCES: permission denied`：不要用 `sudo npm install`，改用 `npm install`（不加 sudo）
- 出现大量 `npm warn`：警告不影响使用，忽略即可；只有 `npm error` 才需要处理

---

### 第 3 步：创建配置文件 / Step 3: Create config file

```bash
cp .env.example .env
```

---

### 第 4 步：编辑配置文件 / Step 4: Edit config file

```bash
nano .env
```

填入你的配置（至少填一个平台的 Token）：

```ini
# ✅ Telegram Bot Token（从 @BotFather 获取 / from @BotFather）
TELEGRAM_BOT_TOKEN=7123456789:AAHxxxYourTokenHere

# ⬜ 可选：Pro 授权码 / Optional: Pro license key
LICENSE_KEY=

# ⬜ 可选：授权服务器 / Optional: License server URL
LICENSE_SERVER_URL=https://license.claudeanywhere.com

# ⬜ 可选：claude 命令路径 / Optional: Path to claude binary
CLAUDE_PATH=

# ⬜ 可选：Claude 工作目录 / Optional: Working directory
CLAUDE_CWD=

# ⬜ 可选：企业微信 / Optional: WeChat Work
WECOM_BOT_ID=
WECOM_SECRET=

# ⬜ 可选：QQ Bot / Optional: QQ Bot
QQ_APP_ID=
QQ_APP_SECRET=
```

---

### 第 5 步：启动 / Step 5: Start

```bash
# 单平台 / Single platform
npm run telegram
npm run wecom
npm run qq

# 所有已配置平台 / All configured platforms
npm start
```

看到 `Bot started` 即成功。
See `Bot started` = success.

---

## 后台运行 / Background Running

### 方式一：tmux（推荐新手 / Recommended for beginners）

```bash
# 安装 tmux / Install tmux
sudo apt install tmux          # Ubuntu/Debian
brew install tmux              # macOS

# 创建后台会话 / Create background session
tmux new -s claude-anywhere

# 在 tmux 里启动 / Start inside tmux
npm run telegram

# 脱离 tmux（Bot 继续在后台运行）/ Detach (bot keeps running)
# 先按 Ctrl+B，松开，再按 D
```

重新进入查看日志 / Reattach to view logs：
```bash
tmux attach -t claude-anywhere
```

---

### 方式二：systemd（推荐生产环境 / Recommended for production）

```bash
# 1. 复制服务文件 / Copy service file
sudo cp systemd/claude-anywhere.service /etc/systemd/system/

# 2. 编辑服务文件，修改路径和用户名
sudo nano /etc/systemd/system/claude-anywhere.service

# 3. 重载并启动 / Reload and start
sudo systemctl daemon-reload
sudo systemctl enable claude-anywhere
sudo systemctl start claude-anywhere

# 4. 查看状态 / Check status
sudo systemctl status claude-anywhere

# 5. 查看实时日志 / View live logs
journalctl -u claude-anywhere -f
```

---

### 方式三：一键启动所有平台 / All-in-one start

在 `.env` 里配好所有平台的 Token，然后：
```bash
npm start
```
会自动检测已配置的平台并全部启动。

---

## 使用方法 / Usage

启动成功后，打开对应平台找到你创建的 Bot，直接发消息即可。
After starting, open your platform, find your bot, and start chatting.

### 命令列表 / Commands

| 命令 / Command | 说明 / Description |
|---|---|
| `/new` | 开始新对话，清除上下文 / Start fresh conversation |
| `/sessions` | 查看所有历史会话 / List all sessions |
| `/resume <id>` | 接续指定会话 / Resume a specific session |
| `/status` | 查看当前账号状态和今日用量 / Show tier & daily usage |
| `/cron <描述>` | 创建定时任务（自然语言）/ Create scheduled task (natural language) |
| `/cron list` | 查看所有定时任务 / List all scheduled tasks |
| `/cron remove <id>` | 删除定时任务 / Remove a scheduled task |
| `/activate <key>` | 激活 Pro 授权码 / Activate Pro license key |
| `/help` | 显示帮助和功能列表 / Show help & feature list |

---

## 🔄 会话管理详解 / Session Management

Claude Anywhere 支持跨设备、跨平台的会话接续，是区别于普通聊天机器人的核心功能。

Claude Anywhere supports cross-device, cross-platform session resumption — a core feature that sets it apart from ordinary chatbots.

### 查看所有会话 / List all sessions

```
/sessions
```

### 接续会话 / Resume a session

```
/resume abc12345
```

Claude Anywhere 会立即恢复该会话的完整上下文，就像你从未离开。
Claude Anywhere immediately restores the full context of that session, as if you never left.

### 使用场景 / Use cases

- **跨设备**：在电脑上开始调试 → 出门后用手机 Telegram 继续
  **Cross-device**: Start debugging on desktop → continue on phone via Telegram

- **跨平台**：早上在企业微信布置任务 → 下午在 QQ 上检查进度
  **Cross-platform**: Assign tasks on WeCom in the morning → check progress on QQ in the afternoon

- **多项目**：同时进行多个项目 → `/sessions` 切换不同工作上下文
  **Multi-project**: Work on multiple projects simultaneously → use `/sessions` to switch contexts

---

## ⏰ 定时任务详解 / Scheduled Tasks (Cron)

Claude Anywhere 支持用自然语言创建定时任务，无需记忆 cron 表达式。
Claude Anywhere supports natural-language scheduled tasks — no cron syntax needed.

### 创建任务 / Create a task

直接用中文或英文描述，Bot 会自动解析时间和内容：

```
/cron 每天早上9点检查服务器状态
/cron 每周一到周五晚8点同步数据
/cron 每周一上午10点发送本周任务总结
/cron every day at 9am check server status
/cron every Monday summarize my tasks
/cron in 30 minutes remind me about the meeting
```

### 管理任务 / Manage tasks

```
/cron list          # 查看所有定时任务 / List all tasks
/cron remove <id>   # 删除任务（id 从 list 获取）/ Remove task by id
/cron help          # 显示帮助 / Show help
```

> ⚠️ 定时任务是 **Pro 专属功能**。QQ 平台不支持主动推送，建议使用 Telegram 或企业微信。
> Scheduled tasks require **Pro**. QQ does not support push notifications; use Telegram or WeChat Work.

---

## 升级 Pro / Upgrade to Pro

Pro 版解锁全部功能：
Pro unlocks everything:

- ✅ 无限消息，无试用期限制 / Unlimited messages, no trial limit
- ✅ 多轮对话，保留完整上下文 / Multi-turn chat with full context
- ✅ 图片分析 / Image analysis
- ✅ 文件分析（PDF、Excel、CSV、代码等）/ File analysis (PDF, Excel, CSV, code, etc.)
- ✅ 会话历史，可随时恢复对话 / Session history with resume support
- ✅ 定时任务（/cron）/ Scheduled tasks (/cron)
- ✅ 无广告 / No ads

**购买地址 / Purchase:** [claudeanywhere.gumroad.com/l/claude-anywhere](https://claudeanywhere.gumroad.com/l/claude-anywhere)（$5.99/月）

购买后，使用 `/activate CA-XXXX-XXXX-XXXX-XXXX` 命令激活。
After purchase, activate with: `/activate CA-XXXX-XXXX-XXXX-XXXX`

---

## 常见问题 / FAQ

**Q: 启动时报错 `claude: command not found`**

A: Claude Code CLI 未安装或未在 PATH 中。运行以下命令安装：
```bash
npm install -g @anthropic-ai/claude-code
claude --version   # 验证
```
如仍报错，在 `.env` 中设置完整路径：
```ini
CLAUDE_PATH=/home/youruser/.local/bin/claude
```
用 `which claude` 或 `find / -name claude 2>/dev/null` 查找实际路径。

---

**Q: Telegram Bot 没有任何响应 / Telegram bot not responding**

A: 按以下步骤排查：
1. 确认 `TELEGRAM_BOT_TOKEN` 填写正确，`=` 后无空格
2. 确认服务正在运行：`systemctl status claude-anywhere` 或终端里直接运行 `npm run telegram`
3. 检查网络能否访问 Telegram：`curl -s https://api.telegram.org` 应有 JSON 响应
4. 确认你在 Telegram 里给 **你的 Bot** 发消息，不是给 BotFather

---

**Q: 报错 `409 Conflict`**

A: 同一个 Bot Token 有多个实例在同时运行。
```bash
pkill -f bridge-telegram
npm run telegram
```

---

**Q: 报错 `code 143` 或对话超时 / Timeout error**

A: Claude 执行超时（默认 10 分钟）。可在 `.env` 中增加超时时间：
```ini
CLAUDE_TIMEOUT_MS=900000   # 15 分钟
```

---

**Q: /sessions 没有显示我电脑上的会话 / /sessions not showing my desktop sessions**

A: 确保 `.env` 中的 `CLAUDE_CWD` 指向你的工作目录。
```ini
CLAUDE_CWD=/home/youruser/your-project
```

---

**Q: 三个平台的会话是共享的吗 / Are sessions shared across platforms?**

A: 是的！在 Telegram 创建的会话，可以在企业微信或 QQ 上用 `/resume` 继续，反之亦然。
Yes! Sessions created on Telegram can be resumed on WeCom or QQ with `/resume`, and vice versa.

---

**Q: 企业微信 Bot 没有响应 / WeChat Work bot not responding**

A: 检查 `WECOM_BOT_ID` 和 `WECOM_SECRET` 是否正确，确认企业微信管理后台中 Bot 已启用并分配给了相应的部门或用户。

---

**Q: 免费版试用期到了还能用吗 / Can I use after free trial?**

A: 试用期结束后需要升级 Pro。购买地址：[claudeanywhere.gumroad.com/l/claude-anywhere](https://claudeanywhere.gumroad.com/l/claude-anywhere)

---

**Q: 是否支持 Windows？/ Does it work on Windows?**

A: 支持，但推荐在 WSL2（Windows Subsystem for Linux）环境下运行。
Yes, but running inside WSL2 is recommended.

---

## 更新日志 / Changelog

查看完整版本历史：[CHANGELOG.md](CHANGELOG.md)

**v1.6.1** (2026-03-28) — 统一所有平台使用微信支付+机器码自动激活，移除 /buy 命令
**v1.6.0** (2026-03-27) — 微信支付自动开通 Pro，付款即激活，无需填写 Key
**v1.5.0** (2026-03-15) — QQ Bot 图片/文件分析，三平台一键启动
**v1.4.0** (2026-02-28) — 定时任务 `/cron`
**v1.3.0** (2026-02-10) — 跨平台会话恢复 `/sessions` `/resume`

---

## 联系 / Contact

有问题或建议，请联系：
For support or feedback:

📧 support@claudeanywhere.com

---

*Claude Anywhere — 随时随地，读写文件、执行命令、分析图片、管理代码。*
*Claude Anywhere — read files, write code, analyze images, manage code, wherever you are.*
