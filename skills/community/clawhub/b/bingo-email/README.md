# 📧 bingo-email

> 统一邮件管理工具，支持**任意 IMAP/SMTP 邮箱**，专为 AI Agent 设计。

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![ClawHub](https://img.shields.io/badge/ClawHub-bingo--email-purple.svg)](https://clawhub.ai)

一个基于 Python 的全功能邮件管理 CLI，作为 [OpenClaw](https://openclaw.ai/) / [ClawHub](https://clawhub.ai) 的 Skill 运行，也可独立使用。

## ✨ 特性

- 🌍 **多邮箱支持** — 腾讯企业邮箱、QQ邮箱、126/163、Gmail、Outlook + 自定义
- 🔧 **126/163 兼容** — 自动处理 IMAP ID (RFC 2971) 要求，告别 "Unsafe Login"
- 🇨🇳 **中文零乱码** — 草稿箱使用 base64 编码（非 quoted-printable）
- 📦 **轻量依赖** — 仅需 `imapclient`，纯 Python 无编译
- 🔒 **安全设计** — 配置文件自动 chmod 600、密码输入无回显、.gitignore 防泄露
- 📩 **完整功能** — 读取、发送、回复、转发、草稿、删除、移动
- 🧵 **线程归并** — 自动设置 In-Reply-To / References 头
- 🤖 **AI 友好** — `check` 命令一键诊断，Agent 无需人工干预

## 🚀 快速开始

### 方式一：作为 ClawHub Skill 安装（推荐）

```bash
clawhub install bingo-email
```

然后运行 `bingo_email.py init` 完成配置即可。

### 方式二：从 GitHub 克隆

```bash
git clone https://github.com/soulcoolzzz/bingo-email.git
cd bingo-email
pip3 install imapclient
python3 scripts/bingo_email.py init
```

### 方式三：独立使用

```bash
# 1. 下载脚本
curl -o ~/bin/bingo_email.py https://raw.githubusercontent.com/soulcoolzzz/bingo-email/main/scripts/bingo_email.py
chmod +x ~/bin/bingo_email.py

# 2. 安装依赖
pip3 install imapclient

# 3. 初始化配置
~/bin/bingo_email.py init
```

## 📖 使用方式

### 初始化 & 检查

```bash
python3 bingo_email.py init      # 交互式初始化（首次必做）
python3 bingo_email.py test      # 测试连接
python3 bingo_email.py check     # 环境诊断（AI Agent 优先调用）
```

### 读取邮件

```bash
python3 bingo_email.py list [N]       # 最近 N 封（默认20）
python3 bingo_email.py unread [N]     # 未读邮件
python3 bingo_email.py read <id>      # 阅读详情
python3 bingo_email.py folders        # 文件夹列表
```

### 发送 & 回复

```bash
python3 bingo_email.py send <to> <subject> --body "正文"
python3 bingo_email.py reply <id> --body "回复" [--all]
python3 bingo_email.py forward <id> <to> --body "附言"
```

### 草稿 & 管理

```bash
python3 bingo_email.py draft --to <addr> --subject <subj> --body "正文"
python3 bingo_email.py draft-reply <id> --body "回复" [--all]
python3 bingo_email.py delete <id>
python3 bingo_email.py move <id> <folder>
```

## ⚙️ 配置

配置文件位于 `~/.config/bingo-email/config.toml`，首次运行 `init` 自动生成。

可参考 [config.toml.example](config.toml.example) 模板手动创建：

```toml
[account]
email = "your@email.com"
display_name = "Your Name"

[imap]
host = "imap.exmail.qq.com"
port = 993
encryption = "tls"
password = "your_auth_code"

[smtp]
host = "smtp.exmail.qq.com"
port = 465
encryption = "tls"
password = "your_auth_code"
```

> ⚠️ **安全提示**：此文件包含明文密码，程序自动设置权限 600。切勿提交到 Git。

## 🔒 安全设计

| 措施 | 说明 |
|------|------|
| **文件权限 600** | `save_config()` 写入后自动 chmod，仅本人可读 |
| **密码无回显** | `init` 使用 `getpass.getpass()` |
| **Git 防泄露** | `.gitignore` 排除 `config.toml` |
| **无硬编码凭据** | 源代码不含任何真实密码 |

详见 [SKILL.md](SKILL.md) 的「🔒 安全 & 开源分享」章节。

## 📁 目录结构

```
bingo-email/
├── SKILL.md                 # Skill 定义（AI Agent 读取）
├── README.md                # 本文件
├── LICENSE                  # MIT-0 协议
├── config.toml.example      # 配置模板
├── .gitignore               # Git 排除规则
└── scripts/
    └── bingo_email.py       # 主程序（~900行）
```

## 🤝 贡献

欢迎 PR！请确保：

1. 代码通过 `python3 -m py_compile scripts/bingo_email.py`
2. 不在代码中硬编码任何凭据
3. 新功能附带 SKILL.md 文档更新

## 📄 许可证

[MIT-0](LICENSE) — 无 attribution 要求，自由使用。
