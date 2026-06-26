---
name: feishu-diagram-chooser
description: "Parse natural language descriptions and output diagram scheme recommendations. Use when user wants to create diagrams, charts, flowcharts, or visualize concepts. Supports Mermaid diagrams (flowchart, sequence, state, ER, class, Gantt, mindmap, timeline), data chart templates, and fallback to image prompts when no suitable diagram type exists. 触发词：图表, 流程图, 时序图, 状态图, ER图, 类图, 甘特图, 思维导图, 时间线, diagram, chart, flowchart, sequence, mermaid, 可视化, 画图, 图形"
available-agents:
  - DesignLite
---

# Feishu Diagram Chooser

Parse natural language descriptions and output structured diagram scheme recommendations.

---

## 0. 触发规则（何时使用本 Skill）

### 0.1 正向触发（应当调用）

当用户的需求满足以下任意条件时，应调用本 Skill：

1. **明确提出要“画图/做图表/可视化”**
   - 示例：
     - 「帮我画一个登录流程图」
     - 「把这个系统架构画出来」
     - 「做个 ER 图/时序图/甘特图」
     - 「把这段业务流程可视化一下」

2. **命中图相关关键词 + 行为词**
   - 图相关关键词（任意一个）：
     - 中文：图表、流程图、时序图、状态图、ER 图、类图、甘特图、思维导图、时间线、架构图、组织结构图
     - 英文：diagram, chart, flowchart, sequence, mermaid
     - 泛词：可视化、画图、图形
   - 行为关键词（至少一个）：
     - 画、生成、做一个、做成、转换成、可视化、展示成、画成

   规则：**(图相关词) AND (行为词)** → 强触发。

3. **上下文已经在“改一张图”，继续编辑**
   - 上几轮已经使用本 Skill 生成了图，本轮用户说：
     - 「再加一个审批节点」
     - 「在中间插一个网关」
     - 「把数据库拆成两个表」
   - 默认继续调用本 Skill，对已有图进行扩展或重构。

### 0.2 负向触发（不应调用）

即使命中图相关词，但属于以下情况时，不调用本 Skill，而是走普通文本回答：

- 用户只是想**理解/评价现有图**：
  - 「帮我解释一下这个 ER 图」
  - 「帮我点评这张架构图」
  - 「这个流程图有没有问题？」
- 用户明确表示**不需要画图**：
  - 「不用画流程图，用文字说明就行」
- 用户要求**禁止使用某类图/某种工具**：
  - 「不要用 Mermaid，只要文字」
  - 「不要用任何图表」

在这些情况下，Skill 只应在用户之后再次明确提出“要画图”时才重新触发。

---

## 1. 输入参数

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `description` | string | Yes | Natural language description of what the user wants to visualize |
| `context` | object | No | Additional context including data structure, style preference, output format constraints |
| `context.dataFormat` | string | No | Data format hint: `structured`, `unstructured`, `relational`, `time-series`, `hierarchical` |
| `context.styleHint` | string | No | Visual style preference: `formal`, `casual`, `colorful`, `minimal`, `technical` |
| `context.constraints` | object | No | Constraints like `maxNodes`, `maxDepth`, `hasTimeDimension`, `mermaidVersion`, `allowedDiagramTypes`, `echartsSupported` |
| `context.constraints.mermaidVersion` | string | No | Mermaid version in use, e.g. `"10.0.0"`, `"10.5.0"` |
| `context.constraints.allowedDiagramTypes` | string[] | No | Whitelist of allowed diagram subtypes, e.g. `["flowchart", "sequenceDiagram", "classDiagram"]` |
| `context.constraints.echartsSupported` | boolean | No | Whether ECharts-based data charts can be rendered in the current environment |
| `context.constraints.maxNodes` | number | No | Estimated maximum comfortable node count for diagram (for complexity control) |

---

## 2. 输出 Schema

