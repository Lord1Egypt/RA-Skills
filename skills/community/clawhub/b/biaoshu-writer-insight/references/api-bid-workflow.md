# 智能解读与标书制作 API

用于“解读招标文件 → 抽包 → 选页数 → 生成成品标书”的完整流程。智能解读和标书制作强相关，放在同一分册。

## 流程

1. `POST /interpretations` 上传招标文件，得到解读任务。
2. `GET /jobs/{job_id}` 轮询解读进度。
3. `GET /jobs/{job_id}/result` 获取 `project_id` 和 8 维度解读结果。
4. `POST /bid-documents/{project_id}/packages` 抽取分包。
5. 展示分包、系统建议页数、最大页数、预计消耗字数、当前可用字数，让用户确认。
6. `POST /bid-documents/{project_id}/generate` 生成成品标书。
7. `GET /jobs/{job_id}/download-url` 获取短时下载链接。

## `POST /interpretations`

- 入参：multipart `file` 或 JSON `{"file_url":"https://..."}`。
- 文件：招标文件 `.pdf/.doc/.docx`，≤ 50 MB。
- 返回：`{"job_id":"..."}`
- 计费：智能解读免费，可用字数为 0 也能发起；生成前按页数做消耗预估，预估仅供参考，实际消耗以平台最终结算为准。

结果中的 `result.project_id` 是后续抽包、生成、标书审查的统一项目句柄。

核心字段：

- `project_info[]`：项目基本信息。
- `compliance[]`：合标/资格要求。
- `disqualification[]`：废标红线。
- `evaluation[]`：评分标准。
- `key_requirements[]`：关键要求。
- `business_terms[]`：商务条款。
- `pricing[]`：报价要求。
- `procurement_analysis{}`：采购背景。
- `decision_analysis{}`：控标洞察、参与建议、风险信号、行动建议。

## `POST /bid-documents/{project_id}/packages`

- 无 body。
- 返回分包列表和页数建议。
- 抽包是标书制作的准备动作，不作为独立成果单独计费。

典型结果：

```json
{
  "service": "bid_document",
  "result": {
    "packages": [],
    "is_multi_package": false,
    "package_count": 1,
    "suggested_pages": 200,
    "max_total_pages": 1200,
    "estimated_words_per_page": 500,
    "estimate_reserve_factor": 1.05,
    "suggested_estimated_words": 105000,
    "estimate_note": "按目标页数约 500 字/页估算，预计消耗仅供参考，实际消耗以平台最终结算为准"
  }
}
```

规则：

- `is_multi_package=true`：必须展示 `packages` 给用户选择，收集 `package_ids`。
- `is_multi_package=false`：不问包，直接进入页数确认，生成时传 `--no-package`。
- 用户未确认页数前不得提交生成任务；用户输入页数不能超过 `max_total_pages`。
- 使用系统建议页数时，也必须把抽包结果里的 `suggested_pages` 明确带入 Skill 生成命令，不能默认按固定页数处理。

## `POST /bid-documents/{project_id}/generate`

入参：

```json
{"package_ids":[11,12],"total_pages":80}
```

非多包项目可省略 `package_ids`。`total_pages` 最高 1200。

计费与拦截：

- 标书制作按实际生成内容消耗可用字数。
- Open API / Skill 提交前按 `total_pages * 500 * 1.05` 预估所需字数；预估仅供页数确认参考，实际消耗以平台最终结算为准；生成前不做余额不足示警。
- Skill 调用 `generate` 时需把抽包结果里的 `max_total_pages` 作为动态上限；超过则本地拒绝，不提交 Open API。
- 生成前只展示预计消耗，不根据余额做字数不足示警，也不阻止创建长任务；生成中如果真实消耗超过剩余可用字数，再按平台规则停止并返回不足提示。
- 生成中如果真实消耗超过剩余可用字数，任务会停止继续写正文，错误码可能是 `insufficient_balance` / `insufficient_points`。如果后端已经成功导出半成品，skill 应先交付半成品下载链接；充值或购买字数包后，用 `continue-generate` 基于同一 `outline_id` 继续生成正文，不要重新解读、抽包或重建大纲。

进度阶段：

- `select`：选包。
- `requirements`：抽需求。
- `outline`：生成大纲。
- `content`：生成正文。
- `templates`：抽取制式模板并识别待填项。
- `export`：导出 Word。

进度字段：

- `/jobs/{job_id}` 应持续返回 `progress.percent`、`progress.stage` / `stage_label`、`progress.message`、`progress.current_step`、`progress.total_steps`、`progress.current_step_label`、`progress.elapsed_seconds`，可选返回 `estimated_remaining_seconds`。
- 如果后端没有写入上述字段，skill 只能展示排队/运行心跳，不能生成章节级进度。

完成前完整性校验：

- 后端在标记 `succeeded` 前应校验计划章节数、已生成章节数、空章节、模板占位符、待填项和导出 docx 结构。
- 发现缺章节或结构异常时，不应标记成功；应自动补写，或把任务置为 `failed` 并返回明确错误码/原因供 skill 转述。

生成成功后先取 `download-url` 给用户短时链接；用户明确要本地文件时，再用 `result -o` 下载本地文件。若 `download-url` 返回 `partial=true`，必须说明这是半成品、展示 `completion.generated/total/missing`，并提示补足可用字数后执行 `continue-generate <project_id> --outline-id <outline_id> --no-wait`。下载链接有效期以后端返回 `expires_in` 为准；如需统一为 1 天，后端签发 token 的 TTL 应为 `86400` 秒，skill 只展示该值。

耗时对齐：

- Open API / skill 链路应与网页端使用同一套生成 worker、模型、并发、缓存与模板填充策略。
- 若耗时明显慢于网页端，排查时记录 `job_id`、页数、包号、提交/完成时间和各阶段进度，先定位是否走了降级慢链路。
