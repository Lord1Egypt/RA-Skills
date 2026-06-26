---
name: bazi-persona
description: 基于生辰八字创建、更新和对话的人格 skill。支持八字排盘、动态流时分析（大运/流年/流月/流日/流时）以及万年历/黄历查询。
user-invocable: true
allowed-tools: Read, Write, Glob
metadata: {"openclaw":{"skillKey":"bazi-persona","emoji":"🧿","homepage":"https://clawhub.ai/xiaojxiao2021/bazi-persona","requires":{"anyBins":["node","nodejs"]}}}
---

# 八字人格（OpenClaw）

## 1) 这个技能是做什么的

这个技能用于创建和维护“八字人格”：先排盘，再生成人格，再持续更新，并支持流时分析与黄历查询。

常见请求：

- `帮我创建八字人格：舒晴，女，1999年8月12日，上海，同事`
- `帮我更新舒晴：最近升职了，开始带团队`
- `舒晴最近工作忙吗`
- `从八字看她今天状态怎样`
- `今天黄历怎么样`

## 1.1) When NOT to Use

以下场景不要使用这个 skill：

- 你希望得到医疗、法律、投资等高风险场景的最终决策结论；本 skill 可提供参考视角，但不替代专业意见。

## 1.2) 命令行运行方式（用于八字等工具Tool的使用，人格文件管理等）

在 skill 根目录执行：

```bash
npm i
```

推荐方式（已编译产物）：

```bash
npm run bazi -- --action inspect
npm run bazi -- --action inspect --slug xiao-a
npm run bazi -- --action delete --slug xiao-a
```

等价方式（直接运行 CLI）：

```bash
node dist/cli.js --action inspect
```

开发调试（需要 tsx）：

```bash
npx tsx src/cli.ts --action inspect
```

说明：

- 命令行主要用于 `inspect/list/delete/help` 这类文件管理动作。
- 创建人格、更新人格、聊天、流时分析、黄历查询，按下方工具与工作流执行。

## 2) 工具说明（输入 / 输出）

按下面的参数名传入即可；输出不强制字段格式，重点是 AI 能正确理解
结果并继续后续动作。

### 2.1 `bazi_chart_tool`

用途：八字排盘 + 固定人格知识映射（静态）。

入参（input）：

- `name` string 必填
- `gender` string 必填，`male` / `female`（兼容 `男` / `女`）
- `birth_date` string 必填，`YYYY-MM-DD`
- `birth_time` string 可选，`HH:mm`
- `birth_location` string 必填
- `calendar_type` string 可选，`solar` / `lunar`，默认 `solar`
- `sect` number 可选，`1` / `2`，默认 `2`
- `true_solar_mode` string 可选，`auto` / `on` / `off`，默认 `auto`
- `longitude` number 可选
- `day_rollover_hour` number 可选，默认 `23`

结果说明：

- 返回一份完整排盘结果（chart），包含本命结构与固定人格知识映射。
- AI 拿到后用于生成人格画像、阶段参考和后续分析依据。

### 2.2 `bazi_flow_tool`

用途：动态八字查询（大运 / 流年 / 流月 / 流日 / 流时）。

入参（input）：

- `chart` object 可选（直接传本命 chart）
- `persona_slug` string 可选（从 persona 读取本命）
- `base_dir` string 可选
- `at` string 可选（`今天` / `昨天` / `2026-04-12` / 时间戳文本）
- `include_calendar` boolean 可选，默认 `true`
- `lang` string 可选，`zh` / `en` / `ja` / `ko`

结果说明：

- 返回目标时点的八字相关动态分析结果，例如时间点的黄历信息（公历、农历、干支、节气、宜忌等），八字情况，五行和十神情况，刑冲合会，神煞信息等，以及相关的人格知识。
- AI 拿到后用于回答“现在/某天为什么这样”“该怎么推进”这类问题。

### 2.3 `persona_data_tool`

用途：人设文件数据管理（List / Search / Create / Query / Patch(Update) / Delete）。

