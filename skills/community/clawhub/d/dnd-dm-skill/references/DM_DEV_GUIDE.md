# DM 城主系统开发规则


本文件指导 **城主系统的开发与维护**（即 AI 在收到老白干一杯的更新要求时如何操作），与 `DM_RULES.md`（指导游戏运行）分离。


---


## 开发规则1：规则冲突先问再改


如果收到更新要求时，发现新要求与已有规则存在**重大矛盾**（即完全无法共存、不可调和），执行以下流程：


```

收到更新要求

    ↓

检查是否与已有规则矛盾

    ↓

  ✅ 无矛盾 → 直接写入新规则

  ❌ 有重大矛盾 → 执行矛盾处理流程

```


### 矛盾处理流程


1. **指出矛盾点**：明确说明新要求和哪条现有规则冲突，冲突的具体内容是什么

2. **提出优化方案**：至少提出 1-2 种可行的修改方案（如：删除旧规则、修改旧规则、调整新要求）

3. **询问修改方向**：由老白干一杯决定采用哪个方案，不得自行选择


### 示例


> **用户要求**："战斗中玩家可以每轮使用两个附赠动作。"

>

> **矛盾检查**：

> - ❌ 与现有规则的"动作经济"冲突——2024版规则每轮只有一个附赠动作

> - 这是规则层级的根本矛盾，不是微调

>

> **响应**：

> "这个要求与现有规则有重大矛盾：2024版核心规则规定每轮只有1个附赠动作，改为2个会彻底改变动作经济系统。

>

> 优化方案：

> 1. 将这条作为模组特殊规则写入，覆盖标准规则

> 2. 修改玩家的要求为'获得一个额外附赠动作的专长/特性'

> 3. 拒绝此修改，维持标准规则

>

> 请决定采用哪个方案。"


---


## 开发规则2：填充内容追踪维护


城主必须在 `工作目录\filled_content.md` 文件中记录所有已使用的填充内容，包括：

- 填充内容出现的时间（游戏内时间/场景名称）

- 简要描述（NPC、地点、物品、事件）

- 该内容是否已结束或被废弃


**文件维护：** 每次使用新的填充内容后，立即更新该文件。


---


## 开发规则3：模组内容自动构建


### 3.1 原则


每个模组的具体加载信息（章节文件列表、关键节点清单、事件流程图、NPC名册等）不应硬编码在规则中，而应在模组启动时从模组剧本文件中解析构建。


### 3.2 启动时构建的内容


当新模组启动时（新开一局），自动构建以下内容：


**① 模组章节结构** `MODULE_STRUCTURE.md`

- 列出所有章节文件的加载顺序

- 每章的等级范围

- 里程碑升级节点

- 章节出口/进入下章的条件


**② 关键节点清单** `MODULE_NODES.md`

- 所有关键节点的编号、名称、触发条件

- 模组文本中的原文位置（文件名+行号/段落标记）

- 已完成/未完成状态追踪


**③ 章节流程图** `MODULE_FLOW.md`

- 关键节点的可视化流程图（文本版）

- 事件之间的分支与依赖关系


**④ NPC 名册**（集成在 `MODULE_INDEX.md` 中）

- 关键NPC姓名、角色、位置、命运


### 3.3 构建方式


读取模组所有章节文件后，分析以下结构：


- **文件命名模式**：如 `Ch.1`、`Ch. 1`、`Chapter 1` 等章节标记

- **事件标记**：如 "**遭遇**"、"**事件**"、"**场景**" 等段落标题

- **NPC 定义**：首次出现时的全名和描述

- **等级范围**：模组文件开头或附录中的等级信息


输出的文件以 `MODULE_*` 命名，存放在工作目录下。


---


## 开发规则4：代码模板库（运行时Token优化核心策略）


### 4.0 核心目标


**在城主系统运行过程中，用预构建函数代替 LLM 逐次生成代码，最大幅度减少 Token 消耗。**


每轮对话中消耗 Token 最严重的环节：


| 环节 | 问题 | 优化方案 | 节省量 |

|------|------|---------|:-----:|

| 战斗轮次追踪 | LLM 需从历史消息中提取HP/状态/位置 | `combat_state.json` 持久化状态 | 🔴极高 |

