---
name: cocoloop-skill-factory
description: 用于创建或升级多平台 Agent Skill 的 Meta Skill。适用于用户想把模糊想法收敛成可生成最终 Skill 的稳定方案、需要结合 Cocoloop 与 ClawHub 搜索参考、选择平台模板、组织原子能力、补齐脚本化规划，并明确平台兼容与发布边界时。
version: 0.3.5
author: tanshow
---

# CocoLoop Skill Factory

## Overview

`cocoloop-skill-factory` 是一个面向 `codex`、`claude code`、`openclaw`、`copaw`、`molili`、`hermes agent` 的 Meta Skill。
它负责把用户的想法推进成一份稳定 spec，并把构建方向、模板选择、原子能力、脚本化策略和平台兼容边界整理清楚，最终服务于 Skill 生成与交付。

当用户出现这些诉求时使用本 Skill：

- 想从零创建一个新 Skill
- 想升级、改造、移植一个已有 Skill
- 想先找现成 Skill，再判断复用、改造还是新做
- 想把平台差异、脚本化能力、模板选择和 benchmark 规划统一起来

## Factory Rules

整个流程都围绕这几条规则执行：

1. 先判定任务域，再继续调研平台、依赖和执行面。
2. 先形成 spec，再进入构建与交付判断。
3. 调研和设计都保持双钻节奏，先发散，再收敛。
4. **分步询问：对话每次只推进一个关键问题，严禁一次性列出所有问题等待用户回答。必须等用户回答后再问下一个问题。**
5. **问题预算：进入调研后要先规划整轮交互的问题预算，默认总问题数不得超过 10 个。能用默认值、环境检测、已有上下文或确认题解决的，不再追加开放式追问。**
6. **环境 gate：在目标运行环境没有确认前，不得开始写 Skill 正文、模板、脚手架、实现步骤或构建命令。必须先拿到环境检测结果，再确认“当前环境是否就是目标环境”；如果不是，要同时写清当前环境和目标环境。**
7. `cocoloop`、`clawhub` 与 `github` 搜索在正常环境下默认进入流程；通用社区检索按需补充；不可用时允许降级，但要记录缺口。
8. 平台兼容声明必须以公开标准或已核实的本地协议为依据，不能凭经验口头承诺。
9. 推荐外部方案时，要同时给出接入方式、依赖门槛、风险和替代路径。
10. `benchmark` 是可选阶段，只在适合比较的任务里进入，并且默认按任务域判断是否适合进入。

## Workflow

命令运行约定：

- 如果当前目录是 `cocoloop-skill-factory/`，使用 `python3 utils/cli/<script>.py ...`
- 如果当前目录是工作区根目录，使用 `python3 cocoloop-skill-factory/utils/cli/<script>.py ...`
- CLI 文件带有 shebang，也可以直接执行，但默认优先推荐 `python3 ...` 的写法

关键 CLI：

- `detect-environment.py`
- `search-registry.py`
- `reference-skill.py`

当前 CLI 边界：

- `detect-environment.py` 用于环境检测
- `search-registry.py` 用于统一承载 `cocoloop`、`clawhub` 与 `github` 搜索
- `reference-skill.py` 用于把本地或 GitHub 候选 Skill 拉取到证据目录，并生成 JSON / Markdown 分析摘要
- 当前版本不提供完整的自动生成与发布 CLI，但必须在文档层明确生成、校验和发布所缺的环节

其中 `search-registry.py` 是对 PRD 中 `cocoloop-search`、`clawhub-search` 与 GitHub 检索的合并实现，只覆盖搜索能力本身，不新增额外流程能力。
其中 `reference-skill.py` 只负责候选方案证据化和目录分析，不替代设计判断。

### Step 1: Initialize

先快速建立当前任务边界。

执行动作：

