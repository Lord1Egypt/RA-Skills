# ak-data-daily-timeout-report 模板化改造说明

这个模板用于把当前技能包快速改造成其他项目可复用版本。

---

## 1. 你要替换的最小变量

### 业务侧

```text
TENANT_ID=AK Data
JOB_TYPE=AmazonListingJob
```

### 数据表侧

```text
JOB_TABLES=job_a,job_b,job_c,job_d
LOG_TABLES=log_a,log_b,log_c,log_d
```

### 输出侧

```text
RAW_DIR=docs/data/raw
REPORT_DIR=docs/data/reports/custom
```

---

## 2. 你要检查的字段映射

当前默认依赖以下字段：

### job 表字段

- `id`
- `req_ssn`
- `tenant_id`
- `type`
- `status`
- `created_at`
- `break_at`
- `depart_at`
- `arrival_at`
- `deliver_at`
- `payload`

### log 表字段

- `req_ssn`
- `ext_ssn`
- `state`
- `request`

如果目标项目字段名不一致，不要硬搬，直接改脚本 SQL。字段不对，所有统计都是假象。

---

## 3. 你要优先改的脚本点

### `run_created_timeout_report.py`

通常需要检查：

- `build_base_union()` 里的 job 分表名
- market 提取逻辑：`payload.market / payload.country`
- 索引名：`index_created_at_status`
- 主任务正式超时基线：`break_at`

### `run_depart_timeout_report.py`

通常需要检查：

- job 分表名
- depart / arrival 字段是否一致
- market 字段从哪里取

### `run_daily_timeout_report.py`

通常需要检查：

- 每日 JSON 输出路径
- comparison 诊断阈值
- 样例筛选字段命名

### `run_daily_timeout_trend_report.py`

通常需要检查：

- 趋势报告输出路径
- 最差日 / 最优日判定逻辑
- 是否需要额外增加 market 漂移分析

---

## 4. 建议的配置抽离方向

如果以后要通用化，建议把下面这些硬编码进一步抽到配置文件：

```json
{
  "tenantId": "AK Data",
  "jobTables": ["job_a", "job_b", "job_c", "job_d"],
  "logTables": ["log_a", "log_b", "log_c", "log_d"],
  "jobType": "AmazonListingJob",
  "marketExtractPaths": ["$.market", "$.country"],
  "output": {
    "rawDir": "docs/data/raw",
    "reportDir": "docs/data/reports/custom"
  }
}
```

现在没做成全配置化，是为了先保证稳定，不把事情搞成配置地狱。

---

## 5. 迁移后的最小验证清单

迁移后至少跑这三条：

### 单天主流程

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh day \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

### 单天样例追问

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh day \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob \
  --example-scope crawler_timeout \
  --example-type overtime_total \
  --example-market au \
  --example-limit 3
```

### 区间趋势

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh trend \
  --start-date-bjt 2026-04-01 \
  --end-date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

---

## 6. 推荐复制策略

### 只想先用

复制：

- `.pi/skills/ak-data-daily-timeout-report/`
- `scripts/data/run_*timeout*.py`
- `.env` 对应 DB 配置

### 想长期维护

再补：

- `docs/data/ak-data-daily-timeout-report.md`
- `docs/skills-catalog.md`
- `.pi/skills/_catalog.json`

---

## 7. 不建议你现在做的事

- 不要一上来就把所有表名、字段名、规则做成超复杂配置系统
- 不要为了“通用”把 AK Data 的明确口径打散
- 不要把 `break_at` 再退化回 `created_at + timeout_hours`

先能稳定迁移，再谈高度抽象。烂抽象比硬编码更恶心。
