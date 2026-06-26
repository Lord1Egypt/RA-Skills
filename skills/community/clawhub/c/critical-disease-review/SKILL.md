---
name: med-critical-disease-review
description: 重大疾病理赔智能评估（支持 28 种病种）。输入住院病历结构化数据，调用内网评估接口，输出原始 JSON 与自然语言结论（结论 + 证据）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏥"
      }
  }
---

# 重大疾病理赔评估

概述
----
给定一份住院病历（结构化 `medicalRecord`，含诊断/文书等），本技能调用内网评估服务，对 **任意重大疾病病种** 进行判定，并返回：

- **最终结论**：符合/不符合（来自 `final_result`）
- **原因与证据**：按条件逐条给出 evidence（可带来源 source）
- **原始结果**：接口返回的完整 JSON（便于追溯与二次加工）

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理完成评估所必需的数据字段；不要求提供与评估无关的身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理（如姓名、证件号、手机号、详细地址、人脸/影像等）。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储（包含磁盘文件、数据库、日志）。仅在内存中短暂处理；**本次调用结束即销毁**。
- **第三方 API 风险提示**：在功能需要时，可能会调用第三方模型/服务接口；此时仅会发送**脱敏后的必要信息**，并使用加密传输。除完成本次请求外，不用于任何其他用途（如训练、画像、营销）。
- **医疗边界**：本技能输出为理赔条款/条件匹配与证据整理的辅助信息，不构成医疗诊断或治疗建议；如涉及临床判断请以执业医生意见为准。

支持病种（28）
--------------
- 心脏瓣膜手术：`heart_valve_surgery`
- 主动脉手术：`aortic_surgery`
- 冠状动脉搭桥术：`coronary_artery_bypass`
- 重大器官或造血干细胞移植术：`major_organ_transplant`
- 恶性肿瘤——重度：`malignant_tumor`
- 严重慢性肾衰竭：`severe_chronic_kidney_failure`
- 严重慢性肝衰竭：`severe_chronic_liver_failure`
- 急性重症肝炎或亚急性重症肝炎：`acute_severe_hepatitis`
- 严重慢性呼吸衰竭：`severe_chronic_respiratory_failure`
- 严重特发性肺动脉高压：`severe_idiopathic_pulmonary_hypertension`
- 严重脑损伤：`severe_brain_injury`
- 深度昏迷：`deep_coma`
- 严重脑中风后遗症：`severe_stroke_sequelae`
- 严重阿尔茨海默病：`severe_alzheimers_disease`
- 严重原发性帕金森病：`severe_primary_parkinsons_disease`
- 严重运动神经元病：`severe_motor_neuron_disease`
- 严重脑炎后遗症或严重脑膜炎后遗症：`severe_brain_encephalitis_sequelae`
- 严重非恶性颅内肿瘤：`severe_non_malignant_intracranial_tumor`
- 瘫痪：`paralysis`
- 双耳失聪：`bilateral_deafness`
- 双目失明：`bilateral_blindness`
- 语言能力丧失：`language_ability_loss`
- 严重克罗恩病：`severe_crohn_disease`
- 严重溃疡性结肠炎：`severe_ulcerative_colitis`
- 重型再生障碍性贫血：`severe_aplastic_anemia`
- 较重急性心肌梗死：`moderate_acute_myocardial_infarction`
- 严重Ⅲ度烧伤：`severe_third_degree_burn`
- 多个肢体缺失：`multiple_limb_loss`

输入格式
--------
请求为 JSON（示例见 `../data/med-major-disease-assess/req_data.json`），最少需要包含：

- `medicalRecord`：病历结构化对象
  - `mainDiagName` / `otherDiagName`：诊断信息（字符串/JSON 字符串均可）
  - `docs`：文书列表（每个 doc 至少包含 `docType` 与文本字段，如 `format_page_text`）

最小校验（先校验，再审核）
--------------------------
脚本会先对入参做最小结构校验，校验通过后才会调用审核接口：
- 请求体必须是 JSON object
- 必须包含 `medicalRecord`（object）
- `medicalRecord.docs` 必须是非空数组
- `docs` 中至少一项包含 `docType`

后端接口
--------
- HTTP API：`http://10.10.20.15:9010/api/v1/assessment/assess/{disease}?model_type=qwq`
- Content-Type：`application/json`

快速开始
--------

```bash
# 在本目录下运行
python3 scripts/major_disease_assess.py \
  --disease aortic_surgery \
  --input ../data/med-major-disease-assess/req_data.json
```

参数说明
--------
- `--disease STRING`
  - 病种类型（如：`aortic_surgery`、`heart_valve_surgery` 等）。
- `--input PATH`
  - 输入请求 JSON 路径（UTF-8）。
- `--output-json PATH`
  - 保存接口原始返回 JSON（默认：`../runs/med-major-disease-assess/{disease}_resp.json`）。
- `--output-text PATH`
  - 保存自然语言结论文本（默认：`../runs/med-major-disease-assess/{disease}_resp.txt`）。
- `--model-type STRING`
  - 查询参数 `model_type`（默认：`qwq`）。
- `--timeout SECONDS`
  - HTTP 超时秒数（默认：60）。

输出约定
--------
- 若指定输出路径的父目录不存在，会自动创建。
- 自然语言输出默认包含：
  - 结论（符合/不符合）
  - 原因（`final_result.reason`）
  - 逐条条件的证据（`conditions[*].evidence`，并附 `source/description`）

备注
----
- **发布约束**：示例输入、运行输出、自测脚本均放在 skill 包外（分别位于 `../data/`、`../runs/`、`../self_tests/`），skill 目录内仅保留可发布的核心文件（`scripts/`、`SKILL.md`、`_meta.json`）。
 

