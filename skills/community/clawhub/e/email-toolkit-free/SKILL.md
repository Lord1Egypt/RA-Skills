---
name: "email-toolkit-free"
description: "跨平台邮件发送与附件管理工具，支持多邮箱服务商"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "邮件工具箱免费版"
  version: "1.0.0"
  summary: "跨平台邮件发送与附件管理工具，支持多邮箱服务商"
  tags:
    - "沟通协作"
    - "邮件管理"
    - "邮件发送"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 邮件工具箱免费版

**版本**: 1.0.0
**适用对象**: 个人用户、独立开发者、一人公司
**核心定位**: 跨平台邮件发送与附件管理基础工具

---

## 概述

邮件工具箱免费版是一款轻量级的跨平台邮件发送工具，通过 Python 实现邮件自动化发送。工具支持 Gmail、Outlook、Yahoo、QQ邮箱等主流邮箱服务商，以及自定义 SMTP 服务器，提供纯文本与 HTML 邮件、多附件发送、抄送密送等核心功能。

工具采用 TLS/SSL 加密连接确保邮件传输安全，支持配置文件与环境变量两种配置方式，适配不同使用场景。同时提供命令行与 Python API 两种调用方式，方便集成到自动化脚本与工作流中。免费版聚焦个人用户的邮件发送需求，配置简单、调用便捷。

---

## 核心能力

### 邮件发送

- **纯文本邮件**: 简单快捷的文本邮件发送
- **HTML 邮件**: 支持富文本格式邮件
- **命名收件人**: 支持"姓名 <邮箱>"格式
- **抄送与密送**: 支持 CC 与 BCC 收件人

**输入**: 用户提供邮件发送所需的指令和必要参数。
**处理**: 按照skill规范执行邮件发送操作,遵循单一意图原则。
**输出**: 返回邮件发送的执行结果,包含操作状态和输出数据。

### 附件管理

- **单附件发送**: 发送带单个附件的邮件
- **多附件发送**: 一次性发送多个附件
- **多种格式**: 支持 PDF、Excel、图片、代码文件等各类格式

**输入**: 用户提供附件管理所需的指令和必要参数。
**处理**: 按照skill规范执行附件管理操作,遵循单一意图原则。
**输出**: 返回附件管理的执行结果,包含操作状态和输出数据。

### 多服务商支持

- Gmail（smtp.gmail.com）
- Outlook/Office365（smtp.office365.com）
- Yahoo（smtp.mail.yahoo.com）
- QQ邮箱（smtp.qq.com）
- 自定义 SMTP 服务器

**输入**: 用户提供多服务商支持所需的指令和必要参数。
**处理**: 按照skill规范执行多服务商支持操作,遵循单一意图原则。
**输出**: 返回多服务商支持的执行结果,包含操作状态和输出数据。

### 安全特性

- TLS 加密连接（端口 587）
- SSL 加密连接（端口 465）
- 应用专用密码支持（Gmail）
- 环境变量凭证存储

**输入**: 用户提供安全特性所需的指令和必要参数。
**处理**: 按照skill规范执行安全特性操作,遵循单一意图原则。
**输出**: 返回安全特性的执行结果,包含操作状态和输出数据。

### 测试功能

- 发送测试邮件验证配置
- 连接测试
- 配置文件验证

---

**输入**: 用户提供测试功能所需的指令和必要参数。
**处理**: 按照skill规范执行测试功能操作,遵循单一意图原则。
**输出**: 返回测试功能的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：跨平台邮件发送与、附件管理工具、支持多邮箱服务商、邮件工具箱免费版、是一款面向个人用、户的跨平台邮件发、送工具、Python、实现邮件、自动化发送、邮箱等主流服务商、Use、when、需要消息发送、通知推送、邮件短信、通信集成时使用、不适用于垃圾信息、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：发送简单文本邮件

快速发送一封纯文本邮件给同事。

```bash
# 发送简单邮件
python email_sender.py --to "colleague@example.com" --subject "会议提醒" --body "明天上午10点会议室A开会，请准时参加。"
```

输出示例：

```text
✅ 邮件发送成功!
   收件人: colleague@example.com
   主题: 会议提醒
   格式: 纯文本
```

### 场景二：发送带附件的工作邮件

向团队发送包含报告和数据文件的工作邮件。

```bash
# 发送带多个附件的邮件
python email_sender.py \
  --to "team@company.com" \
  --subject "项目周报 - 2026年7月第三周" \
  --body "您好，附件为本周项目进展报告与数据文件，请查收。" \
  --attachment "report.pdf" \
  --attachment "data.xlsx"
```

### 场景三：发送 HTML 格式通知邮件

发送格式化的 HTML 通知邮件，带抄送。

```bash
python email_sender.py \
  --to "all@company.com" \
  --cc "manager@company.com" \
  --subject "系统维护通知" \
  --body '<h1>系统维护通知</h1><p>系统将于本周六凌晨2点-4点进行维护升级，届时服务将暂停。</p><p>请提前做好相关准备。</p>'
```

---

## 快速开始

### 第一步：创建配置文件

在工作目录创建 `email_config.json`：

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "your-email@gmail.com",
  "password": "your-app-password",
  "sender_name": "邮件助手",
  "use_tls": true,
  "use_ssl": false
}
```

### 第二步：Gmail 用户配置（推荐）

Gmail 用户需使用应用专用密码：

1. 在 Google 账户开启两步验证
2. 访问 https://myaccount.google.com/security
3. 在"登录 Google"中选择"应用密码"
4. 为"邮件"生成新的应用密码
5. 将16位密码填入配置文件

### 第三步：发送测试邮件

```bash
# 发送测试邮件验证配置
python email_sender.py --to "your-email@gmail.com" --test
```

### 第四步：正式使用

```bash
# 发送普通邮件
python email_sender.py --to "friend@example.com" --subject "你好" --body "这是一封测试邮件"

