---
name: bingo-email
version: 1.0.0
license: MIT-0
description: >
  统一邮件管理技能，用于读取、发送、回复、转发邮件，以及管理草稿箱和文件夹。
  当用户提到"读邮件"、"发邮件"、"回复"、"草稿箱"、"未读邮件"、"收件箱"、
  "邮箱"等任何与电子邮件相关的操作时，使用此技能。替代 himalaya CLI，
  全部使用 Python 脚本操作任意 IMAP/SMTP 邮箱（腾讯企业邮箱、QQ邮箱、
  126/163 网易邮箱、Gmail、Outlook 等）。
  适用于邮件分类整理、批量处理、自动回复草稿生成等场景。
  支持 126/163 邮箱的 IMAP ID (RFC 2971) 要求。
metadata:
  openclaw:
    emoji: "📧"
    homepage: "https://github.com/soulcoolzzz/bingo-email"
    requires:
      bins:
        - python3
      config:
        - "~/.config/bingo-email/config.toml"
    install:
      - kind: uv
        package: imapclient
        bins: []
---

# bingo-email — 统一邮件管理

基于 Python IMAPClient + smtplib 的全功能邮件管理工具，支持**任意 IMAP/SMTP 邮箱**。

## 特性一览

| 特性 | 说明 |
|------|------|
| 多邮箱支持 | 腾讯企业邮箱、QQ邮箱、126/163、Gmail、Outlook + 自定义 |
| 126/163 兼容 | 自动处理 IMAP ID (RFC 2971) 要求 |
| 中文无乱码 | 草稿箱使用 base64 编码（非 quoted-printable） |
| 零外部依赖 | 仅需 `imapclient`（pip install 即可），无需编译 |
| 配置外置 | TOML 配置文件，不含硬编码凭据，可安全共享 |
| 文件权限 600 | `save_config` 后自动 chmod 600，仅本人可读 |
| 回复引用 | 自动附带原始邮件 inline quote（`>` 格式） |
| Reply-All | `--all` 标志一键回复所有人，智能排除自己 |
| 线程归并 | 自动设置 In-Reply-To / References 头 |
| 自动诊断 | `check` 命令非交互式检测依赖和配置状态 |

## 快速开始（AI 自动引导流程）

当用户首次触发邮件相关操作时，AI 应按以下流程自动执行：

### 0. 环境自检（自动，用户无感）

```bash
python3 <skill_path>/scripts/bingo_email.py check
```

- ✅ exit 0 → 直接执行用户请求的邮件操作
- ❌ exit 2 → 提示用户完成缺失步骤后继续

### 第 1 步：安装依赖（check 发现缺失时提示）

```bash
pip3 install imapclient
```

### 第 2 步：初始化配置（check 发现缺失时提示）

```bash
# 运行交互式向导（推荐）
python3 <skill_path>/scripts/bingo_email.py init
```

向导会引导你选择邮箱服务商并填写账号密码。支持预设模板：

| 编号 | 服务商 | 说明 |
|------|--------|------|
| 1 | **腾讯企业邮箱** | `imap.exmail.qq.com` (默认 TLS) |
| 2 | QQ 邮箱 | `imap.qq.com` |
| 3 | **163 网易邮箱** | `imap.163.com` — **自动启用 IMAP ID** |
| 4 | **126 网易邮箱** | `imap.126.com` — **自动启用 IMAP ID** |
| 5 | Gmail | `imap.gmail.com`（需应用专用密码） |
| 6 | Outlook | `outlook.office365.com`（支持 STARTTLS） |
| 7+ | 自定义 | 手动输入服务器地址 |

> **关于授权码**：大部分邮箱不使用登录密码，而是使用「授权码」或「应用专用密码」。
> - 腾讯企业邮箱：企业邮箱后台 → 设置 → POP/SMTP 服务
> - QQ 邮箱：设置 → 账户 → POP3/SMTP服务 → 开启并获取授权码
> - 163/126：设置 → POP3/SMTP/IMAP → 开启并获取授权码
> - Gmail：Google Account → Security → App Passwords（需要开启 2FA）

### 第 3 步：验证连接

