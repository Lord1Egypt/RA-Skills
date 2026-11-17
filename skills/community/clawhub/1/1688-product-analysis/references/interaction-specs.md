# 交互组件详细规范

本文档定义了 1688-product-analysis Skill 中所有交互组件的具体数据结构与映射规则。

## 1. select_abnormal_offer (Table 组件)

### 组件类型

`type: table`

### 业务场景

在执行 `get_abnormal_offers` 获取异常商品列表后，当用户**未明确指定诊断数量**时，以表格形式展示给用户，支持多选要诊断的商品。用户明确说“分析 3 个商品”“体检前五件”等数量时，直接按优先级取 Top-N 进入诊断，**不触发本表格**。

### 数据槽位定义

- **`title`**:
  - 类型: `String`
  - 固定值: `"异常商品列表 — 请选择要诊断的商品"`

- **`columns`**:
  - 类型: `Array<Object>`
  - 说明: 表格列定义，每列包含 `key`（字段名）、`label`（列标题）、`width`（可选，列宽 px）

- **`rows`**:
  - 类型: `Array<Object>`
  - 映射规则: 从 `multi_shop_product_analysis` 返回的各店铺 `items` 汇总后逐条转换；多店汇总最多 20 条（硬封顶，由 `--max_total_rows` 控制），按支付环比跌幅绝对值从大到小排序；单店无截断（原样返回 API 全量数据）；每行字段：id, imageUrl, title, shop_name, reason, payAmount, changeRate, visitorCount, visitorChange, loginId（title 截断 30 个字符（Python `len()` 计数）；共 8 列定义，id 和 loginId 不占显式列但为行必选字段）
  - 必须字段: `id`, `imageUrl`, `title`, `shop_name`, `reason`, `payAmount`, `changeRate`, `visitorCount`, `visitorChange`, `loginId`

### 字段映射规则

从 `get_abnormal_offers` 返回的每条 item 转换为 table row：

| row 字段 | 来源字段 | 转换规则 |
|----------|----------|----------|
| `id` | `item.itemId` | 直接赋值（字符串） |
| `title` | `item.offerTitle` | 直接赋值 |
| `imageUrl` | `item.offerImageUrl` | 直接赋值（CLI 已返回完整 URL，无需拼接前缀） |
| `shop_name` | `item.shop_name` | 直接赋值（归属店铺名称，来自 `multi_shop_product_analysis` 汇总时注入） |
| `reason` | `item.reason` | 直接赋值（如 "支付下跌"、"访客下跌"） |
| `payAmount` | `item.valueMap.payAmt.value` | 格式化为金额字符串 `¥xx,xxx.xx` |
| `changeRate` | `item.valueMap.payAmt.cycleCrc` | 格式化为百分比 `xx.x%`，负值加红色标记 |
| `visitorCount` | `item.valueMap.uv.value` | 若存在则取值，否则为 `"-"` |
| `visitorChange` | `item.valueMap.uv.cycleCrc` | 若存在则格式化为百分比，否则为 `"-"` |
| `loginId` | `item.loginId` | 直接赋值（店铺 loginId，隐藏字段，不在列定义中显示，仅保留组件兼容与候选来源；核心诊断不透传，最终以聚合 Tool 返回值为准） |

### 发现来源列（Step0 双入口场景）

当 Step 0 的"异常商品汇总"入口与"评分分层"第二入口（见 SKILL.md Step 0.5）**都有结果**时，需要把两份候选合并成一张表格，此时：

