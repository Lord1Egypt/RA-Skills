---
name: brain-trust-private-board
description: 智囊团式私董会多专家协作分析框架，支持2-5位专家私董会式动态讨论、正反辩论、红队审查、方案对比和综合决策判断。当用户需要多角度分析复杂问题、战略决策、产品方向、商业方案评审、管理困惑、学习规划、研究分析时使用。
---

# 智囊团：私董会

把专家当作“方法镜头”，不是当作“权威摆设”。
先帮助用户解决问题，再适度借用专家的语言风格。

## 快速开始

1. 如果用户已经指定专家，优先使用该专家。
2. 如果用户没有指定专家，先读 [references/expert-selection.md](references/expert-selection.md) 选 1-3 位最合适的专家。
3. 如果问题类型很明确，再读 [references/high-frequency-use-cases.md](references/high-frequency-use-cases.md) 先走高频场景直达。
4. 只读取 [references/expert-frameworks.md](references/expert-frameworks.md) 中需要的条目，不要一次性加载整份专家库。
5. 如果任务是 skill、prompt、workflow 评审，优先读 [references/skill-prompt-review.md](references/skill-prompt-review.md)。
6. 如果想直接套调用句式，再读 [references/call-patterns.md](references/call-patterns.md)。
7. 如果问题类型仍需要展开，再读 [references/task-recipes.md](references/task-recipes.md)。
8. 如果任务需要私董会式动态讨论、多专家对照、辩论、红队或综合判断，再读 [references/output-modes.md](references/output-modes.md)。
9. 如果需要稳定交付格式，再读 [references/deliverable-templates.md](references/deliverable-templates.md)。
10. 如果想让输出更像成熟顾问稿或评审稿，再读 [references/output-style-templates.md](references/output-style-templates.md)。
11. 交付前用 [references/quality-guardrails.md](references/quality-guardrails.md) 做一次快速检查。

## 工作原则

- 优先还原专家的判断框架、关注点和分析顺序，不要只模仿口吻。
- 默认用第三人称表达专家视角；只有用户明确要求时，才做轻度第一人称风格化输出。
- 不把专家当作事实来源。涉及事实、数据、日期、政策时，仍按正常信息核验流程处理。
- 不伪造专家的具体经历、私下态度或未公开立场。
- 不滥用专家数量。能用 1 位解决，就不要硬凑 3 位。
- 遇到信息不足时，优先明确假设并继续推进；只有关键缺口会直接改变结论时，才补问 1 个短问题。
- 先给结论，再展示专家视角，不要把回答写成纯表演。
- 用户要的是“更好的判断”，不是“更像某个人说话”。
- 多专家场景默认更像“私董会”而不是“轮流念稿”。
- 谁发言、谁接话、谁追问，应由当前话题、冲突点、机会点和盲区决定，而不是固定顺序。
- 允许某位专家连续接话，也允许某位专家整场只在关键节点出声。
- 讨论的目标不是平均发言，而是尽快把问题打深、打透、打出结论。

## 不适用场景

下面这些情况，不要强行调用专家模式：

- 只是普通事实问答
- 只是机械改写、翻译、润色
- 已经有明确标准答案且不需要视角比较
- 用户只要一句直接建议，且专家视角不会增加价值

## 输入约定

如果调用方已经提供结构化输入，优先兼容下面这些字段：

```json
{
  "goal": "任务目标",
  "problem_context": "背景、约束、现状、已有方案",
  "expert_name": "单一专家名，可选",
  "expert_names": ["多个专家名，可选"],
  "mode": "single|compare|debate|panel|boardroom|critique|red-team|synthesis",
  "output_format": "analysis|solution|advice|memo|checklist",
  "audience": "面向谁输出",
  "constraints": ["预算", "时间", "资源", "风险边界"],
  "deliverable": "最终想得到什么",
  "decision_stage": "explore|evaluate|choose|critique|revise",
  "risk_level": "low|medium|high",
  "time_horizon": "short|mid|long"
}
```

如果输入不完整，就从用户原话里自行补齐最小工作上下文：

- 任务到底在解决什么问题
- 决策对象是什么
- 成功标准是什么
- 有哪些明显约束
- 输出更适合分析、建议、方案还是评审

缺信息时，至少把下面四项补到位再开始：

- `goal`
- `constraints`
- `decision_stage`
- `deliverable`

## 执行流程

### 1. 先把问题框住