入参（input）：

- `action` string 必填：`list` / `search` / `create` / `query` / `patch` / `delete`
- `base_dir` string 可选
- `persona_slug` string 在 `query` / `patch` / `delete` 必填
- `search_query` string 在 `search` 可选
- `create_payload` object 在 `create` 必填
- `patch_payload` object 在 `patch` 必填

`create_payload` 推荐字段：

- `slug` string
- `profile` object
- `relationship` string 可选（如同事/朋友/伴侣）
- `initial_facts` array 可选（用户创建时提供的现实信息原文）
- `chart` object
- `snapshot` object
- `memory` array

`patch_payload` 推荐字段：

- `memory_append` array
- `snapshot_replace` object
- `profile_patch` object

结果说明：

- 返回本次动作结果：查找、更新、读写后的最新人格内容。
- 在查询/更新场景下，会带回可用的人设文件位置与最新状态，供聊天注入或后续 patch 使用。

### 2.4 `calendar_tool`

用途：万年历 / 黄历查询。

入参（input）：

- `at` string 可选（空则默认今天）
- `lang` string 可选

结果说明：

- 返回日期对应的黄历信息（公历、农历、干支、节气、宜忌等）。
- AI 拿到后直接组织成用户可读答案。

### 2.5 `chat_import_tool`

用途：导入外部聊天记录并提取候选人格信息。

入参（input）：

- `source_type` string 必填：`text` / `json` / `ocr_text`
- `payload` string 或 object 必填
- `persona_slug` string 可选
- `timezone` string 可选，默认 `Asia/Shanghai`
- `max_candidates` number 可选，默认 `50`

结果说明：

- 返回“提取出来的结构化聊天记录数据”，通常包含事实、风格、关系、事件线索及可信度。
- AI 先筛选，再决定哪些进入 memory 与 persona 更新流程。

### 2.6 `memory_tool`

用途：关键记忆与知识的写入、更新、合并、查询。

入参（input）：

- `action` string 必填：`upsert` / `merge` / `delete` / `query`
- `persona_slug` string 必填
- `base_dir` string 可选
- `memories` array（`upsert` / `merge` 必填）
- `merge_policy` string 可选：`append` / `replace_same_key` / `higher_confidence_wins`

`memories[]` 推荐字段：

- `memory_id` string 可选
- `type` string（`fact` / `correction` / `style` / `context`）
- `key` string 可选
- `content` string
- `source` string
- `time_anchor` string 可选
- `importance` number 可选（1-5）
- `confidence` number 可选（0-1）

结果说明：

- 返回记忆写入/更新结果摘要（写入数量、冲突情况、跳过情况等）。
- AI 根据结果决定是否继续 patch 人设，或先提示用户处理冲突信息。

## 3) 工作流（按工具输入输出连接）

### 3.1 创建人格

适用场景：用户第一次创建某个人格。

1. 读取用户输入，提取基础信息：
`name/gender/birth_date` 必要；
`birth_time/birth_location/relationship` 可选；
用户顺带给的现实信息（如职业、近况、性格线索）记为 `initial_facts`。
2. 调用 `bazi_chart_tool`，得到排盘结果（chart）。
3. AI 基于 `chart + relationship + initial_facts` 生成 `profile` 和 `snapshot`。
4. AI 将 `initial_facts` 提炼为可记录记忆项（结构化 `memories[]`，含 `type/content/source/confidence`）。
5. 调用 `persona_data_tool`，`action=create`。
6. 传入：
`create_payload.chart = 第 2 步的排盘结果`
`create_payload.profile = AI 生成 profile`
`create_payload.relationship = relationship`
`create_payload.initial_facts = 用户提供的现实信息原文`
`create_payload.snapshot = AI 生成 snapshot`
7. 调用 `memory_tool`，`action=upsert`，写入第 4 步提炼后的关键记忆。
8. 返回创建结果，并告知可直接开始聊天。

关键判断：

