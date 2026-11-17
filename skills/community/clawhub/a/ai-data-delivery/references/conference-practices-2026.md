# 2026公开实践：吸收了什么、没有吸收什么

核验日期2026-11-01。这里记录设计依据，不代表合作、认证或厂商效果复现。部分会议只有公开摘要，以下技术细节优先使用可读取的官方文档；没有取得的PPT/录像不声称读过。

| 公开来源及证据层次 | 可迁移机制 | 本仓落点与验证 |
| --- | --- | --- |
| [QCon Datus提纲](https://qcon.infoq.cn/2026/shanghai/presentation/7342)及[DOSI工具文档](https://dosi.datus.ai/agents/) | 指标到明细保留同一语义；聚合与关联必须查粒度，统一定义本身也可能错误 | `query_bundle`同范围、同快照；3/2/1计数、NULL、稳定分页、错误无半成品。保留已有扇出反例；不新增通用多表编译器 |
| [QCon DIBP](https://qcon.infoq.cn/2026/shanghai/presentation/7343)和[AIDE](https://qcon.infoq.cn/2026/shanghai/presentation/7356)：仅公开摘要 | 上下文需要生产、治理、更新、消费；反馈成为规则前需验证 | `select_context`选依赖、保留推断等级、模型变更失效；既有guide_model确认机制继续使用，不另造审批状态机 |
| [Snowflake Autopilot](https://docs.snowflake.com/en/user-guide/views-semantic/autopilot)、[建议队列](https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-suggestions)、[评测文档](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst-evaluations) | 自动生成后需核对；建议不直接发布；运行示例与评测答案分离 | 复用元数据候选，独立硬编码数值与另造数据的前向试用；示例不是泛化评测，无自动提升确认级别 |
| [Databricks Genie Ontology](https://docs.databricks.com/aws/en/genie/genie-ontology)：当前Public Preview文档，非本次实测 | 治理定义与推断片段分开；来源、使用、新鲜度不能替代业务批准 | 上下文保留来源引用与证据等级；明确只提供本地片段，没有Unity Catalog ACL或权威评分引擎 |
| [FabCon发布](https://azure.microsoft.com/en-us/blog/fabcon-and-sqlcon-2026-in-barcelona-building-the-data-foundation-for-microsoft-copilot-and-agents/)及[Ontology Agent文档](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-use-ontology-agent) | 复用已有模型、保留身份；语义变更与数据刷新分别看 | 修复字段依赖lint/drift；证据同时保留模型和快照指纹。已有derive保持稳定ID，不自动覆盖人工描述 |
| [Semantic Layer Summit议程](https://www.semanticlayersummit.com/agenda/)与[案例回顾](https://www.atscale.com/blog/semantic-layers-critical-ai-infrastructure/) | 多消费者共用指标定义，原有可见范围仍有效 | 数值与明细双形态核对，消费者投影检查连接键和来源；不移植案例KPI数、准确率或成本效果 |
| [Collate Context Center](https://docs.getcollate.io/ai-2-0/collate-ai/context-center)：当前产品文档 | 文档副本不自动更新，链接不等于正文，各消费者能读到的内容可能不同 | 包标snapshot、列出省略内容/引用；验证旧包和篡改包拒绝。不声称外部链接已读或消费者完整兼容 |
| [DTCC NineData会后整理](https://ninedata.cloud/newsinfo/11298629.html)、[启动API](https://docs.ninedata.cloud/openapi/replication/startreplicationtask/)、[任务状态API](https://docs.ninedata.cloud/openapi/replication/queryreplicationtaskstatus/) | 请求受理不能代表任务完成 | consumer错误/拒绝/未完成回执即使带正确数值也不通过。不在语义skill内实现生产CDC或任务调度 |
| [云栖Agent论坛](https://yunqi.aliyun.com/2026/session?agendaId=133)与[实时论坛](https://yunqi.aliyun.com/2026/session?agendaId=107)：读取公开议程，未获取录像 | Context与FDE协作值得关注；议程不足以证明具体执行机制 | 暂不新增实时基础设施。交通实践以批次/T+1为主，本轮用快照作证，不因热门议题扩范围 |
| [DataHub scoped MCP文档](https://docs.datahub.com/docs/features/feature-guides/scoped-mcp-servers) | 搜索范围不是权限撤销 | 明确上下文选择不等于授权；本地mock不能证明租户隔离。CONTEXT大会11月4日尚未举办，不引用为已发生实践 |

本轮没有加入生产网关、自动读取所有历史SQL、跨引擎推理、OWL/SHACL、实时权限中心。已有工具中的执行缺陷优先于新增架构。具体可复制命令和反例在[指标消费路径](metric-context.md)；完成的证据与未验证范围在[v0.0.12验证记录](v0.0.12-validation.md)。
