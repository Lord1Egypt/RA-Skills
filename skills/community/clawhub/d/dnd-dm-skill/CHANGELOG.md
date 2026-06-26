# DM 城主系统更新日志
## 1.1.8 (2026-06-09)

### 角色卡模板清理
- **移除旧测试数据**：party-sheet.html 中 embedded 的 4 个旧角色数据（老白/伊索尔德/莉莉安/科林）彻底清除
- **空状态引导**：无角色数据时显示引导页面，提示用户开始游戏或加载存档
- **双源同步**：workspace 和 DMskill/references/ 两个副本一致

### 开发规则补充
- **DM_DEV_GUIDE.md §8.3**：新增发布前四步检查链（解压验证、路径扫描、旧数据清理、依赖验证）

## 1.1.7 (2026-06-09)

### 校验功能移至引擎层
- **`dnd_engine/verify.py` 新建**：`verify_environment()` 纯函数，不依赖 FastAPI 服务
- **CLI 修正**：`cmd_verify()` 从 HTTP 调用改为直接调用 `verify_environment()`
- **DM_RULES.md 规则21 修正**：`GET /api/system/verify` → `dnd_engine.verify.verify_environment()`
- **修复**：玩家在无 API 服务环境下调用 `/verify` 不再报错

### 包完整性修复
- 校验函数随引擎源码打包，解压即用
- DMskill 重构建（23 个 .py，新增 verify.py）

## 1.1.5 (2026-06-09)

### 零安装体验
- **引擎源码内置**：dnd-engine 直接打包在 zip 中，解压即用，无需 pip install
- **code/ 目录移除**：旧代码库全部删除（25 个 .py 已弃用），不再包含在 DMskill 中
- **36 处路径引用迁移**：DM_RULES.md、SKILL.md、DM_TEMPLATES.md、DM_DEV_GUIDE.md、ECHO_ARC.md 中所有 `code/` 引用改为 `dnd-engine/src/dnd_engine/`
- **安装指引精简**：从 5 步缩至 3 步（解压 -> 放规则书和模组 -> /verify）

### ClawHub 合规修复
- **DMskill 清理**：移除 .git 目录、移除安装脚本、移除 Docker 文件
- **换行符修复**：消除 `



` 多余回车导致的显示异常
- **SKILL.md 标准化**：按 AgentSkills 规范保留 metadata，移除所有外部依赖声明

## 1.1.5 (2026-06-09)

### 零安装体验
- **引擎源码内置**：dnd-engine 直接打包在 zip 中，解压即用，无需 pip install
- **code/ 目录移除**：旧代码库全部删除（25 个 .py 已弃用），不再包含在 DMskill 中
- **36 处路径引用迁移**：DM_RULES.md、SKILL.md、DM_TEMPLATES.md、DM_DEV_GUIDE.md、ECHO_ARC.md 中所有 `code/` 引用改为 `dnd-engine/src/dnd_engine/`
- **安装指引精简**：从 5 步缩至 3 步（解压 -> 放规则书和模组 -> /verify）

### ClawHub 合规修复
- **DMskill 清理**：移除 .git 目录、移除安装脚本、移除 Docker 文件
- **换行符修复**：消除 `



` 多余回车导致的显示异常
- **SKILL.md 标准化**：按 AgentSkills 规范保留 metadata，移除所有外部依赖声明

## 1.1.5 (2026-06-09)

### 零安装体验
- **引擎源码内置**：dnd-engine 直接打包在 zip 中，解压即用，无需 pip install
- **code/ 目录移除**：旧代码库全部删除（25 个 .py 已弃用），不再包含在 DMskill 中
- **36 处路径引用迁移**：DM_RULES.md、SKILL.md、DM_TEMPLATES.md、DM_DEV_GUIDE.md、ECHO_ARC.md 中所有 `code/` 引用改为 `dnd-engine/src/dnd_engine/`
- **安装指引精简**：从 5 步缩至 3 步（解压 -> 放规则书和模组 -> /verify）

### ClawHub 合规修复
- **DMskill 清理**：移除 .git 目录、移除安装脚本、移除 Docker 文件
- **换行符修复**：消除 `



` 多余回车导致的显示异常
- **SKILL.md 标准化**：按 AgentSkills 规范保留 metadata，移除所有外部依赖声明

## 1.1.4 (2026-06-08)

