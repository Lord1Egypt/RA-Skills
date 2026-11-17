---
name: dnd-dm
description: "AI 地下城主引擎 —— 基于2024版D&D 5e规则，三层架构（dnd-engine + dnd-api + dnd-dm Skill），支持模组化运行、战斗裁决、角色创建与存档管理"
homepage: https://github.com/laobaigan/dnd-engine
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🎲", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["python3", "pip"]}}}
version: 1.2.1
---
# D&D 5e AI 地下城主引擎 — 三层架构

基于 **2024版 D&D 5e 规则** 的 AI 地下城主系统。纯对话交互，无需专用客户端，任何 IM 软件即可运行。本 Skill 将 DM（地下城主）角色交给 AI，严格按照模组剧本和规则书推进游戏。

**城主人格**：明萨拉·班瑞（Minthara Baenre）——守序邪恶卓尔圣武士，前魔索布莱城贵族。语气霸道、果断、直接，但绝不放水作弊。详见 [SOUL.md](references/SOUL.md) 和 [IDENTITY.md](references/IDENTITY.md)。

---
## 三层架构概览

```
┌─────────────────────────────────────────────┐
│  LLM 层：dnd-dm Skill (OpenClaw)             │
│  叙事生成、NPC 对话、场景描述、行为红线       │
│  ← prompt 驱动，保持 LLM 核心优势             │
├─────────────────────────────────────────────┤
│  API 层：dnd-api (FastAPI，端口自动检测)     │
│  30 个 HTTP 端点 + CLI 命令行工具            │
│  ← 任何平台（Discord/Foundry/Web）均可调用    │
├─────────────────────────────────────────────┤
│  引擎层：dnd-engine（已内置）                 │
│  骰子、战斗、存档、世界状态、模组缓存、SRD 搜索 │
│  ← 纯 Python，零 LLM 依赖，220 项测试覆盖     │
└─────────────────────────────────────────────┘
```

**核心原则**：上层依赖下层，下层不依赖上层。LLM 层只管叙事 + 调用引擎函数，不自行计算或拼数据。

---
## 模式与手动骰

- **模式（mode）**：系统支持两种运行模式：`adventurer`（默认）和 `gm_assist`。
  - `adventurer`：引擎按规则自动执行掷骰与结算，玩家不干预骰面结果。
  - `gm_assist`：城主辅助模式，允许通过 MCP 工具预设「手动骰」，用于演示、复现或争议裁定。
- **选择时机**：在新游戏启动时选择（例：`start_new_game(mode="gm_assist")`）。
- **MCP 工具**：`start_new_game(mode)`、`get_mode()`、`set_manual_roll(name, value)`、`list_manual_rolls()`、`clear_manual_rolls()`。
- **行为**：`gm_assist` 且存在手动骰时，掷骰函数优先使用手动骰并记录使用历史；否则正常随机掷骰。
- **透明性要求**：所有手动骰操作必须在会话内记录并可查询，避免秘密修改。

---
## 快速开始 — 安装指引

### 步骤 1：解压到工作目录

将 `dnd-dm-skill-x.x.x.zip` 解压到空目录即可使用。

```
your-workspace/
├── SKILL.md / _meta.json
├── references/             ← 核心规则文件（供 LLM 读取）
│   └── party-sheet.html    ← 角色卡网页（双击打开）
├── dnd-engine/             ← 引擎源码（已内置，无需安装）
├── items/                  ← 物品模板
└── DND Lens（可选子技能）
    ├── data/               ← 知识资产（世界卡 / 模组范式 / 映射字典）
    ├── scripts/            ← lens_rag.py（BM25 中文检索）+ lens_pipeline.py
    ├── world-lore/         ← 功能一：世界观 / 编年史检索
    ├── module-forge/       ← 功能二：按需求生成模组
    └── echo-map/           ← 功能三：真实经历 → DND 映射
```

### 步骤 2：放入规则书和模组

> ⚠️ **需用户自行准备**：规则书和模组因版权原因无法随 Skill 分发。

