# 调研阶段指南

当前版本阶段声明：
本阶段只产出需求文档和调研结论，不直接落地脚本、模板或 Skill 包。

## 目标

调研阶段的目标是把用户的模糊想法收束成一份可以进入设计阶段的稳定需求结果。
这一阶段关注的是问题定义，不急着写最终产物。

## 进入条件

满足任一条件即可进入本阶段：

- 用户想创建新 Skill
- 用户想升级已有 Skill
- 用户想评估现成 Skill 是否可复用
- 用户只知道想解决的问题，还没有明确平台或实现方向

命令路径约定：

- 如果当前目录是 `cocoloop-skill-factory/`，使用 `python3 utils/cli/<script>.py ...`
- 如果当前目录是工作区根目录，使用 `python3 cocoloop-skill-factory/utils/cli/<script>.py ...`

## 开场动作

1. 先说明 `skill-factory` 能做什么，以及当前会从需求调研开始。
2. 浏览当前工作区、仓库和用户给出的上下文，找已有约束。
3. 运行 `python3 utils/cli/detect-environment.py`，如果当前目录不在 skill 根目录，就改用 `python3 cocoloop-skill-factory/utils/cli/detect-environment.py`，拿到当前环境线索。
4. 先确认“当前环境是否就是目标运行环境”；如果不是，继续追问目标平台、目标系统和关键运行前提。
5. 在环境结论没有确认前，不进入 Skill 正文、模板、脚手架、实现步骤或构建命令的撰写。
6. 继续确认正式名称和展示名称；正式名称必须完成 `cocoloop` 与 `clawhub` 双源去重。
7. 判断外部 `brainstorming` 是否可用；可用就优先复用，不可用就回退到 `sub-skills/brainstorm/SKILL.md`。
8. 把问答和阶段结论整理成文档笔记，供设计阶段引用。

## 任务域路由

在继续追问平台、脚本和依赖之前，先完成任务域判断。

第一轮优先判断这些域：

- `engineering_delivery`
- `frontend_design`
- `browser_ui_testing`
- `document_artifacts`
- `docs_research`

第二层扩展域也有正式预设。需求明显落在下面方向时，可以直接作为主域；如果它们只是影响风险、执行面或外部系统边界，再放入 `peer_domains`：

- `workflow_integration`
- `deploy_platform_ops`
- `security_risk_review`

业务横向扩展域也有正式预设。需求明显落在下面方向时，可以直接作为主域；如果它们只是补充产物、素材、数据或风险边界，再放入 `peer_domains`：

- `content_ops`
- `knowledge_base_ops`
- `data_analysis_reporting`
- `customer_support_ops`
- `ecommerce_growth_ops`
- `finance_investment_research`
- `sales_crm_ops`
- `hr_recruiting_ops`
- `education_training_ops`
- `legal_contract_ops`
- `product_market_research`
- `event_community_ops`

路由动作固定如下：

1. 先给出当前最可能的主任务域候选。
2. 如果用户描述明显跨域，再补 `peer_domains`。
3. 如果 `presets/` 中已有对应文档，立即读取预设问题包。
4. 如果没有完全匹配的预设，仍然要先确定最接近的主域，再把剩余部分记入 `open_gaps`。

## 对话节奏

### 分步询问：一次只推进一个问题（强制要求）

**严禁一次性列出所有问题等待用户回答。**

- 每一轮只问一个关键问题
- 必须得到用户回答后，才能决定并询问下一个问题
- 如果某个问题涉及多个子维度，拆成连续轮次推进
- 禁止在同一次回复中抛出多个问题清单

### 问题预算：先规划，再提问（强制要求）

**正式进入调研后，要先规划问题预算，默认总问题数不得超过 10 个。**

- 把必采集字段先按优先级排成最小问题集，再开始发问
- 总问题数包含开放式问题、选项题、路径题和确认题
- 优先复用当前上下文、环境检测、任务域预设和默认值，减少新增问题
- 如果用户开场已经给了高质量 brief，需要主动跳过已覆盖字段
- 当问题数来到第 6 到第 8 个时，优先做阶段收口，而不是继续发散
- 如果继续追问会超过 10 个，必须把剩余不确定项转写为 `open_gaps`、默认假设或后续设计待确认项
- 不允许为了“问全”而拉长访谈；当前版本强调稳定收口，不强调穷尽式盘问

**为什么这样做：**
一次性抛出所有问题会让用户感到压力，导致回复质量下降或选择性忽略部分问题。分步询问可以保持对话的连贯性和质量。
问题预算则用于限制访谈长度，避免最终产物 Skill 在真实使用时变成高摩擦问卷。

