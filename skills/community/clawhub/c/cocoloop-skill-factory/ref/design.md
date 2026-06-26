# 设计阶段指南

当前版本阶段声明：
本阶段只产出方案设计文档和构建准备输入，不直接生成 Skill 包。

## 目标

设计阶段负责把调研结果转成可以执行的 Skill 方案。
这里要让用户看到选择空间，也要把选择收回到一条明确路线。

## 视觉任务前置门槛

如果任务涉及下面任一情况，先确认风格来源，再进入具体页面、版式或视觉稿设计：

- 网站视觉
- 视觉优先落地页
- 信息图与视觉卡片
- `.pptx` 或 HTML slides 的视觉设计
- 高要求排版页面

允许的风格来源只有四类：

1. 用户明确指定风格名
2. 用户提供自己的 `DESIGN.md`
3. 用户用自然语言给出足够具体的风格描述
4. 用户从 `ref/design-md/` 本地参考库中选一个起点

如果风格来源还没定，设计阶段只允许停留在结构方案、信息架构和低保真方向，不进入具体视觉设计。
如果已经确定进入正式视觉输出，还需要把风格结论继续写入统一 spec 的 `design_md` 块，避免后续模板和生成链丢失这层约束。
如果任务已经明显包含可视化输出，还要同步把这个隐式判断写入 `output_profile.has_visual_output`，避免后续产物漏掉 `design.md` 模板。
如果目标属于视觉叙事型产物，还要继续把共享主线写入 `visual_storytelling`，避免不同产物各自重新发明结构规则。

## 输入

设计阶段默认接收这些输入：

- 调研阶段收口后的需求结果
- 当前任务域与对应预设
- 环境检测结果
- `cocoloop` 与 `clawhub` 搜索结果，或其降级记录
- 用户已有的参考 Skill、仓库或流程样例
- 已确认的脚本偏好、风格偏好、风格来源与自动化风险说明
- 已确认的正式名称、展示名称，以及 slug 去重结论
- 已确认的 `design_md` 结果，或待补齐的设计来源缺口
- 如果适用，已确认的 `visual_storytelling` 结果

## 设计节奏

### 先展开

围绕用户目标提出两到三条可行路线。
如果当前需求已经匹配到任务域预设，先把预设里的默认执行面作为第一层候选。
第一版优先使用这三种路线做比较：

1. 直接复用现成 Skill
2. 基于现成 Skill 做二次设计
3. 从零构建新的 Skill

### 再收敛

比较完路线后，帮助用户确定当前版本该走哪一条。
收敛时不只要写“选了什么”，还要写清楚“为什么这样选”。

## 每条路线都要回答的问题

1. 这条路线解决用户问题的完整度有多高
2. 覆盖目标平台的难度有多高
3. 对外部依赖的要求有多高
4. 需要多少脚本化能力
5. 需要哪些原子能力模块
6. 当前版本能做到多完整
7. 风险和后续扩展点是什么

## 搜索结果的用法

搜索结果不能只作为名字列表存在。
设计阶段要把搜索结果转成决策材料，至少给出这些判断：

- 是否值得直接复用
- 是否适合作为参考后改造
- 是否只适合借鉴其中一部分能力
- 是否应放弃该候选

如果当前需求已经判定主任务域，设计阶段还要回答：

- 候选方案是否覆盖该任务域的核心高频任务
- 候选方案是否符合该任务域默认执行面
- 如果不符合，偏差是能力缺口，还是执行面不匹配

### 本地拉取与深度分析要求

只要某个候选 Skill 进入设计比较范围，就必须先把它全量拉取到本地进行分析，不能只看搜索摘要、商店页面或简短介绍。

优先使用 `reference-skill.py` 固化证据：

- 本地候选：`python3 utils/cli/reference-skill.py fetch --source local --path <skill-dir> --out <evidence-dir> --slug <candidate-slug>`
- GitHub 候选：`python3 utils/cli/reference-skill.py fetch --source github --url <repo-url> --out <evidence-dir> --slug <candidate-slug>`
- 已有目录复查：`python3 utils/cli/reference-skill.py analyze --path <skill-dir> --markdown <analysis.md>`

本地分析时至少要覆盖这些内容：

- `SKILL.md` 的触发说明、流程结构和资源读取顺序
- 目录结构和子 Skill 组织方式
- `scripts/`、`references/`、`assets/`、模板文件和示例文件
- 外部依赖、安装方式、权限要求和运行时假设
- 已体现出来的最佳实践、边界处理和降级策略

如果候选 Skill 无法完整拉取到本地，设计文档里要明确标记分析缺口，不要把不完整观察写成确定结论。

