# 功能二 · Module Forge（按需求自动生成模组）

> 子技能 `dnd-dm-skill:module-forge`
> 输入玩家人数 / 等级 / 时长档 / 冒险类型 / 设定 / 基调，输出 **带 CR 平衡预算** 的模组骨架 JSON。

## 何时调用

- 用户说「给我生成一个 X 级、Y 人、适合 Z 时长的模组」
- 需要快速产出结构化模组骨架（派系 / NPC / 分幕遭遇 / 钩子），再由 DM 填充叙事
- 功能三（echo-map）产出的经历映射草稿，可用本子技能做 CR 平衡

## 核心特性

1. **范式驱动**：从 `data/module_paradigms.json`（59 篇官方模组）按 等级重叠 / 类型 / 时长 选最相似的 3 个范式作结构参考。
2. **CR 平衡（确定性）**：用 DMG 标准表计算每场遭遇的队伍 XP 阈值（按角色等级），并反向建议怪物 CR 与数量（含多怪乘数）。
3. **设定一致性**：可选 `--anchor` 调用 world-lore 检索地点 / 派系锚点，避免与费伦设定冲突。

## 运行方式（脚本）

```bash
python "module-forge/scripts/module_forge.py" \
       --players 4 --level 5 --duration medium \
       --type 都市寻宝 --setting "被遗忘的国度/深水城" --tone 悬疑 \
       --anchor "深水城"          # 可选：检索设定锚点

# 紧凑 JSON（便于程序化下游）
python .../module_forge.py --players 4 --level 3 --duration short --type 地城探险 --json
```

参数说明：
- `--duration`：`short`(2–3 场) / `medium`(4–6 场) / `long`(8–10 场·战役级)，决定分幕数与遭遇数。
- `--level`：取队伍起始等级（用于 CR 预算）。
- 怪物为 CR 平衡建议，可按费伦原生怪物替换；脚本已在 `notes` 中注明。

## 标准循环

1. 收参数（人数 / 等级 / 时长 / 类型 / 设定 / 基调；缺失则向用户追问）。
2. 运行脚本得到骨架 JSON（含 `paradigm_reference` 与 `party_cr_budget`）。
3. 由你（LLM）据 `paradigm_reference` 的节奏 + `notes` 的怪物建议，填充叙事、NPC 台词、场景描写。
4. 如需更贴费伦，用 world-lore 检索锚点；如需把现实经历套进来，先走 echo-map。

> 提示词骨架与分幕/钩子写法见 **`references/module-forge-workflow.md`**。
