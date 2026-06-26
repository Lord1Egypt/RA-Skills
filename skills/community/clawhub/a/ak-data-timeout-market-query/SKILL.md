---
name: ak-data-timeout-market-query
description: Query timeout status and market timeout ranking for any single job type on huge sharded job tables (job_a~job_d) without index changes.
---

# Skill: ak-data-timeout-market-query

用于查询 **指定租户 + 指定单一任务类型** 的超时表现，输出：

> 说明：本 Skill 主口径是 `created_at + break_at/deliver_at`。若用户明确要求 `depart_at` 口径、6项指标、样例自动补 log 字段，请改走 `ak-data-depart-timeout-log-report`。

- 超时总览（总量、超时量、超时率）
- `market` 超时率排行（从 `payload.market` 提取）
- 超时时长统计（小时）
- 代表性超时样本（req_ssn）

> 适配大表场景（亿级），默认不改索引。

---

## 口径定义（固定）

超时条件：

1. `deliver_at > break_at`
2. 或 `deliver_at IS NULL AND UTC_TIMESTAMP() > break_at`

仅统计 `break_at IS NOT NULL` 可判定样本。

约束：
- `jobType` 必须单值；多类型场景按类型拆分执行（不要混查）。
- 单次 SQL 仅允许单日窗口（24h）。

---

## 自然语言默认规则（新增）

当用户说“最近”但未指定日期时：

- 默认解释为：**最近两天（北京时间）**
- 但仍遵守“最多按天查询”规则：
  - 拆成 2 次单日查询（D-1、D-2）
  - 最后再做汇总展示（不允许跨天一次性 SQL）

示例：当前日期 `2026-03-04`，`最近` => 查询 `2026-03-03` 与 `2026-03-02` 两天。

---

## 输入契约

```json
{
  "tenantId": "AK Data",
  "jobType": "AmazonListingJob",
  "dateBjt": "2026-03-02",
  "queryPreset": "single_day",
  "rangeLimit": "single_day_only",
  "tables": ["job_a", "job_b", "job_c", "job_d"],
  "minMarketSample": 1000
}
```

当用户说“最近”时，转换为：

```json
{
  "tenantId": "AK Data",
  "jobType": "AmazonListingJob",
  "queryPreset": "recent_default",
  "recentDays": 2,
  "datesBjt": ["2026-03-03", "2026-03-02"],
  "rangeLimit": "single_day_only"
}
```

时间换算（北京时间 -> UTC）：
- `start_utc = dateBjt - 8h 00:00:00`
- `end_utc = (dateBjt + 1day) - 8h 00:00:00`
- 强校验：`end_utc - start_utc = 24h`（否则拒绝执行）

---

## 性能策略（必须遵守）

1. 只扫 `job_a~job_d`（不碰 `job` 主表）。
2. **最多按天查询**：单次请求只允许 1 个自然日窗口（24h）。
3. 禁止跨天区间一次性查询；多天需求必须拆成多次单日查询后再汇总。
4. 使用已有时间索引：`FORCE INDEX(index_created_at_status)`。
5. 不在过滤列上套函数（避免索引失效）。
6. 大查询拆为“聚合优先”，明细样本再限量取。

---

## 执行流程

### A) single_day
1. 解析 `dateBjt` -> `start_utc/end_utc`。
2. 执行：
   - 超时总览 SQL
   - market 超时率排行 SQL
   - 超时时长 SQL
   - 限量样本 SQL
3. 输出单日报告。

### B) recent_default（用户仅说“最近”）
1. 计算 `datesBjt=[D-1,D-2]`。
2. 对每个 date 按 A 流程独立执行。
3. 产出：
   - `perDay` 两天分日报告
   - `merged` 两天汇总（在应用层合并，不跨天 SQL）

---

## SQL 模板

### 1) 超时总览（单日）