### 设计文档中的沉淀要求

对每个进入深入分析的候选 Skill，设计文档至少要详细记录：

- 哪些能力值得复用或借鉴
- 哪些设计要点适合保留
- 哪些功能实践可以视为最佳实践
- 哪些部分不适合沿用，以及为什么
- 与当前需求、当前平台和当前版本边界的关系

如果设计里涉及浏览器自动化路径比较，设计文档还需要继续记录：

- `opencli`、`agent-browser`、`playwright-interactive` 各自的安装方式和首次使用前置动作
- 哪个方案复用当前浏览器登录态，哪个方案更适合独立自动化或本地调试
- 为什么当前需求选择 `OpenCLI`、`agent-browser` 或 `playwright-interactive`
- 如果推荐 `OpenCLI`，扩展安装说明和 `opencli doctor` 验证如何交付给用户
- 未被选中的路线保留为哪一种降级或替代路径

这些内容建议优先写入：

- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`

其中 `reference-skill-analysis.md` 负责承接候选 Skill 的细节拆解，`design-summary.md` 负责承接设计决策和取舍原因。

### 浏览器自动化方向的推荐顺序

当用户任务强依赖浏览器自动化时，设计阶段默认使用下面的判断顺序：

1. 先确认业务是否已经被 `OpenCLI` 的现成站点命令、`opencli browser` 或适配器流程覆盖
2. 如果覆盖且用户接受扩展安装，优先推荐 `OpenCLI`
3. 如果任务更偏独立浏览器流程、页面验证、结构化截图和表单自动化，优先考虑 `agent-browser`
4. 如果任务更偏本地 Web 或 Electron 调试、持久会话 QA、反复 reload 与复测，再考虑 `playwright-interactive`

这个顺序用于帮助用户收敛，不代表可以跳过比较。设计文档仍然需要把利弊和替代路径写清楚。

## 平台与模板判断

设计阶段必须明确平台差异会怎样影响方案。
至少覆盖这些维度：

- Skill 包结构
- 元数据表达
- 子 Skill 组织方式
- 外部依赖写法
- 安装与使用路径
- 是否需要单独模板

特别要求：

- `molili` 必须按独立平台处理
- 多平台方案要说明哪些内容共用，哪些内容分支

## 原子能力判断

设计阶段要把能力拆成可组合单元，便于后续装配。
优先顺序改为：

1. 当前任务域预设
2. `atomic-capability/index.md`
3. 外部方案或第三方工具

优先从 `atomic-capability/index.md` 中选取能力，再决定是否引入外部方案。

如果需求里已经确认需要视觉风格约束、图片生成流程或写作风格约束，也要在这里明确：

- 这些约束是通过现成 Skill 承接，还是只写入文档与模板
- 风格约束是否属于当前版本范围
- 如果不引入额外 Skill，后续如何在 spec 和模板里保留风格要求
- 如果用户没有自带风格规范，是否采用 `ref/design-md/` 中的本地风格参考作为起点
- 如果最终 Skill 需要交付官方设计实例，是否将所选风格映射到 `design_md.preset_id`
- 最终 Skill 是否需要在 `references/design.md` 中固化官方实例，并保留 `references/design-md/` 作为可切换预设库
- 如果任务包含任何可视化输出，是否已经把 `output_profile.has_visual_output` 写成 `true`

如果设计需要外部方案，必须同步补齐：

- 使用前提
- 安装或接入方式
- 风险与限制
- 不采用它时的替代路径

## 设计结果格式

结束本阶段前，至少产出这些结论：

```text
- chosen_route
- why_this_route
- chosen_execution_plane
- scope_now
- scope_later
- target_platforms
- primary_domain
- peer_domains
- template_direction
- capability_plan
- dependency_strategy
- artifact_plan
- benchmark_decision
```

这份结论应能直接交给构建阶段使用。
如果已经确定进入构建准备，建议把这些结论同步整理成：

- `reference-skill-analysis.md`
- `design-summary.md`
- 更新后的 `spec.md`
- 单独的 `build-plan.md`

其中 `reference-skill-analysis.md` 负责记录本地拉取后的候选 Skill 分析，`design-summary.md` 负责说明路线比较与收敛原因，`build-plan.md` 负责给构建准备阶段提供稳定输入。

## 结束条件

同时满足下面这些条件时，设计阶段结束：

1. 已经比较过两到三条路线
2. 已经确定当前版本的主路线
3. 已经明确目标平台和模板方向
4. 已经明确内置能力、外部依赖和降级路径
5. 已经明确 benchmark 是否进入

结束后进入 `ref/construction.md`。
