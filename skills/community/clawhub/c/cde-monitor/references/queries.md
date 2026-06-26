# Queries

## Supported commands

### breakthrough-announcements

Returns all pages from:

- 信息公开
- 突破性治疗公示
- 拟突破性治疗品种

### breakthrough-included-by-company

Returns filtered results from:

- 信息公开
- 突破性治疗公示
- 纳入突破性治疗品种名单
- Filter: 注册申请人

Command:

```bash
python ./scripts/cde_query.py breakthrough-included-by-company --company "示例公司"
```

### breakthrough-included-by-drug

Returns filtered results from:

- 信息公开
- 突破性治疗公示
- 纳入突破性治疗品种名单
- Filter: 药品名称

Command:

```bash
python ./scripts/cde_query.py breakthrough-included-by-drug --drug "示例药物"
```

### priority-announcements

Returns all pages from:

- 信息公开
- 优先审评公示
- 拟优先审评品种公示

### priority-included-by-company

Returns filtered results from:

- 信息公开
- 优先审评公示
- 纳入优先审评品种名单
- Filter: 注册申请人

### priority-included-by-drug

Returns filtered results from:

- 信息公开
- 优先审评公示
- 纳入优先审评品种名单
- Filter: 药品名称

Command:

```bash
python ./scripts/cde_query.py priority-included-by-drug --drug "示例药物"
```

### in-review-by-company

Returns merged results across the requested years from:

- 信息公开
- 受理品种信息
- 在审品种目录浏览
- Filters: 年度, 企业名称

### in-review-by-drug

Returns merged results across the requested years from:

- 信息公开
- 受理品种信息
- 在审品种目录浏览
- Filters: 年度, 药品名称

## Output shape

The Python CLI still returns structured JSON by default, but the skill should present final user-facing results as Markdown tables.

Recommended answer pattern:

```md
查询条件：`示例公司`
查询范围：`信息公开 > 受理品种信息 > 在审品种目录浏览`
结果汇总：`共 42 条，3 页，年份 2016 至 2026`

| 序号 | 药品名称 | 企业名称 | 受理号 | 年份 |
|---|---|---|---|---|
| 1 | 示例药物A | 示例公司 | CXHS250001 | 2025 |
| 2 | 示例药物B | 示例公司 | CXHS260002 | 2026 |
```

Underlying data fields available to the skill:

- `records[].normalized.drug_name`
- `records[].normalized.company_name`
- `records[].normalized.acceptance_no`
- `records[].normalized.publication_title`
- `records[].normalized.year`
- `records[].normalized.source_menu`
- `records[].normalized.source_tab`
- `records[].normalized.page`
- `metadata.applied_filters`
- `metadata.pages_visited`
- `metadata.years_queried`
- `metadata.total_records`

## Notes for agents

- Use `--max-pages` only for debugging or validation. The default behavior is to keep paginating until the available result set is exhausted or a repeated page fingerprint is observed.
- Use `normalized` fields when composing the answer.
- Keep `raw` only as a fallback when a page uses an unexpected field name.
- Prefer Markdown tables in the final answer whenever records are returned.
- If the user asks for a company-specific or drug-specific query and the name could be ambiguous, confirm the exact string before running the command.