| 模块文件读取 | 每次切换到新场景都需重读文件 | `module_cache.json` 缓存 | 🔴极高 |

| 攻击/伤害描述 | LLM 每次构造格式化文本 | `formulas.py` 预定义格式串 | 🟡高 |

| 存档格式构造 | LLM 每次构建完整JSON | `save/templates.py` 预定义结构 | 🟡高 |

| 规则查询 | LLM 翻阅整篇DM_RULES.md | `quickref.py` 速查函数 | 🟡中 |


运行过程中，通过自然语言生成的代码必须经过函数化改造后记录到 `dnd-engine/` 代码库中，以便下次直接调用。


### 4.1 使用流程


```

需要实现某个功能时

    ↓

搜索 dnd-engine/src/dnd_engine/README.md

    ↓

  ✅ 找到匹配函数 → 直接调用，参数按文档填写

  ❌ 找不到匹配函数 → 由大模型生成代码

                          ↓

                    函数化改造（封装 def）

                          ↓

                    登记到 dnd-engine/ 对应目录

                          ↓

                    更新 CODE_LIBRARY.md 索引

```


### 4.2 代码模板要求


每次新增代码必须满足：


1. **函数化**：封装为函数，有明确的 `def func_name(params) -> return_type`

2. **文档化**：函数必须有 docstring（参数说明、返回值说明、调用示例）

3. **分类存放**：放入 `dnd-engine/src/dnd_engine/<category>/<filename>.py`

4. **索引登记**：在 `CODE_LIBRARY.md` 的对应分类下添加条目


### 4.3 分类规则


| 分类 | 目录 | 内容 |

|------|------|------|

| 🎲 骰子 | `dnd-engine/src/dnd_engine/dice/` | 投骰、随机数、属性生成 |

| ⚔️ 战斗 | `dnd-engine/src/dnd_engine/combat/` | 先攻表、命中判断、伤害结算 |

| 💾 存档 | `dnd-engine/src/dnd_engine/save/` | 存档读写、自动编号 |

| 📦 模组 | `dnd-engine/src/dnd_engine/module/` | 模组扫描、章节解析、结构构建 |

| 👥 角色 | `dnd-engine/src/dnd_engine/party/` | 角色状态、经验计算、物品检索 |


### 4.4 目录结构


```

dnd-engine/src/dnd_engine/

├── CODE_LIBRARY.md    ← 主索引（函数名→描述→文件路径）

├── QUICK_REF.py       ← 快速参考（函数签名速查）

├── dice/rolls.py      ← 骰子操作

├── combat/display.py  ← 战斗展示

├── combat/resolve.py  ← 战斗解析

├── save/io.py          ← 存档读写

├── module/scanner.py  ← 模组扫描

├── module/builder.py  ← 模组文件构建

├── party/live.py      ← 角色状态管理

└── party/xp.py        ← 经验计算

```


### 4.5 检索优先原则


- **强制优先检索**：需要任何代码功能时，先查 `CODE_LIBRARY.md`，有现成函数直接调用

- **无匹配再生成**：确认代码库中没有类似函数后，才通过大模型生成新代码

- **新代码入库**：新生成的代码必须履行函数化登记流程

- **定期整理**：发现重复功能的代码时，合并为统一函数，删除冗余


---


## 开发规则5：模板-代码双向同步


### 5.1 核心原则


`DM_TEMPLATES.md` 中定义的输出模板（如战斗表格式、法术展示表、角色卡布局等）与 `dnd-engine/` 中对应的生成函数**必须保持同步**。模板改 → 代码改，反之亦然。


### 5.2 映射关系


| 模板 | 对应代码函数 | 同步要点 |

|------|------------|---------|

| DM_TEMPLATES.md 9.1 剧情整理 | 无（纯文本模板，无代码依赖） | — |

| DM_TEMPLATES.md 9.2 房间布局 | 无（纯文本模板） | — |

| DM_TEMPLATES.md 9.3 战斗态势表 | `dnd-engine/src/dnd_engine/combat/display.py:build_combat_table()` | 列顺序/列名/格式必须一致 |

