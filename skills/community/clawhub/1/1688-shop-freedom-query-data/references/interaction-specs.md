# 交互组件详细规范

本文档定义了本 Skill 中所有交互组件的具体数据结构与映射规则。

## 1. select_api (Card 组件)

### 组件类型
`type: card`

### 数据槽位定义
- **`apis`**:
  - 类型: `Array<Object>`
  - 映射规则: 从 `rag_query` 返回的 `data.data` 数组转换而来，每个元素包含：
    - `id`: 接口唯一标识（如 `portal/core/overview`）
    - `name`: 接口名称（从 `# 接口名称\\|` 提取）
    - `description`: 接口描述简述（从 `> 描述文字` 提取，限制 50 字符内）
    - `dataSource`: 数据源标识（如 `SYCM`）
  - 必须字段: `id`, `name`, `description`

### 完整数据示例

```json
{
  "apis": [
    {
      "id": "portal/core/overview",
      "name": "核心数据概览",
      "description": "获取店铺核心经营数据的全量概览快照",
      "dataSource": "SYCM"
    },
    {
      "id": "transaction/getTradeCoreIndex",
      "name": "交易概况核心指标",
      "description": "获取交易概况的核心指标全量数据",
      "dataSource": "SYCM"
    }
  ]
}
```

### 端侧渲染选项
端侧会根据 `apis` 数组自动生成选项卡片，每个选项显示：
- 选项文本: `{name} — {description}`
- 选中后返回: `{id}`

---

## 2. select_time_range (Card 组件)

### 组件类型
`type: card`

### 数据槽位定义
- 无额外数据槽位（固定选项）

### 框架自动填充的字段
端侧根据 `selectionType: "time_range"` 自动注入以下固定选项：

| 选项文本 | 对应 dataType 值 |
|---------|----------------|
| 今天 | `RECENT_1` |
| 近7天 | `RECENT_7` |
| 近30天 | `RECENT_30` |
| 本周 | `WEEK` |
| 本月 | `MONTH` |

### 完整数据示例

```json
{}
```

### 端侧渲染选项
端侧自动渲染以下选项卡片：
- 今天
- 近7天
- 近30天
- 本周
- 本月

选中后返回对应的 `dataType` 值（如 `RECENT_7`）。

---

## 3. select_data_export (Card 组件)

### 组件类型
`type: card`

### 数据槽位定义
- 无额外数据槽位（固定选项）

### 框架自动填充的字段
端侧根据 `selectionType: "data_export_selection"` 自动注入以下固定选项：

| 选项文本 | 返回值 |
|---------|--------|
| 生成可视化网页 — 将数据生成交互式 HTML 数据看板 | `visualize` |
| 导出 Excel — 将数据导出为结构化 Excel 文件 | `excel` |
| 不需要 — 到此结束 | `skip` |

### 完整数据示例

```json
{}
```

### 端侧渲染选项
端侧自动渲染以下选项卡片：
- 生成可视化网页
- 导出 Excel
- 不需要

选中后返回对应的操作标识（如 `visualize`、`excel`、`skip`）。
