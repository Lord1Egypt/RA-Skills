# Usage Examples / 使用示例

## New Project / 新项目

User: I want to build a China imported food policy monitoring system.

Flow:

1. Project Lifecycle: define objective, scope, data sources, and MVP.
2. Knowledge Intake Governance: define official sources, source trust levels, staging and archive rules.
3. Project Memory: save PROJECT, TARGET, STATUS, PENDING, NEXT_ACTIONS.

## File Intake / 文件接入

User: Add these customs documents and inspection reports to the knowledge base.

Flow:

1. Classify files by source type and sensitivity.
2. Extract summaries and key facts.
3. Mark sensitive documents as review-required.
4. Stage records in RESEARCH_QUEUE.
5. Ask for confirmation before permanent archive or cloud upload.

## Web + Files Synthesis / 网页 + 文件综合分析

User: Compare the latest regulation pages with my uploaded label documents.

Flow:

1. Search or read current regulation pages.
2. Extract uploaded file content.
3. Normalize records.
4. Compare facts, dates, conflicts, and compliance gaps.
5. Output confirmed findings and next actions.

## Wrap Up / 收工

User: Save progress and prepare handoff.

Flow:

1. Update STATUS, COMPLETED, PENDING, NEXT_ACTIONS.
2. Archive old status if needed.
3. Create HANDOFF summary.
