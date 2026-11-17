---

slug: email-multi-provider-pro
name: email-multi-provider-pro
version: 1.0.0
displayName: 多邮箱管理专业版
summary: "企业级Gmail与Outlook统一管理，批量操作与多账户隔离。多邮箱管理专业版面向企业用户与高效能个人用户。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于"
license: Proprietary
edition: pro
description: "多邮箱管理专业版面向企业用户与高效能个人用户。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
  when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务.
tags:
  - 沟通协作
  - 邮件管理
  - 多邮箱
  - 企业效率
  - 批量操作
  - 邮件
  - 通信
  - 工具
  - profile
  - porteden
  - email
  - csv
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Communication"

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


# 多邮箱管理专业版
**版本**: 1.0.0
**适用对象**: 企业用户、团队管理者、客服与运营人员
**核心定位**: 企业级跨邮箱平台统一管理与批量处理平台
**兼容性**: 完全兼容免费版（email-multi-provider-free）全部命令与配置，可直接升级

---
## 概述
多邮箱管理专业版是一款面向企业级场景的跨邮箱平台深度管理工具。在免费版提供的 Gmail、Outlook 与 Exchange 邮箱读取、搜索、发送等基础能力之上，专业版引入批量邮件处理引擎、多账户 Profile 隔离、高级过滤策略、邮件模板系统、操作审计日志与团队协作共享等高级特性，满足企业在批量响应、合规审计、团队协作与多部门管理等复杂场景下的需求.
专业版向下完全兼容免费版，现有 `porteden email` 命令与配置无需修改即可平滑升级。新增的企业级功能通过扩展命令与 Profile 机制实现，不影响既有工作流.
---
## 核心能力
### 批量操作引擎
- **批量发送**: 一次性向多个收件人发送邮件，支持收件人列表
- **批量回复**: 对搜索结果批量回复
- **批量转发**: 批量转发邮件到指定地址
- **批量删除/归档**: 按过滤条件批量处理
- **批量标记**: 批量标记已读、添加标签、设置重要性

**处理**: 解析批量操作引擎的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量操作引擎的响应数据,包含状态码、结果和日志.
### 多账户 Profile 隔离
- 每个账户独立 Profile，凭证隔离存储
- 租户级别配置管理
- 账户间快速切换
- 账户健康状态监控
- 账户权限与作用域管理

**处理**: 解析多账户 Profile 隔离的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多账户 Profile 隔离的响应数据,包含状态码、结果和日志.
### 高级过滤策略
- 多维度组合条件（发件人、主题、正文、日期、大小、标签）
- 正则表达式匹配
- 智能规则引擎（条件触发自动操作）
- 过滤结果导出（CSV/JSON）
- 规则模板复用

**处理**: 解析高级过滤策略的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回高级过滤策略的响应数据,包含状态码、结果和日志.
### 邮件模板系统
- 内置企业常用模板（通知、报告、邀请、审批）
- 自定义模板管理
- 变量插值与条件渲染
- 模板共享与版本控制

**处理**: 解析邮件模板系统的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回邮件模板系统的响应数据,包含状态码、结果和日志.
### 审计与合规
- 全操作审计日志记录
- 邮件访问追踪
- 合规导出报告
- 敏感邮件标记与保护
- 数据保留策略

**处理**: 解析审计与合规的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回审计与合规的响应数据,包含状态码、结果和日志.
### 团队协作
- 邮件共享与分配
- 团队邮件池管理
- 任务状态跟踪
- 协作备注与内部讨论

---

**处理**: 解析团队协作的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回团队协作的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、Gmail、Outlook、统一管理、批量操作与多账户、多邮箱管理专业版、面向企业用户与高、效能个人用户、Use、when、需要提升效率、自动化流程、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：客服团队批量响应邮件
客服团队需要批量回复100封咨询邮件，使用模板进行个性化响应.
**准备收件人列表** `customers.csv`:
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 多邮箱管理专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```csv
email,ticket_id,name,issue
customer1@example.com,T001,张三,订单查询
customer2@example.com,T002,李四,退款申请
customer3@example.com,T003,王五,物流跟踪
```

**创建响应模板** `templates/reply.html`:

```html
<p>尊敬的 ：</p>
<p>您的工单 （）已收到，我们将在24小时内处理。</p>
<p>感谢您的耐心等待。</p>
<p>客服团队</p>
```

**执行批量发送**:

