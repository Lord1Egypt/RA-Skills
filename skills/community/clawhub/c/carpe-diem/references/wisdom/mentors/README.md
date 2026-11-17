# 行为卡（Mentor 卡片）

> 这些卡片是 Carpe Diem 的"行为导师"——在特定阶段触发时，提供可操作的行为指导。
> 每张卡片回答：**当前最应该做什么，不做什么，以及为什么。**

行为卡的结构统一为：
1. **问题本质** — 为什么这个行为很重要
2. **触发条件** — 什么情况下该激活这张卡
3. **行为指导** — 具体该怎么做（可操作步骤）
4. **不适用场景** — 什么时候不该用

## 卡片总览

### Discover 阶段

| 卡片 | 触发条件 | 为您解决的问题 |
|------|---------|--------------|
| [Mom Test — 识别用户反馈中的真实信号](discover/mom-test.md) | 用户正在收集方向反馈，或因为"很多人说好"而决定推进 | 区分"礼貌性赞美"和"真实需求信号"，避免被虚假反馈误导 |
| [从自身摩擦出发找项目](discover/scratch-your-itch.md) | 用户说"不知道做什么方向"，或花大量时间研究市场报告 | 从个人生活摩擦中发现真实方向，而非从热门赛道分析切入 |
| [用工作陈述定义方向](discover/jtbd-work-statement.md) | 用户在形成机会地图，但描述方式是"做一个 XX 产品"而非"解决 XX 问题" | 把"产品描述"转化为"工作陈述"，从情境、进展、替代方案三个维度定义方向 |
| [反共识检验](discover/secret-test.md) | 用户评估方向时关注"市场规模"和"竞争强度"，忽略了"独特性"维度 | 用反共识问题检验方向是否真正独树一帜，避免在热门赛道中盲目跟随 |
| [脏活测试](discover/dirty-work-test.md) | 用户倾向于选择"听起来很酷"的方向而非"看起来无聊"的方向 | 用"脏活指数"判断方向是否因为没人愿意做而有独特机会 |

### Validate 阶段

| 卡片 | 触发条件 | 为您解决的问题 |
|------|---------|--------------|
| [假设验证卡](validate/test-card.md) | 用户在 Validate 阶段列出待验证假设 | 把模糊假设写成可测试的预测，让验证结果不再模棱两可 |
| [手工验证优先](validate/handmade-first.md) | 用户考虑"先做个原型"来验证想法 | 不写一行代码就测试用户是否愿意付钱，用最小成本获得最大学习 |
| [行为信号](validate/behavior-signal.md) | 用户收集到反馈（尤其是正面反馈）并准备以此做决策 | 区分"态度信号"（用户说好）和"行为信号"（用户做了什么），只基于行为信号做决策 |
| [持续验证](validate/continuous-check.md) | Validate 阶段完成并进入 Plan 阶段，或项目推进过程中出现新假设 | 把验证从"一次性事件"变成"贯穿项目始终的节奏"，设置验证保质期和重新验证条件 |
| [定价验证](validate/pricing-test.md) | Validate 阶段讨论定价或收费模式时 | 在投入开发前测试用户是否愿意付钱，区分"感兴趣"和"愿意付费" |
| [竞品/替代品分析](validate/competitive-analysis.md) | Validate 阶段评估竞争格局或判断方向独特性时 | 系统化分析直接竞品、间接竞品和替代方案，理解用户的选择逻辑和切换成本 |
| [实验设计](validate/experiment-design.md) | 测试卡已写清，正在选择怎样取得足够强的证据时 | 用最低成本但仍有效的证据机制检验预测，不把“做个产品”默认当实验 |
| [Go/No-Go 决策](validate/gonogo-decision.md) | 验证结束后需要判断方向是否值得继续推进时 | 基于事前设定的标准而非沉没成本，做出明确的继续、转向或放弃决定 |
| [用户访谈技巧](validate/user-interview.md) | Validate 阶段发现访谈结果模糊、缺乏有用信息时 | 通过问过去行为、具体场景和追问"为什么"，从访谈中获取真实的用户需求信号 |