- `columns` 在原有 8 列基础上追加一列：`{ "key": "discoverySource", "label": "发现来源", "width": 110 }`
- 每行追加 `discoverySource` 字段：来自异常商品汇总的行填 `"异常下跌"`；来自评分分层 `c_grade_candidates` 的行填 `"评分分层-C级"`
- 若只有一个入口有结果，**不追加**该列和字段，保持原有 8 列结构不变（向后兼容）
- **两个来源各自独立封顶，不做二次压缩**：异常下跌沿用 `multi_shop_product_analysis` 自身的 20 条硬封顶（`max_total_rows`），评分分层沿用 `score_and_select` 的 `c_grade_candidates` 20 条硬封顶（`C_GRADE_CANDIDATES_LIMIT`）；合并后表格最多 40 行（20+20），不额外裁剪。两个来源各自内部排序规则不变（异常下跌按支付环比跌幅绝对值降序；评分分层按综合得分升序，最差优先）

### 列定义

```json
[
  { "key": "imageUrl", "label": "图片", "width": 80 },
  { "key": "title", "label": "商品标题" },
  { "key": "shop_name", "label": "店铺", "width": 100 },
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
    { "key": "shop_name", "label": "店铺", "width": 100 },
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
      "shop_name": "XX贸易有限公司",
      "reason": "支付下跌",
      "payAmount": "¥23,943.19",
      "changeRate": "-19.4%",
      "visitorCount": "-",
      "visitorChange": "-",
      "loginId": "tb123456"
    },
    {
      "id": "779218424674",
      "title": "书架置物架落地多层收纳架实木色办公室书桌旁架子客厅房间矮书柜",
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN01RRLDvW25S2wPiR5fT_!!1992997524-0-cib.jpg",
      "shop_name": "XX贸易有限公司",
      "reason": "访客下跌",
      "payAmount": "¥17,271.00",
      "changeRate": "-9.7%",
      "visitorCount": "725",
      "visitorChange": "-30.7%",
      "loginId": "tb123456"
    },
    {
      "id": "992839699931",
      "title": "实木床头柜免安装2025爆款家用卧室小型极窄简约现代收纳置物柜子",
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN0178vwzE25S36Rlaiq0_!!1992997524-0-cib.jpg",
      "shop_name": "YY科技有限公司",
      "reason": "访客下跌, 支付下跌",
      "payAmount": "¥10,118.00",
      "changeRate": "-20.7%",
      "visitorCount": "436",
      "visitorChange": "-27.9%",
      "loginId": "tb789012"
    }
  ]
}
```

### 交互结果处理

用户选择商品后，从交互返回结果中只提取每条选中行的 `id` 字段作为 `itemId`，传给 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>`。禁止把行内隐藏 `loginId` 或运行时 `userId` 作为该 Tool 的入参。

若用户选择了多条商品，则对每个 `itemId` 各调用一次聚合 Tool 并执行后续诊断；完整任务继续使用最大并发 5 的滑动队列。

若用户明确指定数量，异常候选先按违规/下架/处罚等高风险优先，再按支付环比下跌幅度降序，同幅度按支付金额降序；直接取 Top-N。候选行的隐藏 `loginId` 不作为诊断身份，聚合 Tool 内部（seller-agent 服务端）按 `itemId` 精确定位归属店并校验绑定权限，返回权威 `itemId -> loginId` 映射。完整诊断每批最多并行 5 件，超过 5 件时按排序自动进入后续批次；候选不足 N 件时分析全部候选。

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

从用户输入中提取 10 位及以上的商品 ID，只把每个 `itemId` 传给 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>`，进入 Step 2；调用方不传 `loginId` 或 `userId`。

若用户输入了多个 ID（以逗号或空格分隔），则拆分、去重并校验归属；每批最多并行校验和诊断 5 个，超过 5 个时按输入顺序自动排队，不得截断。商品未找到时提示并跳过；服务暂不可用时必须如实提示，不得说成商品不存在。

---

## 3. 报告末尾后续操作（非阻塞文本 + 精确交接）

### 业务场景