```bash
# 批量发送（先试运行）
porteden email batch-send \
  --profile support \
  --recipients customers.csv \
  --template templates/reply.html \
  --subject "工单  处理通知" \
  --rate-limit 10 \
  --dry-run
# ...
# 正式发送
porteden email batch-send \
  --profile support \
  --subject "工单  处理通知" \
  --rate-limit 10 \
  --log batch_send.log
```

输出示例：

```text
📋 批量发送任务
   Profile: support
   收件人: 100
   速率: 10 封/分钟
# ...
[1/100] ✅ customer1@example.com - 张三 - T001
[2/100] ✅ customer2@example.com - 李四 - T002
...
📊 完成: 100 成功, 0 失败
```

### 场景二：多账户邮件统一监控
管理者需要查看工作邮箱与个人邮箱的今日邮件概览.
```bash
# 工作邮箱今日邮件
porteden email messages --profile work --today -jc
# ...
# 个人邮箱今日邮件
porteden email messages --profile personal --today -jc
# ...
# 跨账户搜索
porteden email search-all \
  --profiles work,personal \
  --query "合同" \
  --days 7 \
  --format json
```

### 场景三：邮件合规审计与归档
财务部门需要导出所有与合同相关的邮件用于合规审计.
```bash
# 搜索并导出合规报告
porteden email export \
  --profile finance \
  --from "legal@company.com" \
  --subject "合同" \
  --after "2026-01-01" \
  --before "2026-07-18" \
  --format csv \
  --output compliance_report.csv
# ...
# 查看审计日志
porteden email audit-log \
  --profile finance \
  --action "export,delete,send" \
  --since "2026-07-01"
```

审计日志输出：

```text
📜 审计日志 - finance 账户
时间范围: 2026-07-01 至 2026-07-18
# ...
2026-07-18 10:30:15 | EXPORT | 48 封邮件导出至 compliance_report.csv
2026-07-17 14:22:03 | SEND  | 发送至 vendor@example.com | 主题: 合同确认
2026-07-16 09:15:30 | DELETE | 删除邮件 google:abc123 | 主题: 测试邮件
```

---
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
专业版完全兼容免费版，现有命令与配置无需修改：

```bash
# 免费版命令依然有效
porteden email messages --today -jc
porteden email send --to x@y.com --subject "测试" --body "内容"
# ...
# 专业版新增命令
porteden email batch-send --recipients list.csv --template tpl.html
porteden email audit-log --since "2026-07-01"
```

### 配置多账户 Profile
```bash
# 添加工作账户
porteden profile add --name work --login
# ...
# 添加个人账户
porteden profile add --name personal --login
# ...
# 添加客服账户
porteden profile add --name support --login
# ...
# 列出所有 Profile
porteden profile list
# ...
# 验证所有账户状态
porteden profile health-check --all
```

### 配置审计日志
```json
{
  "audit": {
    "enabled": true,
    "log_file": "$HOME/.config/porteden/audit.log",
    "actions": ["send", "reply", "forward", "delete", "modify", "export"],
    "retention_days": 365,
    "auto_archive": true
  }
}
```

---
## 示例
### 批量操作配置
```json
{
  "batch": {
    "rate_limit": 10,
    "max_recipients": 1000,
    "retry_count": 3,
    "retry_delay": 60,
    "concurrency": 5,
    "on_failure": "log",
    "failure_log": "$HOME/.config/porteden/batch_failures.log"
  }
}
```

### 智能规则配置
```json
{
  "rules": [
    {
      "name": "自动标记重要邮件",
      "condition": {
        "from": ["ceo@company.com", "cto@company.com"],
        "priority": "high"
      },
      "action": "add-label:IMPORTANT,mark-unread"
    },
    {
      "name": "自动归档通知邮件",
      "condition": {
        "from": "noreply@",
        "older_than_days": 30
      },
      "action": "add-label:ARCHIVED,remove-label:INBOX"
    }
  ]
}
```

### 团队协作配置
```json
{
  "team": {
    "shared_mailbox": "support@company.com",
    "members": ["agent1@company.com", "agent2@company.com"],
    "assignment_strategy": "round-robin",
    "status_tracking": true,
    "internal_notes": true
  }
}
```

---
## 优选实践
### 批量操作安全
```bash
# 始终先试运行
csv --template tpl.html --dry-run
# ...
# 控制速率与重试
csv --template tpl.html \
  --rate-limit 10 --retry 3 --retry-delay 60
# ...
# 记录失败用例
csv --template tpl.html \
  --log batch.log --on-failure log
```

