---
name: bias-auditor
display_name: 偏见审计（Bias Auditor）
display_name_en: "Bias Auditor"
description: "当用户说『AI回答有偏见』『输出性别/地域/年龄刻板印象』『怎么检测模型偏见』『内容要过公平审查』，或在发布面向人群的内容(招聘/推荐/客服/评测)前想做公平性自检时使用。把模型输出当『带视角的生产物』：扫人口群体词·刻板表述·单边归因，标出潜在偏见并给去偏改写建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：偏见检测、bias audit、公平性、刻板印象、AI歧视、内容审查、公平自检、stereotype。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 模型输出疑似带性别/地域/年龄/职业刻板印象
  - 招聘/推荐/评测类内容要过公平审查
  - 用户问「怎么检测 AI 偏见」
  - 对外发布前想做公平性自检
tags: [偏见审计, bias audit, 公平性, 刻板印象, 去偏, 内容审查, AI伦理, 可靠性]
slug: bias-auditor
title: 偏见审计（Bias Auditor）
copyright: SynomosAI
description_zh: "当用户说『AI回答有偏见』『输出性别/地域/年龄刻板印象』『怎么检测模型偏见』『内容要过公平审查』，或在发布面向人群的内容(招聘/推荐/客服/评测)前想做公平性自检时使用。把模型输出当『带视角的生产物』：扫人口群体词·刻板表述·单边归因，标出潜在偏见并给去偏改写建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：偏见检测、bias audit、公平性、刻板印象、AI歧视、内容审查、公平自检、stereotype。"
description_en: "Audit model outputs for bias before publishing people-facing content (hiring, recommendations, support): demographic terms, stereotypes and unfairness scans with fix suggestions."
classification:
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true

changelog: "1.1.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：[skill-quality-gate](../skill-quality-gate/SKILL.md)


## English

### When to use
- When the user questions AI answers for bias, or raises gender/regional/age stereotypes.
- Before publishing people-facing content for hiring, recommendation, or support, to run a fairness self-check.
- When trigger words like "AI discrimination", "fairness review", or "bias detection" appear.

### Usage
- Call directly: `python bias_audit.py --input <text>`.
- Parameters: `--input` is the model output or copy; `--framework` selects the LGD Three Laws validation mode.
- In documentation mode, load `bias_audit.py` to run the automated scan.

### Process
1. Identify the trigger and load the local script `bias_audit.py`.
2. Tokenize the input and extract demographic terms and one-sided attribution patterns.
3. Per the LGD Three Laws, check whether data is registered, evidenced, and gate-compliant.
4. Produce de-biasing rewrite suggestions and flag potential bias risk points.
5. Output a standardized audit report.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 1.1.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用
- 当用户质疑 AI 回答存在偏见，或提出性别/地域/年龄刻板印象时。
- 在发布面向招聘、推荐、客服等人群的内容前需进行公平性自检时。
- 检测到「AI 歧视」「内容过公平审查」或「偏见检测」等触发词指令时。

## 用法
- 直接调用脚本：`python bias_audit.py --input <待检测文本>`
- 参数说明：`--input` 为模型输出或发布文案，`--framework` 用于指定 LGD_Three_Laws 验证模式。
- 若技能处于文档型服务中，可通过加载 `bias_audit.py` 文件读取并执行自动化扫描任务。

## 流程
1. 识别触发指令并加载本地脚本 `bias_audit.py`。
2. 对输入文本进行分词，提取人口群体词与单边归因模式。
3. 依据 LGD 三律检查数据是否有籍、有证及门禁合规性。
4. 生成去偏改写建议并标记潜在偏见风险点。
5. 输出包含审计结论的标准化报告。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
