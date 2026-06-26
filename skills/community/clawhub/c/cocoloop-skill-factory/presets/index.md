# 任务域预设目录

## 目标

这里放的是 `skill-factory` 在调研、设计和构建准备阶段可以直接引用的任务域预设。
预设不是最终 Skill，也不是平台模板。
预设负责三件事：

- 帮主流程先判断任务属于哪个域
- 帮调研阶段少走弯路，直接使用高频问题包
- 帮设计和构建准备阶段快速收口推荐执行面、风险边界和默认产物

## 第一层优先预设

| 预设 | 适用方向 | 文档 |
| --- | --- | --- |
| 工程交付 | PR、CI、仓库维护、MCP、Skill 构建 | [engineering-delivery.md](./engineering-delivery.md) |
| 前端与设计到代码 | 页面、界面、设计稿实现、设计系统 | [frontend-design.md](./frontend-design.md) |
| 浏览器自动化与 UI 测试 | 截图、快照、交互验证、持久 QA | [browser-ui-testing.md](./browser-ui-testing.md) |
| 文档与办公产物 | PDF、Word、PPT、Excel 处理与生成 | [document-artifacts.md](./document-artifacts.md) |
| 文档检索与研究 | 官方文档检索、引用、知识沉淀、研究整理 | [docs-research.md](./docs-research.md) |

## 第二层扩展预设

| 预设 | 适用方向 | 文档 |
| --- | --- | --- |
| 工作流集成 | Notion、Linear、Slack、Jira、飞书、钉钉等系统联动 | [workflow-integration.md](./workflow-integration.md) |
| 部署与平台运维 | 部署、回滚、环境配置、线上健康检查 | [deploy-platform-ops.md](./deploy-platform-ops.md) |
| 安全与风险审查 | 权限、凭据、依赖、日志、威胁建模和发布前风险检查 | [security-risk-review.md](./security-risk-review.md) |

## 业务横向扩展预设

| 预设 | 适用方向 | 文档 |
| --- | --- | --- |
| 内容运营 | SEO、公众号、小红书、博客、邮件、社媒和多渠道内容生产 | [content-ops.md](./content-ops.md) |
| 知识库运营 | Obsidian、Notion、钉钉文档、飞书文档、wiki 化和日常维护 | [knowledge-base-ops.md](./knowledge-base-ops.md) |
| 数据分析与报告 | CSV、Excel、日志、经营数据、图表、周报、月报和仪表盘 | [data-analysis-reporting.md](./data-analysis-reporting.md) |
| 客户支持运营 | 客服对话、工单、FAQ、回复草稿、反馈分析和升级规则 | [customer-support-ops.md](./customer-support-ops.md) |
| 电商增长运营 | 商品内容、活动策划、竞品分析、经营报告和店铺系统联动 | [ecommerce-growth-ops.md](./ecommerce-growth-ops.md) |
| 投研与财务分析 | 公司、行业、市场、财报、组合和风险报告 | [finance-investment-research.md](./finance-investment-research.md) |
| 销售与 CRM 运营 | 线索、商机、客户跟进、漏斗分析和 CRM 写回 | [sales-crm-ops.md](./sales-crm-ops.md) |
| 人力与招聘运营 | JD、简历、面试、候选人、入职和 HR 流程 | [hr-recruiting-ops.md](./hr-recruiting-ops.md) |
| 教育与培训运营 | 课程、教案、题库、课件、学习报告和培训计划 | [education-training-ops.md](./education-training-ops.md) |
| 法务与合同运营 | 合同摘要、条款比对、风险清单、审批和归档 | [legal-contract-ops.md](./legal-contract-ops.md) |
| 产品与市场研究 | 用户反馈、竞品、市场、PRD 输入和机会地图 | [product-market-research.md](./product-market-research.md) |
| 活动与社群运营 | 活动方案、社群日历、报名反馈、复盘和系统写回 | [event-community-ops.md](./event-community-ops.md) |

## 每个预设都固定包含

- `domain_id`
- `common_jobs`
- `default_question_pack`
- `recommended_execution_planes`
- `risk_and_gates`
- `default_outputs`

## default_question_pack 的使用规则

- 它是候选问题池，不是整包必问清单。
- 进入调研后，先从预设里排出最小问题集，再开始追问。
- 整轮需求调研默认不超过 10 个问题，确认题也计入预算。
- 能用已有上下文、环境检测、默认值和确认题解决的，不再重复追问。
- 如果预设问题还没问完但预算已接近上限，把剩余不确定项写入 `open_gaps`，不要继续拉长访谈。

## 使用顺序

1. 先判断主任务域。
2. 如果明显跨域，再补 `peer_domains`。
3. 读取对应预设，使用默认问题包继续调研。
4. 读取预设里的执行面建议，作为设计阶段的默认候选。
5. 读取预设里的默认输出，帮助生成 `spec.yaml`、研究摘要和构建计划。

## 组合规则

- 单域需求：只使用一个预设。
- 跨域需求：先用主域预设，再把次域当补充约束。
- 如果没有预设完全匹配：先选最接近的主域预设，再把剩余部分写入 `open_gaps`。
- 如果需求高度独特：允许跳过预设，但必须在研究产物里说明原因。
