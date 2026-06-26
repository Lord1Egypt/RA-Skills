# Tool Contracts

## Tools

- `caixu-data-mcp.create_or_load_library`
- `caixu-data-mcp.create_pipeline_run`
- `caixu-data-mcp.append_pipeline_step`
- `caixu-data-mcp.complete_pipeline_run`
- `caixu-ocr-mcp.list_local_files`
- `caixu-ocr-mcp.read_local_text_file`
- `caixu-ocr-mcp.extract_parser_text`
- `caixu-ocr-mcp.extract_visual_text`
- `caixu-ocr-mcp.render_pdf_pages`
- `caixu-data-mcp.upsert_parsed_files`

## Route decision

agent 输出的 route 只允许：

- `text`
- `parser_lite`
- `parser_export`
- `ocr`
- `vlm`
- `skip`

## ParsedFile normalization boundary

agent 只决定 route；低层工具返回的真实文本、warnings 和失败由 pipeline 归一化成 `ParsedFile`。

- `ParsedFile.provider` 只能来自低层工具真实 provider
- `file_id / file_name / file_path / size_bytes` 必须来自 `list_local_files`
- 不得仅凭文件名构造 `extracted_text`

## Provider values

- `local`
- `zhipu_parser_lite`
- `zhipu_parser_export`
- `zhipu_ocr`
- `zhipu_vlm`
- `hybrid`

## PipelineRun

ingest run 至少要保留：

- `run_type = "ingest"`
- `latest_stage`
- `counts.parsed / failed / warnings / skipped`

每个关键动作至少要追加 step：

- `route_decision`
- `low_level_extract`
- `persist_parsed_files`