1. 判断用户要创建新 Skill，还是升级已有 Skill。
2. 检查当前仓库、工作区或现有文件里是否已经有相关上下文。
3. 运行 `python3 utils/cli/detect-environment.py`，获取平台、系统、Shell、浏览器与本地工具线索。
4. 先确认当前环境是否就是目标运行环境；如果不是，继续让用户明确目标平台、目标系统和关键运行前提。
5. 在环境结论没有确认前，不进入 Skill 正文、模板、脚手架或构建步骤的撰写。
6. 先判断当前需求属于哪个任务域；如果 `presets/` 里已有对应预设，立即读取。
7. 如果用户说“目标平台就是当前环境”，用检测结果提供候选线索，再请用户确认。
8. 判断当前环境里是否已有成熟 `brainstorming` 能力；如没有，再回退到 `sub-skills/brainstorm/SKILL.md`。

### Step 2: Research

进入需求调研阶段时，阅读 `ref/research.md`。

**调研阶段先做任务域路由**

- 先判定 `primary_domain`
- 如果需求明显跨域，再补 `peer_domains`
- 如果 `presets/` 中已有对应预设，优先按预设问题包继续追问
- 如果没有完全匹配的预设，也要先给出最接近的主域判断，再把剩余部分写入研究缺口

**调研阶段核心原则：分步询问，一次一个问题**

- 每一轮对话只问一个关键问题，严禁一次性列出多个问题
- 必须得到用户回答后，才能决定并询问下一个问题
- 如果用户给出的信息涉及多个维度，拆分成连续轮次推进
- 维持对话的连续性，避免信息过载

**调研阶段核心原则：先规划问题预算，总量不超过 10 个**

- 进入调研后，先根据当前任务域和缺口列出最小问题集，再开始追问
- 整轮需求调研默认总问题数不得超过 10 个，包含确认题
- 如果用户初始信息已经较完整，要主动合并或跳过冗余问题，而不是把预算问满
- 当预计会超过 10 个问题时，优先改成选项题、确认题、默认值和环境检测，不继续扩张访谈
- 在第 6 到第 8 个问题时，优先开始收口，整理已确认项、未确认项和默认假设
- 如果还有缺口但继续追问收益不高，明确记录到 `open_gaps`，再进入设计，不要无限延长调研

**调研阶段核心原则：先确认运行环境，再开始写**

- 优先用环境检测拿到当前环境线索，再确认目标环境
- 如果用户说“就在当前环境里跑”，必须把当前环境和目标环境做一次显式确认
- 如果目标环境与当前环境不同，必须同时记录两者差异，不能只写当前环境
- 在环境未确认前，只允许继续做澄清，不允许开始写 Skill 正文、模板、脚手架、实现步骤或构建命令

**调研阶段核心原则：先确认实现方式，再开始写**

- 必须先确认当前任务的实现方式，也就是选定 `Skill-only`、`Skill + CLI`、`Skill + API/MCP` 或 `Skill + CLI + API/MCP`
- 如果主任务域已有推荐执行面，需要让用户确认是接受该默认执行面，还是切换到替代路径
- 在实现方式没有确认前，不开始写脚本方案、adapter、manifest、依赖安装步骤或构建命令

**提问交互格式：**

1. **选项类问题**：提供 3-5 个有序选项（1-5），便于用户直接回复数字
   - 示例：目标平台选择、交付预期选择
   - 必须标注推荐答案

2. **路径选择类问题**：提供 2-3 个实现路径
   - 示例：复用现成 / 改造 / 从零设计
   - 必须说明各路径的适用场景、优势和风险
   - 明确标注推荐路径及理由

3. **开放式问题**：提供提示和示例，引导用户描述
   - 示例：「请描述核心问题是什么？提示：从谁在什么场景下遇到什么痛点来描述」

4. **确认类问题**：汇总已确认信息，提供继续/暂停/修改选项
   - 示例：「当前已确认：... 是否继续？1. ✅ 确认 2. ⏸️ 暂停 3. 📝 修改」

调研阶段必须拿到这些信息（分步采集）：

