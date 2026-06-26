---
name: feishu-bitable-query
description: Query Feishu Bitable (多维表格) with server-side filter, sort, field selection, and multiple output formats. Activate when querying bitable records with conditions, filtering multidimensional table data, or when data volume is large and client-side filtering is inefficient. Preferred over feishu_bitable_list_records tool when filter expressions or full pagination is needed.
---

# Feishu Bitable Query

Use `scripts/feishu_bitable_query.py` to query Bitable tables with server-side filtering. This avoids pulling all records into context and handles pagination automatically.

## When to Use This Script vs the Built-in Tool

- **Use this script** when: filter conditions are needed, data volume is large (>100 records), need specific output format (TSV/JSONL), or need to pipe results to other scripts
- **Use the built-in tool** (`feishu_bitable_list_records`) when: simple reads, small tables, or no filter needed

## Quick Reference

```bash
SCRIPT="scripts/feishu_bitable_query.py"

# Count records matching a filter
python3 $SCRIPT --app-token APP --table-id TBL --filter 'EXPR' --count

# Query with filter, compact output
python3 $SCRIPT --app-token APP --table-id TBL \
  --filter 'EXPR' \
  --compact-fields '["字段1","字段2"]' \
  --all-pages 2>/dev/null

# Query with view (uses view's built-in filter/sort)
python3 $SCRIPT --app-token APP --table-id TBL --view-id VIEW --all-pages

# TSV output for readability
python3 $SCRIPT --app-token APP --table-id TBL \
  --compact-fields '["描述","状态"]' --format tsv --all-pages 2>/dev/null

# JSONL for piping to other tools
python3 $SCRIPT --app-token APP --table-id TBL --format jsonl --all-pages 2>/dev/null
```

## Key Options

| Option | Description |
|--------|-------------|
| `--filter` | 飞书 filter 表达式 (server-side) |
| `--sort` | Sort expression |
| `--fields` | API 层面只返回指定字段 (JSON array) |
| `--view-id` | 使用视图的筛选排序 |
| `--compact-fields` | 输出时只显示指定字段，自动格式化 (JSON array) |
| `--format` | `json` (default), `jsonl`, `tsv` |
| `--all-pages` | 自动翻页拉取全部 |
| `--count` | 只输出匹配总数 |
| `--include-id` | 输出中包含 record_id |
| `--time-filter` | 本地时间过滤 (可多次), 格式见下方 |
| `--page-size` | 每页条数 1-500, default 500 |

## Filter 两种模式

### 模式 1: 公式语法 `--filter`（GET List API）

```
CurrentValue.[字段名]="值"
AND(CurrentValue.[字段名]="值", CurrentValue.[字段2]="值2")
CurrentValue.[Owner].contains("张三")
```

优点：Link 字段返回完整 text。缺点：日期字段不支持范围比较。

### 模式 2: JSON 结构体 `--filter-json`（POST Search API）

```bash
--filter-json '{
  "conjunction": "and",
  "conditions": [
    {"field_name": "进度 Owner", "operator": "contains", "value": ["ou_xxx"]},
    {"field_name": "结束时间", "operator": "isGreater", "value": ["ExactDate", "1770000000000"]}
  ]
}'
```

支持的 operator: `is`, `isNot`, `contains`, `doesNotContain`, `isEmpty`, `isNotEmpty`, `isGreater`, `isLess`, `isGreaterEqual`, `isLessEqual`

日期字段 value 格式: `["ExactDate", "毫秒时间戳"]`, `["Today"]`, `["TheLastMonth"]`, `["TheNextWeek"]` 等

优点：支持日期范围过滤（服务端）。缺点：DuplexLink 字段不返回 text（只返回 record_id）。

### 选择建议

- **需要 Link 字段文本**（如「所属任务」名称）→ 用 `--filter` + `--time-filter`（本地时间过滤）
- **大量数据只需日期过滤**（不关心 Link 文本）→ 用 `--filter-json`（服务端过滤更高效）
- **两者结合**：先用 `--filter-json` 做粗筛，再用 `--time-filter` 做精细过滤

## Time Filter (本地时间过滤)

飞书 API 不支持对时间戳字段做范围比较，`--time-filter` 在本地过滤（拉取后过滤）。

格式：`字段名:规则`，可多次使用。

```bash
# 前后 N 天
--time-filter '结束时间:14d'

# 未来 N 天
--time-filter '结束时间:14d+'

# 过去 N 天
--time-filter '更新:30d-'

# 晚于/早于指定日期
--time-filter '结束时间:>2026-02-16'
--time-filter '结束时间:<2026-03-16'

# 日期范围
--time-filter '结束时间:2026-02-16~2026-03-16'

# 组合多个时间过滤
--time-filter '结束时间:14d' --time-filter '更新:30d-'
```

## Field Auto-Formatting

`--compact-fields` 自动处理常见字段类型：
- **User 字段**: `[{name: "张三"}]` → `"张三"`
- **时间戳字段** (更新/创建时间/开始时间/结束时间): `1770574521000` → `"2026-02-09"`
- **MultiSelect**: `["opt1", "opt2"]` → `"opt1, opt2"`
- **Link 字段**: `[{text: "xxx"}]` → `"xxx"`

## Piping Pattern

```bash
# Query → filter locally → format
python3 $SCRIPT --app-token APP --table-id TBL \
  --filter 'CurrentValue.[Owner].contains("张三")' \
  --compact-fields '["描述","状态","更新"]' \
  --format jsonl --all-pages 2>/dev/null \
  | python3 -c "
import json,sys
for line in sys.stdin:
    r = json.loads(line)
    if r.get('状态') == '执行中':
        print(f'  - {r[\"描述\"]} ({r[\"更新\"]})')
"
```

## Auth

Script reads credentials from `~/.openclaw/openclaw.json` → `channels.feishu.appId/appSecret` automatically. No manual token needed.

## Stderr vs Stdout

- **stderr**: pagination progress (`Page 1: 500 records...`)
- **stdout**: query results only

Always use `2>/dev/null` when piping to suppress progress output.
