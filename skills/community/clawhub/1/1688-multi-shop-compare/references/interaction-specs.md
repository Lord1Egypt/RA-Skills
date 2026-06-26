# 交互组件详细规范

本文档定义了 1688-multi-shop-compare Skill 中所有交互组件的具体数据结构与映射规则。

**⚠️ 强约束**：所有交互组件均通过 `show_interaction` 渲染，**不通过 Markdown 代码块渲染**。禁止输出 ` ```action-card``` ` 代码块给用户。

---

## 1. select_shop_scope (Card 组件)

### 组件类型
`type: card`，`selectionType: shop_scope`

### 业务场景
当 `get_bindlist` 返回的绑定店铺数量 ≥ 4 时，在数据采集之前触发，让用户多选要分析的店铺并选择分析焦点。通过 `show_interaction` 渲染。

### 触发条件
- 店铺数量 ≥ 4 **且** 用户未在提问中明确表达"所有店铺""全部店铺""全量分析"等全量意图

### 数据槽位定义

- **`shop_options`**:
  - 类型: `Array<Object>`
  - 映射规则: 从 `get_bindlist` 返回的店铺列表动态生成
  - 必须字段:
    - `label`: 店铺公司名称（字符串）
    - `description`: 标注是否为当前登录店铺（字符串，可为空）
  - **默认全部勾选**，用户可取消不需要的店铺
  - **禁止包含 AK**

- **`focus_options`**:
  - 类型: `Array<Object>`
  - 映射规则: 固定的 4 个分析焦点选项
  - 必须字段:
    - `label`: 焦点名称（字符串）
    - `description`: 焦点说明（字符串）

### 焦点选项固定值

| label | description |
|-------|-------------|
| 全量对比 | 店铺层+类目层+商品层+客户地域，输出完整 4 层报告 |
| 聚焦经营概况 | 重点对比各店的经营角色、健康度和核心指标差异 |
| 聚焦商品诊断 | 重点对比各店的商品分层、异常商品和机会商品 |
| 聚焦客户地域 | 重点分析客户重叠、地域互补和协同机会 |

### 调用示例

```
show_interaction({
  type: "card",
  selectionType: "shop_scope",
  shop_options: [
    { label: "深圳市金嘉伟业电子有限公司", description: "当前登录店铺" },
    { label: "品规测试账号01", description: "" },
    { label: "武汉耀丹鸿商贸有限公司", description: "" },
    { label: "雷徐冬", description: "" }
  ],
  focus_options: [
    { label: "全量对比", description: "店铺层+类目层+商品层+客户地域，输出完整 4 层报告" },
    { label: "聚焦经营概况", description: "重点对比各店的经营角色、健康度和核心指标差异" },
    { label: "聚焦商品诊断", description: "重点对比各店的商品分层、异常商品和机会商品" },
    { label: "聚焦客户地域", description: "重点分析客户重叠、地域互补和协同机会" }
  ]
})
```

### 用户选择结果处理

| 用户选择（店铺） | 处理方式 |
|----------------|---------|
| 勾选了全部店铺 | 对所有店铺执行数据采集 |
| 勾选了部分店铺（≥ 2 个） | 仅对用户勾选的店铺执行数据采集 |
| 仅勾选了 1 个店铺 | 提示"至少需要 2 个店铺才能进行对比分析" |
| 未勾选任何店铺 | 默认全部分析，并告知用户 |

| 用户选择（焦点） | 处理方式 |
|----------------|---------|
| 全量对比 | 全量执行分析方法论 Step 1-8 |
| 聚焦经营概况 | 仅采集 `trade_index` + `core_metrics` + `traffic_trend` |
| 聚焦商品诊断 | 仅采集 `top_offer_*` + `abnormal_offer` |
| 聚焦客户地域 | 仅采集 `province` + `customer_detail` |

---

## 2. select_abnormal_action (Card 组件)

### 组件类型
`type: card`，`selectionType: requirement`

### 业务场景
报告输出后，当各店铺存在异常商品时（`abnormal_offer_count > 0`），通过 `show_interaction` 渲染行动选项卡片，让用户单选一项立即执行对应的下游优化技能。

