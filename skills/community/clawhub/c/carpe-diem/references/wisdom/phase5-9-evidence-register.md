# Phase 5–9 证据登记册

> 本文件属于研究层，不在普通对话中自动加载。卡片运行时不复述来源，但维护者必须能从这里定位原始依据。

| ID | 行为卡 | 一手来源定位 | 状态 | 忠实度校正 |
|---|---|---|---|---|
| WD-P5-01 | `validate/pricing-test.md` | [Strategyzer：证据强度从说到做](https://www.strategyzer.com/library/business-testing-is-your-hypothesis-really-validated) | verified-primary | 区分点击、低成本行为和真实承诺；删除通用转化率 |
| WD-P5-02 | `validate/competitive-analysis.md` | [Steve Blank：Customer Discovery](https://steveblank.com/tag/customer-discovery/)；[Blue Ocean Strategy：Strategy Canvas](https://www.blueoceanstrategy.com/tools/strategy-canvas/) | verified-primary | 从同类功能比较扩展到替代方案、选择因素和切换证据 |
| WD-P5-03 | `validate/experiment-design.md` | [Strategyzer：实验与证据强度](https://www.strategyzer.com/programs/design-experiments-prepare-to-test-your-business-idea-part-2) | verified-primary | 与 test-card 分工；最低成本必须仍提供足够有效证据 |
| WD-P5-04 | `validate/gonogo-decision.md` | [Strategyzer：证据驱动继续、转向或停止](https://www.strategyzer.com/library/the-role-of-an-effective-innovation-coach) | verified-primary | 删除普适人数和比例；先审计证据质量 |
| WD-P5-05 | `validate/user-interview.md` | [Product Talk：故事式访谈问题](https://www.producttalk.org/best-customer-interview-questions/) | verified-primary | 询问最近真实行为；定性访谈不预测总体比例 |
| WD-P6-01 | `cross/premature-optimization.md` | [Go 官方文档：Diagnostics / Profiling](https://go.dev/doc/diagnostics) | verified-primary | 以测量和 profiling 定位高成本路径；不把语言工具细节泛化为所有项目的固定流程 |
| WD-P6-02 | `cross/feature-creep.md` | [Basecamp Shape Up：Decide When to Stop](https://basecamp.com/shapeup/3.5-chapter-14) | verified-primary | 与 say-no-by-default 区分为事后范围治理 |
| WD-P6-03 | `cross/analysis-paralysis.md` | [Amazon 2016 Shareholder Letter：two-way doors](https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders) | verified-primary | 不使用固定信息比例；加入真实可逆性和重开条件 |
| WD-P6-04 | `cross/unicorn-mindset.md` | [Paul Graham：Do Things that Don't Scale](https://paulgraham.com/ds.html) | verified-primary | 小核心是学习单位，不保证成功或指数增长 |
| WD-P7-01 | `plan/rfc-design.md` | [React RFC 官方流程](https://github.com/reactjs/rfcs) | verified-primary | RFC 用于决策形成前反馈；ADR 用于决定后记录 |
| WD-P7-02 | `track/code-review.md` | [Google Engineering Practices：Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | verified-primary | “小”是自包含概念改动，无固定 200 行规则 |
| WD-P7-03 | `track/retrospective.md` | [Google SRE：Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) | verified-primary | 无指责不等于无责任；要求复核和可验证行动 |
| WD-P7-04 | `track/tech-debt.md` | [Martin Fowler：Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html) | verified-primary | 债务按利息和改动频率治理，不套固定 20% |
| WD-P7-05 | `cross/async-communication.md` | [GitLab Handbook：Communication](https://handbook.gitlab.com/handbook/communication/) | verified-primary | 异步优先但不是异步唯一；删除 24h 和每周一次硬规则 |
| WD-P8-01 | `cross/growth-flywheel.md` | [Andrew Chen：The Cold Start Problem，Atomic Network](https://andrewchen.com/wp-content/uploads/2022/01/ColdStartProb_9780062969743_AS0928_cc20_Final.pdf) | verified-primary | 先验证最小网络密度；不要求所有产品传播系数大于一 |
| WD-P8-02 | `cross/user-retention.md` | [Nir Eyal：Hooked](https://www.nirandfar.com/hooked)；[Manipulation Matrix](https://www.nirandfar.com/the-art-of-manipulation/) | verified-primary | 以用户价值为前提，加入退出和反操纵边界 |
| WD-P8-03 | `cross/product-strategy.md` | [SVPG：Product Strategy Overview](https://www.svpg.com/product-strategy-overview/) | verified-primary | 战略改为聚焦、洞察、行动和持续管理，不是功能清单 |
| WD-P8-04 | `cross/continuous-discovery.md` | [Product Talk：Continuous Discovery 定义](https://www.producttalk.org/glossary-discovery-continuous-discovery/) | verified-primary | 周节奏是理想基准；按环境调整并关注决策影响 |
| WD-P9-01 | `plan/api-design.md` | [Stripe：API release process](https://stripe.com/blog/introducing-stripes-new-api-release-process) | verified-primary | 从“第一天 URL 版本化”改为按兼容边界选择变更策略 |
| WD-P9-02 | `track/observability.md` | [Honeycomb：Observability Tool](https://www.honeycomb.io/blog/so-you-want-to-build-an-observability-tool) | verified-primary | 删除“三支柱缺一不可”和“提前预知问题”的定义 |
| WD-P9-03 | `plan/data-modeling.md` | [PostgreSQL：Data Definition](https://www.postgresql.org/docs/current/ddl.html)；[Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) | verified-primary | 删除 3NF、JSON 扩展点和只加字段等通用处方；加入演进路径 |
| WD-P9-04 | `plan/security-design.md` | [OWASP：Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | verified-primary | 外部边界语法校验 + 领域语义和授权校验 |

## 状态汇总

- `verified-primary`：22 张；
- `needs-primary-source-check`：0 张；
- `verified-multiple`：0 张；
- `rejected`：0 张。

## 接受规则

- `needs-primary-source-check` 不得在规划或卡片中宣称已经完成来源核验；
- 状态升级时保留精确 URL、主张摘要、适用前提和忠实度校正；
- 反模式若宣称跨场景普适，应补第二个独立来源后升级为 `verified-multiple`；
- 卡片合并或拒绝时保留 ID，并记录迁移目标或拒绝原因。
