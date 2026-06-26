# 交互组件详细规范

本文档定义了 1688-customer-opportunity-identify skill 中所有交互组件的具体数据结构与字段映射规则。

---

## 1. select_buyers_from_cluster（table 组件）

### 组件类型
`type: table`

### 触发时机
以下场景均触发：
- **展开客群明细**：`list_cluster_buyer_detail` 返回后，agent 排序后全量展示（有 planId）
- **查所有客群汇总买家明细**：并行拉所有客群 `list_cluster_buyer_detail`，合并去重后 agent 排序全量展示（有 planId）
- **客户机会监控-有客群**：默认第一个客群，agent 排序后全量展示（有 planId）
- **客户机会监控-无客群**：高价值买家筛选（GMV 高 / 采购频率高 / B类买家），agent 排序后全量展示（**无 planId**）

### 数据槽位定义（统一 2 列格式，所有触发场景一致）

- **`title`**: `String`，按场景动态构造：
  - 有客群（有 `cluster_name`）→ `"{cluster_name}待跟进买家列表（共 N 位）"`
  - 无客群（高价值买家筛选）→ `"待跟进买家列表（共 N 位）"`
- **`columns`**: `Array<Object>`，**必须显式声明**（merchant 类型框架不内置 columns 模板）
- **`rows`**: `Array<Object>`，buyer 列表数据

#### columns 定义（固定 2 列）

```json
[
  { "key": "buyer_login_id", "label": "买家账号", "width": 180 },
  { "key": "画像",            "label": "画像与跟进建议", "width": 400 }
]
```

#### rows 字段映射

| 槽位字段 | 数据来源 | 说明 |
|---------|---------|------|
| `buyer_login_id` | `list_cluster_buyer_detail` / `list_customer_details` 返回 | 买家账号，**禁止展示 userId** |
| `画像` | agent 根据 `customer_reception_advice` 返回的 `buyer_profile` 与 `follow_suggestion` 构造 | 格式：`"画像：{profile_summary}\n建议：{suggestion_summary}"`，profile_summary 与 suggestion_summary 各 ≤50 字（**语义压缩，不硬截**），原始值为空时填"暂无" |

**禁止传**：`buyer_credit_level` / `buyer_profile` / `follow_suggestion`（旧字段，已废弃；如果保留会让前端多渲染列）

#### 画像列语义压缩规则（agent 必读）

`buyer_profile` 和 `follow_suggestion` 原文通常超过 50 字。**必须由 agent 主动提炼，不得整段截取**。

**profile_summary（≤50字）**：保留等级 / GMV / 偏好 / 身份等核心关键词，删除修饰语和解释性背景。

```
❌ "该买家为店铺潜客，平台等级及活跃度等核心数据缺失，无法判定其采购规模与身份，仅能确认其有初步浏览意向"（56字）
✅ "店铺潜客，等级/活跃度数据缺失，初步浏览意向"（22字）

❌ "近12个月GMV为0，无历史交易记录，合作意愿待确认，需结合店铺产品与行业匹配度进一步评估其潜在价值"（50+字）
✅ "近12月GMV为0，无交易记录，合作意愿待确认"（22字）
```

**suggestion_summary（≤50字）**：保留核心行动动词 + 目标，删除解释性原因和背景说明。

```
❌ "1.立即补充买家【等级、客单价、生意赛道】标签，以确认其是否为高价值采购商；2.针对其GMV为0的情况，优先发送店铺介绍"（60+字）
✅ "补充等级/客单价标签确认价值；发送店铺介绍触达"（24字）
```

### 框架自动填充的字段
`selectionType: merchant` —— 框架根据此标识决定**选中数据写入云端的位置**（不影响渲染）。Skill **必须自行声明 columns**，否则前端无法识别列结构。

### 完整数据示例

