---
name: email-cron-handler
description: 邮件指令定时处理任务。通过 IMAP/SMTP 自动接收并执行邮件中的指令，以邮件形式回复执行结果。适用于：(1) 创建定时任务监控指定邮箱 (2) 通过邮件下发指令给 AI Agent (3) 实现邮件驱动的自动化工作流。需配置：收件邮箱、SMTP/IMAP 配置、指令发件人白名单。
---

# Email Cron Handler

通过邮件接收指令、定时执行并回复结果的自动化工作流。

## 核心功能

- 定时检查指定邮箱的新邮件
- 过滤白名单发件人的指令邮件
- 执行邮件中的指令并回复结果
- 支持成功/失败/超时状态反馈

## 文件结构

```
email-cron-handler/
├── SKILL.md
├── scripts/
│   ├── process_email.py      # 主处理脚本
│   └── config.json.example   # 配置示例文件
└── references/
    └── config-template.md    # 详细配置说明
```

## 快速开始

### Step 1: 配置邮箱参数

```bash
cd ~/.agents/skills/email-cron-handler/scripts
cp config.json.example config.json
# 编辑 config.json，填入你的实际配置
```

配置项说明：
- `email`: 你的邮箱账号
- `password`: 邮箱授权码（QQ邮箱需在设置中开启IMAP/SMTP后获取）
- `imap_host`/`imap_port`: IMAP 服务器地址和端口
- `smtp_host`/`smtp_port`: SMTP 服务器地址和端口
- `whitelist_sender`: 白名单发件人（只处理这些地址发来的邮件）

### Step 2: 初始化存储目录

```bash
mkdir -p ~/.openclaw/workspace/memory
echo '[]' > ~/.openclaw/workspace/memory/processed_emails.json
```

### Step 3: 创建定时任务

**方式一：使用脚本（推荐）**

Cron 任务只需执行简单逻辑：
1. 调用 `python process_email.py fetch` 获取未处理邮件
2. 对每封邮件执行指令
3. 调用 `python process_email.py reply <uid> <结果>` 回复结果

**方式二：直接用 LLM（当前方式）**

保持现有指令模板即可，脚本作为备用/调试工具。

## 脚本用法

```bash
# 获取未处理邮件
python process_email.py fetch

# 回复邮件（内容直接提供）
python process_email.py reply <uid> "执行结果内容"

# 回复邮件（从文件读取内容）
python process_email.py reply <uid> --file result.txt

# 标记邮件为已处理（不回复）
python process_email.py mark <uid>
```

## 常见问题

**Q: 如何测试脚本？**
```bash
cd ~/.agents/skills/email-cron-handler/scripts
python process_email.py fetch
```

**Q: 授权码在哪里获取？**
A: QQ 邮箱 → 设置 → 账户 → 开启 IMAP/SMTP 服务 → 获取授权码

**Q: 脚本和 LLM 指令选哪个？**
A: 
- 脚本方式：稳定快速，适合简单场景
- LLM 指令方式：灵活可扩展，适合复杂指令执行
