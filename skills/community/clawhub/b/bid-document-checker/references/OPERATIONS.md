# 项目、资料库与阶段操作

以下路径均相对 `/api/v1/bid-document-checker`，所有管理接口 Ability 为 `bid.inspect`，操作接口 Ability 与 operation 同名。所有 POST 携带稳定 Idempotency-Key。

## 创建和更新项目

POST `/projects`：`name`、`subject`、`deadline`（例如 `2026-11-30T10:00:00+08:00`）、`timezone`（例如 `Asia/Shanghai`）。GET `/projects`、`/projects/{id}` 读取当前 `id`、`version`、文件列表、到期时间。POST `/projects/{id}`：`expected_version` 加要修改的项目字段。POST `/projects/{id}/delete`：`expected_version`，立即撤销并清理项目副本和产物。

## 上传与资料库

POST `/projects/{id}/files` 使用 multipart：`expected_version`、`file`、`role`，角色仅 `tender`、`addendum`、`material`、`other`。POST `/projects/{id}/files/role`：`expected_version`、`file_id`、`role`；POST `/projects/{id}/files/remove`：`expected_version`、`file_id`。

GET `/materials`、`/materials/{id}` 查询独立资料库及不可变版本。POST `/materials` multipart：`file`、`subject`、`material_type`（两者必须出现，未知为null），可选 `issued_on`、`expires_on`（YYYY-MM-DD）、`source`。POST `/materials/{id}`：同上加 `expected_version`，生成新版本；POST `/materials/{id}/delete`：`expected_version`，删除库副本，既有项目副本按30天期限保留。

POST `/projects/{id}/materials`：`expected_version`、`material_id`、`material_version`；冻结独立项目副本，资料库后续替换不改变历史项目。GET `/projects/{id}/revisions` 查询最多50项阶段历史，`stale` 为true不能作为后续来源。

## 预检和分析

五个操作均需 `project_id`、整数 `expected_version`。

`bid.inspect` 无其他字段，免费返回真实页数、OCR需求和解析问题。`bid.analyze` 加 `inspect_revision_id`、`acknowledged_model_transfer: true`（用户已同意必要内容传输和最高费用），输出要求、材料、建议、引用、冲突、覆盖限制。未知字段保持null，OCR失败不表示空白或没有要求。

## 人工确认

`bid.review`：`analysis_revision_id`、`human_confirmed: true`、`confirmations` 数组（必须覆盖全部要求）。每项 `requirement_id`、`material_ids` 数组；可选 `format_confirmation`、`condition_confirmation`、`waiver_reason`。修正要求使用 `corrections`（material_type、quantity、requires_validity、condition、format）及 `correction_reason`。

可选 `material_corrections` 数组：每项 `id`、`reason` 加 subject、material_type、issued_on、expires_on。`conflict_resolutions` 按冲突原索引填 `{reason: "人工适用与优先级理由"}`；未解决项不提供，不能压缩索引造成错配。有补遗还需 `addendum_review_reason`；否则保留未解决。所有确认必须来自用户，Agent不能自行冒充。

## 核验与组包

`bid.check` 加 `review_revision_id`、前阶段64字符 `fingerprint`。结果为 matched（仅已建模条件满足）、issues、pending_confirmation；coverage保留未覆盖页，draft标示未解决。

`bid.package` 加 `check_revision_id`、其 `fingerprint`、`attachment_order`（项目全部附件ID、无重复、用户确认顺序）。核验为草稿时必须由用户明确确认 `acknowledged_draft: true`。生成PDF、ZIP、manifest目录和页码表；ZIP原件checksum不变，汇总PDF不保留数字签名，无法转换时明确不完整草稿。任何项目变化需重新核验，不能沿用旧指纹。

## 从用户资料到可提交请求

先输出一张待核对清单：项目名称、投标企业全称、含时区的截止时刻、业务时区、各文件角色。招标文件不算企业证明材料，补遗的适用顺序由用户确认。没有某项材料时标为缺失，不创建假附件。API 支持 PDF/DOCX/JPG/PNG，每文件10 MiB；若宿主无法读取材料，不推断其内容，上传后依平台证据与工作台进行复核。

