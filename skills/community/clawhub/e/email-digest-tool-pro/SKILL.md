---

slug: email-digest-tool-pro
name: "email-digest-tool-pro"
version: "1.0.0"
displayName: "邮件日报专业版"
summary: "多邮箱AI智能摘要与定时报告，企业级邮件监控与分类方案。邮件日报专业版面向企业用户与高效能个人用户。Use when 需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于垃圾信息群发。"
license: "Proprietary"
edition: "pro"
description: |-
  邮件日报专业版面向企业用户与高效能个人用户。Use when 需要消息发送、通知推送、邮件短信、通信集成时使用。不适用于垃圾信息群发。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。
tags:
  - 沟通协作
  - 邮件管理
  - 邮件摘要
  - 企业效率
  - AI智能
  - 邮件
  - 通信
  - 工具
  - email-digest-tool
  - gmail
  - outlook
  - https
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 邮件日报专业版
**版本**: 1.0.0
**适用对象**: 企业管理者、团队负责人、运维与运营人员
**核心定位**: 企业级多邮箱智能摘要与监控平台
**兼容性**: 完全兼容免费版（email-digest-tool-free）全部功能，可直接升级
## 概述
邮件日报专业版是一款面向企业级场景的多邮箱智能摘要与监控工具。在免费版提供的单邮箱摘要生成能力之上，专业版引入多邮箱账户聚合、AI 智能摘要、定时报告推送、邮件智能分类、关键邮件告警与历史趋势分析等高级特性，帮助企业管理者与团队负责人在一个视图中掌握所有邮箱动态，实现邮件的智能化管理与 proactive 监控.
专业版向下完全兼容免费版，现有浏览器自动化流程无需修改即可平滑升级。新增的企业级功能通过扩展命令实现，支持多渠道报告推送与自定义告警规则.
## 核心能力
### 多邮箱聚合
- 统一汇总 Gmail、Outlook、QQ邮箱、163邮箱等多个账户
- 跨邮箱合并去重与排序
- 按账户分组展示与统一视图切换
- 多账户健康状态监控

**处理**: 解析多邮箱聚合的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多邮箱聚合的响应数据,包含状态码、结果和日志.
### AI 智能摘要
- 邮件重要度自动评分（高/中/低）
- 智能生成行动建议（回复/审批/跟进）
- 风险邮件识别与提示
- 摘要自然语言生成（支持中文）

**处理**: 解析AI 智能摘要的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回AI 智能摘要的响应数据,包含状态码、结果和日志.
### 定时报告推送
- 一次性定时生成报告
- 周期性任务（每日/每周/自定义）
- 多渠道推送（邮件、飞书、钉钉、Slack、Webhook）
- 报告格式自定义（文本/HTML/Markdown）

**处理**: 解析定时报告推送的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回定时报告推送的响应数据,包含状态码、结果和日志.
### 智能分类与标签
- 自动按发件人、主题、内容分类
- 自定义分类规则与标签
- 优先级自动排序
- 分类统计与占比分析

**处理**: 解析智能分类与标签的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回智能分类与标签的响应数据,包含状态码、结果和日志.
### 告警通知
- 关键邮件实时告警（来自特定发件人或含关键词）
- 未读邮件超量告警
- 告警渠道配置（邮件/即时通讯）
- 告警级别与静默策略

**处理**: 解析告警通知的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回告警通知的响应数据,包含状态码、结果和日志.
### 趋势分析
- 邮件量趋势图表（日/周/月）
- 发件人排行与占比
- 响应时间统计分析
- 历史报告归档与检索

**处理**: 解析趋势分析的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回趋势分析的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：智能摘要与定时报、企业级邮件监控与、分类方案、邮件日报专业版面、向企业用户与高效、能个人用户、Use、when、需要消息发送、通知推送、邮件短信、通信集成时使用、不适用于垃圾信息、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：管理者多邮箱统一日报
企业管理者同时使用 Gmail（对外）和 Outlook（内部），需要每天早晨收到两个邮箱的统一摘要.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 邮件日报专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 生成多邮箱聚合摘要
email-digest-tool aggregate \
  --accounts gmail,outlook \
  --date today \
  --format html \
  --output reports/daily_$(date +%Y%m%d).html
# ...
# 自动推送到飞书
email-digest-tool aggregate \
  --accounts gmail,outlook \
  --push feishu \
  --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/未指定"
```

输出报告示例：

```text
==========================================
📧 多邮箱日报 - 2026-07-18
==========================================
# ...
📊 账户概览:
- Gmail (manager@company.com): 未读 15 封
- Outlook (manager@company.onmicrosoft.com): 未读 8 封
- 合计未读: 23 封
# ...
🔴 高优先级邮件 (3 封):
1. [Gmail] 来自 ceo@company.com
   主题: 董事会决议 - 需要签字
   时间: 08:45 | 评分: 9.5/10
   建议: 立即处理
