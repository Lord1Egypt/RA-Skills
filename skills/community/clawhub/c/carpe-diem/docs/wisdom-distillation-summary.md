# Carpe Diem 智慧蒸馏总结

> 本文档汇总了 Carpe Diem 智慧蒸馏工作的完整全景——从研究到产出，从人物到卡片。
> 最后更新：2026-08-31（Phase 5-9 已产出 22 张候选卡；55 张运行文件通过结构校验，新增来源核验仍在推进）

> 状态说明：卡片“已创建”不再等同于“已完成蒸馏验收”。本轮 22 张新增卡均已核到可公开复查的一手来源，并通过证据、边界和路由验收。

---

## 一、蒸馏哲学

Carpe Diem 的智慧蒸馏采用“研究层可追溯、运行层不露来源”的双层规则：

| 规则 | 含义 | 检查标准 |
|------|------|---------|
| **运行时不露来源** | 卡片使用 Carpe Diem 自己的语言，不靠权威背书 | 运行卡不复述来源；研究登记册保留精确出处 |
| **不抽象** | 不是"什么是 X"，而是"当你遇到 Y 时，怎么做 Z" | 每条都有触发条件 + 行为指导 |
| **可操作** | 用户直接得到 actionable 的指导，不是"大师名言" | 指导步骤可在 3-5 轮对话内执行 |

我们不模拟 Paul Graham 的语气、不照搬 Lean Startup 的完整体系、不引入理论官僚主义。每个智慧来源被提炼为 1-3 条可操作的规则，以**行为卡**形式嵌入 Carpe Diem 的现有流程。

---

## 二、研究阶段：覆盖了谁

### Discover 阶段（发现方向）

| 人物 | 核心智慧 | 对 Carpe Diem 的作用 |
|------|---------|-------------------|
| Paul Graham | 从自身摩擦出发、"脏活测试"、做不规模化的手工事 | 引导用户从个人生活摩擦找方向 |
| Rob Fitzpatrick | Mom Test——聊用户的生活，不聊自己的想法 | 帮用户区分"承诺信号"和"礼貌性赞美" |
| Clayton Christensen | JTBD——用户"雇用"产品完成工作 | 帮用户从功能/社交/情感三维度描述机会 |
| Peter Thiel | 从 0 到 1——秘密测试、垄断定位 | 帮用户问"为什么没人做这个" |
| Jason Fried & DHH | Scratch your own itch、最小切口、可持续性 | 帮用户用"不做什么"检验方向 |

### Validate 阶段（验证假设）

| 人物 | 核心智慧 | 对 Carpe Diem 的作用 |
|------|---------|-------------------|
| Eric Ries | Build-Measure-Learn 验证循环 | 验证流程的基础框架 |
| Steve Blank | Customer Development——走出办公室 | 不能只靠桌面研究 |
| Ash Maurya | Lean Canvas——风险排序 | 帮用户优先验证最危险的假设 |
| David Bland | Test Card——实验系统化 | 把假设写成可测试的"如果…那么…" |
| Cindy Alvarez | 低成本持续验证 | 验证不是一次性活动 |

**经典验证案例**：Zappos（手工拍照验证）、Dropbox（视频验证）、Buffer（落地页先行）、Groupon（手工 PDF 优惠券）、Food on the Table（跟用户回家）、AppSumo（手工测试）、Dollar Shave Club（手工打包）、Product Hunt（手工邀请）、Kickstarter（视频验证）、Gumroad（MVP 落地页）

### Plan 阶段（制定计划）

| 人物 | 核心智慧 | 对 Carpe Diem 的作用 |
|------|---------|-------------------|
| Ryan Singer (Shape Up) | Appetite 约束、Hill Chart 确定性分级 | 限制时间，而非限制范围 |
| Eric Evans (DDD) | Bounded Context、Ubiquitous Language | 上下文边界和统一语言 |
| Michael Nygard (Release It!) | 生产环境实战、容错设计 | 计划要考虑崩溃和恢复 |
| Frederick Brooks (Mythical Man-Month) | Brooks 定律、没有银弹 | 计划和实际是不同的 |
| Martin Fowler (Refactoring) | 技术债务、持续重构 | 计划要包含重构周期 |
| Simon Brown (C4 Model) | 架构可视化——Context/Container/Component/Code | 沟通架构的通用语言 |
| Richard Rumelt (Good Strategy) | 诊断→方针→连贯行动 | 战略不是目标，是连贯行动 |
| Alistair Cockburn (Agile) | 不确定性的三个层次 | 按不确定性级别选择计划方法 |

