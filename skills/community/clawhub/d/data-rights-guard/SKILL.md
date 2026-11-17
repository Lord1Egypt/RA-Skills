---
name: data-rights-guard
display_name: 训练数据版权护栏（Data Rights Guard）
display_name_en: "Data Rights Guard"
description: "当用户说『爬的数据能拿来训练吗』『数据集没写许可证』『微调数据版权合规吗』『怎么确认数据能商用』，或在用数据(爬取/购买/公开集/用户授权)做训练/微调/评测前想确认版权与许可边界时使用。把每条数据当『带权属的资产』：查许可证·商用权限·署名要求·来源可溯，缺许可的不许进训练集。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：数据版权、训练数据合规、数据集许可证、版权护栏、数据权属、商用权限、data license、微调合规。"
version: 1.0.5
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要用爬取/购买/公开/用户数据做训练或微调
  - 数据集没写许可证或许可不明
  - 问「这数据能商用吗」
  - 想确认数据来源可溯、署名到位
tags: [数据版权, 训练数据合规, 数据集许可证, 权属护栏, 商用权限, data license, AI合规, 去敏]
slug: data-rights-guard
title: 训练数据版权护栏（Data Rights Guard）
copyright: SynomosAI
description_zh: "当用户说『爬的数据能拿来训练吗』『数据集没写许可证』『微调数据版权合规吗』『怎么确认数据能商用』，或在用数据(爬取/购买/公开集/用户授权)做训练/微调/评测前想确认版权与许可边界时使用。把每条数据当『带权属的资产』：查许可证·商用权限·署名要求·来源可溯，缺许可的不许进训练集。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：数据版权、训练数据合规、数据集许可证、版权护栏、数据权属、商用权限、data license、微调合规。"
description_en: "Copyright and license guard for training data: verify provenance, license terms and commercial-use boundaries before training, fine-tuning or evaluating on scraped, purchased, public or user-authorized data."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/rights_guard.py
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
changelog: "1.0.5: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
This skill applies whenever the user needs to confirm copyright and licensing boundaries *before* building a training set, a fine-tuning set or an evaluation set. It is triggered by questions such as "Can scraped data be used for training?", "The dataset states no license" or "How do I confirm the data may be used commercially" — in other words, any question touching data ownership. It also covers large-scale data collection and third-party licensed data: verify that the source is traceable and that authorization credentials are valid against the LGD Three Laws (registered · evidenced · gated), so that data without a license never enters the training set.

### Usage
Two invocation modes are supported: natural-language keyword trigger and direct CLI call. In natural language, a query containing triggers such as "数据版权", "training compliance" or "data license" is automatically parsed and routed to the core logic implemented in `rights_guard.py`. For direct invocation, tune parameters on the command line: `python rights_guard.py --query <question> --source_type [scraped/purchased/public] --permission [commercial/attribution]`. The script lives in `rights_guard.py`; cache files sit under `__pycache__`. Make sure the skill package is loaded in the runtime and that the process holds data-metadata parser permissions.

### Workflow
Execution follows the standard three-laws gate. First, receive the user input and identify the target data source or dataset identifier. Second, read the data metadata / license files and check that the "registered" (source provenance) and "evidenced" (license credentials) fields are complete. Third, compare against the concrete business scenario (e.g. fine-tuning, commercial use) and check for "gated" restrictions and for missing-license risk. Finally, produce a compliance verdict: whether the data may be admitted to the training set, the required attribution format, and a summary of the legal basis. If no valid authorization is detected, the data intake is blocked automatically and the risk is flagged.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.5
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
本技能适用于用户在构建训练集、微调集或评测集前，需确认数据版权与许可边界的合规场景。当用户提出“爬的数据能拿来训练吗”、“数据集没写许可证”或“怎么确认数据能商用”等涉及数据权属的疑问时，应调用此技能进行审查。此外，在进行大规模数据采集或使用第三方授权数据时，若需要依据 LGD 三律（有籍·有证·有门禁）验证数据来源可溯性与授权凭证的有效性，防止缺许可的数据进入训练集，也属于该技能的核心适用范围。

### 用法
本技能支持自然语言关键词触发与命令行脚本调用两种模式。在自然语言交互中，用户只需输入包含“数据版权”、“训练合规”或 "data license" 等触发的查询，系统会自动解析意图并执行 `rights_guard.py` 中的核心逻辑；在直接调用模式下，可通过命令 `python rights_guard.py --query <问题描述> --source_type [爬取/购买/公开集] --permission [商用/署名]` 进行指定参数调优。脚本位于 `rights_guard.py` 中，相关缓存文件位于 `__pycache__`，需确保运行环境已加载该技能包且具备数据元数据解析器权限。

### 流程
技能执行遵循标准的三律校验流程：首先接收用户输入并识别目标数据来源或数据集标识；其次依据 LGD 理论根基读取数据元数据或许可证文件，核对“有籍”与“有证”信息是否完备；随后对比具体业务场景（如微调、商用），检查是否存在“有门禁”限制及缺许可风险；最后生成合规判定报告，明确是否允许纳入训练集、所需署名格式及法律依据摘要。若检测出无有效授权，则自动阻断数据入库操作并提示风险。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.5
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