### SKILL.md 标准化与优化
- **AgentSkills 标准格式**：添加 `metadata` 字段（emoji、OS兼容、二进制依赖声明、install源）
- **安装指引重写**：分 5 步 Agent 可执行流程，标记 `[Agent 操作]` / `[需用户操作]`
- **中文完整保留**：三层架构、30个API端点表、15条红线、6层规则架构表完整保留

### macOS / Linux 支持
- **install.sh**：macOS/Linux 一键安装脚本（Python检测 → venv → pip install → init）
- **跨平台兼容**：Docker 部署支持、CLI工具跨平台、角色卡HTML跨平台（双击即看）
- **SKILL.md metadata**：声明支持 darwin/linux/win32

### 规则架构修复
- **6层规则重排**：26条规则按层0-5排序，每条规则添加 `<!-- layer: N -->` 标记
- **重复规则清理**：移除重复的规则21副本；规则X恢复（层5模组控制）
- **DM_RULES_INDEX.md 移除**：layer标记已内嵌在每条规则中，索引文件完全冗余
- **DMskill references 同步**：重建后的 DM_RULES.md 同步到所有位置

### 安装引导流程完善
- **`/api/system/verify`**：预飞校验（引用文件、引擎、权限）
- **`/api/system/init`**：自动创建工作目录（saves/ rules/ modules/ live_party.json）
- **`dnd-engine init` CLI**：命令行初始化
- **规则21**：新增安装引导规则（校验→提示→通过→切DM人格）
- **`规则参考来源分工` / `规则层级索引`**：移出规则主体，放至文件末尾

## 1.1.4 (2026-06-08)

### SKILL.md 标准化与优化
- **AgentSkills 标准格式**：添加 `metadata` 字段（emoji、OS兼容、二进制依赖声明、install源）
- **安装指引重写**：分 5 步 Agent 可执行流程，标记 `[Agent 操作]` / `[需用户操作]`
- **中文完整保留**：三层架构、30个API端点表、15条红线、6层规则架构表完整保留

### macOS / Linux 支持
- **install.sh**：macOS/Linux 一键安装脚本（Python检测 → venv → pip install → init）
- **跨平台兼容**：Docker 部署支持、CLI工具跨平台、角色卡HTML跨平台（双击即看）
- **SKILL.md metadata**：声明支持 darwin/linux/win32

### 规则架构修复
- **6层规则重排**：26条规则按层0-5排序，每条规则添加 `<!-- layer: N -->` 标记
- **重复规则清理**：移除重复的规则21副本；规则X恢复（层5模组控制）
- **DM_RULES_INDEX.md 移除**：layer标记已内嵌在每条规则中，索引文件完全冗余
- **DMskill references 同步**：重建后的 DM_RULES.md 同步到所有位置

### 安装引导流程完善
- **`/api/system/verify`**：预飞校验（引用文件、引擎、权限）
- **`/api/system/init`**：自动创建工作目录（saves/ rules/ modules/ live_party.json）
- **`dnd-engine init` CLI**：命令行初始化
- **规则21**：新增安装引导规则（校验→提示→通过→切DM人格）
- **`规则参考来源分工` / `规则层级索引`**：移出规则主体，放至文件末尾

## 1.1.3 (2026-06-07)

### 角色卡网页模板（party-sheet.html）
- **四列网格布局**：`.all-4up` 响应式 CSS（4列→2列→1列随窗口缩窄自动降级）
- **单列卡片格式**：去掉左右分列，改为单一列（属性→豁免→技能→资源→可用动作→装备→特征→背包→物品/资金）
- **完整字段覆盖**：六维属性+调整、豁免(+熟练标签)、技能(熟练o/专精*)、资源、武器攻击表格、法术按环级分组、装备按槽位、特征标签、背包列表、物品/资金
- **`file://` 协议兼容**：XHR在本地文件协议下静默失败，改用内嵌 `PARTY_DATA`
- **角色数据同步**：内嵌数据 + `live_party.json` 双源更新

### 角色数据修复
- **装备补全**：莉莉安 8件（含守护盔帽、海姆圣徽戒指、至恶护符等）
- **老白装备补全**：9件（含提亚马特之牙、暗青龙匕、渡鸦斗篷等）
- **伊索尔德装备补全**：5件（含Blackrazor+3、黯光长剑+盾等）
- **资金/背包修复**：所有角色资金和背包物品按存档实际数据补充
- **AC明细补全**：4角色AC来源计算说明

### 工程改进
- **技能发布流程**：DMskill/ 目录重建脚本，`party-sheet.html` 纳入 references/
- **全列角色卡**：SKILL.md 更新文件列表和版本号
## 1.1.2 (2026-06-06)