先用 3-5 个要素重述问题，例如：

- 目标
- 约束
- 可选路径
- 关键变量
- 主要风险

不要一上来直接“扮演专家”。

如果用户给的是一个很散的问题，先把它压成一句决策句：

- “是否应该……”
- “哪条路径更适合……”
- “现有方案最大的问题是……”
- “要不要继续推进……”

### 2. 选择模式

按任务选择最合适的工作模式：

- `single`：一个专家给出主判断
- `compare`：两个或三个专家并排比较
- `debate`：让立场有张力的专家正反交锋
- `panel`：三到四位专家会诊
- `boardroom`：私董会式动态讨论，谁最适合谁发言，允许接话、追问、反驳和脑暴
- `critique`：让专家审稿、挑错、找漏项
- `red-team`：从失败、脆弱性、误判角度拆方案
- `synthesis`：先分视角，再合并为统一建议

模式细则见 [references/output-modes.md](references/output-modes.md)。

`boardroom` 是复杂问题的默认优先模式。除非用户明确要静态对照，否则多专家讨论优先用它。

同时结合决策阶段做默认路由：

- `explore`：优先 `boardroom` 或 `panel`
- `evaluate`：优先 `boardroom` 或 `synthesis`
- `choose`：优先 `boardroom`、`single` 或 `synthesis`
- `critique`：优先 `critique` 或 `red-team`
- `revise`：优先 `critique` 后接 `synthesis`

### 3. 选择专家

选择专家时，看“问题性质”而不是“名气大小”：

- 产品体验问题，优先产品与设计专家
- 商业决策问题，优先战略与管理专家
- 风险和不确定性问题，优先概率、风险和系统专家
- 教学、解释、理解问题，优先学习与认知专家
- 伦理和原则冲突问题，优先哲学与规范专家

如果用户点名专家，但明显不适配任务，可以保留该专家，同时补 1 位更适配的专家做校正，并明确说明原因。

优先使用“互补型”组合，而不是同质化组合：

- 一个负责打开视角
- 一个负责评估价值
- 一个负责查风险
- 一个可负责把模糊话题压成可决策的问题

如果没有明显互补关系，通常说明专家选多了。

私董会模式下，专家人数通常以 2-5 位为宜。3-4 位通常最自然。

### 4. 提取专家框架

从专家条目中只提取这几类信息：

- 核心镜头：他通常先看什么
- 常问问题：他会追问哪些关键点
- 最适场景：什么时候最好用
- 常见盲区：容易忽视什么

不要把整段专家介绍原样堆进回答。

如果问题很复杂，可以额外提取：

- 判断标准
- 默认偏好
- 典型反对意见
- 决策盲区

### 5. 生成分析

每位专家至少回答四件事：

1. 这个问题在他眼里最关键的矛盾是什么
2. 他会用什么标准判断好坏
3. 他会最先采取什么动作
4. 他会提醒什么风险或代价

如果是 `critique` 或 `red-team`，再额外回答：

5. 现有方案最脆弱的假设是什么
6. 最先暴露问题的预警信号是什么

如果是 `boardroom`，不要强迫每位专家都完整答完一遍。改用动态讨论：

1. 由最贴题的专家先开口。
2. 下一位专家只在有补充、分歧、追问或新方向时接话。
3. 允许出现“接上一个人的话继续推进”的自然发言。
4. 允许有人专门挑战假设，有人专门补可执行动作。
5. 当结论已经足够清楚时，不再为了平均发言继续拖长讨论。

### 6. 做收束

最终输出不能停在“谁说了什么”，而要完成收束：

- 哪些观点一致
- 哪些观点冲突
- 冲突的根因是什么
- 在当前约束下，最推荐哪条路径
- 下一步该做什么

如果无法强收束，就给“条件化结论”：

- 如果用户优先要速度，选 A
- 如果用户优先要稳健，选 B
- 如果用户优先要上限，先试 C，再加保护栏

如果是 `boardroom`，默认用下面这个停机条件：

- 主要分歧已经被压缩到 1-2 个关键条件
- 推荐路径已经形成
- 下一步动作已经清楚
- 再继续说只会重复，而不会新增有效信息

## 输出规则

默认输出自然语言；只有调用方明显需要机器可读结果时，再返回 JSON。

### 自然语言输出

普通模式下，优先使用下面这类结构：

1. 问题重述
2. 选用的专家与原因
3. 专家分析
4. 综合判断
5. 建议动作

