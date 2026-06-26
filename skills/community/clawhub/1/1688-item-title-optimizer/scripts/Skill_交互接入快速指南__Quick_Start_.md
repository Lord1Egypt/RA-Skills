# Skill 交互接入快速指南 (Quick Start)

本指南旨在帮助 Skill 开发者**快速接入** Newton Agent 的客户端交互能力。只需两步：**声明 Metadata** 和 **正文引导**。

---

## 1. 第一步：在 Metadata 中声明交互 (必选)

在 `SKILL.md` 的 YAML Frontmatter 中添加 `interactions` 列表。这是框架识别和大模型发现交互能力的**唯一入口**。

### 核心字段速查

| 字段 | 说明 | 示例值 |
| --- | --- | --- |
| `name` | **交互唯一 ID**，大模型调用时使用 | `select_products` |
| `type` | **组件类型**：`table` (表格), `card` (卡片), `input` (问答) | `table` |
| `selectionType` | **数据类型标识**，决定云端存哪里 | `product`, `merchant` |
| `description` | **业务语义**，告诉大模型何时用 | "从结果中选择商品" |
| `required_data` | **数据槽位**，简要描述需要的数据 | `{ products: "商品列表" }` |

### 快速复制模板

```yaml
---
metadata:
  interactions:
    - name: select_products_for_inquiry
      type: table
      selectionType: product
      description: "从搜索结果中选择要询盘的商品"
      required_data:
        products: "商品列表数组，每项包含 id, title, price"
---

```
---

## 2. 第二步：在正文中引导大模型 (可选但推荐)

在 `SKILL.md` 正文中，用自然语言告诉大模型**何时触发**、**如何填数**，以及**去哪里查规范**。

### 引导话术示例

> **触发时机**： 在执行 `text_search` 获得商品列表后，若用户表现出挑选意向，请调用 `show_interaction` 并设置 `name='select_products_for_inquiry'`。**数据填充**： 将 `text_search` 返回的 `items` 数组赋值给 `products` 槽位。**具体的字段映射规则与组件渲染数据结构请查阅** [`**references/interaction-specs.md**`](./references/interaction-specs.md) **中对应交互的章节。**

#### 📌 完整引导案例（推荐直接复制）

以下是一个完整的 Skill 正文引导示例，展示了如何严格遵循"先查 specs、再构造参数"的流程：

⚠️ **交互渲染（必须执行）**：当此命令返回的 `data.data.products` 包含 ≥2 个商品时，禁止直接用 Markdown 表格输出商品数据，必须通过交互组件渲染：

1.  **先读取** `{baseDir}/references/interaction-specs.md` 中的 `select_products_from_scoring` 章节，获取交互组件的完整数据结构定义
    
2.  **再触发** metadata.interactions 中声明的 `select_products_from_scoring` 交互，严格按 specs 中的字段映射构造参数
    
3.  **调用示例**：
    

### ⚠️ 关键约定

---

## 3. 三种组件的快速参考

根据你的业务场景，选择对应的 `type`：

### A. Table (表格选择) - 适合结构化数据多选

*   **场景**：商品列表、订单筛选。
    
*   **Metadata 示例**：
    

### B. Card (选项卡片) - 适合快速偏好选择

*   **场景**：风格选择、平台确认。端侧会自动追加“输入其他”。
    
*   **Metadata 示例**：
    

### C. Input (澄清问答) - 适合细节确认与自由输入

*   **场景**：预算确认、备注填写。
    