- 主任务域、并列补充域，以及是否跨域
- 用户想解决的问题与使用场景
- 正式名称与展示名称
- 目标平台与运行环境
- 当前环境是否就是目标运行环境，以及两者差异
- 实现方式，也就是最终采用哪种执行面
- 目标平台对应的支持等级、公开标准来源，以及用户是否接受当前等级边界
- 正式名称是否已完成 `cocoloop` 和 `clawhub` 双源去重
- 偏好脚本语言、不可接受的脚本语言，以及运行时限制
- 依赖偏好与权限限制
- 如果涉及网页、图片、Figma 或其他视觉输出，要收集风格偏好，并判断是否需要引入风格约束型 Skill
- 如果已经明显包含可视化输出，要隐式把这个判断写入 `output_profile.has_visual_output`
- 如果涉及创作写作类输出，要收集受众、语气、篇幅、参考边界和禁忌表达
- 如果涉及网站自动化、登录态操作、批量发布或抓取，要先醒目声明账号、频率限制、验证码、反爬和平台规则风险，再继续调研
- 如果涉及强需求浏览器自动化，要比较可用执行面，并明确用户接受的安装与维护成本
- 交付预期
- 哪些能力应脚本化，哪些保持文档或模板表达
- 成功标准与是否需要 benchmark

视觉输出场景的默认推荐顺序：

- 网页、落地页、应用 UI：优先判断是否需要 `frontend-skill`
- 单张信息图、视觉说明图、传播型图卡：优先判断是否需要 `imagegen`
- 用户明确要求 `Nothing` 风格：再引入 `nothing-design`
- 图片生成或图片编辑：判断是否需要 `imagegen` 或 `gemini-image`
- 如果最终交付物是 `.pptx`，优先判断是否需要 `slides`
- 如果当前环境没有合适的风格约束 Skill，仍然要把风格偏好写入 spec，而不是跳过

视觉优先任务的强制规则：

- 如果任务涉及网站视觉、视觉优先页面、信息图、视觉卡片或演示稿视觉，在进入具体设计前，必须先确认风格来源
- 风格来源只允许这四类：用户指定风格、用户提供 `DESIGN.md`、用户详细描述、从 `ref/design-md/` 本地参考库中选择
- 如果这四类输入都没有，只继续追问风格来源，不进入具体版式和视觉方案
- 如果需求进入正式视觉方案，继续把风格结论写入 `design_md`，让最终 Skill 自带 `references/design.md`
- 只要任务包含任何可视化输出，统一 spec 中就必须写出 `output_profile.has_visual_output: true`
- 如果目标产物属于 PPT、网页信息图、展示图、报告页等视觉叙事型产物，优先读取 `atomic-capability/structured-visual-storytelling/`

名称收口的强制规则：

- 正式名称对标最终 slug，必须使用短横线连接的小写英文与数字
- 展示名称对标最终 display name，长度不得超过 20 个字符
- 在进入设计或生成前，必须完成 `cocoloop` 和 `clawhub` 双源去重
- 双源去重结果要写进 `research_gate.skill_identity`

创作写作类场景的处理原则：

- 先确认写作对象、发布场景、语气、篇幅和参考边界
- 如果当前环境里有合适的写作或风格类 Skill，再进入推荐
- 如果没有现成 Skill，也要把风格约束明确写进需求结果与后续 spec

强需求浏览器自动化场景的处理原则：

- 先判断任务能否被文本接口、公开 API 或轻量抓取替代，能替代时不要默认上浏览器自动化
- 如果必须上浏览器自动化，至少向用户比较 2 条方向，常用候选是 `opencli`、`agent-browser`、`playwright-interactive`
- 比较时至少说明这几个维度：是否复用现有登录态、安装门槛、调试深度、稳定性、维护成本、失败后的替代路径
- 如果用户接受额外安装，且任务已落在 `OpenCLI` 已有站点命令、`opencli browser` 或适配器流程可覆盖的范围内，优先推荐 `OpenCLI`
- 选择 `OpenCLI` 时，补充 `atomic-capability/browser-access/opencli-browser-bridge.md` 中的扩展安装与 `opencli doctor` 验证步骤
- 如果任务更偏本地页面验证、结构化截图、表单回归或独立浏览器流程，优先把 `agent-browser` 作为候选
- 如果任务更偏本地 Web 或 Electron 调试、持久会话 QA、反复迭代验证，再把 `playwright-interactive` 纳入候选

如果用户一开始就已经给出很清楚的 spec，可缩短调研轮数，但不能跳过收口确认。

### Step 3: Search And Reference

