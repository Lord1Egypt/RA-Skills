---
name: ak-data-daily-timeout-report
description: "Unified daily timeout entry for AK Data single job type: task timeout + crawler timeout + comparison + drill-down examples with log request."
---

# Skill: ak-data-daily-timeout-report

> 可迁移入口脚本：`./run.sh`
>
> - 单天查询：`./run.sh day ...`
> - 趋势查询：`./run.sh trend ...`
> - 迁移说明：`./MIGRATION.md`
> - 模板说明：`./TEMPLATE.md`
> - 短命令包装：项目根目录 `bin/timeout`
> - 打包脚本：`scripts/data/package_ak-data_daily_timeout_skill.py`

统一入口：用于查询 **AK Data 单任务类型** 在某一天的：

1. **主任务超时**（task timeout）
2. **爬虫超时**（crawler timeout）
3. **两种口径对比结论**
4. **支持继续追问具体任务例子**（自动补齐 log `ext_ssn + log_state + request`）

> 这是入口 Skill，不直接替代底层统计逻辑。
>
> - 主任务超时底层能力：`ak-data-task-timeout-created-report`
> - 爬虫超时底层能力：`ak-data-depart-timeout-log-report`
>
> 本 Skill 负责：**统一调度、统一输出、统一追问接口**。

---

## 快速使用

### 1) 单天联合超时

```bash
./run.sh day --date-bjt 2026-04-05 --job-type AmazonListingJob
```

### 2) 单天 + 样例追问

```bash
./run.sh day \
  --date-bjt 2026-04-05 \
  --job-type AmazonListingJob \
  --example-scope crawler_timeout \
  --example-type overtime_total \
  --example-market au \
  --example-limit 5
```

### 3) 区间趋势

```bash
./run.sh trend \
  --start-date-bjt 2026-04-01 \
  --end-date-bjt 2026-04-05 \
  --job-type AmazonListingJob
```

## 适用场景

当 LeeHoo 的问题是以下类型时，优先使用本 Skill：

- “查 4.5 超时情况”
- “查 4.5 主任务超时和爬虫超时对比”
- “查某天 AmazonListingJob 的超时情况”
- “给我几个超时例子，带 request”
- “继续看 4.5 的 nl / jp / au 样例”
- “导出未Deliver / 未Arrival / WAITING 样例”

---

## 口径边界（强制）

### 1) 主任务超时（task timeout）

- 时间窗口：`created_at` 落在 `dateBjt` 对应自然日
- **正式超时判定基线：`break_at`**
- 不得把主任务超时偷换成 `depart_at` 口径
- 不得把主任务超时简化成固定 `created_at + 12h` 口径后对外宣称“正式口径”

### 2) 爬虫超时（crawler timeout）

- 时间窗口：`depart_at` 落在 `dateBjt` 对应自然日
- 超时判定：
  - 已到达：`arrival_at - depart_at > timeoutHours`
  - 未到达：`now_utc - depart_at > timeoutHours`
- 若查询日是当天，可启用 `cutoffHours` 做成熟母本截断

### 3) 追问具体任务例子

例子查询必须能区分：

- `scopeType = task_timeout`
- `scopeType = crawler_timeout`

不得混口径返回。

---

## 输入契约

```json
{
  "tenantId": "AK Data",
  "jobType": "AmazonListingJob",
  "dateBjt": "2026-04-05",
  "includeTaskTimeout": true,
  "includeCrawlerTimeout": true,
  "samplePerState": 3,
  "needMarketSplit": true,
  "needLogEnrich": true,
  "cutoffHours": 0,
  "exampleQuery": {
    "scopeType": "crawler_timeout",
    "sampleType": "overtime_total",
    "market": "au",
    "status": "PENDING",
    "limit": 5,
    "includeRequest": true
  }
}
```

### 字段说明

- `includeTaskTimeout`：是否生成主任务超时部分
- `includeCrawlerTimeout`：是否生成爬虫超时部分
- `samplePerState`：底层脚本每类抽样条数
- `needLogEnrich`：是否自动补齐 log 字段
- `cutoffHours`：仅爬虫口径支持；用于当日成熟母本截断
- `exampleQuery`：可选，用于继续追问例子

