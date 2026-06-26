# get_customer_profile

查询单个客户的详细档案，包括基础信息、采购习惯、采购决策依据、跨店询盘信息，以卡片式区块展示。

## 前置条件

- 已配置 AK
- 推荐传 `--buyer-id-list` 一次查多个客户；仅查一位且只有昵称时，传 `--nick-name` 作为兜底

## 参数

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| `buyerIdList` | Array<string> | 二选一 | 客户 ID **字符串**数组，多人一次查（首选），如 `["abc","def"]`；后端类型为 `Array<String>`，加密格式 ID 原样透传即可 |
| `nickName` | string | 二选一 | 买家昵称，单查兜底，模糊查询 |

## 返回字段

`data.data[0]` 为匹配到的买家详情，关键字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `nickName` | string | 买家昵称 |
| `lLevel` | string | 客户等级 |
| `buyerConstitution` | String | 客户体质 |
| `mainCate` | string | 主采类目 |
| `payCnt180d` | int | 采购次数 |
| `payAmt180d` | int | 半年同本店类目采购额 |
| `buyerPurchaseHabits` | JSON | 客户采购习惯 |
| `purchaseDecisions` | JSON | 采购决策依据 |
| `otherShopInqInfor` | JSON | 跨店询盘信息 |

## 典型用法

```bash
# 多人批量（首选）
python3 {baseDir}/cli.py get_customer_profile --buyer-id-list '["id1","id2","id3"]'

# 单人查询（兜底）
python3 {baseDir}/cli.py get_customer_profile --nick-name 张三
```

## 展示规则

客户基础信息由以下独立字段组合渲染：nickName、lLevel、buyerConstitution、mainCate、payCnt180d、payAmt180d

### 串场话语（必须）

每个区块之间必须有一句桥梁语，避免直接贴数据显得突兀：

| 区块 | 串场语模板 |
|------|-----------|
| 👤 客户基础信息 | "首先是客户的身份画像与近半年采购规模：" |
| 🛒 客户采购习惯 | "接着看客户日常的采购节奏与偏好，帮你挑选最合适的沟通时机：" |
| 🟨 采购决策依据 | "然后看看客户下单前最在意的决策点，跟进时要优先回应这些：" |
| 🏪 跨店询盘信息 | "最后看看客户在其他店铺的询盘动作，掌握外部对比信号：" |

### 颜色区块规范

- 以 HTML 颜色区块形式展示，不同模块用不同背景色区分
- 👤 **客户基础信息** — 浅蓝色 `#e0f2fe`
- 🛒 **客户采购习惯** — 浅绿色 `#dcfce7`
- 🟨 **采购决策依据** — 浅黄色 `#fef3c7`
- 🏪 **跨店询盘信息** — 浅紫色 `#f3e8ff`
- 区块内字段逐行展示，`<b>字段名</b>：值`（字段名尽量用中文可读名）
- 空值统一展示为 `—`
- **流失风险分 / 风险分 / riskScore** 等数值字段必须由 cmd.py 自动转换为「极高 / 较高 / 中等 / 较低 / 很低」的程度描述，禁止直接透出原始分数