```json
{
  "type": "table",
  "selectionType": "merchant",
  "title": "流失买家待跟进买家列表（共 2 位）",
  "columns": [
    { "key": "buyer_login_id", "label": "买家账号", "width": 180 },
    { "key": "画像",            "label": "画像与跟进建议", "width": 400 }
  ],
  "rows": [
    {
      "buyer_login_id": "alice123",
      "画像": "画像：近期采购意愿较强，偏好皮具\n建议：优先跟进，推送新品优惠"
    },
    {
      "buyer_login_id": "bob456",
      "画像": "画像：长期静默，意愿较低\n建议：低优跟进"
    }
  ],
  "actions": [
    {
      "key": "view_plan",
      "label": "查看客群运营计划",
      "description": "进入开启客群方案分支：调 get_cluster_marketing_plan --plan-id {planId} → confirm_marketing_plan input → activate_cluster_plan",
      "variant": "primary"
    }
  ]
}
```

### 自定义 Actions（Case 4 模式）

`actions` 数组根据当前场景是否有 `planId` 动态构造，1 个按钮：

**有 planId 时（客群场景）：**

| key | label | description（给大模型的指令，不展示给用户）| variant |
|-----|-------|-----|---------|
| `view_plan` | `查看客群运营计划` | 进入开启客群方案分支：调 get_cluster_marketing_plan --plan-id {planId} → confirm_marketing_plan input → activate_cluster_plan | `primary` |

**无 planId 时（高价值买家筛选场景）：**

| key | label | description（给大模型的指令，不展示给用户）| variant |
|-----|-------|-----|---------|
| `next_batch` | `换一批` | 商家对当前买家列表不满意，重新调 list_customer_details 并更换筛选条件（换优先级或扩大范围） | `primary` |

**回传结构**（点击自定义按钮时）：
```json
{
  "selectionType": "merchant",
  "data": {
    "selectedRows": [ { "buyer_login_id": "alice123", "画像": "..." } ],
    "action": {
      "key": "send_message",
      "label": "下单",
      "description": "..."
    }
  }
}
```

> ⚠️ **actions 按 planId 动态切换**：有 planId 用 `view_plan`（查看客群运营计划）；无 planId 用 `next_batch`（换一批）。

- 点「确认选择」：`"action": "confirm"`，按铁律 D 分支 A 处理
- 点「跳过」：`"action": "skip"`，selectedRows=[]，弹「换个客群」AskUserQuestion

### 商家操作回传结构（agent 必读）

商家完成选择后回传：

```json
{
  "selectionType": "merchant",
  "data": {
    "selectedRows": [ { "buyer_login_id": "alice123", "画像": "..." }, ... ],
    "action": "confirm" | "skip"
  }
}
```

| `data.action` | `data.selectedRows` | agent 行为（详见 SKILL.md 铁律 D 节） |
|---|---|---|
| `"confirm"` | ≥1 | 弹「行动选项」AskUserQuestion（3/4 选项，按 planId 决定） |
| `"skip"` 或 selectedRows=[] | `[]` | 弹「翻页/换组」2 选项 AskUserQuestion |

### ⚠️ rows 传参方式（高频错误）

```
❌ 错误：rows 是 JSON 字符串（直接导致 InvalidArgumentError: received string）
{ "rows": "[{\"buyer_login_id\":\"alice\"}]" }

✅ 正确：rows 是原生数组
{ "rows": [{"buyer_login_id": "alice", "画像": "画像：xxx\n建议：xxx"}] }
```

### 注意事项
- **`rows` 必须是原生数组**，禁止 `json.dumps` / `JSON.stringify` 序列化成字符串再传入——平台验证类型，传字符串直接报 `InvalidArgumentError`
- **两接口配合**：先调 `list_cluster_buyer_detail`（或 `list_customer_details`）拿 loginId 列表，再调 `customer_reception_advice` 拿画像与建议，agent 按 loginId join 后构造 2 列 rows
- `rows` 数组不能为空，调用前需确认有返回数据
- **禁止**将 `userId` / `buyer_user_id` 放入 rows 数组
- 总人数需另行告知用户（来自 `data.data.buyer_count` 或合并后总数）

---

## 2. confirm_marketing_plan（input 组件）

### 组件类型
`type: input` —— 多步澄清/自由输入题，端侧按顺序逐题展示