```bash
python3 <skill_path>/scripts/bingo_email.py test
```

输出示例：
```
正在测试连接...
  邮箱: you@example.com
  IMAP: imap.example.com:993
  SMTP: smtp.example.com:465

  ✓ IMAP 连接成功 — 收件箱共 42 封邮件
  ✓ SMTP 连接成功
```

看到两个 ✓ 就说明配置正确。

---

## 配置文件详解

配置保存在 `~/.config/bingo-email/config.toml`：

> ⚠️ **安全警告**：此文件包含明文密码/授权码！
> - 文件权限已自动设为 **600**（仅本人可读），请勿修改权限
> - **绝对不要**将此文件提交到 Git / GitHub（已通过 `.gitignore` 排除）
> - 分享 skill 给他人时，只分享代码，不分享此文件
> - 如果不小心上传了，**立即轮换授权码**

```toml
# bingo-email 配置文件
[account]
email = "your@email.com"
display_name = "Your Name"

[imap]
host = "imap.exmail.qq.com"
port = 993
encryption = "tls"           # tls | starttls | none
login = "your@email.com"
password = "your_auth_code"
require_imap_id = false       # ⚠️ 关键字段！126/163 必须设为 true

[smtp]
host = "smtp.exmail.qq.com"
port = 465
encryption = "tls"           # tls | starttls | none
login = "your@email.com"
password = "your_auth_code"
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `account.email` | ✅ | 你的邮箱地址 |
| `account.display_name` | ❌ | 发件显示名称 |
| `imap.host` | ✅ | IMAP 服务器地址 |
| `imap.port` | ❌ | IMAP 端口（默认 993） |
| `imap.encryption` | ❌ | 加密方式：`tls`(SSL), `starttls`, `none` |
| `imap.login` | ❌ | IMAP 登录名（默认同 email） |
| `imap.password` | ✅ | 授权码或密码 |
| `imap.require_imap_id` | ❌ | **是否发送 IMAP ID 命令**（126/163 必须=true） |
| `smtp.host` | ✅ | SMTP 服务器地址 |
| `smtp.port` | ❌ | SMTP 端口（默认 465） |
| `smtp.encryption` | ❌ | 加密方式（同 imap） |
| `smtp.login` | ❌ | SMTP 登录名（默认同 email） |
| `smtp.password` | ✅ | 授权码或密码（可与 imap 共用） |

---

## ⚠️ 126 / 163 网易邮箱特殊说明

### 问题背景

网易的 126 和 163 邮箱**强制要求 RFC 2971 IMAP ID 扩展**。客户端必须在 LOGIN 之前或之后立即发送 `ID` 命令，否则服务器会拒绝登录并返回 `"Unsafe Login"` 错误。

### 解决方案

bingo-email 内置了两种连接模式：

1. **标准模式**（`require_imap_id = false`）：使用 imapclient 库正常连接。适用于腾讯企业邮箱、QQ、Gmail、Outlook 等大多数邮箱服务商。

2. **IMAP ID 模式**（`require_imap_id = true`）：通过 raw SSL socket 手动实现完整的 IMAP 握手流程：
   ```
   TCP Connect → TLS Handshake → CAPABILITY → ID → LOGIN → [Ready]
   ```

### 配置方法

选择 **126** 或 **163** 预设模板时，`require_imap_id` 会**自动设为 true**。手动配置时确保：

```toml
[imap]
host = "imap.163.com"        # 或 imap.126.com
require_imap_id = true        # ← 这行是关键
```

### 技术细节

IMAP ID 命令格式（RFC 2971）：

```
A02 ID (("name" "bingo-email") ("version" "1.0"))
```

这告诉服务器客户端的身份信息，满足网易的安全策略要求。标准 IMAP 客户库（如 imapclient）默认不发送此命令，因此需要对 126/163 做特殊处理。

---

## 使用方式

```bash
python3 <skill_path>/scripts/bingo_email.py <command> [args...]
```

### 支持的全部命令

#### 初始化 & 测试 & 环境检查

```bash
python3 bingo_email.py init              # 交互式初始化配置（首次必做）
python3 bingo_email.py test              # 测试 IMAP/SMTP 连接
python3 bingo_email.py check             # 非交互式环境检查（自动诊断依赖+配置）
```

> **🤖 AI Agent 注意**：在执行任何邮件操作之前，**必须先运行 `check` 命令**确认环境就绪。
> - 如果 exit code = 0 → 环境正常，继续执行用户请求的操作
> - 如果 exit code ≠ 0 → 根据输出提示用户完成缺失的步骤（安装依赖或运行 init）

#### 读取类

```bash
python3 bingo_email.py list [N]          # 列出最近 N 封邮件（默认20封）
python3 bingo_email.py unread [N]        # 列出未读邮件
python3 bingo_email.py read <id>         # 读取指定 ID 的邮件详情
python3 bingo_email.py folders           # 列出所有文件夹
```

#### 发送类

```bash
python3 bingo_email.py send <to> <subject> [--body "正文"]
python3 bingo_email.py reply <id> [--body "回复正文"] [--all]        # --all = 回复所有人
python3 bingo_email.py forward <id> <to> [--body "附言"]
```

> **回复功能说明**：
> - `reply` 默认只回复发件人，自动附带**原始邮件 inline quote 引用**（标准 `>` 格式）
> - `reply ... --all` 为 **Reply-All** 模式，额外 Cc 给原始邮件 To/Cc 中的其他收件人（自动排除自己）
> - 回复邮件自动设置 `In-Reply-To` 和 `References` 头，确保邮件客户端能正确归并对话线程
> - `draft-reply` 同样支持 `--all` 参数，保存为回复全部草稿

#### 草稿类

```bash
python3 bingo_email.py draft --to <addr> --subject <subj> [--body "正文"]
python3 bingo_email.py draft-reply <id> [--body "回复正文"] [--all]   # --all = 回复所有人草稿
```

#### 管理类

```bash
python3 bingo_email.py delete <id>        # 删除邮件（移至已删除）
python3 bingo_email.py move <id> <folder> # 移动到其他文件夹
```

### 正文输入方式

三种方式传入邮件正文（优先级从高到低）：

1. **`--body` 参数**（推荐用于脚本调用）：
   ```bash
   python3 bingo_email.py send a@b.com "主题" --body "这是正文内容"
   ```

2. **管道传入**：
   ```bash
   echo "正文内容" | python3 bingo_email.py send a@b.com "主题"
   ```

3. **交互输入**（不带以上两种时自动进入）：
   ```bash
   python3 bingo_email.py send a@b.com "主题"
   # 请输入邮件正文（输入空行结束）:
   # > 第一行
   # > 第二行
   # > （直接回车结束）
   ```

---

## 输出格式

| 操作 | 输出格式 | 说明 |
|------|----------|------|
| `list` / `unread` | 表格 | ID / 标记(*=未读) / 主题(截断40字) / 发件人 / 日期 |
| `read` | 结构化文本 | From, To, Cc, Subject, Date, Message-ID + 正文 |
| `folders` | 列表 | 文件夹名称 + flags |
| `send/reply/forward/draft` | 状态行 | `✓ 操作结果` |
| 错误 | 以 `错误:` 开头 | 后跟具体原因 |

---

## 与 himalaya 对比

| 维度 | himalaya | bingo-email |
|------|----------|-------------|
| 语言 | Rust CLI | Python 脚本 |
| 中文草稿 | quoted-printable → **乱码** ✗ | base64 → **正常** ✓ |
| 126/163 | 需编译自定义版本 | 配置项一键切换 |
| 配置 | TOML 文件 | TOML 文件（兼容格式） |
| 依赖 | 单二进制 | imapclient (~1MB pip 包) |
| 可定制性 | 需改源码重编译 | 直接改 Python |

---

## 安装 & 分享给他人

### 方法一：作为 WorkBuddy Skill 安装

将整个 `bingo-email/` 目录放到 WorkBuddy skills 目录：

```bash
# 复制到用户级 skills 目录（所有项目可用）
cp -r bingo-email/ ~/.workbuddy/skills/