| DM_TEMPLATES.md 9.4 地形图 | `dnd-engine/src/dnd_engine/combat/formulas.py:environment_text()` | 地形/光线/特殊字段顺序一致 |

| DM_TEMPLATES.md 9.5 任务清单 | `dnd-engine/src/dnd_engine/save/templates.py:new_quest_template()` | 任务状态字段格式一致 |

| DM_TEMPLATES.md 9.6 角色卡 | `dnd-engine/src/dnd_engine/party/live.py:get_all_characters()` | 属性顺序/装备展示方式一致 |

| DM_TEMPLATES.md 9.7 队伍总览 | `dnd-engine/src/dnd_engine/party/live.py:get_party_summary()` | 摘要字段一致 |

| DM_TEMPLATES.md 规则11 法术展示 | 无独立函数（由LLM查模板直接生成） | 模板改后LLM输出自动同步 |


### 5.3 触发同步的变更类型


以下变更要求同时更新 `DM_TEMPLATES.md` 和 `dnd-engine/`：


1. **列增加/删除/重命名**：如战斗表增加"状态效果"列 → `build_combat_table()` 必须同步修改

2. **格式调整**：如角色卡从多行改为表格 → `get_all_characters()` 输出格式同步

3. **新增展示类型**：如新增"NPC关系图"模板 → 生成对应函数并入库

4. **字段排序变更**：代码输出的字段顺序必须与模板中列的顺序一致


### 5.4 不同步的后果


- 玩家看到的展示（来自模板）与代码计算的结果（来自函数）不一致

- LLM 引用代码的输出后，再按模板格式化时出现重复或冲突

- `combat_state.json` 的字段与战斗表模板列不匹配，导致输出错乱

- 存档升级时无法正确恢复角色数据（字段名不匹配）


### 5.5 执行流程


```

需要修改模板 → 在 DM_TEMPLATES.md 中修改

    ↓

查找 dnd-engine/src/dnd_engine/README.md 中对应的生成函数

    ↓

同步修改函数参数/返回格式/输出文本

    ↓

验证：运行函数查看输出是否与模板一致

    ↓

更新 CODE_LIBRARY.md 函数签名文档（如参数变化）

    ↓

通知：告知玩家"模板[名称]已更新，对应代码已同步"

```


---


## 开发规则6：SRD代码优先引用


### 6.0 核心原则


> **在 dnd-engine/src/dnd_engine/ 代码库新增任何函数前，必须优先检索 srd/scripts/ 中的 Python 脚本是否能满足需求。SRD 已有功能的，强制引用 SRD 代码，禁止重复造轮。**


安装 dnd5e-srd skill 后，工作目录 srd/ 提供了完整的 SRD 5.2.1 RAG 检索能力（search_with_positions.py + expand_context.py），覆盖法术数据、职业特性、装备参数、怪物数据、状态定义等大量结构化数据。在 dnd-engine/ 中新增函数时，如所需数据 SRD 已有，优先通过搜索脚本获取，而非自建数据库或硬编码数据。


### 6.1 检索优先级


```

玩家提出新的交互需求 -> 需要代码实现

    |

第一步：搜索 srd/scripts/ 能否满足

    |

  [OK] SRD 搜索可直接覆盖 -> 在 dnd-engine/ 中创建引用函数，内部调用 SRD 脚本

  [OK] SRD 可提供所需数据 -> 在 dnd-engine/ 中创建数据提取函数，寄生 SRD 搜索

  [NO] SRD 无法覆盖 -> 才走 开发规则4 的代码生成流程

```


### 6.2 "SRD 覆盖" 的判断标准


只有以下情况才判定为 "SRD 无法覆盖"：


1. **非 SRD 内容**：玩家要求实现的内容不包含在 SRD 5.2.1 中（如自制规则、模组专有物品、自定义法术）

2. **需要写入本地状态**：功能涉及写入文件（存档、战斗状态、角色数据），SRD 脚本是只读搜索

3. **纯计算逻辑**：如 XP 计算、先攻排序、概率运算等，这些 SRD 不提供函数

4. **交互操作**：需要读取/写入 live_party.json、combat_state.json 等运行时文件