### 沉浸感修复
- **回声系统重写**（规则20）：新增硬性红线（禁真人模式/禁系统术语）、三步触发流程（角色内回应→奇幻邀约→接受或拒绝）、主线回归机制（短/中/长分档退出路径）
- **ECHO_ARC.md 重写**：去掉所有 Python exec 引用，LLM 直接自然语言映射；新增响应话术模板
- **规则4.3**：新增回声支线例外（可延长至6轮后强制标注「支线」）
- **场景描述修复**：§9.2 禁止暴露房间编号和功能名；规则1.3 新增强制检查清单（三问自检）；规则17.6 输出前强制自检
- **偏差纠正修复**：规则8.3和8.6重写为保沉浸版——轻度偏差自然消失不承认，禁止"我跑偏了""回退到节点"等 meta 语言
- **规则18.2**：完整函数映射表（16个dnd_engine import + API调用示例），禁止临时生成脚本文件

### API 层扩展（+4端点，总数30）
- `POST /api/combat/roll-initiative` — 一键掷先攻+排序
- `POST /api/party/rest` — 短休/长休结算
- `GET /api/party/character/{name}` — 角色属性查询
- `POST /api/party/level-up` — 升级自动结算
- `party/live.py` 加入 dnd-engine

### 角色卡模板更新
- §9.6 新增按环级分组的法术展示格式（━━━分隔、■□法术位、每行法术名+效果+检定+专注）
- 加 ⚠️强制格式 警告

### 开发规则
- DM_RULES.md §15b.6：战斗结束检查临时 .py 文件
- DM_DEV_GUIDE.md §8.0：发布前检查临时文件，有价值则加入 API
- DM_DEV_GUIDE.md §9.6：战斗结束清理流程

## 1.1.1 (2026-06-05)

### 上下文优化
- **DM_RULES.md 规则重新编号**：删除6个重复节，24规则按升序排列（0→0a→0.5→...→20）
- **DM_RULES.md 四项压缩**：规则5(删城主指南引用)、规则0(压缩回声询问)、规则8(压缩过渡协议)、规则17(删场景示例)，合计-409t
- **SOUL.md + IDENTITY.md 合并去重**：IDENTITY.md 压缩至226t（-65%），SOUL.md 去重至855t（-41%），合计-1,512t
- **DM_TEMPLATES.md 五项代码化**：角色卡(-372t)、法术展示(-334t)、任务清单(-172t)、模组列表(-49t)、经验结算(-28t)
- **上下文总量从 12,113t 降至 10,364t**（-15%），进入规则19目标范围

### 响应速度优化
- **exec→import 替代**：规则18改为强制使用 `from dnd_engine import ...` 替代 `exec("python ...")`，消除子进程启动开销（每场战斗省~3-4s）
- **场景缓存按需拆分**：`scene_cache.py` 新增 `split_cache()` / `get_nearby_rooms()` / `get_room_detail()`，索引轻量常驻（~300t），详情按需加载
- **resolve-round API 端点**：`POST /api/combat/resolve-round` 一键合并命中+伤害+状态更新，单次替代2-3次链式调用（每轮省~400ms推理）
- **DM_DEV_GUIDE.md SRD引用改为API调用**：从 `subprocess.run` 改为 `GET /api/srd/search`

### 文件变更
- DM_RULES.md: 规则编号重排，四项压缩
- SOUL.md: 去重压缩（移除铁则一/铁则二/角色定义）
- IDENTITY.md: 压缩至核心约束+风格简述
- DM_TEMPLATES.md: 五项模板代码化
- DM_DEV_GUIDE.md: SRD引用改为API
- `dnd-engine/src/dnd_engine/save/scene_cache.py`: 新增拆分/按需函数
- `dnd-engine/api/server.py`: 新增 resolve-round 端点

## 1.1.0 (2026-06-04)

### 重大架构变更
- **三层架构重构**：从单层 Skill 拆分为 dnd-engine（引擎层）+ dnd-api（API 层）+ dnd-dm Skill（LLM 层）
- **引擎层独立发布**：`dnd-engine` 发布为 PyPI 包（`pip install dnd-engine`），纯 Python 零 LLM 依赖
- **API 层上线**：`dnd-api` 基于 FastAPI，22 个 HTTP 端点，支持任何平台集成