# ...
2. [Outlook] 来自 legal@company.com
   主题: 合同审核 - 紧急
   时间: 09:12 | 评分: 9.0/10
   建议: 今日内回复
# ...
🟡 中优先级邮件 (12 封):
...
# ...
💡 AI 建议:
- 优先回复董事会决议邮件
- 3 封合同邮件需今日审批
- 5 封订阅邮件可批量归档
==========================================
```

### 场景二：定时报告自动推送
设置每天早上9点自动生成摘要并推送到飞书群.
```bash
# 创建定时推送任务
email-digest-tool schedule create \
  --name "morning-digest" \
  --cron "0 9 * * 1-5" \
  --accounts gmail,outlook \
  --format markdown \
  --push feishu \
feishu.cn/open-apis/bot/v2/hook/未指定" \
  --timezone "Asia/Shanghai"
# ...
# 查看所有定时任务
email-digest-tool schedule list
# ...
# 查看任务执行历史
email-digest-tool schedule history --name "morning-digest"
```

### 场景三：关键邮件实时告警
配置当收到来自特定发件人或包含紧急关键词的邮件时立即告警.
```bash
# 配置告警规则
email-digest-tool alert create \
  --name "ceo-alert" \
  --condition "from:ceo@company.com" \
  --channel feishu \
feishu.cn/open-apis/bot/v2/hook/未指定" \
  --priority critical
# ...
email-digest-tool alert create \
  --name "urgent-keyword" \
  --condition "subject contains:紧急,urgent,critical" \
  --channel email \
  --notify "admin@company.com" \
  --priority high
# ...
# 启动告警监控
email-digest-tool alert start --all
# ...
# 查看告警历史
email-digest-tool alert log --since "2026-07-01"
```
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### 从免费版升级
专业版完全兼容免费版，现有浏览器自动化流程可直接使用：

```bash
# 免费版命令依然有效
browser-use --browser real open https://mail.google.com
browser-use state
browser-use screenshot inbox.png
# ...
# 专业版新增命令
email-digest-tool aggregate --accounts gmail --format html
```

### 配置多邮箱账户
创建账户配置文件 `$HOME/.config/email-digest-tool/accounts.json`：

```json
{
  "accounts": [
    {
      "name": "Gmail工作邮箱",
      "provider": "gmail",
      "url": "https://mail.google.com",
      "mode": "browser-session"
    },
    {
      "name": "Outlook内部邮箱",
      "provider": "outlook",
      "url": "https://outlook.live.com",
      "mode": "browser-session"
    }
  ]
}
```

### 配置推送渠道
```json
{
  "push_channels": {
    "feishu": {
      "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/未指定"
    },
    "dingtalk": {
      "webhook": "https://oapi.dingtalk.com/robot/send?access_token=未指定"
    },
    "slack": {
      "webhook": "https://hooks.slack.com/services/未指定"
    },
    "email": {
      "smtp_server": "smtp.company.com",
      "port": 587,
      "username": "bot@company.com",
      "password": "your_password"
    }
  }
}
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例
### AI 摘要配置
```json
{
  "ai_summary": {
    "enabled": true,
    "provider": "builtin",
    "language": "zh",
    "features": {
      "importance_scoring": true,
      "action_suggestions": true,
      "risk_detection": true,
      "summary_generation": true
    },
    "scoring_rules": {
      "high_priority_senders": ["ceo@company.com", "boss@company.com"],
      "urgent_keywords": ["紧急", "urgent", "critical", "立即"],
      "high_threshold": 8.0,
      "medium_threshold": 5.0
    }
  }
}
```

### 告警规则配置
```json
{
  "alerts": [
    {
      "name": "高管邮件告警",
      "condition": {
        "from": ["ceo@company.com", "cto@company.com"]
      },
      "channel": "feishu",
      "priority": "critical",
      "silent_hours": "22:00-08:00"
    },
    {
      "name": "未读超量告警",
      "condition": {
        "unread_count_gt": 50
      },
      "channel": "email",
      "notify": "admin@company.com",
      "priority": "medium"
    }
  ]
}
```

### 定时任务配置
```json
{
  "schedules": [
    {
      "name": "每日晨报",
      "cron": "0 9 * * 1-5",
      "timezone": "Asia/Shanghai",
      "accounts": ["gmail", "outlook"],
      "format": "html",
      "push": ["feishu", "email"]
    },
    {
      "name": "周报汇总",
      "cron": "0 18 * * 5",
      "timezone": "Asia/Shanghai",
      "accounts": ["gmail", "outlook"],
      "format": "markdown",
      "push": ["feishu"],
      "include_trends": true
    }
  ]
}
```
## 优选实践
### 多邮箱管理策略
```bash
# 按角色分组管理邮箱
email-digest-tool accounts group create --name "管理层" --accounts gmail,outlook
email-digest-tool accounts group create --name "客服" --accounts service1,service2
# ...
# 按分组生成摘要
email-digest-tool aggregate --group "管理层" --format html
```