下面 JSON 为最小结构样例。`REPLACE_*` 必须替换成当前响应中的真实值，整数版本也要按当前回执替换；不得直接照抄占位标识。每一阶段使用独立稳定幂等键。

创建 `POST /projects`：

```json
{"name":"设备采购投标","subject":"示例公司有限公司","deadline":"2026-11-30T10:00:00+08:00","timezone":"Asia/Shanghai"}
```

管理响应 `data.id` 是项目 UUID，`data.version` 是版本。随后 multipart `POST /projects/{id}/files`，表单字段为 `file`、`expected_version`、`role`。例如招标文件 role=tender，营业执照 role=material。每次上传后重新 GET 项目读取最新 `data.version`，不能沿用第一次的版本。

```sh
: "${BID_DOCUMENT_CHECKER_API_KEY:=${AI_SKILLS_API_KEY:?请先配置平台密钥}}"
SITE="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer ${BID_DOCUMENT_CHECKER_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: $UPLOAD_REQUEST_KEY" \
  -F "expected_version=$PROJECT_VERSION" -F 'role=tender' \
  -F "file=@$TENDER_FILE" "$SITE/api/v1/bid-document-checker/projects/$PROJECT_ID/files"
```

执行预检 `POST /bid.inspect`：

```json
{"project_id":"REPLACE_PROJECT_ID","expected_version":3}
```

轮询预检任务。读取 `result.revision_id`、`result.project_version` 及覆盖问题，再核对 GET 项目的当前版本。分析 `POST /bid.analyze`，只有用户授权了模型传输及当时最高费用才设置 accepted 字段：

```json
{"project_id":"REPLACE_PROJECT_ID","expected_version":3,"inspect_revision_id":"REPLACE_INSPECT_REVISION_ID","acknowledged_model_transfer":true}
```

分析后读取 `result.revision_id`，从 `GET /projects/{id}/revisions` 取得该非 stale 修订的完整 payload，向用户展示全部要求与材料证据。确认样例仅适用于确实只有一项要求、没有额外条件或补遗冲突的情况：

```json
{"project_id":"REPLACE_PROJECT_ID","expected_version":3,"analysis_revision_id":"REPLACE_ANALYSIS_REVISION_ID","human_confirmed":true,"confirmations":[{"requirement_id":"REPLACE_REQUIREMENT_ID","material_ids":["REPLACE_MATERIAL_FILE_ID"]}]}
```

用户确认的 material_ids 来自当前项目的企业材料文件 ID；不是资料库ID，也不是 requirement_id。有条件、格式、补遗或冲突时按前文补齐理由，不省略问题来取得通过。以上请求提交到 `/bid.review`。

核验 `POST /bid.check` 使用 review 的修订及指纹：

```json
{"project_id":"REPLACE_PROJECT_ID","expected_version":3,"review_revision_id":"REPLACE_REVIEW_REVISION_ID","fingerprint":"REPLACE_REVIEW_FINGERPRINT"}
```

组包 `POST /bid.package` 使用 check 的修订及指纹：

```json
{"project_id":"REPLACE_PROJECT_ID","expected_version":3,"check_revision_id":"REPLACE_CHECK_REVISION_ID","fingerprint":"REPLACE_CHECK_FINGERPRINT","attachment_order":["REPLACE_TENDER_FILE_ID","REPLACE_MATERIAL_FILE_ID"]}
```

attachment_order 必须是当前项目全部附件的无重复排列，由用户确认。check 标记草稿时，需要用户另行同意收费草稿才加 `acknowledged_draft:true`；拒绝时停在核对，不代为确认。分析、核验和组包各自收费前都要核对当前价格与授权，不能把分析授权当作无限后续付费授权。

## 每个阶段的状态卡

保存 operation、项目ID、当前版本、来源revision_id、fingerprint、原请求、稳定幂等键及task_id。请求成功不等于核验通过；只有完整证据、用户确认与相应任务结果都满足条件后才进入下一步。发现 `_truncated` 或 `_meta.truncated` 不得把摘要当完整要求，改读项目管理的修订；仍不完整则工作台复核。