### 环境 gate：先确认运行环境，再开始写（强制要求）

**在目标运行环境没有确认前，不允许开始写 Skill 正文、模板、脚手架、实现步骤或构建命令。**

- 优先用环境检测拿到当前环境线索
- 如果用户说“当前环境就是目标环境”，必须做一次显式确认
- 如果目标环境与当前环境不同，必须同时记录当前环境和目标环境，不能混写
- 如果环境仍不明确，只继续做澄清，不提前进入设计或构建表达
- 环境确认可以借助默认值和确认题压缩轮数，但不能被跳过

### 实现方式 gate：先确认执行面，再开始写（强制要求）

**在实现方式没有确认前，不允许开始写脚本方案、adapter、manifest、依赖安装步骤或构建命令。**

- 必须先确认当前任务最终采用哪种执行面
- 当前允许的标准选项只有四种：`Skill-only`、`Skill + CLI`、`Skill + API/MCP`、`Skill + CLI + API/MCP`
- 如果主任务域已有推荐执行面，需要先确认用户是接受默认推荐，还是切换到替代路径
- 如果实现方式仍不明确，只继续做澄清，不进入实现表达

### 标准提问格式

#### 选项类问题（3-5个选项）

使用有序列表编码，便于用户直接回复数字：

```
请选择您的目标平台：

1. **claude code** - 适合日常开发任务
2. **codex** - 适合大规模代码生成
3. **openclaw** - 适合浏览器自动化
4. **copaw** - 适合企业工作流
5. **其他** - 请说明

推荐：**claude code**（当前环境匹配）

请回复选项编号（1-5）：
```

#### 路径选择类问题（2-3个方向）

```
请选择实现路径：

1. **复用现成 Skill** → 推荐
   - 适合：需求与现有 Skill 高度重合
   - 优势：快速交付

2. **基于现成改造**
   - 适合：需求部分重合

3. **从零设计**
   - 适合：需求独特

请回复 1、2 或 3：
```

#### 开放式问题

```
请描述核心问题是什么？

💡 提示：从「谁在什么场景下遇到什么痛点」来描述

请直接输入：
```

#### 确认类问题

```
当前已确认：
- 目标平台：claude code
- 核心问题：自动化代码格式化

是否继续？

1. ✅ 确认并继续
2. ⏸️ 暂停
3. 📝 修改

请回复 1、2 或 3：
```

### 先发散，再收敛

前半段让用户把目标、痛点、理想效果和顾虑讲出来。
后半段把范围缩回到当前版本真正要做的内容。

### 维持阶段感

在阶段内持续向用户说明三件事：

- 已经确认了什么
- 还缺什么
- 下一轮要确认什么

## 必采集信息

进入设计阶段前，至少要采集到下面这些字段：

### 任务域字段

- `primary_domain`
- `peer_domains`
- 是否跨域
- 当前主域默认执行面是否可用

### 任务目标

- 这个 Skill 要解决什么问题
- 谁会用它
- 在什么场景里使用

### 名称身份

- 正式名称，也就是最终 slug
- 展示名称，也就是最终 display name
- 正式名称是否已经完成 `cocoloop` 与 `clawhub` 双源去重

### 目标平台

- 主平台是什么
- 是否要同时覆盖多个平台
- 如果用户说“当前环境就是目标平台”，用环境检测结果确认
- 如果是多平台方案，要区分主平台和次平台，不要只记成一个混合答案
- 每个平台当前属于 `supported_public`、`supported_authoring_only`、`supported_local_only`、`planned` 还是 `unverified`
- 平台等级要能追溯到正式来源；没有来源时不能写成正式兼容

### 运行环境

- 操作系统
- Shell 或执行环境
- 网络能力
- 浏览器能力
- 权限限制
- 是否依赖账号、Cookie、API key 或本地工具
- 当前环境是否就是目标运行环境
- 如果不是，目标环境与当前环境的差异是什么

### 脚本偏好

- 优先使用什么脚本语言，例如 `bash`、`python`、`typescript`、`powershell`
- 明确哪些脚本语言或运行时不能接受
- 是否要求脚本尽量跨平台，还是允许针对单一平台优化
- 是否接受额外安装运行时、包管理器或第三方 CLI

### 依赖偏好

- 更偏向内置能力、外部 Skill、第三方服务，还是混合方案
- 是否接受安装额外工具
- 是否接受在线 API

### 交付预期

- 只要文档
- 需要 Skill 骨架
- 需要完整 Skill 包
- 需要附带 benchmark 计划
- 如果用户要求公开发布，要继续确认目标平台是否真的达到 `supported_public`

### 默认执行面

任务域判断完成后，需要继续确认：

