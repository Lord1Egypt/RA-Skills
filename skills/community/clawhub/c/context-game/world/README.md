# 《上下文》世界库总览

`skill/world/` 是《上下文》游戏的所有世界定义。当前共 **14 个题材（平行）**，各提供三层文件（骨架 / 精写 / GDD），可任选一层开局。

---

## 文件清单

| 题材 | tone_family | 骨架 JSON | 精写 JSON | GDD 文档 |
|---|---|---|---|---|
| 硬科幻政治惊悚 | `hard-sci-fi-political-thriller` | `hard-sci-fi.json` | `hard-sci-fi-detailed.json`（《双陆纪元》） | `hard-sci-fi-gdd.md` |
| 现代都市 | `modern-urban` | `modern-urban.json` | `modern-urban-detailed.json`（《明珠湾区》） | `modern-urban-gdd.md` |
| 军事 | `military` | `military.json` | `military-detailed.json`（《逐鹿大陆》） | `military-gdd.md` |
| 悬疑 | `mystery` | `mystery.json` | `mystery-detailed.json` | `mystery-gdd.md` |
| 商战 | `corporate-war` | `corporate-war.json` | `corporate-war-detailed.json` | `corporate-war-gdd.md` |
| 校园 | `campus` | `campus.json` | `campus-detailed.json`（《青岸学潮》） | `campus-gdd.md` |
| 情感 | `romance` | `romance.json` | `romance-detailed.json`（《锦城情局》） | `romance-gdd.md` |
| 穿越 | `isekai` | `isekai.json` | `isekai-detailed.json`（《双轨异界》） | `isekai-gdd.md` |
| 修仙 | `cultivation` | `cultivation.json` | `cultivation-detailed.json` | `cultivation-gdd.md` |
| 封闭囚笼 | `closed-circle` | `closed-circle.json` | `closed-circle-detailed.json`（《礁屿狱城》） | `closed-circle-gdd.md` |
| 宫廷权谋 | `court-intrigue` | `court-intrigue.json` | `court-intrigue-detailed.json`（《九重阙》） | `court-intrigue-gdd.md` |
| 末日废土 | `apocalypse` | `apocalypse.json` | `apocalypse-detailed.json`（《余烬荒年》） | `apocalypse-gdd.md` |
| 谍战 | `espionage` | `espionage.json` | `espionage-detailed.json`（《长夜暗局》） | `espionage-gdd.md` |
| 江湖武侠 | `wuxia` | `wuxia.json` | `wuxia-detailed.json`（《烟波江湖》） | `wuxia-gdd.md` |

配套基础设施：
- `world-gen-protocol.md` — 自定义世界生成协议（含 14 个 tone_family、势力语义漂移表、8 条自洽清单、命名合规护栏、题材遴选四问）
- （开发环境可能有 `world-gen-protocol.md.bak` 备份文件，发布包不含）

---

## 三层文件定位

| 层 | 文件 | 用途 | 密度 |
|---|---|---|---|
| **骨架** | `<topic>.json` | 仅 5 顶层字段（meta/continents/nations/neutral_port/faction_matrix），运行时可直接开局，agent 现场补 NPC/地点/历史 | 50-80 行 |
| **精写** | `<topic>-detailed.json` | 扩展 core_npcs / key_locations / history / world_tech / opening_situation 五类增强字段，密度对齐硬科幻题材《双陆纪元》 | 330-380 行 |
| **GDD** | `<topic>-gdd.md` | 设计文档：题材定位、参考作品点名、势力设计与关系张力机器映射、玩家胜利通道、题材设计说明、8 条自洽清单自查报告 | 200-500 行 |

推荐开局时**直接用精写版**（用 `python scripts/save.py world-init --slot <槽位> --payload world/<topic>-detailed.json`）；骨架版只用于快速试跑或让 agent 生成变体。

---

## 跨题材一致性核查（阶段三验证结果）

所有 14 个世界均满足以下硬性指标：

| 指标 | 要求 | 实测 |
|---|---|---|
| nation 数 | 4-6 | 全部 5 |
| faction_matrix pair 数 | 15（5 势力 + 1 中立港的完全图） | 全部 15 |
| relation 值两两互不相同 | 强制 | 全部通过（save.py 硬约束） |
| NPC 数（精写版） | 10-15 | 10-15 |
| ≤ -50 结构性敌意对 | ≥ 2 | 全部满足（2-3 对） |
| ≥ 50 表面同盟藏裂缝 | ≥ 1 | 全部满足（1-4 对） |
| tension_seeds 可追溯 | 8 条自洽清单 #3 | 全部 PASS |
| 跨题材零重名 | 强制 | 全部通过 |

---

## 势力语义漂移（题材特色）

《上下文》的核心是**关系张力机器**（多方势力互算 + 结构性敌意 + 表面同盟藏裂缝 + 中立交汇点）。机器骨架不变，但"势力"的语义在题材间漂移：