*   **Metadata 示例**：
    
    ### D 打开 Tab 标签页 - 适合页面跳转与外部资源展示
    
    输出 type='open\_tab' 时，客户端立即在工作区右侧新开一个 webview Tab，加载指定 URL 并渲染指定页面名称；工具不等用户操作即返回（fire-and-forget），聊天区同步出现一张"已为你打开 xxx"的只读气泡卡片
    
    ---
    
    ## 3.5 真实交互 Case 速查
    
    以下是三种组件在实际场景中的**完整可拷贝示例**，可直接作为 `show_interaction` 的入参参考。
    
    ### 通用字段速查（所有 case 通用）
    
    | 字段 | 适用类型 | 说明 |
    | --- | --- | --- |
    | `type` | 必填 | `card` / `table` / `input` |
    | `selectionType` | 可选 | 数据类型标识（`product` / `merchant` / `style` / `requirement` 等），影响 UI 标签和云端分类 |
    
    #### card / input 专属（`questions[ ]` 内字段）
    
    | 字段 | 类型 | 默认 | 说明 |
    | --- | --- | --- | --- |
    | `question` | string | — | 问题文本，**支持 Markdown 渲染**（加粗、链接、列表、行内代码、`\n` 换行） |
    
    | `options`
    
*   [ ] | — | 候选选项，2~6 个；不传或传 
    

`[ ]` 表示纯自由输入题 |

| `allowMultiple` | boolean | `false` | 是否多选；多选题端侧自动出现「全选 / 取消全选」按钮（选项 ≥2 时） | | `required` | boolean | `false` | 是否必填；**默认可跳过**，端侧会显示「跳过此题」按钮，跳过的题回传 `{ answer: null, skipped: true }` |

#### table 专属

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `title` | string | 表格标题，**支持 Markdown 渲染** |

| `columns[ ].editable` | boolean | 该列是否可在表格中直接编辑 |

| `columns[ ].width` | number | 列宽（像素），不传自适应 |

| `totalCount` | number | 总数据量提示（与 `rows.length` 可不一致，用于分页场景） | | `actions` | array | **自定义按钮**，配置后追加在「确认选择」右侧；点击后会把选中行 + 该按钮的 `description` 一起回传给大模型；不配置时仅展示「跳过」+「确认选择」 |

#### open\_tab 组件

### 数据字段定义

*   `**url**` (必填)
    
    *   类型: `string`
        
    *   约束: 必须以 `http://\` 或 `https://\` 开头
        
    *   映射规则: 从 `shop_query_tool` 的 `backend_url` 字段取值，拼接业务 query 参数
        
*   `**pageTitle**` (必填)
    
    *   类型: `string`
        
    *   建议长度: ≤ 20 字符（超出会在 Tab 上被 `...` 截断）
        
    *   映射规则: `${platformName} ${pageSubject}`，如 `"Ozon 订单管理"`
        
*   `**pageDescription**` (可选)
    
    *   类型: `string`
        
    *   长度: ≤ 80 字符
        
    *   用途: 在气泡卡片第二行展示，告诉用户页面做了哪些
        
*   `**iconUrl**` (可选)
    
    *   类型: `string`（http/https URL）
        
    *   用途: 卡片左侧的 18×18 方形图标；不传则显示默认 🌐
        

### 完整数据示例

```json
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://seller.ozon.ru/app/orders",
  "pageTitle": "Ozon 店铺订单",
  "pageDescription": "查看今日待发货订单"
}

```
> **端侧默认能力**（无需在参数里声明，自动可用）：

---

### Case 1：Input 多步澄清（含必填、可跳过、Markdown 渲染、纯自由输入混合）

典型场景：在启动一个新需求前，连续向用户确认项目类型、模块、规模、上线时间等多维度信息。`questions` 是有序数组，端侧会按顺序逐题展示。

**本 case 演示**：

*   通过 `required: true` 把「项目类型」「团队规模」标为必填，其余题可跳过
    
*   通过 `allowMultiple: true` + `required: false` 让多选题既能多选也能跳过
    
*   通过 Markdown 在 question 文本里加 `**加粗**`、`\n` 换行、行内代码 ``code`` 来增强可读性
    
*   通过 `options: [ ]` 表示纯自由输入题
    

**回传结构**（同时演示已答 + 跳过的回传形态）：

```json
[
  { "question": "...", "answer": "电商系统" },
  { "question": "...", "answer": ["用户管理", "订单系统"] },
  { "question": "...", "answer": null, "skipped": true }
]

```

