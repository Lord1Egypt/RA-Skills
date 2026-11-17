# Module Forge 工作流与提示词骨架

> 配套 `module-forge` 子技能。脚本负责「结构 + CR 预算」，LLM 负责「叙事血肉」。

---

## §1 脚本已确定的部分（无需 LLM 计算）

- **分幕数**：short=2 / medium=3 / long=5。
- **每幕难度曲线**：开场 Medium → 中段 Hard → 终幕 Deadly（高潮）。
- **每场 XP 预算**：`XP_THRESHOLDS[level][难度] × 玩家数`（DMG 标准表）。
- **怪物建议**：在 `[level-4, level+2]`（高潮 +3）CR 窗口内，选利用率最高的「单一怪物类型 × 数量」组合，并按多怪乘数核算调整 XP。

> 这些数值 **必须来自脚本输出**，LLM 不自算 CR / AC / XP（遵守 dnd-dm-skill 红线第 9 条）。

---

## §2 LLM 填充叙事（提示词骨架）

```
基于以下模组骨架 JSON，撰写可游玩的模组叙事（中文）：

<<module_forge.py 输出>>

要求：
1. premise：用 2–3 句设定钩子开场，呼应基调「<<tone>>」。
2. 每个 act.beat 扩写成一幕场景：环境描写 + 一个社交/探索节点 + 一场战斗（用 suggested 怪物）。
3. factions / npcs：给每个 NPC 一句口头禅与一个动机（不要改 suggested 的 CR/职业）。
4. 终幕 Deadly 战斗后给一段「余波」与可能续接《<<现役战役>>》的钩子。
5. 不要自行修改怪物数量/CR（平衡已由脚本保证）；如需更强反派，用「加一个非战斗 Boss」而非改数值。
```

---

## §3 时长档 → 节奏参考

| 时长档 | 分幕 | 遭遇数 | 适合 |
|:----|:----|:----|:----|
| short | 2 | 2–3 | 单晚跑团 / 试玩 |
| medium | 3 | 4–6 | 标准战役的单个任务弧 |
| long | 5 | 8–10 | 跨多周的战役级模组 |

---

## §4 与另两功能的衔接

- **→ world-lore**：生成前用 `lens_rag.py --anchor` 或 `lore_query.py pack` 检索地点/派系，保证设定一致。
- **→ echo-map**：把真实经历映射出的 `final.json` 作为 `premise/npcs/locations` 输入，再跑本脚本做 CR 平衡（覆盖 level_range / duration）。
