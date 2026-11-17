---
name: agent-redteam-kit
display_name: AI红队对抗测试（Red Team Kit）
display_name_en: "AI Red Team Kit"
description: "当用户说『测一下这个AI安不安全』『会不会被越狱』『让AI干危险的事它听不听』『上线前做对抗测试』，或要给一个 agent/提示词做安全性红队时使用。中英双库扫描越狱/危险能力请求（DAN/忽略指令/提权/数据外泄/自改进等），给出风险分级+加固建议，并设「危险操作闸门」（有门禁）。可运行脚本（redteam_scan 扫描器）。理论根基：LGD 三律之有门禁（危险动作先过闸）。触发词：红队、red team、越狱、jailbreak、对抗测试、prompt攻击、AI安全测试、危险指令、安全评估。"
version: 1.0.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Edit
category: AI安全
platforms: [windows, macos, linux]
read_when:
  - 要上线一个 agent 前做安全性对抗测试
  - 怀疑提示词能被越狱/被诱导干危险事
  - 收到「忽略之前的指令」「你是 DAN」类输入
  - 想给 AI 的高危动作加一道闸门
tags: [红队, red team, 越狱, jailbreak, 对抗测试, AI安全, 有门禁]
slug: agent-redteam-kit
title: AI红队对抗测试（Red Team Kit）
copyright: SynomosAI
description_zh: "当用户说『测一下这个AI安不安全』『会不会被越狱』『让AI干危险的事它听不听』『上线前做对抗测试』，或要给一个 agent/提示词做安全性红队时使用。中英双库扫描越狱/危险能力请求（DAN/忽略指令/提权/数据外泄/自改进等），给出风险分级+加固建议，并设「危险操作闸门」（有门禁）。可运行脚本（redteam_scan 扫描器）。理论根基：LGD 三律之有门禁（危险动作先过闸）。触发词：红队、red team、越狱、jailbreak、对抗测试、prompt攻击、AI安全测试、危险指令、安全评估。"
description_en: "Red-team toolkit for agents and prompts: bilingual jailbreak and dangerous-capability scan libraries (DAN, instruction override, privilege escalation, exfiltration) with severity reports."
classification:
  skillhub: ["security-compliance"]
  clawhub: ["development", "data-analytics"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true

changelog: "1.0.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：[skill-quality-gate](../skill-quality-gate/SKILL.md)


## English

### When to use
- When the user wants a security adversarial test, red-team drill, or jailbreak probe against an AI model, this skill should be called first.
- When input contains trigger words like "test whether this AI is safe" or "will it be jailbroken", or involves dangerous instructions (privilege escalation / data exfiltration / DAN).
- When running adversarial testing before an agent goes live, requiring risk grading and hardening advice.
- When a potential relay attack, instruction override, or self-improvement request is detected.

### Usage
No complex configuration is needed; the user triggers the keywords to activate the `redteam_scan` scanner automatically. To call the analysis via API, use: `redteam_scan --target <prompt text> --mode <attack mode>`. Here `<prompt text>` is the instruction or context under test, and `<attack mode>` is one of `dan`, `ignore_instruction`, `data_leak`, `privilege_escalation`, `self_improve`.

### Process
1. Identify security-related trigger words or implied intent in the user input.
2. Submit the target text to `redteam_scan.py` for scanning.
3. The script returns the jailbreak / dangerous-capability request type and a match score.
4. Judge the risk level per the LGD Three Laws and generate concrete hardening advice.
5. Run the "dangerous-action gate" check and output whether to allow or block the response.
6. Output the complete red-team test report and the final safety disposition.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 1.0.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用
当用户意图表达要对 AI 模型进行安全对抗测试、红队演练或越狱探测时，应优先调用此技能；
当输入包含『测一下这个 AI 安不安全』『会不会被越狱』等触发词，或涉及危险指令（提权/数据外泄/DAN）时；
在 Agent 上线前进行对抗测试评估，需执行风险分级与加固建议时；
检测到潜在的中继攻击、忽略指令或自改进请求时。

## 用法
调用本技能无需复杂配置，用户直接触发关键词即可自动激活 `redteam_scan` 扫描器；
若需主动通过 API 调取分析能力，请使用命令：`redteam_scan --target <prompt 文本> --mode <攻击模式>`；
参数说明中 `<prompt 文本>` 为待安全测试的指令或上下文，`<攻击模式>` 可选值为 `dan`, `ignore_instruction`, `data_leak`, `privilege_escalation`, `self_improve`。

## 流程
第一步：识别用户输入中的安全相关触发词或隐含意图；
第二步：将目标文本提交至 `redteam_scan.py` 脚本进行扫描；
第三步：脚本返回越狱/危险能力请求类型及匹配度评分；
第四步：根据 LGD 三律判定风险等级，生成具体加固建议；
第五步：执行「危险操作闸门」门禁校验，输出是否允许执行或拦截响应；
第六步：向用户输出完整的红队测试报告及最终安全处置意见。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
