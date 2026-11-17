# 标书审查 API

用于发起标书合规审查。标书审查不是免费能力，按平台规则消耗可用字数。

## `POST /projects/{project_id}/compliance-reviews`

前置：`project_id` 来自智能解读结果。招标文件必须先解读，审查复用同一个 project，不重复上传招标文件。

入参：

- multipart `bid_files`：一份或多份投标文件。
- 或 JSON `{"file_urls":[...],"is_blind_bid":false,"is_electronic_bid":false}`。

文件限制：

- 投标文件支持 `.doc/.docx/.pdf`。
- 最多 100 份。
- 单份 ≤ 1024 MB。
- 总大小 ≤ 2 GB。

选项：

- `is_blind_bid`：暗标。
- `is_electronic_bid`：电子投标。
- `sibling_unit_names`：敏感单位名称。
- `semantic_review=false` 或 `enable_semantic_review=false`：关闭语义审查，仅保留规则类检查。

返回：`{"job_id":"..."}`

计费：

- 发起前校验可用字数。
- 审查完成后按平台规则消耗可用字数；具体消耗以平台流水为准。
- 可用字数不足返回 402 `insufficient_balance`。

## 结果字段

`GET /jobs/{job_id}/result` 返回：

```json
{
  "service": "compliance",
  "result": {
    "compliance": {
      "run_id": 42,
      "status": "completed",
      "summary": {},
      "partial_summary": {},
      "bid_files": [],
      "issues": [],
      "similarity_issues": [],
      "manual_items": [],
      "scope_summary_lines": [],
      "error_message": null
    }
  }
}
```

重点字段：

- `summary`：高风险/待复核/提示数量、一句话结论、语义审查状态。
- `partial_summary`：部分结果或阶段性结果提示。
- `issues[]`：合规问题，含风险等级、招标依据、投标证据、修改建议。
- `similarity_issues[]`：多份投标文件之间的雷同线索。
- `manual_items[]`：人工核查清单。
- `scope_summary_lines[]`：检查范围。

如果 `semantic_review` 或 `partial_summary` 表示语义审查未完整完成，必须如实说“当前为部分结果/语义审查未完整完成”，不能说成完整审查。

## 常见错误

- 409 `report_task_conflict`：同一用户已有合规/查重类任务运行中，等完成后再发起。
- 422 `validation_error`：投标文件缺失、类型不支持、数量或选项不合法。
- 413：文件超出单份或总大小限制。
- 402：可用字数不足，提示购买会员或字数包后重试。
