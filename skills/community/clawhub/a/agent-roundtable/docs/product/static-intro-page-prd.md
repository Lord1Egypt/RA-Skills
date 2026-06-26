# Roundtable 静态介绍页 PRD

版本：v1.0
负责人：饼哥（产品）
目标交付：供设计、开发落地的轻量 PRD
页面类型：静态介绍页 / Landing Page
计划部署：Vercel（本任务不执行真实发布）
交付路径：`docs/product/static-intro-page-prd.md`

---

## 目录

1. 背景与目标
2. 目标用户与核心价值
3. 一句话定位与信息策略
4. 页面信息架构
5. 首屏文案建议
6. 内容模块详细需求
7. 视觉与交互建议
8. 技术与部署约束
9. SEO 与分享需求
10. 验收标准
11. 后续迭代建议

---

## 1. 背景与目标

Roundtable / agent-roundtable 是面向 AI Agent 团队的多智能体圆桌讨论引擎。它不是单个聊天机器人，也不是重型 Agent 编排平台，而是一个轻量“会议协议层”：把多个 Agent / 角色放进同一个 discussion，按轮次组织发言，追踪共识与分歧，并沉淀结构化会议记录和结论。

静态介绍页的核心任务是完成“10 秒理解、30 秒建立兴趣、2 分钟完成行动”。README 已经能承载较完整说明，但 Landing Page 要更像产品入口：首屏给清楚定位，中段给痛点和能力证据，尾部给安装、发布渠道和 CTA。

从产品角度来说，用户要的不是钻头，是墙上的洞。访问者真正要确认的是：Roundtable 能不能让多个 Agent 像开会一样讨论、反驳、收敛，并留下可追溯的决策资产。

### 1.1 页面目标

- 让首次访问者在 10 秒内理解：Roundtable 是多 Agent 圆桌讨论引擎。
- 让开发者在 30 秒内确认：它可以通过 `pip install agent-roundtable` 接入 Python / Agent 系统。
- 让潜在用户在 2 分钟内判断：是否适合产品决策、技术评审、代码 Review、需求澄清、多 Agent 工作流沉淀等场景。
- 为后续 PyPI、Hermes Skill Hub、OpenClaw Skill Hub 发布提供统一的外部介绍入口。

### 1.2 非目标

- 不承载完整 API 文档，详细用法仍跳转 README / GitHub。
- 不做动态后端、登录、在线试用或真实会议运行。
- 不在本任务中执行 Vercel 发布。
- 不承诺所有发布渠道已经上线；未上线渠道需标记 Coming soon。

## 2. 目标用户与核心价值

### 2.1 目标用户

1. AI Agent 框架开发者
   - 已经在构建 Hermes Agent、OpenClaw、内部 Agent 平台或其他多 Agent 系统。
   - 痛点是多个 Agent 能各自完成任务，但缺少统一讨论、反驳、收敛和记录机制。

2. 产品、技术与运营负责人
   - 需要组织多个角色围绕方案做评审，例如产品、设计、后端、运维、安全、增长。
   - 痛点是 AI 输出分散，讨论过程不可追溯，最后只能靠人工整理结论。

3. 开源工具评估者与早期贡献者
   - 关注包是否轻量、是否易接入、是否可扩展到不同 Agent runtime。
   - 痛点是多数多 Agent demo 停留在一次性 prompt 编排，缺少可复用的会议状态模型。

### 2.2 核心价值

- 讨论可组织：用 topic、participants、max_rounds 把多 Agent 对话组织成有边界的会议。
- 过程可追踪：记录每位参与者观点、发言顺序、轮次、状态和收敛度。
- 结论可沉淀：输出 summary、consensus、disagreement、conclusion，形成决策资产。
- 接入门槛低：Python 包形态，核心零外部依赖，`pip install agent-roundtable` 后即可嵌入现有系统。
- 生态入口清晰：同一套定位可延展到 PyPI、Hermes Skill Hub、OpenClaw Skill Hub。

### 2.3 用户问题与页面回答

| 用户问题 | 页面需要给出的回答 |
|---|---|
| 这是什么？ | 面向 AI Agent 团队的多智能体圆桌讨论引擎 |
| 解决什么问题？ | 让多个 Agent 围绕同一议题发言、追踪共识分歧并沉淀会议记录 |
| 怎么开始？ | `pip install agent-roundtable`，导入 `roundtable` 使用核心 API |
| 适合什么场景？ | 产品决策、技术评审、代码 Review、需求澄清、多 Agent 工作流 |
| 和普通聊天 / 多 Agent demo 有什么不同？ | 它强调讨论状态、轮次、收敛、共识 / 分歧与可追溯结论 |

