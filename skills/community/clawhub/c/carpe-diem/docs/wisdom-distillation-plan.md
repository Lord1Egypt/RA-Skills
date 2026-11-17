# Carpe Diem 智慧蒸馏综合规划文档

> 本文档汇总了针对 Carpe Diem 四阶段（Discover → Validate → Plan → Track）的智慧来源研究，以及跨阶段通用智慧来源，形成一份完整的蒸馏蓝图。
>
> 研究日期：2026-08-31
> 研究来源：5 份阶段研究报告 + 1 份跨阶段研究报告

---

## 一、蒸馏哲学定位

### 我们想要什么样的蒸馏

1. **行为卡，而非大师口吻**。Carpe Diem 的每个阶段都有明确的"主动讲授→Agent 动作→用户决策→状态写入→下一步路由"结构。智慧应以"行为卡"形式嵌入这个结构，而不是让 Agent 扮演某位大师的口吻。我们不模拟"如果 Paul Graham 现在会怎么说"，而是提供"当你遇到 X 情况时，可以尝试 Y 方法"的规则。

2. **可验证的工程实践，而非抽象理念**。Linux Kernel 的 subsystem maintainer 模型、React 的 RFC 流程、SQLite 的测试哲学——这些是多年运行的工程实践，有明确的机制和结果证据，比个人观点更适合转成 Agent 行为。个人智慧只有在"可转化为可操作规则"时才纳入。

3. **轻量嵌入，而非体系照搬**。每个智慧来源被提炼为 1-3 条可蒸馏规则，以"方法卡"形式嵌入 Carpe Diem 现有流程的特定触发点。不改变主流程结构，不引入完整的理论体系（如不把整个 Shape Up 六周周期搬进来，只提取 appetite 约束和 Hill Chart 确定性分级）。

4. **互补而非冲突**。多位思想领袖的智慧在同一个阶段往往互补：Paul Graham 的"脏活测试"（发现机会来源） + Rob Fitzpatrick 的"Mom Test"（验证证据真实性） + Clayton Christensen 的"JTBD"（描述机会结构）——三者共同构成一条完整的发现路径，而非互斥的方法论。

### 我们不想要的蒸馏

1. **不模拟"大师"风格**。不要求 Agent 模仿 Paul Graham 的写作风格、Peter Thiel 的提问方式或 DHH 的语气。Agent 的角色是"Carpe Diem 的智慧引导者"，不是"某位大师的替身"。

2. **不照搬完整体系**。不把整个 Lean Startup 方法、完整的 DDD 战术模式、Shape Up 的六周周期照搬进来。只提取对 Carpe Diem 四阶段有直接作用的部分。

3. **不引入理论官僚主义**。不因为"JTBD 要求完整的工作陈述"就在 Carpe Diem 中加入 5 个必填字段的表格。Carpe Diem 应在 3-5 轮对话内获得一个足够好的工作陈述，而不是追求学术级别的精确。

4. **不忽略反向提醒**。每个智慧来源都有其适用边界。DHH 的"Scratch Your Own Itch"可能导致太小众，Thiel 的"垄断"思维不适合个人项目，Brooks 的观察基于 1960 年代的大型系统。这些边界必须与规则本身一起蒸馏。

---

## 二、四阶段智慧来源总览表

| 阶段 | 核心人物 | 核心书籍/项目 | 蒸馏主题 |
|------|---------|-------------|---------|
| **Discover**（发现方向） | Paul Graham、Rob Fitzpatrick、Clayton Christensen、Peter Thiel、Jason Fried & DHH | The Mom Test、Zero to One、Rework、YC 方法论、JTBD 理论 | 如何发现真实问题、区分真假需求、形成结构化机会描述 |
| **Validate**（验证假设） | Eric Ries、Steve Blank、Ash Maurya、David Bland、Cindy Alvarez | The Lean Startup、Running Lean、Testing Business Ideas、Customer Development | 如何用最小实验验证假设、区分行为信号与态度信号、可持续验证习惯 |
| **Plan**（制定计划） | Ryan Singer、Eric Evans、Michael Nygard、Frederick Brooks、Martin Fowler、Simon Brown、Richard Rumelt、Alistair Cockburn | Shape Up、DDD、Release It!、Mythical Man-Month、Refactoring、C4 Model | 如何让计划可执行、可验证、可调整——战略连贯性、范围约束、架构描述 |
| **Track**（追踪进度） | Gene Kim、Nicole Forsgren、David J. Anderson、Eliyahu Goldratt、Kent Beck、Ryan Singer | The Phoenix Project、Accelerate、Kanban、The Goal、XP、Shape Up | 如何诚实地评估进度、识别瓶颈和约束、用指标驱动决策 |
| **跨阶段通用** | DHH、John Ousterhout、Geoffrey Moore、Paul Graham | Rework、A Philosophy of Software Design、Crossing the Chasm | 贯穿所有阶段的减法思维、复杂度管理、市场聚焦原则 |

---

## 三、每个阶段详细展开

### 3.1 Discover 阶段——发现值得做的方向

#### 要蒸馏的人

**人物 A：发现真实问题的刺猬视角**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 机会来源 | "Live in the future, then build what's missing"——最好的想法来自你本人作为用户遇到的真问题 | Y Combinator（孵化 Airbnb、Stripe、Dropbox 等 4000+ 公司）、Viaweb（被 Yahoo 收购） | 引导用户优先从"个人摩擦"出发寻找机会，而非从"市场分析"切入 |
| 筛选项 | "Schlep blindness"——人们本能回避脏活，但恰恰是这些"没人愿意做的事"构成最有价值的创业机会 | 《Hackers and Painters》 | 在 7 维度比较中引入"脏活测试"：方向是否足够"脏"（没人愿意做）以至于成为护城河？ |
| 验证姿态 | "Do things that don't scale"——早期阶段应用手动服务用户，不是过早追求自动化 | YC 毕业后服务模式 | 指导用户先"用手服务"一个真实用户，而不是写计划书或做市场调研 |
| 窄起点 | "Start with a narrow, sharp version"——从小而具体用户群体开始，让一部分人热爱而不是所有人轻度喜欢 | Airbnb 早期聚焦设计社区、Stripe 早期聚焦开发者 | 在"个人匹配"和"真实问题"两个维度上优先考虑窄起点 |

