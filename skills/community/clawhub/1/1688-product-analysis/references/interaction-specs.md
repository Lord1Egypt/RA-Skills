# 交互组件详细规范

本文档定义了 1688-product-analysis Skill 中所有交互组件的具体数据结构与映射规则。

## 1. select_abnormal_offer (Table 组件)

### 组件类型

`type: table`

### 业务场景

在执行 `get_abnormal_offers` 获取异常商品列表后，以表格形式展示给用户，支持多选要诊断的商品。

### 数据槽位定义

- **`title`**:
  - 类型: `String`
  - 固定值: `"异常商品列表 — 请选择要诊断的商品"`

- **`columns`**:
  - 类型: `Array<Object>`
  - 说明: 表格列定义，每列包含 `key`（字段名）、`label`（列标题）、`width`（可选，列宽 px）

- **`rows`**:
  - 类型: `Array<Object>`
  - 映射规则: 从 `get_abnormal_offers` 返回的 `data.items` 数组逐条转换
  - 必须字段: `id`, `title`, `reason`, `payAmount`, `changeRate`

### 字段映射规则

从 `get_abnormal_offers` 返回的每条 item 转换为 table row：

| row 字段 | 来源字段 | 转换规则 |
|----------|----------|----------|
| `id` | `item.itemId` | 直接赋值（字符串） |
| `title` | `item.offerTitle` | 直接赋值 |
| `imageUrl` | `item.offerImageUrl` | 拼接前缀 `https://cbu01.alicdn.com/` + 原值 |
| `reason` | `item.reason` | 直接赋值（如 "支付下跌"、"访客下跌"） |
| `payAmount` | `item.valueMap.payAmt.value` | 格式化为金额字符串 `¥xx,xxx.xx` |
| `changeRate` | `item.valueMap.payAmt.cycleCrc` | 格式化为百分比 `xx.x%`，负值加红色标记 |
| `visitorCount` | `item.valueMap.uv.value` | 若存在则取值，否则为 `"-"` |
| `visitorChange` | `item.valueMap.uv.cycleCrc` | 若存在则格式化为百分比，否则为 `"-"` |

### 列定义

```json
[
  { "key": "imageUrl", "label": "图片", "width": 80 },
  { "key": "title", "label": "商品标题" },
  { "key": "reason", "label": "异常原因", "width": 120 },
  { "key": "payAmount", "label": "支付金额", "width": 120 },
  { "key": "changeRate", "label": "支付环比", "width": 100 },
  { "key": "visitorCount", "label": "访客数", "width": 100 },
  { "key": "visitorChange", "label": "访客环比", "width": 100 }
]
```

### 完整数据示例

```json
{
  "title": "异常商品列表 — 请选择要诊断的商品",
  "columns": [
    { "key": "imageUrl", "label": "图片", "width": 80 },
    { "key": "title", "label": "商品标题" },
    { "key": "reason", "label": "异常原因", "width": 120 },
    { "key": "payAmount", "label": "支付金额", "width": 120 },
    { "key": "changeRate", "label": "支付环比", "width": 100 },
    { "key": "visitorCount", "label": "访客数", "width": 100 },
    { "key": "visitorChange", "label": "访客环比", "width": 100 }
  ],
  "rows": [
    {
      "id": "668758083302",
      "title": "KA舟/W56",
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN016jGswI25S34m9mS2I_!!1992997524-0-cib.jpg",
      "reason": "支付下跌",
      "payAmount": "¥23,943.19",
      "changeRate": "-19.4%",
      "visitorCount": "-",
      "visitorChange": "-"
    },
    {
      "id": "779218424674",
      "title": "书架置物架落地多层收纳架实木色办公室书桌旁架子客厅房间矮书柜",
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN01RRLDvW25S2wPiR5fT_!!1992997524-0-cib.jpg",
      "reason": "访客下跌",
      "payAmount": "¥17,271.00",
      "changeRate": "-9.7%",
      "visitorCount": "725",
      "visitorChange": "-30.7%"
    },
    {
      "id": "992839699931",
      "title": "实木床头柜免安装2025爆款家用卧室小型极窄简约现代收纳置物柜子",
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN0178vwzE25S36Rlaiq0_!!1992997524-0-cib.jpg",
      "reason": "访客下跌, 支付下跌",
      "payAmount": "¥10,118.00",
      "changeRate": "-20.7%",
      "visitorCount": "436",
      "visitorChange": "-27.9%"
    }
  ]
}
```

### 交互结果处理

