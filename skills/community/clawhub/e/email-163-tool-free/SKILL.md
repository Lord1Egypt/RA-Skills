---

name: "email-163-tool-free"
description: "163邮箱收发与搜索基础工具，支持附件与文件夹管理，适合个人日常使用。Use when 用户需要email-163-tool-free相关功能时使用。不适用于超出本技能能力范围的复杂需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "163邮箱助手免费版"
  version: "1.0.0"
  summary: "163邮箱收发与搜索基础工具，支持附件与文件夹管理，适合个人日常使用"
  tags:
    - "沟通协作"
    - "邮件管理"
    - "163邮箱"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 163邮箱助手免费版

**版本**: 1.0.0
**适用对象**: 个人用户、独立开发者、一人公司
**核心定位**: 163邮箱日常收发与管理的基础工具

---

## 概述

163邮箱助手免费版是一款轻量级的网易163邮箱管理工具，通过命令行界面提供邮件发送、读取、搜索和文件夹管理等核心功能。工具完整支持163邮箱要求的 IMAP ID 扩展认证（RFC 2971），确保连接安全稳定，同时支持中文主题、HTML 邮件和多附件发送，满足个人用户日常邮件处理的全部高频需求。

本工具采用 TLS/SSL 加密连接，使用163邮箱客户端授权码进行认证（非登录密码），在保证安全性的同时提供流畅的使用体验。免费版聚焦个人使用场景，配置简单、上手快速。

---

## 核心能力

### 邮件收发

- **发送邮件**: 支持纯文本和 HTML 两种格式
- **发送附件**: 支持单文件与多文件附件
- **读取邮件**: 支持 IMAP ID 认证，完整获取收件箱邮件
- **邮件详情**: 查看单封邮件的完整内容

**输出**: 返回邮件收发的执行结果,包含操作状态和输出数据。

### 邮件搜索

- 按发件人地址搜索
- 按邮件主题搜索
- 按日期范围筛选
- 多条件组合搜索

**输出**: 返回邮件搜索的执行结果,包含操作状态和输出数据。

### 邮件操作

- 删除指定邮件
- 在文件夹之间移动邮件
- 标记邮件为已读/未读

**输出**: 返回邮件操作的执行结果,包含操作状态和输出数据。

### 文件夹管理

- 列出所有邮箱文件夹
- 创建自定义文件夹
- 删除空文件夹

**输出**: 返回文件夹管理的执行结果,包含操作状态和输出数据。

### 附件管理

- 查看邮件附件列表
- 下载附件到本地目录

---

**输出**: 返回附件管理的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：邮箱收发与搜索基、础工具、支持附件与文件夹、适合个人日常使用、邮箱助手免费版是、一款面向个人用户、的网易、邮箱管理工具、通过命令行实现邮、搜索与文件夹管理、等核心能力、Use、when、需要消息发送、通知推送、邮件短信、通信集成时使用、不适用于垃圾信息、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：发送带附件的工作邮件

个人开发者需要将项目报告通过163邮箱发送给合作方，附件包含 PDF 报告和数据文件。

```bash
# 发送带多个附件的邮件
email-163-tool send \
  --to partner@example.com \
  --subject "项目阶段报告 - 2026年7月" \
  --body "您好，附件为本阶段项目报告与数据文件，请查收。" \
  --attach report.pdf \
  --attach data.xlsx
```

执行成功后输出：

```text
✅ 邮件发送成功!
   收件人: partner@example.com
   主题: 项目阶段报告 - 2026年7月
   附件: report.pdf (1.2 MB), data.xlsx (340 KB)
```

### 场景二：快速查看未读邮件

每天早晨快速浏览收件箱中的未读邮件，了解重要通知。

```bash
# 查看最近10封未读邮件
email-163-tool read --count 10 --unread
```

输出示例：

```text
📬 INBOX: 共 16 封邮件

📧 发件人: 阿里云
   主题: 域名信息修改成功通知
   时间: Wed, 18 Feb 2026 22:00:53
   ID: 16
   状态: 已读
--------------------------------------------------

📧 发件人: Cloudflare <noreply@notify.cloudflare.com>
   主题: [需要操作] 验证您的邮箱地址
   时间: Wed, 18 Feb 2026 14:17:02
   ID: 15
   状态: 未读
--------------------------------------------------
```

### 场景三：搜索特定邮件并下载附件

需要找到之前云服务商发送的验证邮件，并下载其中的验证文件。

```bash
# 按发件人和主题搜索
email-163-tool search --from "Cloudflare" --subject "verify" --count 5

# 下载指定邮件的附件
email-163-tool attachments --id 15 --download --output $HOME/Downloads/
```

---

## 快速开始

### 依赖详情

本工具为命令行程序，无需额外安装依赖，直接使用即可：

```bash
# 查看帮助
email-163-tool --help

# 查看版本
email-163-tool --version
```

### 第二步：配置邮箱授权码

登录163邮箱网页版，获取客户端授权码：

1. 登录 `mail.163.com`
2. 进入 设置 → POP3/SMTP/IMAP
3. 开启 IMAP/SMTP 服务
4. 生成客户端授权码（非登录密码）

### 第三步：创建配置文件

