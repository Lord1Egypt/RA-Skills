---
name: fin-reg-calc
description: fin-reg-calc — LGD 三律在金融 / 持牌机构 AI（投顾·风控·反洗钱）域的纵深合规工具（零依赖）：投资者适当性匹配 + 大额上报阈值校验，对 AI 系统/数据做可执行合规校验。 适用场景：当需要金融AI合规计算能力时使用本技能；触发词：fin-reg-calc。
slug: fin-reg-calc
version: 1.0.1
display_name: 金融AI合规计算
display_name_en: Finance AI Compliance Calculator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: SynomosAI
description_zh: "fin-reg-calc — LGD 三律在金融 / 持牌机构 AI（投顾·风控·反洗钱）域的纵深合规工具（零依赖）：投资者适当性匹配 + 大额上报阈值校验，对 AI 系统/数据做可执行合规校验。"
description_en: "LGD three-laws compliance for licensed financial AI (advisory, risk control, AML): investor suitability matching plus large-amount reporting threshold checks (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [fin-reg-calc, AI 治理, 金融合规, 适当性, 反洗钱]
read_when:
  - AI 投顾系统向用户推荐金融产品前要校验投资者适当性等级匹配
  - 交易风控模块识别大额/异常资金流动时要做反洗钱上报阈值检查
  - 金融机构内审要对 AI 决策模型做 LGD 三律符合性检测
  - 用户说「这个产品能不能卖给这个客户」「大额要不要上报」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/fin_reg_calc.py
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
1. Before an AI advisory system recommends financial products to a user, when investor-suitability grade must be matched.
2. When a trading risk-control module detects large or unusual fund flows, and AML reporting-threshold compliance must be checked.
3. When internal auditors at a financial institution need a deep LGD three-laws conformance check on an AI decision model.

### Usage
- The main script is `fin_reg_calc.py`, runnable directly in a Python environment or from the command line.
- Key parameters: `--investor_profile` (investor profile JSON) and `--product_risk` (product risk-grade code).
- Make sure the local config has loaded the LGD rule set, or let the script read its built-in compliance logic library.

### Workflow
1. Initialize the runtime; confirm the Python version and script execution permissions.
2. Build the dataset with customer info, product info and transaction amount.
3. Launch `fin_reg_calc.py` to run suitability matching and the large-amount reporting-threshold check.
4. The system outputs the compliance verdict (pass / reject) and the corresponding risk score grade.
5. Generate a standardized compliance report for front-end display or automatic archiving.
6. Write the audit log so this check is traceable and meets regulatory requirements.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. AI 投顾系统在向用户推荐金融产品前，需校验投资者适当性等级是否匹配。
2. 交易风控模块在识别大额或异常资金流动时，需执行反洗钱上报阈值合规检查。
3. 金融机构内部审计人员需对 AI 决策模型进行 LGD 三律符合性深度检测。

### 用法
- 主要调用脚本为 `fin_reg_calc.py`，支持通过 Python 环境直接执行或命令行调用。
- 关键参数说明：`--investor_profile` (投资者画像数据 JSON)、`--product_risk` (产品风险等级代码)。
- 需确保本地配置已加载 LGD 规则集，或直接读取内置合规逻辑库进行运算。

### 流程
1. 初始化执行环境，确认 Python 版本及脚本执行权限无误。
2. 构建包含客户信息、产品信息及交易金额的数据集合。
3. 启动 `fin_reg_calc.py` 进行适当性匹配与大额上报阈值校验运算。
4. 系统输出合规判定结果（通过/拒绝）及对应的风险评分等级。
5. 生成标准化合规报告供前端显示或自动归档存储。
6. 完成审计日志记录，确保本次校验操作可追溯并符合监管要求。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