**人物 B：不撒谎的客户发现**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 提问方式 | "Talk about their life, not your idea."——不要问"你觉得怎么样"，问"你现在是怎么做的" | 《The Mom Test》 | 在证据收集阶段，引导用户使用"聊用户生活，不说自己想法"的方式进行访谈 |
| 证据过滤 | 区分"承诺信号"（真兴趣：愿意花时间、花钱）vs "前进信号"（礼貌性赞美） | 独立出版后成为创业者社区经典 | 为每个"用户反馈"标注信号类型，仅承诺信号可进入机会地图 |
| 行为锚定 | "Be so specific that they can't lie"——询问具体情境、具体次数、具体金额 | Y Combinator、Stanford、MIT 推荐读物 | 引导用户具体化：上次发生这个问题是什么时候？你当时做了什么？花了多少钱？ |

**人物 C：用户"雇用"产品完成工作**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 问题定义 | "People don't buy products; they hire them to do a job."——用户不是按人口属性购买，而是在特定情境下雇用产品完成工作 | 《创新者的窘境》、《Competing Against Luck》 | 引导用户完成"工作陈述"：在什么情境下，想取得什么进展，但只能用替代方案，它有什么不足 |
| 三维度 | 功能、社交、情感三个维度——忽略社交和情感维度会错过核心机会 | 克莱顿·克里斯滕森研究所 | 从功能、社交、情感三个维度描述机会缺口 |
| 竞品定义 | 竞争不是同类产品，而是用户当前"雇用"的任何方案——包括手工方案、Excel、甚至"不做" | 经典案例"奶昔" | 把间接替代品也纳入竞争分析 |

**人物 D：从 0 到 1 的独特判断**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 独特切口 | "What important truth do very few people agree with you on?"——找到你相信但大多数人反对的真相 | PayPal、Palantir、Founders Fund | 在"独特切口"维度引入"秘密测试"：用户相信但大多数人不同意的真相是什么 |
| 竞争分析 | "Monopoly is the goal, not competition"——好的生意是垄断（在某个细分市场做到不可替代） | 《Zero to One》 | 引导用户思考：什么细分市场我们能做到第一而不是第 N |
| 幂律注意力 | 投资回报遵循幂律分布——少数项目创造绝大部分价值 | Facebook、SpaceX、Airbnb 早期投资 | 在 3 个候选方向中区分"最可能产生极端价值"的候选，集中精力 |

**人物 E：做少、做小、做利润**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 个人匹配 | "Scratch your own itch"——最好的产品来自创始人作为用户的真实需求 | Basecamp、HEY、Writebook | "个人摩擦"维度的理论基础——优先识别自己作为用户遇到的问题 |
| 最小切口 | "Underdo your competition"——不是做得比对手多，而是做得比对手少 | 《Rework》、《Remote》、《It Doesn't Have to Be Crazy at Work》 | 引导用户找到"核心问题的最小切口"——不是"做更好的邮件服务"，而是"解决邮件通知太吵的问题" |
| 可持续性 | "Build a small business, not a unicorn"——小而盈利比亏损但增长快更可持续 | Ruby on Rails（DHH 创建） | 引入"没有外部融资也能活下去"的测试。在"可完成性"维度纳入可持续性检查 |

#### 推荐的蒸馏卡片

| 优先级 | 卡片名称 | 来源 | 触发点 |
|--------|---------|------|-------|
| P0 | `discover/mom-test` | 人物 B | 用户展示证据时，帮助过滤"礼貌性赞美"和"真实需求" |
| P0 | `discover/scratch-your-itch` | 人物 E | 从自身经历出发寻找机会，而非从"市场分析"切入 |
| P1 | `discover/jtbd-work-statement` | 人物 C | 形成机会地图时，确保每个候选有完整的工作陈述 |
| P1 | `discover/secret-test` | 人物 D | 在"独特切口"维度评估时，引入反共识测试 |
| P2 | `discover/dirty-work-test` | 人物 A | 在 7 维度比较中评估"脏活指数" |

---

### 3.2 Validate 阶段——用现实证据验证方向

#### 要蒸馏的人

**人物 A：Build-Measure-Learn 验证引擎**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 验证结构 | 每个验证项目格式化为：可证伪假设 → 最简实验 → 行为/结果指标 → 事前成功/失败阈值 → PASS/PIVOT/REJECT | 《The Lean Startup》、IMVU | 确保每个验证结论都有明确的"事前阈值"支撑 |
| 学习即进展 | 进展单位是"已证实的知识"，不是"写了多少代码" | 被 Google、IBM、GE 等采纳 | 在 Validate 状态中明确记录"新增学习"字段 |
| 可行动指标 | 区分可行动指标（如转化率、留存率）vs 虚荣指标（总注册数、总下载量） | Dropbox、Zappos 等案例 | 引导用户区分"有人说好"（虚荣）和"有人愿意付钱"（可行动） |

**人物 B：Customer Development——走出办公室**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 假设清单 | "There are no facts inside the building, only opinions."——你和你团队的所有认知都是假设 | 《The Four Steps to the Epiphany》、《The Startup Owner's Manual》 | 在验证前增加一步：列出所有假设，标注哪些已在办公室外验证过 |
| 过早扩张警告 | "Premature scaling is the #1 cause of startup death."——过早扩张是创业失败的首要原因 | Hacking for X 系列、Lean LaunchPad、NSF 采纳 | 如果用户未验证核心假设就开始规划大规模发布，发出警告并建议回到 Validate |
| 搜索 vs 执行 | "A startup is a temporary organization designed to search for a repeatable and scalable business model." | 长期影响力 | 帮助用户区分"搜索阶段"（Validate）和"执行阶段"（Plan/Track） |