- 当前任务更适合 `Skill-only`、`Skill + CLI`，还是 `Skill + API/MCP`
- 用户是否接受当前主域推荐的执行面
- 如果不接受，替代路径是什么

### 脚本化比例

把关键动作分成三类：

- 适合脚本化
- 适合模板化
- 更适合保留人工判断

### 风格偏好与风格约束

如果任务涉及网页、图片、视觉稿、Figma 或其他视觉输出，必须继续确认：

- 希望的视觉风格，例如简约、科技感、杂志感、卡通、品牌化、运行时可切换
- 风格是否需要稳定复用，还是只要本次输出对齐
- 用户是否希望预装或复用风格约束型 Skill
- 风格来源到底是什么
  - 用户明确指定风格名
  - 用户提供自己的 `DESIGN.md`
  - 用户用自然语言详细描述
  - 用户从 `ref/design-md/` 本地风格参考中选择

并且要同步完成一条隐式判断：

- 当前任务是否包含任何可视化输出
- 这个判断直接写入 `output_profile.has_visual_output`
- 只要判断为真，后续 spec 就必须继续带上 `design_md`

视觉优先任务的强制规则：

- 如果任务涉及网站视觉、视觉优先页面、信息图、视觉卡片或演示稿，在风格来源未明确前，不进入具体设计
- 如果用户没有自己的品牌规范，优先让用户从 `ref/design-md/` 中选起点，或要求用户补自然语言描述
- 不允许默认使用“通用科技感”“通用高级感”这类空泛描述直接进入设计
- 一旦确认了风格来源，继续收口到 `design_md` 字段，避免后续生成 Skill 时丢失设计输入

本地 `DESIGN.md` 参考库入口：

- `ref/design-md/index.md`
- 当前官方预设：IBM、Stripe、Notion、Framer、Figma、Nothing、Apple
- 扩展参考：Linear、Vercel

当前版本默认推荐这些已知可用的风格相关 Skill：

- `frontend-skill`
  适用于网页、落地页、应用界面、交互原型等视觉要求较高的前端任务
- `imagegen`
  适用于单张信息图、视觉海报、说明图、图片生成或位图编辑
- `nothing-design`
  只在用户明确要求 `Nothing` 风格时推荐
- `gemini-image`
  适用于用户明确希望通过 Gemini 工作流生成图片

如果当前环境没有适用的风格类 Skill，也不能跳过风格收集，仍然要把偏好写入需求结果。

### 信息图类任务的补充收集

如果任务是信息图、信息卡片、可视化说明图或传播型视觉页，需要继续确认：

- 最终是单张位图成品，还是后续需要可编辑版式
- 画幅和投放平台
- 哪些文案和数字必须逐字准确
- 更接近海报式传播，还是更接近一页 slide

默认判断顺序：

- 单张传播图优先考虑 `imagegen`
- 如果文本极多、数字必须频繁改动，优先改成可编辑 PPT 或文档页

### PPT 类任务的补充收集

如果最终交付物是 `.pptx`，需要继续确认：

- 目标受众
- 使用场景
- 页数范围
- 比例要求
- 是否必须保留可编辑性
- 是否已有参考 deck、截图或 PDF

当前环境已有 `slides` 能力时，优先把它作为 PPT 生成方向的推荐路径。

### 创作写作类项目的补充收集

如果任务包含文章、脚本、文案、播客提纲、演讲稿或其他创作写作输出，必须继续确认：

- 面向谁写
- 语气与风格是什么
- 篇幅和结构预期是什么
- 是否有参考样本，哪些表达必须避免
- 需要更偏模板化、自由创作，还是强约束改写

如果当前环境里没有合适的写作风格 Skill，就把这些约束直接沉淀到需求结果与 spec，不把 Skill 安装当成前提。

### 网站自动化类任务的风险提示

如果任务涉及网站自动化、登录态操作、批量抓取、批量发布、社媒互动或模拟用户行为，进入细化调研前必须先醒目提示这些风险：

- 账号封禁或限流风险
- 触发验证码、风控或反爬策略的风险
- 平台服务条款、合规与授权边界风险
- 自动化频率过高导致任务不稳定的风险
- 对 Cookie、账号口令、本地会话的安全风险

### 强需求浏览器自动化的路线比较

如果任务在风险提示之后仍然确定要走浏览器自动化，需要继续确认这些内容：

- 当前任务是否已经有公开 API、导出接口或轻量抓取替代路径
- 用户是否接受安装额外 CLI、浏览器扩展、Chrome for Testing 或 Playwright 依赖
- 用户是否必须复用当前 Chrome 或 Chromium 的已登录会话
- 用户更看重现成命令、独立浏览器流程，还是本地调试深度