```typescript
interface DiagramScheme {
  // Primary recommendation
  primary: {
    type: 'mermaid' | 'echarts' | 'image';
    subtype: string;           // Specific diagram subtype
    reasoning: string;         // Why this type is recommended
    mermaidCode?: string;      // Generated Mermaid code (if type='mermaid')
    chartConfig?: object;      // ECharts option config (if type='echarts')
    imagePrompt?: string;      // Image generation prompt (if type='image')
  };

  // Alternative options, ordered by preference (descending)
  alternatives: Array<{
    type: 'mermaid' | 'echarts' | 'image';
    subtype: string;
    reasoning: string;
    score?: number;            // Optional relative score (0-1), primary is highest
  }>;

  // Confidence score 0-1 for primary choice
  confidence: number;

  // When classification is ambiguous or confidence < 0.6, provide clarification questions
  clarificationNeeded?: string[];
}
```

约定：`alternatives` 按推荐优先级排序，前面的方案优于后面的方案。

---

## 3. 决策逻辑

### 3.1 Intent Classification（意图分类）

分析 `description`，分类可视化意图：

| Intent Category | Keywords | Data Characteristics |
|-----------------|----------|---------------------|
| **Process** | 流程, 步骤, 怎么做, process, workflow, step, how-to | Sequential actions with decisions |
| **Relationship** | 关系, 连接, 依赖, relation, dependency, connect | Entities and their connections |
| **Hierarchy** | 结构, 组织, 层级, hierarchy, structure, org | Parent-child relationships |
| **Time-based** | 时间, 进度, 计划, 时间线, timeline, schedule, Gantt, 里程碑 | Temporal sequences or durations |
| **Comparison** | 对比, 比较, 排名, compare, rank, vs | Multiple items for comparison |
| **Distribution** | 分布, 占比, 比例, distribution, percentage, ratio | Part-to-whole relationships |
| **State** | 状态, 变化, 转换, 生命周期, state, status, transition | State machines or lifecycle |
| **Architecture** | 架构, 系统, 模块, 组件, architecture, system, module | Component relationships |
| **Journey/UX** | 用户旅程, 体验路径, journey, funnel | User journey, experience flows |

若描述同时出现多种意图（如既有流程又有架构、又有数据），应：

- 降低 `confidence`
- 优先生成 `clarificationNeeded`，询问用户关注的主视角

示例澄清问题：

- 「你更想重点展示：1）流程步骤 2）系统组件关系 3）数据趋势，哪一个？」
- 「时间线和流程图你更想要哪种表现形式？」

### 3.2 Mermaid Type Mapping（结构图映射）

在满足以下条件时，优先使用 Mermaid：

- 环境支持 Mermaid（默认 true）
- `context.constraints.allowedDiagramTypes` 未显式禁用对应子类型
- 或 ECharts 不可用（见 3.3 中兜底逻辑）

映射表：

| Diagram Type | Subtype | Best For | Syntax Version | Notes |
|--------------|---------|----------|----------------|-------|
| **Flowchart** | `flowchart TD` / `flowchart LR` | Process, workflow, decision trees | 10.0+ | 默认方向 TD，节点 > `maxNodes` 时考虑拆分或改用其他图 |
| **Sequence** | `sequenceDiagram` | Interaction between actors, API calls | 10.0+ | 多角色交互优先选择 |
| **State** | `stateDiagram-v2` | State machines, status transitions | 10.0+ | 生命周期、状态流转 |
| **ER** | `erDiagram` | Database schema, entity relationships | 10.0+ | 仅用于“实体-字段-关系”的场景 |
| **Class** | `classDiagram` | OOP class structures, inheritance | 10.0+ | 用于类/接口结构 |
| **Gantt** | `gantt` | Project schedules, timelines with tasks | 10.0+ | 含任务、阶段、起止日期 |
| **Mindmap** | `mindmap` | Hierarchical thinking, brainstorming | 10.5+ (experimental) | 仅在 `mermaidVersion >= 10.5` 且未被禁用时推荐 |
| **Timeline** | `timeline` | Chronological events, history | 10.5+ (experimental) | 同上，适用于历史事件/里程碑 |
| **Gitgraph** | `gitGraph` | Git branch history, version control | 10.0+ | 代码分支场景专用 |
| **User Journey** | `journey` | User experience flows | 10.0+ | 用户旅程/漏斗型体验 |
| **C4Context** | `C4Context`, `C4Container` | System architecture (C4 model) | 10.0+ | 复杂架构时可选，若环境不支持则降级为 flowchart/classDiagram |