当需求轮廓已经稳定，就进入搜索判断。

默认顺序：

1. 先根据主任务域和预设整理默认搜索关键词
2. 运行 `python3 utils/cli/search-registry.py --source cocoloop --query '...' --exact-slug '<slug>'`
3. 运行 `python3 utils/cli/search-registry.py --source clawhub --query '...' --exact-slug '<slug>'`
4. 运行 `python3 utils/cli/search-registry.py --source github --query '...'`
5. 对进入正式比较范围的本地或 GitHub 候选，运行 `python3 utils/cli/reference-skill.py fetch ...` 拉取并生成 `_reference-analysis.md`
6. 如仍有明显缺口，再补通用社区或网页搜索
7. 把结果整理成“直接复用 / 参考改造 / 仅供借鉴 / 放弃”四种结论

判断时至少回答这些问题：

- 候选 Skill 与当前需求的重合度有多高
- 是否覆盖当前主任务域的核心高频任务
- 是否覆盖目标平台
- 是否有明显依赖门槛或安全风险
- 如果采用它，用户得到的是安装、二次设计，还是只拿它的能力结构
- 如果它属于浏览器自动化候选，当前覆盖面是否已经足够支撑任务，还是只能作为备选路径

如果搜索不可用，保留降级记录，再继续设计流程。

### Step 4: Design

进入设计阶段时，阅读 `ref/design.md`。

设计阶段的硬规则：

- 优先读取当前主任务域对应的预设，再展开方案比较
- 如果任务涉及排版、视觉设计、网站风格、信息图或演示稿视觉，先确认风格来源，再进入具体设计
- 如果任务属于更广义的视觉叙事型产物，先走 `structured-visual-storytelling` 的共享主线，再选 `ppt`、`web_infographic` 或 `showcase_graphic` adapter
- 只要搜索结果里有需要深入判断的候选 Skill，就**必须**先把候选 Skill 全量拉取到本地再分析，不能只依据搜索摘要做设计决策
- 本地分析时，要完整查看 `SKILL.md`、子目录结构、脚本、参考文档、模板、依赖声明和关键资源
- 需要复用或借鉴的能力、设计要点、功能最佳实践和限制条件，必须详细写入设计文档，而不是只保留在临时分析里
- 如果当前设计在比较浏览器自动化方向，需要把 `opencli`、`agent-browser`、`playwright-interactive` 的安装方式、运行前置动作、适用边界和推荐顺序一起写进设计文档

视觉风格参考默认读取顺序：

1. 用户自己的品牌规范或 `DESIGN.md`
2. 用户明确点名的风格
3. `ref/design-md/` 本地风格参考库
4. 用户的自然语言风格描述

当前官方预设优先级：

1. IBM
2. Stripe
3. Notion
4. Framer
5. Figma
6. Nothing
7. Apple

设计阶段必须先展开两到三条路线，再帮助用户收敛。常见路线：

- 直接复用现成 Skill
- 基于现成 Skill 做二次设计
- 从零构建新 Skill

设计收口时，要明确这些结论：

- 当前版本的目标与边界
- 目标平台集合
- 主流程结构
- 内置原子能力与外部依赖的取舍
- 平台模板选择
- benchmark 是否进入，以及为什么

### Step 5: Construction Planning

进入构建准备时，阅读 `ref/construction.md`。

此阶段的核心动作：

1. 把研究与设计结论整理成统一 spec 和构建说明。
   先形成一份结构化 `spec.yaml`，再继续整理研究摘要、设计摘要和构建计划。
   如果没有 `primary_domain`、`coverage_status` 或 `open_gaps` 的收口结果，不得进入下一步。
   如果任务涉及视觉排版产物，还需要继续补齐 `output_profile` 与 `design_md`。