## 3. 一句话定位与信息策略

### 3.1 一句话定位

中文主定位：

> Roundtable 是面向 AI Agent 团队的多智能体圆桌讨论引擎，让多个 Agent 围绕同一问题按轮次发言、追踪共识与分歧，并自动沉淀结构化会议记录和结论。

英文辅助定位：

> Roundtable is a multi-agent discussion engine that helps AI agents speak in turns, track consensus and disagreements, and produce decision-ready meeting notes.

### 3.2 信息策略

页面采用“先给结论，再给证据，再给行动”的结构：

1. 首屏直接说明它是什么、解决什么问题、如何安装。
2. 第二屏解释痛点：多 Agent 有输出，但缺少会议协议层。
3. 中段展示能力：discussion、turns、consensus / disagreement、summary、adapters。
4. 后段展示场景与接入方式：产品决策、技术评审、需求澄清、代码 Review。
5. 末尾强化发布渠道与 CTA：GitHub、PyPI、Hermes Skill Hub、OpenClaw Skill Hub。

### 3.3 差异化表达

- 不是聊天机器人：Roundtable 不负责扮演单个助手，而是管理多个 Agent 的会议过程。
- 不是重型编排平台：Roundtable 不绑定特定 Agent 框架，核心是轻量讨论协议层。
- 不是一次性 prompt demo：Roundtable 有 discussion、participant、round、status、summary、conclusion 等可追踪对象。
- 面向开发者真实接入：Python 包形态，核心零外部依赖，适合嵌入现有系统。

## 4. 页面信息架构

页面建议采用单页 Landing Page，信息流从“理解价值”到“确认适配”再到“立即行动”。整体节奏控制在 6–8 个模块，适合静态部署到 Vercel。

### 4.1 Hero：10 秒理解

目标：首屏在移动端和桌面端都能直接看到产品名、定位、核心价值和主 CTA。

内容要素：

- 产品名：Roundtable / agent-roundtable
- 主标题：多 Agent 圆桌讨论引擎
- 副标题：让多个 Agent 按轮次讨论、追踪共识分歧、生成结构化会议记录
- 关键标签：Python package、Framework agnostic、Consensus tracking、Meeting notes
- 主 CTA：Get Started / 快速开始
- 次 CTA：View on GitHub / 查看 GitHub
- 安装命令卡片：`pip install agent-roundtable`

### 4.2 痛点：为什么需要它

建议用 3 个痛点卡片呈现：

1. 多 Agent 会说话，但不会“开会”
   - 多个 Agent 输出容易变成平行独白，缺少顺序、轮次和会议状态。
2. 讨论过程难复盘
   - 聊天记录里有观点，但缺少结构化共识、分歧和决策依据。
3. 结论难沉淀到工作流
   - 产品、技术、Review 等场景需要可追溯 summary，而不是散落的片段。

### 4.3 能力：Roundtable 提供什么

建议展示 4 个能力模块：

1. Discussion lifecycle
   - 创建讨论、设置 topic、participants、max rounds。
2. Ordered speaking
   - 管理参与者发言顺序和轮次，减少上下文混乱。
3. Consensus & disagreement tracking
   - 展示 convergence score、consensus points、disagreement points。
4. Structured meeting notes
   - 输出 summary、conclusion，可用于 PRD、架构评审、代码 Review 记录。

### 4.4 使用场景：谁会在什么情况下用

建议用场景矩阵或横向卡片：

- 产品决策圆桌：产品、设计、开发、增长讨论 MVP 边界，输出优先级和暂缓项。
- 技术方案评审：架构、后端、运维、安全围绕方案风险和成本收敛，输出选型依据。
- 代码 Review 辩论：质量、安全、性能、可维护性多角度审查，输出阻塞问题和改进建议。
- 需求澄清：多个专家角色对模糊需求追问、反驳，形成共识、风险和未决问题。
- 多 Agent 工作流：作为 coordinator 的讨论协议层，给自动化流程留下可查询会议记录。

### 4.5 安装 / 接入：让开发者能立刻行动

必须包含：

```bash
pip install agent-roundtable
```

补充说明：

