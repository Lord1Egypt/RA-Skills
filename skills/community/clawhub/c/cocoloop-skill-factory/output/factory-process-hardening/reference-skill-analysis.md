# Factory Process Hardening - 参考 Skill 本地分析

## 分析方式

本次分析只使用已经在本地可读取的 Skill 文件，不依赖技能市场摘要。

分析对象：

- `/Users/tanshow/.agents/skills/brainstorming/SKILL.md`
- `/Users/tanshow/.codex/skills/skill-creator/SKILL.md`
- `/Users/tanshow/.codex/skills/frontend-skill/SKILL.md`
- `/Users/tanshow/.codex/skills/nothing-design/SKILL.md`
- `/Users/tanshow/.codex/skills/.system/imagegen/SKILL.md`
- `/Users/tanshow/.codex/skills/gemini-image/SKILL.md`

本次除了读取 `SKILL.md`，也检查了这些对象在本地的目录结构：

- `brainstorming`：`agents/`、`scripts/`、`spec-document-reviewer-prompt.md`、`visual-companion.md`
- `skill-creator`：`agents/`、`scripts/init_skill.cjs`、`scripts/package_skill.cjs`、`scripts/validate_skill.cjs`
- `frontend-skill`：`agents/`、`LICENSE.txt`
- `nothing-design`：`agents/`、`references/tokens.md`、`references/components.md`、`references/platform-mapping.md`
- `imagegen`：`agents/`、`assets/`、`references/`、`scripts/image_gen.py`
- `gemini-image`：`agents/`、`scripts/open_gemini.sh`、`scripts/check_page_ready.sh`、`scripts/send_prompt.sh`、`scripts/wait_and_download.sh`

对没有 `scripts/`、`references/` 或 `assets/` 的 Skill，本次按“目录层缺失即代表该层未提供额外资源”处理，而不是假设存在未读内容。

## 1. brainstorming

### 值得吸收的能力

- 进入实现前先完成设计和确认
- 一次只推进一个问题
- 先给 2 到 3 条路线，再收敛
- 要形成设计文档，并设置独立审查环节

### 设计要点

- 把“对话节奏”和“设计产物”绑定起来
- 不只承接问答，还要求产出可复查的 spec
- `agents/openai.yaml` 说明它本身还有单独的 agent 配置层
- `scripts/` 和 `visual-companion.md` 说明它不仅是对话规范，也包含视觉辅助与审查提示的资源组织

### 最佳实践

- 通过硬门槛避免在需求不清楚时过早实现
- 用清晰的阶段出口控制流程质量

### 不直接沿用的部分

- 上游 Skill 要求用户逐段批准设计，这个节奏对 `skill-factory` 来说太重，当前项目只保留“分步确认”的核心

## 2. skill-creator

### 值得吸收的能力

- `scripts / references / assets` 的资源组织方式
- progressive disclosure 的加载思路
- 初始化、编辑、打包、安装、迭代的完整路径

### 设计要点

- 构建 Skill 时，核心指令和可选资源要分层
- 需要把可复用资源前置设计，而不是写完再补
- `scripts/init_skill.cjs`、`package_skill.cjs`、`validate_skill.cjs` 说明它把初始化、校验和打包分成独立脚本，而不是混在文档里

### 最佳实践

- 在 `SKILL.md` 中只保留核心流程，把详细资料放到引用文件
- 要用脚本承接重复、脆弱和高确定性的工作

### 不直接沿用的部分

- 上游面向通用 Skill 创建，本项目需要额外补入多平台、搜索、本地分析和原子能力治理

## 3. frontend-skill

### 值得吸收的能力

- 视觉输出任务需要显式确认视觉方向，而不是直接开始做页面
- 先写 visual thesis、content plan、interaction thesis，再进入实现

### 设计要点

- 风格不是一句“科技感”就结束，需要进一步收口成画面、结构和动效取向
- 该 Skill 没有额外 `references/` 或 `scripts/`，说明它更适合作为轻量风格约束入口，而不是重型流程依赖

### 最佳实践

- 把设计风格问题前置到调研阶段
- 把“何时应该启用此类 Skill”写得足够明确

### 不直接沿用的部分

- 其大量视觉细节规则不应直接复制到 `skill-factory`，这里只需要在推荐流程中承接触发条件和适用边界

## 4. nothing-design

### 值得吸收的能力

- 风格类 Skill 应严格依赖明确触发词
- 需要在进入设计前声明前置条件，例如字体和模式选择

### 设计要点

- 某些风格类 Skill 不应自动推荐，必须由用户明确提出
- `references/` 下拆出了 `tokens`、`components`、`platform-mapping` 三类资料，适合作为“风格类 Skill 需要二级资料承接”的样例

### 最佳实践

- 用清晰的“何时使用 / 何时绝不自动触发”控制误触发

### 不直接沿用的部分

- 该 Skill 自带的特定设计系统规则是 `Nothing` 专属，不适合作为通用默认值

## 5. imagegen

### 值得吸收的能力

- 明确区分适用场景和不适用场景
- 先判断是生成还是编辑，再决定执行路径
- 对输出文件路径和覆盖策略做明确约束

### 设计要点

- 图片相关能力不只是“会生成图”，还需要明确边界、落盘策略和保留策略
- `references/` 与 `scripts/image_gen.py` 的组合说明：复杂能力既要有流程说明，也要有备用执行层

### 最佳实践

- 将工作流拆成决策树，再进入执行步骤
- 用明确的约束条件减少误用

### 不直接沿用的部分

- 其具体图像生成执行细节不进入 `skill-factory`，这里只保留推荐和能力判断逻辑

## 6. gemini-image

### 值得吸收的能力

- 对外部服务型 Skill，要把前置条件写清楚
- 工作流要包含会话首次使用时的特殊步骤
- 浏览器自动化类流程需要把环境前提和失败处理写明

### 设计要点

- 如果未来 `skill-factory` 推荐此类 Skill，必须同步提示平台、浏览器、账号和权限前提
- `scripts/` 目录中的多个 shell 脚本说明它是强执行路径 Skill，不适合在只要风格建议时默认触发

### 最佳实践

- 对外部服务自动化，使用分步骤流程和错误处理说明

### 不直接沿用的部分

- 该 Skill 强依赖 macOS、Chrome 和 Google 账号，不适合作为通用默认推荐

## 汇总结论

这次本地分析确认了两件事：

1. 已完成 todo 中的“调研补齐收集项”和“本地拉取后再设计”都不是抽象建议，它们背后有成熟 Skill 可以支撑的正式方法论
2. `skill-factory` 在推荐外部 Skill 时，必须把“触发条件、适用边界、前置依赖、最佳实践”一起沉淀下来，否则设计文档仍然是不完整的

## 本次分析缺口

本次已经覆盖了本地目录结构、显式脚本、显式引用文件和可见资源层。

仍然存在的边界如下：

- 没有逐个深入阅读所有引用文件全文，只在需要时确认了其存在与用途分层
- 没有执行外部 Skill 自带脚本，本次目标是设计方法验证，不是功能验证
- 对没有 `references/` 或 `scripts/` 的 Skill，不额外假设存在隐藏资源

这些缺口已经被明确记录，因此本次结论只用于 `skill-factory` 的流程设计，不直接作为外部 Skill 的功能验收结论。
