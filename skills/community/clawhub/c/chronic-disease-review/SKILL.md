---
name: med-chronic-disease-review
description: 门诊慢病审核（糖尿病/高血压）。输入 OCR 结果数组 JSON，输出审核结论与原因（原始 JSON + 自然语言结论）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 门诊慢病审核

概述
----
给定一份 OCR 结果数组（每项包含 `fileName/page/docType/ocrText`），本技能会：

- 输出审核接口原始 JSON
- 输出自然语言摘要（结论 + 原因）

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理审核所必需的文本内容；不要求也不鼓励提供与审核无关的身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理（如姓名、证件号、手机号、详细地址、人脸/影像等）。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储（包含磁盘文件、数据库、日志）。仅在内存中短暂处理；**本次调用结束即销毁**。
- **第三方 API 风险提示**：在功能需要时，可能会调用第三方模型/服务接口；此时仅会发送**脱敏后的必要信息**，并使用加密传输。除完成本次请求外，不用于任何其他用途（如训练、画像、营销）。
- **医疗边界**：本技能输出为审核规则匹配与原因摘要的辅助信息，不构成医疗诊断或治疗建议；如涉及临床判断请以执业医生意见为准。

输入格式
--------
输入必须是 JSON 数组（list），示例：

```json
[
  {"fileName":"xxx.pdf","page":1,"docType":"出院记录","ocrText":"..."},
  {"fileName":"xxx.pdf","page":2,"docType":"检验报告","ocrText":"..."}
]
```

快速开始
--------
从 `skills` 目录执行：

```bash
# 糖尿病
python3 scripts/chronic_disease_review.py \
  --disease-code diabetes \
  --input data/med-chronic-disease-review/糖尿病_ocr_task_result.json

# 高血压
python3 scripts/chronic_disease_review.py \
  --disease-code hypertension \
  --input data/med-chronic-disease-review/高血压_ocr_task_result.json
```

参数说明
--------
- `--disease-code STRING`：**必填**。糖尿病/高血压（也支持 `diabetes/hypertension/dm/htn` 别名）。本 skill 每次只审核一个病种。
- `--review-type STRING`：可选。默认 `慢病审核`（也可传 `大病审核` 等服务支持的值）。
- `--input PATH`：OCR 数组 JSON（UTF-8）。
- `--base URL`：后端 base（默认：`http://10.10.20.15:9011`）。
- `--llm-model STRING`：可选。模型名。
- `--timeout SECONDS`：HTTP 超时；`0` 表示一直等待（默认：0）。
- `--output-json PATH`：保存原始返回 JSON（默认：`../runs/med-chronic-disease-review/{scenario}_resp.json`）。
- `--output-text PATH`：保存自然语言摘要（默认：`../runs/med-chronic-disease-review/{scenario}_resp.txt`）。

输出约定
--------
- 若输出路径父目录不存在，会自动创建。
- 自然语言摘要重点字段：
  - `final_decision`：通过/不通过
  - `reasoning`：原因（可选）

备注
----
- **发布约束**：示例输入、运行输出、自测脚本均放在 skill 包外（分别位于 `../data/`、`../runs/`、`../self_tests/`），skill 目录内仅保留可发布的核心文件（`scripts/`、`SKILL.md`、`_meta.json`）。