以下情况**判定为 SRD 可覆盖**：


1. **查询某条规则定义** -> 用 search_with_positions.py 搜索关键词

2. **查询某个法术数据** -> 搜索法术名

3. **查询某个怪物数据** -> 搜索怪物名

4. **查询某个装备属性** -> 搜索装备名

5. **查询某个状态效果** -> 搜索状态名称


### 6.3 引用 SRD 的代码模式


当判定为 SRD 可覆盖时，在 dnd-engine/ 中创建轻量包装函数，而非复制 SRD 数据：


```python

def lookup_spell(spell_name: str) -> str:

    # 正确做法：包装函数，调用 SRD 脚本

    # ✅ 改用 API 调用，比 exec 子进程快 10-100 倍

    import urllib.request, json, urllib.parse

    base = "http://localhost:8081"

    r = json.loads(urllib.request.urlopen(

        base + "/api/srd/search?q=" + urllib.parse.quote(spell_name)

    ).read())

    if r["results"]:

        # expand first result

        res = r["results"][0]

        data = json.dumps({"filename": res["file"].split(chr(92))[-1],

                          "position": res["char_start"],

                          "match_text": res["match_text"][:30],

                          "mode": "paragraph"}).encode()

        expanded = json.loads(urllib.request.urlopen(

            urllib.request.Request(base + "/api/srd/expand", data=data,

                                  headers={"Content-Type": "application/json"})

        ).read())

        return expanded["context"]

    return "未找到"

```


### 6.4 代码索引标注


在 CODE_LIBRARY.md 中登记的每个函数，新增一列标注数据来源：


| 函数 | 来源 | 说明 |

|------|------|------|

| lookup_spell() | srd | 包装 SRD 搜索脚本 |

| calc_combat_xp() | 本地 | 纯计算逻辑 |

| write_save() | 本地 | 文件 I/O |


### 6.5 SRD 脚本引用示例


```bash

# 战斗时查询法术

python srd/scripts/search_with_positions.py "fireball" --all

python srd/scripts/expand_context.py "fireball" --result 1 --mode section --all


# 查询怪物

python srd/scripts/search_with_positions.py "Aboleth" --all

python srd/scripts/expand_context.py "Aboleth" --result 1 --mode section --all


# 查询状态

python srd/scripts/search_with_positions.py "Charmed" --all

python srd/scripts/expand_context.py "Charmed" --result 1 --mode section --all


# 查询装备

python srd/scripts/search_with_positions.py "longsword" --all

python srd/scripts/expand_context.py "longsword" --result 1 --mode section --all

```


### 6.6 与开发规则4的整合


开发规则4（代码模板库）中的 "检索优先原则" 流程扩展为：


```

需要实现某个功能时

    |

第一步：搜索 srd/scripts/ 能否满足

  [OK] SRD 覆盖 -> 创建包装函数引用 SRD

  [NO] SRD 无法覆盖 -> 走第二步

    |

第二步：搜索 dnd-engine/src/dnd_engine/README.md

  [OK] 找到匹配函数 -> 直接调用

  [NO] 找不到 -> 由大模型生成代码

    |

函数化改造 -> 登记到 dnd-engine/ -> 更新 CODE_LIBRARY.md

```


> **违反规则的后果**：若在 SRD 可覆盖的情况下仍自建数据（如手动硬编码法术列表到 dnd-engine/ 中），属于 **重复建设**。

> 这会导致：数据不同步（SRD 更新后本地硬编码不会自动更新）、代码膨胀、维护成本上升。


---


## 开发规则7：DM_RULES.md 中移入的开发流程（系统维护参考）


以下规则原本位于 DM_RULES.md，经审计后确认为开发/维护流程而非游戏运行规则，移至此处。


### 7.1 沙盒限制处理

（原 DM_RULES.md 规则18.3）


无法执行Python时：本地终端手动执行 → 结果粘贴 → 记录格式下次直接套用。


### 7.2 无匹配时兜底

（原 DM_RULES.md 规则18.4）


搜`CODE_LIBRARY.md` → 未找到 → LLM生成 → 函数化封装 → 登记入库 → 下次直接调用。


### 7.3 玩家新交互自动入库

