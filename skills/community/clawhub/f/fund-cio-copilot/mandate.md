# Investment Mandate（基金画像）

## 定位
GP 日常语言是"这个 deal 在不在 mandate 里"，不是"我们的 strategy 是什么"。Mandate 是硬约束 + 软偏好的集合，任何分析前先查。

## 字段定义
| 字段 | 说明 | 类型 |
|------|------|------|
| fund_size | 基金规模 | 数值 |
| remaining_quota | 剩余可投额度 | 数值 |
| stage | 投资阶段（PreA / A / B…） | 枚举 |
| sector | 产业方向（机器人/AI/新能源…） | 列表 |
| region | 落地/返投区域 | 列表 |
| ticket | 单项目额度上限 | 数值 |
| ownership | 目标股比区间 | 区间 |
| capital_source | 财政资金比例 / LP 构成 | 文本 |
| gov_constraints | 返投要求（如 50%）、招商要求（制造业优先） | 文本 |
| return_target | 回报要求（如 IRR 25%） | 数值 |
| annual_kpi | 年度任务（投资数 / 落地数） | 文本 |

## 匹配算法（硬约束 vs 软对齐）
```
Mandate Fit = 硬约束通过 ? 软对齐评分 : 直接 FAIL
```

### 硬约束（任一违反 → Mandate Fit ❗，建议终止深度分析）
- stage 不在范围
- sector 不在方向
- region 不符合
- 拟融资额 > ticket
- 无法满足 gov_constraints（返投/招商）

### 软对齐（0-100 评分，只参考不卡死）
- sector 战略契合度
- region 招商价值
- 补链强链价值
- 与年度 KPI 匹配度

## 输出格式
```
【Mandate Check】
Mandate Fit：✅ / ❗
硬约束：
  Stage ✓ / ✗
  Sector ✓ / ✗
  Region ✓ / ✗
  Ticket ✓ / ✗（拟融资 X，上限 Y）
  Gov ✓ / ✗
软对齐评分：78（战略契合高 / 招商价值中）
建议：进入分析 / 终止（除非战略投资理由）
```

## 首次配置（Setup 捕获，首跑必做）
首次进入任意 Mode 前，若 `config/mandate.json` 的 `configured` 为 false，按以下一轮捕获并持久化（借鉴 Matt Pocock「setup-first」：先固化本地配置，通用 skill 才不脆弱）：
- 必问（一轮问完，给推荐默认值 ➡️）：region（返投/落地区域）、ticket（单项目额度上限）、sector（产业方向）、gov_constraints（返投/招商要求）、return_target（回报要求）
- 选填（缺省用行业默认）：fund_size、remaining_quota、stage、ownership、capital_source、annual_kpi
- 捕获后写入 `config/mandate.json` 并将 `configured` 置 true，后续每次评估直接读取，不再反问
- 变更硬约束需人工确认（定义权在 GP）

## 持久化与回退
- 配置落点：`config/mandate.json`（本 skill 目录下）
- 未配置时：禁止静默用"默认 VC 权重"兜底；必须显式提示"未配置基金画像，建议先配置"并引导完成 Setup 捕获