2. 阅读 `atomic-capability/index.md`，为关键能力选择可复用模块。
3. 阅读 `presets/index.md` 和当前主任务域预设，确认默认输出、风险门槛和执行面。
4. 阅读 `utils/template/` 下的目标平台模板，明确输出骨架、元数据差异和脚本策略。
5. 调用 `sub-skills/skill-creator/SKILL.md`，把 spec 转成可执行的构建计划。
6. 如果任务适合比较验证，再阅读 `utils/benchmark.md`，只规划 benchmark 的进入条件、样本和判定标准。
7. 如果目标平台属于任意 `supported_*`，继续补平台安装、校验和发布边界；`supported_public` 可进入打包准备，`supported_authoring_only` 与 `supported_local_only` 只能停在作者规范或本地激活边界。
8. 条件满足时，先在 `factory-skill-builder/` 执行 `npm install`，再使用 `factory-skill-builder/scripts/build_skill_from_spec.cjs` 生成最小 Skill 骨架，并用平台校验脚本确认结果；生成链要把模板选择结果一并写入产物。
   如果 `output_profile.has_visual_output` 为真，生成链还要继续输出 `references/design.md` 与 `references/design-md/`。

建议在这一阶段保留的文档产物：

- `spec.yaml`
- `brainstorming-notes.md`
- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- `benchmark-plan.md`（仅在进入 benchmark 时）
- `platform-support-notes.md`（平台声明有特殊边界时）

### Step 6: Deliver

默认交付物包括：

- 一份收口后的统一 spec
- 一份设计决策摘要
- 一份构建计划或构建说明
- 外部依赖的接入说明
- 一份平台兼容与发布边界说明
- 按需生成的 benchmark 计划

如果用户只想得到设计方案，不想立即落地产物，可以在 spec 和设计决策确认后结束。

## Fast Paths

### 用户已经带着参考 Skill 来了

先检测环境，再直接做差异分析：

1. 当前参考 Skill 覆盖了哪些能力
2. 哪些地方要保留
3. 哪些地方要替换
4. 哪些平台适配要重写

### 用户只想找现成 Skill

仍然要先补齐最小需求轮廓，再搜索。
不要在问题尚未收敛时直接把一串候选列表甩给用户。

### 用户只想做平台迁移

优先保留原 Skill 的目标、触发方式和能力边界，再聚焦模板映射、依赖表达和目录结构变化。

## Local Resources

按下面的顺序读取资源，避免一次加载过多内容：

- `ref/research.md`
  需求调研阶段的对话骨架、必填信息和阶段出口
- `ref/design.md`
  方案展开、比较和收口方式
- `ref/platform-support-matrix.md`
  子仓内的本地平台支持矩阵与声明边界
- `factory-skill-builder/scripts/`
  `factory` 内部的 `spec -> skill` 渲染、平台校验与打包入口
- `ref/construction.md`
  如何把统一 spec 收口为构建计划与产物边界
- `sub-skills/brainstorm/SKILL.md`
  没有外部 brainstorming 时的兜底调研子 Skill
- `sub-skills/skill-creator/SKILL.md`
  进入构建准备阶段时的规划子 Skill
- `presets/index.md`
  任务域预设目录和对应问题包、执行面建议
- `atomic-capability/index.md`
  原子能力索引与组合建议
- `utils/template/spec-template.yaml`
  统一结构化协议模板
- `utils/template/*.md`
  平台模板、结构差异和选择条件
- `output/README.md`
  `output/` 目录契约和每类产物职责
- `utils/cli/*.py`
  环境检测与搜索标准化
- `utils/benchmark.md`
  benchmark 进入条件与输出格式

## Output Contract

产出构建计划或 Skill 方案文档时，至少检查这些项目：

1. `SKILL.md` 是否能独立说明触发场景、流程和资源读取顺序
2. 目标平台模板是否与最终目录结构一致
3. 外部依赖是否都有接入说明和降级路径
4. 当前阶段允许脚本化的动作是否已经覆盖环境检测、搜索、最小渲染与平台校验
5. `molili` 是否按独立平台处理，没有被并入 `copaw`
6. 是否已经明确目标平台对应的目录和元数据要求
7. benchmark 若被启用，是否明确了 `0 skill` 与目标 Skill 方案效果的比较对象

## Boundaries

本 Skill 负责 spec 驱动、方案组织、参考检索和构建规划。
它不会把搜索命中当作唯一前提，也不会默认替用户跳过需求收口。

如果当前任务只适合出文档，不适合进入下一阶段实现，可以在说明原因后收口到文档阶段。
