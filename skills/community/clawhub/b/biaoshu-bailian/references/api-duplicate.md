# 标书查重 API

用于比较 2-3 份不同投标文件之间的雷同/相似风险。标书查重不是免费能力，按平台规则消耗可用字数。

## 发起前流程

1. 先收齐 2-3 份投标文件。
2. 招标文件可选，只能作为 `tender_file` 公共表述基线，不能算作投标文件。
3. 发起前必须确认用户合法持有并有权处理全部投标文件/招标文件。

## `POST /bid-duplicate/runs`

入参：

- multipart `bid_files`：2-3 份投标文件。
- multipart `tender_file`：可选 1 份招标文件。
- 或 JSON / 表单 URL 字段：`bid_file_urls`、`tender_file_url`。
- 必填：`legal_possession_attested=true`。

文件限制：

- 投标文件支持 `.doc/.docx/.pdf`，必须 2-3 份。
- 投标文件单份 ≤ 1024 MB。
- 招标文件可选 1 份，≤ 50 MB。
- 总大小 ≤ 2 GB。
- 不支持扫描型 PDF。

选项：

- `enable_image`：图片相似检查，默认 true。
- `enable_metadata`：文档元数据检查，默认 true。
- `enable_semantic`：语义相似检查，默认 true。
- `exclude_tender_baseline`：排除招标原文共同表述，默认 true。

返回：`{"job_id":"..."}`

计费：

- 发起前校验可用字数。
- 查重完成后按平台规则消耗可用字数；具体消耗以平台流水为准。
- 可用字数不足返回 402 `insufficient_balance`。

## 结果字段

`GET /jobs/{job_id}/result` 返回：

```json
{
  "service": "bid_duplicate",
  "result": {
    "run_id": 123,
    "duplicate": {}
  }
}
```

`duplicate` 按文件对展示：

- 文本相似。
- 图片相似。
- 文档元数据。
- 主体线索。
- 招标原文共同表述。
- 风险率、证据片段和修改建议。

查重只输出风险线索，不输出“已串标/确认围标”等定性结论，也不提供规避监管的一键降重建议。

## 常见错误

- 422 `validation_error`：投标文件不足 2 份、超过 3 份、未确认合法持有、文件类型或大小不合法。
- 409 `report_task_conflict`：同一用户已有合规/查重类任务运行中。
- 402 `insufficient_balance`：可用字数不足，提示购买会员或字数包后重试。
- 500/任务失败 `bid_duplicate_failed`：优先转述 `duplicate_error_message`；错误详情会带 `run_id`、`duplicate_status`，用于后台定位。