**调用入参**：

```json
{
    "type": "input",
    "selectionType": "project_info",
    "questions": [
        {
            "question": "**第一步**：您的项目类型是？\n\n> 不同类型对应不同的技术栈推荐。",
            "options": ["电商系统", "社交平台", "企业管理系统", "其他"],
            "allowMultiple": false,
            "required": true
        },
        {
            "question": "**第二步**：您需要哪些功能模块？（可多选，可跳过）",
            "options": ["用户管理", "订单系统", "支付集成", "数据分析", "消息通知", "文件存储"],
            "allowMultiple": true,
            "required": false
        },
        {
            "question": "**第三步**：您的团队规模是？",
            "options": ["1-5人", "6-20人", "21-50人", "50人以上"],
            "required": true
        },
        {
            "question": "**第四步**：预期的上线时间？\n\n（如不确定可跳过此题，我们后续再讨论）",
            "options": ["1个月内", "3个月内", "半年内", "1年内"],
            "allowMultiple": false,
            "required": false
        },
        {
            "question": "**第五步**：您关注哪些非功能性指标？（可多选）",
            "options": ["性能", "安全", "可扩展性", "可维护性", "合规性"],
            "allowMultiple": true,
            "required": false
        },
        {
            "question": "**第六步**：目标用户群体？",
            "options": ["个人消费者", "中小企业", "大型企业", "政府机构"],
            "required": false
        },
        {
            "question": "**第七步**：是否有其他特殊需求？请用一句话描述。\n\n例如：`需要对接钉钉` / `必须支持私有化部署`",

            "options": [ ],

            "required": false
        }
    ]
}

```
---

### Case 2：Card 选项卡片（风格偏好收集，全部可跳过 + 多选全选）

典型场景：在生图 / 生文等创意类任务前，快速收集用户的风格偏好。所有题目均设为可跳过，让用户对没强偏好的维度直接放过；多选题端侧会自动出现「全选」按钮。

**本 case 演示**：

*   全部题目 `required` 省略（即默认 false，可跳过）
    
*   多选题（颜色偏好、风格关键词）端侧自动出现「全选 / 取消全选」按钮
    
*   Markdown 在 question 中说明每个维度的语义
    

**调用入参**：

```json
{
    "type": "card",
    "selectionType": "style",
    "questions": [
        {
            "question": "**整体风格**：你希望作品偏向哪种基调？",
            "options": ["简约", "复古", "科技感", "国潮", "暗黑"],
            "allowMultiple": false
        },
        {
            "question": "**主色调**：可选多个，端侧会出现「全选」按钮，方便你一键选齐。",
            "options": ["黑白灰", "暖色系", "冷色系", "莫兰迪", "高饱和", "霓虹"],
            "allowMultiple": true
        },
        {
            "question": "**风格关键词**（可多选，可跳过）",
            "options": ["极简", "繁复", "写实", "插画", "抽象", "故事感"],
            "allowMultiple": true
        },
        {
            "question": "**目标受众**：作品主要给谁看？",
            "options": ["Z世代", "都市白领", "亲子家庭", "高净值人群", "通用"],
            "allowMultiple": false
        }
    ]
}

```
---

### Case 3：Table 表格选择（含可编辑列 + Markdown 标题）

典型场景：商品列表批量选择，部分列允许用户在表格内直接修改（如名称、价格、类目）。

**本 case 演示**：

*   `columns[ ].editable: true` 让指定列可编辑
    
*   `title` 使用 Markdown 加粗 + 行内代码强调操作要点
    
*   端侧表头自动出现「全选 / 取消全选」按钮（行数 ≥2 时）
    

**调用入参**：