### 触发条件
- 各店铺 `abnormal_offer` 合计数量 > 0
- §B 的 `seller-report` 代码块已完整闭合

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`，固定 1 个问题
  - 必须字段:
    - `question`: 问题文案（字符串），固定为"以上是多店对比分析结果。建议优先处理以下异常商品，请选择一项执行："
    - `options`: 选项数组（`Array<String>`），根据异常商品动态生成，2-6 个
    - `allowMultiple`: `false`
    - `required`: `true`

### 选项格式

每个选项格式为：`{动作}｜{店铺名}｜商品{offerId}｜{异常简述}`

- 动作为 `优化主图` 或 `优化标题`
- 异常简述从 `reason` + 变化值提炼，控制在 12 字内

### 选项生成规则

| `reason` 关键词 | 生成动作 | 下游技能 |
|----------------|---------|---------|
| 主图、图片、CTR、点击率 | 优化主图 | `1688-item-image-optimizer` |
| 标题、关键词、SEO、搜索 | 优化标题 | `1688-item-title-optimizer` |
| 访客下跌（未命中其他关键词） | 优化标题 | `1688-item-title-optimizer` |
| 支付下跌（未命中其他关键词） | 优化主图 | `1688-item-image-optimizer` |
| 访客下跌 + 支付下跌（双跌） | 同时生成两条 | 各一条 |

### 选项约束

1. 合计选项数 ≥ 2 且 ≤ 6
2. 超过时按异常严重度截断
3. 按异常严重度从高到低排序
4. 同一商品多个选项相邻排列（优化主图在前，优化标题在后）
5. 每个选项必须包含店铺名前缀
6. 商品 ID 必须来自接口返回，禁止编造

### 调用示例

```
show_interaction({
  type: "card",
  selectionType: "requirement",
  questions: [
    {
      question: "以上是多店对比分析结果。建议优先处理以下异常商品，请选择一项执行：",
      options: [
        "优化主图｜深圳市金嘉伟业电子有限公司｜商品912345678｜双跌·支付-1.85万",
        "优化标题｜深圳市金嘉伟业电子有限公司｜商品912345678｜双跌·访客-52%",
        "优化主图｜武汉耀丹鸿商贸有限公司｜商品887766554｜支付-9.2k",
        "优化标题｜武汉耀丹鸿商贸有限公司｜商品776655443｜访客-38%"
      ],
      allowMultiple: false,
      required: true
    }
  ]
})
```

### 用户选择结果处理

- **选择"优化主图"选项**：从选项中解析 offerId，调用 `1688-item-image-optimizer`
- **选择"优化标题"选项**：从选项中解析 offerId，调用 `1688-item-title-optimizer`
- **通过"输入其他"自由输入**：尝试匹配商品 ID 和操作意图，若无法匹配则提示重新选择

---

## 3. input_offer_for_optimize (Card 组件)

### 组件类型
`type: card`，`selectionType: requirement`

### 业务场景
报告输出后，当各店铺均未识别到异常商品时（`abnormal_offer_count == 0`），通过 `show_interaction` 渲染两步问答卡片，收集商家想要优化的商品 offerId 和优化方向，然后调用对应下游优化技能。

### 触发条件
- 各店铺 `abnormal_offer` 合计数量 == 0
- §B 的 `seller-report` 代码块已完整闭合

### 数据槽位定义

- **`questions`**:
  - 类型: `Array<Object>`，固定 2 个问题
  - 第 1 题（自由输入）:
    - `question`: `"请输入要优化的商品 offerId"`
    - `options`: `[]`
    - `required`: `true`
  - 第 2 题（单选）:
    - `question`: `"请选择优化方向"`
    - `options`: `["优化主图", "优化标题"]`
    - `allowMultiple`: `false`
    - `required`: `true`

### 调用示例

```
show_interaction({
  type: "card",
  selectionType: "requirement",
  questions: [
    {
      question: "请输入要优化的商品 offerId",
      options: [],
      required: true
    },
    {
      question: "请选择优化方向",
      options: ["优化主图", "优化标题"],
      allowMultiple: false,
      required: true
    }
  ]
})
```

### 用户选择结果处理

- **用户输入 offerId + 选择"优化主图"**：调用 `1688-item-image-optimizer`，携带 offerId
- **用户输入 offerId + 选择"优化标题"**：调用 `1688-item-title-optimizer`，携带 offerId
- **offerId 格式校验失败**：提示用户输入纯数字的商品 ID