**人物 C：Running Lean——从精益到系统化**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 风险优先 | "Prioritize risks before solutions"——先识别最大风险，再用最小实验验证 | 《Running Lean》、Lean Canvas、LeanStack | 在验证前增加"风险排序"：从问题风险、客户风险、方案风险、渠道风险、收益风险中选出最危险的一项 |
| Plan A 假设 | "Document your plan A, then systematically test it"——承认你的初始计划几乎可以肯定是错的 | Lean Canvas 被全球创业者广泛使用 | 引导用户明确写出"当前方向假设"——"如果我是对的，那么什么为真？" |
| 三阶段意识 | Problem/Solution Fit → Product/Market Fit → Scale，每个阶段有不同的验证重点 | 第二版 Running Lean | 帮助用户识别当前处于哪个阶段，实验设计不应过早跳到原型测试 |

**人物 D：把假设变成实验**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| Test Card 模板 | 将假设转化为可测试的实验：假设 → 方法 → 指标 → 门槛 → 时间/成本 → 结果 → 结论 | 《Testing Business Ideas》、Strategyzer | 为每个验证项目引入 Test Card 结构化格式 |
| 三维度验证 | 验证的三个维度：用户是否想要（desirability）、商业模式是否可持续（viability）、技术是否可实现（feasibility） | NASA、Microsoft、Intel 等客户 | 确保验证覆盖所有三个维度，而不只是技术可行性 |
| 实验匹配 | 根据不确定性水平推荐验证方法：高不确定性 → 访谈/观察；中等不确定性 → 原型/落地页；低不确定性 → A/B 测试 | 与 Alexander Osterwalder 合著 | 帮助用户选择"适合当前不确定性的验证方法" |

**人物 E：以用户为中心的低成本验证**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 持续验证 | "Customer development is not just for startups"——客户开发不是一次性的活动，而是持续进行的过程 | 《Lean Customer Development》、Microsoft 实践 | 在 Plan 和 Track 阶段也保留"用户验证"检查点 |
| 低成本方法 | "Low-cost, low-fidelity methods"——简单的纸质原型、场景演练就足够获得有效反馈 | Yammer 早期用户研究 | 为 Validate 推荐零成本验证方法：描述产品概念 → 观察用户反应 |
| 右用户选择 | "You don't need a lot of users, just the right ones"——5 个深度访谈比 50 个问卷更有价值 | O'Reilly 出版，覆盖消费产品、企业软件、NGO | 帮助用户找到"已经对这个问题有强烈感受"的人，而非随机样本 |

#### 经典验证案例的蒸馏

| 案例 | 验证假设 | 验证方法 | 对 Carpe Diem 的启发 |
|------|---------|---------|-------------------|
| **Zappos** | 人们是否愿意在网上买鞋 | 手工拍照、去店里买鞋再寄出 | 手工服务少数用户比构建系统更有助于验证核心假设 |
| **Dropbox** | 人们是否想要跨平台文件同步工具 | 3 分钟概念演示视频发到 Hacker News | 验证不一定需要可用产品，概念视频足够验证需求 |
| **Buffer** | 人们是否愿意为社交媒体定时发布工具付费 | 落地页 + 三个定价方案 + 注册按钮（点击后是"还在开发中"） | 验证"付费意向"不需要真正的支付系统 |
| **Groupon** | 人们是否愿意接受每日团购优惠 | WordPress 博客 + Apple Mail 邮件合并 + PDF 优惠券 | 多边参与的商业模式，需要验证"每一方"的意愿 |
| **Airbnb** | 人们愿意付钱住陌生人家里 | 在 SXSW 期间租了 3 个充气床垫 | 轻量验证：有人愿意为"体验"而非"住宿"付费 |

#### 推荐的蒸馏卡片

| 优先级 | 卡片名称 | 来源 | 触发点 |
|--------|---------|------|-------|
| P0 | `validate/test-card` | 人物 C、D | 将每个待验证假设格式化为 Test Card |
| P0 | `validate/risk-priority` | 人物 C | 验证前识别"最不确定且后果最严重的假设" |
| P0 | `validate/handmade-first` | 经典案例 | 优先考虑手工验证方式，而非原型开发或系统构建 |
| P1 | `validate/behavior-signal` | 人物 A、D | 评估验证结果时，区分行为信号和态度信号 |
| P1 | `validate/continuous-check` | 人物 E | 在 Plan 和 Track 阶段保留"最近一次验证时间"检查点 |

---

### 3.3 Plan 阶段——打磨完整的实施计划

#### 要蒸馏的人

**人物 A：Shape Up——固定时间、可变范围**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| Appetite 约束 | 先固定时间预算，再确定范围。不是"需要多少时间"，而是"我们愿意投入多少" | 《Shape Up》（Basecamp 免费出版） | 每个里程碑声明 appetite（固定时间预算），防止范围膨胀 |
| Pitch 提案格式 | 包含问题、appetite、方案、风险陷阱（rabbit holes）、非目标（no-gos）的结构化提案 | Basecamp 官方方法论 | Plan 阶段的"目标与非目标"章节借鉴 pitch 格式 |
| Hill Chart | 横轴=时间，纵轴=确定性。上坡=仍在弄清怎么做，下坡=知道怎么做 | 被产品社区广泛采纳 | Track 阶段最缺失的工具——区分"还在弄清怎么做"和"知道怎么做" |
| 固定时间可变范围 | 固定截止日期，调整范围而非延期 | 防止"计划延期→更多计划→继续延期"的恶性循环 | 超限时默认缩范围，不悄悄延长 |

