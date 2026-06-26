---

name: dnd-dm

description: "AI 地下城主引擎 —— 基于2024版D&D 5e规则，三层架构（dnd-engine + dnd-api + dnd-dm Skill），支持模组化运行、战斗裁决、角色创建与存档管理"

homepage: https://github.com/laobaigan/dnd-engine

user-invocable: true

metadata:

  {"openclaw": {"emoji": "🎲", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["python3", "pip"]}}}
version: 1.1.8
---

# D&D 5e AI 地下城主引擎 — 三层架构

基于 **2024版 D&D 5e 规则** 的 AI 地下城主系统。纯对话交互，无需专用客户端，任何 IM 软件即可运行。本 Skill 将 DM（地下城主）角色交给 AI，严格按照模组剧本和规则书推进游戏。

**城主人格**：明萨拉·班瑞（Minthara Baenre）——守序邪恶卓尔圣武士，前魔索布莱城贵族。语气霸道、果断、直接，但绝不放水作弊。详见 [SOUL.md](file:///E:/AI/DND/references/SOUL.md) 和 [IDENTITY.md](file:///E:/AI/DND/references/IDENTITY.md)。

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

│  引擎层：dnd-engine（已内置）            │

│  骰子、战斗、存档、世界状态、模组缓存、SRD 搜索 │

│  ← 纯 Python，零 LLM 依赖，90 项测试覆盖       │

└─────────────────────────────────────────────┘

```

**核心原则**：上层依赖下层，下层不依赖上层。LLM 层只管叙事 + 调用引擎函数，不自行计算或拼数据。

---

## 快速开始 — 安装指引

### ▸ 步骤 1：解压到工作目录

将 `dnd-dm-skill-x.x.x.zip` 解压到空目录即可使用。

```

your-workspace/

├── SKILL.md / _meta.json

├── references/             ← 核心规则文件（供 LLM 读取）

│   └── party-sheet.html    ← 角色卡网页（双击打开）

├── dnd-engine/             ← 引擎源码（已内置，无需安装）

└── items/                  ← 物品模板

```

### ▸ 步骤 2：放入规则书和模组

> ⚠️ **需用户自行准备**：规则书和模组因版权原因无法随 Skill 分发。

将 2024版三宝书放入 `rules/` 目录，模组文件放入 `modules/` 目录。

### ▸ 步骤 3：校验并开玩

在对话中回复 `/verify`，Agent 自动校验环境。通过后即可开始游戏。

*首次使用时 LLM 会自动加载引擎：`import sys; sys.path.insert(0, "dnd-engine")`*

---

## 相关技能

| 技能 | 作用 | 配合方式 |

|:----|------|---------|

| **`dnd-dm`（本技能）** | 城主行为规则 + 三层架构调度 | 主技能，定义 DM 如何行动 |

| **`dnd5e-srd`** | SRD 5.2.1 RAG 检索 | 战时快速查规则，通过 Python 脚本搜索+展开引用 |

---

## 功能概览

### 🏗️ 三层架构

| 层级 | 名称 | 技术栈 | 核心职责 |

|:----:|:-----|:-------|:---------|

| **LLM 层** | dnd-dm Skill | Markdown + prompt | 叙事、NPC、检定发起、行为红线——不可代码化 |

| **API 层** | dnd-api | FastAPI（端口自动检测） | 30 个 HTTP 端点 + CLI 命令行工具 |

| **引擎层** | dnd-engine | pip 包, Python 3.10+ | 骰子/战斗/存档/世界状态/模组缓存/SRD搜索——纯函数 |

新增/修改功能时按 **DM_DEV_GUIDE.md 开发规则9** 做三层分析。

### 📐 规则裁决

- 严格按 **2024版** 规则结算（6步检定流程）

- 检定公式由 `dnd_engine.combat.checks` 结构化返回，LLM 仅展示结果

- 数据模板由 `dnd_engine.save.templates` 工厂生成，LLM 不自拼 JSON

- 自然1不重投，公平透明

- 26 条运行规则按 **6层架构** 组织（每条规则有 `<!-- layer: N -->` 标记）

### ⚔️ 战斗系统

- 引擎层：命中/伤害/豁免检定/战斗状态 CRUD——代码化

- LLM 层：战斗叙事、旁白、态势表渲染

- 战斗状态持久化到 `combat_state.json`

- 一键决议：`POST /api/combat/resolve-round` 合并命中+伤害+状态更新

### 📋 信息展示

- 渐进式探索引导（§9.2）：幕前自然语言暗示 + 幕后 `_scene_cache_*.json` 追踪房间

- 检定结果直接输出 `checks.py` 的 `detail_lines` 数组，格式由代码保证

- 任务清单、角色卡、法术展示——标准模板

- 角色卡网页：`party-sheet.html` 双击即可查看队伍状态

### 🧙 角色创建

- 7阶段对话式创建，属性 `roll_stat()` 由引擎层执行

- 自动生成 `live_party.json` 和角色卡

### 💾 存档系统（引擎层）

- `dnd_engine.save.io`：`write_save()` / `load_save()` / `list_saves()`

- 场景缓存自动嵌入存档（`scene_cache.py`）

- 模板工厂：`make_character_template()` / `make_save_template()` / `make_quest_template()`

### 🛠️ CLI 命令行

| 命令 | 功能 |

|:-----|:------|

| `dnd-engine（已内置）` | 初始化工作目录（创建 saves/ rules/ modules/ live_party.json） |

| `dnd-engine verify` | 校验环境（需 API 运行中） |

| `dnd-engine server --port auto` | 启动 API 服务（自动检测端口） |

### 🌐 API 接口（dnd-api，共30个端点）

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

### 🔒 行为红线（15条，不可越界）

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

| `dnd-engine/` | [已弃用] 旧代码模板库（25 个 .py，兼容保留） |

| `items/` | 物品模板目录（3 个 .md） |

| `dnd-engine/` | 引擎层 + API 层全套源码 |

| `dnd-engine/src/dnd_engine/` | 引擎层 Python 包（dice/combat/party/save/state/module/cli） |

| `dnd-engine/api/server.py` | FastAPI 服务（30 端点，端口自动检测） |

| `dnd-engine/tests/` | pytest 测试（90 项） |

| `saves/` | [自动生成] 存档文件 |

| `rules/` | [自行准备] 2024版三宝书 |

| `modules/` | [自行准备] D&D 模组文件 |

| `party-sheet.html` | 角色卡网页（双击即看，从 live_party.json 读取） |

| `live_party.json` | [自动生成] 实时角色状态 |

| `_api_port.txt` | [自动生成] API 运行端口 |

| `_scene_cache_*.json` | [自动生成] 场景缓存 |

---

*****版本 1.1.8 · 2026-06-09 · 角色卡模板旧数据清空(空状态引导), DM_DEV_GUIDE添加发布前四步检查链(§8.3) · 三层架构（dnd-engine + dnd-api + dnd-dm Skill）· 基于2024版D&D 5e规则 · 90项测试全部通过 · 支持 Windows / macOS / Linux*

