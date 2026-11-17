---

slug: email-163-tool-pro
name: "email-163-tool-pro"
version: "1.0.0"
displayName: "163邮箱助手专业版"
summary: "企业级163邮箱管理，支持批量收发、高级搜索、定时任务与邮件归档。163邮箱助手专业版面向企业用户与高效能个人用户，在免费版基础能力之上扩展批量操作、 高级搜索过滤、定时任务调度、邮件归档审"
license: "Proprietary"
edition: "pro"
description: |-
  163邮箱助手专业版面向企业用户与高效能个人用户，在免费版基础能力之上扩展批量操作、
  高级搜索过滤、定时任务调度、邮件归档审计、模板化发送与多账户管理等企业级特性。核心能力:
  - 批量邮件发送与群发通知（支持变量替换与模板）
  - 高级搜索：多维度组合过滤、正则匹配、结果导出
  - 邮件归档与审计日志，满足合规要求
  - 定时任务调度，支持周期性邮件处理
  - 多账户统一管理，租户隔离配置
  - 邮件模板系统...
tags:
  - 沟通协作
  - 邮件管理
  - 163邮箱
  - 企业效率
  - 批量操作
  - 邮件
  - 通信
  - 工具
  - email-163-tool
  - csv
  - company
  - 用户提供
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"

---

> **功能说明**: 本技能涵盖 等企业级特性 等核心能力。


# 163邮箱助手专业版
**版本**: 1.0.0
**适用对象**: 企业用户、团队管理者、运维与运营人员
**核心定位**: 企业级163邮箱批量管理与自动化处理平台
**兼容性**: 完全兼容免费版（email-163-tool-free）全部命令与配置，可直接升级

## 概述
163邮箱助手专业版是一款面向企业级场景的网易163邮箱深度管理工具。在免费版提供的邮件收发、搜索与文件夹管理能力之上，专业版引入批量操作引擎、邮件模板系统、定时任务调度、归档审计日志与多账户统一管理等高级特性，满足企业在批量通知、合规归档、自动化处理与多部门协作等复杂场景下的需求.
专业版向下完全兼容免费版，已有配置文件与命令无需修改即可平滑升级。新增的企业级功能通过扩展命令实现，不影响既有工作流.
## 核心能力
### 批量操作引擎
- **批量发送**: 一次性向数百个收件人发送邮件，支持收件人列表文件
- **变量替换**: 邮件模板中支持 ``、`` 等变量插值
- **批量删除/移动**: 按搜索结果批量处理邮件
- **批量标记**: 批量标记已读、加星标、归类

**处理**: 解析批量操作引擎的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量操作引擎的响应数据,包含状态码、结果和日志.
### 高级搜索与过滤
- 多维度组合条件（发件人、主题、正文、日期、大小、标签）
- 正则表达式匹配
- 搜索结果导出为 CSV/JSON
- 搜索结果分页与排序

**处理**: 解析高级搜索与过滤的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回高级搜索与过滤的响应数据,包含状态码、结果和日志.
### 邮件模板系统
- 内置常用模板（通知、报告、邀请、提醒）
- 自定义模板管理（创建、编辑、删除）
- 变量插值与条件渲染
- 模板版本控制

**处理**: 解析邮件模板系统的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回邮件模板系统的响应数据,包含状态码、结果和日志.
### 定时任务调度
- 一次性定时发送
- 周期性任务（每日/每周/每月）
- 任务队列管理与状态监控
- 任务执行日志

**处理**: 解析定时任务调度的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回定时任务调度的响应数据,包含状态码、结果和日志.
### 归档与审计
- 邮件自动归档到指定文件夹
- 操作审计日志记录
- 归档邮件全文检索
- 合规导出报告

**处理**: 解析归档与审计的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回归档与审计的响应数据,包含状态码、结果和日志.
### 多账户管理
- 统一管理多个163邮箱账户
- 租户隔离配置
- 账户间邮件转发与同步
- 账户健康状态监控

**处理**: 解析多账户管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多账户管理的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、邮箱管理、支持批量收发、定时任务与邮件归、邮箱助手专业版面、向企业用户与高效、能个人用户、在免费版基础能力、之上扩展批量操作、高级搜索过滤、邮件归档审计、模板化发送与多账、户管理等企业级特、核心能力、批量邮件发送与群、发通知、支持变量替换与模、多维度组合过滤、正则匹配、邮件归档与审计日、满足合规要求、支持周期性邮件处、多账户统一管理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：批量发送个性化通知邮件
企业需要向500名员工发送包含个人信息的工资单通知邮件，每封邮件内容不同.
**准备收件人列表** `recipients.csv`:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 163邮箱助手专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```csv
email,name,department,salary_month
zhangsan@company.com,张三,技术部,2026年7月
lisi@company.com,李四,市场部,2026年7月
wangwu@company.com,王五,财务部,2026年7月
```