- PyPI 包名：`agent-roundtable`
- Python 导入模块：`roundtable`
- 发布前可从 GitHub 源码安装：`pip install -e .`
- 不要引导用户安装 `roundtable` 或 `roundtable-ai`，它们不是本项目。

### 4.6 发布渠道：外部入口统一

展示当前或计划发布渠道：

- GitHub：源码、README、Issue、贡献入口。
- PyPI：Python 包安装入口。
- Hermes Skill Hub：Hermes Agent 用户接入入口。
- OpenClaw Skill Hub：OpenClaw 生态接入入口。

尚未正式上线的渠道统一标记为 Coming soon，避免用户误以为已经可用。

### 4.7 CTA：转化动作

页面底部重复 CTA，避免用户看完后无下一步：

- Install with pip
- View GitHub
- Read Documentation / README
- Publish / Skill Hub links（如果尚未上线，可标记 Coming soon）

## 5. 首屏文案建议

首屏目标是让用户 10 秒内完成三件事：知道这是什么、知道为什么需要、知道下一步怎么做。文案以中文为主，但保留英文短句照顾英文开发者和开源传播。

### 5.1 中文首屏推荐版

主标题：

> 多 Agent 圆桌讨论引擎

副标题：

> Roundtable 让多个 AI Agent 像开会一样围绕同一问题按轮次发言，自动追踪共识与分歧，并生成结构化会议记录和结论。

辅助说明：

> 适合产品决策、技术评审、代码 Review、需求澄清和多 Agent 工作流沉淀。

CTA：

- 主按钮：快速开始
- 次按钮：查看 GitHub

安装命令：

```bash
pip install agent-roundtable
```

### 5.2 面向英文开发者的辅助文案

Headline:

> Structured roundtable discussions for AI Agent teams

Subheadline:

> Roundtable helps multiple agents speak in turns, track consensus and disagreements, and produce decision-ready meeting notes.

CTA:

- Get Started
- View on GitHub

### 5.3 首屏信息优先级

1. 产品名：Roundtable
2. 一句话定位：多 Agent 圆桌讨论引擎
3. 关键结果：讨论、追踪、沉淀
4. 安装命令：`pip install agent-roundtable`
5. CTA：GitHub / Quick Start

首屏不要堆太多实现细节。用户先买“这件事值得试”，再进入代码细节。这个 MVP 可以先跑起来，后续再补 demo 动画和 benchmark。

## 6. 内容模块详细需求

### 6.1 Hero 模块

必须包含：

- Roundtable logo 或文字标识。
- 中文主标题 + 英文辅助说明。
- 安装命令代码块，支持一键复制则加分，但非必须。
- 2 个 CTA：Get Started、GitHub。
- 可信信号：Python 3.10+、Apache-2.0、Zero Dependencies / SQLite。

成功标准：用户不滚动也能知道 Roundtable 是什么。

### 6.2 痛点模块

建议标题：

> 多 Agent 不缺发言，缺的是一张能收敛的圆桌

内容点：

- 多个 Agent 独立输出，缺少统一讨论上下文。
- 观点有冲突，但缺少结构化记录分歧的方法。
- 讨论完成后，还需要人工整理会议纪要和结论。
- Demo 可以跑，生产系统需要可追溯、可嵌入的状态模型。

### 6.3 能力模块

建议用 4 张卡片表达：

1. Create Discussion
   - 输入 topic、participants、max_rounds。
   - 输出 discussion_id 和初始状态。
2. Speak in Turns
   - 按角色记录每轮发言。
   - 支持产品、设计、开发、安全等角色视角。
3. Track Convergence
   - 展示 convergence score。
   - 区分 consensus points 与 disagreement points。
4. Summarize Decisions
   - 生成结构化 summary。
   - 记录 conclusion，形成可追溯决策资产。

### 6.4 使用场景模块

每个场景需要用“谁在讨论 + 讨论什么 + 产出什么”表达，避免只列名词。

| 场景 | 参与角色示例 | 讨论主题 | 页面表达重点 |
|---|---|---|---|
| 产品决策 | 产品、设计、开发、增长 | MVP 范围和优先级 | 从分散意见到可执行决策 |
| 技术评审 | 架构、后端、运维、安全 | 数据库、部署、权限方案 | 记录选型依据和风险 |
| 代码 Review | 质量、安全、性能、可维护性 Agent | 实现方案或 PR | 输出阻塞问题和改进建议 |
| 需求澄清 | 领域专家、产品、工程 | 模糊需求边界 | 形成共识、风险、未决问题 |
| 多 Agent 工作流 | Coordinator + 专家 Agent | 自动化任务推进 | 留下可查询会议记录 |

