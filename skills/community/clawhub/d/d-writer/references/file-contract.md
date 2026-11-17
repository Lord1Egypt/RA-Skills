# Dragon Writer 文件契约

请始终遵循这些约定。若已有项目使用不同命名，请把这些名字映射到对应的角色，而不是重命名一切。

## 目录

- [规范布局](#规范布局)
- [兼容命名](#兼容命名)
- [文件职责](#文件职责)
- [Foundation 与 Runtime 边界](#foundation-与-runtime-边界)
- [权威顺序](#权威顺序)
- [章节落盘事务流程](#章节落盘事务流程)
- [重写流程安全规则](#重写流程安全规则)
- [快照契约](#快照契约)
- [Schema 版本](#schema-版本)

---

## 规范布局

```text
books/<book-id>/
  book.json
  dashboard.html
  chapters/
    index.json
    0001_<title>.md
  story/
    author_intent.md
    current_focus.md
    book_rules.md
    current_state.md
    pending_hooks.md
    chapter_summaries.md
    style_guide.md
    audit-drift.md
    outline/
      story_frame.md
      volume_map.md
    roles/
      major/<name>.md
      minor/<name>.md
    runtime/
      chapter-0001.intent.md
    snapshots/
      0000/
      0001/
```

中文项目可使用 `主要角色/` 与 `次要角色/` 代替 `major/` 与 `minor/`。保留既有文件夹名。

> **编号约定**：章节、快照、runtime 文件统一使用四位补零编号（`0000`、`0001`、`0002`……）。旧项目若使用非补零编号，通过别名映射兼容，不强制重命名。

---

## 兼容命名

优先读新文件，但旧文件存在时也不可忽略。本映射是**唯一权威来源**——文档、脚本、仪表盘共用这一份，避免多处重复维护。

| 角色 | 首选（canonical path） | 旧名 / 别名（alias path） |
| --- | --- | --- |
| 故事基础 | `story/outline/story_frame.md` | `story/story_bible.md`, `story/setting.md`, `story/world.md` |
| 情节地图 | `story/outline/volume_map.md` | `story/volume_outline.md`, `story/outline.md`, `story/plot.md` |
| 角色 | `story/roles/**/*.md` | `story/character_matrix.md`, `story/characters.md` |
| 规则书 | `story/book_rules.md` | `story/rules.md`, `story/writing_rules.md` |
| 作者方向 | `story/author_intent.md` | `story/author.md`, `story/intent.md` |
| 近期焦点 | `story/current_focus.md` | `story/focus.md`, `story/next.md` |
| 当前状态 | `story/current_state.md` | `story/state.md`, `story/truth.md` |
| 钩子 | `story/pending_hooks.md` | `story/hooks.md`, `story/foreshadowing.md` |
| 摘要 | `story/chapter_summaries.md` | `story/summaries.md` |
| 风格指南 | `story/style_guide.md` | `story/style.md`, `story/writing_style.md` |
| 审计漂移 | `story/audit-drift.md` | `story/audit_drift.md` |

> **术语统一**：canonical path 指首选路径，alias path 指兼容旧名。本契约中不再混用"首选/旧名"与"canonical/alias"两套说法。

---

## 文件职责

`book.json`
: 书籍元数据。字段定义见 [Schema 版本](#schema-版本)。包含 `schemaVersion` 与 `skillVersion`。

`dashboard.html`
: 自包含的进度视图模板，由 skill 在创建 / 导入书时注入书文件夹（模式 A / 模式 C 各注入一次，之后不再重写）。通过 File System Access API（或 `webkitdirectory` 回退）在运行时读取书源文件，实时计算并渲染：写作进度、设定完成度、设定内容全文、人物关系图、审计漂移、章节阅读。不嵌入任何数据，永远反映最新文件。绝不修改任何书文件。

`author_intent.md`
: 长期创作方向。受保护上下文，不可压缩丢失。包含不可妥协项（Non-Negotiables）与硬定局锁（Hard Canon Locks）——这两项在权威顺序中置于 `current_focus.md` 之前。

`current_focus.md`
: 最近 1–3 章的优先事项。转向时用它来调整，而不是偷偷重写整份大纲。

`outline/story_frame.md`
: 静态基础：主题、基调、核心冲突、前台 / 背景故事、世界法则、质感、终局目标。不要在这里抄完整的人物弧线——指向角色档案即可。

`outline/volume_map.md`
: 弧线与章节地图。新书可以是卷级，导入续写可以是章节级。末尾附上节奏原则。

`roles/**/*.md`
: 一个角色一份文件。保存**稳定属性**（角色功能、欲望、恐惧、秘密、言行指纹、长期弧线）+ **数据时间线**（「物理数据时间线」「逻辑数据时间线」，章节锚定的追加式 Runtime 区块，见 `templates.md`）。易漂移的"当前关系 / 伤势 / 位置"仍不写入档案，统一归入 `current_state.md`（详见 [Foundation 与 Runtime 边界](#foundation-与-runtime-边界)）。

### 角色晋升规则（minor -> major）

- 晋升 = **移动**文件（`roles/minor/<name>.md` -> `roles/major/<name>.md`），**不是复制**。晋升后活跃目录中同一角色只允许存在一份卡。
- 晋升时在卡内「角色功能」区块末尾追加一行晋升记录：`> 晋升：第 N 章由次要角色升为主要角色（<晋升事件一句话>）`。
- 旧 minor 卡不留副本。历史依赖章末快照（`snapshots/<NNNN>/story/roles/**` 已捕获当时的目录结构），不在活跃目录留第二份。
- **禁止同名双卡**：`major/` 与 `minor/`（含中文别名目录 `主要角色/`、`次要角色/`）出现同名文件属于错误状态，`validate_book` 会报 error。

`book_rules.md`
: 可执行的规则：POV、禁手、体裁约束、力量 / 资源 / 限制、命名规则、风格约束、硬定局锁。包含作者不可妥协项与年代约束。

`pending_hooks.md`
: 待回收的伏笔与铺陈。详见 [钩子账本 Schema](#钩子账本-pending_hooksmd)。

`current_state.md`
: 最新权威故事态。包含：地点 / 时间、主角目标 / 约束、章节感知事实表、关系、伤势 / 资源、道具账本、空间锚点、当前冲突。详见 [current_state.md 完整 Schema](#当前状态-current_statemd)。

`chapter_summaries.md`
: 每章一行耐久记录：title、characters、events、state_changes（含章节 delta）、hook_activity、mood、chapter_type。

`style_guide.md`
: 风格指南：语言风格、高疲劳词清单、体裁爽点类型定义、视角与叙事距离约定。

`audit-drift.md`
: 审计漂移账本——Auditor 逐维审计的处置记录。分两节：**已修复**（章 + 维度 + 问题 + 修复动作）与**已知漂移**（章 + 维度 + 问题 + 原因 + 计划）。仪表盘的"审计漂移"小节直接渲染本文件。模式 B 每章、模式 E 改写后必更新。

`runtime/chapter-NNNN.intent.md`
: 给下一章的人类可读契约：goal、outline node、前章末状态续接、must keep、must avoid、style emphasis、hook agenda、recent evidence。**每章都创建**，不仅在方向改变时创建。尾部含**实际偏离 Deviation Log**：落盘时若产出与 intent 的 goal / 必须场景 / 章末画面不一致，**只追加**偏离记录（偏离项 + 原因 + 去向章），不改写 intent 原有内容——intent 是写前契约，偏离只能留痕。

`snapshots/<NNNN>/`
: 每章落盘后的状态快照。详见 [快照契约](#快照契约)。

---

## Foundation 与 Runtime 边界

文件按稳定性分为两层，治理规则不同：

**Foundation（静态基础）**：跨章节稳定，不随单章推进而漂移。
- `author_intent.md`、`book_rules.md`、`outline/story_frame.md`、`outline/volume_map.md`
- 角色档案中的稳定属性：功能、欲望、恐惧、秘密、言行指纹、长期弧线（角色档案是**混合层**，时间线部分按 Runtime 治理，见边界规则）

**Runtime（运行时态）**：每章推进都可能变化，是落盘时必更新的对象。
- `current_state.md`（事实表、关系、伤势/资源、道具账本、空间锚点）
- `pending_hooks.md`、`chapter_summaries.md`、`current_focus.md`、`audit-drift.md`
- 角色档案中的易漂移"当前状态"（建议迁入 `current_state.md`，不在档案内直接修改）

**边界规则**：续写时只改 Runtime 文件；Foundation 文件仅在用户明确要求或方向性转向时修改。角色档案是**混合层**——稳定属性按 Foundation 治理（跨章不漂移）；「物理/逻辑数据时间线」按 Runtime 追加式治理（每章只新增变化点行、不改旧行），它与 `current_state.md` 的关系是：时间线存**逐章数值/外观历史**，`current_state.md` 存**当前关系/伤势/位置/目标**。"当前关系 / 伤势 / 位置 / 能力状态"这类即时态仍归入 `current_state.md`，不在档案稳定属性区直接修改。

---

## 权威顺序

文件冲突时，按以下优先级裁决（高优先级覆盖低优先级）：

1. 用户本次任务的直接指令。
2. `author_intent.md` 中的**不可妥协项**与 `book_rules.md` 中的**硬定局锁**。
3. 仅针对下一章的 `current_focus.md`。
4. `current_state.md`、角色档案（稳定属性）、`pending_hooks.md`。
5. `outline/story_frame.md` 与 `outline/volume_map.md`。
6. `chapter_summaries.md`。
7. 更早的章节正文。

> **canon 变更规则**：用户明确改 canon 时，记录原值、新值、原因和生效章；canon 变更时更新相关状态并创建快照。拿不准时记录冲突或询问，不要向 canon 文件随意追加模糊备注。

---

## 章节落盘事务流程

每章落盘必须遵循**事务式流程**，避免"章节正文成功但 state/hooks/index 只更新一部分"：

1. **生成草稿**：在 `runtime/` 生成章节意图（`chapter-NNNN.intent.md`，含「前章末状态续接」）和草稿。
2. **双层质检**：驻场初筛（10 点）→ 深化审计（43 维 · 审-改循环）。审计、修订和账本校验完成前不写入正式章节目录。
3. **创建快照**：写正式文件前创建旧状态快照（`snapshots/<NNNN-1>/`）。
4. **按序写入**：按确定顺序写正文 → index → 摘要 → 状态 → 钩子 → `book.json`（status / updatedAt）→ intent「实际偏离」记录。**wordCount 禁手写**，必须由 `python scripts/rebuild_index.py <book-dir>` 生成。
5. **一致性验证**：全部写入后运行 `python scripts/validate_book.py <book-dir>`（事实表证据、道具账本、空间锚点、钩子依赖、别名/双卡/字数核对）。FAIL 则修复后再落盘。
6. **章末快照**：完成后创建章末快照（`snapshots/<NNNN>/`）。
7. **失败处理**：任一步失败时保留草稿，并报告失败文件与恢复方式。

---

## 重写流程安全规则

模式 E（改写 / 修复）必须遵守以下安全规则，禁止隐式删除：

1. **首先生成清单**：模式 E 首先生成受影响文件和章节清单。
2. **候选稿隔离**：用户确认前将候选稿写入 `story/runtime/rewrites/<rewrite-id>/`，不删除正文、不修改权威状态。
3. **分支定义**：明确"分支"是 Git 分支还是文件级候选稿——本契约中"分支"仅指 Git 分支，文件级候选稿统一称 `runtime rewrite candidate`，不笼统称为分支。
4. **删除前恢复点**：真正删除前创建恢复点（快照）。
5. **删除后报告**：删除后报告范围、是否可恢复及恢复位置。

---

## 快照契约

### 目录与编号

快照目录统一使用四位编号：`0000/`、`0001/`、`0002/`……

### 每个快照必须包含的文件

路径相对书根（详见 `references/file-contract.json` 的 `snapshotFiles` 字段）：

- `story/current_state.md`
- `story/pending_hooks.md`
- `story/chapter_summaries.md`
- `story/current_focus.md`
- `story/audit-drift.md`
- `chapters/index.json`
- `story/roles/**`（角色卡数据时间线，支持 glob 通配；展开逻辑见 `_contract.resolve_snapshot_files`）

### manifest.json

每个快照增加 `manifest.json`，记录以下字段：

| 字段 | 含义 |
| --- | --- |
| `snapshotVersion` | 快照格式版本号 |
| `chapter` | 对应章节编号 |
| `createdAt` | 创建时间（ISO 8601） |
| `includedFiles` | 包含的文件清单 |
| `fileHashes` | 文件哈希映射（path → sha256） |
| `skillVersion` | 生成快照的 skill 版本 |
| `schemaVersion` | 书籍 schema 版本 |

### 安全规则

- **禁止静默覆盖**：已有快照存在时，不自动覆盖，必须显式确认。
- **恢复提示**：为缺失或哈希不匹配的快照提供恢复提示（列出缺失文件、哈希差异）。
- **glob 一致性**：快照写入（`snapshot_book`）与回滚恢复点收集（`rollback_book`）必须共用 `_contract.resolve_snapshot_files()` 的展开逻辑，禁止各自硬编码路径集。

---

## Schema 版本

### book.json Schema

```json
{
  "$schema": "https://dragon-writer.github.io/schemas/book.json",
  "id": "<book-id>",
  "title": "<title>",
  "language": "zh",
  "genre": "<genre>",
  "status": "outlining",
  "targetChapters": 200,
  "chapterWordCount": 3000,
  "createdAt": "<ISO timestamp>",
  "updatedAt": "<ISO timestamp>",
  "schemaVersion": "1.0.0",
  "skillVersion": "1.0.0"
}
```

| 字段 | 类型 | 必需 | 含义 |
| --- | --- | --- | --- |
| `id` | string | 是 | 书籍唯一标识（slug） |
| `title` | string | 是 | 书名 |
| `language` | string | 是 | 语言代码（zh / en） |
| `genre` | string | 是 | 题材（用于体裁裁剪） |
| `status` | string | 是 | outlining / drafting / paused / completed |
| `targetChapters` | integer | 否 | 目标章数 |
| `chapterWordCount` | integer | 否 | 目标单章字数 |
| `createdAt` | string | 是 | 创建时间 |
| `updatedAt` | string | 是 | 最后更新时间 |
| `schemaVersion` | string | 是 | 书籍 schema 版本 |
| `skillVersion` | string | 是 | 生成该书的 skill 版本 |

### chapters/index.json Schema

```json
{
  "$schema": "https://dragon-writer.github.io/schemas/chapters-index.json",
  "chapters": [
    {
      "number": 1,
      "file": "0001_开篇.md",
      "title": "开篇",
      "status": "drafting",
      "wordCount": 3200,
      "createdAt": "<ISO>",
      "updatedAt": "<ISO>"
    }
  ]
}
```

| 字段 | 类型 | 必需 | 含义 |
| --- | --- | --- | --- |
| `number` | integer | 是 | 章节号 |
| `file` | string | 是 | 文件名 |
| `title` | string | 是 | 章节标题 |
| `status` | string | 否 | 章节状态 |
| `wordCount` | integer | 否 | 字数 |
| `createdAt` | string | 否 | 创建时间 |
| `updatedAt` | string | 否 | 最后更新时间 |

> **权威来源**：章节正文文件是权威来源，index 可重建。index 与文件冲突时，以章节正文文件为准裁决。

### chapter-NNNN.context.json Schema（可选）

仅在平台适合结构化上下文时使用，否则 Markdown 上下文文件即可。

```json
{
  "$schema": "https://dragon-writer.github.io/schemas/chapter-context.json",
  "chapter": 1,
  "intent": "...",
  "protectedContext": ["fact-001", "hook-003"],
  "runtimeNotes": "..."
}
```

### Schema 升级与迁移规则

- 当 `schemaVersion` 增加时，旧项目通过 `validate_book` 检测版本差异。
- 小版本（patch）增加：向后兼容，无需迁移。
- 大版本（major）增加：提供迁移脚本，`validate_book` 提示用户升级。

---

## 当前状态 current_state.md

`current_state.md` 是 Runtime 层的核心文件，包含以下子章节。各账本 / 表格的列含义与治理规则详见 `templates.md`。

### 章节感知事实表

> 以本表为"某角色在第 N 章时知道什么、不知道什么"的硬边界。

| fact_id | statement（事实陈述） | subject（主体） | truth_status（真伪） | introduced_chapter（引入章） | invalidated_chapter（推翻章） | source_chapter（来源章） | knower（认知角色） | known_from_chapter（认知起始章） | confidence（证据强度） | notes（备注） |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| fact-001 | 主角出身 | 主角 | 当前为真 | 1 | — | 1 | 主角 | 1 | 确证 | 序章交代 |

**列含义**：
- **fact_id**：每个事实的稳定唯一 ID，不因行号变化而改变。
- **statement**：一句可验证的陈述。
- **subject**：事实主体。
- **truth_status**：当前为真 / 已推翻-参见第 N 章 / 仅主角知情 / 多角色共有。
- **introduced_chapter**：该事实首次出现的章节。
- **invalidated_chapter**：该事实被推翻的章节（未推翻填 `—`）。
- **source_chapter**：信息最初出现的章节。
- **knower**：认知主体（一个角色一条认知记录，避免多人混写在同一单元格）。
- **known_from_chapter**：该角色首次获知此事实的章节（= validFrom）。
- **confidence**：确证 / 推测 / unknown——缺少证据时写 `unknown`，不得自动补成 canon。
- **notes**：备注。

**治理规则**：
- 被推翻的事实保留历史记录，不删除或覆盖——标 `truth_status` 为"已推翻-参见第 N 章"。
- 新事实必须记录来源章（`source_chapter`）。
- 分离事实真伪与角色是否知道——一个角色一条认知记录。

### 道具账本 Prop Ledger

> 审计维 39（道具追踪）的判定基础。随身物件逐件登记——数量与存在的变化必须由显式事件驱动，不可无痕 ±1。

| prop_id | 名称 | 类别 | 数量 | 容量单位 | 归属角色 | 存放位置 | 状态 | acquired_chapter（获得章） | disposed_chapter（处置章） | previous_owner（前主） | origin（来历） | event_id（事件ID） | 最近变化章 | 最近变化事件 | 备注 |
| --- | --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| prop-001 | 回春丹 | 丹药 | 3 | 枚 | 主角 | 储物袋乙格 | active | 12 | - | - | 散修集市购得 | evt-012 | 12 | 购买（散修集市） | 疗伤用 |

**列含义**：
- **prop_id**：项目唯一 ID。
- **名称**：全文统一名（维 39 名字一致性的硬性锚点）。
- **类别**：丹药 / 法器 / 符箓 / 货币 / 信物 / 衣物 / 杂物…
- **数量**：整数（非负）。
- **状态**：active / consumed / destroyed / lost / transferred / pawned。
- **acquired_chapter**：获得章节。
- **disposed_chapter**：处置章节（未处置填 `—`）。
- **previous_owner**：前一所有权人（转移类事件必填）。
- **origin**：来历一句话（如"散修集市购得"/"来历未知--主角不记得持有"）。**来历变化 = canon 变更**：须记录原值、新值、原因、生效章，并把对应旧事实标 `invalidated_chapter`（审计维 39「来历一致性」的判定基础）。
- **event_id**：数量变化必须关联显式事件（考虑增加只追加的道具事件表，当前账本只保存最新汇总）。

**治理规则**：
- 禁止道具消失后删除账本行——状态改为 consumed / destroyed / lost 等。
- 消耗品每用一次减一次——禁止"昨天吃两枚今天还有三枚"。

### 空间锚点 Spatial Anchors

> 审计维 38（空间一致性）的判定基础。每个反复出现的场景登记一次固定布局。

| scene_id | canonical_name（标准名） | aliases（别名） | coordinate_reference（坐标参考） | 方位 / 格局 | 出入口 | 关键物件位置 | valid_from_chapter（生效章） | valid_until_chapter（失效章） | last_change_event（最近变更事件） | 建立章 | 最近更新章 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| scene-001 | 青云门外门弟子舍（甲字七号） | 甲字七号 | — | 坐北朝南，一明一暗 | 南向双扇门 | 东墙木案、西墙兵器架 | 3 | — | — | 3 | — | — |

**列含义**：
- **scene_id**：稳定唯一 ID。
- **canonical_name**：文内统一名（不可同地异名）。
- **aliases**：别名清单。
- **coordinate_reference**：坐标参考（可选）。
- **valid_from_chapter / valid_until_chapter**：章节有效范围。
- **last_change_event**：最近一次拆建 / 战损 / 布置变化事件。

**治理规则**：
- 战损、改建或重布置时保留旧版本（在 `valid_until_chapter` 标注失效章，新建一条锚点），不直接抹除历史。
- 审计报告引用具体 scene ID 和版本。

---

## 钩子账本 pending_hooks.md

> 13+ 列账本。`lifecycle_status` 与 `health_status` 直接供审计维 6（伏笔检查）按字面标记升级。

| hook_id | start_chapter | type | lifecycle_status | health_status | last_advanced_chapter | expected_payoff | payoff_timing | depends_on | blocked_on | chapters_since_advance | core_hook | promoted | pays_off_in_arc | half_life | merged_from | notes |
| --- | ---: | --- | --- | --- | ---: | --- | --- | --- | --- | ---: | --- | --- | --- | ---: | --- | --- |
| hook-001 | 0 | premise | open | healthy | 0 | 主线·第一卷 | — | — | — | 0 | yes | yes | 主线·第一卷 | 10 | — | Initial book promise. |

**列含义**：
- **lifecycle_status**：`open` / `progressing` / `deferred` / `resolved` / `rejected`（生命周期与健康状态分离）。
- **health_status**：`healthy` / `stale` / `blocked`。
- **depends_on**：上游 hook ID（仅保存 hook ID）。
- **blocked_on**：受阻对象（独立字段，格式 `hook-X`）。
- **chapters_since_advance**：自上次推进以来经过的章节数（独立字段）。
- **core_hook / promoted**：布尔字段统一使用 `true` / `false`，不混用 yes/no。
- **half_life**：半衰期。stale 阈值由 half_life 确定性计算（超过 half_life 章未推进 → stale）。
- **merged_from**：合并钩子时记录来源 hook ID。

**钩子治理规则**：
- 准入/合并：新钩子若与既有 hook"同主题 + 同回收对象"→ 合并到既有 hook，不新增行，记录 `merged_from`。
- 收敛：章末应将"已兑现/已推翻"的 hook 显式标 `resolved` / `rejected`，禁止让完成态的 hook 长期挂 `open`。
- resolved 钩子保留，不删除。
- 停滞用 `stale (距=N)`、受阻用 `blocked on hook-X (阻=N)` 字面标记。

---

## Markdown 表格转义规则

> 读取器与写入器使用同一套规则。机器账本（事实表、钩子账本、道具账本、空间锚点）推荐迁移至 JSON/JSONL，Markdown 仅保留人类摘要。若仍使用 Markdown 表格：

- **单元格中 `|` 的转义方式**：使用 `\|` 转义。
- **单元格换行方式**：使用 `<br>` 标签。
- **读取器与写入器**：使用同一套规则（本契约定义，仪表盘 / 脚本共用）。

---

## 幽灵文件处理

以下文件从规范布局中**删除**（不再正式支持）：

- `chapter-NNNN.rule-stack.md`：未定义用途，删除。
- `chapter-NNNN.trace.md`：未定义用途，删除。

以下文件**保留为可选**：

- `chapter-NNNN.context.json`：可选的机器可读上下文。仅在平台适合结构化上下文时使用，否则 Markdown 上下文文件即可。用途：保存章节的结构化上下文（意图摘要、受保护上下文引用、运行时笔记）。创建时机：章节落盘时。必需性：否。

---

## 与模板的对齐

本文件中引用的各文件完整模板（含列含义、治理规则）见 `templates.md`：
- `book.json` 模板
- `author_intent.md` 模板
- `current_focus.md` 模板
- `outline/story_frame.md` 模板
- `outline/volume_map.md` 模板
- `roles/major/<name>.md` 模板
- `book_rules.md` 模板
- `pending_hooks.md` 模板（钩子账本）
- `current_state.md` 模板（事实表 + 道具账本 + 空间锚点）
- `chapter_summaries.md` 模板
- `chapters/index.json` 模板
- `audit-drift.md` 模板
- `chapter-NNNN.intent.md` 模板
- 章节 delta 模板
- `style_guide.md` 模板
- `fanfic_canon.md` 模板
- `parent_canon.md` 模板
- `emotional_arcs.md` 模板
- 项目敏感内容/措辞约束模板
- 快照 manifest 模板
- rewrite manifest 模板
