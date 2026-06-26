# Skill: editor-story-architect — 故事建筑师

## 用途
在剧本创作的最上游，负责 Story Premise 校验、Story Architecture Map 设计和情感弧线规划。是整个创作流程的"承重墙"——没有它，故事没有骨架。

## 触发时机
- 阶段 1：Story Premise Extraction（故事前提提取与校验）
- 阶段 2：Story Architecture Map 生成（情感弧线 + 张力蓝图）

---

## 能力 1：Story Premise Extraction

不管输入是什么 Level，必须提炼出四个核心前提要素：

1. **Central Dramatic Question（核心戏剧问题）**
   - 这集故事让观众追问的终极问题是什么？
   - 例："张飞能不能独自守住长坂桥？"

2. **Protagonist's Want vs Need（主角的欲望 vs 真正需要）**
   - Want：角色以为自己想要的（表面目标）
   - Need：角色真正需要的（深层成长）
   - 好故事 = Want 与 Need 的冲突与和解

3. **Emotional Contract with Audience（与观众的情感契约）**
   - 这集向观众承诺的情感体验是什么？
   - 例："你会为一个看似粗犷的人的柔软内心而感动"

4. **What's at Stake?（什么处于危险中）**
   - 如果主角失败，会失去什么？（必须是观众在乎的东西）
   - 没有真正失去的可能 → 没有紧张感 → 没有故事

### 校验规则

| 校验结果 | 含义 | 处理 |
|---------|------|------|
| **Premise Solid** | 四要素齐全且有张力 | 进入阶段 2 |
| **Premise Weak** | 要素齐全但张力不足（Want=Need 或 Stake 太低） | 上报 help_requested，附诊断报告 |
| **Premise Missing** | 核心要素缺失 | 上报 help_requested，标为 Level-1（前提不成立） |

---

## 能力 2：Story Architecture Map 生成

为 execution_brief.json 增加 story_architecture 和 tone_blueprint 字段：

### story_architecture 结构

```json
{
  "structure_type": "三幕式 | 五幕式 | 丹·哈蒙故事圈 | 非线性",
  "midpoint_shift": "中点转折的精确描述",
  "dark_night_of_soul": "灵魂暗夜时刻（最关键的情感低谷）",
  "thematic_throughline": "主题贯穿线",
  "emotional_arc": [
    {
      "scene_range": "1-3",
      "target_emotion": "好奇+轻微不安",
      "dramatic_question": "这个新世界有什么危险？"
    }
  ]
}
```

### tone_blueprint 结构

```json
{
  "primary_tone": "冒险喜剧",
  "comedy_ratio": "40%",
  "tension_peaks": [3, 7],
  "breather_scenes": [4, 8],
  "emotional_ceiling": "最高情感强度点及触发条件",
  "emotional_floor": "最低情感强度点及触发条件"
}
```

### 张力曲线设计原则

1. **心电图原则**：张力曲线不能是平的，也不能只升不降——必须有起有伏
2. **低谷蓄力原则**：每个低谷都在为下一个高峰蓄力
3. **呼吸感原则**：紧张段之间必须有松弛段（breather scenes）
4. **中点裂变原则**：中点必须有转折，故事前后半段的驱动力必须不同
5. **终章加速原则**：最后 1/3 的节奏必须加速，不给观众喘息的机会

---

## 输入

- 任务 source_materials
- memory/ip-{IP名}.md（角色圣经、世界规则）
- workbench_get_artifact 获取的项目级物料

## 输出

- `premise_report.json`（阶段 1 产物）
- 更新 `execution_brief.json` 的 story_architecture + tone_blueprint（阶段 2 产物）

---

## 禁止事项

- ❌ 不得跳过四要素校验直接进入创作
- ❌ 不得在 Premise Weak 时自行"脑补"补全前提——必须上报 help_requested
- ❌ 不得设计没有情感低谷的弧线（没有 Dark Night = 没有共鸣）
- ❌ 不得设计没有呼吸段的节奏（全程紧绷 = 观众疲劳）