### 6.5 安装 / 接入模块

必须明确包名和导入名：

```bash
pip install agent-roundtable
```

```python
from roundtable import RoundtableCore

core = RoundtableCore()
result = core.create_discussion(
    topic="选择数据库：PostgreSQL vs MySQL vs TiDB",
    participants=[
        {"profile": "architect", "role": "架构师"},
        {"profile": "ops", "role": "运维工程师"},
        {"profile": "product", "role": "产品经理"},
    ],
    max_rounds=3,
)
```

补充说明：

- PyPI 包名：`agent-roundtable`
- Python 导入名：`roundtable`
- 发布前源码安装：`pip install -e .`
- 不建议出现 `pip install roundtable`，避免与其他包混淆。

### 6.6 发布渠道模块

建议标题：

> 一套圆桌协议，多处 Agent 生态可用

展示渠道：

- PyPI：面向 Python 开发者。
- Hermes Skill Hub：面向 Hermes Agent 用户。
- OpenClaw Skill Hub：面向 OpenClaw 用户。
- GitHub：源码、Issue、贡献、Roadmap。

渠道状态需要用标签区分：Available、Coming soon、Planned。设计和开发不要硬编码“已上线”，以发布实际状态为准。

### 6.7 CTA 收尾模块

建议文案：

> 把一次性的多 Agent 对话，变成可追踪、可复盘、可沉淀的圆桌讨论。

CTA：

- 安装：`pip install agent-roundtable`
- 阅读快速开始
- 在 GitHub 查看源码

## 7. 视觉与交互建议

### 7.1 视觉方向

页面应保持开发者工具气质：清晰、可信、轻量，不做过度营销。可参考 README 现有 logo、深浅色资产和 demo.gif，形成统一品牌感。

建议视觉关键词：

- 圆桌 / 多角色 / 讨论流
- 结构化 / 状态可追踪 / 决策沉淀
- 开源工具 / Python 包 / 轻量接入

### 7.2 版式建议

- 首屏采用左文案右示意图或上下结构，移动端优先保证标题、安装命令、CTA 不被折叠太深。
- 痛点和能力区使用卡片式布局，桌面端 3–4 列，移动端单列。
- 安装命令区使用代码块样式，复制按钮可作为增强项。
- 场景区建议使用矩阵或卡片，避免大段正文。
- 发布渠道区使用状态 Badge，清楚标记 Available / Coming soon。

### 7.3 交互建议

- 所有 CTA 都应是普通链接或锚点，不依赖后端。
- 安装命令复制可以用少量前端脚本实现；如果影响复杂度，可先不做。
- 页面内导航可选：Hero、Use Cases、Install、Channels、GitHub。
- 移动端点击区域不小于 44px，按钮文案明确。

## 8. 技术与部署约束

### 8.1 技术边界

- 静态页面，无后端依赖。
- 可部署到 Vercel，构建过程应简单可复现。
- 若使用框架，优先选择项目已有技术栈；若无必要，纯静态 HTML / CSS / 少量 JS 即可。
- 页面需要能在本地直接预览，降低后续设计和开发验收成本。

### 8.2 内容数据约束

- 包名固定为 `agent-roundtable`。
- Python 导入模块固定为 `roundtable`。
- License 展示为 Apache-2.0。
- Python 版本展示为 3.10+。
- 核心依赖表达为 Zero external dependencies / stdlib + SQLite。
- 未上线发布渠道需标记 Coming soon 或 Planned。

### 8.3 链接建议

后续开发落地时至少预留以下链接位：

- GitHub Repository
- README / Documentation
- PyPI Project Page
- Hermes Skill Hub Page
- OpenClaw Skill Hub Page
- Issues / Contribution Guide

如果链接尚未确定，先使用 disabled 状态或 Coming soon 文案，不要使用空链接误导用户。

## 9. SEO 与分享需求

### 9.1 SEO 基础信息

建议页面基础 meta：

- Title：`Roundtable - Multi-Agent Discussion Engine`
- Description：`Roundtable is a multi-agent discussion engine for structured debates, consensus tracking, and decision-ready meeting notes. Install with pip install agent-roundtable.`
- Keywords：multi-agent, AI agents, roundtable, consensus tracking, meeting notes, Python package, agent-roundtable
- Language：页面主体中文，可通过英文标题、副标题和 meta 兼顾英文开发者。