`delivery=component` 的 interactive 诊断由组件交付基础诊断，行动点和定时任务入口由 `footer_actions` 承载，主对话只输出同款比较；不得在主对话重复行动点或定时任务提示。只有 `delivery=markdown` 的报告才在 `merchant_report` 末尾用普通文本按商品汇总可执行行动，并在 interactive 确认未配置相关自动体检任务时追加设置定时任务提示。automatic 是唯一免选择卡、免诊断组件和免隐藏区块的特例：按现有优先级排序，按 offerId 去重后最多诊断 5 个商品；0 个候选正常结束，1–4 个全部诊断，5 个以上只取前 5 个，不展示候选表、不要求输入商品 ID 或关键词。automatic 固定直接输出完整 Markdown 报告，跳过定时任务查询和入口；可执行建议仍可作为文字报告的一部分，但不得自动修改商品。若自动诊断的 Top 5 有部分商品未完成，报告末尾追加“未完成商品”，只列商品 ID 和商家可理解的安全原因，不能静默少件。商品体检当前轮不再展示阻塞式确认卡，也不调用完成 notice；输出报告后立即结束当前回复。

工作流过程区先用一条商家语言说明本 Skill 支持经营表现诊断、同款对比和商品库建议。实时状态由 workflow phase 展示为“确定体检商品 → 查看经营表现 → 对比优秀同款 → 整理诊断报告 → 准备后续操作”。多商品必须把每件商品的经营数据、同款和商品库查询、报告生成作为一个完整任务；内部每批最多 5 个任务并行，超过 5 个时后续任务自动排队。开始时对商家统一说明“共 {N} 件商品，将开始商品体检，完成后会逐件更新结果”，不得展示并发数、批次或排队等内部调度细节。每件商品只在完整任务结束时显示“已完成/暂未完成 x/N 件商品诊断”，并带具体商品 ID；不展示经营数据读取、同款查询或报告生成等逐商品中间状态。最终报告仍按用户选择顺序展示。诊断结束后对应追加“商品经营表现检查完成”“同款对比和商品库建议核对完成”“已生成 {N} 件商品的完整诊断报告”。由于普通过程消息会永久保留，只允许输出能力范围、开始记录或完成状态，禁止保留“正在……”类过期状态。

自动选择 Top-N 和候选表展示必须使用同一确定性排序与同一份记录：异常候选按高风险、支付跌幅绝对值、支付金额排序，C级候选按综合得分升序；商品 ID、选择原因和排序指标随记录进入诊断。详情标题与候选标题冲突时，以详情标题为准并显示数据一致性提示；详情内部标题、类目、描述和属性明显冲突时，只分析不受影响的经营指标，不直接判为类目错放。

### 报告末尾格式

```markdown
### 后续操作

以下商品可以执行一键优化：
- 电动牙刷充电底座（ID：997433848144）：设置包邮、标题优化
- 无线蓝牙耳机（ID：888222333444）：主图优化

需要继续时，回复“进入一键优化”。一键优化会再逐项确认执行或跳过。

⏰需要我自动帮你找出需要优化的商品嘛？点击设置定时任务

需要配置时，回复“设置定时任务”。
```

“进入一键优化”和“设置定时任务”必须按上面示例输出为普通文本，禁止添加 `**`、`__`、反引号或其他 Markdown 包裹。

本格式只适用于 `delivery=markdown`：没有可执行行动时，省略一键优化段落；只有 interactive 确认未配置相关自动体检任务时才保留定时任务段落；automatic 不保留定时任务段落。若两者都没有，报告末尾不追加“后续操作”。`delivery=component` 的相同行动点和定时任务入口只由 `footer_actions` 承载，主对话不追加“后续操作”。

导出版（`商品体检报告.md` 文件与报告缓存）的“后续操作”只保留按商品列出的可执行行动清单；“需要继续时，回复……”“⏰需要我自动帮你……”等对话交互引导只出现在对话报告（`merchant_report`）里，不写入导出文件。

### 一键优化精确交接结构