```json
{
    "type": "table",
    "selectionType": "product",
    "title": "请选择并修改商品信息 — **可直接在表格内编辑** `名称 / 价格 / 类目`",
    "columns": [
        { "key": "id", "label": "商品ID", "width": 100 },
        { "key": "name", "label": "商品名称", "width": 200, "editable": true },
        { "key": "price", "label": "价格(元)", "width": 120, "editable": true },
        { "key": "stock", "label": "库存", "width": 80 },
        { "key": "category", "label": "类目", "width": 120, "editable": true },
        { "key": "status", "label": "状态", "width": 100 }
    ],
    "rows": [
        { "id": "1001", "name": "无线蓝牙耳机 Pro", "price": "299", "stock": 156, "category": "电子产品", "status": "在售" },
        { "id": "1002", "name": "机械键盘 RGB版", "price": "599", "stock": 42, "category": "电脑配件", "status": "在售" },
        { "id": "1003", "name": "人体工学椅", "price": "1299", "stock": 8, "category": "办公家具", "status": "库存紧张" },
        { "id": "1004", "name": "4K显示器 27寸", "price": "2499", "stock": 23, "category": "电脑配件", "status": "在售" },
        { "id": "1005", "name": "智能手表", "price": "899", "stock": 67, "category": "穿戴设备", "status": "新品" }
    ],
    "totalCount": 5
}

```
---

### Case 4：Table + 自定义 Actions（落库 / 下单 / 重新搜索）

典型场景：选完商品后，用户可以选择不同的「下一步动作」。每个按钮都会把选中行 + 自己的 `description` 一起回传给大模型，让大模型在确认数据的同时直接得到「该做什么」的指令。

**本 case 演示**：

*   `actions` 数组配置 3 个自定义按钮，覆盖 `primary` / `default` / `destructive` 三种 variant
    
*   每个按钮的 `description` 是给大模型的"附加任务指令"，**不会展示给用户**（用户看到的只是 `label`）
    
*   「跳过」+「确认选择」按钮始终保留（端侧默认行为，无需声明）
    

**回传结构**：

用户点了自定义按钮（以「落库」为例）时：

```json
{
  "selectionType": "product",
  "data": {
    "selectedRows": [ { "id": "1001", "name": "...", ... } ],
    "action": {
      "key": "store_to_db",
      "label": "落库",
      "description": "把选中的商品数据直接写入到 ods_product_pool 表，跳过人工确认环节"
    }
  }
}

```

用户点了默认「确认选择」时（兼容老逻辑）：

```json
{
  "selectionType": "product",
  "data": { "selectedRows": [ ... ], "action": "confirm" }
}

```

用户点了「跳过」时：

```json
{
  "selectionType": "product",

  "data": { "selectedRows": [ ], "action": "skip" }

}

```

**调用入参**：

```json
{
    "type": "table",
    "selectionType": "product",
    "title": "请选择目标商品，并通过下方按钮告诉我要执行哪一种后续操作",
    "columns": [
        { "key": "id", "label": "商品ID", "width": 100 },
        { "key": "name", "label": "商品名称", "width": 220 },
        { "key": "price", "label": "价格", "width": 100 },
        { "key": "stock", "label": "库存", "width": 80 }
    ],
    "rows": [
        { "id": "1001", "name": "无线蓝牙耳机 Pro", "price": "¥299", "stock": 156 },
        { "id": "1002", "name": "机械键盘 RGB版",   "price": "¥599", "stock": 42  },
        { "id": "1003", "name": "人体工学椅",       "price": "¥1299","stock": 8   }
    ],
    "totalCount": 3,
    "actions": [
        {
            "key": "store_to_db",
            "label": "落库",
            "description": "把选中的商品数据直接写入到 ods_product_pool 表，跳过人工确认环节",
            "variant": "primary"
        },
        {
            "key": "create_order",
            "label": "立即下单",
            "description": "对选中的商品创建采购订单，使用默认收货地址，订单状态置为待支付",
            "variant": "primary"
        },
        {
            "key": "research_again",
            "label": "重新搜索",
            "description": "用户对当前结果不满意，请放大搜索范围（去掉品牌限定、扩大价格区间到 ±50%）后重新调用 text_search",
            "variant": "default"
        },
        {
            "key": "blacklist",
            "label": "加入黑名单",
            "description": "把选中的商品 ID 加入用户黑名单，后续搜索结果中永不出现",
            "variant": "destructive"
        }
    ]
}

```
> `**variant**` **视觉效果速查**：