| 题材 | 势力是什么 | 中立交汇点是什么 |
|---|---|---|
| 硬科幻政治惊悚 | 国家 / 军政府 / 城邦 | 免税深水港（灰潮港） |
| 现代都市 | 财团 / 资本 / 媒体 / 军方承包商 / 市政 | 中间人 / 独立调查者 |
| 军事 | 国家 / 军政派系 / 雇佣兵团 / 情报机构 / 南方联盟 | 中立缓冲带（银湾） |
| 悬疑 | 官方调查组 / 民间侦探 / 嫌疑人方 / 掩护势力 / 真相持有者 | 医院 / 殡仪馆 / 独立记者 |
| 商战 | 敌对公司 / 友商联盟 / 投行 / 律所 / 家族企业 | 董事会 / 收购中介 / 反垄断局 |
| 校园 | 学生会 / 教师派系 / 社团联盟 / **校外势力** / 学生小团体 | 图书馆 / 匿名树洞 / 校外咖啡馆 |
| 情感 | 女方家族 / 男方家族 / 前段关系网 / 现段关系网 / 闺蜜兄弟圈 | 心理咨询 / 婚礼场地 / 共同友人 |
| 穿越 | **原时空派系 + 新时空派系**（双 matrix 共存一文件） | 两界渡（裂隙观测站） |
| 修仙 | 宗门 / 皇朝 / 秘境主 / 散修联盟 / 魔道 | 坊市 / 拍卖会 / 秘境入口 |
| 封闭囚笼 | 狱政当局 / 狱霸帮派 / 内线 / 家属互助网 / 走私势力 | 放风场（唯一公共空间） |
| 宫廷权谋 | 后党 / 贵妃系 / 权臣 / 宦官 / 储君党 | 朝会鼓楼（禁动刀兵） |
| 末日废土 | 市政残部 / 军阀 / 幸存者聚落 / 末日教会 / 商队 | 旧站集市（安全交易地） |
| 谍战 | 我方情报机关 / 敌国渗透组 / 双重间谍网 / 地下抵抗网 / 中立线人 | 接头暗点（茶楼） |
| 江湖武侠 | 正道剑派 / 天下大帮 / 药毒谷 / 镖局联盟 / 杀手情报楼 | 通衢客栈（栈内禁斗） |

---

## 各题材横向对照

- **矩阵密度**：全部 5×15，完全对齐
- **NPC 数**：14 题材 10-15，量级一致
- **tension_seeds 数量**：全部每国 2-3 条
- **增强字段**：14 个精写题材均含 5 类扩展（core_npcs / key_locations / history / world_tech / opening_situation）
- **命名风格**：硬科幻题材音译（卡萨德/麟河/奥斯特），其余题材各自风格化（都市用场景派生、军事用硬核现代、校园用场景词、情感用姓氏、穿越双时空对比、修仙全古风音译、武侠用门帮谷会楼、宫廷用殿阁司堂、谍战用代号隐喻、废土用废墟环境词、囚笼用封闭机构词）

---

## 使用流程

```bash
cd <技能根目录>

# 1. 选题材开局（例如修仙精写）
python scripts/save.py init --slot my_xiuxian --mode custom
python scripts/save.py world-init --slot my_xiuxian --payload world/cultivation-detailed.json

# 2. 进入游戏：对 agent 说"开始游戏"
#    agent 会读取 SKILL.md，从 saves/my_xiuxian/world.json 加载世界
#    然后按 SKILL.md 开局流程问你选身份（旅人/本地人/空白身世）

# 3. 回合循环：自由文本行动 → agent 解析 → 掷骰 → 写回
```

---

## 跨题材命名区隔核查：全部通过

所有 14 个世界的**势力词根**与**实体 id** 在题材间互不复用（词根 = 国名/势力名前 2 字；id = `nation_*`/`port_*` 前缀）。此前存在的 3 组跨题材重名已全部消除，另有 1 处撞现实地名的改名：

| 词根 | 最终保留处 | 已改名处 |
|---|---|---|
| 北岭 | 军事 · 北岭联邦（`nation_beiling`） | 现代都市：北岭资本 → **鼎丰资本**（`nation_dingfeng`）；穿越：北岭集团 → **浔海集团**（`nation_xunhai`） |
| 东岸 | 穿越 · 东岸总署（`nation_dongan`） | 现代都市：东岸集团 → **东浦集团**（`nation_dongpu`） |
| 沈氏 | 情感 · 沈氏旧部（`nation_shenshi`） | 商战：沈氏实业 → **郑氏实业**（`nation_zhengshi`），NPC 沈烨/沈伯 → 郑烨/郑伯 |
| 关岛 | ——（与既有题材不冲突，但撞现实地名 Guam，故改名） | 谍战：关岛线 → **孤星线**（`nation_guxing`） |

**命名区隔规则**：不同题材的世界不得复用同一词根或同一实体 id；词根（国名/势力名前 2 字）在所有题材间须唯一（见 `world-gen-protocol.md` §5.3 跨题材命名区隔）。理由：便于玩家跨题材快速区分，避免"换皮观感"。3 处改名的世界均已重跑 `save.py world-init` 校验通过（5 势力 / 15 对矩阵）。