```sql
SET @tenant_id := 'AK Data';
SET @job_type  := 'AmazonListingJob';
SET @start_utc := '2026-03-01 16:00:00';
SET @end_utc   := '2026-03-02 16:00:00';

SELECT
  SUM(total_cnt) AS total_cnt,
  SUM(timeout_cnt) AS timeout_cnt,
  ROUND(SUM(timeout_cnt) / NULLIF(SUM(total_cnt), 0), 6) AS timeout_rate
FROM (
  SELECT COUNT(*) total_cnt,
         SUM(CASE WHEN break_at IS NOT NULL
                   AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                     OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
                  THEN 1 ELSE 0 END) timeout_cnt
  FROM job_a FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type

  UNION ALL
  SELECT COUNT(*),
         SUM(CASE WHEN break_at IS NOT NULL
                   AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                     OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
                  THEN 1 ELSE 0 END)
  FROM job_b FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type

  UNION ALL
  SELECT COUNT(*),
         SUM(CASE WHEN break_at IS NOT NULL
                   AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                     OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
                  THEN 1 ELSE 0 END)
  FROM job_c FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type

  UNION ALL
  SELECT COUNT(*),
         SUM(CASE WHEN break_at IS NOT NULL
                   AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                     OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
                  THEN 1 ELSE 0 END)
  FROM job_d FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
) t;
```

### 2) market 超时率排行（单日，进一步查询）

```sql
SET @tenant_id := 'AK Data';
SET @job_type  := 'AmazonListingJob';
SET @start_utc := '2026-03-01 16:00:00';
SET @end_utc   := '2026-03-02 16:00:00';
SET @min_sample := 1000;

SELECT
  market,
  SUM(total_cnt) AS total_cnt,
  SUM(timeout_cnt) AS timeout_cnt,
  ROUND(SUM(timeout_cnt)/NULLIF(SUM(total_cnt),0), 6) AS timeout_rate,
  ROUND(SUM(timeout_cnt)/NULLIF(SUM(total_cnt),0)*100, 4) AS timeout_rate_pct,
  SUM(completed_late_cnt) AS completed_late_cnt,
  SUM(unfinished_overtime_cnt) AS unfinished_overtime_cnt
FROM (
  SELECT
    LOWER(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(payload,'$.market')), ''), 'unknown')) AS market,
    COUNT(*) AS total_cnt,
    SUM(CASE WHEN break_at IS NOT NULL
              AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
             THEN 1 ELSE 0 END) AS timeout_cnt,
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NOT NULL AND deliver_at > break_at
             THEN 1 ELSE 0 END) AS completed_late_cnt,
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NULL AND UTC_TIMESTAMP() > break_at
             THEN 1 ELSE 0 END) AS unfinished_overtime_cnt
  FROM job_a FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
  GROUP BY market

  UNION ALL
  SELECT
    LOWER(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(payload,'$.market')), ''), 'unknown')),
    COUNT(*),
    SUM(CASE WHEN break_at IS NOT NULL
              AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NOT NULL AND deliver_at > break_at
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NULL AND UTC_TIMESTAMP() > break_at
             THEN 1 ELSE 0 END)
  FROM job_b FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
  GROUP BY 1

  UNION ALL
  SELECT
    LOWER(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(payload,'$.market')), ''), 'unknown')),
    COUNT(*),
    SUM(CASE WHEN break_at IS NOT NULL
              AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NOT NULL AND deliver_at > break_at
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NULL AND UTC_TIMESTAMP() > break_at
             THEN 1 ELSE 0 END)
  FROM job_c FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
  GROUP BY 1

  UNION ALL
  SELECT
    LOWER(COALESCE(NULLIF(JSON_UNQUOTE(JSON_EXTRACT(payload,'$.market')), ''), 'unknown')),
    COUNT(*),
    SUM(CASE WHEN break_at IS NOT NULL
              AND ((deliver_at IS NOT NULL AND deliver_at > break_at)
                OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NOT NULL AND deliver_at > break_at
             THEN 1 ELSE 0 END),
    SUM(CASE WHEN break_at IS NOT NULL AND deliver_at IS NULL AND UTC_TIMESTAMP() > break_at
             THEN 1 ELSE 0 END)
  FROM job_d FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
  GROUP BY 1
) x
GROUP BY market
HAVING SUM(total_cnt) >= @min_sample
ORDER BY timeout_rate DESC, timeout_cnt DESC;
```