**版本约束：**

- 当 `context.constraints.mermaidVersion` 存在时：
  - 若 `< 10.5`，不推荐 `mindmap` / `timeline`
  - 若某 subtype 不在 `allowedDiagramTypes` 中，也不推荐

---

### 3.3 Data Chart Mapping（数据图映射 & 兜底策略）

当描述明显指向“数据可视化”时，先尝试 ECharts：

| Intent | Chart Type | Library | 注意点 |
|--------|------------|---------|--------|
| Trend over time | Line, Area | ECharts | 类别较多时优先 line；时间维度清晰 |
| Category comparison | Bar (vertical/horizontal) | ECharts | 类别数 > 10 时谨慎使用饼图 |
| Part-to-whole | Pie, Donut, Treemap | ECharts | 类别数 ≤ 8 更适合 Pie/Donut |
| Multi-variable comparison | Radar, Parallel | ECharts | 维度数 ≤ 6 更可读 |
| Correlation | Scatter, Heatmap | ECharts | 连续变量之间关系 |
| Geographic | Map | ECharts | 需要地理维度 |
| Flow/Conversion | Sankey, Funnel | ECharts | 流转关系/转化漏斗 |
| Text frequency | WordCloud | ECharts + echarts-wordcloud | 文本频次、标签云 |

#### ✳ ECharts 不可视化时的兜底链路

当满足以下任一条件时，**不要输出 `type='echarts'` 作为 primary**，而是执行分级兜底：

- `context.constraints.echartsSupported === false`
- 当前运行环境无法渲染 ECharts（由上层 Agent 判定后传入）
- 上下文明确指出「无法使用 ECharts」或「当前环境不支持图表渲染」

**兜底顺序：**

1. **尝试用 Mermaid 图近似表达数据关系**（结构化代替可视化图表）
   - 例如：
     - 数据流/转化 → `flowchart` / `journey` / `sankey-like` 流程图
     - 类别对比 → 用 `flowchart` 列出节点 + 简要文字标注
     - 时间趋势 → `timeline` / `gantt`（若版本支持），或用 flowchart 线性列出关键时间点
   - 此时：
     - `primary.type = 'mermaid'`
     - `primary.reasoning` 中要明确说明：“因为当前环境无法渲染 ECharts，改用 Mermaid 结构图近似展示关键关系”。

2. **若 Mermaid 也不适合表达（纯统计图需求，结构化表达会严重失真）**  
   则退而求其次使用图片生成：

   - `primary.type = 'image'`
   - `primary.subtype = 'ai-generated'`
   - 通过数据描述 + styleHint 构造 `imagePrompt`

3. ECharts 在任何情况下**可以作为 `alternatives`** 出现在返回结果中，以便在其他环境下渲染：
   - 例如：
     ```jsonc
     {
       "primary": { "type": "mermaid", ... },
       "alternatives": [
         {
           "type": "echarts",
           "subtype": "bar",
           "reasoning": "在支持 ECharts 的环境中，这种图表能更好呈现数据对比",
           "score": 0.8
         }
       ]
     }
     ```

---

### 3.4 Fallback Strategy（通用兜底）

当无法确定合适的结构图或者数据图（`confidence < 0.6` 且意图仍不清晰）：

1. **尝试生成 Mermaid 的高层结构草图**  
   - 使用 `flowchart` 或 `mindmap`（若支持）粗略表达要素和关系
   - 若仍然感觉强行结构化会误导用户 → 放弃结构图

2. **生成图片描述（Image Prompt）作为最终兜底**

```typescript
function generateImagePrompt(description: string, style: string): string {
  const base = "Professional technical illustration";
  const styleModifiers = {
    formal: "clean corporate style, blue and gray color scheme",
    casual: "friendly hand-drawn style, warm colors",
    colorful: "vibrant modern design, multiple accent colors",
    minimal: "minimalist line art, monochromatic",
    technical: "detailed engineering diagram, precise annotations"
  };

  return `${base}. ${description}. ${styleModifiers[style] || styleModifiers.formal}. 
    No text, no labels, purely visual representation. 
    White background, high contrast.`;
}
```

