# Carpe Diem 实战经验库

> 从 AI 公司博客、工程实践和真实案例中蒸馏的可复用方法论。
> 这些卡片不是理论，是经过验证的实战模式。

## 目录结构

```
wisdom/
├── README.md                    # 本文件
├── mentors/                     # 行为卡（Mentor 卡片）：按阶段触发的可操作行为指导
│   ├── README.md                 # 卡片索引和阶段匹配规则（55 张）
│   ├── discover/
│   │   ├── mom-test.md           # 识别用户反馈中的真实信号
│   │   ├── scratch-your-itch.md  # 从自身摩擦出发找项目
│   │   ├── jtbd-work-statement.md# 用工作陈述定义方向
│   │   ├── secret-test.md        # 反共识检验
│   │   └── dirty-work-test.md    # 脏活测试
│   ├── validate/
│   │   ├── test-card.md          # 假设验证卡
│   │   ├── handmade-first.md     # 手工验证优先
│   │   ├── behavior-signal.md    # 行为信号
│   │   ├── continuous-check.md   # 持续验证
│   │   ├── pricing-test.md       # 定价验证
│   │   ├── competitive-analysis.md# 竞品/替代品分析
│   │   ├── experiment-design.md  # 实验设计
│   │   ├── gonogo-decision.md    # Go/No-Go 决策
│   │   └── user-interview.md     # 用户访谈技巧
│   ├── plan/
│   │   ├── strategy-kernel.md    # 战略内核
│   │   ├── appetite-constraint.md# 时间预算约束
│   │   ├── c4-architecture.md    # 架构可视化
│   │   ├── bounded-context.md    # 上下文边界
│   │   ├── adr-rfc-enhance.md    # ADR 增强
│   │   ├── pitch-format.md       # Pitch 格式
│   │   ├── stability-patterns.md # 稳定性设计模式
│   │   ├── test-first.md         # 测试优先
│   │   ├── document-as-deliverable.md# 文档即交付物
│   │   ├── api-design.md         # API 设计哲学
│   │   ├── data-modeling.md      # 数据建模
│   │   ├── security-design.md    # 安全设计
│   │   └── rfc-design.md         # RFC / 设计文档
│   ├── track/
│   │   ├── certainty-level.md    # 确定性分级
│   │   ├── wip-detection.md      # WIP 检测
│   │   ├── constraint-diagnosis.md# 约束诊断
│   │   ├── four-metrics.md       # 四种量化指标
│   │   ├── milestone-state.md    # 里程碑状态
│   │   ├── heartbeat.md          # 心跳
│   │   ├── integration-health.md # 集成健康度
│   │   ├── regular-departure.md  # 定期发车
│   │   ├── value-stream.md       # 价值流
│   │   ├── observability.md      # 可观测性
│   │   ├── code-review.md        # Code Review
│   │   ├── retrospective.md      # 回顾 / 复盘
│   │   └── tech-debt.md          # 技术债管理
│   └── cross/
│       ├── beachhead.md          # 先攻一个窄市场再扩张
│       ├── say-no-by-default.md  # 默认说"不"
│       ├── complexity-budget.md  # 复杂度预算
│       ├── handmade-validation.md# 手工服务不扩展
│       ├── pmf-survey.md         # PMF 满意度调查
│       ├── user-behavior-metric.md# 用户行为指标
│       ├── premature-optimization.md# 过早优化
│       ├── feature-creep.md      # 功能蔓延
│       ├── analysis-paralysis.md # 分析瘫痪
│       ├── unicorn-mindset.md    # 独角兽思维
│       ├── async-communication.md# 异步沟通
│       ├── growth-flywheel.md    # 增长飞轮
│       ├── user-retention.md     # 用户留存
│       ├── product-strategy.md   # 产品战略
│       └── continuous-discovery.md# 持续发现
├── real-world-patterns/         # 从真实案例中提取的实战模式
│   ├── claude-code-best-practices.md
│   ├── building-effective-agents.md
│   ├── context-engineering.md
│   └── agent-skills.md
└── project-archetypes/          # 项目类型模板
    ├── README.md                 # 模板索引和使用说明
    ├── cli-tool.md               # CLI 工具模板
    ├── web-app.md                # Web 应用模板
    └── devtool.md                # 开发者工具模板
```

## 自动加载机制