### 新增：dnd-engine（引擎层）
- `dnd_engine/dice/rolls.py` — 骰子表达式求值、d20、属性投点
- `dnd_engine/combat/{checks, resolve, state}.py` — 命中判定、伤害结算、技能检定、战斗状态 CRUD
- `dnd_engine/party/xp.py` — XP 计算、升级需求
- `dnd_engine/save/{io, scene_cache, templates}.py` — 存档 CRUD、场景缓存绑定、数据模板工厂
- `dnd_engine/state/world.py` — 世界状态管理（派系、任务、NPC、场景）
- `dnd_engine/module/{scanner, scene_index, cache, init}.py` — 模组扫描、场景索引、文件缓存

### 新增：dnd-api（API 层）
- 16 个核心接口：roll / check-hit / calc-damage / skill-check / combat-state(+6) / xp / save(+3) / world-state
- 4 个 SRD 接口：search / search-in-file / expand / files
- 自动生成 Swagger UI 文档页（`/docs`）
- 全套 Pydantic 请求/响应模型

### 新增：SRD 搜索 API
- `GET /api/srd/search?q=` — 跨 20 个 SRD 文件搜索关键词
- `GET /api/srd/expand` — 展开搜索结果上下文
- `GET /api/srd/files` — 列出所有 SRD 参考文件

### 核心文件精简
- DM_RULES.md 从 51KB 精简至 43KB（-15.2%）——移除角色/存档/任务 JSON schema 表、18.2 代码映射表、15b.2 公式说明
- DM_TEMPLATES.md 从 21KB 精简至 19KB（-10.4%）——移除 9.11 检定格式规范（由 checks.py 结构化返回替代）
- LLM 层 prompt 总计节省 ~2,500 token（13.8%）

### 新增开发规则
- DM_DEV_GUIDE.md 开发规则9：三层架构原则——新增/修改功能必须先做三层分析，再选择对应层实现
- LLM 层不再自行拼接 JSON、计算公式、组织展示格式

### 测试覆盖
- 从 46 项增至 90 项 pytest 测试用例，全部通过
- 新增测试模块：test_save.py（21项）、test_state.py（12项）、test_module_scanner.py（7项）、test_module_cache.py（4项）
- 覆盖模板工厂、存档 CRUD、世界状态 CRUD、模组扫描、场景索引、边界异常

### 文档
- `DnD_城主系统_三层架构方案.docx` 架构方案文档
- dnd-engine/README.md 引擎层使用说明
- dnd-engine/pyproject.toml 标准包元数据

## 1.0.15 (2026-06-01)

### 新增
- **渐进式房间探索引导系统**（DM_TEMPLATES.md §9.2 重写）：幕前/幕后分离 —— 幕后生成 `_scene_cache_*.json` 记录所有房间编号、连接、状态、NPC、感知线索；幕前仅用自然语言描述环境、方向、感官提示，不暴露房间编号和进度清单
- **场景缓存与存档绑定**（`code/save/scene_cache.py`）：存档时自动将活跃的 `_scene_cache_*.json` 嵌入存档 `_scene_cache` 字段；读档时自动还原缓存文件到工作目录；支持 `cleanup_orphan_caches()` 清理孤立缓存
- `code/save/io.py`: `write_save()` / `load_save()` 集成场景缓存的自动嵌入和还原



### 变更
- DM_TEMPLATES.md §9.2 从简单房间列表升级为隐藏引导规则（5条不可省略规则 + 场景缓存生成指引 + 存档关联说明）


### 文件结构新增
```
├── code/save/scene_cache.py    ← 场景缓存与存档绑定模块（新增）
├── _scene_cache_*.json         ← [自动生成] 场景缓存（不在版本控制中）
```


## 1.0.14 (2026-05-31)

### 新增
- **回声系统启动开关**：每次新开一局或载入存档前，自动询问玩家是否启用回声系统（规则20）
  - `world_state.json` 新增 `echo_enabled` 字段
  - `code/state/world.py` 新增 `set_echo_enabled()` / `get_echo_enabled()` 函数
  - `code/save/templates.py` 存档模板新增 `echoEnabled` 字段
  - `code/save/io.py` 存档写入时自动同步 echo 状态；`load_save()` 自动从存档恢复 echo 设置
  - `code/rule/retriever.py` 新增回声/echo 等关键词→规则20 映射
- **DM_RULES.md 规则0 会话启动流程更新**：
  - 三步拆为四步：先问回声开关（第三步），再问载入/新开/查看（第四步），后续顺延
  - 规则20 开头新增启动方式说明，指向规则0