```json
{
  "source": "1688-product-analysis",
  "tasks": [
    {
      "itemId": "997433848144",
      "title": "电动牙刷充电底座",
      "loginId": "shop_login_id",
      "opKey": "free_shipping",
      "actionLabel": "设置包邮"
    },
    {
      "itemId": "997433848144",
      "title": "电动牙刷充电底座",
      "loginId": "shop_login_id",
      "opKey": "title_opt",
      "actionLabel": "标题优化"
    },
    {
      "itemId": "888222333444",
      "title": "无线蓝牙耳机",
      "loginId": "other_shop_login_id",
      "opKey": "main_img_opt",
      "actionLabel": "主图优化"
    }
  ]
}
```

### 构造与处理规则

1. 合并原商品诊断标题/主图行动、商品库原始 `actions` 和具有明确 V2 证据的对标行动；相同 `(itemId, opKey)` 只保留一条
2. 仅允许 one-click `OP_REGISTRY` 已知的行动点；价格、定价、调价、涨价或降价不得进入 `tasks`
3. 每条 task 精确表达一个商品对应一个行动点，禁止把商品集合和行动点集合重新做笛卡尔积
4. 仅 interactive 的 workflow 调用 `check_auto_diagnosis_schedule` 只读当前 workspace 定时任务；只有 `enabled=true` 且名称包含“1688商品自动体检”或“1688商品体检”，或者描述同时包含“1688商品体检”和“自动找出需要优化的商品 / 找出待优化商品 / 商品诊断报告”任一业务描述时才视为已配置，`enabled=false` 不算已配置。automatic 必须跳过该查询
5. interactive 已配置相关任务或查询失败时，workflow 不追加定时任务提示；只有确认无相关任务时才追加。automatic 不展示设置定时任务入口。Agent 禁止调用 `Schedule(action="list")`、重新判断或追加独立入口
6. `delivery=markdown` 时当前回复只能输出完整 `merchant_report`，不得调用 notice、card、其他 workflow 或 skill；输出报告后立即结束当前回复。`delivery=component` 时基础诊断、行动点和定时任务入口由组件及 `footer_actions` 承载，主对话仅输出 `same_offer_markdown`，同样立即结束当前回复
7. 用户下一条消息明确回复“进入一键优化”且 `tasks` 非空时，只调用一次 `1688-item-one-click` workflow；把整个 JSON 序列化后的完整字符串直接作为 workflow args，禁止包装成 `query`/`params`
8. 商品体检当前轮不逐项选择行动；一键优化必须用自己的 `one_click_task_list` 对所有 task 逐项确认“执行/跳过”
9. interactive 的 `footer_actions.SCHEDULE_TASK.prompt` 固定返回“请帮我设置‘1688商品自动体检’定时任务，任务执行内容固定为：‘自动按优先级挑出【最该优化的 5 个商品】，完成诊断后直接在对话中输出完整报告和每个商品的优化建议’。请先询问执行频率和时间，再打开定时任务设置让我确认；不要自动修改商品。”，前端原样回填
10. 用户下一条消息明确表达设置商品自动体检定时任务的意图（包括手动回复“设置定时任务”或组件按钮完整 prompt 回填）后，进入 Newton 原生定时任务设置流程；实际任务 prompt 默认且完整使用“自动按优先级挑出【最该优化的 5 个商品】，完成诊断后直接在对话中输出完整报告和每个商品的优化建议”，仅自动运行商品体检并生成报告和行动点，禁止自动修改商品
11. workflow 只根据原始 query 判断执行意图，不宣称识别真实调度来源。明确要求先选择、先询问或确认后执行时固定为 interactive 且不调用模式模型；出现自动挑选/分析、无需反问或直接继续等无人值守候选语义时调用结构化模型节点，模型返回 `automatic=true` 时进入 automatic，“直接”不是必需词，“开始执行”等附加文字不影响判断。若 query 已同时明确表达自动执行、完成诊断、在对话交付完整报告和逐商品优化建议，则即使模型返回 false、输出异常或调用失败也兜底为 automatic；其他情况保守回到 interactive。automatic 的执行清单必须记录 `selectedCount`、`completed`、`failed` 和逐商品 `products` 状态

