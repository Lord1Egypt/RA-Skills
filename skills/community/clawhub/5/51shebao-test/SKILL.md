---
name: hr-calculator
description: HR 税费计算器。用户问工资个税/税后收入/到手工资、劳务报酬、稿酬、特许权使用费、离职补偿金个税，或要做"税后反推税前"时使用。触发词：个税、到手工资、税后、税前、五险一金、劳务费、稿酬、特许权使用费、补偿金、反推工资。
---

# HR 计算器

hr-tool 服务的纯本地计算移植版，无网络依赖。全部为 Python 3 标准库脚本。

## 用法

统一入口（输出 JSON）：

```bash
python3 scripts/hr_calc.py <子命令> [参数]
```

| 用户问题 | 子命令 | 示例 |
|---|---|---|
| 工资个税、到手工资 | `salary` | `salary --before-tax 20000 --periods 1 --social-ee 1050.50 --fund-ee 1400` |
| 税后反推税前工资 | `reverse-salary` | `reverse-salary --after-tax 15000 --periods 1` |
| 劳务报酬个税 | `labor` | `labor --before-tax 10000` |
| 劳务报酬反推 | `reverse-labor` | `reverse-labor --after-tax 8400` |
| 稿酬个税 | `author` | `author --before-tax 5000` |
| 特许权使用费个税 | `privilege` | `privilege --before-tax 5000` |
| 特许权使用费反推 | `reverse-privilege` | `reverse-privilege --after-tax 4200` |
| 离职补偿金(N+1)个税 | `compensation` | `compensation --before-tax 300000 --avg-salary 12000` |

## 参数收集

- `salary` / `reverse-salary`：
  - 必填：`--before-tax`（或 `--after-tax`）；`--periods` 期数（月），默认 1——累计预扣法下"算一年中第 12 个月"就传 12
  - `--social-ee` 社保个人月缴总额、`--fund-ee` 公积金个人月缴额，默认 0。用户不知道数额时：提示查工资条或当地社保 APP；也可传 0 做纯个税估算，但必须向用户注明结果是估算
  - 六项专项附加扣除（月度额，默认 0）：`--deduction-child-edu` 子女教育、`--deduction-continue-edu` 继续教育、`--deduction-medical` 大病医疗、`--deduction-house` 住房、`--deduction-elder` 赡养老人、`--deduction-infant` 3岁以下婴幼儿照护
  - `--personal-pension` 个人养老金，默认 0
- `compensation`：`--avg-salary` 是当地上年职工月平均工资——需用户自行提供（当地统计局/人社局公布），skill 不内置该数据
- 其余子命令只需 `--before-tax` 或 `--after-tax`

## 输出解读

- `salary`：`after_tax_income` 到手、`personal_income_tax` 本期个税、`taxable_income` 累计应纳税所得额、`tax_rate` 预扣率档位(%)、`quick_deduction` 速算扣除数、`five_deduction` 专项附加扣除明细
- `labor`/`author`/`privilege`：`income_tax` 税额；`taxable_income_formula` 是应纳税所得额的计算公式，可直接解释给用户
- 注意：salary 的到手按**未舍入**税额计算（与原 hr-tool 服务一致），可能与"税前 − 显示税额 − 社保 − 公积金"有 1 分钱舍入差，向用户解释时不必纠结这 1 分钱

## 边界说明

- 五险一金按用户自报数额计算，不查询实时城市社保参数（原服务经保险中台查询）
- 税则按现行个税法：综合所得 7 级累进、起征点 5000/月；政策调整时更新 `scripts/calc/constants.py`
- 更详细的公式与税率表见 `references/tax-rules.md`