### 9.2 Open Graph / 社交分享

建议提供：

- og:title：`Roundtable - Multi-Agent Discussion Engine`
- og:description：`让多个 AI Agent 像开圆桌会议一样讨论、追踪共识分歧并沉淀结构化会议记录。`
- og:image：使用现有 `docs/design/assets` 中的品牌图或后续设计产出的分享图。
- og:type：website

### 9.3 页面内容 SEO 要点

- H1 只保留一个：Roundtable 或“多 Agent 圆桌讨论引擎”。
- 首屏正文自然出现 `agent-roundtable`、`multi-agent discussion engine`、`consensus tracking`、`meeting notes`。
- 安装命令使用文本代码块，不要只放在图片里。
- 页面需要有 GitHub / Documentation 链接，提升可信度和搜索理解。

## 10. 验收标准

### 10.1 产品验收

- 访问者在首屏 10 秒内能理解：Roundtable 是多 Agent 圆桌讨论引擎。
- 首屏必须出现产品名、核心定位、安装命令、主 CTA。
- 页面至少覆盖 Hero、痛点、能力、使用场景、安装 / 接入、发布渠道、CTA 七类信息。
- 中文文案为主，英文开发者能通过 headline、subheadline、badge、CTA 理解核心价值。
- 发布渠道状态表达准确，未上线渠道不得暗示已经可用。

### 10.2 设计验收

- 桌面端首屏信息层级清晰，不依赖滚动才能看到定位和 CTA。
- 移动端 375px 宽度下无横向滚动，标题、安装命令和 CTA 可读可点。
- 按钮、链接、代码块、卡片的视觉状态清晰。
- 页面视觉与 Roundtable 现有 logo / README 风格一致。

### 10.3 开发验收

- 页面可通过公开 URL 访问，计划部署在 Vercel。
- 页面为静态资源，无后端服务依赖。
- 首屏主要内容加载快；在常规网络下应做到体感 2 秒内可读。
- 基础 SEO meta、Open Graph meta、页面 title 已配置。
- 所有外链可点击；未确定链接使用 Coming soon / disabled 状态，不出现空 href。
- 安装命令准确：`pip install agent-roundtable`。
- 导入名说明准确：`roundtable`。

### 10.4 兼容性验收

- Chrome、Safari、Firefox 最新稳定版可正常展示。
- iOS Safari 与 Android Chrome 基础浏览无错位。
- 无必须依赖的第三方脚本；即使 JS 失败，核心内容仍可阅读。

## 11. 后续迭代建议

这个 MVP 可以先跑起来。第一版静态页优先保证定位、信息架构和 CTA 转化，不必追求复杂动效。后续可按数据和反馈逐步增强：

1. 增加交互式 demo
   - 展示一个讨论从 init、speak、status 到 summarize 的完整过程。
2. 增加真实案例
   - 产品决策、技术评审、代码 Review 各提供一个短案例。
3. 增加生态入口
   - PyPI、Hermes Skill Hub、OpenClaw Skill Hub 上线后替换 Coming soon 链接。
4. 增加英文完整版本
   - 若 GitHub / PyPI 海外流量增加，可提供英文 Landing Page 或语言切换。
5. 增加转化追踪
   - 在不影响隐私和开源气质的前提下，统计 GitHub 点击、复制安装命令、PyPI 点击。

## 附录：页面模块优先级

| 优先级 | 模块 | 是否首版必须 | 说明 |
|---|---|---|---|
| P0 | Hero + 定位 + CTA | 是 | 决定 10 秒理解 |
| P0 | 安装命令 | 是 | 开发者转化关键 |
| P0 | 痛点与核心能力 | 是 | 解释为什么需要它 |
| P1 | 使用场景 | 是 | 帮助用户自我匹配 |
| P1 | 发布渠道 | 是 | 对齐 PyPI / Skill Hub 路径 |
| P1 | SEO / OG | 是 | 静态页必须具备基础传播能力 |
| P2 | 复制按钮 | 否 | 体验增强，可后续补 |
| P2 | 动态 Demo | 否 | 可作为二期增强 |

我画个饼给你看：第一版页面只要把“多 Agent 不是聊天，而是可收敛的圆桌会议”讲清楚，就已经完成核心转化；后面再逐步加案例、动效和生态入口，产品飞轮就能转起来。
