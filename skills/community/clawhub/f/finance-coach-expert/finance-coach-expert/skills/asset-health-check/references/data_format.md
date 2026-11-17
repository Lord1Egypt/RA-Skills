# 输入数据格式与脱敏规范（data_format.md）

## 一、脱敏铁律

用户只需提供：**金额 + 类别 + 四桶归属（bucket）+ 备注**。

**绝对不采集**：账号、证件号、手机号、银行卡号、平台登录名、真实姓名、家庭住址。

数据全程**本地处理不出本机**，报告落本地文件。可告知用户："可全程不登录任何平台。"

## 二、输入 JSON 结构（assets.json）

```json
{
  "experience": "L1",
  "monthly_expense": 6000,
  "risk_tolerance": "balanced",
  "assets": [
    {"cat": "现金存款", "amount": 50000, "bucket": "flexible", "note": ""},
    {"cat": "货币基金", "amount": 30000, "bucket": "flexible", "note": ""},
    {"cat": "债券基金", "amount": 40000, "bucket": "steady", "note": ""},
    {"cat": "股票", "amount": 60000, "bucket": "growth", "note": ""},
    {"cat": "公募基金", "amount": 50000, "bucket": "growth", "note": ""},
    {"cat": "商业保险现金价值", "amount": 20000, "bucket": "protection", "note": ""}
  ],
  "liabilities": [
    {"item": "房贷剩余本金", "amount": 200000},
    {"item": "信用卡分期", "amount": 8000}
  ],
  "insurance_flagged": ["重疾险", "医疗险"],
  "ai_identified_items": [
    {"cat": "某银行理财", "amount": 30000, "needs_review": true}
  ]
}
```

## 三、字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `experience` | 否（默认 L1） | `L1`=0 基础 / `L2`=有经验但理论不扎实。**进入时先问用户**："你操作过股票/基金吗？主要靠什么决定买卖？"据此分档 |
| `monthly_expense` | 建议给 | 月刚性支出（元），算应急金月数的基准。缺 → 应急金标"信息不全" |
| `risk_tolerance` | 否 | `conservative`/`balanced`/`aggressive`，用户自填标签，只用于选择中性经验区间对照，**不做风险测评、不判适不适合** |
| `assets[].cat` | 是 | 类别名（脱敏，如"现金存款"，不写"XX银行活期"） |
| `assets[].amount` | 是 | 金额（元）。无效/缺失 → 该项不计入并进信息缺口 |
| `assets[].bucket` | 建议 | 四桶之一：`flexible`(灵活取用) / `steady`(稳健) / `growth`(进取) / `protection`(保障)。缺 → 该项不入桶 |
| `assets[].note` | 否 | 备注。**矛盾事实检测依赖它**：备注同时含"保本"与"年化/收益/息"+数字 → 列为矛盾事实 |
| `liabilities[].item` / `amount` | 是 | 负债名 + 金额（房贷按**剩余本金**，不是总贷款额） |
| `insurance_flagged` | 否 | 已持有的保障项名称列表。只做事实陈述，**不荐险种、不做医疗判断** |
| `ai_identified_items[]` | 否 | 从截图/PDF 识别的项，必须带 `needs_review: true`。**未核对不进任何结论**，只在体检卡列"待核对清单" |

## 四、四桶归类速查

| bucket | 中文 | 典型资产 |
|---|---|---|
| `flexible` | 灵活取用 | 现金、活期、货币基金、随时可取理财 |
| `steady` | 稳健 | 债券基金、定期存款、国债、固收+ |
| `growth` | 进取 | 股票、股票型/混合型公募基金、指数基金 |
| `protection` | 保障 | 保单现金价值、年金现值（注意：保费≠现金价值） |

归类拿不准时问用户"这笔钱短期内会不会动用/亏了会不会睡不好"，不要替用户硬分。

## 五、截图/PDF 处理规则（可信度分级）

1. 截图/PDF **仅作辅助预览**，识别结果一律先入 `ai_identified_items` 且标 `needs_review: true`。
2. **强制人工核对**：把识别结果逐项列给用户确认（"识别为 XX 30,000 元，对吗？"），错读金额/类别比没读更危险。
3. 用户确认后，让用户把核对过的项**自己并入手填 `assets`**（或明确说"我核对无误"后再转入），并标 `reviewed: true`。
4. 识别失败/看不清 → 直接退回手填，**不硬猜、不脑补金额**。
5. 报告中每条数据带可信度标签：`手填(可信)` / `AI识别(待核)`，**体检结论只用"手填(可信)"项**。

## 六、CSV 输入格式（可选，适合表格党）

约定：`#` 开头为元信息注释行（key=value）；资产段表头首列必须是 `cat`；负债段表头首列必须是 `item`；两段之间用空行分隔。

```csv
# experience=L1
# monthly_expense=6000
# risk_tolerance=balanced
# insurance_flagged=重疾险|医疗险

cat,amount,bucket,note
现金存款,50000,flexible,
货币基金,30000,flexible,
债券基金,40000,steady,

item,amount
房贷剩余本金,200000
信用卡分期,8000
```

- `bucket` 列可留空：脚本按类别关键词自动归桶（如"XX理财"→稳健），并在信息缺口里提示核对。
- `insurance_flagged` 多个险种用 `|` 分隔。
- 注意：CSV 无 `ai_identified_items` 段——截图/PDF 识别出来的待核对项只能走 JSON 录入；两边对**同样数据**的静态计算结果一致。

## 七、自动归桶规则（脚本内置）

| 类别含关键词 | 归入桶 |
|---|---|
| 现金/活期/定期存款/货币基金/货基/余额宝/零钱/随时/备用金 | flexible 灵活取用 |
| 债券/债基/国债/固收/定期理财/理财 | steady 稳健 |
| 股票/股基/指数基金/混合基金/权益/ETF | growth 进取 |
| 保险/年金/寿险/保单 | protection 保障 |

自动归桶只是兜底，结果会在"信息缺口"区提示用户核对；归类拿不准的项保持"未入桶"并提示。

### P2 扩展字段（2026-11-04，可选）

| 字段 | 必填 | 说明 |
|---|---|---|
| `monthly_income` | 否 | 月税后收入（元）。给了才出「现金流月报」节（结余率 + 532 教学参照） |
| `liabilities[].rate` | 否 | 各笔负债年化利率（%）。给了才出「负债成本事实卡」（按利率降序，≥18% 标注高息事实） |
| `housing_loan_plan` | 否 | 大额决策测算：`{"loan_amount": 本金, "years": 年限, "rate_annual": 年化利率}` → 出月供测算与月供/月收入比（等额本息公式，纯事实） |

三个字段全部可选——不给就不出对应节，体检卡其余部分不受影响。三个节都只报事实与教学参照，不下"该不该"的判断。
