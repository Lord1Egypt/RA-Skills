# 图表使用手册（Chart Bindbook）

> 写代码前必读。每个组件包含：适用场景、禁用场景、API 签名。

---

## 页面骨架

```python
r = ReportBuilder("页面title")
r.header("大标题", "副标题", ["时间:2026-05-14", "来源:XX平台"])
r.nav([("核心指标", "#kpi"), ("平台对比", "#platform")])
r.footer("页脚文字")
```

```python
with r.section("章节id", "编号", "章节标题", "章节描述"):
    # 在此添加内容
```

```python
r.grid(2)       # 2/3/4 列布局
r.grid_end()
```

---

## KPI 卡片

**适用**：页面顶部展示 4-8 个核心经营指标

**禁用**：章节中间的数字展示（用 `metric_grid` 代替）

```python
r.kpi_grid()
r.kpi("标签", "数值", "单位", "变化说明", down=False)
r.kpi_end()
```

- `down=True` 表示下降（红色），`False` 为上升（绿色）
- ⚠️ 不支持 `color` 参数

---

## 卡片与图表容器

```python
r.card("卡片标题", dot_color=r.C_TAOBAO)
r.chart("chartId", size="normal")            # size="lg" 为 500px 高
r.card_end()
```

**适用**：`r.chart()` 仅用于 ECharts 图表（`chart_bar`/`chart_pie`/`chart_radar`/`chart_heatmap`/`chart_stacked_bar`/`chart_script`）

**禁用**：以下组件前面禁止加 `r.chart()`（它们自带 HTML 结构，误加会产生空白占位区）：
- `progress_group` / `progress_bar`
- `metric_grid` / `metric`
- `r.table()`
- `r.insight()`

---

## chart_bar（柱状图 / 双Y轴组合图）

### 适用场景
- 同类对象的数值大小对比或排名（如 TOP5 商品销量、各渠道 GMV）
- 一组对象同时有两个维度时，用 `dual_y=True` 组合柱+线（如销量柱 + 转化率线）

### 禁用场景
- 同一 series 的 `data` 数组中最大值/最小值 > 10 倍（小值柱子不可见）
- 不同量纲的绝对值混放（如"支付金额 79000"和"客单价 175"放在同一 series）

### API

```python
# 基础柱状图（渐变色 + 数值标签）
r.chart_bar("chartId",
    categories=["A", "B", "C"],
    series=[
        {"name": "销量", "data": [120, 200, 150], "gradient": ["#6cf7c2", "#3b82f6"]},
    ],
    show_label=True,
    yname="销量(万件)"
)

# 多系列
r.chart_bar("chartId",
    categories=["A", "B", "C"],
    series=[
        {"name": "系列A", "data": [120, 200, 150], "color": r.C_TAOBAO},
        {"name": "系列B", "data": [80, 160, 100], "color": r.C_DOUYIN},
    ],
    legend=["系列A", "系列B"]
)

# 双Y轴组合图（柱+线）
r.chart_bar("chartId",
    categories=["A", "B", "C"],
    series=[
        {"name": "销量", "data": [120, 200, 150], "gradient": ["#f76c8b", "#be185d"], "type": "bar"},
        {"name": "增长率", "data": [22, 15, 28], "color": r.C_XIAOHONGSHU, "type": "line", "yAxisIndex": 1},
    ],
    dual_y=True,
    show_label=True
)
```

---

## chart_pie（饼图 / 环形图）

### 适用场景
- 占比构成数据（各项加总 = 100% 或近似 100%）
- 渠道分布、客户类型占比、产品分类占比

### 禁用场景
- 有序数据（价格区间、时间序列）——饼图丢失顺序信息
- 超过 8 个分类——太多扇区无法辨认，改用 `chart_bar`

### API

```python
r.chart_pie("chartId",
    data=[
        {"value": 78.6, "name": "直播", "color": r.C_DOUYIN},
        {"value": 18.5, "name": "短视频", "color": r.C_ORANGE},
        {"value": 2.9, "name": "商城", "color": r.C_TAOBAO},
    ],
    inner_radius="45%",    # 可选，设置后变为环形图
    outer_radius="70%"     # 可选
)
```

---

## chart_radar（雷达图）

### 适用场景
- 2-4 个对象在 3-7 个**同量纲或已归一化维度**上的多维对比
- 数据已经是百分比或评分（0-100）等统一量纲

### 禁用场景
- 只有 1 个对象（无对比意义，只是一个多边形形状，看不出强弱）
- 各维度量纲不同且未归一化（如"销量 5000"和"转化率 3%"混放）
- 维度 < 3 个（退化为线段）

### API

```python
r.chart_radar("chartId",
    indicators=[
        {"name": "维度A", "max": 100},
        {"name": "维度B", "max": 100},
        {"name": "维度C", "max": 50},
    ],
    data=[
        {"name": "对象1", "value": [80, 90, 40], "color": r.C_DOUYIN},
        {"name": "对象2", "value": [60, 70, 45], "color": r.C_TAOBAO},
    ]
)
```

- `indicators[].max`：该维度的最大刻度值，应设为数据最大值的 1.2-1.5 倍
- ⚠️ 当前不支持数据点数值标签显示，读者通过 tooltip 悬浮查看具体数值