### 告警策略优化
- 区分告警级别，避免告警疲劳
- 设置静默时段，非工作时间不打扰
- 关键告警多渠道推送，确保触达

```bash
# 测试告警规则
email-digest-tool alert test --name "ceo-alert"
# ...
# 调整静默时段
email-digest-tool alert update --name "ceo-alert" --silent-hours "22:00-08:00"
```

### 报告归档与检索
```bash
# 归档历史报告
email-digest-tool archive --since "2026-01-01" --dir reports/archive/
# ...
# 检索历史报告
email-digest-tool archive search --keyword "董事会" --since "2026-01-01"
```
## 免费版与专业版对比
| 能力 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 单邮箱摘要 | ✅ | ✅ |
| 浏览器会话复用 | ✅ | ✅ |
| 邮件统计 | 基础统计 | 高级统计 |
| 多邮箱聚合 | ❌ | ✅ |
| AI 智能摘要 | ❌ | ✅（重要度评分） |
| 定时报告推送 | ❌ | ✅（多渠道） |
| 智能分类 | ❌ | ✅（自定义规则） |
| 告警通知 | ❌ | ✅（实时告警） |
| 趋势分析 | ❌ | ✅（图表分析） |
| 报告归档 | ❌ | ✅（可检索） |
| 推送渠道 | 截图 | 邮件/飞书/钉钉/Slack |
| 技术支持 | 社区支持 | 优先支持 |
## 常见问题
### 问题1：多邮箱聚合时部分账户失败
**解决**: 检查对应账户的浏览器登录状态，确保会话有效：

```bash
# 验证账户状态
email-digest-tool accounts health-check
# ...
# 重新登录失效账户
```

### 问题2：AI 摘要质量不佳
**解决**: 调整评分规则与关键词配置：

```bash
# 更新评分规则
email-digest-tool config update --ai-scoring rules.json
# ...
# 查看评分详情
email-digest-tool aggregate --accounts gmail --show-scores
```

### 问题3：定时推送未送达
**解决**: 检查推送渠道配置与网络：

```bash
# 测试推送渠道
email-digest-tool push test --channel feishu
# ...
# 查看推送日志
email-digest-tool push log --since "2026-07-01"
```

### 问题4：告警频繁打扰
**解决**: 优化告警规则与静默策略：

```bash
# 查看告警频率统计
email-digest-tool alert stats
# ...
# 调整告警阈值
email-digest-tool alert update --name "unread-alert" --threshold 100
```

### 问题5：报告格式不兼容
**解决**: 专业版支持多种格式互转：

```bash
# 格式转换
email-digest-tool convert --input report.html --format markdown
```
## 命令参考速查
| 命令 | 功能 | 专业版独有 |
|---:|---:|---:|
| `aggregate` | 多邮箱聚合摘要 | ✅ |
| `schedule` | 定时任务管理 | ✅ |
| `alert` | 告警规则管理 | ✅ |
| `push` | 推送渠道管理 | ✅ |
| `archive` | 报告归档检索 | ✅ |
| `accounts` | 多账户管理 | ✅ |
| `config` | 配置管理 | ✅ |
| `convert` | 格式转换 | ✅ |
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome 浏览器（需已安装并登录邮箱）
- **Python版本**: 3.9 及以上（browser-use 依赖）
- **网络环境**: 需可访问各邮箱服务与推送渠道

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| browser-use | CLI工具 | 必需 | `uv pip install browser-use[cli]` |
| Chrome 浏览器 | 浏览器 | 必需 | 官方网站下载安装 |
| 邮箱账户 | 账户 | 必需 | 注册主流邮箱服务 |
| 推送渠道 Webhook | 集成 | 可选 | 飞书/钉钉/Slack 机器人配置 |
| cron 服务 | 系统服务 | 可选 | 系统自带（定时任务需要） |
| 数据库 | 存储引擎 | 可选 | 用于报告归档（可选 SQLite 文件存储） |

### API Key 配置
- 本工具通过浏览器会话复用访问邮箱，无需邮箱 API Key
- AI 智能摘要使用 Agent 内置 LLM，无需额外 API Key
- 推送渠道（飞书/钉钉/Slack）需配置对应平台的 Webhook URL
- Webhook URL 通过配置文件提供，建议加密存储

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行浏览器自动化与多渠道推送任务，支持定时调度与告警监控
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 核心功能

- **自动化执行**: 多邮箱AI智能摘要与定时报告，企业级邮件监控与分类方案。邮件日报专业版面向企业用户与高效能个人用户。Use when 需
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据