### Plan 阶段

| 卡片 | 触发条件 | 为您解决的问题 |
|------|---------|--------------|
| [战略内核](plan/strategy-kernel.md) | Plan 阶段用户提供的是"功能清单"而非"核心挑战" | 把"列目标"变成"诊断核心挑战→制定指导方针→规划一致行动" |
| [时间预算约束](plan/appetite-constraint.md) | Plan 阶段规划里程碑范围时，用户先列功能清单再估算时间 | 先定时间预算再定范围，让范围去适应时间而非让时间去适应范围 |
| [架构可视化](plan/c4-architecture.md) | Plan 阶段进入架构章节时，用户直接讨论技术选型而非系统全貌 | 从系统上下文图开始逐层展开，确保可版本化、可 Diff 审查 |
| [上下文边界](plan/bounded-context.md) | Plan 阶段进入"架构、组件、数据流"章节，按技术层而非业务职责划分模块 | 按业务职责划分模块边界，建立术语表，明确接口契约 |
| [ADR 增强](plan/adr-rfc-enhance.md) | 架构决定已经接受，需要记录理由和落地路径时 | 在 ADR 中增加未决问题和采用策略，让已作出的决定进入实施 |
| [Pitch 格式](plan/pitch-format.md) | Plan 阶段组织章节结构时，各章节格式不统一 | 用"问题、时间预算、方案、风险陷阱、非目标"五要素统一计划章节格式 |
| [稳定性设计模式](plan/stability-patterns.md) | Plan 阶段架构涉及外部依赖或多服务时，未讨论故障场景 | 用断路器、舱壁隔离、超时/重试/幂等方式保护系统，确保故障时优雅降级 |
| [测试优先](plan/test-first.md) | Plan 阶段进入"测试策略"章节，或用户说"测试后面再补" | 把测试从"验证"变为"安全网"，用分支覆盖和回归测试保障重构安全 |
| [文档即交付物](plan/document-as-deliverable.md) | Plan 阶段定义交付物时，只列出了"代码功能"未包含"文档" | 把文档列为里程碑交付物，确保代码和文档同步提交、同步验收 |
| [API 设计哲学](plan/api-design.md) | Plan 阶段开始设计系统 API 接口 | 先定义调用者契约和兼容边界，再选择适合的变更与发布策略 |
| [数据建模](plan/data-modeling.md) | Plan 阶段进入"架构"章节，开始设计数据库 schema 或数据模型 | 从业务概念出发设计数据模型，用约束保障数据完整性，避免过度设计和命名不一致 |
| [安全设计](plan/security-design.md) | 系统新增外部输入、用户数据或访问边界 | 在实现前定义输入验证、领域约束、授权和失败处理 |
| [RFC / 设计文档](plan/rfc-design.md) | 重大方案尚未定案，需要多人评审和形成共识 | 在决定形成前用书面提案收集反馈；决定接受后转入 ADR |

### Track 阶段

