# 交互组件详细规范

本文档定义了 1688-shop-health-check Skill 中所有交互组件的具体数据结构与映射规则。

## 1. select_analysis_direction (Card 组件)

### 组件类型
`type: card`

### 业务场景
在输出店铺健康总览（第一阶段）后，让用户通过卡片选择希望深入分析的方向，而非手动输入文字。用户可选择单个方向，端侧会自动追加"输入其他"选项。

### 数据槽位定义

- **`directions`**:
  - 类型: `Array<Object>`
  - 映射规则: 固定的 7 个分析方向选项，无需从外部 Tool 获取，直接硬编码
  - 必须字段:
    - `label`: 方向名称（字符串，≤ 10 字）
    - `description`: 方向说明（字符串，≤ 30 字）

### 方向与编号映射

用户选择后，需要将 `label` 映射回对应的分析方向编号：

| label | 对应编号 | 调用接口 |
|-------|---------|---------|
| 异常商品诊断 | 1 | `seller_import_abnormal_offer` |
| 流量趋势分析 | 2 | `get_traffic_trend` |
| 增长驱动与主力商品 | 3 | `seller_top_offer`（4 种榜单） |
| 活动效果分析 | 4 | `seller_activity_registered_info` |
| 客户地域分布 | 5 | `seller_customer_business_province` |
| 头部老客户分析 | 6 | `seller_customer_detail` |
| 完整诊断报告 | 7 | 全部接口 |

### 完整数据示例

```json
{
  "type": "card",
  "selectionType": "analysis_direction",
  "directions": [
    { "label": "异常商品诊断", "description": "识别拖累店铺的异常商品，定位流量/转化问题源" },
    { "label": "流量趋势分析", "description": "分析逐日流量波动，识别异常日期和流量质量变化" },
    { "label": "增长驱动与主力商品", "description": "识别成交/流量/拉新/复购四大维度的主力商品" },
    { "label": "活动效果分析", "description": "评估近 30 天活动效果，识别高效/低效活动" },
    { "label": "客户地域分布", "description": "分析客户地域集中度和拓展机会" },
    { "label": "头部老客户分析", "description": "分析高价值客户稳定性、活跃度和流失风险" },
    { "label": "完整诊断报告", "description": "全量分析，输出包含以上所有方向的完整报告" }
  ]
}
```

### 用户选择结果处理

- **用户选择了 1-6 中的某个方向**: 按对应编号执行聚焦型分析
- **用户选择了"完整诊断报告"**: 等同于选择编号 7，执行全量取数
- **用户通过"输入其他"自由输入**: 尝试匹配已有方向，若无法匹配则告知用户不支持该方向并自动执行完整诊断

---

## 2. select_abnormal_action (Card 组件)

### 组件类型

`type: card` — 异常商品诊断（用户选择方向 1 或方向 7 走到异常商品环节）的可视化 JSON 输出**完成之后**，把每个 TOP 异常商品 × 推荐操作合并成一张卡片，用户**单选**一项即直接调用对应优化技能。

### 触发条件