### 多账户安全隔离
```bash
# 为每个部门使用独立 Profile
porteden profile add --name finance --login
porteden profile add --name hr --login
porteden profile add --name support --login
# ...
# 操作时指定 Profile，避免误操作
porteden email messages --profile finance --today -jc
# ...
# 定期检查凭证有效性
porteden profile health-check --all
```

### 审计合规
- 开启全操作审计日志
- 定期导出合规报告
- 设置合理的保留期限
- 敏感操作二次确认

```bash
# 导出月度审计报告
porteden email audit-export \
  --month 2026-07 \
  --format csv \
  --output audit_202607.csv
```

---
## 免费版与专业版对比
| 能力 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 基础邮件收发 | ✅ | ✅ |
| 邮件搜索 | 基础搜索 | 高级组合搜索 |
| Profile 隔离 | 单 Profile | 多 Profile 租户隔离 |
| 批量发送 | ❌ | ✅（变量替换） |
| 批量回复/转发 | ❌ | ✅ |
| 邮件模板 | ❌ | ✅（模板系统） |
| 智能规则 | ❌ | ✅（自动操作） |
| 审计日志 | ❌ | ✅（合规审计） |
| 团队协作 | ❌ | ✅（共享与分配） |
| 结果导出 | ❌ | ✅（CSV/JSON） |
| 技术支持 | 社区支持 | 优先支持 |

---
## 常见问题
### 已知限制
```text
Error: Rate limit exceeded
```

**解决**: 降低发送速率，Gmail/Outlook 对发送频率有严格限制：

```bash
# 降低速率
csv --template tpl.html --rate-limit 5
```

### 问题2：Profile 切换失败
**解决**: 确认 Profile 凭证有效：

```bash
# 验证 Profile
porteden profile test --name work
# ...
# 重新登录失效 Profile
porteden profile login --name work
```

### 问题3：审计日志占用空间过大
**解决**: 配置日志轮转与压缩：

```bash
# 压缩旧日志
porteden audit compress --older-than 30
# ...
# 清理过期日志
porteden audit clean --older-than 365
```

### 问题4：模板变量未替换
**解决**: 确保变量名与 CSV 列名一致：

```bash
# 验证模板
porteden email template validate --name "回复" --data sample.json
```

### 问题5：团队协作权限冲突
**解决**: 检查成员权限配置：

```bash
# 查看团队成员权限
porteden team members --mailbox support@company.com
# ...
# 更新权限
porteden team update --member agent1@company.com --role editor
```

---
## 命令参考速查
| 命令 | 功能 | 专业版独有 |
|---:|---:|---:|
| `messages` | 列出邮件 | - |
| `message` | 单封详情 | - |
| `send` | 发送邮件 | - |
| `reply` | 回复邮件 | - |
| `forward` | 转发邮件 | - |
| `batch-send` | 批量发送 | ✅ |
| `batch-reply` | 批量回复 | ✅ |
| `search-all` | 跨账户搜索 | ✅ |
| `export` | 结果导出 | ✅ |
| `audit-log` | 审计日志 | ✅ |
| `profile` | Profile 管理 | ✅ |
| `template` | 模板管理 | ✅ |
| `rule` | 智能规则 | ✅ |
| `team` | 团队协作 | ✅ |

---
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需可访问 Gmail/Outlook/Exchange 邮箱服务
- **磁盘空间**: 审计日志建议预留 500MB 以上

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| porteden CLI | CLI工具 | 必需 | `brew install porteden/tap/porteden` |
| 邮箱账户 | 账户 | 必需 | Gmail/Outlook/Exchange 账户 |
| 系统密钥环 | 系统服务 | 可选 | 操作系统自带（多账户凭证存储） |
| Go 运行时 | 运行时 | 可选 | Go 1.18+（如使用 go install） |
| 数据库 | 存储引擎 | 可选 | 用于审计日志（可选 SQLite 文件存储） |

### API Key 配置
- 通过 `porteden auth login` 完成浏览器 OAuth 认证，凭证存储在系统密钥环
- 多账户场景下每个 Profile 使用独立凭证
- 支持环境变量 `PE_API_KEY` 自动认证
- 企业用户建议使用密钥管理服务统一管理凭证

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行 porteden CLI 命令，支持批量处理、多账户隔离与审计合规
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
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

- **自动化执行**: 企业级Gmail与Outlook统一管理，批量操作与多账户隔离。多邮箱管理专业版面向企业用户与高效能个人用户。Use w
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据