| 卡片 | 触发条件 | 为您解决的问题 |
|------|---------|--------------|
| [确定性分级](track/certainty-level.md) | Track 阶段开始报告里程碑进度时 | 区分"上坡（还不知怎么做）"和"下坡（知道怎么做）"，用确定性等级替代完成百分比 |
| [WIP 检测](track/wip-detection.md) | Track 阶段发现多个里程碑同时处于"进行中"状态 | 统计在制品数量，超过阈值时建议集中推进，减少上下文切换 |
| [约束诊断](track/constraint-diagnosis.md) | Track 阶段发现进度偏差，里程碑卡在同一个环节 | 找到并消除瓶颈，用约束决定整个项目的节奏 |
| [四种量化指标](track/four-metrics.md) | Track 阶段需要判断项目整体健康度时 | 用合并频率、前置时间、变更失败率、恢复时间四个信号替代"感觉"，辅助判断项目状态 |
| [里程碑状态](track/milestone-state.md) | Track 阶段检查里程碑是否真正完成时 | 用测试证据、集成频率和 CI 状态替代"声称完成"，判断里程碑的真实完成状态 |
| [心跳](track/heartbeat.md) | Track 阶段开始执行时，建立持续反馈循环 | 用"流动→反馈→学习"的三段式循环替代单向汇报，让每次 Track 都是上一次心跳的延续 |
| [集成健康度](track/integration-health.md) | Track 阶段采集流动证据时，发现代码在分支上累积或合并冲突增多 | 用集成频率、分支老化、合并粒度、CI 首次通过率四个维度评估项目真实流动状态 |
| [定期发车](track/regular-departure.md) | 特性超出预期时间或交付时间被多次推迟时 | 用固定时间表替代范围承诺，让交付节奏可预测 |
| [价值流](track/value-stream.md) | Track 阶段发现进度偏差，需要定位"问题出在哪个环节" | 从想法到交付的全流程成像，量化等待时间，定位偏差在哪一环 |
| [可观测性](track/observability.md) | 系统已上线，但团队无法用系统输出解释未知故障 | 从待回答的运行时问题反推遥测和关联上下文，让异常可调查 |
| [Code Review](track/code-review.md) | 团队开始协作，或用户说"我们做 CR 但没什么效果" | 用小而专注的 PR、关注设计而非细节、针对代码而非作者，让 CR 成为知识传递工具而非形式主义 |
| [回顾 / 复盘](track/retrospective.md) | 里程碑完成、项目延期、或用户说"同样的问题又出现了" | 用无指责基调、系统性原因分析、可执行的改进措施，把错误转化为改进机会 |
| [技术债管理](track/tech-debt.md) | 用户说"代码越来越难改了"或"先快速实现，后面再重构" | 区分有意债务和质量问题，按债务利息安排可见的还债容量 |

### 反模式系列

| 卡片 | 触发条件 | 适用阶段 | 为您解决的问题 |
|------|---------|---------|--------------|
| [过早优化——在不确定方向时过度设计](cross/premature-optimization.md) | 用户说"我先把这个架构搭好"或"以后扩展会很难"，或把"代码质量"和"过度设计"混为一谈 | 全阶段 | 在方向未验证时，避免把时间花在性能、扩展性、通用性上，专注于验证核心价值 |
| [功能蔓延——如何恢复已失控的范围](cross/feature-creep.md) | 已承诺的范围持续增长，时间预算不变且核心价值开始模糊 | 全阶段 | 对现有范围做事后治理，恢复边界并设置停止条件 |
| [分析瘫痪——过度收集信息导致迟迟不做决定](cross/analysis-paralysis.md) | 用户说"我再调研一下"或"我想收集更多数据"频率超过执行频率 | 全阶段 | 用决策截止时间、可逆/不可逆决策区分、足够好原则替代最优原则 |
| [独角兽思维——每个项目都想做成百亿公司](cross/unicorn-mindset.md) | 用户说"这个市场太小了"或"这个方向做不大"，或用市场规模否定方向 | 全阶段 | 从第一个用户出发而非市场规模，先聚焦再扩展，接受小众市场 |

### 跨阶段通用

