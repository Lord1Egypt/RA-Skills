---
name: bce-bls
description: >
  查询和操作百度智能云日志服务(BLS, Baidu Log Service)。当用户需要以下操作时使用此 skill：
  (1) 查询日志组(Project)列表
  (2) 查询日志集(LogStore)列表或详情
  (3) 查询日志集的索引(Index)配置情况
  (4) 根据用户描述的查询意图，生成 BLS 检索/SQL 查询语句
  (5) 调用 BLS API 检索分析日志并返回结果
  触发关键词：BLS、日志服务、日志查询、LogStore、日志集、检索日志
---

# BLS 日志服务查询

## 前置条件

- **Region**：bj/gz/su/bd/fwh/hkg/nj/yq/cd，必填，用户未提供时主动询问
- **AK/SK**：脚本自动按以下顺序解析，无需手动处理
  1. 命令行参数 `--ak` / `--sk`
  2. 环境变量 `BCE_BLS_ACCESS_KEY` / `BCE_BLS_SECRET_KEY`
  3. 配置文件 `~/.bce_bls/credentials`（INI，`[default]` section）

## 能力清单

所有命令统一前缀：`python3 <skill_path>/scripts/bls_query.py --region <region>`

| 子命令 | 作用 | 关键参数 |
| --- | --- | --- |
| `list-projects` | 列出 Project | `--name` 过滤、`--page-no/--page-size` |
| `list-logstores` | 列出/搜索日志集 | `--project`（可选）、`--logstore-name`（模糊匹配，可跨项目）、分页 |
| `describe-index` | 查看日志集索引配置 | `--logstore`（必填）、`--project`（可选） |
| `query` | 执行检索/SQL 分析 | `--logstore`、`--query`、`--start/--end`（UTC，可省）、`--marker` 翻页 |

## 关键决策规则

**起点选择**（避免无谓调用）：
- 用户**同时给了 project 和日志集名** → 直接进入 `describe-index` / `query`，**跳过** list-logstores。
- 用户只给了**日志集名** → 直接 `list-logstores --logstore-name <name>`，从结果中精确匹配 `logStoreName` 拿到 `project`。**不要**先 list-projects。
- 用户只给了 **project 名**但没给日志集 → 直接 `list-logstores --project <p>`。
- 用户**只想浏览** project 列表 → 才用 list-projects。

**查询语句生成**（必须先 `describe-index` 确认索引状态）：
- 有全文索引 → 关键词搜可用 `match keyword`
- 有字段索引 → 字段过滤可用 `match field:value`，统计可用 SQL
- **无索引** + `@raw` 是 JSON → **优先建议用户去 BLS 控制台为目标字段开启索引**；用户坚持立即查询才用 SQL + `JSON_EXTRACT_SCALAR(\`@raw\`, '$.field')` 兜底（扫描成本高、性能差）
- **无索引** + `@raw` 非 JSON → 无法有效查询，提示用户去 BLS 控制台开启索引
- 过滤后再统计 → 混合 `match ... | select ...`

**查询格式**：
- 关键词搜索 → `match`
- 统计聚合 → SQL（**不要写 FROM 子句**）
- 先过滤后统计 → `match ... | select ...`

**时间处理**：
- API 时间格式必须是 UTC ISO8601（如 `2026-01-10T13:00:00Z`）
- 北京时间需要 **-8h** 转换
- `--start` / `--end` 省略时默认最近 1 小时

**结果展示**：
- SQL 结果 → 表格展示 `columns + rows`
- match 结果 → 展示 `@raw` 原文
- `datasetScanInfo.isTruncated == true` → 提示用户可翻页（`--marker <nextMarker>`），仅 match 支持翻页，SQL 不支持

## 常见查询模板

```sql
-- 关键词搜索
match error
match status=500 and msg:"some keyword"

-- Top N 统计
select uid, count(*) as cnt group by uid order by cnt desc limit 10

-- 时间趋势
select histogram(cast(`@timestamp` as timestamp), interval 1 hour) as hour, count(*) as cnt group by hour order by hour

-- 慢请求
select path, avg(latency) as avg_lat, max(latency) as max_lat, count(*) as cnt group by path order by avg_lat desc limit 10

-- 提取非索引 JSON 字段（兜底方案：无索引时通过 @raw 字段解析；性能差且扫描成本高，
-- 应优先建议用户去 BLS 控制台为该字段开启索引后再用 match/SQL 查询）
select JSON_EXTRACT_SCALAR(`@raw`, '$.field') as f, count(*) as cnt group by f order by cnt desc limit 10

-- 先过滤后统计
match level:error | select caller, count(*) as cnt group by caller order by cnt desc limit 10
```

## 参考文档

- API 参数和响应格式：[references/api_reference.md](references/api_reference.md)
- SQL 函数：[references/sql_syntax.md](references/sql_syntax.md)
- MATCH 语法：[references/match_syntax.md](references/match_syntax.md)