在这一类任务里，调研阶段不能直接替用户拍板工具，需要至少比较 2 条方向。默认比较顺序如下：

1. `opencli`
   - 适合：任务可落在现成站点命令、`opencli browser` 或适配器流程里，且用户愿意复用当前浏览器登录态
   - 优势：支持面明确，能复用 Chrome 或 Chromium 已登录状态，`opencli doctor` 可直接验收
   - 前置：安装 `@jackwener/opencli`，安装 `OpenCLI Browser Bridge` 扩展

2. `agent-browser`
   - 适合：需要独立浏览器自动化、截图、快照、表单操作、页面核对、回归验证
   - 优势：命令面集中，截图与结构化快照能力直接，适合 Web 页面验证
   - 前置：安装 `agent-browser`，首次运行执行 `agent-browser install`

3. `playwright-interactive`
   - 适合：本地 Web 或 Electron 调试、持久会话 QA、反复改代码再验证
   - 优势：保留 Playwright 会话句柄，适合深度调试
   - 前置：需要 `js_repl`、`playwright` 依赖和更高的环境准备成本

调研阶段输出中必须明确：

- 比较过哪些路径
- 为什么推荐当前路径
- 用户接受了哪些安装前提
- 如果推荐 `OpenCLI`，是否已经补充扩展安装指南与 `opencli doctor` 验证方式

风险提示后，继续确认用户是否接受这些边界，以及最终方案需要怎样的降级路径或人工接管点。

## 搜索进入点

当下面这些信息已经基本稳定时，就应该准备进入搜索：

- 问题和场景已经清楚
- 目标平台已经确定或接近确定
- 用户已经开始关心复用还是新做
- 外部参考会影响设计决策

此时运行：

1. `python3 utils/cli/search-registry.py --source cocoloop --query '...' --exact-slug '<slug>'`，如果当前目录不在 skill 根目录，就改用 `python3 cocoloop-skill-factory/utils/cli/search-registry.py --source cocoloop --query '...' --exact-slug '<slug>'`
2. `python3 utils/cli/search-registry.py --source clawhub --query '...' --exact-slug '<slug>'`，如果当前目录不在 skill 根目录，就改用 `python3 cocoloop-skill-factory/utils/cli/search-registry.py --source clawhub --query '...' --exact-slug '<slug>'`
3. `python3 utils/cli/search-registry.py --source github --query '...'`，如果当前目录不在 skill 根目录，就改用 `python3 cocoloop-skill-factory/utils/cli/search-registry.py --source github --query '...'`
4. 如果这三类结果仍不足以支撑判断，再补通用社区或网页搜索

这里使用的是一个共享搜索入口，分别承载 `cocoloop`、`clawhub` 与 `github` 三类检索能力，不额外扩展到其他阶段动作。

如果搜索失败，不要中断主流程。
要在需求结果里标记“缺少外部参考”。

如果进入搜索后已经形成稳定结论，建议同步写一份 `research-summary.md`，把：

- 环境结论
- 搜索结论
- 需求边界
- 是否需要 benchmark

压成一页摘要，供设计阶段直接引用。

## 调研结果格式

结束本阶段前，要整理出一份统一需求结果，至少包含：

```text
- problem
- audience
- scenario
- skill_identity.slug
- skill_identity.display_name
- target_platforms
- environment
- dependency_preference
- script_preference
- delivery_goal
- scriptable_scope
- style_preference
- output_profile
- design_md
- risk_notes
- benchmark_intent
- reference_search_status
```

这份结果可以是 Markdown 摘要，也可以先落到统一 spec 草稿里。
如果任务涉及网页、信息图、展示图或演示稿，建议在统一 spec 中同步收口：

- `output_profile.has_visual_output`
- `output_profile.visual_output_types`
- `design_md.enabled`
- `design_md.applies_to`
- `design_md.source_mode`
- `design_md.preset_id` 或 `design_md.user_provided_ref`
- `design_md.custom_style_notes`
建议同时保留：

- `brainstorming-notes.md`
- `research-summary.md`
- `requirements.md`
- `environment-notes.md`
- `search-summary.md`

## 结束条件

同时满足下面这些条件时，调研阶段结束：

1. 问题定义已经明确
2. 目标平台已经明确，或收敛到可接受范围
3. 依赖偏好和环境限制已经明确
4. 当前环境与目标运行环境的关系已经明确
5. 当前任务的实现方式已经明确
6. 搜索是否进入、进入后得到了什么，已经完成记录
7. 当前版本的交付预期已经明确

结束后进入 `ref/design.md`。