| 卡片 | 触发条件 | 适用阶段 | 为您解决的问题 |
|------|---------|---------|--------------|
| [先攻一个窄市场再扩张](cross/beachhead.md) | Discover 评估方向/ Track 完成里程碑后考虑下一步 | Discover, Track | 找到"能赢的细分市场"而非"最大的市场"，先聚焦再扩张 |
| [默认说"不"](cross/say-no-by-default.md) | 任何阶段面临"要不要加功能/方向/范围"的决策 | 全阶段 | 用减法思维做决策——知道拒绝什么比知道加什么更重要 |
| [复杂度预算](cross/complexity-budget.md) | 任何阶段面临"要不要加这个功能/模块/依赖"的决策，或审查架构变更时 | 全阶段 | 评估每个改动的复杂度成本，避免复杂度失控，用"深模块"替代"浅模块" |
| [手工服务不扩展](cross/handmade-validation.md) | Cross 阶段考虑扩大用户规模时，或用户想先做自动化而非手工服务 | Validate, Cross | 在自动化之前先亲手服务用户，用不可扩展的手工服务获取深度反馈和信任 |
| [PMF 满意度调查](cross/pmf-survey.md) | Cross 阶段需要判断产品是否达到产品-市场匹配时 | Cross, Track | 用"如果不能再使用，你会多失望"简洁调查和 40% 阈值判断是否达到 PMF |
| [用户行为指标](cross/user-behavior-metric.md) | Cross 阶段评估产品健康度时，用户在看"总用户数"等虚荣指标 | Cross, Track | 区分虚荣指标和可行动指标，用同期群分析和关键行为时刻指导决策 |
| [增长飞轮](cross/growth-flywheel.md) | 已有留存信号，但增长仍依赖一次性外部获客 | Cross, Track | 验证能重复产生价值或新参与者的增长循环，不用新增流量掩盖留存问题 |
| [用户留存](cross/user-retention.md) | 已有用户进入产品，但未获得持续价值并很快离开 | Cross, Track | 先定位价值、激活和退出原因，再决定是否扩大获客 |
| [产品战略](cross/product-strategy.md) | 多个方向争夺资源，但没有聚焦的目标客群和问题 | Cross, Plan | 用聚焦、洞察和一致行动约束功能选择，并持续管理战略 |
| [持续发现](cross/continuous-discovery.md) | 近期产品决定依赖未经更新的用户假设 | Cross, Validate, Track | 用与决策风险相称的持续接触更新证据，而非套固定访谈频率 |
| [异步沟通](cross/async-communication.md) | 用户说"会议太多了"或"总是被打断" | 全阶段 | 用文档替代会议、设定回复期望、区分同步和异步场景，让团队保持深度工作状态 |

## 按需路由规则

SKILL.md 的"每次调用"流程第6步会先用当前阶段缩小候选集，再根据具体触发信号选择卡片。阶段不是批量加载指令。

### 阶段匹配规则

| 当前阶段 | 候选目录 | 匹配逻辑 |
|----------|--------------|---------|
| **Discover** | `discover/`，必要时 `cross/` | 只有出现具体触发信号才选 1 张主卡 |
| **Validate** | `validate/`，必要时 `cross/` | `test-card` 定义测试；`experiment-design` 选实验；`gonogo-decision` 审计结果，不同时抢占 |
| **Plan** | `plan/`，必要时 `cross/` | 以当前正在确认的计划章节和风险为触发，不预读其他章节卡 |
| **Track** | `track/`，必要时 `cross/` | 只基于已授权的只读证据选卡，卡片不得扩大读取或写入权限 |

### 近邻卡判定

| 状态 | 主卡 | 不抢占的卡 |
|---|---|---|
| 测试尚未定义 | `validate/test-card.md` | `experiment-design`、`gonogo-decision` |
| 测试卡已就绪，实验未执行 | `validate/experiment-design.md` | `test-card`、`gonogo-decision` |
| 实验已经完成，需要决定 | `validate/gonogo-decision.md` | `test-card`、`experiment-design` |
| 单个新请求尚未承诺 | `cross/say-no-by-default.md` | `feature-creep` |
| 已承诺范围持续膨胀 | `cross/feature-creep.md` | `say-no-by-default` |
| 重大方案尚未决定 | `plan/rfc-design.md` | `adr-rfc-enhance` |
| 决定已经接受，需要记录采用 | `plan/adr-rfc-enhance.md` | `rfc-design` |
| 用户持续离开 | `cross/user-retention.md` | `growth-flywheel` |
| 留存成立但增长不可重复 | `cross/growth-flywheel.md` | `user-retention` |

