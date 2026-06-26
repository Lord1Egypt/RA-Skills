# dimens-manager 报表章节 Recharts 组件生成规范

## 1. 文档目标

这份文档专门约束：

1. 当前报表前端真实渲染引擎是 `recharts@3.6.0`
2. Skill 在生成报表组件时，必须按前端真实支持的 `type + dataMapping + chartConfig` 输出
3. 当数据源来自多维表格时，必须同时补齐 `dataSource.sheet` 元信息和最终 `dataMapping`

它不是接口文档，而是“如何一次生成成功”的生成规范。

---

## 2. 当前前端真实组件类型

以下类型来自前端真实实现 [ChartRenderer.tsx](/Users/lixiang/data/代码库管理/binterAi/多维项目开发/web/src/components/report/charts/ChartRenderer.tsx)：

| 组件类型 | 前端支持状态 | 说明 |
| --- | --- | --- |
| `line` | 已支持 | 折线图 |
| `bar` | 已支持 | 柱状图，支持横向 / 纵向布局 |
| `area` | 已支持 | 面积图 |
| `pie` | 已支持 | 饼图 / 环图 |
| `composed` | 已支持 | 组合图，当前是柱 + 线 |
| `radar` | 已支持 | 雷达图 |
| `scatter` | 已支持 | 散点图 |
| `funnel` | 已支持 | 漏斗图 |
| `radialBar` | 已支持 | 径向柱图 |
| `treemap` | 已支持 | 矩形树图 |
| `stat` | 已支持 | 指标卡 |
| `heatmap` | 已支持 | HTML 自绘，不是 Recharts 原生图 |
| `timeline` | 已支持 | HTML 自绘，不是 Recharts 原生图 |
| `table` | 已支持 | 表格占位视图，不走 Recharts 图形渲染 |
| `wordCloud` | 已支持 | HTML 自绘词云 |

Skill 不要输出前端未支持的图表类型名，也不要自造 `chartType`。

---

## 3. 数据结构分层

报表组件成功渲染至少涉及四层：

| 层级 | 作用 | 是否必看 |
| --- | --- | --- |
| `type` | 决定用哪个前端图表组件 | 必填 |
| `dataSource` | 说明数据来自哪里 | 必填 |
| `dataMapping` | 告诉图表用哪一列做维度 / 数值 / 系列 | 必填 |
| `chartConfig` | 控制样式、布局、半径、曲线类型等 | 选填，但不能乱写 |

### 3.1 `dataSource` 和 `dataMapping` 不是一回事

这是最容易生成失败的点。

| 字段 | 作用 | 示例 |
| --- | --- | --- |
| `dataSource.sheet.recommendedMapping` | 给系统的推荐映射，通常是规范化键名 | `nameKey: "name", valueKey: "value"` |
| `dataSource.sheet.previewMapping` | 预览 / 查询层建议映射，常带聚合、排序、limit | `aggregation: "sum"` |
| `dataMapping` | 真正给前端渲染层使用，通常是实际列名 | `nameKey: "名称", valueKey: "销售额"` |

结论：

- `recommendedMapping` 不能替代 `dataMapping`
- 有 `sheet.columns` 也不能省略 `dataMapping`
- 只给 `dataMapping` 不给 `sheet.fieldIds / previewMapping`，查询链路也容易失败

---

## 4. 多维表格数据源的必填清单

当 `dataSource.mode = "sheet"` 时，至少应补齐下面这些字段：

```json
{
  "dataSource": {
    "mode": "sheet",
    "sheet": {
      "sheetId": "sh_xxx",
      "sheetName": "数据管理",
      "columns": [
        { "fieldId": "fld_name", "label": "名称", "type": "text" },
        { "fieldId": "fld_value", "label": "销售额", "type": "number" }
      ],
      "fieldIds": ["fld_name", "fld_value"],
      "recommendedMapping": {
        "nameKey": "name",
        "valueKey": "value"
      },
      "previewMapping": {
        "nameKey": "name",
        "valueKey": "value",
        "aggregation": "sum",
        "sort": {
          "key": "销售额",
          "order": "desc"
        },
        "limit": 10
      },
      "limit": 10
    }
  },
  "dataMapping": {
    "nameKey": "名称",
    "valueKey": "销售额",
    "limit": 10
  }
}
```

### 4.1 字段选择规则

| 场景 | 维度字段 | 数值字段 |
| --- | --- | --- |
| 折线 / 柱状 / 面积 / 饼图 | 文本、日期、枚举类字段 | 数字字段 |
| 组合图 | 一列维度 + 至少一列数值 | 当前默认主值走 `valueKey`，趋势可走 `trend` |
| 散点图 | 一列数字作为 `x` | 一列数字作为 `y` |
| 雷达图 / 漏斗 / 矩形树图 | 类别字段 | 数字字段 |
| 指标卡 | 可无类目字段 | 一列聚合后的数字字段 |

