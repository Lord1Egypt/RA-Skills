---
name: caixu-ingest-materials
description: "Import Personal Documents. Use when the user wants to import a local directory or explicit files into 材序 at the ingest stage, including “导入一批材料”“先把这个目录吃进去”“先建立可继续建库的解析上下文”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill creates or loads a library, starts an ingest pipeline run, lets the agent choose per-file routes over low-level OCR and parser tools, persists ParsedFile records, and hands off library_id plus run_id to build-asset-library. Do not use it for asset extraction, lifecycle judgment, package building, or submission."
---

# Import Personal Documents

在用户要“导入一批材料”“先把这个目录吃进去”“先建立可继续建库的解析上下文”时使用这个 skill。

## Quick flow

1. 创建或加载 `library_id`，再创建 `ingest` pipeline run
2. 调 `list_local_files`，让 agent 为每个文件选择 route
3. 调低层工具提取文本，归一化成 `ParsedFile`，写入 `upsert_parsed_files`

## Read next only when needed

- 输入是目录、混合格式、需要 route 判断时，读 [references/workflow.md](references/workflow.md)
- 需要确认低层工具输入输出、route 含义或 `PipelineRun` 结构时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 需要最小 JSON 输出模板时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到 route 决策失败、部分文件失败或写库失败时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.create_or_load_library`
- `caixu-data-mcp.create_pipeline_run`
- `caixu-ocr-mcp.list_local_files`
- `caixu-ocr-mcp.read_local_text_file`
- `caixu-ocr-mcp.extract_parser_text`
- `caixu-ocr-mcp.extract_visual_text`
- `caixu-ocr-mcp.render_pdf_pages`
- `caixu-data-mcp.upsert_parsed_files`
- `caixu-data-mcp.append_pipeline_step`
- `caixu-data-mcp.complete_pipeline_run`

## Required input

- `input_root` or explicit local files
- `library_id?`
- `owner_hint?`

## Workflow

1. 如果上下文里没有 `library_id`，先调 `create_or_load_library`。
2. 创建 `ingest` run；之后每个关键动作都要追加 step。
3. 先用 `list_local_files` 展开目录，再让 agent 为每个文件选择 `text | parser_lite | parser_export | ocr | vlm | skip`。
4. 只调低层工具，不自己做 OCR/Parser 大一统封装。
5. 把成功结果归一化成 `ParsedFile`，再统一写入 `upsert_parsed_files`。
6. 结束时完成 pipeline run，并返回单个 `ToolResult` 风格结果，至少包含：
   - `data.library_id`
   - `data.run_id`
   - `data.file_ids`
   - `data.parsed_count`
   - `data.failed_count`
   - `data.warning_count`
   - `data.skipped_count`
   - `data.parsed_files`
   - `data.failed_files`
   - `data.warning_files`
   - `data.skipped_files`
7. 成功或部分成功时，推荐下一步 `build-asset-library`。

## Guardrails

- 不要发明文件内容、OCR 结果、issuer、date 或任何资产字段。
- 不要把目录路径直接当文件列表使用；必须先 `list_local_files`。
- 这是 ingest skill，不负责 `asset_card` 抽取、归并、生命周期判断、打包或提交。
- 单文件失败不能阻断成功文件；但 route 决策失败必须明确记 step 与结构化错误。
- 如果 route 决策连续失败，允许 pipeline 保守回退到 `suggested_route`，但必须留下 step 和 warning。
- 低价值或不支持格式应走 `skip`，不要硬塞进 parser/OCR。
- 如果低层提取成功但 `upsert_parsed_files` 失败，返回结构化存储错误，并停止推荐下一步。
