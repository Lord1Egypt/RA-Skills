# Deal Closer / 成交加速器

> 智能 CRM 助手 — 商机管理、邮件信号提取、销售漏斗分析、AI 跟进邮件起草、自学习销售智能、CRM 知识图谱
>
> Smart CRM Assistant — Deal management, email signal extraction, pipeline analytics, AI follow-up drafting, self-learning sales intelligence, CRM knowledge graph

---

## 功能亮点 / Features

- **商机全生命周期管理** — 从线索到成交，8 个阶段精细化追踪，自动记录阶段变更历史
  - Full deal lifecycle management — 8 stages from lead to close, with automatic stage history tracking

- **邮件信号提取** — 扫描 Gmail / Outlook 邮件，自动识别积极/消极/中性信号，关联商机
  - Email signal extraction — Scan Gmail / Outlook, auto-detect positive/negative/neutral signals

- **销售漏斗分析** — 漏斗转化率、加权收入预测、风险预警，一键生成报告
  - Pipeline analytics — Funnel conversion, weighted forecast, risk alerts, one-click reports

- **AI 跟进邮件** — 基于商机上下文和互动历史，智能起草跟进邮件，5 种模板覆盖全流程
  - AI follow-up drafting — Context-aware email drafts with 5 templates covering the full sales cycle

- **会议追踪** — 记录会议纪要、行动项和下一步，汇总摘要一目了然
  - Meeting tracking — Log notes, action items and next steps, generate meeting summaries

- **自学习销售智能** — 从成交模式中持续学习，预测商机胜率，提供教练建议
  - Self-learning sales intelligence — Learn from deal outcomes, predict win rates, provide coaching tips

- **CRM 关系图谱** — 可视化客户关系网络，追踪决策人、组织架构和影响力链路
  - CRM knowledge graph — Visualize contact networks, track decision makers, org charts and influence chains

- **原生邮件支持** — 任意邮箱直连(IMAP/SMTP)，无需 OAuth2 配置，支持 QQ/163/Gmail/Outlook 等
  - Native email support — Direct IMAP/SMTP connection, works with any email provider

- **Mermaid 可视化** — 饼图、柱状图、折线图、关系图谱内嵌报告，无需额外工具
  - Mermaid visualization — Pie, bar, line charts, relationship graphs embedded in reports

- **数据安全** — 所有数据本地存储，手机号和邮箱自动脱敏
  - Data security — All data stored locally, phone and email auto-masked

---

## 版本对比 / Plan Comparison

| 功能 / Feature | 免费版 / Free | 付费版 / Paid ¥149/月 |
|----------------|:------------:|:--------------------:|
| 商机管理 / Deal CRUD | 最多 30 个 | 最多 500 个 |
| 基础漏斗报告 / Basic funnel | 支持 | 支持 |
| CSV 导出 / CSV export | 支持 | 支持 |
| 手动跟进 / Manual follow-up | 支持 | 支持 |
| 邮件扫描 / Email scan (Gmail/Outlook/IMAP) | - | 支持 |
| IMAP/SMTP 原生邮件 / Native email | - | 支持 |
| 会议日历同步 / Calendar sync | - | 支持 |
| 收入预测 / Revenue forecast | - | 支持 |
| AI 跟进邮件 / AI follow-up | - | 支持 |
| 自动跟进起草 / Auto follow-up draft | - | 支持 |
| Mermaid 图表 / Mermaid charts | - | 支持 |
| 高级分析 / Advanced analytics | - | 支持 |
| 自学习销售智能 / Self-learning intelligence | - | 支持 |
| CRM 知识图谱 / CRM knowledge graph | - | 支持 |
| AI 胜率预测 / AI win prediction | - | 支持 |
| 批量导入 / Bulk import | - | 支持 |

---

## 快速开始 / Quick Start

### 1. 安装 / Install

在 ClawHub 中搜索 `deal-closer`，点击安装，或使用命令行：

```bash
openclaw skill install deal-closer
```

### 2. 添加商机 / Add a Deal

```bash
/deal-closer add --data '{"name":"企业ERP升级项目","contact_name":"张经理","company":"科技有限公司","amount":"50万","stage":"初步接触"}'
```

### 3. 查看管道 / View Pipeline

```bash
/deal-closer funnel
```

### 4. 起草跟进邮件 / Draft Follow-up (Paid)

```bash
/deal-closer draft --data '{"deal_id":"D20260319...","sender_name":"销售经理"}'
```

### 5. 扫描邮件 / Scan Emails (Paid)

```bash
# 配置邮箱凭据
export DC_GMAIL_CREDENTIALS="/path/to/credentials.json"

/deal-closer scan
```

---

## 使用示例 / Example

```
用户：帮我添加一个商机，名称是"智慧园区项目"，联系人王总，公司是鑫科技，金额 200 万，阶段是需求确认。

助手：商机「智慧园区项目」已添加！

| 字段 | 值 |
|------|-----|
| ID | D20260319143022... |
| 名称 | 智慧园区项目 |
| 联系人 | 王总 |
| 公司 | 鑫科技 |
| 金额 | ¥200.00万 |
| 阶段 | 需求确认 |
| 成交概率 | 25% |

建议：需求确认阶段建议尽快安排面谈，深入了解客户具体需求后提交方案。
```

---

## 数据存储 / Data Storage

所有数据以 JSON 格式存储在本地：

```
~/.openclaw-bdi/deal-closer/
  deals.json         # 商机数据
  emails.json        # 邮件记录
  meetings.json      # 会议记录
  followups.json     # 跟进计划
  learning.json      # 自学习数据（成交模式、预测模型）
  crm_graph.json     # CRM 知识图谱
  email_config.json  # IMAP/SMTP 连接配置（不含密码）
```

可通过 `DC_DATA_DIR` 环境变量自定义存储路径。

---

## 常见问题 / FAQ

### Q1: 免费版有哪些限制？
免费版支持最多 30 个商机管理、基础漏斗报告和 CSV 导出。邮件扫描、AI 跟进、高级分析等功能需付费版。

### Q2: 数据会上传到云端吗？
不会。所有数据存储在本地 JSON 文件中，不会离开你的运行环境。

### Q3: 如何配置邮件扫描？
详见 `references/email-setup-guide.md`，需完成 Gmail OAuth2 或 Outlook Azure AD 配置。

### Q4: 支持哪些邮件类型的信号识别？
支持中英文关键词匹配，自动识别积极（同意、感兴趣等）、消极（推迟、竞争对手等）和中性（咨询、了解等）信号。

### Q5: Mermaid 图表在哪里可以渲染？
GitHub / GitLab Markdown 预览、VS Code（Mermaid 插件）、Typora、Obsidian 等工具均支持。

### Q6: 如何从其他 CRM 迁移数据？
准备标准 CSV 文件（支持中英文列名），使用导入功能即可批量迁移。

---

## 技术支持 / Support

- 文档 / Docs：查看 `references/` 目录
- 问题反馈 / Issues：在 ClawHub Skill 页面提交
- 社区 / Community：`#deal-closer` 频道
- 邮件 / Email：skill-support@clawhub.dev

---

*deal-closer v1.1.0 | 兼容 OpenClaw 0.5+*