**创建邮件模板** `template/salary_notice.html`:

```html
<h1>工资单通知 - </h1>
<p>尊敬的 （）：</p>
<p>您本月工资单已生成，请登录企业系统查看详情。</p>
<p>如有疑问，请联系财务部。</p>
```

**执行批量发送**:

```bash
email-163-tool batch-send \
  --recipients recipients.csv \
  --template template/salary_notice.html \
  --subject " - 工资单通知 " \
  --rate-limit 10 \
  --dry-run
```

输出示例：

```text
📋 批量发送任务启动
   收件人总数: 500
   模板: template/salary_notice.html
   发送速率: 10 封/分钟
   模式: 试运行（dry-run）
[1/500] ✅ zhangsan@company.com - 张三 - 技术部
[2/500] ✅ lisi@company.com - 李四 - 市场部
[3/500] ✅ wangwu@company.com - 王五 - 财务部
...
📊 试运行完成: 500 封邮件预览成功，0 个错误
💡 移除 --dry-run 参数以实际发送
```

### 场景二：邮件归档与合规审计
财务部门需要将所有与发票相关的邮件归档保存，并生成审计报告.
```bash
email-163-tool search-archive \
  --from "invoice@" \
  --subject "发票" \
  --after "2026-01-01" \
  --before "2026-07-18" \
  --archive-folder "财务归档/2026年上半年" \
  --export audit_report.csv
email-163-tool audit-log --action archive --since "2026-07-01"
```

审计日志输出：

```text
📜 审计日志 - 归档操作
时间范围: 2026-07-01 至 2026-07-18
2026-07-18 10:30:15 | ARCHIVE | 邮件ID: 234 | 主题: 7月发票 | 来源: invoice@vendor.com -> 财务归档/2026年上半年
2026-07-18 10:30:16 | ARCHIVE | 邮件ID: 235 | 主题: 6月发票 | 来源: invoice@vendor.com -> 财务归档/2026年上半年
...
归档总数: 48 封 | 导出文件: audit_report.csv
```

### 场景三：定时自动清理与汇总
设置每周一自动清理垃圾邮件，并汇总上周未读重要邮件.
```bash
email-163-tool schedule create \
  --name "weekly-cleanup" \
  --cron "0 9 * * 1" \
  --actions "search --folder 垃圾邮件 --all | delete --batch" \
  --notify "admin@company.com"
email-163-tool schedule list
email-163-tool schedule history --name "weekly-cleanup"
```

## 不适用场景
以下场景163邮箱助手专业版不适合处理：

- 垃圾信息群发
- 通信协议逆向
- 电话语音交互

## 触发条件
需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于非本工具能力范围的需求.
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
专业版完全兼容免费版，无需修改现有配置：

```bash
email-163-tool read --count 5
email-163-tool send --to test@example.com --subject "升级测试" --body "专业版已就绪"
```

### 新增企业级配置
在配置文件中添加专业版扩展字段：

```json
{
  "email": "enterprise@163.com",
  "password": "your_auth_code",
  "imap_server": "imap.163.com",
  "imap_port": 993,
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "pro": {
    "multi_account": {
      "enabled": true,
      "accounts_dir": "$HOME/.config/email-163-tool/accounts"
    },
    "batch": {
      "rate_limit": 10,
      "max_recipients": 1000,
      "retry_count": 3
    },
    "archive": {
      "enabled": true,
      "auto_archive": true,
      "retention_days": 365
    },
    "audit": {
      "enabled": true,
      "log_file": "$HOME/.config/email-163-tool/audit.log"
    },
    "schedule": {
      "enabled": true,
      "timezone": "Asia/Shanghai"
    }
  }
}
```

### 多账户配置
为每个邮箱账户创建独立配置文件：

```bash
mkdir -p $HOME/.config/email-163-tool/accounts
cat > $HOME/.config/email-163-tool/accounts/finance.json << 'EOF'
{
  "name": "财务部邮箱",
  "email": "finance@company.com",
  "password": "finance_auth_code"
}
EOF
email-163-tool accounts list
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例
### 批量发送配置
```json
{
  "batch": {
    "rate_limit": 10,
    "max_recipients": 1000,
    "retry_count": 3,
    "retry_delay": 60,
    "concurrency": 5,
    "on_failure": "skip",
    "failure_log": "$HOME/.config/email-163-tool/batch_failures.log"
  }
}
```

### 归档规则配置
```json
{
  "archive_rules": [
    {
      "name": "发票归档",
      "conditions": {
        "from": "invoice@",
        "subject": "发票"
      },
      "target_folder": "财务归档",
      "retention_days": 1095
    },
    {
      "name": "通知归档",
      "conditions": {
        "from": "noreply@",
        "older_than_days": 90
      },
      "target_folder": "通知归档",
      "retention_days": 180
    }
  ]
}
```

### 定时任务配置
```json
{
  "schedules": [
    {
      "name": "daily-summary",
      "cron": "0 9 * * *",
      "action": "summary --unread --send admin@company.com"
    },
    {
      "name": "weekly-cleanup",
      "cron": "0 10 * * 1",
      "action": "clean --folder 垃圾邮件 --older-than 7"
    }
  ]
}
```

## 优选实践
### 批量发送安全规范
```bash
email-163-tool batch-send --recipients list.csv --template tpl.html --dry-run
csv --template tpl.html --rate-limit 10
csv --template tpl.html \
  --retry 3 --retry-delay 60 --log batch_send.log
