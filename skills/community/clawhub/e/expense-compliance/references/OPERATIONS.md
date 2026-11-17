# 操作、规则与结果结构

## 识别票据

`receipt.extract` 接收 `document_type`、`file_name`、`mime_type` 与纯 Base64 `image_base64`。支持 JPEG、PNG、WebP，解码后最大 5 MB。结果包含票号、日期、销售方、税号、购买方、金额、币种、原始文字和置信度。

低于 `0.80` 的置信度会标记 `requires_confirmation: true`。不得把空字段补成推测值。

## 创建与更新制度

`policy.create` 接收 `name` 和 `rules`。`policy.update` 还需要 `policy_id` 与 `expected_version`，并以完整规则数组替换当前版本。

支持规则：

- `amount_limit`：字段 `maximum`、`currency`，可选 `category`。
- `required_document`：字段 `document_types`，可选 `category`。
- `allowed_currency`：字段 `currencies`。
- `maximum_document_age_days`：字段 `days`。
- `blocked_merchant`：字段 `names`。

每条规则可包含稳定 `id`，并使用 `severity: review|reject`。没有提供 ID 时平台生成 UUID。

示例：

```json
[
  {"id":"hotel-limit","type":"amount_limit","category":"hotel","maximum":"600.00","currency":"CNY","severity":"review"},
  {"id":"invoice-required","type":"required_document","document_types":["invoice"],"severity":"reject"}
]
```

## 审核申请

`claim.audit` 接收：

- `policy_id`、`expected_policy_version`
- `claim_number`、`claim_date`
- `category`、`claimed_amount`、`currency`
- 当前用户 1 至 10 个成功 `receipt.extract` 任务组成的 `receipt_task_ids`
- 可选 `confirmed_receipt_task_ids`：用户明确对照原图核验无误的 OCR 任务 ID，必须是本次 `receipt_task_ids` 的子集。平台保留模型原始 `confidence`，并独立记录人工确认用户与时间

结果 `outcome`：

- `compliant`：未命中已配置规则，不等于付款批准。
- `manual_review`：尚未人工确认的低置信度票据、疑似重复或 review 级规则需要人工核对。
- `non_compliant`：金额不一致、完全重复或 reject 级规则命中。

每项 `findings` 包含 `code`、`severity`、`message`、`rule_id` 与 `evidence`。

## 读取与导出

`policy.read`、`claim.read` 免费。`claim.export` 生成私有 Markdown 与 JSON，报告保留审核时的制度版本和免责声明。