# 或复制到项目级 skills 目录（仅当前项目可用）
cp -r bingo-email/ .workbuddy/skills/
```

然后运行 `init` 命令配置自己的邮箱即可。

### 方法二：独立使用（不需要 WorkBuddy）

```bash
# 1. 下载脚本
curl -o ~/bin/bingo_email.py https://your-host/scripts/bingo_email.py
chmod +x ~/bin/bingo_email.py

# 2. 安装依赖
pip3 install imapclient

# 3. 初始化配置
~/bin/bingo_email.py init

# 4. 使用
~/bin/bingo_email.py unread
```

### 分享检查清单

给其他人使用前，确认对方完成以下步骤：

- [ ] Python 3.8+ 已安装
- [ ] `pip3 install imapclient`
- [ ] 运行 `bingo_email.py init` 完成配置
- [ ] 运行 `bingo_email.py test` 验证连接
- [ ] 如果是 126/163 邮箱，确认 `init` 时选择了对应预设（或手动设 `require_imap_id = true`）

> **新用户快速验证**：直接运行 `python3 bingo_email.py check` 即可一键诊断所有前置条件。

---

## 🔒 安全 & 开源分享

### 已内置的安全措施

| 措施 | 实现方式 |
|------|----------|
| **文件权限 600** | `save_config()` 写入后自动 `chmod 0o600`，仅文件所有者可读写 |
| **密码输入无回显** | `init` 命令使用 `getpass.getpass()` 终端不显示明文 |
| **Git 防泄露** | `.gitignore` 已排除 `config.toml` 和 `__pycache__/` |
| **无硬编码凭据** | 源代码中不含任何真实密码或 token |

### 开源到 GitHub 的检查清单

发布前确认以下事项：

- [ ] **`config.toml` 不在仓库中**：确认 `.gitignore` 包含 `config.toml`
- [ ] **历史提交无凭据**：`git log -p -- config.toml` 确认从无此文件
- [ ] **无敏感信息在示例中**：SKILL.md / README 中的配置示例只用 `your_auth_code` 占位符
- [ ] **添加 LICENSE**：建议 MIT 或 Apache 2.0
- [ ] **添加 SECURITY.md**：告知用户如何安全报告漏洞

### 如果不小心泄露了授权码

1. **立即去邮箱后台轮换（重新生成）授权码**
2. 更新本地 `config.toml`
3. 如果已推送到 GitHub：
   ```bash
   # 使用 BFG 或 git-filter-repo 从历史中彻底删除
   # 然后强制推送（需谨慎！）
   ```

### 用户侧安全建议（可写入文档）

最终用户应了解：

1. 保持 `config.toml` 权限为 `600`（程序自动设置）
2. 不要在公共场合截图包含此文件内容
3. 定期检查是否有未授权的邮件操作（查看"已发送"文件夹）
4. 多设备使用时各自独立配置，不要复制粘贴配置文件

---

## 常见问题

### Q: 提示 "未找到配置文件"？
**A:** 首次使用必须先运行 `python3 bingo_email.py init` 进行配置。

### Q: 登录失败 "Authentication failed"？
**A:** 检查以下几点：
1. 是否使用了**授权码**而不是登录密码？（QQ/163/126/腾讯企业邮箱都是授权码）
2. 授权码是否有过期？部分服务的授权码会定期失效
3. Gmail 必须使用**应用专用密码**（App Password），不是 Google 账号密码

### Q: 126/163 报 "Unsafe Login"？
**A:** 确认配置中 `require_imap_id = true`。如果用的旧版配置，重新运行 `init` 选择 126 或 163 模板即可。

### Q: 草稿箱中文乱码？
**A:** 这个问题在 bingo-email 中**不会出现**——草稿统一使用 MIMEText + base64 编码写入。如果遇到乱码请报 bug。

### Q: 如何切换邮箱账号？
**A:** 编辑 `~/.config/bingo-email/config.toml` 修改账号信息，或重新运行 `init` 覆盖配置。

---

## 注意事项

- 企业邮箱已发送文件夹通常名为 `Sent Messages`（不是 `Sent`）
- 草稿箱为 `Drafts`
- 删除操作默认移至"已删除"文件夹，不做物理删除
- Message ID 在列表中显示为整数 UID，每次刷新可能变化（IMAP 特性）