---

## 4. select_products_from_scoring (Table 组件)

### 组件类型

`type: table` — 用于展示评分分层结果，供两种场景复用：
1. **Step 0.5 第二发现入口**：展示 `score_and_select` 返回的 `c_grade_candidates`（C 级候选），供用户选择要深度诊断的商品。此场景下候选商品并入诊断链路，**无论候选数量多少（含只有1个）都触发本交互**，与 `select_abnormal_offer` 现有行为一致（不做"≥2才触发"的例外），确保用户在进入耗时的深度诊断前都能先确认商品
2. **独立使用场景**（用户明确要"选品/圈选重点品"但不接诊断）：从 `products` 中仅保留 S/A/B 级商品后展示。**沿用 item-select 原有规则：候选 ≥2 个才触发本交互；只有 1 个时直接输出 Markdown 报告，不触发交互**

### 数据槽位定义

- **`title`**:
  - 类型: `String`
  - 说明: 表格标题，Step 0.5 场景固定为 `"评分分层候选商品 — 请选择要诊断的商品"`；独立选品场景固定为 `"重点品圈选结果"`

- **`columns`**:
  - 类型: `Array<Object>`
  - 说明: 表格列定义，每列包含 `key`（字段名）、`label`（列标题）、`width`（可选，列宽 px）

- **`rows`**:
  - 类型: `Array<Object>`
  - 映射规则: Step 0.5 场景从 `score_and_select` 返回的 `data.data.c_grade_candidates` 数组逐项转换；独立选品场景从 `data.data.products` 数组逐项转换。两者字段结构相同，映射规则一致
  - 必须字段: `id`, `title`, `level`, `levelName`, `totalScore`, `payAmount`, `buyerCount`, `uv`

### 映射规则

从 `score_and_select` 返回的每个 product 对象（`c_grade_candidates` 或 `products` 数组里的元素结构相同）：

| 源字段路径 | 目标字段 | 说明 |
|-----------|---------|------|
| `item_id` | `id` | 商品 ID |
| `title` | `title` | 商品标题 |
| `classification.level` | `level` | 分层等级，如 S级、C级 |
| `classification.name` | `levelName` | 分层名称，如 优化调整品 |
| `scores.total_score` | `totalScore` | 综合得分 |
| `key_metrics.pay_ord_amt_1d` | `payAmount` | 支付金额 |
| `key_metrics.pay_ord_byr_cnt_1d` | `buyerCount` | 支付买家数 |
| `key_metrics.ipv_uv_1d` | `uv` | 访客数 |

### columns 定义

```json
[
  { "key": "id", "label": "商品ID", "width": 100 },
  { "key": "title", "label": "商品标题" },
  { "key": "level", "label": "等级", "width": 70 },
  { "key": "levelName", "label": "分层", "width": 100 },
  { "key": "totalScore", "label": "综合得分", "width": 90 },
  { "key": "payAmount", "label": "支付金额", "width": 100 },
  { "key": "buyerCount", "label": "买家数", "width": 80 },
  { "key": "uv", "label": "访客数", "width": 80 }
]
```

### 交互结果处理

用户选择商品后，从交互返回结果中提取每条选中行的 `id` 字段，即为 `item_id`。