### Track 阶段（追踪进度）

| 人物 | 核心智慧 | 对 Carpe Diem 的作用 |
|------|---------|-------------------|
| Gene Kim (The Phoenix Project) | 三步工作法——流动/反馈/持续学习 | 追踪不再是"老板看你完没完成" |
| Nicole Forsgren (Accelerate) | 四种关键指标——部署频率/变更前置时间/变更失败率/恢复时间 | 用指标驱动决策 |
| David J. Anderson (Kanban) | 可视化工作流、WIP 限制、瓶颈管理 | 可视化进度并识别瓶颈 |
| Eliyahu Goldratt (The Goal) | Theory of Constraints——找到并消除瓶颈 | 把约束作为追踪焦点 |
| Kent Beck (XP/TDD) | 测试驱动、持续集成、简单设计 | 追踪质量信号 |
| Ryan Singer (Shape Up) | Hill Chart——不确定性可视化 | 把"不知道"也画出来 |

### 跨阶段通用

| 人物 | 核心智慧 | 对 Carpe Diem 的作用 |
|------|---------|-------------------|
| DHH (Rework) | 减法思维、默认说不、不要做大 | 贯穿所有阶段的决策原则 |
| John Ousterhout (A Philosophy of Software Design) | 复杂度管理——每次改动都在降低复杂度 | 复杂度是持续的敌人 |
| Geoffrey Moore (Crossing the Chasm) | 滩头阵地——先攻一个窄市场再扩张 | 市场聚焦策略 |
| Paul Graham (Maker's Schedule) | 创造者日程 vs 管理者日程 | 保护创造者的连续工作块 |

**跨阶段项目案例**：GitHub（从周末项目到收购）、Airbnb（从充气床垫到上市）、Superhuman（从邮件到 PMF 标杆）、Stripe（从开发者 API 到支付巨头）

---

## 三、产出成果

### 3.1 研究文件（6 份）

| 文件 | 内容 | 行数 |
|------|------|------|
| `references/wisdom/researcher-t1-discover-sources.md` | Discover 阶段 5 位思想领袖研究 | 227 |
| `references/wisdom/researcher-t2-validate-sources.md` | Validate 阶段 6 位人物 + 10 个验证案例 | ~200+ |
| `docs/research/2026-08-30-plan-stage-wisdom-sources.md` | Plan 阶段 8 位思想领袖研究 | ~200+ |
| `docs/research/2026-08-30-track-stage-wisdom-sources.md` | Track 阶段 6 位人物研究 | ~200+ |
| `docs/research/2026-08-30-cross-stage-wisdom-sources.md` | 跨阶段 4 位人物 + 4 个项目案例 | ~200+ |
| **`docs/wisdom-distillation-plan.md`** | **综合规划蓝图（汇总文件）** | **549** |

### 3.2 行为卡（55 张运行文件；Phase 5–9 来源核验 22/22）

| 阶段 | 卡片 | 文件 | 行数 | 关键问题 |
|------|------|------|------|---------|
| **Discover** | Mom Test | `mentors/discover/mom-test.md` | 63 | 如何区分真实需求和礼貌性赞美 |
| **Discover** | Scratch Your Itch | `mentors/discover/scratch-your-itch.md` | 70 | 如何从个人摩擦发现方向 |
| **Discover** | 工作陈述 | `mentors/discover/jtbd-work-statement.md` | 83 | 如何用"情境+进展+替代方案"定义方向 |
| **Discover** | 反共识检验 | `mentors/discover/secret-test.md` | 80 | 如何用反共识问题检验方向独特性，避免在热门赛道中盲目跟随 |
| **Discover** | 脏活测试 | `mentors/discover/dirty-work-test.md` | 87 | 如何用"脏活指数"判断方向是否因为没人愿意做而有独特机会 |
| **Validate** | Test Card | `mentors/validate/test-card.md` | 158 | 如何把假设写成可测试的预测 |
| **Validate** | Handmade First | `mentors/validate/handmade-first.md` | 141 | 如何不写代码就验证需求 |
| **Validate** | 行为信号 | `mentors/validate/behavior-signal.md` | 167 | 如何区分态度信号和行为信号，只基于行为做决策 |
| **Validate** | 持续验证 | `mentors/validate/continuous-check.md` | 198 | 如何把验证从一次性事件变成持续节奏 |
| **Plan** | 战略内核 | `mentors/plan/strategy-kernel.md` | — | 如何把"列目标"变成"诊断→方针→行动" |
| **Plan** | 时间预算约束 | `mentors/plan/appetite-constraint.md` | — | 如何先定时间预算再定范围 |
| **Plan** | 架构可视化 | `mentors/plan/c4-architecture.md` | — | 如何从系统上下文图逐层展开架构 |
| **Plan** | 上下文边界 | `mentors/plan/bounded-context.md` | 106 | 如何按业务职责划分模块边界，建立术语表 |
| **Plan** | ADR 增强 | `mentors/plan/adr-rfc-enhance.md` | 102 | 如何用"未解决问题"和"采用策略"字段让 ADR 从文档走向落地 |
| **Plan** | Pitch 格式 | `mentors/plan/pitch-format.md` | 100 | 如何用"问题、时间预算、方案、风险陷阱、非目标"五要素统一计划格式 |
| **Plan** | 稳定性设计模式 | `mentors/plan/stability-patterns.md` | 95 | 如何用断路器、舱壁隔离、超时/重试/幂等方式确保系统优雅降级 |
| **Plan** | 测试优先 | `mentors/plan/test-first.md` | 110 | 如何把测试从"验证"变为"安全网"，用分支覆盖保障重构安全 |
| **Plan** | 文档即交付物 | `mentors/plan/document-as-deliverable.md` | 92 | 如何把文档列为里程碑交付物，确保代码和文档同步提交 |
| **Track** | 确定性分级 | `mentors/track/certainty-level.md` | — | 如何用确定性等级替代完成百分比 |
| **Track** | WIP 检测 | `mentors/track/wip-detection.md` | — | 如何检测在制品数量并减少上下文切换 |
| **Track** | 约束诊断 | `mentors/track/constraint-diagnosis.md` | — | 如何找到并消除瓶颈 |
| **Track** | 四种量化指标 | `mentors/track/four-metrics.md` | 260 | 如何用四个指标替代"感觉"判断项目健康度 |
| **Track** | 里程碑状态 | `mentors/track/milestone-state.md` | 265 | 如何用测试证据和集成频率判断真实完成状态 |
| **Track** | 心跳 | `mentors/track/heartbeat.md` | 277 | 如何建立"流动→反馈→学习"的持续追踪脉搏 |
| **Track** | 集成健康度 | `mentors/track/integration-health.md` | 280 | 如何用集成频率、分支老化、合并粒度、CI 通过率评估项目真实流动状态 |
| **Track** | 定期发车 | `mentors/track/regular-departure.md` | 245 | 如何用固定时间表替代范围承诺，让交付节奏可预测 |
| **Track** | 价值流 | `mentors/track/value-stream.md` | 320 | 如何从想法到交付全流程成像，量化等待时间，定位偏差环节 |
| **Cross** | Beachhead | `mentors/cross/beachhead.md` | 72 | 如何先攻窄市场再扩张 |
| **Cross** | Say No By Default | `mentors/cross/say-no-by-default.md` | 71 | 如何用减法做决策 |
| **Cross** | 复杂度预算 | `mentors/cross/complexity-budget.md` | 125 | 如何评估每个改动的复杂度成本，避免失控 |
| **Cross** | 手工服务不扩展 | `mentors/cross/handmade-validation.md` | 112 | 如何在自动化之前先亲手服务用户，用不可扩展的手工服务获取深度反馈 |
| **Cross** | PMF 满意度调查 | `mentors/cross/pmf-survey.md` | 111 | 如何用"如果不能再使用，你会多失望"调查和 40% 阈值判断 PMF |
| **Cross** | 用户行为指标 | `mentors/cross/user-behavior-metric.md` | 133 | 如何区分虚荣指标和可行动指标，用同期群分析指导决策 |
| **Validate** | 定价验证 | `mentors/validate/pricing-test.md` | 105 | 如何在投入开发前测试用户是否愿意付钱，区分"感兴趣"和"愿意付费" |
| **Validate** | 竞品/替代品分析 | `mentors/validate/competitive-analysis.md` | 93 | 如何系统化分析直接竞品、间接竞品和替代方案，理解用户的选择逻辑和切换成本 |
| **Validate** | 实验设计 | `mentors/validate/experiment-design.md` | 117 | 如何用最小投入设计验证实验，根据结果决定继续/转向/放弃 |
| **Validate** | Go/No-Go 决策 | `mentors/validate/gonogo-decision.md` | 107 | 如何基于事前设定的标准而非沉没成本，做出明确的继续、转向或放弃决定 |
| **Validate** | 用户访谈技巧 | `mentors/validate/user-interview.md` | 114 | 如何通过问过去行为、具体场景和追问"为什么"，从访谈中获取真实的用户需求信号 |
| **Cross** | 过早优化 | `mentors/cross/premature-optimization.md` | 99 | 如何在方向未验证时，避免把时间花在性能/扩展性/通用性上，专注于验证核心价值 |
| **Cross** | 功能蔓延 | `mentors/cross/feature-creep.md` | 97 | 如何控制功能增长，避免产品臃肿、维护成本飙升、核心价值模糊 |
| **Cross** | 分析瘫痪 | `mentors/cross/analysis-paralysis.md` | 96 | 如何用决策截止时间、可逆/不可逆决策区分、足够好原则替代最优原则 |
| **Cross** | 独角兽思维 | `mentors/cross/unicorn-mindset.md` | 96 | 如何从第一个用户出发而非市场规模，先聚焦再扩展，接受小众市场 |
| **Plan** | RFC / 设计文档 | `mentors/plan/rfc-design.md` | 93 | 如何用书面化决策替代口头决策，让团队对齐、让历史可查 |
| **Track** | Code Review | `mentors/track/code-review.md` | 98 | 如何用小而专注的 PR、关注设计而非细节、针对代码而非作者，让 CR 成为知识传递工具 |
| **Track** | 回顾 / 复盘 | `mentors/track/retrospective.md` | 93 | 如何用无指责基调、系统性原因分析、可执行的改进措施，把错误转化为改进机会 |
| **Track** | 技术债管理 | `mentors/track/tech-debt.md` | 93 | 如何区分有意债务和质量问题，按债务利息与改动频率安排治理顺序 |
| **Cross** | 异步沟通 | `mentors/cross/async-communication.md` | 93 | 如何用文档替代会议、设定回复期望、区分同步和异步场景，让团队保持深度工作状态 |
| **Cross** | 增长飞轮 | `mentors/cross/growth-flywheel.md` | 109 | 在留存成立后验证可重复增长循环，而非依赖一次性外部流量 |
| **Cross** | 用户留存 | `mentors/cross/user-retention.md` | 123 | 先定位用户价值、激活和退出原因，再决定是否扩大获客 |
| **Cross** | 产品战略 | `mentors/cross/product-strategy.md` | 114 | 用聚焦、洞察和一致行动约束产品选择 |
| **Cross** | 持续发现 | `mentors/cross/continuous-discovery.md` | 127 | 用与决策风险相称的持续接触更新用户证据 |
| **Plan** | API 设计哲学 | `mentors/plan/api-design.md` | 91 | 先定义调用者契约和兼容边界，再选择变更与发布策略 |
| **Track** | 可观测性 | `mentors/track/observability.md` | — | 从运行时问题反推遥测与关联上下文，让未知异常可调查 |
| **Plan** | 数据建模 | `mentors/plan/data-modeling.md` | — | 从业务实体、不变量和演进路径设计数据约束 |
| **Plan** | 安全设计 | `mentors/plan/security-design.md` | — | 在外部边界区分语法验证、领域语义和授权检查 |

### 3.3 索引与集成

| 文件 | 内容 | 行数 |
|------|------|------|
| `references/wisdom/mentors/README.md` | 行为卡索引（55 张）、阶段匹配规则、触发条件匹配规则 | 234 |
| `SKILL.md`（已更新） | 步骤 6 使用具体触发路由；每轮最多 1 张主卡 + 1 张互补辅卡 | — |

---

## 四、完成状态一览

```
阶段划分：        Discover → Validate → Plan → Track → 跨阶段
研究完成：          ✅         ✅        ✅       ✅       ✅
规划文档：          ✅         ✅        ✅       ✅       ✅

卡片实现：
  第一阶段（核心）:  ✅ 6 张 — mom-test, scratch-your-itch, test-card, 
                               handmade-first, beachhead, say-no-by-default
  第二阶段（计划）:  ✅ 已集成 — strategy-kernel, appetite-constraint, c4-architecture
                               (由第三阶段合并交付)
  第三阶段（追踪+深化）: ✅ 14 张 — certainty-level, wip-detection, constraint-diagnosis,
                               jtbd-work-statement, behavior-signal, continuous-check,
                               bounded-context, four-metrics, milestone-state, 
                               heartbeat, complexity-budget
  第四阶段（完善与扩展）: ✅ 13 张 — secret-test, dirty-work-test,
                                adr-rfc-enhance, pitch-format, stability-patterns,
                                test-first, document-as-deliverable,
                                integration-health, regular-departure, value-stream,
                                handmade-validation, pmf-survey, user-behavior-metric
  第五阶段（Phase 5 - Validate 补强）: ✅ 5 张 — pricing-test, competitive-analysis,
                                experiment-design, gonogo-decision, user-interview
  第六阶段（Phase 6 - 反模式系列）: ✅ 4 张 — premature-optimization, feature-creep,
                                analysis-paralysis, unicorn-mindset
  第七阶段（Phase 7 - 团队与协作）: ✅ 5 张 — rfc-design, code-review, retrospective,
                                tech-debt, async-communication
  第八阶段（Phase 8 - 产品维度）: ✅ 4 张 — growth-flywheel, user-retention,
                                product-strategy, continuous-discovery
  第九阶段（Phase 9 - 工程维度）: ✅ 4 张 — api-design, observability, data-modeling,
                                security-design
  总计: 55 张运行文件 — 结构完成；Phase 5-9 来源验收继续进行
```

---

## 五、蒸馏路线图

```
第一阶段（已完成 ✅）：
  discover/mom-test          — 源自 Rob Fitzpatrick
  discover/scratch-your-itch — 源自 Paul Graham + Jason Fried/DHH
  validate/test-card         — 源自 David Bland
  validate/handmade-first   — 源自 Zappos/Dropbox/Buffer 等 10 个验证案例
  cross/beachhead            — 源自 Geoffrey Moore
  cross/say-no-by-default    — 源自 DHH + Jason Fried

第二阶段（已完成 ✅）：
  plan/strategy-kernel       — 源自 Richard Rumelt
  plan/appetite-constraint   — 源自 Ryan Singer (Shape Up)
  plan/c4-architecture       — 源自 Simon Brown
  track/certainty-level      — 源自 Ryan Singer (Hill Chart)
  track/wip-detection        — 源自 David J. Anderson (Kanban)
  track/constraint-diagnosis — 源自 Eliyahu Goldratt

第三阶段（已完成 ✅）：
  discover/jtbd-work-statement  — 源自 Clayton Christensen
  validate/behavior-signal      — 源自 Steve Blank + Eric Ries
  validate/continuous-check     — 源自 Cindy Alvarez
  plan/bounded-context          — 源自 Eric Evans
  track/four-metrics            — 源自 Nicole Forsgren
  track/milestone-state         — 源自 Kent Beck (XP)
  track/heartbeat               — 源自 Gene Kim (DevOps)
  cross/complexity-budget       — 源自 John Ousterhout

第四阶段（已完成 ✅）：
  discover/secret-test            — 源自 Peter Thiel
  discover/dirty-work-test        — 源自 Paul Graham
  plan/adr-rfc-enhance            — 源自 Michael Nygard
  plan/pitch-format               — 源自 Ryan Singer (Shape Up)
  plan/stability-patterns         — 源自 Michael Nygard
  plan/test-first                 — 源自 Kent Beck (XP)
  plan/document-as-deliverable    — 源自 Martin Fowler
  track/integration-health        — 源自 Kent Beck (XP) + Gene Kim
  track/regular-departure         — 源自 Ryan Singer (Shape Up)
  track/value-stream              — 源自 David J. Anderson (Kanban)
  cross/handmade-validation      — 源自 Paul Graham + 经典验证案例
  cross/pmf-survey                — 源自 Superhuman 等 PMF 方法
  cross/user-behavior-metric      — 源自 Nicole Forsgren + Eric Ries
```

---

## 六、关键数字

| 指标 | 数字 |
|------|------|
| 研究覆盖的人物 | **24 位** |
| 研究覆盖的项目/书籍案例 | **16 个** |
| 研究文件总行数 | **~1,400+ 行** |
| 规划文档 | **549 行**（Phase 1-4）+ **427 行**（Phase 5-9） |
| 已创建的行为卡 | **55 张**（33 原卡 + 22 新卡） |
| 已完成的行为卡行数 | **~5,700+ 行** |
| 规划中的总卡片数 | **55 张**（Phase 1-4: 33 + Phase 5-9: 22） |
| 运行文件结构完成率 | **100%**（55/55，通过自动校验） |
| Phase 5-9 一手来源核验 | **22/22** |

---

*本文档随智慧蒸馏工作持续推进而更新。*