### 3) 超时时长统计（单日）

```sql
SET @tenant_id := 'AK Data';
SET @job_type  := 'AmazonListingJob';
SET @start_utc := '2026-03-01 16:00:00';
SET @end_utc   := '2026-03-02 16:00:00';

SELECT
  COUNT(*) AS timeout_cnt,
  ROUND(AVG(overdue_hours), 4) AS avg_hours,
  ROUND(MAX(overdue_hours), 4) AS max_hours
FROM (
  SELECT TIMESTAMPDIFF(SECOND, break_at, COALESCE(deliver_at, UTC_TIMESTAMP())) / 3600.0 AS overdue_hours
  FROM job_a FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
    AND break_at IS NOT NULL
    AND ((deliver_at IS NOT NULL AND deliver_at > break_at) OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))

  UNION ALL
  SELECT TIMESTAMPDIFF(SECOND, break_at, COALESCE(deliver_at, UTC_TIMESTAMP())) / 3600.0
  FROM job_b FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
    AND break_at IS NOT NULL
    AND ((deliver_at IS NOT NULL AND deliver_at > break_at) OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))

  UNION ALL
  SELECT TIMESTAMPDIFF(SECOND, break_at, COALESCE(deliver_at, UTC_TIMESTAMP())) / 3600.0
  FROM job_c FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
    AND break_at IS NOT NULL
    AND ((deliver_at IS NOT NULL AND deliver_at > break_at) OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))

  UNION ALL
  SELECT TIMESTAMPDIFF(SECOND, break_at, COALESCE(deliver_at, UTC_TIMESTAMP())) / 3600.0
  FROM job_d FORCE INDEX(index_created_at_status)
  WHERE created_at >= @start_utc AND created_at < @end_utc
    AND tenant_id=@tenant_id AND type=@job_type
    AND break_at IS NOT NULL
    AND ((deliver_at IS NOT NULL AND deliver_at > break_at) OR (deliver_at IS NULL AND UTC_TIMESTAMP() > break_at))
) t;
```

---

## 输出契约

### single_day 输出

```json
{
  "scope": {
    "tenantId": "AK Data",
    "jobType": "AmazonListingJob",
    "dateBjt": "2026-03-02",
    "rangeLimit": "single_day_only"
  },
  "summary": {
    "total": 0,
    "timeout": 0,
    "timeoutRate": 0
  },
  "marketRank": [],
  "durationHours": {
    "avg": 0,
    "median": 0,
    "p90": 0,
    "p95": 0,
    "max": 0
  },
  "samples": [],
  "visualization": {
    "charts": [
      "overview pie/bar chart",
      "market top horizontal-bar chart",
      "day trend chart (single_day 可退化为单点)"
    ]
  }
}
```

### recent_default 输出

```json
{
  "scope": {
    "tenantId": "AK Data",
    "jobType": "AmazonListingJob",
    "queryPreset": "recent_default",
    "recentDays": 2,
    "datesBjt": ["2026-03-03", "2026-03-02"]
  },
  "perDay": [
    { "dateBjt": "2026-03-03", "summary": {}, "marketRank": [] },
    { "dateBjt": "2026-03-02", "summary": {}, "marketRank": [] }
  ],
  "merged": {
    "summary": {},
    "marketRank": []
  },
  "visualization": {
    "charts": [
      "overview pie chart",
      "market top horizontal-bar chart",
      "per-day timeout rate line/bar chart"
    ]
  }
}
```