**人物 B：Domain-Driven Design——以领域为核心**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 限界上下文 | 每个模型有明确的边界，不同上下文间的术语可以不同，但映射关系必须显式 | 《Domain-Driven Design》 | 架构模块按 bounded context 划分，每个上下文有明确的职责、术语和接口契约 |
| 通用语言 | 团队和领域专家使用同一套术语，代码中的命名与业务语言一致 | 软件行业经典 | 产出项目术语表，确保所有 ADR、里程碑描述、测试用例使用同一套术语 |
| 防腐层 | 当项目依赖外部系统或遗留代码时，识别哪些接口需要防腐层 | Eric Evans 在 2003 年提出 | 在 Plan 阶段识别外部依赖接口的防腐层需求 |

**人物 C：Release It!——生产就绪的稳定性设计**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 稳定性模式 | Circuit Breaker、Bulkhead、Timeout、Handshaking 等模式 | 《Release It!》第 2 版 | 每个外部依赖和关键路径指定超时、熔断、隔离策略 |
| 逃生舱设计 | 提供降级路径，让用户在功能不可用时仍能继续 | Pragmatic Bookshelf 经典 | 每个里程碑包含降级路径和逃生舱设计 |
| 生产就绪检查清单 | 系统上线前的检查清单 | 分布式系统设计经典 | Plan 阶段末尾生成生产就绪检查清单 |

**人物 D：The Mythical Man-Month——软件工程的永恒教训**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 布鲁克斯法则 | 给延期的项目加人只会让它更晚 | 《The Mythical Man-Month》 | 里程碑以"单人·周"为粒度，不依赖"加人加速"幻觉 |
| 概念完整性 | 系统的架构应来自少数统一的设计理念，而非委员会设计 | Addison-Wesley 经典 | 检查所有 ADR 是否来自统一的设计理念，避免内部矛盾 |
| 第二系统效应 | 第二个系统是开发者最危险的——倾向于加入所有第一版没加的功能 | 1995 年纪念版 | 对"首版"和"后续版本"设置明确边界，防止第二系统效应 |

**人物 E：Refactoring——持续改进的设计**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 测试是重构前提 | 没有充分测试覆盖的模块，不应该列入"后续重构" | 《Refactoring》第 2 版 | 测试策略覆盖"重构安全网"需求 |
| Monolith First | 先做单体，再按需拆分微服务 | Martin Fowler 的 bliki | 架构决策默认推荐单体架构，除非有明确拆分理由 |
| 代码坏味道 | 22 种常见的代码质量问题信号 | 200+ 种重构手法的目录 | 可用于 Track 阶段的"质量偏差"检测 |

**人物 F：C4 Model——架构描述的层次框架**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 四层模型 | Context → Container → Component → Code 逐层细化 | C4 Model 官方网站 | Plan 阶段的"架构"章节按 C4 层次组织 |
| 架构图文本化 | 用 PlantUML 或 Mermaid 生成架构图 | 《Software Architecture for Developers》 | 架构图可版本化、可 Diff 审查、可自动生成 |
| 上下文图优先 | 先画系统上下文图——明确系统边界、外部依赖、用户角色 | Structurizr | 在进入架构细节之前，先完成系统上下文图 |

**人物 G：Good Strategy/Bad Strategy——战略连贯性**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 战略内核 | 诊断 → 指导方针 → 一致行动 | 《Good Strategy/Bad Strategy》 | 计划首页强制形成：核心挑战 → 总体解法 → 共同落实的里程碑 |
| 近端目标 | 可达成的、具体的、有时间限制的目标 | Crown Business | 里程碑的"可达性"标准 |
| Bad Strategy 检查 | 空话、没有真正面对挑战、把目标当战略、糟糕的战略目标 | Richard Rumelt 在 UCLA 的教学 | 计划的质量检查清单 |

**人物 H：Hexagonal Architecture——端口与适配器**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 端口与适配器 | 核心业务逻辑通过端口接口与外部世界交互，适配器实现具体技术 | Alistair Cockburn 2005 年提出 | 架构设计中核心领域逻辑通过"端口"与外部交互，基础设施为"适配器" |
| 依赖反转 | 核心层不依赖外部技术，外部技术依赖核心层定义的接口 | 六边形架构模式 | 直接提升可测试性——核心逻辑可在不启动外部服务的情况下测试 |

#### 要蒸馏的项目

| 项目 | 核心机制 | 可蒸馏的规则 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| **Basecamp Shape Up 流程** | 六周周期、Betting Table、Pitch 标准化、Cool-Down 期、无 Backlog | 固定时间约束、Pitch 标准化模板、里程碑之间的缓冲期 | Plan 阶段的里程碑约束和交接机制 |
| **Linux Kernel 治理模型** | Subsystem Maintainer、Merge Window、Test Robot、Signed-off-by 链、No Regressions 原则 | 模块化治理、合并窗口、责任追溯、不退化要求 | Plan 阶段模块职责明确 + Track 阶段责任链检查 |
| **React RFC 流程** | RFC 模板、公开讨论期、Lazy Consensus、Champion 制度、渐进式采纳 | ADR 增加"未解决问题"和"采用策略"字段、低风险决策的 Lazy Consensus | Plan 阶段 ADR 模板增强 |
| **SQLite 测试哲学** | 100% Branch Coverage、TH3 测试框架、Fuzz Testing、回归测试、测试代码量超产品代码 100 倍 | 测试优先文化、回归测试强制、模糊测试计划 | Plan 阶段测试策略 + Track 阶段质量指标 |
| **PostgreSQL 社区治理** | Core Team、Commit Fest、Patch Review 文化、Backward Compatibility 承诺、文档即功能 | Commit Fest 集中审查、文档即交付物、向后兼容承诺 | Plan 阶段交付物标准 + Track 阶段文档检查 |

#### 推荐的蒸馏卡片