### 变更
- `DM_RULES_INDEX.md`：规则19（Token优化）/规则20（回声映射）移入层1；层0移除重复的规则19
- `world_state.json` 新增 `echo_enabled: false` 默认字段

### 规则更新
- **规则0.第三步**：回声系统询问（新增）
- **规则0.第五步**：读档时从存档恢复 `echoEnabled` 状态到 world_state
- **规则14.存档字段表**：新增 `echoEnabled` 字段

## 1.0.13 (2026-05-31)

### 新增
- **🌊 回声映射系统 (Echo)**：现实→奇幻自动叙事引擎
  - `code/echo/echo_generator.py` — 情绪提取 + 主题分类 + 任务骨架生成
  - `code/echo/mapper_rules.md` — 映射规则全集（情绪→氛围、现实→奇幻、人物→NPC）
  - `code/echo/themes.json` — 玩家情绪记录 + 已生成任务档案
- **DM_RULES.md 规则20：回声映射** — 映射流程定义 + 5条隐私红线 + P0-P5 优先级
- **CODE_LIBRARY.md 注册 echo 函数**：`extract_mood()` / `extract_themes()` / `map_to_quest()` / `save_to_journal()`

### 映射规则
| 现实主题 | 奇幻任务 | 隐喻示例 |
|---------|---------|---------|
| 工作压力 | 限时拯救 | 老板→暴君，Deadline→诅咒倒数 |
| 人际关系 | 外交斡旋 | 争吵→派系冲突 |
| 个人成长 | 试炼之路 | 瓶颈→封印锁链 |
| 健康 | 寻药之旅 | 生病→诅咒疫病 |
| 经济 | 偿还契约 | 没钱→灵魂债契 |
| 成就 | 加冕时刻 | 升职→血脉觉醒 |

### 隐私红线
- 玩家不主动倾诉，绝不追问私人生活
- 映射必须转换隐喻，不直接复制现实
- 映射解密权在玩家
- themes.json 本地存储，不推送 GitHub

## 1.0.12 (2026-05-23)

### 新增
- **场景级懒加载系统**：`code/module/scene_index.py` — 按 `##` 标题建立场景行范围索引，只加载当前场景原文（~2.5K tokens）替代整章文件（~27-55K tokens）
- **结构化世界状态**：`code/state/world.py` + `world_state.json` — 6种数据结构（派系关系/任务进度/NPC状态/地点发现/游戏天数/当前场景），内置增量更新 API
- **剧情摘要系统（P0）**：`code/summary/generate.py` + `plot_summary.json` — 每次存档自动生成100-300 token摘要，会话启动优先加载摘要替代完整聊天历史
- **规则关键词检索**：`code/rule/retriever.py` — 19组关键词→规则ID映射，按需加载规则文本替代整层加载
- **通用模块初始化**：`code/module/init.py` — `init_module(module_name)` 接受任意模组名，自动生成通用模板数据文件（零硬编码）
- **玩家端检定展示函数**：`code/combat/checks.py` — `resolve_skill_check()`、`check_hit_v2()`、`resolve_save_check()`，显示完整加值构成明细

### 改进
- **通用性架构重构**：所有代码/数据文件消除特定模组硬编码引用（博德之门：坠入阿弗纳斯），支持任意 D&D 5e 模组
- **MODULE_INDEX.md 压缩 77%**：从 12.4K 降至 2.8K，改为指针格式（引用场景索引+world_state 动态摘要）
- **MODULE_ARC.md 压缩 87%**：从 6.9K 降至 0.9K，通用运行结构模板
- **world_state.json 通用化**：从硬编码6派系+12任务+7NPC 改为通用空模板，运行时动态填充
- **scanner 支持中英文场景标签**：`/combat|战斗|battle|fight/` 等双语关键词
- **DM_RULES.md 审计清理**：开发流程规则（18.3-18.6、12.1、19.4）移至 DM_DEV_GUIDE.md，所有规则通用化

### 架构变更
- **5级上下文加载优先级（P0-P5）**：DM_RULES.md 规则19
  - P0 常驻（~2.3K）：SOUL + 世界状态摘要 + 剧情摘要
  - P1 当前场景（~3.5-6.5K）：场景原文 + NPC 数据
  - P2 对话（~2K）：最近5轮
  - P3+P4 按需检索（0-3K）
  - 总计 ~5.8K-12K（优化前 ~50K-75K，节省 70-85%）
- **存档即摘要**：`write_save_with_summary()` 将存档与剧情摘要生成绑定
- **会话启动流**：`load_summary()` → 摘要文本（100-300t） → 按需恢复完整历史