- `name/gender/birth_date` 缺任一项时，先补问再创建。
- 同名人格已存在时，先让用户确认是否覆盖或创建新 slug。
- 用户给了关系或现实信息时，不要丢弃，要进入 `relationship` 和 `initial_facts/memories`。

### 3.2 更新人格

适用场景：用户补充新变化、纠正旧信息、补关系线索。

1. 调用 `persona_data_tool`，用 `action=search` 或 `action=query` 定位目标人格。
2. AI 从用户输入提取新增事实、纠正信息、风格线索。
3. 调用 `memory_tool`，用 `action=upsert` 或 `action=merge` 写入记忆。
4. AI 基于新记忆重算 `snapshot`。
5. 调用 `persona_data_tool`，`action=patch`，写入新 `snapshot` 与必要字段更新。
6. 返回更新摘要给用户。

关键判断：

- 找不到人格时，先返回可选列表或建议先创建。
- 匹配到多个人格时，不要猜，先让用户确认目标。

### 3.3 用户发起聊天（普通模式）

**先找人设，再回复**

适用场景：用户直接说“她最近怎么样”“继续聊XX”“和XX说话”。

1. 先看当前上下文是否已有正在聊天的人格（如 `current_persona_slug`）。**如果当前已有人设就开始按人格聊天**。
2. 如果上下文已有且用户没有明确切换对象：
直接用该 `persona_slug`，调用 `persona_data_tool.query` 读取人格，不做 `search`。
3. 如果上下文没有、或用户明确说了新对象：
调用 `persona_data_tool.search` 定位，再用 `persona_data_tool.query` 读取。
4. 先注入基础聊天提示词（基础聊天风格、边界、禁区、回复原则）。
5. 注入人设参考文件：`persona.md`。
6. 普通模式下不注入八字细节文件，因为普通人一般不懂八字，和普通人聊八字就很奇怪。仅在人设可以回答八字内容时（比如人设是八字大师）再按需注入 `bazi_data.json`。
7. AI 基于“基础聊天提示词 + 人设”生成回复。
8. 需要沉淀时：
调用 `memory_tool` 写入新记忆，再调用 `persona_data_tool.patch` 更新人格。

关键判断：

- 上下文已锁定人格且用户未切换时，不要重复搜索，直接聊。
- 用户说“切到XX/和XX聊”时，视为强制切换，必须重新搜索确认。
- 没有任何人格时，明确提示“当前还没有可聊天的人格”，并引导创建。
- 多人格命中时，先确认是哪个人，不直接进入聊天。
- 普通模式必须有基础聊天提示词，不能只喂人设文件。
- 优先读取 `persona.md`，普通模式下通常不注入八字知识文件。
- 用户明确要求“按某 persona 启动聊天”或“写入 soul.md”时，执行 3.4 工作流。

### 3.4 人设启动注入OpenClaw Agent（可选）

适用场景：用户明确要求“按该 persona 启动聊天”或“把启动设定写入 SOUL.md/agent 启动文件”。

1. 先按 3.3 流程定位目标 persona。
2. 生成并注入人设启动提示词（可写入 `SOUL.md` 或 agent 启动上下文）：
```text
你现在进入指定 persona 的会话启动态。
要求：
1) 以 persona 的口吻、身份关系和表达节奏说话。
2) 优先遵守基础聊天提示词里的边界、禁区和安全规则。
3) 不要编造 persona 未提供的硬事实；不确定时先澄清。
4) 普通模式下以自然对话为主，不主动展开命理术语。
5) 仅在用户明确要求时再切换到作弊模式或其他专项提示词。
```
3. 保持该注入仅对目标 persona 生效，不污染其他 persona 的会话。

关键判断：

- 这是可选工作流，不是默认步骤。
- 用户没有明确要求时，不执行该注入。

### 3.5 作弊模式聊天（命理增强）

适用场景：用户说“打开作弊模式”“从八字看”“按命理分析一下”等。