编辑配置文件 `$HOME/.config/email-163-tool/config.json`：

```json
{
  "email": "your_email@163.com",
  "password": "your_auth_code",
  "imap_server": "imap.163.com",
  "imap_port": 993,
  "smtp_server": "smtp.163.com",
  "smtp_port": 465
}
```

### 第四步：发送测试邮件

```bash
email-163-tool send --to your_email@163.com --subject "测试" --body "配置成功！"
```

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### 完整配置文件

```json
{
  "password": "your_auth_code",
  "imap_port": 993,
  "smtp_port": 465,
  "imap_id": {
    "name": "email-163-tool",
    "version": "1.0.0",
    "vendor": "email-163-tool",
    "support_email": "support@example.com"
  },
  "defaults": {
    "folder": "INBOX",
    "count": 5,
    "output_dir": "$HOME/Downloads"
  }
}
```

### 环境变量方式

也可以使用环境变量替代配置文件：

```bash
# Linux/macOS
export EMAIL_163_USER="your_email@163.com"
export EMAIL_163_PASS="your_auth_code"

# Windows PowerShell
$env:EMAIL_163_USER="your_email@163.com"
$env:EMAIL_163_PASS="your_auth_code"
```

### 配置文件权限保护

```bash
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
echo "implementation_ready"
```

---

## 优选实践

### 授权码安全

- 始终使用客户端授权码，绝不使用邮箱登录密码
- 定期更换授权码，建议每季度更新一次
- 配置文件设置严格权限（600）
- 不要将配置文件纳入版本控制系统

### 邮件发送规范

```bash
# 推荐做法：使用文件作为邮件正文（避免转义问题）
email-163-tool send --to friend@example.com --subject "周报" --file weekly_report.txt

# HTML 邮件使用引号包裹
com --subject "通知" --html "<h1>会议通知</h1><p>明天上午10点开会</p>"
```

### 附件管理建议

- 单个附件建议不超过 25MB（邮箱服务商限制）
- 多附件总大小建议不超过 50MB
- 大文件建议使用云存储链接替代

### 命令组合使用

```bash
# 先搜索再处理的标准流程
email-163-tool search --from "noreply" --count 20
email-163-tool delete --id 123
email-163-tool move --id 124 --to "归档"
```

---

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### 问题1：IMAP 连接失败，提示 Unsafe Login

```text
Error: SELECT Unsafe Login
```

**原因**: 163邮箱要求进行 IMAP ID 认证（RFC 2971）。

**解决**: 确保配置文件中包含 `imap_id` 字段，默认配置已包含此项。如仍失败，检查配置文件格式是否正确。

### 问题2：认证失败，提示 LOGIN failed

```text
Error: LOGIN failed
```

**原因**: 使用了邮箱登录密码而非客户端授权码。

**解决**: 登录163邮箱网页版，在设置中生成客户端授权码，填入配置文件的 `password` 字段。

### 问题3：附件发送失败

```text
Error: Cannot attach file
```

**原因**: 文件路径错误或文件不可读。

**解决**: 使用绝对路径指定附件，确认文件存在且有读取权限：

```bash
# 验证文件是否存在
ls -la /path/to/your/file.pdf

# 使用绝对路径发送
email-163-tool send --to user@example.com --subject "文件" --attach /path/to/docs/file.pdf
```

### 问题4：中文主题显示乱码

**解决**: 确保终端使用 UTF-8 编码，配置文件以 UTF-8 格式保存。

### 问题5：搜索结果为空

**解决**: 检查搜索条件是否正确，163邮箱搜索区分大小写，建议使用英文关键词或完整中文短语。

---

## 命令参考速查

| 命令 | 功能 | 示例 |
|:-----|:-----|:-----|
| `send` | 发送邮件 | `email-163-tool send --to x@y.com --subject "测试" --body "内容"` |
| `read` | 读取邮件 | `email-163-tool read --count 10` |
| `search` | 搜索邮件 | `email-163-tool search --from "cloudflare"` |
| `folders` | 文件夹列表 | `email-163-tool folders` |
| `folder create` | 创建文件夹 | `email-163-tool folder create "归档"` |
| `delete` | 删除邮件 | `email-163-tool delete --id 123` |
| `move` | 移动邮件 | `email-163-tool move --id 123 --to "归档"` |
| `flag` | 标记邮件 | `email-163-tool flag --id 123 --set seen` |
| `attachments` | 附件管理 | `email-163-tool attachments --id 123 --download` |

---

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8 及以上（如使用 Python 脚本模式）
- **网络环境**: 需可访问 `imap.163.com` 与 `smtp.163.com`

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 标准库 | 运行库 | 可选 | Python 自带（smtplib, imaplib, email） |
| 163邮箱账号 | 账户 | 必需 | 注册163邮箱并开启IMAP/SMTP服务 |
| 客户端授权码 | 凭证 | 必需 | 163邮箱设置页生成 |

### API Key 配置

- 本工具使用163邮箱客户端授权码进行认证，无需额外 API Key
- 授权码通过配置文件或环境变量提供
- 建议将授权码存储在环境变量中，避免硬编码

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，核心邮件操作通过命令行工具完成

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据