（原 DM_RULES.md 规则18.5）


玩家提出新需求 → 生成函数 → 入库 `dnd-engine/src/dnd_engine/<category>/` → 更新 `CODE_LIBRARY.md` → 告知玩家已录入。


### 7.4 模板-代码同步约束

（原 DM_RULES.md 规则18.6）


`DM_TEMPLATES.md` 格式与 `dnd-engine/` 函数输出必须一致。模板改→代码改，反之亦然。参见开发规则5。


### 7.5 模块初始化流程

（原 DM_RULES.md 规则12.1）


```

玩家选择模组 → init_module(module_name)

                ↓

        自动生成所有数据文件（不依赖模组名）：

        ├─ MODULE_INDEX.md（通用索引模板）

        ├─ MODULE_ARC.md（通用运行结构模板）

        ├─ world_state.json（空状态，动态填充）

        └─ srd/scenes_index.json（第一章场景索引）

                ↓

        规则0a → 角色创建 → 开始游戏

```


**通用性保证**：

- 所有文件通过 `scan_modules()` 自动发现，无硬编码模组名

- `init.py` 生成的模板不包含任何特定模组的NPC/派系/任务数据

- 具体NPC/派系数据在模组运行过程中通过 `world_state.py` 动态填充

- `modules/` 目录中的任意 D&D 5e 模组均可使用


### 7.6 Token预算参考

（原 DM_RULES.md 规则19.4）


```

P0（常驻）:   SOUL(~2K) + 世界状态摘要(~0.1K) + 剧情摘要(~0.2K)  = ~2.3K

P1（场景）:   当前场景原文(~3-6K) + NPC索引条目(~0.5K)             = ~3.5-6.5K

P2（对话）:   最近5轮(~2K)                                         = ~2K

P3+P4（检索）:按需加载                                              = 0~3K

────────────────────────────────────────────────────

总计:                                                             = ~5.8K~12K

优化前:                                                           = ~50K-75K

预期节省:                                                         = 70-85%


---


## 开发规则8：版本发布完整性约束


生成新版 Skill 时（如 `DMskill/` 目录），**必须同时更新以下所有文件**，缺一不可：


| # | 文件路径 | 必须更新的内容 |

|:-:|----------|--------------|

| 1 | `DMskill/CHANGELOG_DM_v2.md` | 追加新版本条目（新增/改进/架构变更/技术细节） |

| 2 | **根目录 `CHANGELOG_DM_v2.md`** | 与 DMskill 中的版本完全一致，必须同步复制 |

| 3 | `DMskill/SKILL.md` | 更新 version 字段；更新 description；更新功能概览反映新功能；更新文件说明表；更新版本脚注 |

| 4 | `DMskill/_meta.json` | 更新 version 字段；更新 description（与 SKILL.md 一致） |


### 8.0 预发布：检查战斗生成的 .py 文件


每次发布新 Skill 版本前，检查工作目录中是否有战斗/运行期间生成的 `.py` 文件。

逐件分析：

- 功能有价值且可复用 → **移入 `dnd-engine/api/` 并注册为 API 端点**

- 已有对应实现 → **删除**

- 无价值 → **删除**


确认无遗留临时文件后再进行版本发布。


### 8.1 检查清单


每次版本发布完成后，执行以下验证：


```

☐ CHANGELOG: 根目录 + DMskill/ 两个文件均有新版本条目

☐ SKILL.md: version 字段改为最新版本号

☐ SKILL.md: description 体现新版本的功能亮点

☐ SKILL.md: 功能概览 / 文件说明 已同步更新

☐ SKILL.md: 脚注版本号已更新

☐ _meta.json: version 与 SKILL.md 一致

☐ _meta.json: description 与 SKILL.md 一致

☐ ZIP 包: 从 DMskill/ 目录重新打包

☐ ZIP 包: 无 __pycache__ 残留