- **Step 0.5 场景**：只把 `itemId` 传给 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>`，进入 Step 2（与 Step 1 情况A 的处理方式一致，最多并发处理 5 个）
- **独立选品场景**：不进入诊断流程，直接结束（不触发聚合 Tool）

---

## 5. select_products_from_search (Table 组件)

### 组件类型

`type: table` — 用于展示关键词搜索结果，供 Step 1 情况B 的用户从中勾选目标商品。

### 数据槽位定义

- **`title`**:
  - 类型: `String`
  - 说明: 表格标题
  - 示例值: `"搜索结果: {keyword}"`，其中 `{keyword}` 为用户输入的搜索关键词

- **`columns`**:
  - 类型: `Array<Object>`
  - 说明: 表格列定义

- **`rows`**:
  - 类型: `Array<Object>`
  - 映射规则: 从 `search_offer_by_keyword` 返回的 `data.data.items` 数组逐项转换
  - 必须字段: `id`, `title`, `imageUrl`, `minPrice`, `maxPrice`, `status`

### 映射规则

从 `search_offer_by_keyword` 返回的每个 item 对象：

| 源字段路径 | 目标字段 | 说明 |
|-----------|---------|------|
| `itemId` | `id` | 商品 ID |
| `title` | `title` | 商品标题 |
| `mainImage` | `imageUrl` | 商品主图 URL |
| `minPrice` | `minPrice` | 最低价（元） |
| `maxPrice` | `maxPrice` | 最高价（元） |
| `status` | `status` | 商品状态，需转换为中文：`PUBLISHED` → `上架中`，其他值 → `未上架` |

### columns 定义

```json
[
  { "key": "imageUrl", "label": "图片", "width": 80 },
  { "key": "id", "label": "商品ID", "width": 140 },
  { "key": "title", "label": "商品标题" },
  { "key": "minPrice", "label": "最低价(元)", "width": 100 },
  { "key": "maxPrice", "label": "最高价(元)", "width": 100 },
  { "key": "status", "label": "状态", "width": 90 }
]
```

### 交互结果处理

用户选择商品后，只提取选中行的 `id` 字段作为 `itemId`，传给 `alibaba.1688.get.item.diagnosis.context --item_id <itemId>` 并进入 Step 2（与 Step 1 情况A 的处理方式一致）；不传 `loginId` 或 `userId`。

用户未选择任何商品时结束本次体检，禁止默认选择第一行。

---

## 6. choose_product_locator (Card 组件)

### 组件类型

`type: card` — 当异常商品与评分分层至少一个来源可用、但最终均为成功零结果时，让用户选择继续定位商品的方式。

### 数据结构

```json
{
  "questions": [
    {
      "question": "请选择一种方式继续定位商品：",
      "options": ["输入商品 ID", "关键词搜索"]
    }
  ]
}
```

选择“输入商品 ID”后触发 `input_offer_id`；选择“关键词搜索”后触发 `input_search_keyword`。用户未选择时结束本次体检，禁止自动进入任一分支。

---

## 7. input_search_keyword (Input 组件)

### 组件类型

`type: input` — 用户选择关键词搜索但当前请求未提供关键词时，收集要搜索的商品关键词。

### 数据结构

```json
{
  "questions": [
    {
      "question": "请输入要搜索的商品关键词：",
      "placeholder": "例如：护眼套装"
    }
  ]
}
```

取得非空关键词后调用 `search_offer_by_keyword`；未输入时结束本次体检。搜索接口失败时立即终止搜索，成功零结果才允许进入相似词或手工 ID 恢复流程。

---

## 8. 报告交付顺序

1. workflow 返回完整 `merchant_report` 和内部一键优化精确任务清单；automatic 固定使用 Markdown，直接输出报告，不调用选择卡、诊断组件或隐藏区块
2. `delivery=markdown` 时 Agent 必须先把 `merchant_report` 完整输出到主对话；`delivery=component` 时基础诊断、行动点和定时任务入口由组件及 `footer_actions` 承载，主对话只输出 `same_offer_markdown`
3. 当前回复不得调用 notice、card、其他 workflow 或 skill
4. 输出报告后立即结束当前回复，不追加总结或追问
5. 用户下一条消息明确回复“进入一键优化”或“设置定时任务”后，再进入对应流程