SKILL.md 的"每次调用"流程第6步会**自动**加载匹配的智慧卡片，分为两类：

### 1. 实战模式卡片（real-world-patterns/）

加载流程：
1. 先阅读 `references/wisdom/real-world-patterns/README.md` 了解可用卡片
2. 根据当前阶段（Discover / Validate / Plan / Track）和用户方向，选择匹配的卡片
3. 仅加载与当前阶段有对应指引的卡片（卡片中"对 Carpe Diem 用户的启发"包含当前阶段小节）
4. 加载后，在对话中自然引用卡片洞察，而非生硬照搬

### 2. 行为卡（mentors/）

加载流程：
1. 先阅读 `references/wisdom/mentors/README.md` 了解可用卡片及其触发条件
2. 根据当前阶段自动加载对应阶段的行为卡
3. 同时根据用户对话中的触发条件动态加载匹配的跨阶段卡片
4. 加载后，将行为指导融入当前阶段的引导，而非单独展示"卡片内容"

### 匹配规则（实战模式卡片）

| 当前阶段 | 匹配方式 |
|----------|----------|
| Discover | 卡片中"对 Carpe Diem 用户的启发 → Discover 阶段"存在内容 |
| Validate | 卡片中"对 Carpe Diem 用户的启发 → Validate 阶段"存在内容 |
| Plan     | 卡片中"对 Carpe Diem 用户的启发 → Plan 阶段"存在内容 |
| Track    | 卡片中"对 Carpe Diem 用户的启发 → Track 阶段"存在内容（如适用） |

此外，当用户方向（如"构建 Agent 系统"、"优化 Prompt"）与卡片主题高度匹配时，即使当前阶段只有部分指引，也应加载该卡片。

## 卡片编写规范

每张卡片必须包含以下结构才能被自动加载机制正确识别：

```markdown
# 实战模式：<模式名称>

> 来源：<来源>
> 蒸馏日期：<日期>

## 问题本质

<这个模式解决的核心问题>

## 关键洞察

<核心发现和原理>

## 对 Carpe Diem 用户的启发

### Discover 阶段

<可选，该模式对发现阶段的启发>

### Validate 阶段

<可选，该模式对验证阶段的启发>

### Plan 阶段

<可选，该模式对计划阶段的启发>

### Track 阶段

<可选，该模式对跟踪阶段的启发>

## 反向提醒

<不适用场景和注意事项>
```

- 至少一个阶段小节有内容才能被自动加载
- 阶段小节按 `### 阶段名 阶段` 格式命名（如 `### Discover 阶段`）
- 英文卡片使用 `### <Phase> Phase` 格式

## 添加新卡片

每篇卡片包含：
1. 问题本质
2. 关键洞察
3. 对 Carpe Diem 各阶段的启发
4. 反向提醒

添加新卡片后需同步更新 `references/wisdom/real-world-patterns/README.md` 中的卡片列表，并确认 SKILL.md 的自动加载步骤能正确匹配。

---

## 项目类型模板（project-archetypes/）

与实战模式卡片不同，项目类型模板回答的是"**用户想做的项目属于什么类型，这个类型有哪些典型模式和注意事项**"。

### 格式规范

每份项目类型模板包含 7 个独立章节：

```markdown
# 项目类型模板：<类型名称>

> 适用于<类型描述>
> 创建日期：<日期>

## 问题本质

<这类项目解决的核心问题>

## 典型特征

<目录结构、技术栈选择、依赖关系模式>

## 对 Carpe Diem 各阶段的启发

### Discover 阶段

<该类项目在发现阶段的注意事项>

### Validate 阶段

<该类项目在验证阶段的注意事项>

### Plan 阶段

<该类项目在规划阶段的注意事项>

## Prompt 模式

<给 Coding Agent 写 Prompt 的最佳实践>

## 验证策略

<如何验证输出质量和测试策略>

## 常见陷阱

<最容易踩的坑>

## 反向提醒

<不适合的场景和使用注意事项>
```

### 加载时机

项目类型模板在 Plan 阶段进入"架构设计"章节时自动加载匹配的模板。匹配规则：
- 用户确认的**项目方向描述**与模板标题和开头描述匹配
- 多个模板可同时加载作对比参考
- 模板中的"Prompt 模式"和"验证策略"部分可直接用于指导用户与 Coding Agent 协同工作