```


### 8.2 违反后果


遗漏任何一个文件，会导致以下问题：

- 用户从 ClawHub 安装后看到旧版描述，误以为没有新功能

- `_meta.json` 中的 description 与实际版本不匹配，影响 ClawHub 搜索排序

- CHANGELOG 仅存在于 ZIP 内，根目录没有记录导致日志断裂

- 旧版 ZIP 包覆盖新版包文件，实际内容与版本号不匹配



### 8.3 发布前四步检查链

每次构建新版本前，必须执行以下四步检查：

**第一步：解压验证**
- 模拟新用户视角解压 zip，核对实际拿到的文件清单
- 对照 SKILL.md 文件树，逐项确认

**第二步：路径引用扫描**
- 扫描所有 .md 中的文件引用（\ile:///\、\dnd-engine/\、\srd/\ 等）
- 每个被引用的路径必须在 zip 包中存在
- 重点检查新增规则中提及的文件路径

**第三步：旧测试数据清理**
- 检查 party-sheet.html 等模板中是否嵌入了旧测试角色数据
- 嵌入的角色数据必须替换为空占位或默认模板
- 检查 live_party.json 等自动生成文件是否包含敏感数据

**第四步：依赖完整性验证**
- 所有 import 语句指向的模块必须在 zip 中
- CLI 命令对应的函数必须存在
- 重启 OpenClaw 加载 Skill，确认无报错
### 8.3 同步策略


```

修改完成所有代码/规则/模板

    ↓

统一更新所有版本标记文件（CHANGELOG / SKILL.md / _meta.json / 脚注）

    ↓

从根目录同步 CHANGELOG 到 DMskill/

    ↓

从根目录同步所有引用文件到 DMskill/

    ↓

打包 DMskill/ 为 ZIP

    ↓

执行 8.1 检查清单

```


---

- **party-sheet.html 标题动态化**：从 live_party.json 的 `module` 字段读取，不硬编码。确保 live_party.json 模板有 `module: ""`。

### 8.4 发布版禁止嵌入测试数据（铁则）

party-sheet.html 等模板文件在发布时：

1. **`var CHARS` 必须为 `[]`** — 禁止从 live_party.json 或任何测试存档读取角色数据嵌入
2. **禁止包含任何旧游戏的角色名**（如"老白"、"伊索尔德"等），发布前执行全文搜索确认
3. 角色卡数据唯一来源是玩家开始游戏后生成的 live_party.json，不是发布包中的硬编码
4. 违反此规则直接导致版本号 +0.1（如 1.1.8 → 1.1.9 重新发布）


## 开发规则9：三层架构原则


### 9.1 架构总览


城主系统从 v1.0.15 开始采用 **三层架构** 取代原来的单层 Skill 模式：


```

LLM 层 (dnd-dm Skill)     ← 叙事生成、NPC 对话、场景描述、行为规则

    ↕ 调用

API 层 (dnd-api)          ← HTTP 接口（FastAPI），标准化输入输出

    ↕ 包装

引擎层 (dnd-engine)       ← PyPI 包，纯 Python 函数库

```


| 层级 | 名称 | 技术栈 | 职责 |

|:----:|:-----|:-------|:-----|

| **LLM 层** | dnd-dm Skill | OpenClaw Skill (Markdown + prompt) | 叙事生成、NPC 对话、场景描述、检定发起、行为规则、红线和道德约束。**不可代码化** |

| **API 层** | dnd-api | FastAPI, 端口 :8081 | 包装引擎层为 HTTP 接口，供非 Python 平台（Discord、Web、Foundry VTT）调用 |

| **引擎层** | dnd-engine | pip install dnd-engine, Python 3.10+ | 骰子、战斗结算、存档 CRUD、世界状态、模组缓存、XP 计算、场景索引。**纯函数，零 LLM 依赖** |


### 9.2 新增/修改功能的归层原则


收到开发需求时，**必须**先做三层分析，然后选择正确的层进行修改。禁止不做分析直接修改 prompt 或代码。


#### 分析流程


```

收到功能需求

    ↓

按以下三问分析：

    ↓

问1：这个功能需要创造/生成文本内容吗？  → 是 → LLM 层

    ↓

问2：这个功能是纯计算/数据操作吗？      → 是 → 引擎层

    ↓

问3：这个功能需要被非 Python 平台调用吗？→ 是 → API 层

    ↓

确定归属层 → 在该层实现

