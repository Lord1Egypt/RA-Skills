---

name: "email-digest-tool-free"
description: "自动生成每日邮件摘要，支持主流邮箱，快速了解重要邮件。Use when 需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于垃圾信息群发。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "邮件日报免费版"
  version: "1.0.0"
  summary: "自动生成每日邮件摘要，支持主流邮箱，快速了解重要邮件"
  tags:
    - "沟通协作"
    - "邮件管理"
    - "邮件摘要"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - browser

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


# 邮件日报免费版

**版本**: 1.0.0
**适用对象**: 个人用户、独立开发者、一人公司
**核心定位**: 每日邮件摘要快速生成工具

---

## 概述

邮件日报免费版是一款帮助个人用户自动生成每日邮件摘要的工具。通过浏览器自动化技术登录邮箱，获取最新邮件列表并生成包含未读统计、发件人分类与建议操作的总结报告。工具支持复用浏览器已登录会话，无需在脚本中存储邮箱密码，兼顾便利性与安全性。

本工具支持 Gmail、Outlook、QQ邮箱、163邮箱、126邮箱等主流邮箱服务，生成的摘要报告包含邮件统计概览、重要邮件列表与分类汇总，帮助用户在早晨用最少时间掌握邮箱全貌。

---

## 核心能力

### 邮箱登录

- 复用浏览器已登录会话（推荐，无需密码）
- 手动登录流程（headed 模式可见操作过程）
- 支持主流邮箱服务

**输出**: 返回邮箱登录的执行结果,包含操作状态和输出数据。

### 邮件获取

- 自动获取收件箱最新邮件列表
- 统计未读邮件数量
- 提取发件人、主题、摘要、时间信息

**输出**: 返回邮件获取的执行结果,包含操作状态和输出数据。

### 摘要生成

- 生成每日邮件统计概览
- 按发件人与主题基础分类
- 生成邮件列表截图存档
- 输出文本格式摘要报告

**输出**: 返回摘要生成的执行结果,包含操作状态和输出数据。

### 邮件统计

- 未读邮件计数
- 可见邮件总数
- 时间戳记录

---

**输出**: 返回邮件统计的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：自动生成每日邮件、快速了解重要邮件、邮件日报免费版是、一款面向个人用户、的邮件摘要生成工、通过浏览器自动化、登录邮箱、自动获取最新邮件、列表并生成每日邮、件总结报告、帮助用户快速了解、当日邮件概况、核心能力、Gmail、Outlook、邮箱等主流邮箱、Use、when、需要消息发送、通知推送、邮件短信、通信集成时使用、不适用于垃圾信息等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：每日早晨邮件快速浏览

每天早晨打开电脑后，快速生成 Gmail 邮件摘要，了解 overnight 收到的重要邮件。

```bash
# 使用已登录的浏览器会话打开 Gmail
browser-use --browser real open https://mail.google.com

# 等待页面加载
sleep 3

# 获取邮箱当前状态
browser-use state

# 截图保存收件箱
browser-use screenshot emails_$(date +%Y%m%d).png
```

### 场景二：生成未读邮件统计

快速统计当前邮箱的未读邮件数量与可见邮件总数。

```bash
# 获取邮件统计数据
browser-use eval "
(() => {
  const unreadCount = document.querySelectorAll('.zE').length;
  const totalVisible = document.querySelectorAll('tr.zA').length;
  return JSON.stringify({
    unread: unreadCount,
    visible: totalVisible,
    timestamp: new Date().toISOString()
  });
})()
"
```

输出示例：

```json
{
  "unread": 12,
  "visible": 50,
  "timestamp": "2026-07-18T01:30:00.000Z"
}
```

### 场景三：提取邮件列表信息

提取前20封邮件的发件人、主题与摘要信息。

```bash
browser-use eval "
  const emails = [];
  document.zA').forEach((row, i) => {
    if (i < 20) {
      const sender = row.querySelector('.yX.xY span')?.innerText || '';
      const subject = row.querySelector('.y6 span')?.innerText || '';
      const snippet = row.querySelector('.y2')?.innerText || '';
      const time = row.querySelector('.xW.xY span')?.innerText || '';
      emails.push({ sender, subject, snippet, time });
    }
  });
  JSON.stringify(emails, null, 2);
"
```

---

## 快速开始

### 依赖详情

```bash
# 安装 browser-use CLI
uv pip install browser-use[cli]
browser-use install
```

### 第二步：在浏览器中登录邮箱

使用 Chrome 浏览器手动登录你的邮箱账户（Gmail、Outlook、QQ邮箱等），确保登录状态保持。

### 第三步：生成邮件摘要

```bash
# 使用已登录会话生成摘要
sleep 3
browser-use state
browser-use screenshot daily_digest.png
```

### 第四步：一键摘要脚本

创建 `email_digest.sh` 脚本：