- 必须在 Step 3 异常商品定位的可视化 JSON 输出之后触发（不可在文字段中或可视化 JSON 之前触发）
- 仅当 `seller_import_abnormal_offer` 返回的异常商品数量 > 0 时触发；为 0 时改用 `input_offer_for_optimize`
- Agent 必须先完成异常商品诊断的全部输出（文字结论 + 可视化 JSON），再追加此交互

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`
  - 说明: 问题列表，每项包含 `question`（问题文本）和 `options`（选项数组）
  - 端侧会自动追加"输入其他"选项

### 选项构造规则

1. **逐商品生成**：对 Step 3 输出的每个 TOP 异常商品，根据其 `reason` 字段或行动重点关键词匹配下表生成选项
2. **关键词映射表**：

   | 异常商品 `reason` / 行动重点关键词 | 选项文案模板 | 对应技能 |
   |---|---|---|
   | 主图、图片、优化图、CTR、点击率、曝光转点击 | `🖼️ 优化商品 {offerId} 主图（{异常类型简述}）` | `1688-item-image-optimizer` |
   | 标题、关键词、SEO、搜索、词覆盖 | `✏️ 优化商品 {offerId} 标题（{异常类型简述}）` | `1688-item-title-optimizer` |

3. **默认兜底**：
   - `reason` = "访客下跌" 且未明确命中关键词 → 默认 `✏️ 优化标题`（拉搜索曝光）
   - `reason` = "支付下跌" 且未明确命中关键词 → 默认 `🖼️ 优化主图`（提点击转化）
   - `reason` = "访客下跌, 支付下跌"（双跌） → **两条选项都生成**
4. **数量限制**：最少 2 个，最多 6 个；超过时按异常严重度（`valueMap.payAmt.cycleCqc.value` 负向绝对值）截断
5. **排序规则**：按异常严重度从高到低排列；同一商品的多个选项相邻排列，🖼️ 优先于 ✏️
6. **文案中的「异常类型简述」**：从 `reason` 提炼，如"访客 -45%"、"支付 -2.3 万"，控制在 12 字内

### 完整数据示例

假设 Step 3 输出的 TOP 异常商品为：
1. offerId `912345678`，reason `访客下跌, 支付下跌`，访客 -52%、支付 -¥18,500
2. offerId `887766554`，reason `支付下跌`，支付 -¥9,200
3. offerId `776655443`，reason `访客下跌`，访客 -38%

则构造的交互数据为：

```json
{
  "questions": [
    {
      "question": "🛠️ 以上是异常商品诊断结果。建议针对以下商品立即开展优化，请选择一项执行：",
      "options": [
        "🖼️ 优化商品 912345678 主图（双跌·支付 -1.85万）",
        "✏️ 优化商品 912345678 标题（双跌·访客 -52%）",
        "🖼️ 优化商品 887766554 主图（支付 -9.2k）",
        "✏️ 优化商品 776655443 标题（访客 -38%）"
      ]
    }
  ]
}
```

### 用户选择后的处理

| 用户选择文案 | Agent 行为 |
|---|---|
| `🖼️ 优化商品 {offerId} 主图（…）` | 直接调用 `1688-item-image-optimizer`，携带 `offerId` 作为上下文 |
| `✏️ 优化商品 {offerId} 标题（…）` | 直接调用 `1688-item-title-optimizer`，携带 `offerId` 作为上下文 |
| 输入其他 | 等待用户输入自定义需求，Agent 根据内容判断应调用的技能 |

> ⚠️ 用户选择后应**直接调用对应技能**，无需用户再次输入触发词或重新提供 offerId。

---

## 3. input_offer_for_optimize (Card 组件)

### 组件类型

`type: card` — 异常商品诊断完成但**未识别到异常商品**时使用，通过标准 Card 组件的两步问答收集商家想要优化的商品 offerId 和优化方向，然后直接调用对应下游优化技能。

### 触发条件

- 用户走到异常商品诊断环节（方向 1 或方向 7）
- `seller_import_abnormal_offer` 返回的异常商品数量 == 0
- Agent 必须先用 1 句话说明"当前周期未识别到明显异常商品"再追加此卡片

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`，固定 2 题，端侧按顺序逐题展示
  - **第一题（offerId 收集）**：
    - `question`: 引导用户输入 offerId 的问题文本，支持 Markdown 渲染
    - `options`: `[]`（空数组，表示纯自由输入题）
    - `required`: `true`（必填，不可跳过）
  - **第二题（优化方向选择）**：
    - `question`: 引导用户选择优化方向的问题文本
    - `options`: `["🖼️ 优化主图", "✏️ 优化标题"]`（固定 2 项）
    - `allowMultiple`: `false`（单选）
    - `required`: `true`（必填，不可跳过）

### 完整数据示例

```json
{
  "type": "card",
  "selectionType": "requirement",
  "questions": [
    {
      "question": "**请输入要优化的商品 offerId**\n\n请填写纯数字的商品 ID，例如：`912345678`",
      "options": [],
      "required": true
    },
    {
      "question": "**请选择优化方向**",
      "options": ["🖼️ 优化主图", "✏️ 优化标题"],
      "allowMultiple": false,
      "required": true
    }
  ]
}
```

### 回传结构

```json
[
  { "question": "**请输入要优化的商品 offerId**...", "answer": "912345678" },
  { "question": "**请选择优化方向**", "answer": "🖼️ 优化主图" }
]
```

### 用户操作后的处理

| 用户回传 | Agent 行为 |
|---|---|
| 第一题回答了有效 offerId + 第二题选择 `🖼️ 优化主图` | 直接调用 `1688-item-image-optimizer`，携带用户输入的 `offerId` |
| 第一题回答了有效 offerId + 第二题选择 `✏️ 优化标题` | 直接调用 `1688-item-title-optimizer`，携带用户输入的 `offerId` |
| 第一题输入了非数字内容 | Agent 提示"offerId 须为纯数字，请重新输入"，不调用下游技能 |
| 用户通过"输入其他"自由输入 | 等待用户输入自定义需求，Agent 根据内容判断应调用的技能 |

> ⚠️ Agent 必须校验第一题回传的 offerId 为纯数字后再调用下游技能，不要自行编造 offerId。