| 优先级 | 卡片名称 | 来源 | 触发点 |
|--------|---------|------|-------|
| **P0** | `plan/strategy-kernel` | 人物 G | 计划生成时确保"诊断→指导方针→一致行动"三要素 |
| **P0** | `plan/appetite-constraint` | 人物 A | 每个里程碑有投入上限、可削减范围和已知陷阱 |
| **P0** | `plan/c4-architecture` | 人物 F | 架构章节按 Context→Container→Component 组织 |
| **P1** | `plan/bounded-context` | 人物 B | 架构模块按 bounded context 划分 |
| **P1** | `plan/adr-rfc-enhance` | React RFC 流程 | ADR 增加"未解决问题"和"采用策略"字段 |
| **P1** | `plan/pitch-format` | 人物 A | 每个规划章节按 pitch 格式呈现 |
| **P2** | `plan/stability-patterns` | 人物 C | 外部依赖的熔断、超时、隔离策略 |
| **P2** | `plan/test-first` | SQLite + 人物 E | 测试不仅是验收，也是重构安全网 |
| **P2** | `plan/document-as-deliverable` | PostgreSQL | 文档是交付物的一部分 |

---

### 3.4 Track 阶段——记录进度与识别偏差

#### 要蒸馏的人

**人物 A：The Phoenix Project / DevOps——价值流与改善套路**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 三大原则 | 流动（Flow）→ 反馈（Feedback）→ 持续学习（Continuous Learning） | 《The Phoenix Project》、《The DevOps Handbook》、《The Unicorn Project》 | Track 阶段遵循"采集流动证据→收集反馈→沉淀学习"的循环 |
| 价值流图 | 绘制从想法到交付的完整流程，识别等待时间和浪费 | IT Revolution Press 经典 | 当 Track 发现进度偏差时，定位到"哪个环节"出了问题 |
| 改善套路 | 当前状态 → 目标状态 → 瓶颈分析 → 最可能的下一步 | 改善套路在 DevOps 中的应用 | 建议输出使用"当前状态 → 目标状态 → 瓶颈 → 下一步"结构 |

**人物 B：Accelerate——四个关键指标**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 四个关键指标 | 部署频率、变更前置时间、变更失败率、服务恢复时间 | 《Accelerate》、《State of DevOps Report》 | Track 阶段最核心的量化指标框架——合并频率、前置时间、失败率、恢复时间 |
| 可预测性 > 速度 | 不是"更快"，而是"可预测的交付速度" | ELITE / HIGH / MEDIUM / LOW 分级 | Track 关注"计划 vs 实际"的偏差模式，而非绝对速度 |
| 证据等级 | 基于自我报告的数据失真率很高 | Westrum 组织文化模型 | 证据等级优先：自动化证据 > 客观证据（文件存在）> 声称完成 |

**人物 C：Kanban——流动可视化与在制品限制**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 可视化工作流 | 将工作流程显式化，让阻塞和瓶颈可见 | 《Kanban》、《Essential Kanban Condensed》 | Track 报告不仅报告"完成了什么"，也报告"正在做什么"和"卡在什么" |
| WIP 限制 | 限制同时进行的工作数量，防止多任务导致的吞吐量下降 | Lean Kanban University | 检测"在制品过多"——同时推进多个里程碑但一个都没完成 |
| 累积流图 | 显示各阶段工作数量的堆积图，识别瓶颈 | 技术社区广泛采用 | 用"状态分布"（已规划/进行中/已验证完成）替代"完成百分比" |

**人物 D：Theory of Constraints——约束识别与五步聚焦法**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 五步聚焦法 | 识别约束 → 利用约束 → 服从约束 → 提升约束 → 重复 | 《The Goal》、《Critical Chain》 | 偏差诊断从"识别约束"开始——哪个环节最慢？ |
| 鼓-缓冲-绳子 | 用约束环节的节奏驱动整个系统 | 制造业→软件开发的迁移 | 识别项目的"鼓点节奏"——最慢环节决定整体节奏 |
| 关键链项目管理 | 考虑资源约束和不确定性，而不是只考虑任务依赖 | North River Press | 里程碑估计应考虑资源约束，设置统一的"项目缓冲" |

**人物 E：XP / TDD——持续集成与可持续节奏**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 持续集成 | 每天多次集成代码，每次集成通过自动化测试 | 《Extreme Programming Explained》 | Track 检查"集成频率"——如果长时间无集成，项目可能偏离轨道 |
| 可持续节奏 | 每周 40 小时，不加班 | 《Test-Driven Development: By Example》 | 检测"深夜/周末提交"模式作为节奏失控的信号 |
| 信息化工作空间 | 工作空间应展示所有关键信息 | XP 经典实践 | Track 报告本身就是"信息化工作空间"的数字版本 |

**人物 F：Hill Chart（补充）**

| 维度 | 核心智慧 | 成功项目/书籍 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| 确定性分级 | 将进度分为"上坡"（仍不确定怎么做）和"下坡"（知道怎么做） | 《Shape Up》 | 将现有"四类状态"扩展为"确定性等级"：上坡、下坡、已完成 |
| 不把任务完成数当进度 | "花了 3 周完成了 80% 的任务"不等于"80% 完成" | Basecamp 产品开发方法论 | 报告"哪些进入下坡"而非"完成了多少任务" |

#### 要蒸馏的项目