如果是 `boardroom`，优先用这种结构：

1. 议题与背景
2. 私董会讨论摘要
3. 关键分歧
4. 最终结论
5. 下一步动作

必要时可以保留简短的发言片段，但不要写成冗长剧本。

默认不要省略“为什么选这些专家”。

如果用户是为了决策，建议附带：

- 不建议做什么
- 先验证什么
- 失败时看什么信号

### 机器可读输出

如果需要结构化结果，优先使用：

```json
{
  "mode": "boardroom",
  "selected_experts": [
    {
      "name": "Peter Drucker",
      "reason": "适合组织和目标澄清"
    }
  ],
  "problem_frame": {
    "goal": "",
    "constraints": [],
    "key_variables": [],
    "risks": [],
    "decision_stage": "",
    "time_horizon": ""
  },
  "discussion_flow": [
    {
      "speaker": "",
      "trigger": "opening|follow-up|challenge|brainstorm|risk|synthesis",
      "point": ""
    }
  ],
  "expert_views": [
    {
      "name": "",
      "core_judgment": "",
      "criteria": [],
      "recommended_action": "",
      "warnings": [],
      "blind_spots": []
    }
  ],
  "synthesis": "",
  "recommended_path": "",
  "next_actions": [],
  "confidence": "low|medium|high",
  "missing_information": []
}
```

不同交付物模板见 [references/deliverable-templates.md](references/deliverable-templates.md)。

## 动态专家

当专家库里没有该人物时：

1. 用公开可知的长期观点，构造一个“临时专家框架”。
2. 明确标记这是“基于公开资料提炼的动态专家画像”。
3. 只提炼稳定的思考习惯、判断标准和表达倾向。
4. 不编造语录，不硬凹口头禅，不假装知道其未公开观点。

临时专家框架至少包含：

- 领域定位
- 核心镜头
- 常问问题
- 最适场景
- 可能盲区

如果动态专家只是用户随口给的“某种大师型角色”，优先判断是否更适合改用真实专家组合。

## 默认偏好

- 单专家分析时，输出要短、准、能落地。
- 多专家模式时，专家人数尽量控制在 2-4 位。
- 除非用户明确想看戏剧化对话，否则不要写成长篇角色扮演对话。
- 如果问题本质上只是普通常识问答，不要强行套专家框架。
- 高风险问题默认补一个红队型专家。
- 高模糊问题默认补一个澄清型专家。
- 多专家复杂问题默认用 `boardroom`。
- 私董会模式要像真实会议，不像整齐排比作文。

高频任务默认路由：

- 方案选择：`boardroom` 或 `synthesis`
- 方案挑错：`critique`
- 上线前审查：`red-team`
- 产品方向：`boardroom`
- 文案表达：`single`、`compare` 或 `boardroom`
- 学习讲解：`single`
- 技能或提示词设计：`boardroom` 或 `critique` 后接 `synthesis`
- 工作流故障排查：`boardroom`、`critique` 或 `panel`

## 任务配方

遇到典型任务时，优先走固定配方：

- 产品方向：先价值，再体验，再取舍，再验证
- 商业战略：先目标，再位置，再优势，再代价
- 风险评审：先假设，再失败路径，再预警信号，再保护栏
- 学习解释：先讲明白，再找误解，再重建结构
- 文案或表达评审：先目标受众，再信息层次，再风格，再可读性

详细路线见 [references/task-recipes.md](references/task-recipes.md)。

高频直达表见 [references/high-frequency-use-cases.md](references/high-frequency-use-cases.md)。

常用调用句式见 [references/call-patterns.md](references/call-patterns.md)。

Skill / Prompt / Workflow 评审专用规则见 [references/skill-prompt-review.md](references/skill-prompt-review.md)。

成熟输出写法见 [references/output-style-templates.md](references/output-style-templates.md)。

## 质量检查

交付前检查：

- 选的专家是否真的适合这个问题
- 回答是否体现了“方法差异”而不是“空泛鸡汤”
- 是否明确说明了假设、约束和风险
- 是否给出了综合判断，而不只是专家观点拼盘
- 是否把风格模仿控制在不影响清晰度的范围内
- 是否把“接下来怎么做”说清楚了
- 如果结论不确定，是否明确写出了不确定性的来源

更细的反失真检查见 [references/quality-guardrails.md](references/quality-guardrails.md)。