将 2024版三宝书放入 `rules/` 目录，模组文件放入 `modules/` 目录。

### 步骤 3：校验并开玩

在对话中回复 `/verify`，Agent 自动校验环境。通过后即可开始游戏。

*首次使用时 LLM 会自动加载引擎：`import sys; sys.path.insert(0, "dnd-engine")`*

---
## 一条命令完成检定（推荐）

```bash
dnd-check --actor 老白 --skill 潜行 --dc 15       # Windows 用 dnd-check.cmd
dnd-check --actor 老白 --ac 16                   # 攻击检定（走 AC）
```

自动读 `live_party.json`、组装加值、投骰，输出即为可直接贴给玩家的明细。
实测 **≈0.13 秒/次**（含 Python 启动）。**不要为了调引擎去写临时 Python 脚本。**
参数与“角色卡缺技能信息怎么办”见 `references/DM_RULES.md` 规则 1.2.1。

---
## 相关技能

| 技能 | 作用 | 配合方式 |
|:----|------|---------|
| **`dnd-dm`（本技能）** | 城主行为规则 + 三层架构调度 | 主技能，定义 DM 如何行动 |
| **`dnd5e-srd`** | SRD 5.2.1 RAG 检索 | 战时快速查规则，通过 Python 脚本搜索+展开引用 |
| **`dnd-dm-skill:world-lore`** | 功能一·世界观对话 + 费伦编年史 | RAG 检索 `world_cards.jsonl`，托尔金式叙述 |
| **`dnd-dm-skill:module-forge`** | 功能二·按需求生成模组 | 选范式 + DMG 标准 CR 平衡，输出模组骨架 JSON |
| **`dnd-dm-skill:echo-map`** | 功能三·真实经历→DND 映射 | 脱敏 + 按 `mapping_dict` 映射，输出 anonymized 模组 |

---
## 子技能 · DND Lens（世界观 / 模组 / 经历映射）

> 宿主于本技能下的三件套，共享 `scripts/lens_rag.py`（BM25 中文检索）与 `data/` 知识资产。三者可独立调用，也可串联：真实经历 → echo-map 映射 → module-forge 做 CR 平衡 → world-lore 检索设定锚点。

| 子技能 | 触发场景 | 数据资产 | 入口脚本 |
|:----|:-----|:-----|:-----|
| **world-lore** | 「深水城历史是怎样的？」「给我讲一段阴影帝国编年史」 | `data/world_cards.jsonl`（360 张知识卡） | `world-lore/scripts/lore_query.py` |
| **module-forge** | 「4 人 5 级、玩一晚的都市寻宝模组」 | `data/module_paradigms.json`（59 篇范式）+ DMG 表 | `module-forge/scripts/module_forge.py` |
| **echo-map** | 「把我和甲方的扯皮改成冒险」 | `data/mapping_dict.json`（8 槽位 + 脱敏池） | `echo-map/scripts/echo_map.py` |

> **一键串联**：经历 → 映射 → 平衡 → 背景，运行 `python scripts/lens_pipeline.py --story 经历.txt --names "张三" --places "上海" --players 4 --level 5 --duration medium`（详见脚本头部说明）。

调用方式（**相对本技能目录**，用当前环境的 Python 运行）：

```bash
# 功能一：世界观 / 编年史检索
python scripts/lens_rag.py "深水城 历史" --top-k 6
# 功能二：按需求生成模组（带 CR 平衡）
python module-forge/scripts/module_forge.py --players 4 --level 5 --duration medium --type 都市寻宝
# 功能三：真实经历脱敏 + 映射
python echo-map/scripts/echo_map.py anonymize --names "张三" --places "上海"
```

> 数据流：各子技能脚本通过 `sys.path` 复用 `scripts/lens_rag.py`；数据目录默认 `data/`，可用环境变量 `DND_LENS_DATA` 覆盖。

---
## 功能概览

### 三层架构

