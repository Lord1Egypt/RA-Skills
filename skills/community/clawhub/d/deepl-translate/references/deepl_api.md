# DeepL API 参考摘要

本文件基于 2026-03-25 可见的 DeepL 官方文档整理，目标是给 skill 提供一个紧凑的接口导航，而不是完整复制原始文档。

主要参考：

- https://developers.deepl.com/api-reference
- https://developers.deepl.com/api-reference/translate
- https://developers.deepl.com/api-reference/document
- https://developers.deepl.com/api-reference/usage-and-quota/check-usage-and-limits
- https://developers.deepl.com/docs/api-reference/glossaries
- https://github.com/DeepLcom/openapi

## 认证与基础地址

- 认证头：`Authorization: DeepL-Auth-Key <api-key>`
- Pro 基础地址：`https://api.deepl.com`
- Free 基础地址：`https://api-free.deepl.com`

## 当前脚本覆盖的接口

### 文本翻译

- `POST /v2/translate`

常见字段：

- `text`
- `target_lang`
- `source_lang`
- `context`
- `formality`
- `model_type`
- `glossary_id`
- `tag_handling`
- `tag_handling_version`
- `split_sentences`
- `preserve_formatting`
- `outline_detection`
- `show_billed_characters`
- `style_id`
- `custom_instructions`
- `non_splitting_tags`
- `splitting_tags`
- `ignore_tags`

已知限制：

- 最多 50 个 `text`
- 总请求体不超过 128 KiB

### 语言查询

- `GET /v2/languages`

常见查询参数：

- `type=source`
- `type=target`

### 用量查询

- `GET /v2/usage`

常见返回字段：

- `character_count`
- `character_limit`
- `products`
- `api_key_character_count`
- `api_key_character_limit`
- `start_time`
- `end_time`

### 文本润色 / 改写

- `POST /write/rephrase`

常见字段：

- `text`
- `target_lang`
- `writing_style`
- `tone`

说明：

- 更适合同语言变体转换、润色、语气调整。
- 如果只是 `EN-US` 和 `EN-GB` 之间转换，优先考虑这一类接口，而不是 `translate`。

### 文档翻译

- `POST /v2/document`
- `POST /v2/document/{document_id}`
- `POST /v2/document/{document_id}/result`

上传常见字段：

- `file`
- `target_lang`
- `source_lang`
- `filename`
- `formality`
- `glossary_id`
- `output_format`

说明：

- 文档翻译是异步流程。
- 常见格式包括 `docx/doc`、`pptx`、`xlsx`、`pdf`、`txt`、`html`、`xlf/xliff`、`srt`、部分图片格式。
- 输出文件通常要在状态变为 `done` 后再下载。

### Glossary v2

- `GET /v2/glossary-language-pairs`
- `GET /v2/glossaries`
- `POST /v2/glossaries`
- `GET /v2/glossaries/{glossary_id}`
- `GET /v2/glossaries/{glossary_id}/entries`
- `DELETE /v2/glossaries/{glossary_id}`

创建常见字段：

- `name`
- `source_lang`
- `target_lang`
- `entries`
- `entries_format`

说明：

- v2 glossary 面向单语言对。
- v2 glossary 不可原地编辑，通常通过“下载条目、重建、删除旧 glossary”的方式实现更新。

### Glossary v3

- `GET /v3/glossaries`
- `POST /v3/glossaries`
- `GET /v3/glossaries/{glossary_id}`
- `PATCH /v3/glossaries/{glossary_id}`
- `DELETE /v3/glossaries/{glossary_id}`
- `GET /v3/glossaries/{glossary_id}/entries`
- `PUT /v3/glossaries/{glossary_id}/dictionaries`
- `DELETE /v3/glossaries/{glossary_id}/dictionaries`

创建或更新常见字段：

- `name`
- `dictionaries`
- `source_lang`
- `target_lang`
- `entries`
- `entries_format`

说明：

- v3 glossary 支持多语言对，优先级高于 v2。
- `PATCH` 适合改名称或向指定字典合并条目。
- `PUT /dictionaries` 适合整包替换某个语言对字典。
- `DELETE /dictionaries` 适合只删除某个语言对，而不是整个 glossary。

## 响应说明

脚本默认会做两类输出：

- 对翻译类接口，优先输出译文或结果文本
- 对查询类、管理类接口，默认输出 JSON

如果你需要完整原始结构，统一加 `--json`。

## 风险提示

- DeepL 文档与 OpenAPI 规范可能持续演进，新字段未必第一时间覆盖到脚本参数层。
- 某些接口返回结构可能按产品计划、账户类型、beta 状态有所差异。
- 如果某个端点新增字段但脚本还未暴露，可以先用 `perform_request` 现有模式继续扩参。