---

## 标准执行流程（强制）

### A. 每日总览查询

1. 如果 `includeTaskTimeout=true`
   - 调用 `run_created_timeout_report.py`
   - 读取输出 JSON
2. 如果 `includeCrawlerTimeout=true`
   - 调用 `run_depart_timeout_report.py`
   - 读取输出 JSON
3. 生成 unified report：
   - 总览
   - market 对比
   - 主任务 vs 爬虫差值
   - 诊断结论

### B. 对比诊断规则

至少输出：

- 主任务超时率
- 爬虫超时率
- gap（百分点）
- top market 重合情况
- 结论

#### 建议判定规则

- 若两者超时率差值 `< 1 pct`
  - 判定：**基本贴脸一致，问题主要由 crawler 链路传导**
- 若主任务明显高于爬虫 `> 2 pct`
  - 判定：**deliver / 状态收口尾段可能存在额外拖后腿**
- 若 top risk market 高度重合
  - 判定：**风险源一致**
- 若主任务新增 crawler 不明显的 market
  - 判定：**后链路异常需单独下钻**

### C. 追问例子（drill-down）

当用户继续问“给几个例子”时：

1. 优先复用对应 JSON 中的 `samples`
2. 若用户指定过滤维度（market/status/sampleType），则从标准化样例集合中过滤
3. 若默认样例不足，再调用底层脚本增强抽样能力或补充专用导出脚本

默认要补齐的字段：

- `req_ssn`
- `source_table`
- `log_table`
- `market`
- `status`
- `created_at / depart_at / arrival_at / deliver_at`
- `task_hours / crawl_hours`
- `ext_ssn`
- `log_state`
- `request`
- `request_truncated`

---

## 输出契约

```json
{
  "scope": {
    "tenantId": "AK Data",
    "jobType": "AmazonListingJob",
    "dateBjt": "2026-04-05"
  },
  "taskTimeout": {
    "baseline": "break_at",
    "generatedAtUtc": "2026-04-06 08:00:00",
    "total": {},
    "markets": [],
    "samples": {}
  },
  "crawlerTimeout": {
    "baseline": "depart_at",
    "generatedAtUtc": "2026-04-06 08:00:00",
    "total": {},
    "markets": [],
    "samples": {}
  },
  "comparison": {
    "taskTimeoutRate": 0.087,
    "crawlerTimeoutRate": 0.0854,
    "gapPct": 0.16,
    "topOverlapMarkets": ["nl", "jp", "pl"],
    "diagnosis": "主任务超时与爬虫超时基本贴脸一致，说明问题主要由 crawler 链路传导"
  },
  "exampleQueryResult": {
    "scopeType": "crawler_timeout",
    "sampleType": "overtime_total",
    "market": "au",
    "status": "PENDING",
    "limit": 5,
    "rows": []
  }
}
```

---

## 输出文案要求（对话）

对 LeeHoo 汇报时，建议固定结构：

1. **执行范围**
2. **总览指标**
3. **主任务 vs 爬虫差值**
4. **Top market / 高风险 market**
5. **诊断结论**
6. **如用户要求，补具体样例（带 request）**
7. **最后给出文件路径**

---

## 风险与降级

- 若某一底层报告失败：
  - 返回另一部分成功结果
  - 明确标记 `partial=true`
- 若 log 缺失：
  - 保留主记录
  - `log_found=false`
- 若 `request` 非法 JSON：
  - 返回原文字符串
  - `request_parse_error=true`
- 若 sample 不足：
  - 明确提示“默认样例不足，当前仅返回已有样例”

---

## 结论型经验（已沉淀）

- LeeHoo 对该类问题的真实诉求不是单一口径，而是：
  - **某天总体超时怎样**
  - **主任务超时与爬虫超时是否贴脸一致**
  - **是否属于 crawler 传导，而不是 deliver 尾段独立炸锅**
  - **继续追问具体任务例子，并看 request 字段**
- 因此统一入口 Skill 比两个分散 Skill 更适合作为对话层默认路由。