---

## 图表模板（强制，稳定输出）

当产出给 Web Luca 前端时，必须附带 **3 张标准 chart 配置**（正文后用 ```chart 包裹）。

### Chart-1：总览（超时 vs 非超时）

```json
{
  "type": "pie",
  "title": "{jobType} 超时占比（{scopeLabel}）",
  "xAxisKey": "name",
  "data": [
    { "name": "timeout", "value": 355807 },
    { "name": "ontime", "value": 327460 }
  ],
  "series": [
    { "key": "value", "name": "任务量", "color": "#ef4444" },
    { "key": "value", "name": "任务量", "color": "#22c55e" }
  ],
  "summary": [
    { "label": "总任务", "value": 683267 },
    { "label": "超时任务", "value": 355807 },
    { "label": "超时率", "value": "52.07%", "progress": 52.07, "color": "#f59e0b" }
  ],
  "description": "用于快速判断整体风险水平。"
}
```

### Chart-2：market Top 风险（横向条形）

```json
{
  "type": "horizontal-bar",
  "title": "{jobType} Market 超时率 Top10（{scopeLabel}）",
  "xAxisKey": "market",
  "labelKey": "timeout_rate_pct",
  "data": [
    { "market": "uk", "timeout_rate_pct": 86.75, "timeout_cnt": 12345, "total_cnt": 14230 },
    { "market": "de", "timeout_rate_pct": 76.42, "timeout_cnt": 10002, "total_cnt": 13088 }
  ],
  "series": [
    { "key": "timeout_rate_pct", "name": "超时率(%)", "color": "#ef4444" }
  ],
  "summary": [
    { "label": "样本门槛", "value": "min 1000" },
    { "label": "Top1", "value": "uk 86.75%", "progress": 86.75, "color": "#ef4444" }
  ],
  "description": "优先排查前 3 market 的队列积压与上游限流。"
}
```

### Chart-3：分天趋势（最近两天）

```json
{
  "type": "line",
  "title": "{jobType} 分天超时率趋势",
  "xAxisKey": "date",
  "data": [
    { "date": "2026-03-02", "timeout_rate_pct": 46.45, "total_cnt": 341154, "timeout_cnt": 158475 },
    { "date": "2026-03-03", "timeout_rate_pct": 57.68, "total_cnt": 342113, "timeout_cnt": 197332 }
  ],
  "series": [
    { "key": "timeout_rate_pct", "name": "超时率(%)", "color": "#f59e0b" }
  ],
  "summary": [
    { "label": "D-2", "value": "46.45%", "progress": 46.45, "color": "#22c55e" },
    { "label": "D-1", "value": "57.68%", "progress": 57.68, "color": "#ef4444" }
  ],
  "description": "用于识别最近是否恶化；若 D-1 显著上升，优先做小时级热点排查。"
}
```

规则：
1. 单次单一 `jobType`，图里不得混入其他类型。
2. recent_default 必须来自两次单日查询汇总，不得跨天大 SQL。
3. 数值字段保持 number；`summary.value` 可字符串用于展示。
4. 若数据不足（如 market 样本 < 阈值），chart 仍输出，但 `data` 可为空并在 `description` 说明。
5. 文本报告结构固定为：执行范围 -> 核心结论（<=3 条）-> 3 张图 -> 行动建议（P0/P1/P2）。

---

## 失败与降级策略

- 若 JSON 解析 market 失败：归入 `unknown`。
- 若某分表超时/报错：先返回其余分表结果，并在报告显式标注缺失分表。
- 若全量时长分位查询过慢：先返回 `avg/max + 样本`，分位数改离线补算。

---

## 使用提示

- 这是“运营诊断”技能，不做 DDL，不改线上结构。
- 多天查看请走“按天拆分 + 汇总”，不要跨天大 SQL。