| 项目 | 核心机制 | 可蒸馏的规则 | 对 Carpe Diem 的作用 |
|------|---------|-------------|-------------------|
| **GitLab OKR + 里程碑追踪** | OKR 分层、里程碑权重、燃尽图、发布自动化、价值流分析 | Track 展示"里程碑→目标"对齐链、里程碑完成时生成发布标记、计划 vs 实际对比 | Track 报告结构 + 目标对齐链 |
| **Kubernetes KEP 追踪** | KEP 状态机（Provisional → Implementable → Implemented → Graduated → Stable）、毕业条件、SIG 审查 | 里程碑状态模型：Proposed → In Progress → Implemented → Verified → Accepted → Stale | 里程碑的全生命周期状态追踪 |
| **Mozilla Firefox 发布跟踪** | 发布火车（固定时间不等特性）、Nightly → Aurora → Beta → Release 渠道提升、Go/No-Go 决策、质量门禁 | 固定时间约束、渠道提升模型、里程碑末尾的 Go/No-Go 决策 | 里程碑时间约束 + 质量门禁 |
| **Rust 铁路模型与版本承诺** | Edition 版本、稳定性承诺、Train Model、Feature Gates、Stabilization Period | 版本边界定义、向后兼容检查、特性门控分离"代码完成"和"功能可用" | 版本管理 + 兼容性检查 |
| **Basecamp 复盘 / Heartbeat** | 心跳报告、Cool-Down 期、Betting Table、No Backlog、Pitch 回顾 | 里程碑结束时输出心跳报告、里程碑之间安排缓冲期、不维护待办列表完成率 | Track 复盘的标准化格式 |

#### 推荐的蒸馏卡片

| 优先级 | 卡片名称 | 来源 | 触发点 |
|--------|---------|------|-------|
| **P0** | `track/certainty-level` | 人物 F（Hill Chart） | 报告进度时，对每个里程碑评定"确定性等级" |
| **P0** | `track/wip-detection` | 人物 C（Kanban） | 检测是否在同时推进太多里程碑 |
| **P0** | `track/constraint-diagnosis` | 人物 D（TOC） | 偏差诊断从"识别约束"开始 |
| **P1** | `track/four-metrics` | 人物 B（Accelerate） | 采集合并频率、前置时间、变更失败率、恢复时间 |
| **P1** | `track/milestone-state` | Kubernetes KEP | 里程碑状态机：Proposed → In Progress → Verified → Accepted → Stale |
| **P1** | `track/release-train` | Mozilla Firefox | 固定时间，不等迟到的特性 |
| **P1** | `track/heartbeat` | Basecamp | 里程碑结束时输出"心跳报告" |
| **P2** | `track/integration-health` | 人物 E（XP） | 检测最近一次集成时间 |
| **P2** | `track/value-stream` | 人物 A（Gene Kim） | 定位偏差在哪个环节 |

---

### 3.5 跨阶段通用智慧来源

#### 要蒸馏的人

**人物 A：减法思维——约束催生创造力**

| 核心智慧 | 跨阶段映射 | 对 Carpe Diem 的作用 |
|---------|-----------|-------------------|
| "Scratch Your Own Itch"——从自身需求出发 | Discover：自身需求 → 最真实的问题信号；Validate：自身需求可立即验证 → 不需要去"研发"用户；Plan：知道自己的需求 → 精确的边界；Track：自己是否还在使用 → 最诚实的进度指标 | 全阶段统一原则：优先考虑"创始人自身需求"驱动的项目 |
| "Say No by Default"——默认拒绝 | Plan：非目标（no-gos）的设定原则——"不做什么"比"做什么"更重要 | 每个阶段都应有"不做什么"清单 |
| "Constraints Drive Creativity"——约束催生创造力 | Plan：appetite 约束的理论基础——有限预算催生更好设计 | 里程碑的约束设计原则 |

**来源**：DHH（Rework、It Doesn't Have to Be Crazy at Work）、Basecamp、Ruby on Rails、HEY

**人物 B：复杂度管理——深模块与增量复杂度**

| 核心智慧 | 跨阶段映射 | 对 Carpe Diem 的作用 |
|---------|-----------|-------------------|
| "Complexity Is Incremental"——复杂度是增量积累的 | Discover：识别"复杂度来源"——不是所有问题都值得解决；Validate：验证"复杂度是否可控"；Plan：设计"复杂度最优"的架构；Track：检测"复杂度是否在增长" | 全阶段复杂度意识：每个决策都需评估复杂度成本 |
| "Deep Module"——深模块原则 | Plan：架构评估标准——接口是否足够深？内部是否处理了复杂度？ | 架构决策的评估标准 |
| "Strategic vs. Tactical Programming"——战略编程 vs 战术编程 | 所有阶段：战略思维 vs 战术思维的贯穿 | 帮助用户区分"长期有价值"和"短期能做完" |

**来源**：John Ousterhout（A Philosophy of Software Design）、Tcl、RAMCloud

**人物 C：市场聚焦——滩头阵地与跨越鸿沟**

| 核心智慧 | 跨阶段映射 | 对 Carpe Diem 的作用 |
|---------|-----------|-------------------|
| "Beachhead"——滩头阵地 | Discover：找"我们能赢的细分市场"——不是最大的市场，而是能建立绝对优势的市场 | 机会评估的"独特切口"维度理论基础 |
| "The Chasm"——鸿沟 | Validate：验证早期用户和大众用户之间是否存在鸿沟 | 验证阶段的两类用户区分 |
| "Whole Product"——完整产品 | Plan：首版范围——"最小可行"不等于"不完整"，需要完整性 | 首版范围定义标准 |
| "Bowling Alley"——保龄球道 | Track：里程碑建议应考虑"下一个滩头阵地" | 下一阶段建议的扩展方向考量 |

**来源**：Geoffrey Moore（Crossing the Chasm、Inside the Tornado）

**人物 D：Maker's Schedule——创造者日程与不规模化**

| 核心智慧 | 跨阶段映射 | 对 Carpe Diem 的作用 |
|---------|-----------|-------------------|
| "Do Things That Don't Scale"——做不规模化的事 | Discover + Validate：手工服务比自动化更有价值 | 验证方法的首选原则 |
| "Maker's Schedule"——创造者日程 | Plan：里程碑以"半天"为最小粒度单元 | 里程碑粒度设计原则 |
| "Make Something People Want"——做出人们想要的东西 | 所有阶段：贯穿始终的北极星 | 验证的核心问题只有一个："用户是否真的想要？" |
| "Write Like You Speak"——写作像说话一样自然 | Track：报告风格——简洁、直接、自然 | Track 报告的风格指导 |