---

### Case 5：open\_tab 打开店铺后台

```markdown
典型场景：用户问"我店铺今天有多少待发货订单"，大模型判断需要跳转到后台页面时，直接打开对应页面，并继续往下回答或
执行下一步（fire-and-forget 的关键优势）。
{
  "type": "open_tab",
  "selectionType": "shop_backend",
  "url": "https://work.1688.com/home/page/index.htm",
  "pageTitle": "Ozon 店铺订单",
  "pageDescription": "查看今日待发货订单"
}
```

## 4. 

## 关键注意事项 (避坑指南)

1.  `**selectionType**` **必须准**：填 `product` 还是 `merchant` 直接决定数据存入哪张表，请勿随意填写。
    
2.  **Table 不能为空**：调用 `table` 类型交互前，务必确保 `rows` 有真实数据，否则前端会报错。
    
3.  **细节下沉**：Metadata 中只写**槽位名**和**简要描述**。复杂的 JSON 结构、Props 定义和数据映射规则应写入 `references/interaction-specs.md`，实现声明与实现的解耦。
    

**推荐目录结构**：

```text
my-skill/
├── SKILL.md                      # 轻量级声明与业务逻辑
└── references/
    └── interaction-specs.md      # 详细的组件 Props 与数据格式定义

```
---

## 5. `references/interaction-specs.md` 编写规范

该文档是 Skill 内部的**交互详细说明书**，供大模型在调用 `show_interaction` 前查阅，确保数据结构正确。

### 编写原则

1.  **一个交互一节**：每个在 Metadata 中声明的 `interactions` 条目，对应文档中的一个章节，标题与 `name` 一致。
    
2.  **聚焦数据结构**：只写**渲染数据结构**和**字段映射规则**，不要重复 Metadata 中已有的业务描述。
    
3.  **给出真实示例**：提供一段可直接拷贝的 JSON 示例，便于大模型对照填充。
    

### 标准模板

```markdown
# 交互组件详细规范

本文档定义了本 Skill 中所有交互组件的具体数据结构与映射规则。

## 1. <交互 name> (<组件类型> 组件)

### 组件类型
`type: table` | `card` | `input`

### 数据槽位定义
- **`<槽位名>`**:
  - 类型: `Array<Object>` / `String` / ...
  - 映射规则: 描述该槽位的数据从哪个 Tool 的哪个字段转换而来。
  - 必须字段: 列出对象内必须包含的 key。

### 框架自动填充的字段（如有）
说明框架会根据 `selectionType` 自动注入哪些默认值（如 Table 的 `columns`），Skill 无需手动指定。

```json
[
  { "key": "imageUrl", "label": "图片", "width": 80 },
  { "key": "title", "label": "商品标题" },
  { "key": "price", "label": "价格" }
]

```

### 完整数据示例

```json
{
  "products": [
    { "id": "p1", "title": "示例商品", "price": 99, "imageUrl": "https://..." }
  ]
}

```
```plaintext

### 编写要点速查

| 章节 | 必须包含 | 说明 |
| :--- | :--- | :--- |
| 组件类型 | ✅ | 与 Metadata 的 `type` 保持一致 |
| 数据槽位定义 | ✅ | 每个 `required_data` 槽位都要展开 |
| 映射规则 | ✅ | 明确指出数据来源的 Tool 与字段路径 |
| 框架自动填充 | ⭕ | 仅 `selectionType` 有内置模板时需要写 |
| 完整数据示例 | ✅ | 一段可直接拷贝的 JSON |

---


*更多详细技术实现请参考：[SIMPLE_INTERACTION_PROTOCOL.md](./SIMPLE_INTERACTION_PROTOCOL.md)*


```