---

## chart_heatmap（热力图）

### 适用场景
- N 对象 × M 指标的矩阵，所有格子都是**同量纲连续数值**（如归一化评分 0-100、转化率）
- 至少 2×3 或 3×2 以上的矩阵规模

### 禁用场景
- 格子中是分类/布尔/枚举值（如"是否降权""有/无"）——热力图只适合连续数值
- 矩阵中大量格子为 0 或空（稀疏矩阵，大面积同色无信息量）
- x/y 轴维度不可量化比较（如"风险类型" + "有/无"二值）——用 `table` + 标签高亮

### API

```python
r.chart_heatmap("chartId",
    x_labels=["指标A", "指标B", "指标C"],
    y_labels=["对象1", "对象2"],
    data=[
        [0, 0, 92], [1, 0, 88], [2, 0, 78],   # [x_index, y_index, value]
        [0, 1, 95], [1, 1, 82], [2, 1, 88],
    ]
)
```

---

## chart_stacked_bar（堆积柱状图）

### 适用场景
- 有序区间的构成对比（如价格带各平台占比）
- 同一总量的内部分解（如各渠道贡献的 GMV 堆积）

### 禁用场景
- 两个独立指标的并列对比（如"投入成本" vs "成交金额"不是同一总量的组成部分）

### API

```python
r.chart_stacked_bar("chartId",
    categories=["0-50", "50-100", "100-150"],
    series=[
        {"name": "抖音", "data": [18.5, 32.4, 24.6], "color": r.C_DOUYIN},
        {"name": "淘宝", "data": [5.2, 12.8, 22.5], "color": r.C_TAOBAO},
    ]
)
```

---

## progress_bar（进度条）

### 适用场景
- 完成度、提及率、评分、渗透率等有"满格"概念的数据
- 数据组内最大值/最小值 ≤ 10 倍

### 禁用场景
- 数据组内极差 > 10 倍（小值条宽度 < 10%，内部数值文字不可见）
- 负值数据（进度条无法表达负数方向）

### max_val 设置规则
必须取数据组中最大值（或略大于最大值的整数），**禁止固定写 100**（除非数据本身就是百分比且最大值接近 100）。

### API

```python
r.progress_group()
r.progress_bar("尺码不准", 42.5, max_val=50, color=r.C_DOUYIN, suffix="高退货")
r.progress_bar("面料不符", 28.3, max_val=50, color=r.C_DOUYIN, suffix="高退货")
r.progress_bar("做工问题", 18.2, max_val=50, color=r.C_ORANGE, suffix="中等")
r.progress_group_end()
```

- `label`：左侧标签
- `value`：当前值（显示在进度条内部）
- `max_val`：最大值，决定宽度百分比
- `color`：渐变起始色
- `suffix`：右侧补充文字

---

## metric_grid（数字卡片网格）

### 适用场景
- 章节中间展示 3-6 个关键数字
- 指标间量纲各异或量级差距 > 10 倍，不适合放在同一图表中

### 禁用场景
- 超过 8 个数字（信息过载，改用表格）

### API

```python
r.metric_grid()
r.metric("32.4%", desc="抖音 50-100元占比", color=r.C_DOUYIN)
r.metric("51.1%", desc="淘宝 100-250元占比", color=r.C_TAOBAO)
r.metric_end()
```

- `value`：核心数字
- `unit`：单位（可选）
- `desc`：下方说明文字
- `color`：数字颜色

---

## table（数据表格）

### 适用场景
- 维度 ≥ 6 列或包含文本字段（品牌名、关键词、建议等）
- 图表无法表达的文本维度的补充展示

### API

```python
r.table(
    headers=["列1", "列2", "列3"],
    rows=[["数据A", "数据B", "数据C"]]
)
```

**单元格支持 HTML 透传**：
- 高亮标签：`<span class="tag tag-green">值</span>`（绿）、`tag-pink`（粉）、`tag-orange`（橙）、`tag-purple`（紫）
- 趋势色：`<span class="trend-up">↑</span>`（绿）、`<span class="trend-down">↓</span>`（红）、`<span class="trend-steady">→</span>`（黄）
- 星级：`<span class="stars">★★★☆☆</span>`

---

## insight（洞察框）

```python
r.insight("标题", ["要点 1", "要点 2", "要点 3"])
```

---

## chart_script（自定义 ECharts）

```python
r.chart_script("customChart", {
    "xAxis": {"type": "category", "data": ["A", "B"]},
    "yAxis": {"type": "value"},
    "series": [{"type": "scatter", "data": [[1, 2], [3, 4]]}]
})
```

---

## raw_html

```python
r.raw_html('<div class="custom">任意 HTML</div>')
```

---

## 颜色常量

| 变量 | 色值 | 用途 |
|------|------|------|
| `r.C_DOUYIN` | `#f76c8b` | 抖音 / 警示 / 下降 |
| `r.C_TAOBAO` | `#6c7af7` | 淘宝/天猫 / 主色 |
| `r.C_XIAOHONGSHU` | `#6cf7c2` | 小红书 / 正向 / 增长 |
| `r.C_ORANGE` | `#f7c96c` | 参考 / 中性 |
| `r.C_PURPLE` | `#c96cf7` | 辅助 |
