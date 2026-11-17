# Echo Map 工作流与提示词骨架

> 配套 `echo-map` 子技能。语义映射由 LLM 完成；脚本只做脱敏与契约兜底。

---

## §1 抽取 → 映射（严格按 mapping_dict）

从脱敏后的经历中抽 6 类要素，逐槽映射到 DND：

| 现实要素 | 槽位 | 映射目标 | 取值约束（来自字典 candidates） |
|:----|:-----|:----|:-----|
| 人物（同事/对手/贵人） | `person` | 种族+职业+阵营 | race/class/alignment 候选集 |
| 掌握资源者（老板/甲方/体制） | `authority` | 贵族/术士/邪术师 + 派系 | 倾向守序/邪恶 |
| 守护者/导师 | `guardian` | 圣武士/牧师/德鲁伊 | 倾向善良 |
| 核心冲突/阻碍 | `conflict` | 反派原型 + 怪物类型 + CR | 用 `cr_scale` 定紧张度 |
| 地点/空间 | `location` | 地城/城市/荒野/异界 节点 | map_type + location_node |
| 目标/争夺物 | `objective` | 神器/被窃圣物/诅咒物 + quest_goal | artifact + quest_goal |
| 情绪基调 | `tone` | adventure_tone | 英雄/暗黑/喜剧/史诗/恐怖 |
| 时间跨度 | `timespan` | 模组时长档 + 编年史事件 | 单场/短/战役 |

### 映射要点
- **人物三元组**：按 `role_presets` 的角色定位（技术型→法师、资源型→吟游诗人…）选职业；阵营按其在经历中的行为倾向定。
- **冲突 CR**：用 `conflict.cr_scale`——日常摩擦 CR¼–1，项目危机 CR2–4，跨组织大战 CR5–8，人生级灾难 CR10+。
- **地点节点**：`location_node` 已给直译（办公室→议事厅/密室，通勤路→荒野小径，服务器→异界神殿…）。

---

## §2 提示词骨架（LLM 内部使用）

```
你将用户的真实经历改写为 DND 5e 冒险。已脱敏，不得出现真实姓名/机构名/地名。

【经历（已脱敏）】
<<anon_story>>

【映射字典摘要】
<<mapping_dict 的 slots + candidates 摘要>>

步骤：
1. 抽取 6 类要素（人物/权威/守护者/冲突/地点/目标/基调/时长）。
2. 逐槽映射：人物→种族+职业+阵营；冲突→反派+怪物类型（CR 按 cr_scale）；地点→设定节点。
3. 复用功能二模组 JSON 结构输出：
   title / pitch / level_range / type / premise / factions / npcs / locations / acts / rewards / timeline / hooks_for_current_campaign
4. 末尾附 chronicle_note：这段经历在费伦编年史中可记为何事。
要求：叙事有趣、不自怜；怪物可按费伦原生怪物替换；不要暴露任何真实信息。
```

---

## §3 输出契约（normalize 校验）

最终 JSON 须含：`title, pitch, level_range, type, premise, factions, npcs, locations, acts, rewards, timeline, hooks_for_current_campaign, chronicle_note`。

`echo_map.py normalize` 会：
- 对全部字符串值执行脱敏替换（真实名→幻想名）；
- 若缺 `chronicle_note` 自动补占位；
- 缺 `title/premise/npcs/acts` 任一时打印警告；
- 追加 `_meta`（字典版本 + 隐私声明）。