```


#### 各层能做什么（示例）


**LLM 层能做的（留在 Skill prompt 中）：**

- 描述场景、NPC 对话、战斗旁白

- 发起检定（调用引擎层函数，不自行计算）

- 模板化展示（调用引擎层函数获取结构化数据后渲染）

- 行为规则、红线、道德约束

- 角色创建引导（对话式 7 阶段）

- 回声映射叙事


**引擎层能做的（移到 dnd-engine 代码中）：**

- 骰子表达式求值（rolling, roll_d20, roll_stat）

- 战斗结算（check_hit, calc_damage, calc_save_dc, skill_check）

- 战斗状态管理（new_combat, advance_turn, apply_damage）

- 存档 CRUD（write_save, load_save, list_saves）

- 世界状态管理（update_faction, discover_location, update_quest）

- 场景缓存与存档绑定（embed_scene_cache, extract_scene_cache）

- XP 计算（calc_combat_xp, level_up_requirement）

- 模组扫描与场景索引（scan_modules, build_scene_index, load_chapter_cache）

- 数据模板工厂（make_character_template, make_save_template, make_quest_template）

- SRD 搜索（search_files, expand_context）


**API 层能做的（注册为 FastAPI 端点）：**

- 任何引擎层函数需要被 HTTP 调用时

- 外部平台（Discord Bot、Foundry VTT、Web 前端）需要接入时

- 健康检查、服务状态查询


#### 各层不能做什么（红线）


**LLM 层不能做：**

- ❌ 自行拼接 JSON 数据（存档、角色、任务数据）——应调模板工厂

- ❌ 自行计算 AC/DC/攻击加值——应调 engine.combat.resolve

- ❌ 自行计算检定公式展示——应使用 checks.py 的 detail_lines

- ❌ 自行拼接检定结果格式——应直接输出 detail_lines

- ❌ 自行计算 XP——应调 engine.party.xp


**引擎层不能做：**

- ❌ 创建或修改 LLM 行为规则

- ❌ 生成叙事文本

- ❌ 判断模组剧情走向

- ❌ 自行决定何时调用自身（由 LLM 层调度）


**API 层不能做：**

- ❌ 包含任何业务逻辑——只做请求解析 + 转发引擎层

- ❌ 绕过引擎层直接处理数据


### 9.3 代码存放位置


| 层级 | 代码存放位置 |

|:-----|:-------------|

| LLM 层 | `DM_RULES.md`, `DM_TEMPLATES.md`, `DM_RULES_INDEX.md`, `SOUL.md`, `IDENTITY.md`, `ECHO_ARC.md`, `CHAR_CREATION.md`, `MODULE_ARC.md`, `MODULE_INDEX.md` |

| 引擎层 | `dnd-engine/src/dnd_engine/` (Python 包) |

| API 层 | `dnd-engine/api/server.py` (FastAPI) |

| 测试 | `dnd-engine/tests/` (pytest) |


### 9.4 版本标记规则


- `SKILL.md` / `_meta.json` 的版本号对应 **LLM 层 + 引擎层 + API 层**的统一版本

- `dnd-engine/pyproject.toml` 中的版本独立标记引擎层版本

- 引擎层版本号前缀与 Skill 版本一致（如 Skill v1.0.15 → engine v0.1.x）


### 9.5 违反后果


### 9.6 战斗结束清理流程（强制）


每场战斗结算完成后，扫描工作目录中战斗期间意外生成的 `.py` 临时文件（如 `roll_*.py`、`damage_*.py` 等），分类处理：


- 功能已存在于 `dnd_engine` 或 API → 删除临时文件

- 有重复实现或无用 → 删除

- 新功能有价值 → 评估是否加入 API 层（按9.2归层原则）


同时删除 `combat_state.json` 残留（引擎层已自动保存所需数据）。


- 把属于引擎层的代码放入 LLM prompt → 每次加载浪费 token，LLM 可能执行错误

- 把属于 LLM 层的叙事逻辑放入引擎层 → 引擎层不再纯净，失去平台无关性

- 直接修改 API 层而不更新引擎层 → 接口与实现不一致，端到端测试失败

- 跳过分析流程直接修改 → 功能可能放错层，后续维护成本上升


