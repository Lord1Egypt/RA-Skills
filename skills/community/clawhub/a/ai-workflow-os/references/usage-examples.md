# Usage Examples / 使用示例

## New Project / 新项目

User: I want to build a China imported food policy monitoring system.

Flow:

1. Route lifecycle discovery to `project-lifecycle-navigator`.
2. Route official-source research and intake to `web-search-rules`.
3. If formal governance is needed, hand the confirmed intent to `cms-project-governance`.
4. Use `daily-workflow` only when the user explicitly asks to save a checkpoint or handoff.

## File Intake / 文件接入

User: Add these customs documents and inspection reports to the knowledge base.

Flow:

1. Route to `web-search-rules` when available; otherwise use the intake fallback.
2. Classify files by source type and sensitivity.
3. Extract summaries and claim evidence.
4. Mark sensitive or unverified documents as review-required.
5. Stage records in the specialist-owned queue.
6. Ask for confirmation before permanent archive or cloud upload.

## Web + Files Synthesis / 网页 + 文件综合分析

User: Compare the latest regulation pages with my uploaded label documents.

Flow:

1. Use `web-search-rules` to search, open, and verify current regulation pages.
2. Extract uploaded file content.
3. Normalize records.
4. Compare facts, dates, conflicts, and compliance gaps.
5. Output supported findings, conflicts, `cannot-confirm` gaps, and next actions.

## Wrap Up / 收工

User: Save progress and prepare handoff.

Flow:

1. Route the explicit persistence request to `daily-workflow`.
2. Preserve project governance and coding-loop evidence.
3. Update only the project-owned memory files and create a self-contained handoff.