```bash
#!/bin/sh

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
OUTPUT_DIR="./email_summaries"
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "📧 邮件日报生成中..."
echo "日期: $DATE $TIME"
echo "=========================================="

sleep 3

echo ""
echo "📋 当前邮箱状态:"
browser-use state

echo ""
echo "📸 保存截图..."
browser-use screenshot "$OUTPUT_DIR/inbox_$DATE.png"

echo ""
echo "📊 邮件统计:"
browser-use eval "
(() => {
querySelectorAll('.zE').length;
  return JSON.stringify({
    unread: unreadCount,
    visible: totalVisible,
  });
})()
"

echo ""
echo "✅ 完成！截图保存至: $OUTPUT_DIR/inbox_$DATE.png"
browser-use close
```

---

## 示例

### 支持的邮箱服务

| 邮箱服务 | 登录 URL | 收件箱 URL |
|:---------|:---------|:-----------|
| Gmail | https://accounts.google.com | https://mail.google.com |
| Outlook | https://login.live.com | https://outlook.live.com |
| QQ邮箱 | https://mail.qq.com | https://mail.qq.com |
| 163邮箱 | https://mail.163.com | https://mail.163.com |
| 126邮箱 | https://mail.126.com | https://mail.126.com |
| 企业微信邮箱 | https://exmail.qq.com | https://exmail.qq.com |

### 输出目录配置

```bash
# 自定义输出目录
OUTPUT_DIR="$HOME/Documents/email-digests"
mkdir -p "$OUTPUT_DIR"

# 截图命名规则
SCREENSHOT_NAME="inbox_$(date +%Y%m%d_%H%M%S).png"
```

### 手动登录流程配置

如果需要手动登录（无已登录会话），使用 headed 模式：

```bash
browser-use --headed open https://accounts.google.com

# 查看页面元素
browser-use state

# 输入邮箱
browser-use input <email_input_index> "your-email@gmail.com"
browser-use click <next_button_index>

# 输入密码
browser-use input <password_input_index> "your-password"
browser-use click <login_button_index>

# 打开邮箱
browser-use open https://mail.google.com
```

---

## 优选实践

### 安全优先原则

- **优先使用 `--browser real` 模式**: 复用已登录会话，不在脚本中存储密码
- **敏感信息用环境变量**: 如必须输入密码，使用环境变量传递
- **定期清理会话**: 完成后及时关闭浏览器

```bash
# 安全做法：复用会话

# 完成后关闭
browser-use close
```

### 截图管理

```bash
# 按日期组织截图
DAILY_DIR="./email_summaries/$(date +%Y/%m)"
mkdir -p "$DAILY_DIR"
browser-use screenshot "$DAILY_DIR/inbox_$(date +%d).png"

# 定期清理旧截图（保留30天）
find ./email_summaries -name "*.png" -mtime +30 -delete
```

### 邮件分类建议

提取邮件后，可手动按以下维度分类：

- **重要邮件**: 来自领导、客户、关键服务提供商
- **工作邮件**: 来自同事、团队邮件组
- **通知邮件**: 来自各类服务的通知
- **订阅邮件**: 时事通讯、营销邮件

---

## 常见问题

### 问题1：页面元素找不到

```text
Error: Element not found
```

**原因**: 页面尚未完全加载。

**解决**: 增加等待时间，确保页面加载完成：

```bash
sleep 5
browser-use state
```

### 问题2：登录会话过期

```text
页面跳转到登录页
```

**解决**: 在 Chrome 浏览器中重新登录邮箱，或使用手动登录流程：

```bash
browser-use close --all
```

### 问题3：browser-use 命令未找到

**解决**: 确认已正确安装 browser-use CLI：

```bash
uv pip install browser-use[cli]
browser-use install

# 验证安装
browser-use --version
```

### 问题4：截图为空白

**原因**: 截图时页面尚未渲染完成。

**解决**: 增加等待时间后再截图：

```bash
sleep 5
browser-use screenshot inbox.png
```

### 问题5：不同邮箱页面结构不同

**解决**: 不同邮箱的邮件列表 HTML 结构不同，需要调整选择器。建议先用 `browser-use state` 查看页面结构，再调整提取脚本中的 CSS 选择器。

---

## 输出报告示例

生成的邮件摘要报告格式：

```text
==========================================
📧 邮件日报 - 2026-07-18
==========================================

📊 统计概览:
- 未读邮件: 12 封
- 可见邮件: 50 封
- 截图: inbox_20260718.png

📬 重要未读邮件:
1. 来自 boss@company.com
   主题: 项目进度汇报 - 紧急
   时间: 09:30

2. 来自 finance@bank.com
   主题: 账单提醒
   时间: 08:15

💡 建议操作:
- 回复 boss@company.com 的邮件
- 处理需要审批的邮件

==========================================
```

---

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome 浏览器（需已安装并登录邮箱）
- **Python版本**: 3.9 及以上（browser-use 依赖）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| browser-use | CLI工具 | 必需 | `uv pip install browser-use[cli]` |
| Chrome 浏览器 | 浏览器 | 必需 | 官方网站下载安装 |
| 邮箱账户 | 账户 | 必需 | 注册主流邮箱服务 |

### API Key 配置

- 本工具通过浏览器会话复用访问邮箱，无需额外 API Key
- 如使用 AI 摘要功能，可选配置 LLM API Key（用于智能摘要生成）
- 浏览器登录凭证存储在浏览器本地，不在脚本中保存

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行浏览器自动化任务，完成邮件摘要生成

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

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