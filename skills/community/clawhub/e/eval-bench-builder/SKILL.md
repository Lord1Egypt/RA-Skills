---
name: eval-bench-builder
display_name: 评测基准构建器（Eval Bench Builder）
display_name_en: "Eval Benchmark Builder"
description: "当用户说『怎么评测这个AI/技能好不好』『给我造个测试集』『评测用例怎么设计』『要可复现的评测』，或要给一个 agent/模型/技能建可复现评测基准时使用。从能力说明+边界用例生成结构化 eval 样本（输入/期望/判定标准），保证可复现、可回归。可运行脚本（bench_build 生成器）。理论根基：LGD 三律之有证（评测可复现、可核验）。触发词：评测基准、eval、测试集、benchmark、可复现评测、评测用例、怎么测AI。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 要评测一个 agent/模型/技能的效果
  - 需要可复现、可回归的测试集
  - 不知道评测用例怎么设计
  - 收到「造个评测」类指令
tags: [评测基准, eval, benchmark, 测试集, 可复现, 有证]
slug: eval-bench-builder
title: 评测基准构建器（Eval Bench Builder）
copyright: SynomosAI
description_zh: "当用户说『怎么评测这个AI/技能好不好』『给我造个测试集』『评测用例怎么设计』『要可复现的评测』，或要给一个 agent/模型/技能建可复现评测基准时使用。从能力说明+边界用例生成结构化 eval 样本（输入/期望/判定标准），保证可复现、可回归。可运行脚本（bench_build 生成器）。理论根基：LGD 三律之有证（评测可复现、可核验）。触发词：评测基准、eval、测试集、benchmark、可复现评测、评测用例、怎么测AI。"
description_en: "Build reproducible evaluation benchmarks for agents, models and skills: structured samples (input, expected, judge) generated from capability statements plus boundary cases."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/bench_build.py
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
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
Use it when the user's intent includes keywords like "evaluate how good this AI / model / skill is", "build me a test set" or "design reproducible evaluation cases". It fits any moment where structured input / expected-output / judge-criteria must be generated so that results are reproducible and theoretically grounded. It also fits when the user's current capability statement is vague and a benchmark dataset with clear boundaries must be built on the LGD Three Laws — verifiable by construction.

### Usage
Natural-language instructions are supported; the parameters must name the target object (e.g. the model name), the evaluation dimensions and the verifiable criteria. The script `bench_build.py` runs the core construction logic; the input is auto-parsed and injected into the Python runtime. To reproduce the run locally, follow the generated script path and execute it on the terminal.

### Workflow
1. Recognize the trigger words and extract the evaluation target and boundary conditions. 2. On the LGD Three Laws, assemble the input / expected / judge templates in memory. 3. Call `bench_build.py` to perform the automated benchmark generation. 4. Validate that the generated data structure meets reproducibility and file-format requirements. 5. Emit the benchmark file or code snippet containing the complete test cases. 6. Return an executable command so the user can run the script in a terminal for regression checks.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.1.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
当用户意图包含“评测 AI/模型/技能好坏”、“造测试集”或“设计可复现评测用例”等关键词时。在需要生成结构化输入/期望/判定标准，以确保评估结果具备可复现性和理论依据的场景下。当用户对现有能力说明感到模糊，需基于 LGD 三律构建边界明确且可核验的基准数据集时。

### 用法
调用方式支持自然语言指令，参数需明确指定目标对象（如模型名称）、评测维度及可验证标准。脚本 `bench_build.py` 将负责执行核心构建逻辑，系统会自动解析输入并注入 Python 运行时环境。若需直接复现，用户应参考生成的脚本文件路径进行本地执行。

### 流程
1. 技能识别触发词并提取评测目标与边界条件信息。2. 依据 LGD 三律理论，在内存中组装输入/期望/判定标准模板。3. 调用 `bench_build.py` 脚本完成自动化基准生成任务。4. 校验生成的数据结构是否符合可复现性要求及文件格式规范。5. 输出包含完整测试用例的基准文件或代码片段。6. 返回可执行指令，允许用户通过终端运行脚本进行回归验证。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