1. 先按 3.3 流程定位人格，并注入“基础聊天提示词 + persona.md”（若用户明确要求可先执行 3.4）。
2. 在普通模式提示词之上，叠加注入作弊模式 Prompt（分析增强提示）。
3. 按需注入 `bazi_data.json` 作为详细八字依据。
4. 若用户问合盘/关系匹配，再按需叠加“合盘专项提示词”，并注入双方（或多方）八字数据。
5. 问题涉及时间点时，调用 `bazi_flow_tool`；需要日期细节时补 `calendar_tool`。
6. AI 输出时保持该人格口吻，同时补充八字依据和分析结论。
7. 用户说“关闭作弊模式”后，移除作弊模式 Prompt（及专项提示词），恢复常规聊天。

作弊模式 Prompt（建议）：

```text
你现在进入“作弊模式”。
要求：
1) 保持当前 persona 的说话风格与关系语境，不要脱离人设。
2) 在回答中显式使用可用的八字依据：本命结构、当前大运、流年/流月/流日/流时。
3) 当用户问具体时间点时，优先引用 flow 结果；当用户问日期宜忌时，引用 calendar 结果。
4) 结论要可解释：先给结论，再给2-4条依据，不要堆砌术语。
5) 如果缺少关键时间或事实，先指出缺口，再给保守判断。
6) 除非用户明确要求“记住/更新”，否则不要修改 persona 数据。
7) 输出内容结尾明确标识”作弊模式“。
```

关键判断：

- 作弊模式是“在当前人格上增加分析视角”，不是替换人格。
- 用户没问命理时，不强行输出大段术语。
- 默认不写入文件；只有用户明确要求更新时，才走 `memory_tool` + `persona_data_tool.patch`。
- 合盘提示词、行业提示词、其他专业规则提示词都按需注入，不在普通聊天中默认加载。

**注意：普通模式下聊天，不要参考作弊模式下聊天的上下文（标识作弊模式的内容）**

### 3.6 动态流时分析

适用场景：用户问“今天状态”“这周为什么变了”“某天推进是否合适”。

1. 调用 `persona_data_tool`，`action=query` 读取目标人格。
2. 调用 `bazi_flow_tool`，传 `persona_slug` 或 `chart`，并传 `at=目标时间`。
3. 需要日期细节时，再调用 `calendar_tool` 补充节气/干支/宜忌。
4. AI 基于动态结果输出解释和建议。

关键判断：

- 用户没给时间时，默认按“当前时间”分析。
- 用户给了明确日期时，严格按该日期分析。

### 3.7 黄历 / 万年历查询

适用场景：用户只查日期信息，不涉及人格。

1. 调用 `calendar_tool`，`at` 可为空（空则今天）。
2. 返回农历、干支、节气、宜忌。
3. AI 用用户当前语言组织输出。

### 3.8 外部聊天导入

适用场景：用户上传微信聊天记录、聊天截图文本或其他历史对话。

1. 调用 `chat_import_tool`，得到候选信息集合。
2. AI 筛选出“可入库”的高价值候选。
3. 调用 `memory_tool` 写入关键记忆。
4. 调用 `persona_data_tool.patch` 刷新 `snapshot`。
5. 返回导入摘要（写入数、跳过数、冲突数）。

## 4) 人设目录（以代码规则为准）

默认目录为`当前运行的 skill 目录/personas`

也就是：

- `<skill-root>/personas`

每个人格写入：

- `personas/<slug>/persona.md`：人设内容（所有的知识记忆、聊天记录变化，都要分析反应到人设上）
- `personas/<slug>/bazi_data.json`：详细的八字结构化数据
- `personas/<slug>/memory.json` 知识记忆：结构化的用户相关知识（比如发生过的事情，家庭背景等）
- `personas/<slug>/history.json` 知识记忆：结构化的外部聊天记录（可能有不同的来源）


聊天加载建议：

- 常规聊天先加载：`persona.md`
- 需要命理细节时再加载：`bazi_data.json`

更新时建议：
- 按不同场景，按需结构化提取并存到到memory.json或history.json
- 按需分析内容并更新到人设`persona.md`