**来源**：Paul Graham（YC、Viaweb、Hackers and Painters）

#### 要蒸馏的项目

| 项目 | 完整故事线 | 可复用的模式 | 对 Carpe Diem 的作用 |
|------|----------|-------------|-------------------|
| **GitHub** | 从"周末项目"到"被微软 75 亿美元收购" | 自用驱动 → 社区先行 → 极简首版 → 用户反馈驱动 | 验证了"从自身需求出发 → 最小范围 → 用户即度量"的完整路径 |
| **Airbnb** | 从"充气床垫"到"全球平台上市" | 极小起点 → 手工验证 → 不规模化的事 → 发现真正的约束 | 验证了"从具体问题出发 → 手工验证 → 非技术约束识别"的路径 |
| **Superhuman** | 从"邮件体验差"到"PMF 方法论标杆" | 痛点驱动 → 深度访谈先行 → 极致减法 → PMF 调查 | 验证了"痛点驱动 → 深度访谈 → 极致减法 → PMF 40% 法则"的路径 |
| **Stripe** | 从"支付集成太痛苦"到"650 亿美元估值" | 开发者痛点 → 原型验证 + 聚焦 → 极简 API → 集成时间指标 | 验证了"开发者痛点 → 先验证技术可行 → 5 分钟集成"的路径 |

#### 跨阶段通用原则

从所有来源中提取的贯穿四个阶段的通用原则：

| 原则 | 说明 | 来源 |
|------|------|------|
| **从自身需求出发** | 最可靠的项目始于创始人自己的问题 | 人物 A、GitHub、Airbnb、Stripe、Superhuman |
| **减法思维** | 成功的核心是"删什么"而非"加什么" | 人物 A、Superhuman、Stripe、GitHub |
| **手工验证优先** | 在写代码之前先手工验证"有人需要" | 人物 D、Airbnb、Superhuman |
| **用户行为 > 自述** | 用户做什么比用户说什么更可靠 | Airbnb、Superhuman、Stripe |
| **约束催生创造力** | 有限的资源产生更好的设计 | 人物 A、人物 C（滩头阵地）、人物 B |
| **复杂度是敌人** | 复杂度是增量积累的，需要持续管理 | 人物 B、人物 A（约束）、人物 C（聚焦） |
| **聚焦单一市场** | 先在一个细分市场建立绝对优势 | 人物 C、GitHub（社区先行）、Stripe（开发者） |
| **交付证据 > 承诺** | 产品本身是最好的沟通方式 | 人物 A、GitHub、Stripe |

#### 跨阶段核心问题链

Carpe Diem 的每个阶段应回答的核心问题：

```
Discover：  谁（包括你自己）遇到了什么问题？
               ↓
Validate：  你如何确认这个问题是真的，有人愿意为解决它付费/使用？
               ↓
Plan：      你如何以最小的范围解决这个问题，同时保持完整性？
               ↓
Track：     你如何知道问题是否真的被解决了？用户在做什么？
               ↓
（循环）    下一个最关键的问题是什么？（回到 Discover 或 Validate）
```

#### 推荐的跨阶段蒸馏卡片

| 优先级 | 卡片名称 | 来源 | 适用阶段 |
|--------|---------|------|---------|
| **P0** | `cross/scratch-your-itch` | 人物 A | 全阶段，Discover 优先 |
| **P0** | `cross/beachhead` | 人物 C | Discover + Track |
| **P0** | `cross/say-no-by-default` | 人物 A | 全阶段，Plan 优先 |
| **P1** | `cross/complexity-budget` | 人物 B | Plan + Track |
| **P1** | `cross/handmade-validation` | 人物 D + Airbnb | Validate 优先 |
| **P1** | `cross/pmf-survey` | Superhuman | Track 优先 |
| **P2** | `cross/user-behavior-metric` | Airbnb + Superhuman + Stripe | Track 优先 |

---

## 四、蒸馏优先级建议

### 4.1 按阶段优先级

| 排序 | 阶段 | 核心蒸馏主题 | 推荐卡片数 | 理由 |
|------|------|-------------|-----------|------|
| **1** | **Discover** | 机会发现 + 证据过滤 | 5 张（P0-P2） | 最上游的阶段，决定后续所有阶段的方向质量 |
| **2** | **Validate** | 验证结构 + 手工验证 | 5 张（P0-P2） | 最容易被跳过的阶段，也是最需要行为引导的阶段 |
| **3** | **Plan** | 战略连贯性 + 约束 + 架构描述 | 9 张（P0-P2） | 已有基础框架，补充约束机制和架构描述层次 |
| **4** | **Track** | 确定性分级 + 约束识别 + 指标 | 9 张（P0-P2） | 已有基础框架，最需要的是"不确定性可视化" |

### 4.2 按卡片优先级

**P0（立即蒸馏，核心必需）**：

