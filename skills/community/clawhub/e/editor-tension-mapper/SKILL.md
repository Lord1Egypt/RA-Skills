# Skill: editor-tension-mapper — 张力绘图师

## 用途
自动绘制剧本的张力曲线（Tension Curve），检测平段、过山车、单调递增等节奏问题。用量化数据验证故事的节奏感，而非依赖主观判断。

## 触发时机
- 阶段 3：Beat Sheet 生成后，验证张力曲线合理性
- 阶段 4 Stage 1.5：Story Impact Review 时，提供张力曲线数据

---

## 核心能力：Tension Curve Mapping

### 张力评分标准（1-10 分）

| 分值 | 含义 | 观众状态 |
|------|------|---------|
| 1-2 | 极低张力 | 放松、呼吸、建立情感 |
| 3-4 | 低张力 | 好奇、轻微不安、铺垫 |
| 5-6 | 中等张力 | 紧张、期待、矛盾升级 |
| 7-8 | 高张力 | 焦虑、屏息、冲突爆发 |
| 9-10 | 极高张力 | 窒息、心碎、生死一线 |

### 张力曲线绘制

对每场戏评分后，生成张力曲线数据：

```json
{
  "tension_curve": [
    { "scene": 1, "tension": 3, "emotion": "好奇", "note": "新世界引入" },
    { "scene": 2, "tension": 5, "emotion": "紧张", "note": "冲突初现" },
    { "scene": 3, "tension": 7, "emotion": "焦虑", "note": "危机升级" },
    { "scene": 4, "tension": 4, "emotion": "释然", "note": "呼吸段" },
    { "scene": 5, "tension": 6, "emotion": "期待", "note": "蓄力" },
    { "scene": 6, "tension": 9, "emotion": "窒息", "note": "高潮爆发" },
    { "scene": 7, "tension": 5, "emotion": "感慨", "note": "余波与收束" }
  ],
  "diagnostics": {}
}
```

---

## 诊断规则

### 1. 平段检测（Flat Segment）

**条件**：连续 3 场戏张力波动 ≤ 1

**诊断**：`FLAT_SEGMENT`
**建议**：在平段中插入微转折或情感变奏，避免观众注意力流失

### 2. 过山车检测（Whipsaw）

**条件**：相邻两场戏张力差 ≥ 5

**诊断**：`WHIPSAW`
**建议**：大起大落之间需要过渡场景，否则观众情感跟不上

### 3. 单调递增检测（Monotonic Climb）

**条件**：全场戏张力只升不降

**诊断**：`MONOTONIC_CLIMB`
**建议**：必须插入呼吸段（breather scenes），全程紧绷 = 观众疲劳

### 4. 中点塌陷检测（Midpoint Collapse）

**条件**：中点附近（场景 40%-60% 位置）张力 ≤ 全剧中位数

**诊断**：`MIDPOINT_COLLAPSE`
**建议**：中点必须有转折或升级，这是故事的"第二次启动"

### 5. 终章减速检测（Finale Deceleration）

**条件**：最后 1/3 张力均值 < 前 2/3 张力均值

**诊断**：`FINALE_DECELERATION`
**建议**：终章必须加速，节奏只能越来越快直到高潮

### 6. 呼吸段缺失检测（No Breather）

**条件**：高张力段（≥7）之后没有低张力段（≤4）衔接

**诊断**：`NO_BREATHER`
**建议**：观众需要消化高强度情感，给一个缓冲场景

---

## 输出

### 诊断报告格式

```json
{
  "tension_curve": [...],
  "diagnostics": {
    "issues_found": ["MIDPOINT_COLLAPSE", "NO_BREATHER"],
    "details": [
      {
        "issue": "MIDPOINT_COLLAPSE",
        "affected_scenes": [4],
        "current_tension": 3,
        "recommended_tension": 6,
        "suggestion": "场景4需要增加转折，可作为故事方向的第二次启动"
      },
      {
        "issue": "NO_BREATHER",
        "after_scene": 5,
        "current_tension": 9,
        "suggestion": "场景6需要降为低张力呼吸段，让观众消化高潮冲击"
      }
    ],
    "overall_verdict": "NEEDS_ADJUSTMENT",
    "curve_health_score": 6.5
  }
}
```

### 判定规则

| curve_health_score | 判定 | 处理 |
|---|---|---|
| ≥ 8 | HEALTHY | 张力曲线合理，继续 |
| 5-7 | NEEDS_ADJUSTMENT | 需按 diagnostics 建议调整场景张力 |
| < 5 | UNHEALTHY | 强制打回阶段 3，重写节拍表 |

---

## 与其他 Skill 的协作

- **editor-story-architect**：提供 tone_blueprint.tension_peaks 和 breather_scenes 作为设计目标
- **editor-scene-painter**：高张力场景需配备最强视觉记忆点
- **editor-adversarial-reviewer**：审查时可参考张力曲线数据

---

## 禁止事项

- ❌ 不得用"感觉"评分——每场戏的张力值必须有明确的观众状态对应
- ❌ 不得为了"曲线好看"而篡改故事逻辑——张力服务于故事，不是反过来
- ❌ 不得忽视诊断结果——任何 detected issue 都必须在创作层面回应