### 4.2 系统字段使用规则

系统字段如：

- `__system_createTime`
- `__system_updateTime`
- `__system_createdBy`
- `__system_updatedBy`

可以作为候选字段出现在 `sheet.columns`，但不要默认把它们拿来做主维度或主指标，除非用户明确要求按创建时间、更新时间、创建人等维度出图。

---

## 5. 各图表类型的最小成功模板

### 5.1 折线图 / 柱状图 / 面积图

最小要求：

- `dataMapping.nameKey`
- `dataMapping.valueKey`
- `dataSource.sheet.fieldIds`

模板：

```json
{
  "type": "line",
  "title": "销售趋势",
  "dataSource": {
    "mode": "sheet",
    "sheet": {
      "sheetId": "sh_xxx",
      "sheetName": "订单表",
      "columns": [
        { "fieldId": "fld_date", "label": "月份", "type": "text" },
        { "fieldId": "fld_amount", "label": "销售额", "type": "number" }
      ],
      "fieldIds": ["fld_date", "fld_amount"],
      "recommendedMapping": { "nameKey": "name", "valueKey": "value" },
      "previewMapping": { "nameKey": "name", "valueKey": "value", "aggregation": "sum", "limit": 12 },
      "limit": 12
    }
  },
  "dataMapping": {
    "nameKey": "月份",
    "valueKey": "销售额",
    "limit": 12
  },
  "showLegend": true,
  "showGrid": true,
  "showTooltip": true
}
```

### 5.2 组合图 `composed`

当前前端实现是：

- 柱状部分固定读 `valueKey`
- 折线部分优先读 `trend`，没有 `trend` 时回退到 `valueKey`

因此如果想让组合图真正体现“双序列”，数据里最好包含：

```json
{
  "name": "Q1",
  "value": 500,
  "trend": 100
}
```

如果底层多维表还没有 `trend` 对应字段，Skill 应明确说明当前会退化成单值组合图，不要假装是完整双轴分析。

### 5.3 饼图 `pie`

最小要求：

- 类别字段唯一性尽量高
- 数值字段必须可累计
- 可选 `chartConfig.innerRadius` 控制是否为环图

### 5.4 散点图 `scatter`

最小要求：

- `dataMapping.nameKey` 最终会被转成 `x`
- `dataMapping.yKey` 必须明确
- `valueKey` 可作为兜底数值

模板：

```json
{
  "type": "scatter",
  "dataMapping": {
    "nameKey": "客单价",
    "yKey": "利润率",
    "valueKey": "利润率"
  }
}
```

### 5.5 指标卡 `stat`

最小要求：

- 最终数据必须能落成单值
- 默认取 `data[0][valueKey]`
- 如果有对比值，前端会拿 `data[1][valueKey]` 作为上期

---

## 6. 展示层建议默认值

如果用户没有特殊要求，建议生成以下默认值：

```json
{
  "colSpan": 6,
  "height": 300,
  "description": "User added widget",
  "chartConfig": null,
  "showLegend": true,
  "showGrid": true,
  "showDataLabels": false,
  "showTooltip": true
}
```

说明：

- `chartConfig` 可以为 `null`
- 但不能把不存在的配置键乱塞给前端
- `bar` 的横向布局要放在 `chartConfig.layout = "horizontal"`
- `pie` 的环图要放在 `chartConfig.innerRadius`

---

## 7. 一次生成成功 Checklist

生成报表组件前，Skill 应强制检查：

1. 图表 `type` 是否属于前端真实支持列表
2. 是否明确 `sheetId`
3. 是否明确维度字段和数值字段
4. `sheet.columns` 是否包含实际字段标签和类型
5. `sheet.fieldIds` 是否与选中字段一致
6. `recommendedMapping` 是否使用规范键名
7. `dataMapping` 是否使用真实字段标签
8. 是否明确 `limit`
9. 是否给出默认展示配置
10. 如果是 `composed` / `scatter` / `stat` 这类特殊图，是否补齐特殊字段要求

只要上面任一项缺失，Skill 就不应该直接说“可以创建成功”。

---

## 8. 常见错误

| 错误写法 | 为什么错 | 正确做法 |
| --- | --- | --- |
| 只写 `type: line` 和 `sheetId` | 前端不知道拿哪列做横轴和纵轴 | 同时补 `sheet.columns`、`fieldIds`、`dataMapping` |
| 把 `recommendedMapping` 直接当最终映射 | 推荐映射是规范层，不是渲染层 | `dataMapping` 仍然要写实际列名 |
| 给饼图使用文本数值字段 | Recharts 无法累计 | 数值字段必须是 `number` 或可转数值 |
| 组合图只有 `valueKey` 却宣称双序列 | 当前前端第二条线优先读 `trend` | 没有 `trend` 时明确说明退化 |
| 默认拿系统字段做图 | 很容易不符合业务意图 | 系统字段只在用户明确要求时使用 |