| 卡片 | 阶段 | 来源 | 投入评估 |
|------|------|------|---------|
| `discover/mom-test` | Discover | Rob Fitzpatrick | 低——可转化为 1-2 条决策规则 |
| `discover/scratch-your-itch` | Discover | DHH / 37signals | 低——Carpe Diem 已有"个人摩擦"维度，增强即可 |
| `validate/test-card` | Validate | David Bland / Ash Maurya | 中——需要设计模板和验证流程 |
| `validate/handmade-first` | Validate | 经典案例（Zappos、Dropbox） | 低——原则性规则，提供案例参考即可 |
| `plan/strategy-kernel` | Plan | Richard Rumelt | 中——需要设计"诊断→指导方针→一致行动"检查流程 |
| `plan/appetite-constraint` | Plan | Ryan Singer | 中——需要修改里程碑结构，加入 appetite |
| `plan/c4-architecture` | Plan | Simon Brown | 中——需要设计架构描述模板 |
| `track/certainty-level` | Track | Ryan Singer（Hill Chart） | 中——需要在现有"四类状态"上叠加确定性等级 |
| `track/wip-detection` | Track | David J. Anderson | 低——计算当前进行中里程碑数量即可 |
| `track/constraint-diagnosis` | Track | Eliyahu Goldratt | 中——需要设计五步聚焦法的轻量版本 |
| `cross/beachhead` | 跨阶段 | Geoffrey Moore | 低——原则性规则，嵌入现有评估维度 |
| `cross/say-no-by-default` | 跨阶段 | DHH | 低——原则性规则，嵌入"不做什么"清单 |

**P1（重要，可逐步实施）**：

| 卡片 | 阶段 | 来源 | 投入评估 |
|------|------|------|---------|
| `discover/jtbd-work-statement` | Discover | Clayton Christensen | 中——需要设计工作陈述模板 |
| `discover/secret-test` | Discover | Peter Thiel | 低——在"独特切口"维度加入一个问题 |
| `validate/behavior-signal` | Validate | Eric Ries / David Bland | 低——规则性引导，区分行为信号和态度信号 |
| `validate/continuous-check` | Validate | Cindy Alvarez | 低——在 Plan 和 Track 阶段添加检查点 |
| `plan/bounded-context` | Plan | Eric Evans | 中——需要设计模块划分引导流程 |
| `plan/adr-rfc-enhance` | Plan | React RFC 流程 | 低——ADR 模板增加字段 |
| `plan/pitch-format` | Plan | Ryan Singer | 中——需要设计章节模板 |
| `track/four-metrics` | Track | Nicole Forsgren | 中——需要采集和计算指标 |
| `track/milestone-state` | Track | Kubernetes KEP | 中——需要设计状态机模型 |
| `track/release-train` | Track | Mozilla Firefox | 低——原则性规则，嵌入时间约束 |
| `track/heartbeat` | Track | Basecamp | 中——需要设计心跳报告模板 |
| `cross/complexity-budget` | 跨阶段 | John Ousterhout | 中——需要设计复杂度评估方法 |
| `cross/handmade-validation` | 跨阶段 | Paul Graham / Airbnb | 低——原则性规则 |
| `cross/pmf-survey` | 跨阶段 | Superhuman | 低——引入一个简洁的满意度问题 |

**P2（有价值，可延后）**：

| 卡片 | 阶段 | 来源 | 投入评估 |
|------|------|------|---------|
| `discover/dirty-work-test` | Discover | Paul Graham | 低——在 7 维度中引入一个子问题 |
| `plan/stability-patterns` | Plan | Michael Nygard | 中——需要设计模式选择引导 |
| `plan/test-first` | Plan | SQLite / Martin Fowler | 中——需要修改测试策略章节 |
| `plan/document-as-deliverable` | Plan | PostgreSQL | 低——检查清单条目 |
| `track/integration-health` | Track | Kent Beck | 低——读取 Git 时间戳 |
| `track/value-stream` | Track | Gene Kim | 中——需要设计偏差定位流程 |
| `cross/user-behavior-metric` | 跨阶段 | 多个来源 | 低——原则性规则 |

### 4.3 实施路线图建议

```
第一阶段（核心基础）：
  ├── discover/mom-test
  ├── discover/scratch-your-itch
  ├── validate/test-card
  ├── validate/handmade-first
  ├── cross/beachhead
  └── cross/say-no-by-default

第二阶段（计划与追踪）：
  ├── plan/strategy-kernel
  ├── plan/appetite-constraint
  ├── plan/c4-architecture
  ├── track/certainty-level
  ├── track/wip-detection
  └── track/constraint-diagnosis

第三阶段（深化与补充）：
  ├── discover/jtbd-work-statement
  ├── validate/behavior-signal
  ├── validate/continuous-check
  ├── plan/bounded-context
  ├── track/four-metrics
  ├── track/milestone-state
  ├── track/heartbeat
  └── cross/complexity-budget

第四阶段（完善与扩展）：
  ├── 剩余 P1 卡片
  ├── 所有 P2 卡片
  └── 持续优化迭代
```

---

## 五、研究结论

1. **五个阶段的研究成果高度互补**。Discover 和 Validate 阶段（研究员 1）提供了"如何发现和验证问题"的智慧，Plan 和 Track 阶段（研究员 2）提供了"如何规划和追踪解决方案"的智慧，跨阶段研究则将两者连接为一条完整的"问题发现 → 验证 → 规划 → 追踪"链条。

2. **最核心的蒸馏原则**：不模拟"大师"风格，以"行为卡"形式嵌入现有流程，在特定触发点提供额外行为指导。每个智慧来源应被提炼为 1-3 条可操作的规则，而非完整的理论体系。

3. **项目案例比人物更可靠**：Linux Kernel 的治理模型、Kubernetes 的 KEP 状态机、SQLite 的测试哲学——这些是多年运行的工程实践，有明确的机制和结果证据，更适合转成 Agent 行为。

4. **跨阶段通用原则贯穿始终**：从自身需求出发、减法思维、手工验证优先、用户行为 > 自述、约束催生创造力、复杂度是敌人、聚焦单一市场、交付证据 > 承诺——这八条原则是所有阶段共同遵循的底层逻辑。

5. **与 Carpe Diem 现有设计完全兼容**。上述所有推荐不改变 Carpe Diem 四阶段的主流程结构，而是在现有流程的特定触发点叠加行为卡，补充现有设计的缺口——如 Discover 的"证据过滤"、Validate 的"验证结构化"、Plan 的"战略连贯性"、Track 的"不确定性可视化"。