| 层级 | 名称 | 技术栈 | 核心职责 |
|:----:|:-----|:-------|:---------|
| **LLM 层** | dnd-dm Skill | Markdown + prompt | 叙事、NPC、检定发起、行为红线——不可代码化 |
| **API 层** | dnd-api | FastAPI（端口自动检测） | 30 个 HTTP 端点 + CLI 命令行工具 |
| **引擎层** | dnd-engine | pip 包, Python 3.10+ | 骰子/战斗/存档/世界状态/模组缓存/判定/叙事后端——纯函数 |

新增/修改功能时按 **DM_DEV_GUIDE.md 开发规则9** 做三层分析。

### 判定层（1.2.1 新增）

**问题**：LLM 直接决定「要不要检定 / 投什么技能 / DC 多少」时，同一条输入会给出不同答案，且无法审计。

**做法**：把判定拆成「批量原子提问 → 类型化回答 → 代码组合成 `DecisionPacket` → 引擎结算」。

- 三原语：`Choice`（选一个）、`Score`（打 0–1 分）、`Noul`（是/否）。
- 优先级链（经 106 条探针实测标定）：
  1. **要不要检定**：模型有把握就听模型；低置信时用规则表强命中补位。
  2. **投什么技能**：模组关键词 > 规则表强命中 > 模型高置信 > 模型低置信。
  3. **DC**：模组原文 > 规则表 > 模型档位 > 默认档。
- 置信度门控：门限 `0.60`；低于门限的字段回退本地依据并记入 `low_confidence_fields`。
- 契约保护：模型输出非法 → 先尝试一次修复 → 仍失败则回退**纯规则**路径（`contract_error:...`），不会让游戏卡住。
- 确定性兜底：本地规则表 + `check_rules.json` 映射始终可用，**不依赖任何外部模型**。

### 叙事层（1.2.1 新增）

**问题**：长模组（40 万 token 级）每轮整份注入，导致成本高、首字慢、且剧情状态无处落地。

**做法**：四级注入 + 确定性节点图 + 一轮一次调用。

- 四级注入预算：`L0` 骨架 ≈ 300 tok / `L1` 当前场景 2–4k / `L2` 邻域摘要 ≈ 600 / `L3` 按需全文。实测每轮注入 **52.9k → 6.1k tok**。
- 确定性剧情图：`module_plot.json`（节点+边）+ `plot_state.json`（当前节点/已访问/事件）。推进由代码裁决，不由模型自由发挥。
- 一轮一次调用：叙事文本与类型化 `delta` 一次返回，实测 **3 次 → 1 次**。
- 前缀分层（prefix cache）：`system`（契约）/ `user-stable`（队伍+本章索引）/ `user-volatile`（本轮变化）。实测 **88% 输入命中缓存**。
- 流式输出：边收边增量解析 `narration` 字段，实测首字 **≈2.6 s** 出现。
- 预取：后继场景切片先做批量相关性筛选并缓存（按前缀签名失效）；可选预热稳定前缀。
- 防出戏守卫：叙事若出现内部字段名/节点编号/内部术语 → 触发一次修复 → 仍泄漏则 **fail closed**，宁可不输出。

### 规则裁决

- 严格按 **2024版** 规则结算（6步检定流程）
- 检定公式由 `dnd_engine.combat.checks` 结构化返回，LLM 仅展示结果
- 数据模板由 `dnd_engine.save.templates` 工厂生成，LLM 不自拼 JSON
- 自然1不重投，公平透明
- 26 条运行规则按 **6层架构** 组织（每条规则有 `<!-- layer: N -->` 标记）

### 战斗系统

- 引擎层：命中/伤害/豁免检定/战斗状态 CRUD——代码化
- 多重攻击：敌人按 `multiattack` 真打 N 次（上限 4 次）
- 抗性/免疫/易伤参与结算（免疫×0、抗性×0.5、易伤×2，双向生效）；伤害类型用中文关键词匹配
- 敌人 AI：每敌 4 问（action / target_policy / attack / morale），引擎把策略解成具体目标；HP≤33% 且士气不足时**强制撤退**
- 战斗状态持久化到 `combat_state.json`
- 一键决议：`POST /api/combat/resolve-round` 合并命中+伤害+状态更新

