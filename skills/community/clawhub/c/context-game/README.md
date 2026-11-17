# 《上下文》— 装在 agent 里的开放世界多题材博弈游戏

一款以 WorkBuddy Skill 形态存在的 AI agent 对话游戏：开放世界、关系/影响力驱动的博弈。
玩家用自由文本行动，**agent 担任游戏引擎**——世界模拟、叙事、裁判三位一体。

> **版本**：1.5.0 · 内置 **14 个题材（完全平行，无主次）**（每题材三层：骨架 / 精写 / GDD）· 十四大 tone_family · 渗透者悬疑局模块 · 信息边界铁律
>
> **v1.5.0 更新要点（题材扩充至 14 个）**：新增 5 个平行题材——封闭囚笼 `closed-circle` / 宫廷权谋 `court-intrigue` / 末日废土 `apocalypse` / 谍战 `espionage` / 江湖武侠 `wuxia`，各含骨架 / 精写 / GDD 三层；协议新增 §3.0「题材遴选四问」（新增 tone_family 的门槛）；`save.py` 的 `TONE_FAMILIES` 白名单同步扩至 14 个家族。
>
> **v1.4.0 更新要点（题材平行化 + 命名区隔）**：全部题材**完全平行**——取消"官方世界/基准世界"层级（`official-world.json` → `hard-sci-fi-detailed.json`，并补齐硬科幻骨架版 `hard-sci-fi.json`，9 题材各三层同规格）；跨题材命名区隔（消除"北岭/东岸/沈氏"3 组重名与 id 复用，硬规则写入协议 §5.3）；9 份 GDD 统一为 7 节标准结构。
>
> **v1.3.0 更新要点（渗透者悬疑局模块 + 信息边界铁律）**：新增 `rules/suspicion.md`——以狼人杀元素为蓝本的**局部事件模块**（非主范式）：内鬼效忠某真实 rival 势力、有政治目标，走「潜伏→发酵→爆发→裁决」四阶段；信息三通道（行为痕迹 / 带伪证词 / 代价验人）+ **泄底铁律**；指认由 `roll` 四档裁决；五维稀缺闸门控制触发频率。同时将泄底铁律升级为**信息边界铁律**（覆盖一切叙事，含玩家不在场的世界事件），落成**三级信息呈现标尺**（在场→具体 / 传闻→传闻层面 / 不可知→不写），并确立「落盘 ≠ 玩家可知」总则。悬疑局**只改状态层，绝不动 world.json**。
>
> **v1.2.0 更新要点（挑战性机制修复）**：判定难度改为**四档白名单 40/60/75/90**（save.py 硬校验，非四档拒写）；判定新增 `--reason` 必填（修正值来源可追溯，杜绝关系/情报对判定零影响）；新增 `pressure` 子命令驱动**世界压力掷表**（时间推进时世界主动演化、玩家无视也照样发生）；失败必须产生可量化硬后果、惨败必触发世界性不可逆变化。

## 目录结构

```
skill/  （压缩包内顶层目录为 context-game/，解压后即技能根目录）
├── SKILL.md                    # 技能入口：agent 行为契约（≤300 行）
├── README.md                   # 本文件
├── scripts/
│   └── save.py                 # 存档引擎（唯一合法写入口，纯标准库；含 roll 四档校验 / --reason / pressure）
├── rules/
│   ├── rules.md                # 核心规则：时间成本、判定公式、围猎阈值、关系 schema
│   ├── events.md               # 事件模板库（18 个模板 + 联动表 + 渗透者悬疑局模板，按题材语义漂移映射）
│   └── suspicion.md            # 渗透者悬疑局模块（狼人杀元素：四阶段 / 三通道信息 / 泄底铁律 / 五维闸门）
├── world/
│   ├── README.md               # 世界库总览（14 大题材清单、三层文件定位、跨题材一致性核查）
│   ├── <topic>.json            # 14 个题材的骨架版（仅五顶层字段，快速试跑；hard-sci-fi.json 即硬科幻题材）
│   ├── <topic>-detailed.json   # 14 个题材的精写版（含 NPC/地点/历史/技术/开局局势，推荐）
│   ├── <topic>-gdd.md          # 14 个题材的 GDD 设计文档
│   └── world-gen-protocol.md   # 自定义世界生成协议（十四大 tone_family + 题材遴选四问 + 自洽清单）
└── saves/                      # 运行时存档（首次运行由 save.py 自动创建）
```

> 14 个题材（平行）：硬科幻政治惊悚 / 现代都市 / 军事 / 悬疑 / 商战 / 校园 / 情感 / 穿越 / 修仙 / 封闭囚笼 / 宫廷权谋 / 末日废土 / 谍战 / 江湖武侠。
> 完整清单与三层文件对照见 `world/README.md`。

运行时每个存档槽位（如 `saves/default/`）：

```
state.json     # 账本：player→location→clock→relations→flags→events（紧凑 JSON，固定顺序）
memory.md      # 叙事记忆：压缩区（≤500 字）+ 活跃区（≤30 条）
world.json     # 该档世界骨架（world-init 落盘）
rolls.jsonl    # 骰子日志（只追加，每行一条，含种子与运势）
.bak / archives/NNN.md   # 备份与归档段
```

## 安装到 WorkBuddy

