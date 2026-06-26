# 复习计划生成规范

## 一、知识结构图（echarts_tree_data）

### 数据格式

生成一个 JSON 对象，直接嵌入 `{{echarts_tree_data}}` 占位符，作为 ECharts 树图的数据源。

**根节点**：
```json
{
  "name": "📚 {exam_type}",
  "itemStyle": { "color": "#6C63FF", "borderColor": "#6C63FF" },
  "children": [ ...类别节点 ]
}
```

**类别节点**（每个 category 一个）：

`color` 和 `borderColor` 按该类别最高 importance 取值：

| 最高 importance | color |
|----------------|-------|
| ≥ 0.8 | `#FF4757`（红色，高优先级）|
| 0.6–0.79 | `#F0920A`（橙色，中优先级）|
| < 0.6 | `#18A85A`（绿色，低优先级）|

```json
{
  "name": "微积分",
  "hours": "4.5",
  "itemStyle": { "color": "#FF4757", "borderColor": "#FF4757" },
  "label": { "color": "#FF4757", "fontWeight": "bold" },
  "children": [ ...考点节点 ]
}
```

**考点节点**（每个 point 一个叶节点）：

- `is_weak_point = true` → name 前加 `⚠️`，color 用 `#FF4757`
- `coverage_gap = true` → name 后加 ` 📖`
- 普通考点 → color 继承类别色（用 `#9CA3AF` 浅灰）
- `evidence` 字段（取 point.evidence[0]，若有）存入节点的 `evidence` 属性供 tooltip 展示

```json
{
  "name": "⚠️ 极限计算",
  "evidence": "出现于历年真题第3题",
  "itemStyle": { "color": "#FF4757", "borderColor": "#FF4757" }
}
```

**类别排序**：按该类别最高 importance 降序；同分时薄弱点类别优先。

**溢出处理**：单类别考点 > 6 个时，按 importance 降序取前 6 个，末尾追加：
```json
{ "name": "…及{N}个考点", "itemStyle": { "color": "#9CA3AF" } }
```

**时长计算**（存入类别节点 `hours` 字段）：
```
单考点时长 = importance × 3h，上下限 [0.5h, 3h]，取 0.5h 步长
紧急模式（days_remaining ≤ 7）：× 0.75
充裕模式（days_remaining > 30）：× 1.2
类别时长 = Σ 该类别所有展示考点时长（保留一位小数）
```

### 完整示例

```json
{
  "name": "📚 高等数学冲刺",
  "itemStyle": { "color": "#6C63FF", "borderColor": "#6C63FF" },
  "children": [
    {
      "name": "微积分",
      "hours": "7.5",
      "itemStyle": { "color": "#FF4757", "borderColor": "#FF4757" },
      "label": { "color": "#FF4757", "fontWeight": "bold" },
      "children": [
        {
          "name": "⚠️ 极限计算",
          "evidence": "出现于历年真题",
          "itemStyle": { "color": "#FF4757", "borderColor": "#FF4757" }
        },
        {
          "name": "导数与微分",
          "itemStyle": { "color": "#9CA3AF", "borderColor": "#9CA3AF" }
        },
        {
          "name": "不定积分 📖",
          "itemStyle": { "color": "#9CA3AF", "borderColor": "#9CA3AF" }
        }
      ]
    },
    {
      "name": "线性代数",
      "hours": "4.0",
      "itemStyle": { "color": "#F0920A", "borderColor": "#F0920A" },
      "label": { "color": "#F0920A", "fontWeight": "bold" },
      "children": [
        {
          "name": "矩阵运算",
          "itemStyle": { "color": "#9CA3AF", "borderColor": "#9CA3AF" }
        },
        {
          "name": "⚠️ 行列式",
          "evidence": "错题笔记高频",
          "itemStyle": { "color": "#FF4757", "borderColor": "#FF4757" }
        }
      ]
    }
  ]
}
```

---

## 二、薄弱点预警（weak_points_html）

筛选 knowledge_map.points 中 is_weak_point = true 的所有考点，按 importance 降序。

每条生成一个 `<div class="wp-item">` 块：
- wp-name：考点名
- wp-cat：所属类别名
- wp-evidence：取 point.evidence[0]（若为空则填"出现于知识库标注"）

```html
<div class="wp-item">
  <div class="wp-header">
    <span class="wp-name">极限计算</span>
    <span class="wp-cat">微积分</span>
  </div>
  <div class="wp-evidence">出现在错题笔记与历年真题中</div>
</div>
```

薄弱点为 0 时：输出一个提示块：
```html
<div class="wp-item" style="border-left-color:var(--color-low)">
  <div class="wp-header">
    <span class="wp-name" style="color:var(--color-low)">暂无标注薄弱点</span>
  </div>
  <div class="wp-evidence">知识库中未发现错题或薄弱标注，整体掌握良好。</div>
</div>
```

---

## 三、复习计划（study_plan_html）

### 渲染模式与阶段数

| 模式 | 触发条件 | 阶段数 | plan_mode 文本 |
|------|---------|--------|--------------|
| 紧急 | days_remaining ≤ 7 | 逐日 | ⚡ 紧急冲刺 |
| 标准 | 8–30 天 | 3 | 📘 标准复习 |
| 充裕 | > 30 天 | 4 | 📅 充裕备考 |

### 标准模式（3阶段）

```
阶段1（前40%天数）：基础夯实 → importance ≥ 0.8 的考点
阶段2（中40%天数）：重点突破 → importance 0.6–0.79 的考点 + 薄弱点一轮
阶段3（后20%天数）：冲刺收尾 → 全部薄弱点 + 高频考点回顾
```

### 充裕模式（4阶段）

```
阶段1（前25%）：全局预习 → 所有考点浏览（建立知识框架）
阶段2（25–55%）：系统学习 → 所有考点详细复习
阶段3（55–80%）：重点强化 → importance ≥ 0.75 + 薄弱点
阶段4（后20%）：冲刺收尾 → 薄弱点 + coverage_gap 补充 + 高频回顾
```

### 紧急模式（逐日）

每天一个阶段，只纳入 importance ≥ 0.8 的考点，按 importance 降序分配到各天，平均每天 2–4 个考点。

### phase-focus class 规则

| 阶段重点 | class |
|---------|-------|
| 仅 importance ≥ 0.8 | high |
| 混合中高优先级 | mid |
| 薄弱点/收尾 | high |
| 全局/综合 | all |

### HTML 片段示例

```html
<div class="plan-phase">
  <div class="plan-phase-header">
    <div class="phase-label">第一阶段</div>
    <div class="phase-range">5月7日 - 5月14日 · 8天</div>
    <div class="phase-focus high">重点突破</div>
  </div>
  <div class="plan-topics">
    <div class="plan-topic">
      <div class="topic-cat">📐 微积分</div>
      <div class="topic-points">极限计算、导数与微分、不定积分</div>
      <div class="topic-time">6h</div>
    </div>
    <div class="plan-topic">
      <div class="topic-cat">📊 线性代数</div>
      <div class="topic-points">矩阵运算、行列式</div>
      <div class="topic-time">3h</div>
    </div>
  </div>
</div>
```

**日期计算**：阶段起始日 = 当前日期（今天），按天数比例切分，终止日 = exam_date 前一天。