### 技术细节
- `scene_index.py` 使用 `module_name:filename` 键格式避免多章覆盖
- `world.py` 提供 `get_world_summary()` 返回50-100 token摘要字符串
- `plot_summary.json` 增量更新保留核心内容+追加最新事件，上限6行
- `retriever.py` 的 `load_rules_by_keywords()` 替代加载整层（5K→0.5-2K tokens）

## 1.0.11 (2026-05-23)

### 新增
- **SRD 5.2.1 集成**：`srd/references/` 部署 20 个 SRD 参考文件 + `srd/scripts/` Python 搜索脚本
- **Related Skills 声明**：`SKILL.md` 新增「相关技能」节，声明与 `dnd5e-srd` 的配合关系

### 变更
- 插件文件结构：新增 `srd/` 子目录
- 版本号 1.0.10 → 1.0.11

### 引用说明
- SRD 文件来源：`dnd5e-srd` skill（原始安装路径 `~/AppData/Roaming/LobsterAI/SKILLs/dnd5e-srd/references/`）
- 20 个参考文件 DND5eSRD_*.md，共 1.47 MB
- SRD 5.2.1 基于 CC-BY-4.0 许可

## 1.0.10 (2026-05-22)

### 重大变更
- **DM_RULES.md 分层重构**：扁平23节 → 6层结构（层0常驻~层5模组控制），按场景按需细读
- **新增 DM_RULES_INDEX.md**：层级索引文件，每次会话常驻，指导 LLM 按场景查阅对应层
- **规则13压缩**（升级）：10项清单+触发时机保留，详细逐项引导整合回 body
- **规则14压缩**（存档）：触发时机+格式验证保留，完整字段定义整合回 body
- **规则18压缩**（代码模板）：13行对照表+沙盒/兜底/入库/同步全部保留
- **规则0+规则6合并**：重复的会话启动协议合并为一条
- **SOUL.md 更新**：增加 DM_RULES_INDEX.md 引用
- **DM_DEV_GUIDE.md 新增开发规则6**：新规则必须归层，跨层规则拆分的强制流程
- **DM_RULES.md 新增新规则归层约束**：`<!-- layer: N -->` 标记 + INDEX 同步，违反视为结构污染
- **Token 节省**：日常探索~2,500 tokens（原~4,925），节省~49%

## 1.0.8 (2026-05-22)

### 新增
- **规则18：运行时代码模板优先** — 运行时强制使用 `code/` 预构建函数代替 LLM 生成代码，大幅减少 Token 消耗
- **规则18.6：玩家新交互需求自动入库** — 玩家提出的新交互首次生成的代码自动登记到 `CODE_LIBRARY.md`
- **代码模板库** `code/`：战斗状态持久化（`combat/state.py`）、战斗公式模板（`combat/formulas.py`）、模组内容缓存（`module/cache.py`）、存档格式模板（`save/templates.py`）、规则速查表（`quickref.py`）
- `DM_DEV_GUIDE.md` 开发规则4：运行时代码模板使用流程 + Token 优化策略表
- **文件整理**：DM_RULES.md 内容迁移至 DM_TEMPLATES.md（展示模板）、DM_DEV_GUIDE.md（开发规则）

### 变更
- `DM_RULES.md` 精简至 825 行（原 937 行），剥离模板和开发内容
- `DM_TEMPLATES.md` 扩展至 439 行，新增 9.8-9.11 模板
- 法术展示模板全面更新：增加检定方式列和推荐理由列（规则11）
- 角色卡模板更新：已装备物品单独列出并标注生效属性（9.6a/9.6b）
- 存档规则：自动递增编号 + 时间戳记录（规则14）
- 战斗结算规则：装备加成全面纳入计算（规则15b）
- 升级流程：7步逐项引导（规则13.2）
- 模组选择：新开一局先选模组（规则0a）
- 检定信息管控：先描述情景再叫投骰（规则17）

## 1.0.6 (2026-05-21)

### 变更
- 文件重组：展示模板移入 `DM_TEMPLATES.md`，开发规则移入 `DM_DEV_GUIDE.md`
- 技能包发布结构更新

## 1.0.5 (2026-05-20)

### 新增
- 初始版本：D&D 5e 2024版 DM 城主系统
- 14条运行规则（规则0-16）
- DM 展示模板（9.1-9.6）
- 地图系统（DM_MAP_SYS.md）
- 角色创建流程（CHAR_CREATION.md）
- 存档/升级系统