### 触发时机
**「开启客群方案」分支**：`get_cluster_marketing_plan` 返回文案后，让商家确认或修改旺旺文案

### 数据槽位定义

- **`questions`**: `Array<Object>`，**固定 1 题**（**⚠️ input 类型禁止传 `title` / `columns` / `rows`，平台强制报 INVALID_INPUT**）

#### questions 固定结构（1 题）

| 题号 | question 文本 | options | allowMultiple | 商家行为 | 回写到 activate_cluster_plan |
|------|---------------|---------|---------------|---------|-----------------------------|
| 1 | `"旺旺文案"` | `["<get_cluster_marketing_plan 返回的 sale_desc>", "老客回馈，多品类好物等您来选，品质保障，期待再次合作！"]` —— 第 1 项动态取 sale_desc、第 2 项固定通用兜底 | `false` | 选预设或在端侧输入框写新文案 | 直接传 `saleDescription` |

**🚨 options 构造铁律（平台强制 ≥2 项，违反报错）：**

平台对 input 类型 options 校验 **`minimum: 2, inclusive: true`** —— 数组长度必须 ≥ 2，**`[]` 也会被拒**。

文案构造规则：

| 第 1 项（动态，取 get_cluster_marketing_plan.sale_desc） | 第 2 项（固定，禁止修改） |
|------|------|
| 直接复用 `sale_desc` 原文（若超过 100 字可适当精简，但语义不变） | `"老客回馈，多品类好物等您来选，品质保障，期待再次合作！"` |

**禁止**：
- ❌ 传 `options: []` / 单元素数组（平台报 `Too small: expected array to have >=2 items`）
- ❌ 用「自定义文案」/「请在输入框填写」等占位伪选项
- ❌ 修改第 2 项固定文案

### 框架自动填充的字段
`selectionType: 确认客群运营计划` —— 框架根据此标识决定**输入结果写入云端的位置**（不影响渲染）。

### 完整数据示例

```json
{
  "type": "input",
  "selectionType": "确认客群运营计划",
  "questions": [
    {
      "question": "旺旺文案",
      "options": [
        "26年纺织辅料代工老厂，支持小批量起订（100件），快反供应+多工艺整合，立即咨询获取专属方案。",
        "老客回馈，多品类好物等您来选，品质保障，期待再次合作！"
      ],
      "allowMultiple": false
    }
  ]
}
```

### 商家操作后处理（agent 必读）

> ⚠️ **强红线**：input 类型**无 `action.key` 字段**，agent 必须按下表硬绑定行为，禁止靠"语义判断"决定下一步。

| input 回传字段 | agent 必须立即执行 | 禁止行为 |
|---|---|---|
| `selectionType="确认客群运营计划"` + `data.questions[0]` 有答案 | **同一 turn 内**：取答案作为 `saleDescription` → 按 `references/capabilities/activate_cluster_plan.md` 构造 JSON → 调 `activate_cluster_plan --plan-json '<JSON>'` | ❌ 禁止重新调 `list_customer_cluster` 或重新展示 AI 客群列表<br>❌ 禁止再次弹 `confirm_marketing_plan`<br>❌ 禁止追加任何 AskUserQuestion 二次确认<br>❌ 禁止仅回复"已确认"等文字而不调用 tool |

**判断"input 已完成"的唯一信号**：回传中 `data.questions[0]` 存在用户答案（无论是 options 选中项还是自由输入）。**禁止**把端侧"已确认需求·确认客群运营计划"的渲染态当作"待用户继续操作"——那只是 input 完成后的展示气泡，不是按钮。

### 注意事项

- `questions` 必须是**原生数组**（Array），禁止 `json.dumps` / `JSON.stringify`
- 旺旺文案 `options` **必须传 2 项数组**（平台 minimum:2 强制）；第 1 项取 `get_cluster_marketing_plan.sale_desc` 原文；第 2 项固定兜底文案（**禁止修改**）
- **禁止**传 `[]`、单元素数组、`[..., "自定义"]`
- **input 类型禁止传 table 字段（`title` / `columns` / `rows`）** —— 平台校验直接拒绝并返回 `INVALID_INPUT`