1. 把整个 `skill/` 目录放进你的 WorkBuddy 技能目录
   （Windows 默认：`C:\Users\<你>\.workbuddy\skills\context-game\`，
   或当前工作区技能目录，以你的 WorkBuddy 版本说明为准）。
2. 确认 SKILL.md 位于该目录根部（YAML frontmatter 已写好 `name: context-game`）。
3. 重启 / 重载 WorkBuddy 会话，对 agent 说"**开始游戏**"即可。

要求：Python 3.8+ 在 PATH 中（仅标准库，无 pip 依赖）。

## 怎么开始玩

- **开始游戏** → agent 检查 `saves/`：有档则读档恢复；无档则让你选世界——
  **14 个题材（平行）**之一：硬科幻政治惊悚《双陆纪元》/ 现代都市 / 军事 / 悬疑 / 商战 / 校园 / 情感 / 穿越 / 修仙 / 封闭囚笼 / 宫廷权谋 / 末日废土 / 谍战 / 江湖武侠，
  也可以选**自定义世界**（按协议现场生成）。选定后再选三种开局身份（旅人 / 本地人 / 空白身世）。
- 然后就是自由对话。移动、调查、交易、说服、对质、蛰伏都会推进游戏内时钟；
  问玩法、切档、退休写史书不会。
- 高危动作 agent 会先预警风险等级，掷骰结果以运势词呈现
  （惨败 / 失败 / 勉强成功 / 成功 / 意外转机）。

## 十四大题材（tone_family）

| 题材 | tone_family | 世界文件前缀 | 势力语义 |
|---|---|---|---|
| 硬科幻政治惊悚 | `hard-sci-fi-political-thriller` | `hard-sci-fi` | 国家 / 军政府 / 城邦 |
| 现代都市 | `modern-urban` | `modern-urban` | 财团 / 政界 / 媒体 / 军方承包商 |
| 军事 | `military` | `military` | 国家 / 军政派系 / 雇佣兵团 / 情报机构 |
| 悬疑 | `mystery` | `mystery` | 官方调查组 / 民间侦探 / 嫌疑人方 |
| 商战 | `corporate-war` | `corporate-war` | 敌对公司 / 友商联盟 / 投行 / 律所 |
| 校园 | `campus` | `campus` | 学生会 / 教师派系 / 社团 / 校外势力 |
| 情感 | `romance` | `romance` | 女方家族 / 男方家族 / 闺蜜兄弟圈 |
| 穿越 | `isekai` | `isekai` | 原时空派系 + 新时空派系（双 matrix） |
| 修仙 | `cultivation` | `cultivation` | 宗门 / 皇朝 / 秘境主 / 散修 / 魔道 |
| 封闭囚笼 | `closed-circle` | `closed-circle` | 狱政当局 / 狱霸帮派 / 内线 / 家属网 / 走私 |
| 宫廷权谋 | `court-intrigue` | `court-intrigue` | 后党 / 贵妃系 / 权臣 / 宦官 / 储君党 |
| 末日废土 | `apocalypse` | `apocalypse` | 市政残部 / 军阀 / 幸存者聚落 / 教会 / 商队 |
| 谍战 | `espionage` | `espionage` | 情报机关 / 敌对机构 / 双面间谍 / 抵抗网 / 线人 |
| 江湖武侠 | `wuxia` | `wuxia` | 正道剑派 / 大帮 / 药毒谷 / 镖局联盟 / 杀手楼 |

完整世界库说明（三层文件定位、跨题材一致性核查、势力语义漂移表）见 `world/README.md`。

## save.py 命令速查

均在 `skill/` 目录下执行（或用绝对路径）：

| 命令 | 说明 |
|---|---|
| `python scripts/save.py init --slot NAME [--mode official\|custom]` | 初始化新档（state.json + memory.md 骨架） |
| `python scripts/save.py update --slot NAME --payload FILE\|-` | 校验并原子写入 state.json（`-` 读 stdin） |
| `python scripts/save.py roll --slot NAME --difficulty N --modifier N --reason TEXT [--label TEXT]` | 掷骰判定（`--difficulty` 必须为 40/60/75/90 四档之一；`--reason` 必填，说明难度依据+修正来源），结果追加 rolls.jsonl |
| `python scripts/save.py pressure --slot NAME [--table TEXT]` | 掷世界压力表（确定性 d100，1..100），供时间推进时驱动被动事件，结果追加 rolls.jsonl |
| `python scripts/save.py validate --slot NAME` | 校验存档完整性 |
| `python scripts/save.py world-init --slot NAME --payload FILE\|-` | 校验自定义世界骨架并落盘为该档 world.json |
| `python scripts/save.py archive --slot NAME [--summary FILE\|-]` | 活跃区归档到 archives/NNN.md，可同时替换压缩区 |

写入安全：`update` 前自动备份旧档为 `.bak`，用临时文件 + `os.replace` 原子写；
schema（STATE_SCHEMA 常量）内嵌于 `save.py` 模块 docstring 与 `_check_state`。

## 迁移到其他 agent 平台的注意事项

**WorkBuddy 依赖（迁移时需替换）**
- SKILL.md 的 YAML frontmatter（name/description）是 WorkBuddy 的技能发现机制。
- "触发与初始化"里的"玩家说开始游戏即触发"依赖 WorkBuddy 的 description 匹配。
- agent 需要有文件读写与 Shell 执行能力（Read/Write/Glob/Bash 等工具），
  平台不同则工具名不同，SKILL.md 第 0、1 节里的工具叫法需对照替换。

**通用（可原样迁移）**
- `scripts/save.py`：纯标准库 CLI，任何能跑 Python 的 agent 平台都能用。
- `rules/`、`world/`（含 14 大题材 + 生成协议）、`saves/` 结构与全部游戏规则：平台无关。
- 核心契约——"state.json 只经 save.py 修改""名字即契约"
  "信息边界铁律（渲染信息量严格等于玩家已掌握信息量，含三级呈现标尺）"
  "写关系张力不写风景""失败改变棋局不清档"——是平台无关的 agent 行为约束，写在 SKILL.md 正文中。