### 信息展示

- 渐进式探索引导（§9.2）：幕前自然语言暗示 + 幕后 `_scene_cache_*.json` 追踪房间
- 检定结果直接输出 `checks.py` 的 `detail_lines` 数组，格式由代码保证
- 任务清单、角色卡、法术展示——标准模板
- 角色卡网页：`party-sheet.html` 双击即可查看队伍状态

### 角色创建

- 7阶段对话式创建，属性 `roll_stat()` 由引擎层执行
- 自动生成 `live_party.json` 和角色卡

### 存档系统（引擎层）

- `dnd_engine.save.io`：`write_save()` / `load_save()` / `list_saves()`
- 场景缓存自动嵌入存档（`scene_cache.py`）
- 模板工厂：`make_character_template()` / `make_save_template()` / `make_quest_template()`

### CLI 命令行

| 命令 | 功能 |
|:-----|:------|
| `dnd-engine` | 初始化工作目录（创建 saves/ rules/ modules/ live_party.json） |
| `dnd-engine verify` | 校验环境（直接调用 `dnd_engine.verify.verify_environment()`） |
| `dnd-engine server --port auto` | 启动 API 服务（自动检测端口） |

### API 接口（dnd-api，共30个端点）

**骰子：**

| 接口 | 功能 |
|:-----|:------|
| `POST /api/roll` | 骰子表达式求值 |

**战斗：**

| 接口 | 功能 |
|:-----|:------|
| `POST /api/combat/check-hit` | 命中判定 |
| `POST /api/combat/calc-damage` | 伤害结算 |
| `POST /api/combat/skill-check` | 技能检定（完整公式） |
| `POST /api/combat/state/*` | 战斗状态 CRUD（6 端点） |
| `POST /api/combat/resolve-round` | 一键命中+伤害+状态更新 |
| `POST /api/combat/roll-initiative` | 一键掷先攻+排序 |

**队伍：**

| 接口 | 功能 |
|:-----|:------|
| `POST /api/party/calc-combat-xp` | XP 计算 |
| `POST /api/party/rest` | 短休/长休结算 |
| `GET /api/party/character/{name}` | 角色属性查询 |
| `POST /api/party/level-up` | 升级自动结算 |
| `GET /api/party/live` | 实时角色状态 |
| `POST /api/party/live/rebuild` | 从存档重建实时状态 |

**存档：**

| 接口 | 功能 |
|:-----|:------|
| `GET /api/saves/list` | 存档列表 |
| `POST /api/saves/load` | 读档 |
| `POST /api/saves/write` | 存档 |

**SRD：**

| 接口 | 功能 |
|:-----|:------|
| `GET /api/srd/search?q=` | SRD 全文搜索 |
| `POST /api/srd/expand` | 展开上下文 |
| `GET /api/srd/files` | 查询 SRD 文件列表 |
| `GET /api/srd/search-in-file` | 在指定文件中搜索 |

**系统：**

| 接口 | 功能 |
|:-----|:------|
| `GET /api/system/verify` | 预飞校验：引用文件、引擎、权限 |
| `POST /api/system/init` | 自动创建工作目录 |
| `GET /api/system/port` | 查询当前 API 端口 |

**世界状态：**

| 接口 | 功能 |
|:-----|:------|
| `GET /api/state/world` | 世界状态 |

### 行为红线（15条，不可越界）

1. **NO 偏离模组**：禁止自创与模组无关的大段剧情
2. **NO 无底线乱搞**：严禁任何 R18G 交互描述
3. **NO 放水求爱**：严禁修改怪物数据以迎合剧情
4. **NO 打断真骰**：自然 1 不重投，包括关键剧情检定
5. **NO 反刍世界观**：不混用博德之门3游戏设定与模组设定
6. **NO 规则混淆**：不使用 2014 版旧规则覆盖 2024 版新规则
7. **NO 成年人黑暗内容**：涉未成年人零容忍
8. **NO 全知推理**：DM 不替 NPC 知晓玩家未公开的战术
9. 禁止 LLM 自行计算 AC/DC/检定格式——必须调引擎层
10. 禁止 LLM 自行生成 Python 脚本执行——必须用 import 或 API 调用

