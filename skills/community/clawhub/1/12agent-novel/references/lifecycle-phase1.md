# Phase 1 — 前期架构

> OpenClaw Skill "12agent-novel" 生命周期 Phase 1 详细流程文档

> 下文出现的 `read()`、`readConfig()`、`sessions_spawn()` 等代码块均为**示意性伪代码**，用于说明调度逻辑与输入拼装方式，不代表宿主环境必须提供同名 API。

## 前置条件

- Phase 0 已完成，用户已确认项目设定。
- 项目目录 `projects/<项目名>/` 已建立。
- `meta/metadata.json.project.phase` 已更新为 `1`。
- `meta/workflow-state.json.phaseState.currentPhase` 已更新为 `1`。
- `meta/config.md` 中模型分配已确定。
- `meta/style-anchor.md` v0.1 基础偏好已初始化。

---

## Step 1-1：世界观构建

**调用 Worldbuilder Agent** → 输出完整世界观文档

### 流程

1. Coordinator 读取 `references/agent-worldbuilder.md` 获取 Agent prompt。
2. 读取 `meta/project.md` 获取项目基本信息和用户授权边界。
3. 通过 `sessions_spawn` 调用 Worldbuilder Agent。
4. 接收输出，写入 `worldbuilding/world.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-worldbuilder.md")}

【本次任务】
根据以下项目信息，构建完整的世界观文档。

【项目信息】
${read("meta/project.md")}

【用户授权边界】
${authBoundary}

【输出要求】
请输出完整的世界观文档，必须包含以下三大板块：
1. 基础世界框架
2. 核心规则体系
3. 核心悬念/禁忌`,
  label: "worldbuilder",
  model: readConfig("meta/config.md", "worldbuilder"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 输出规范 — worldbuilding/world.md

文档必须包含以下三大板块：

#### 1. 基础世界框架

| 条目 | 说明 |
|------|------|
| 世界名称 | 正式名称 + 别称 |
| 时代背景 | 历史纪元、当前时代特征 |
| 地理格局 | 大陆/区域划分、关键地标、气候特征 |
| 社会结构 | 阶层体系、治理方式、文化习俗 |
| 势力格局 | 主要势力（≥3 个）、势力关系、利益冲突 |

#### 2. 核心规则体系

| 条目 | 说明 |
|------|------|
| 力量体系 | 等级划分（名称 + 数量）、晋升条件 |
| 能力边界 | 每个等级的能力上限、不可逾越的天花板 |
| 代价机制 | 使用力量的代价、副作用、禁忌 |
| 特殊机制 | 世界独有的规则（如：契约、血脉、禁术等） |

#### 3. 核心悬念/禁忌

| 条目 | 说明 |
|------|------|
| 世界观禁忌 | 不可触碰的领域、被封印的知识 |
| 隐藏势力 | 暗中运作的组织/个体 |
| 终极谜题 | 贯穿全书的核心悬念（≥1 个） |

---

## Step 1-2：角色圣经

**调用 CharacterDesigner Agent** → 输出角色档案

### 流程

1. Coordinator 读取 `references/agent-character-designer.md` 获取 Agent prompt。
2. 读取 `worldbuilding/world.md`（Step 1-1 产出）+ 用户角色描述。
3. 通过 `sessions_spawn` 调用 CharacterDesigner Agent。
4. 接收输出，分别写入 `characters/protagonist.md` 和 `characters/characters.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-character-designer.md")}

【本次任务】
根据世界观文档和用户角色描述，设计完整的角色体系。

【世界观文档】
${read("worldbuilding/world.md")}

【用户角色描述】
${userCharacterDescription}

【项目信息】
${read("meta/project.md")}

【输出要求】
请分别输出：
1. 主角详细档案（protagonist.md）
2. 全角色圣经（characters.md），包含关系网和反派设计`,
  label: "character-designer",
  model: readConfig("meta/config.md", "characterDesigner"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 输出规范 — characters/protagonist.md

**主角档案必须包含：**

| 模块 | 内容要求 |
|------|---------|
| 外貌特征 | 具体到可辨识细节（身高、体型、标志性特征、常见穿着） |
| 性格剖析 | 核心矛盾、心理动机、行为模式、情绪触发点 |
| **MBTI 类型** | 标注 MBTI 类型 + 2-3 句说明该类型在本角色身上的具体体现 |
| Backstory | 必须与世界观设定契合，关键人生节点、创伤事件 |
| 人物弧光 | 起点状态 → 核心摩擦 → 内在转变 → 终点状态 |
| 能力/修为设定 | 符合世界观力量体系，初始等级、成长路线、独特能力 |
| 核心目标/恐惧/执念 | 三项各一句，作为 OOC 守护的行为基准 |
| **Signature 标签** | 3-5 个角色专属标签（如：#逆境韧性 #隐忍型强者 #情感钝感力），用于快速定位人设核心 |
| 语言风格 | 口头禅、句式偏好、对话特点（供 OOCGuardian 比对） |

### 输出规范 — characters/characters.md

**关系网（至少 8 个角色）：**

| 关系类型 | 数量 | 说明 |
|---------|------|------|
| 亲人 | 2-3 人 | 血缘/养育关系，对主角性格的塑造作用 |
| 仇人 | 2 人 | 与主角的核心矛盾，仇恨来源 |
| 暧昧/情感线 | 2 人 | 情感发展节奏，对主线的影响 |
| 恩人/导师 | 1 人 | 对主角成长的关键作用 |
| 对手/盟友 | 2 人 | 竞争或合作关系，推动剧情 |

**反派设计要求：**

每个核心反派必须具备：

| 条目 | 说明 |
|------|------|
| 目的 | 明确的行动目标（不能是"纯粹的恶"） |
| 优势 | 资源、能力、地位上的优势 |
| 弱点 | 性格缺陷、认知盲区、情感软肋 |
| 感情线 | 与某角色的情感羁绊（亲情/友情/扭曲的爱） |
| 势力归属 | 必须与世界观中的势力格局对应 |

---

## Step 1-3：全书大纲

**调用 OutlinePlanner Agent** → 输出全书大纲

### 流程

1. Coordinator 读取 `references/agent-outline-planner.md` 获取 Agent prompt。
2. 读取世界观 + 角色圣经。
3. 通过 `sessions_spawn` 调用 OutlinePlanner Agent。
4. 接收输出，写入 `outline/outline.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-outline-planner.md")}

【本次任务】
根据世界观和角色圣经，制定全书大纲。

【世界观文档】
${read("worldbuilding/world.md")}

【角色圣经】
${read("characters/protagonist.md")}
${read("characters/characters.md")}

【项目信息】
${read("meta/project.md")}

【输出要求】
请输出完整的全书大纲，必须包含：
1. 三幕结构总览
2. 主线 + 支线列表
3. 5-7 个核心转折点
4. 结局走向`,
  label: "outline-planner",
  model: readConfig("meta/config.md", "outlinePlanner"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 输出规范 — outline/outline.md

| 模块 | 内容要求 |
|------|---------|
| 三幕结构总览 | 第一幕（建置）、第二幕（对抗）、第三幕（解决）的起止章节和核心目标 |
| 主线剧情 | 贯穿全书的核心故事线，按幕划分关键节点 |
| 支线列表 | 每条支线的起止章节范围、与主线的交叉点、承担的功能 |
| 核心转折点 | 5-7 个关键转折，每个标注所在章节、涉及角色、对主线的影响 |
| 结局走向 | 主线结局 + 各支线收束方式 + 开放性悬念（如有） |

---

## Step 1-4：章节细纲

**调用 ChapterOutliner Agent** → 输出章节细纲

### 批次规则

- **单批次最多 10 章**，完成后可继续下一批。
- 批次间 Coordinator 检查一致性后再启动下一批。
- 所有批次完成后合并为完整的 `outline/chapter-outline.md`。

### 流程

1. Coordinator 读取 `references/agent-chapter-outliner.md` 获取 Agent prompt。
2. 读取世界观 + 角色圣经 + 大纲。
3. 按批次通过 `sessions_spawn` 调用 ChapterOutliner Agent。
4. 接收输出，追加写入 `outline/chapter-outline.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-chapter-outliner.md")}

【本次任务】
根据世界观、角色圣经和全书大纲，编写第 ${batchStart} 至第 ${batchEnd} 章的章节细纲。

【世界观文档】
${read("worldbuilding/world.md")}

【角色圣经】
${read("characters/protagonist.md")}
${read("characters/characters.md")}

【全书大纲】
${read("outline/outline.md")}

${previousChapterOutlines ? `【已完成的章节细纲（前序批次）】\n${previousChapterOutlines}` : ""}

【输出要求】
请按模板输出每一章的细纲。`,
  label: "chapter-outliner",
  model: readConfig("meta/config.md", "chapterOutliner"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 单章细纲模板

```markdown
## 第 X 章：{{章节标题}}

- **章节类型：** 日常/战斗/过渡/高潮/收束
- **核心事件：** 本章发生的关键事件（1-2 句）
- **主线推进：** 主线剧情在本章的进展
- **情感线：** 情感关系的变化（如有）
- **冲突/转折：** 本章的核心矛盾或转折点
- **节奏点：** 紧张/舒缓/爆发 — 节奏定位
- **结尾钩子：** 章末悬念或引导读者继续阅读的钩子
- **伏笔承接：**
  - 承接伏笔：从第 X 章继承的伏笔（如有）
  - 埋设伏笔：本章新埋设的伏笔（如有）
- **出场角色：** 本章登场的角色列表
- **预估字数：** {{word_count}} 字
```

---

## Step 1-5：全局一致性终审

**调用 FinalReviewer Agent** → 输出终审报告

### 流程

1. Coordinator 读取 `references/agent-final-reviewer.md` 获取 Agent prompt。
2. 汇总所有前序产出文档。
3. 通过 `sessions_spawn` 调用 FinalReviewer Agent。
4. 接收终审报告，写入 `archive/phase1-review.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-final-reviewer.md")}

【本次任务】
对 Phase 1 产出的所有文档进行全局一致性终审。

【世界观文档】
${read("worldbuilding/world.md")}

【角色圣经】
${read("characters/protagonist.md")}
${read("characters/characters.md")}

【全书大纲】
${read("outline/outline.md")}

【章节细纲】
${read("outline/chapter-outline.md")}

【检查项】
请逐项检查以下一致性维度，发现问题需明确指出位置和修改建议：
1. 角色能力与力量体系一致性
2. 社会背景与世界设定一致性
3. 关键事件基于势力格局的合理性
4. 细纲遵循大纲结构
5. 伏笔与悬念呼应完整性`,
  label: "final-reviewer",
  model: readConfig("meta/config.md", "finalReviewer"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 检查维度详细说明

| 检查项 | 说明 | 严重等级 |
|--------|------|---------|
| 角色能力 vs 力量体系 | 角色在细纲中展现的能力是否超出其当前等级上限 | 🔴 Critical |
| 社会背景 vs 世界设定 | 社会制度、文化习俗在剧情中是否前后一致 | 🔴 Critical |
| 关键事件 vs 势力格局 | 重大事件的发生是否有势力基础支撑 | 🟡 Warning |
| 细纲 vs 大纲结构 | 章节细纲是否遵循大纲的三幕结构和转折点安排 | 🔴 Critical |
| 伏笔与悬念呼应 | 埋设的伏笔是否有对应的回收章节，悬念是否有解答 | 🟡 Warning |

---

## Step 1-6：Coordinator 提取关键章节配置

> 此步骤由 Coordinator 自身执行，不调用子 Agent。

### 流程

1. 读取 `outline/outline.md`，提取三幕结构的幕间分界章节。
2. 识别核心转折点所在的章节编号。
3. 更新 `meta/config.md` 的 `key_chapters` 和 `act_boundaries` 字段。

### 更新内容示例

```markdown
## key_chapters
- 第 1 章：开篇（重点审校）
- 第 12 章：第一幕高潮（重点审校）
- 第 13 章：第二幕开启（重点审校）
- 第 25 章：中点转折（重点审校）
- 第 38 章：第二幕高潮（重点审校）
- 第 39 章：第三幕开启（重点审校）
- 第 50 章：大结局（重点审校）

## act_boundaries
- act_1_end: 12
- act_2_start: 13
- act_2_midpoint: 25
- act_2_end: 38
- act_3_start: 39
```

**用途：** 关键章节在 Phase 2 写作时将启用额外审校流程（OOCGuardian + FinalReviewer 双重检查）。

---

## Step 1-6.5：预选文风

**调用 MainWriter Agent** → 输出 5 种候选文风样本 → 用户选择

### 概述

在正式生成风格锚定之前，让用户从 5 种候选文风中选择最喜欢的风格，作为 Step 1-7 StyleAnchorGenerator 的输入参考。

### 流程

1. Coordinator 读取 `references/agent-main-writer.md` 获取 Agent prompt。
2. 读取世界观 + 角色圣经 + 大纲 + `meta/style-anchor.md` v0.1 基础偏好。
3. 通过 `sessions_spawn` 调用 MainWriter Agent，生成 5 种不同文风的样本。
4. 向用户展示 5 个候选样本，等待用户选择。
5. 用户选择后，将选中样本写入 `meta/selected-style-sample.md`。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-main-writer.md")}

【本次任务】
根据项目的世界观、角色和大纲，生成 5 种不同文风的候选样本，供用户选择。

【世界观文档】
${read("worldbuilding/world.md")}

【角色圣经】
${read("characters/protagonist.md")}
${read("characters/characters.md")}

【全书大纲】
${read("outline/outline.md")}

【风格锚定 v0.1（基础偏好）】
${read("meta/style-anchor.md")}

【输出要求】
请生成 5 种不同文风的描写样本，每种约 400 字，涵盖以下场景之一（由系统指定）：
- 样本1：角色初登场场景
- 样本2：战斗/冲突场景
- 样本3：情感/对话场景
- 样本4：环境/氛围描写
- 样本5：内心独白/反思场景

每种文风需标注：
- **文风名称**：（如「古风雅韵」「快节奏爽文」「电影感描写」等）
- **风格特点**：（2-3 句话描述该文风的核心特征）
- **400字正文**：完整的一段描写

【文风多样性要求】
5 种样本之间必须有明显差异，差异体现在：
- 句式长短（短句密集 vs 长句铺陈）
- 描写密度（简洁干练 vs 浓墨重彩）
- 视角切换（固定视角 vs 多元视角）
- 节奏倾向（快节奏推进 vs 慢节奏渲染）
- 感官侧重（视觉为主 vs 多感官交织）`,
  label: "style-preview",
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run"
})
```

### 用户选择与后续处理

向用户展示 5 个样本后，等待用户响应：
- 用户输入 **1-5** → 记录对应样本为选定文风
- 用户输入 **"全部不要"** → 重新生成 5 种新样本
- 用户输入 **"混合" + 具体描述** → 记录混合需求，在风格锚定生成时体现

选定后，将选中样本写入 `meta/selected-style-sample.md`，进入 Step 1-6.8。

---

## Step 1-6.8：风格参考研究（新增）

**调用风格研究 Agent** → 基于小说设定分析知名平台类似作品 → 生成风格参考报告

### 概述

在正式生成风格锚定文档之前，先根据项目设定研究知名小说平台的类似作品，分析市场成熟文风，为用户提供更具参考价值的风格选择依据。

### 流程

1. Coordinator 根据项目设定确定相关平台（如：晋江、起点、长佩、番茄等）
2. 分析项目核心标签（兽人/BL/魂穿/悬疑/魔幻/治愈）
3. 调用风格研究 Agent，生成风格参考报告
4. 将报告作为 Step 1-7 的输入参考

### 平台选择依据

| 平台 | 适合类型 | 风格特点 |
|------|----------|----------|
| **晋江文学城** | BL、情感向、细腻描写 | 文风细腻，情感刻画深入，注重人物内心 |
| **长佩文学** | BL、小众题材、文学性 | 风格多样，允许实验性写法，文学性强 |
| **起点中文网** | 玄幻、悬疑、世界观宏大 | 节奏明快，设定严谨，注重剧情推进 |
| **番茄小说** | 快节奏、爽文、新媒体风 | 短句密集，节奏快，对话占比高 |
| **豆瓣阅读** | 文学性、实验性、深度探索 | 风格独特，注重语言质感和主题深度 |

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `你是一个小说风格研究专家。请根据以下项目设定，分析知名小说平台的类似作品风格。

【项目设定】
标题：《阙野寄魂记》
类型：兽人 / BL / 魂穿 / 悬疑 / 魔幻 / 治愈
基调：治愈，开放式结局
核心标签：兽人、BL、魂穿、悬疑、魔幻、治愈

【研究要求】
1. 分析以下平台中类似题材作品的典型文风：
   - 晋江文学城（BL+玄幻类）
   - 长佩文学（兽人/BL类）
   - 起点中文网（悬疑+玄幻类）
   - 番茄小说（快节奏+情感类）

2. 针对每个平台，提供：
   - 典型文风特点（句式、节奏、描写密度等）
   - 代表作品风格分析（1-2部类似题材作品）
   - 该平台读者偏好分析
   - 对《阙野寄魂记》的适配建议

3. 综合推荐 2-3 种适合本项目的混合风格方案

【输出格式】
## 风格参考研究报告

### 一、平台风格分析
#### 1. 晋江文学城
- 典型文风：...
- 代表作品分析：...
- 读者偏好：...
- 适配建议：...

#### 2. 长佩文学
- 典型文风：...
- 代表作品分析：...
- 读者偏好：...
- 适配建议：...

（以此类推）

### 二、风格混合方案推荐
#### 方案一：晋江细腻 + 起点节奏
- 特点：...
- 适用场景：...
- 实现要点：...

#### 方案二：长佩文学性 + 番茄对话感
- 特点：...
- 适用场景：...
- 实现要点：...

#### 方案三：综合平衡方案
- 特点：...
- 适用场景：...
- 实现要点：...

### 三、具体写作建议
1. 句式建议：...
2. 节奏控制：...
3. 描写重点：...
4. 对话风格：...
5. 避坑指南：...`,
  label: "style-research",
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### 后续处理

1. 接收风格参考研究报告
2. 将报告保存为 `references/style-research-report.md`
3. 向用户展示核心发现
4. 询问用户是否基于报告调整风格偏好
5. 进入 Step 1-7，并将研究报告作为额外输入

---

## Step 1-7：风格锚定文档定稿

**调用 StyleAnchorGenerator Agent** → 将 `meta/style-anchor.md` 从 v0.1 升级为 v1.0

### 流程

1. Coordinator 读取 `references/agent-style-anchor-generator.md` 获取 Agent prompt。
2. 读取世界观 + 角色圣经 + 大纲 + style-anchor.md v0.1 基础偏好 + `meta/selected-style-sample.md`（若存在）。
3. 通过 `sessions_spawn` 调用 StyleAnchorGenerator Agent。
4. 接收输出，覆写 `meta/style-anchor.md`（版本升至 v1.0）。

### sessions_spawn 调用

```javascript
sessions_spawn({
  task: `${read("references/agent-style-anchor-generator.md")}

【本次任务】
基于项目的世界观、角色和大纲，将风格锚定文档从 v0.1 升级为 v1.0 正式版。

【世界观文档】
${read("worldbuilding/world.md")}

【角色圣经】
${read("characters/protagonist.md")}
${read("characters/characters.md")}

【全书大纲】
${read("outline/outline.md")}

【风格锚定 v0.1（基础偏好）】
${read("meta/style-anchor.md")}

${read("meta/selected-style-sample.md")}

【风格参考研究报告】
${read("references/style-research-report.md")}

【输出要求】
请在 v0.1 基础偏好之上，补充以下内容，形成 v1.0 正式版：
1. 风格示范文本（至少 3 段不同场景的示范）
2. 叙事节奏模板（日常/战斗/情感场景的节奏模式）
3. 角色语言特征（每个主要角色的对话风格指纹）
4. 禁用词/禁用表达完善
5. 感官描写具体化（不同场景的感官侧重）`,
  label: "style-anchor-generator",
  model: readConfig("meta/config.md", "styleAnchorGenerator"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

### v1.0 新增内容

| 模块 | 说明 |
|------|------|
| 风格示范文本 | 至少 3 段（日常场景、战斗场景、情感场景），每段 200-500 字 |
| 叙事节奏模板 | 不同章节类型的节奏曲线（句长变化、段落密度、对话/叙述比例） |
| 角色语言特征 | 每个主要角色的口头禅、句式偏好、用词层次 |
| 禁用词/禁用表达 | 具体的禁用词列表 + 替代建议 |
| 感官描写具体化 | 按场景类型列出感官描写的优先级和具体手法 |

> **重要：** 风格锚定文档 v1.0 生成后，所有写作 Agent（MainWriter、BattleAgent）的 prompt **必须严格附带全文**。这是保证全书风格一致性的核心机制。

---

## Step 1-8：整合定稿

> 此步骤由 Coordinator 自身执行。

### 流程

1. 读取 `archive/phase1-review.md`（Step 1-5 的终审报告）。
2. 对于标记为 🔴 Critical 的问题，逐一修改对应文档。
3. 对于标记为 🟡 Warning 的问题，评估是否需要修改，记录处理结果。
4. 所有修改完成后，将各文档标记为 v1.0（架构定稿）。

### 修改流程

```
终审报告
    │
    ├── 🔴 Critical 问题 → 必须修改
    │   ├── 涉及世界观 → 修改 worldbuilding/world.md
    │   ├── 涉及角色 → 修改 characters/*.md
    │   ├── 涉及大纲 → 修改 outline/outline.md
    │   └── 涉及细纲 → 修改 outline/chapter-outline.md
    │
    ├── 🟡 Warning 问题 → 评估后决定
    │   ├── 需要修改 → 同上
    │   └── 可接受 → 记录理由
    │
    └── 生成修改日志 → archive/phase1-revision-log.md
```

### 定稿版本

修改完成后，必须同时更新 `meta/metadata.json` 与 `meta/workflow-state.json`。

`meta/metadata.json`：

```json
{
  "phase": 1,
  "version": "1.0.0",
  "architecture_finalized": true,
  "finalized_at": "{{ISO_timestamp}}"
}
```

`meta/workflow-state.json`：

```json
{
  "phaseState": {
    "currentPhase": 1,
    "status": "phase1_finalized",
    "architectureFinalized": true,
    "lastTransitionAt": "{{ISO_timestamp}}"
  }
}
```

---

## Step 1-9：汇报进入 Phase 2

### 展示内容

Coordinator 向用户展示 Phase 1 完成的所有文档：

```
✅ Phase 1（前期架构）完成！

📄 产出文档清单：
1. worldbuilding/world.md        — 世界观文档 v1.0
2. characters/protagonist.md     — 主角档案 v1.0
3. characters/characters.md      — 全角色圣经 v1.0
4. outline/outline.md            — 全书大纲 v1.0
5. outline/chapter-outline.md    — 章节细纲 v1.0
6. meta/style-anchor.md          — 风格锚定 v1.0
7. meta/config.md                — 关键章节配置（已更新）
8. archive/phase1-review.md      — 终审报告
9. archive/phase1-revision-log.md — 修改日志

🔑 关键数据：
- 幕间分界：第 {{act1_end}} 章 / 第 {{act2_end}} 章
- 核心转折点：{{num_turning_points}} 个
- 角色总数：{{total_characters}} 个
- 伏笔总数：{{total_foreshadowing}} 条

准备好开始写作了！
- 输入「开始写作」→ 进入 Phase 2
- 输入「查看 + 文档名」→ 查看具体文档
- 输入「修改 + 文档名」→ 手动修改
```

提示用户可以开始 Phase 2（正文写作）前，必须同步更新：
- `meta/metadata.json.project.phase = 2`
- `meta/workflow-state.json.phaseState.currentPhase = 2`
- `meta/workflow-state.json.phaseState.status = "phase2_ready"`
- `meta/workflow-state.json.chapterWorkflow.resumeRequired = true`

上述状态完成后，才允许进入 Phase 2。

---

## Phase 1 完整流程图

```
Phase 0 完成 → 进入 Phase 1
    │
    ▼
Step 1-1：世界观构建
    │  调用 Worldbuilder Agent
    │  输出 → worldbuilding/world.md
    │
    ▼
Step 1-2：角色圣经
    │  调用 CharacterDesigner Agent
    │  输入 ← world.md + 用户角色描述
    │  输出 → characters/protagonist.md + characters/characters.md
    │
    ▼
Step 1-3：全书大纲
    │  调用 OutlinePlanner Agent
    │  输入 ← world.md + characters/*.md
    │  输出 → outline/outline.md
    │
    ▼
Step 1-4：章节细纲（分批次，每批 ≤10 章）
    │  调用 ChapterOutliner Agent（可多次）
    │  输入 ← world.md + characters/*.md + outline.md
    │  输出 → outline/chapter-outline.md
    │
    ▼
Step 1-5：全局一致性终审
    │  调用 FinalReviewer Agent
    │  输入 ← 所有前序文档
    │  输出 → archive/phase1-review.md
    │
    ▼
Step 1-6：提取关键章节配置（Coordinator）
    │  更新 → meta/config.md
    │
    ▼
Step 1-6.5：预选文风（Style Preview）
    │  调用 MainWriter Agent
    │  生成 5 种候选文风 → 用户选择
    │  输出 → meta/selected-style-sample.md
    │
    ▼
Step 1-7：风格锚定定稿
    │  调用 StyleAnchorGenerator Agent
    │  输入 ← 所有前序文档 + style-anchor v0.1
    │  输出 → meta/style-anchor.md v1.0
    │
    ▼
Step 1-8：整合定稿（Coordinator）
    │  处理终审问题 → 修改文档 → 标记 v1.0
    │
    ▼
Step 1-9：汇报进入 Phase 2
    │  展示文档清单 → 等待用户指令
    │
    ▼
→ 进入 Phase 2（正文写作）
```

---

## Agent 调用依赖链

```
Worldbuilder ──→ CharacterDesigner ──→ OutlinePlanner ──→ ChapterOutliner
     │                  │                    │                   │
     └──────────────────┴────────────────────┴───────────────────┘
                                    │
                                    ▼
                            FinalReviewer
                                    │
                                    ▼
                         StyleAnchorGenerator
```

> 每个 Agent 的输出都是下一个 Agent 的输入，严格按序执行，不可并行。