用户选择商品后，从交互返回结果中提取每条选中行的 `id` 字段，即为 `itemId`，作为后续 `get_offer_data --offer_id <商品ID>` 的入参。

若用户选择了多条商品，则依次对每个 `offer_id` 执行 Step 2 和 Step 3。

---

## 2. input_offer_id (Input 组件)

### 组件类型

`type: input`

### 业务场景

当 `get_abnormal_offers` 返回的异常商品列表为空（`data.items` 为空数组或 `data.count` 为 0）时，说明当前店铺暂无异常商品。此时通过 Input 组件引导用户手动输入想要诊断的商品 ID。

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`
  - 说明: 问题列表，每项包含 `question`（提示文本）和 `options`（可选的快捷选项）
  - 必须字段: `question`

### 完整数据示例

```json
{
  "questions": [
    {
      "question": "当前店铺暂无异常商品 🎉 请输入您想要诊断的商品 ID：",
      "options": []
    }
  ]
}
```

### 交互结果处理

用户输入的文本即为商品 ID（`offer_id`），直接作为后续 `get_offer_data --offer_id <商品ID>` 的入参，进入 Step 2。

若用户输入了多个 ID（以逗号或空格分隔），则拆分后依次对每个 `offer_id` 执行 Step 2 和 Step 3。

---

## 3. select_action (Card 组件)

### 组件类型

`type: card` — 在 Step 3 输出诊断报告后，根据报告中"优化项"动态生成可执行的行动选项，让用户一键进入下一步优化技能（当前支持：商品主图优化、商品标题优化）。

### 触发条件

- 诊断报告 Markdown 输出完成后
- Agent 必须先完成报告生成，再触发此交互
- 禁止在报告输出前或中途触发

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`
  - 说明: 问题列表，每项包含 `question`（问题文本）和 `options`（选项数组，元素为字符串）
  - 端侧会自动追加"输入其他"选项

### 构造规则

1. **动态生成**：选项不固定，Agent 必须根据本次诊断报告中实际输出的"优化项"来决定展示哪些选项
2. **数量限制**：`options` 最少 1 个，最多 2 个（当前仅支持主图优化、标题优化两个行动）
3. **排序**：按优化项在报告中的优先级从高到低排列（违规 > 流量 > 转化 > 一般建议）
4. **选项文案格式**：`emoji + 行动名称（简短说明）`，简短说明来自诊断报告中对应优化项的内容
5. **兜底逻辑**：如果两个关键词都未命中，仍至少展示 1 个最相关的选项（默认优先 `✏️ 优化商品标题`），避免空交互
6. **携带商品 ID**：选项文案中应带上当前诊断的 `offer_id`，便于下游技能识别上下文
7. Agent 应根据优化项内容，匹配以下关键词来生成对应的行动选项：

| 优化项关键词                       | 选项 emoji + 名称   | 对应技能                      |
| ---------------------------------- | ------------------- | ----------------------------- |
| 主图、图片、白底图、视频、视觉素材 | 🖼️ 优化商品主图    | `1688-item-image-optimizer`   |
| 标题、关键词、SEO、搜索词、类目词  | ✏️ 优化商品标题    | `1688-item-title-optimizer`   |

### 完整数据示例

假设当前诊断 `offer_id = 1048050628164`，报告"优化项"为：

1. 补充白底主图（违反类目规范）
2. 标题缺少核心类目词"实木床头柜"，建议补充

则构造的交互数据为：

```json
{
  "questions": [
    {
      "question": "📋 以上是商品 1048050628164 的诊断报告。根据分析，建议您优先执行以下优化，请选择：",
      "options": [
        "🖼️ 优化商品 1048050628164 主图（补充白底主图，符合类目规范）",
        "✏️ 优化商品 1048050628164 标题（补充核心类目词\"实木床头柜\"）"
      ]
    }
  ]
}
```

### 用户选择后的处理

| 用户选择                | Agent 行为                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| 选项文案含 🖼️ / "主图" | 直接调用 `1688-item-image-optimizer` 技能，并把当前诊断的 `offer_id` 作为上下文传入，无需用户再次输入   |
| 选项文案含 ✏️ / "标题" | 直接调用 `1688-item-title-optimizer` 技能，并把当前诊断的 `offer_id` 作为上下文传入，无需用户再次输入   |
| 输入其他                | 等待用户输入自定义需求，Agent 根据内容判断应调用的技能                                                  |

> ⚠️ 用户选择后应**直接调用对应技能**，无需用户再次输入触发词。调用时应携带当前诊断的 `offer_id` 与对应优化项原文，帮助下游技能快速定位问题。