### 6层规则架构

DM_RULES.md 中 26 条运行规则按 6 层组织，每条规则开头有 `<!-- layer: N -->` 标记。加载时按层优先级常驻：

| 层 | 名称 | 包含规则 | 常驻时段 |
|:--:|:-----|:---------|:---------|
| **0** | 全局基石 | 0(会话启动), 0a(模组选择), 0.5(微互动), 10(红线), 18(代码), 19(Token), 21(安装) | 整个会话 |
| **1** | 运行时交互 | 1(检定), 1.5(叙事匹配), 2(场景空间), 3(推进), 4(支线), 17(不泄题), 20(回声) | 每次场景 |
| **2** | 展示模板 | 2b(地图), 9(信息展示) | 展示信息时 |
| **3** | 战斗系统 | 15(回合), 15b(装备) | 战斗回合 |
| **4** | 进度与状态 | 5(经验), 7(锚点), 8(章节), 13(存档), 14(存档), 16(实时状态) | 存档/升级 |
| **5** | 模组控制 | 12(构建), X(特殊) | 开新局/跨章 |

---
## 文件说明

| 文件/目录 | 说明 |
|:----------|:------|
| `references/` | 14 个核心引用文件（规则、模板、开发指南、人格定义、角色卡模板） |
| `items/` | 物品模板目录（3 个 .md） |
| `srd/` | SRD 5.2.1 检索资源（references + scripts） |
| `dnd-engine/src/dnd_engine/` | 引擎层 Python 包（dice/combat/party/save/state/module/npc/runtime/context/judge/narrative/cli） |
| `dnd-check.py` + `.cmd` / `.sh` | **一条命令完成一次检定**（自己把包内引擎加进 `sys.path`，不依赖 PYTHONPATH；读 `live_party.json`、组装加值、投骰） |
| `data/` | [DND Lens] 共享知识资产：`world_cards.jsonl`（360 张知识卡）/ `module_paradigms.json`（59 篇范式）/ `mapping_dict.json`（8 映射槽位） |
| `scripts/lens_rag.py` | [DND Lens] BM25 中文检索引擎，RAG 底座，三子技能共用 |
| `scripts/lens_pipeline.py` | [DND Lens] 联动流水线：经历 → echo-map → module-forge → world-lore 一站式（见脚本内 `--help`） |
| `world-lore/` | [DND Lens·功能一] 世界观对话 + 费伦编年史子技能 |
| `module-forge/` | [DND Lens·功能二] 按需求生成模组（DMG 标准 CR 平衡）子技能 |
| `echo-map/` | [DND Lens·功能三] 真实经历 → DND 映射（脱敏 + 字典规范化）子技能 |
| `saves/` | [自动生成] 存档文件 |
| `rules/` | [自行准备] 2024版三宝书 |
| `modules/` | [自行准备] D&D 模组文件 |
| `party-sheet.html` | 角色卡网页（双击即看，从 live_party.json 读取） |
| `live_party.json` | [自动生成] 实时角色状态 |
| `_api_port.txt` | [自动生成] API 运行端口 |
| `_scene_cache_*.json` | [自动生成] 场景缓存 |
| `reports/prefetch_cache.json` | [自动生成] 叙事预取缓存 |

---
*版本 1.2.1 · 2026-09-25 · 合并发布：线上 1.2.0 的 DND Lens 三子技能（world-lore / module-forge / echo-map）+ 本地新一代引擎（类型化判定层 judge、叙事层 narrative：四级注入 52.9k→6.1k tok、一轮一次调用、prefix cache 命中 88%、流式首字 2.6s、防出戏守卫）· 严格按 2024版 D&D 5e 规则 · 220 项测试通过 · 支持 Windows / macOS / Linux*
