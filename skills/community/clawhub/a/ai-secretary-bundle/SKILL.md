---
name: ai-secretary-bundle
version: 1.0.0
description: |
  AI秘书套装 - 24小时智能助理，整合邮件管理、日程提醒、新闻摘要、待办管理四大核心能力。专为企业高管、自由职业者和忙碌专业人士设计，每天节省1-2小时工作时间。定价¥99/套。
---

# AI秘书套装 (AI Secretary Bundle)

> 你的24小时智能助理，让效率翻倍，让时间自由

## 💼 套装定位

专为忙碌的专业人士、企业主和高管设计，整合邮件、日程、资讯和任务管理四大核心能力，打造一站式AI秘书体验。

---

## 🎯 包含技能

### 1. 邮件管理 (email-mail-master)
- **功能**：多邮箱统一管理、智能摘要、自动分类、定时发送
- **适用场景**：每日邮件处理、批量回复、邮件归档
- **价值**：节省每天1-2小时邮件处理时间

### 2. 日程提醒 (qqbot-cron / cron)
- **功能**：智能定时提醒、周期性任务、重要事项通知
- **适用场景**：会议提醒、截止日期、习惯养成
- **价值**：不再错过任何重要事项

### 3. 每日新闻摘要 (ai-news-collector / ai-news-oracle)
- **功能**：AI领域最新动态、热度排序、中文摘要
- **适用场景**：晨间简报、行业动态追踪
- **价值**：10分钟掌握全天重要资讯

### 4. 待办管理 (task-tracker)
- **功能**：任务状态追踪、进度更新、失败恢复
- **适用场景**：项目管理、个人任务追踪
- **价值**：任务可视化，进度一目了然

---

## 📦 套装内容

```
ai-secretary-bundle/
├── SKILL.md                 # 本文件 - 套装总览
├── config/
│   ├── email-config.yaml    # 邮箱配置模板
│   ├── cron-schedule.yaml   # 定时任务模板
│   └── news-sources.yaml    # 新闻源配置
├── examples/
│   ├── daily-routine.md     # 每日工作流程示例
│   ├── meeting-prep.md      # 会议准备示例
│   └── weekly-review.md     # 周回顾示例
└── README.md                # 快速上手指南
```

---

## 🚀 快速开始

### 第一步：安装技能

```powershell
# 安装邮件管理
py -m clawhub install email-mail-master

# 安装定时提醒
py -m clawhub install qqbot-cron

# 安装新闻收集
py -m clawhub install ai-news-collector

# 安装任务追踪
py -m clawhub install task-tracker
```

### 第二步：配置邮箱

编辑 `config/email-config.yaml`：

```yaml
email_accounts:
  - name: "工作邮箱"
    type: "imap"
    server: "imap.company.com"
    username: "your-email@company.com"
    password: "${EMAIL_PASSWORD}"
    folders:
      - "INBOX"
      - "Sent"
      - "Important"
  
  - name: "个人邮箱"
    type: "gmail"
    username: "your-email@gmail.com"
    app_password: "${GMAIL_APP_PASSWORD}"
```

### 第三步：设置每日简报

```powershell
# 设置每天早上8点的新闻摘要
py -m clawhub run cron:add --name "daily-news" --schedule "0 8 * * *" --task "ai-news-collector --category=ai --summary=true"
```

---

## 💡 典型使用场景

### 场景1：晨间例行 (Morning Routine)

```
用户：开始我的一天

AI秘书：
📧 邮件摘要：您有5封新邮件，2封需要回复
   - 来自张总：项目进度询问（高优先级）
   - 来自李经理：会议改期通知

📰 今日AI资讯（3条热榜）：
   1. OpenAI发布GPT-5预览版...
   2. Google Gemini 2.0重大更新...
   3. 国内大模型价格战升级...

📋 今日待办：
   ☐ 上午10点 - 产品评审会
   ☐ 下午2点 - 客户电话
   ☐ 本周五前 - 提交季度报告

需要我帮您回复张总的邮件吗？
```

### 场景2：会议准备

```
用户：帮我准备下午3点的项目评审会

AI秘书：
✅ 已为您准备会议资料：

📎 相关邮件：
   - 项目启动邮件（3月15日）
   - 上周进度更新（3月18日）

📊 待讨论事项：
   1. 技术方案确认
   2. 时间节点调整
   3. 资源分配问题

⏰ 已设置会议提醒：下午2:45
📧 已发送会议议程给参会人员
```

### 场景3：周回顾

```
用户：帮我做本周回顾

AI秘书：
📈 本周数据概览：
   - 处理邮件：127封
   - 完成任务：23项
   - 参加会议：8场
   - 节省时间：约12小时

🎯 下周重点：
   - 周一：产品发布准备
   - 周三：客户演示
   - 周五：团队复盘

⚠️ 需要关注：
   - 3个任务即将到期
   - 2封邮件待回复超过48小时
```

---

## ⚙️ 配置模板

### 定时任务配置

```yaml
# config/cron-schedule.yaml
cron_jobs:
  - name: "morning-briefing"
    schedule: "0 8 * * 1-5"
    tasks:
      - "email-mail-master:summary --unread-only"
      - "ai-news-collector --category=ai,tech"
      - "task-tracker:list --today"
  
  - name: "weekly-review"
    schedule: "0 18 * * 5"
    tasks:
      - "email-mail-master:stats --week"
      - "task-tracker:report --week"
  
  - name: "end-of-day"
    schedule: "0 18 * * 1-5"
    tasks:
      - "task-tracker:remind --tomorrow"
      - "email-mail-master:check --flagged"
```

### 新闻源配置

```yaml
# config/news-sources.yaml
news_sources:
  ai:
    - "OpenAI Blog"
    - "Google AI Blog"
    - "Anthropic News"
    - "机器之心"
    - "量子位"
  
  tech:
    - "TechCrunch"
    - "The Verge"
    - "36氪"
    - "虎嗅"
  
  filter:
    keywords:
      - "AI"
      - "大模型"
      - "ChatGPT"
      - "Claude"
    exclude:
      - "广告"
      - "招聘"
```

---

## 💰 定价与价值

| 项目 | 传统方案 | AI秘书套装 |
|------|----------|------------|
| 邮件处理 | 2小时/天 | 30分钟/天 |
| 资讯获取 | 1小时/天 | 10分钟/天 |
| 任务管理 | 手动记录 | 自动追踪 |
| 月度成本 | ¥3000+ (助理) | **¥99** |

**套装定价：¥99/套（一次性购买，终身使用）**

---

## 🛠️ 技术要求

- OpenClaw >= 2.0
- Windows 10/11 或 macOS 或 Linux
- 网络连接（用于邮件同步和新闻获取）

---

## 📞 售后支持

- 文档：https://docs.clawhub.com/ai-secretary
- 社区：加入飞书群获取更新
- 更新：购买后终身免费更新

---

*让AI成为你的超级助理，把时间留给更重要的事。*