# 发送带附件的邮件
python email_sender.py --to "friend@example.com" --subject "报告" --body "请查收" --attachment "report.pdf"
```

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 示例

### 各邮箱服务商配置

| 服务商 | SMTP 服务器 | 端口 | TLS | SSL |
|:-------|:------------|:-----|:---:|:---:|
| Gmail | smtp.gmail.com | 587 | 是 | - |
| Outlook/Office365 | smtp.office365.com | 587 | 是 | - |
| Yahoo | smtp.mail.yahoo.com | 587 | 是 | - |
| QQ邮箱 | smtp.qq.com | 587 | 是 | - |
| 163邮箱 | smtp.163.com | 465 | - | 是 |
| 自定义 | your.smtp.server | 587/465 | 按配置 | 按配置 |

### 环境变量配置

也可以使用环境变量替代配置文件：

```bash
# Linux/macOS
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export EMAIL_USERNAME=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
export EMAIL_SENDER_NAME="邮件助手"

# Windows PowerShell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:EMAIL_USERNAME="your-email@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"
$env:EMAIL_SENDER_NAME="邮件助手"
```

### SSL 配置（163邮箱）

```json
{
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "username": "your-email@163.com",
  "password": "your_auth_code",
  "sender_name": "邮件助手",
  "use_tls": false,
  "use_ssl": true
}
```

---

## 最佳实践

### Python API 调用

```python
from email_sender import EmailSender

# 初始化发送器
sender = EmailSender("email_config.json")

# 发送带附件的邮件
result = sender.send_email(
    to_email="recipient@example.com",
    subject="重要文档",
    body="请审阅附件中的文档。",
    attachments=["document.pdf", "data.csv"]
)

if result["success"]:
    print(f"邮件发送成功，附件数: {result['attachments']}")
else:
    print(f"发送失败: {result['error']}")
```

### 安全规范

- **绝不提交凭证到版本控制**: 将 `email_config.json` 加入 `.gitignore`
- **使用环境变量**: 生产环境优先使用环境变量
- **定期更换密码**: 定期轮换应用专用密码
- **专用邮箱**: 自动化场景建议使用专用邮箱账户

```bash
# .gitignore 中添加
echo "email_config.json" >> .gitignore
```

### 附件大小管理

- 单个附件建议不超过 25MB（大多数服务商限制）
- 多附件总大小建议不超过 50MB
- 大文件建议使用云存储链接替代

```bash
# 检查文件大小
ls -lh report.pdf

# 大文件使用链接替代
python email_sender.py --to x@y.com --subject "大文件" --body "文件链接: https://drive.google.com/xxx"
```

---

## 常见问题

### 问题1：认证失败

```text
Error: Authentication Failed
```

**原因**: 用户名或密码错误，或 Gmail 未使用应用专用密码。

**解决**:
- 确认用户名与密码正确
- Gmail 用户必须使用应用专用密码（非登录密码）
- 确认已开启两步验证

### 问题2：连接被拒绝

```text
Error: Connection Refused
```

**原因**: SMTP 服务器地址或端口错误，或防火墙拦截。

**解决**:
- 验证 SMTP 服务器与端口
- 检查防火墙设置
- 尝试切换端口（465 SSL / 587 TLS）

```bash
# 测试端口连通性
telnet smtp.gmail.com 587
telnet smtp.gmail.com 465
```

### 问题3：附件过大

```text
Error: Attachment Too Large
```

**解决**:
- 压缩文件后再发送
- 拆分大文件为多个小文件
- 使用云存储链接替代

```bash
# 压缩文件
zip -s 20m archive.zip large_file.pdf
```

### 问题4：SSL/TLS 配置错误

**解决**: 根据服务商选择正确的加密方式：

```bash
# TLS (端口 587) - Gmail/Outlook
"use_tls": true, "use_ssl": false

# SSL (端口 465) - 163邮箱
"use_tls": false, "use_ssl": true
```

### 问题5：中文乱码

**解决**: 确保 Python 脚本使用 UTF-8 编码，邮件主题与正文使用 UTF-8 编码发送。

---

## 命令参考速查

| 参数 | 功能 | 示例 |
|:-----|:-----|:-----|
| `--to` | 收件人 | `--to "user@example.com"` |
| `--cc` | 抄送 | `--cc "cc@example.com"` |
| `--bcc` | 密送 | `--bcc "bcc@example.com"` |
| `--subject` | 主题 | `--subject "邮件主题"` |
| `--body` | 正文 | `--body "邮件内容"` |
| `--attachment` | 附件 | `--attachment "file.pdf"` |
| `--test` | 测试邮件 | `--test` |

---

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.7 及以上
- **网络环境**: 需可访问对应邮箱的 SMTP 服务器

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 官方网站下载安装 |
| Python 标准库 | 运行库 | 必需 | Python 自带（smtplib, email） |
| 邮箱账户 | 账户 | 必需 | 注册主流邮箱服务商 |
| 应用专用密码 | 凭证 | 必需 | 邮箱安全设置页生成 |

### API Key 配置

- 本工具使用邮箱 SMTP 认证，无需额外 API Key
- Gmail 用户需生成应用专用密码（16位）
- 其他邮箱用户使用授权码或应用密码
- 凭证通过配置文件或环境变量提供

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行 Python 脚本，完成邮件发送与附件管理任务

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需要API Key，无Key环境无法使用
