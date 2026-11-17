---
name: fund-fee-calc
description: 资管费率净收益试算器 — 试算管理/托管/销售三费总成本与净收益，宣传含保本承诺即 FAIL（零依赖） 适用场景：当需要资管费率净收益试算器能力时使用本技能；触发词：fund-fee-calc。
slug: fund-fee-calc
version: 1.0.1
display_name: 资管费率净收益试算器
display_name_en: Fund Fee & Net Return Calc
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "资管费率净收益试算器 — 试算管理/托管/销售三费总成本与净收益，宣传含保本承诺即 FAIL（零依赖）"
description_en: "Fund fee and net-return calculator: management, custody and sales fee total cost with net return; guarantee-of-principal claims FAIL (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [fund-fee-calc, AI 治理, 资管费率, 净收益, 保本承诺]
read_when:
  - 买基金/资管产品前要测算管理/托管/销售三费对净收益的影响
  - 要检查营销材料里有没有"保本""刚性兑付"等违规话术
  - 要对比不同费率结构下投资者实际到手收益
  - 用户说「这个产品扣完费还剩多少」「宣传说保本能信吗」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/fund_fee_calc.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. Before investing in a fund or asset-management product, when you need to precisely model how the three fees (management, custody, sales) affect final net value.
2. When screening financial product marketing materials for illegal wording such as "guaranteed principal", under zero-dependency compliance logic.
3. When an investor needs to compare actual take-home returns across fee structures to judge a product's real profitability.

### Usage
1. Run `python fund_fee_calc.py` directly, or import the `fund_fee_calc` module for function calls.
2. Core inputs: `principal`, `duration` (holding days), `fees` (three-fee structure object) and `marketing_terms` (promotional copy).
3. If the marketing text contains keywords like "principal guarantee" or "rigid payment", the zero-dependency FAIL logic fires and refuses to compute net return.

### Workflow
1. **Gather info**: prepare principal, holding period and the corresponding fee details.
2. **Compliance screen**: feed in the promotional copy / marketing content for a first-pass guarantee-of-principal risk check.
3. **Trigger the script**: run `fund_fee_calc.py`; compliance rules are validated first.
4. **Output**: the system returns the net-return value or a FAIL status code — no floor-return figures are ever output.
5. **Cross-check**: verify that the three-fee total covers expected returns; confirm the fee structure is reasonable.
6. **Decision feedback**: based on the trial calculation, generate compliant recommendations and a risk-warning list for the user.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在进行基金或资管产品投资前，需精确测算包含管理、托管及销售在内的三费总成本对最终净值的影响时。
2. 在评估金融产品营销材料中是否存在“保本承诺”等违规话术，且必须遵循零依赖合规逻辑的场景下。
3. 投资者需要对比不同费率结构下的实际到手收益，以判断产品真实盈利能力的财务分析场景中。

### 用法
1. 直接执行 `python fund_fee_calc.py` 脚本，或导入 `fund_fee_calc` 模块进行函数调用。
2. 核心输入参数包括：`principal`（本金）、`duration`（投资天数）、`fees`（三费结构对象）及 `marketing_terms`（宣传文案）。
3. 若检测到营销文本中包含保本、刚性兑付等关键词，将自动执行零依赖 FAIL 逻辑，拒绝计算净收益。

### 流程
1. **信息收集：** 准备投资本金、持有期限及对应费率明细数据。
2. **合规筛查：** 输入宣传文案或营销内容，进行保本承诺风险初筛。
3. **脚本触发：** 通过 `fund_fee_calc.py` 执行计算逻辑，优先验证合规规则。
4. **结果输出：** 系统返回净收益数值或 FAIL 状态码，不输出任何保底收益信息。
5. **交叉验证：** 检查三费成本合计是否覆盖预期收益，确认费用结构合理性。
6. **决策反馈：** 基于试算报告，向用户生成合规建议及风险提示清单。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