可执行回归判例见 [`routing-acceptance-cases.json`](routing-acceptance-cases.json)。

### 触发条件匹配

当用户状态或对话触发某张卡片的**触发条件**时，把它加入候选。若多张同时命中，选择最能改变当前下一步的一张；只有职责互补时再加一张，且总数不超过两张：

- 用户说"很多人在做这个方向，但我们可以做得更好" → 加载 `secret-test`
- 用户说"这个方向太 boring 了，不值得做" → 加载 `dirty-work-test`
- 用户说"很多人说这个方向好" → 加载 `mom-test`
- 用户说"不知道做什么" → 加载 `scratch-your-itch`
- 用户在形成机会地图时描述方式是"做一个 XX 产品"而非"解决 XX 问题" → 加载 `jtbd-work-statement`
- 用户说"我的想法确实很好，很多人说不错" → 加载 `behavior-signal`
- 用户说"Validate 已经通过了，可以安心推进了" → 加载 `continuous-check`
- 单个新功能请求尚未承诺，正在判断是否纳入 → 加载 `say-no-by-default`
- 用户说"这个市场太小了" → 加载 `beachhead`
- 用户说"先做出来再说，后面再优化" → 加载 `complexity-budget`
- 用户在架构审查时发现"模块接口太多，但内部处理很浅" → 加载 `complexity-budget`
- 用户在 Validate 阶段列出假设 → 加载 `test-card`
- 用户说"我想先做个原型" → 加载 `handmade-first`
- 用户在 Validate 阶段问"这个能收费吗？"或"定价多少合适？" → 加载 `pricing-test`
- 用户说"先免费，后面再收费"或"等产品做好了再考虑定价" → 加载 `pricing-test`
- 用户说"访谈中用户都说愿意付钱"但未做过实际付费测试 → 加载 `pricing-test`
- 用户设计验证方案时只验证了"是否需要"而未验证"是否愿意付费" → 加载 `pricing-test`
- 用户说"市场上没有竞品"或"这个方向没人做" → 加载 `competitive-analysis`
- 用户说"我们是唯一做这个的"但未考虑替代方案 → 加载 `competitive-analysis`
- 用户只分析了直接竞品，未考虑间接竞品和替代方案 → 加载 `competitive-analysis`
- 用户说"竞品做得不好，我们做得更好"但未分析切换成本 → 加载 `competitive-analysis`
- 测试卡已经写清，正在选择怎样获取足够强的证据 → 加载 `experiment-design`
- 用户说"这个功能很简单，做出来让用户试试" → 加载 `experiment-design`
- 用户在 Validate 阶段直接开始设计产品功能而非验证实验 → 加载 `experiment-design`
- 用户说"先做出来，看用户反馈再说" → 加载 `experiment-design`
- 用户说"验证结果还行"或"结果还可以"但说不出具体标准 → 加载 `gonogo-decision`
- 用户说"再验证一下"但迟迟不做决定 → 加载 `gonogo-decision`
- 实验已经完成，但团队无法据结果决定继续、转向或停止 → 加载 `gonogo-decision`
- 用户说"已经花了这么多时间，不继续就浪费了" → 加载 `gonogo-decision`
- 用户说"我做了访谈，但没得到有用的信息" → 加载 `user-interview`
- 用户说"访谈中用户都说好" → 加载 `user-interview`
- 用户只准备了"产品介绍"和"你觉得怎么样"类问题去做访谈 → 加载 `user-interview`
- 用户说"用户说他们一定会用" → 加载 `user-interview`
- 用户提供的是"功能清单"而非"核心挑战" → 加载 `strategy-kernel`
- 用户先列功能清单再问"需要多少时间" → 加载 `appetite-constraint`
- 用户直接讨论技术选型而非系统全貌 → 加载 `c4-architecture`
- 用户按技术层划分模块，而非按业务职责 → 加载 `bounded-context`
- 用户编写或评审 ADR 时，发现"决策看起来没问题，但不知道具体怎么落地" → 加载 `adr-rfc-enhance`
- 用户说"我们先列一下计划需要包含哪些章节" → 加载 `pitch-format`
- 用户说"这个外部服务应该很稳定，不太可能出问题" → 加载 `stability-patterns`
- 用户说"测试后面再补" 或 "这部分代码我不敢动" → 加载 `test-first`
- 用户说"这个功能很简单，不需要文档" 或 "文档下次补上" → 加载 `document-as-deliverable`
- 用户开始设计 API 接口，或说"先实现功能，API 后面再统一" → 加载 `api-design`
- 用户开始设计数据库 schema 或数据模型 → 加载 `data-modeling`
- 用户讨论中直接讨论"字段类型"和"存储方式"而非"业务实体之间的关系" → 加载 `data-modeling`
- 用户说"安全后面再考虑" 或 "我们项目小，没人会攻击" → 加载 `security-design`
- 架构讨论中完全没有涉及"谁可以访问什么"、"数据如何保护"等安全话题 → 加载 `security-design`
- 用户报告"感觉一直在做，但好像没完成什么" → 加载 `wip-detection`
- 用户说"不知道哪个环节拖了后腿" → 加载 `constraint-diagnosis`
- 用户说"感觉项目进展不错" 或 "项目好像变慢了" → 加载 `four-metrics`
- 用户说"这个功能做完了" 或 "代码写完了，但还没来得及测试" → 加载 `milestone-state`
- 用户说"上次 Track 说的问题还在吗" 或 "感觉同样的偏差出现了好几次" → 加载 `heartbeat`
- 用户说"代码写完了，但还没合并" 或 "合并的时候出了很多冲突" → 加载 `integration-health`
- 用户说"这个特性快做完了，再等两天就好" 或 "再加一个小功能" → 加载 `regular-departure`
- 用户说"代码写完了，但还在等测试/审查/部署" 或 "感觉一直在做，但好像没完成什么" → 加载 `value-stream`
- 用户说"系统出问题了才知道" 或 "不知道系统运行得怎么样" → 加载 `observability`
- 系统部署后，团队只在"收到用户投诉"时才去排查问题 → 加载 `observability`
- 用户说"我们要把这个流程自动化" 或 "手工服务太慢，效率太低" → 加载 `handmade-validation`
- 用户说"产品应该达到 PMF 了" 或 "不确定是否准备好扩大规模" → 加载 `pmf-survey`
- 用户在看"总用户数"、"总浏览量"、"总下载量"来判断产品健康度 → 加载 `user-behavior-metric`
- 用户说"产品做好了但没人用"或"怎么获得第一批用户" → 加载 `growth-flywheel`
- 用户说"我要投广告来获取用户" → 加载 `growth-flywheel`
- 已有稳定留存信号，但增长只依赖一次性外部投放 → 加载 `growth-flywheel`
- 用户说"用户来了但留不住"或"流失率很高" → 加载 `user-retention`
- 用户说"注册量很大，但活跃用户很少" → 加载 `user-retention`
- 用户说"用户试用一下就走了" → 加载 `user-retention`
- 用户只关注"总用户数"和"新增用户数"，未关注"回头客"和"活跃用户" → 加载 `user-retention`
- 用户说"我们有很多功能要做"或"不知道优先做什么" → 加载 `product-strategy`
- 用户说"用户想要的功能太多了，不知道该做哪个" → 加载 `product-strategy`
- 用户说"我们要做平台"或"我们要做生态" → 加载 `product-strategy`
- 用户说"先做这个功能，看看效果"但功能之间没有逻辑关联 → 加载 `product-strategy`
- 用户说"我们已经验证过了"或"产品上线了不需要再验证了" → 加载 `continuous-discovery`
- 用户说"我们只需要按计划执行就行" → 加载 `continuous-discovery`
- 用户说"用户反馈已经够多了，不需要再做什么发现了" → 加载 `continuous-discovery`
- 团队的节奏是"开发→发布→开发→发布"，没有"发现→验证→学习"的循环 → 加载 `continuous-discovery`
- 用户说"我先把这个架构搭好"或"以后扩展会很难" → 加载 `premature-optimization`
- 用户在 Validate 阶段选择复杂技术栈"为未来做准备" → 加载 `premature-optimization`
- 用户把"好代码"和"加了抽象层/接口的代码"混为一谈 → 加载 `premature-optimization`
- 用户说"先把性能优化好"但此时还没有任何用户 → 加载 `premature-optimization`
- 已承诺的功能列表不断增长，但时间预算和核心目标没有调整 → 加载 `feature-creep`
- 用户因为"竞品有"而添加功能，未评估是否符合产品定位 → 加载 `feature-creep`
- 用户说"先加上去，后面可以关掉" → 加载 `feature-creep`
- 用户说"我再调研一下"或"我想收集更多数据"频率超过执行频率 → 加载 `analysis-paralysis`
- 用户花在分析选择上的时间远多于执行的时间 → 加载 `analysis-paralysis`
- 用户试图找到"最佳选项"而非"足够好的选项" → 加载 `analysis-paralysis`
- 用户已经做了决定，但仍在收集信息来"验证"这个决定 → 加载 `analysis-paralysis`
- 用户说"这个市场太小了"或"这个方向做不大" → 加载 `unicorn-mindset`
- 用户优先考虑"市场规模"而非"谁需要这个" → 加载 `unicorn-mindset`
- 用户同时推进多个方向，每个方向都"看起来很大" → 加载 `unicorn-mindset`
- 用户说"这个方向太小了，不值得做"但尚未验证过任何方向 → 加载 `unicorn-mindset`
- 项目进入多人协作阶段，决策依赖口头讨论 → 加载 `rfc-design`
- 用户说"我们讨论过但大家理解不一样" → 加载 `rfc-design`
- 团队反复讨论同一个决策，没有可引用的决策记录 → 加载 `rfc-design`
- 用户说"这个决策是谁做的？为什么这么做？"但找不到答案 → 加载 `rfc-design`
- 团队开始协作，但 CR 流程不明确 → 加载 `code-review`
- 用户说"我们做 CR 但没什么效果"或"CR 就是走个过场" → 加载 `code-review`
- CR 讨论变成"个人喜好"之争（命名、格式偏好） → 加载 `code-review`
- 审查者说"这个代码我看不懂"或"太复杂了" → 加载 `code-review`
- 里程碑完成或项目延期，没有安排复盘 → 加载 `retrospective`
- 用户说"同样的问题又出现了" → 加载 `retrospective`
- 项目出问题后，团队第一反应是"谁的责任" → 加载 `retrospective`
- 用户说"复盘就是走个过场"或"复盘的结论没人执行" → 加载 `retrospective`
- 用户说"代码越来越难改了"或"改一个功能要改很多地方" → 加载 `tech-debt`
- 用户说"先快速实现，后面再重构" → 加载 `tech-debt`
- 用户说"新功能开发速度越来越慢了" → 加载 `tech-debt`
- 用户说"这部分代码我不敢动"或"动一下就可能出问题" → 加载 `tech-debt`
- 用户说"会议太多了"或"一天都在开会，没时间做事" → 加载 `async-communication`
- 用户说"总是被打断"或"刚进入状态就被消息打断了" → 加载 `async-communication`
- 团队在即时消息中讨论复杂问题，讨论结果难以追溯 → 加载 `async-communication`
- 用户说"我不知道别人在做什么"或"信息不透明" → 加载 `async-communication`

### 加载方式

1. 先阅读本文件了解候选卡片，不打开整阶段文件
2. 从对话或状态中摘出具体触发信号
3. 比较候选卡职责，选 1 张主卡；必要时加 1 张互补辅卡
4. 只加载最终选中的卡片，自然融入阶段引导，不复述卡名或来源
5. 没有强信号、卡片冲突或卡片会越过安全边界时，不加载
