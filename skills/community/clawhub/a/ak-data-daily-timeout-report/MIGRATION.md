# ak-data-daily-timeout-report 迁移说明

## 目的

把 AK Data 每日超时能力作为一个 **可迁移技能包** 使用。

该技能包覆盖：

- 单天主任务超时 + 爬虫超时联合查询
- 日期区间趋势汇总
- 继续追问具体任务样例（支持 log request）

---

## 先回答一个关键问题

### 迁移会不会把 Python 脚本一起带走？

**会，而且必须一起迁移。**

这个 skill 不是纯文档型 skill，它的实际执行依赖下面这些 Python 脚本：

```text
scripts/data/run_created_timeout_report.py
scripts/data/run_depart_timeout_report.py
scripts/data/run_daily_timeout_report.py
scripts/data/run_daily_timeout_trend_report.py
```

只迁移 `.pi/skills/ak-data-daily-timeout-report/` 目录是不够的，那样只剩说明书和壳，跑不起来。

如果你想一把打包走，可以使用：

```bash
python3 scripts/data/package_ak-data_daily_timeout_skill.py
```

默认输出：

```text
dist/ak-data-daily-timeout-report.bundle.tgz
```

## 最小迁移清单

迁移到新项目时，至少复制以下文件：

### Skill 层

```text
.pi/skills/ak-data-daily-timeout-report/SKILL.md
.pi/skills/ak-data-daily-timeout-report/run.sh
.pi/skills/ak-data-daily-timeout-report/MIGRATION.md
.pi/skills/ak-data-task-timeout-created-report/SKILL.md
.pi/skills/ak-data-depart-timeout-log-report/SKILL.md
```

### 执行脚本层（必须一起迁移）

```text
scripts/data/run_created_timeout_report.py
scripts/data/run_depart_timeout_report.py
scripts/data/run_daily_timeout_report.py
scripts/data/run_daily_timeout_trend_report.py
```

### 配置（推荐一起迁移）

```text
configs/skills/ak-data-daily-timeout-report.json
```

> 当前版本已经预留配置文件，但底层 Python 脚本还没有完全做到“全配置驱动”。
> 也就是说：配置文件是迁移辅助，不是魔法。目标项目表结构变了，还是要改脚本。

### 文档（推荐）

```text
docs/data/ak-data-daily-timeout-report.md
```

---

## 环境依赖

### Python

建议 Python 3.10+

### 依赖包

至少需要：

```bash
pip install pymysql
```

### 配置文件

默认配置文件：

```text
configs/skills/ak-data-daily-timeout-report.json
```

最少需要确认：

- `tenantId`
- `jobTables`
- `logTablePrefix`
- `marketExtractPaths`
- `output.rawDir`
- `output.reportDir`

### 环境变量

需要在项目 `.env` 中提供：

```env
ANKER_JOB_DB_HOST=xxx
ANKER_JOB_DB_PORT=3306
ANKER_JOB_DB_USER=xxx
ANKER_JOB_DB_PASSWORD=xxx
ANKER_JOB_DB_NAME=collector
ANKER_JOB_DB_CHARSET=utf8mb4
```

---

## 使用方式

### 0. 解压后先改配置

先修改：

```text
configs/skills/ak-data-daily-timeout-report.json
```

再确认项目根目录 `.env` 中数据库连接可用；bundle 内会附带 `.env.example` 作为填写模板。

### 1. 单天联合查询

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh day \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

### 2. 单天 + 样例追问

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh day \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob \
  --example-scope crawler_timeout \
  --example-type overtime_total \
  --example-market au \
  --example-limit 5
```

### 3. 区间趋势

```bash
.pi/skills/ak-data-daily-timeout-report/run.sh trend \
  --start-date-bjt 2026-04-01 \
  --end-date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

---

## 测试方法（强制建议按顺序跑）

### 测试 1：看帮助

```bash
./bin/timeout
```

预期：输出 day / trend 两种用法说明。

### 测试 2：单天主流程

```bash
./bin/timeout day \
  --config configs/skills/ak-data-daily-timeout-report.json \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

预期：生成单天 JSON + Markdown。

### 测试 3：单天样例追问

```bash
./bin/timeout day \
  --config configs/skills/ak-data-daily-timeout-report.json \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob \
  --example-scope crawler_timeout \
  --example-type overtime_total \
  --example-market au \
  --example-limit 3
```

预期：输出 JSON 中 `exampleQueryResult.rows` 非空或明确返回空样例，但命令能正常完成。

### 测试 4：区间趋势

```bash
./bin/timeout trend \
  --config configs/skills/ak-data-daily-timeout-report.json \
  --start-date-bjt 2026-04-01 \
  --end-date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

预期：生成趋势 JSON + Markdown。

### 测试 5：打包迁移包

```bash
python3 scripts/data/package_ak-data_daily_timeout_skill.py
```

预期：生成：

```text
dist/ak-data-daily-timeout-report.bundle.tgz
```

## 输出路径

### 单天

```text
docs/data/raw/ak-data_daily_timeout_<date>_<jobType>.json
docs/data/reports/custom/ak-data_daily_timeout_<date>_<jobType>.md
```

### 趋势

```text
docs/data/raw/ak-data_daily_timeout_trend_<start>_to_<end>_<jobType>.json
docs/data/reports/custom/ak-data_daily_timeout_trend_<start>_to_<end>_<jobType>.md
```

---

## 迁移注意事项

### 1. 主任务超时口径

- 日窗：`created_at`
- 正式判定：`break_at`

不要再退回到 `created_at + 12h` 的伪口径。

### 2. 爬虫超时口径

- 日窗：`depart_at`
- 判定：`arrival_at - depart_at`

### 3. request 字段

样例支持自动带 log `request`，但前提是：

- 对应 `log_a ~ log_d` 表存在
- `req_ssn` 能关联上

---

## 推荐迁移方式

如果目标项目目录结构兼容当前仓库，直接复制上述文件即可。

如果目录结构不同，优先修改：

- `.pi/skills/ak-data-daily-timeout-report/run.sh`

其中：

- `ROOT_DIR` 的相对路径推导可能需要调整。

这是唯一最容易因为目录层级变化而坏掉的地方。