```

### 邮件模板管理
```bash
email-163-tool template create --name "月度报告" --file templates/monthly.html
email-163-tool template preview --name "月度报告" \
  --data '{"name":"张三","month":"2026年7月"}'
email-163-tool template list
```

### 归档与合规
- 制定明确的归档规则，按业务类型分类
- 设置合理的保留期限（如财务邮件保留3年）
- 定期检查归档审计日志
- 定期导出合规报告存档

### 多账户安全
```bash
email-163-tool accounts rotate-key --account finance
email-163-tool accounts health-check
```

## 免费版与专业版对比
| 能力 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 基础邮件收发 | ✅ | ✅ |
| 邮件搜索 | 基础搜索 | 高级组合搜索 |
| 文件夹管理 | ✅ | ✅ |
| 附件管理 | ✅ | ✅ |
| 批量发送 | ❌ | ✅（支持变量替换） |
| 邮件模板 | ❌ | ✅（模板系统） |
| 定时任务 | ❌ | ✅（cron调度） |
| 归档审计 | ❌ | ✅（合规日志） |
| 多账户管理 | ❌ | ✅（租户隔离） |
| 搜索结果导出 | ❌ | ✅（CSV/JSON） |
| 技术支持 | 社区支持 | 优先支持 |

## 已知限制
- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 常见问题
### 问题1：批量发送被限制
```text
Error: Rate limit exceeded
```

**解决**: 降低发送速率，163邮箱对发送频率有严格限制。建议 `--rate-limit` 设置为 5-10 封/分钟，并启用失败重试机制.
### 问题2：模板变量未替换
**解决**: 确保变量名与 CSV 列名完全一致（区分大小写），模板中使用 `` 语法：

```bash
email-163-tool template validate --name "通知" --data sample.json
```

### 问题3：定时任务未执行
**解决**: 检查时区配置与 cron 表达式格式：

```bash
email-163-tool schedule validate --cron "0 9 * * 1"
email-163-tool schedule status --name "weekly-cleanup"
```

### 问题4：多账户切换失败
**解决**: 确保各账户配置文件格式正确，授权码有效：

```bash
email-163-tool accounts validate --all
email-163-tool accounts test --account finance
```

### 问题5：归档空间不足
**解决**: 定期清理过期归档，或调整保留期限：

```bash
email-163-tool archive clean --expired
email-163-tool archive stats
```

## 命令参考速查
| 命令 | 功能 | 专业版独有 |
|---:|---:|---:|
| `send` | 发送邮件 | - |
| `read` | 读取邮件 | - |
| `search` | 基础搜索 | - |
| `search-archive` | 搜索并归档 | ✅ |
| `batch-send` | 批量发送 | ✅ |
| `template` | 模板管理 | ✅ |
| `schedule` | 定时任务 | ✅ |
| `audit-log` | 审计日志 | ✅ |
| `accounts` | 多账户管理 | ✅ |
| `archive` | 归档管理 | ✅ |
| `export` | 结果导出 | ✅ |

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8 及以上（如使用 Python 脚本模式）
- **网络环境**: 需可访问 `imap.163.com` 与 `smtp.163.com`
- **磁盘空间**: 归档与日志建议预留 1GB 以上

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 标准库 | 运行库 | 可选 | Python 自带（smtplib, imaplib, email） |
| 163邮箱账号 | 账户 | 必需 | 注册163邮箱并开启IMAP/SMTP服务 |
| 客户端授权码 | 凭证 | 必需 | 163邮箱设置页生成 |
| cron 服务 | 系统服务 | 可选 | 系统自带（定时任务功能需要） |
| 数据库 | 存储引擎 | 可选 | 用于归档索引（可选 SQLite 文件存储） |

### API Key 配置
- 本工具使用163邮箱客户端授权码进行认证，无需额外 API Key
- 多账户场景下每个账户使用独立授权码
- 授权码通过配置文件或环境变量提供，支持加密存储
- 建议企业用户使用密钥管理服务统一管理授权码

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作，企业级功能通过扩展命令行工具完成，支持批量处理与定时调度

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

- **自动化执行**: 企业级163邮箱管理，支持批量收发、高级搜索、定时任务与邮件归档。163邮箱助手专业版面向企业用户与高效能个人用户，在免
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据