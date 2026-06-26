# 展示规范

本文档定义了 1688-customer-opportunity skill 所有场景下的输出展示规则。

---

## 数据展示

- `customer_reception_advice` 批量结果：**≤5 人用 Markdown 表格展示画像+建议，>5 人引导导出 Excel**（先展示结果概览表）
- **表格列动态裁剪**：展示前检查所有数据行，若某列在所有行中均无值（null / 空字符串 / —），则删除该列，禁止展示空列
- 直接展示返回的表格，不要额外补充数据日期、T+1、数据分区等说明
- 不要提及 rank / 优先级字段
- `list_cluster_buyer_detail` 返回的买家列表只展示前 10 名，需向用户说明总人数
- `get_cluster_marketing_plan` 展示时**忽略 offer_list**，不展示推荐商品列表
- 导出 Excel 时生成 Python 脚本，脚本中**只能使用英文引号**（`'` 或 `"`），禁止中文引号（`""`/`''`），避免语法错误

---

## 隐私约束

- **禁止展示 planId**：planId 仅用于后续 API 调用参数，不在任何表格或文字中展示给用户
- **禁止展示 userId / buyer_user_id**：所有场景（claw 表格、Excel 导出、文字描述）均不得展示用户 ID，买家标识统一用 loginId / 手机号 / 序号替代

---

## 交互后

- **每次展示结果后，必须用 AskUserQuestion 询问下一步操作**（例如：是否分析某客户的跟进方案、是否查看运营方案等），不要在 markdown 里写建议文字

---

## 其他约束

- **调用 customer_crowd_analysis 前的强制前置步骤**：必须已调用 list_customer_details 获取买家客群归属，crowd_type 参数必须来自返回结果，不可自行推断或猜测
- **禁止向用户透出内部执行逻辑**，如"按照技能流程"、"不展示明细表格"、"根据指引"等，直接执行并展示结果即可