3. 提供 `clarificationNeeded`，引导用户收窄需求视角：
   - 「你更关注时间演进、结构关系还是数据对比？」
   - 「这张图是用来沟通给非技术同学，还是技术设计评审？」

---

## 4. Mermaid 代码生成规范（质量与兼容性）

为减少渲染失败，生成 Mermaid 代码时遵守：

1. **节点 ID 使用英文与数字，不含空格和中文**：
   - 用 `node_login`, `node_approve1` 这类 ID
   - 中文展示放在方括号/圆括号内容中，例如：`node_login[用户登录]`

2. **中文标签统一包在节点文本中**：
   - `A[用户输入账号密码]`
   - 避免在 ID 中直接使用中文或特殊字符

3. **特殊字符转义和注释**：
   - 避免在标签中包含 `:`, `{`, `}` 等影响语法的字符，必要时用文本描述替代
   - 顶部可添加注释：`%% auto-generated by feishu-diagram-chooser`

4. **复杂图建议分组 / section**（尤其是 Gantt、journey 等）

---

## 5. Quality Checklist

- [ ] 触发场景正确（未误触解释型需求）
- [ ] 意图正确分类，并处理多意图混合（必要时给出澄清问题）
- [ ] 推荐类型符合环境约束（版本、allowedDiagramTypes、echartsSupported）
- [ ] Mermaid 类型与版本兼容（mindmap/timeline 仅在支持时使用）
- [ ] ECharts 环境不支持时，已优先切换到 Mermaid，再退回图片
- [ ] Mermaid 语法合法，节点命名规范，可渲染
- [ ] ECharts 配置是模板化的，可由上层填充真实数据
- [ ] `alternatives` 有清晰的优先级/评分，理由明确
- [ ] 输出符合 Schema（primary/alternatives/confidence/clarificationNeeded）

---

## 6. 触发示例（正例 / 反例）

### 6.1 正例：应该调用本 Skill

1. **明确要画流程图**
   - 用户输入：
     > 帮我画一个用户登录的流程图，包含密码错误三次锁定账号
   - 结果：
     - 命中「画」「流程图」→ 触发
     - Intent = Process → 推荐 `flowchart TD`

2. **数据对比可视化，环境支持 ECharts**
   - 用户输入：
     > 想做一个柱状图，对比今年各产品线的销售额
   - 上下文：`echartsSupported = true`
   - 结果：
     - Intent = Comparison → 推荐 `echarts` + `bar`

3. **时间线展示历史事件**
   - 用户输入：
     > 帮我把公司这五年的大事件画成一条时间线
   - 上下文：`mermaidVersion >= 10.5`
   - 结果：
     - Intent = Time-based → 推荐 `timeline`

4. **在已有图基础上继续修改**
   - 上一轮已用本 Skill 输出登录流程图
   - 本轮输入：
     > 在登录失败后加一个验证码步骤
   - 结果：
     - 识别为对现有图的增量修改 → 继续用本 Skill 更新 Mermaid

### 6.2 反例：不应该调用本 Skill

1. **只是解释已有图**
   - 用户输入：
     > 帮我解释一下这张 ER 图每个字段的含义
   - 结果：
     - 虽然有「ER 图」，但没有「画/生成/可视化」等行为词
     - 不触发本 Skill，用普通文本解释

2. **明确不要画图**
   - 用户输入：
     > 不用画流程图，你直接用文字帮我描述登录过程就行
   - 结果：
     - 包含「流程图」，但与否定意图绑定
     - 不触发本 Skill

3. **禁止使用某种图形工具**
   - 用户输入：
     > 不要用 Mermaid 帮我画图，你直接给一个文字版的接口调用顺序
   - 结果：
     - 明确禁止 Mermaid
     - 不调用本 Skill；除非后续用户再次主动提出要画图

4. **仅想要概念说明**
   - 用户输入：
     > ER 图和类图有什么区别，给我讲一下
   - 结果：
     - 只是知识问答，不是生成新图
     - 不调用本 Skill
