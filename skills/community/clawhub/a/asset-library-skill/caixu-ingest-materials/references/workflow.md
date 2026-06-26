# Workflow

## When this skill should trigger

- “把这个目录导入进来”
- “先把这些文件解析成可继续建库的材料”
- “帮我把下载目录里的文件吃进去”

## Input normalization

- 高层输入优先是 `input_root`，不是 `file_paths[]`。
- 如果用户给的是零散文件，也先整理成显式本地路径，再交给 `list_local_files`。
- `library_id` 缺失时先创建/加载库，不要猜已有库。
- `owner_hint` 只有在用户身份明确时才传。

## Route selection

agent 必须逐文件决定 route：

- `text`
- `parser_lite`
- `parser_export`
- `ocr`
- `vlm`
- `skip`

要求：

- `.txt/.md/.json/.csv/.tsv/.yaml/.yml` 优先 `text`
- `pdf/doc/docx/xls/xlsx/ppt/pptx` 优先 `parser_*`
- `png/jpg/jpeg` 走 `ocr` 或 `vlm`
- `zip/mhtml/tif/~$*.docx` 这类低价值或不支持文件应 `skip`

## Sequencing

1. `create_or_load_library`
2. `create_pipeline_run`
3. `list_local_files`
4. agent 逐文件 route decision
5. 调低层工具提取文本
6. `upsert_parsed_files`
7. `complete_pipeline_run`
8. 交给 `build-asset-library`

## What this skill must not do

- 不做 `asset_card` 抽取
- 不做归并
- 不做生命周期判断
- 不做 package/export/submit
- 不跳过 pipeline run 持久化
