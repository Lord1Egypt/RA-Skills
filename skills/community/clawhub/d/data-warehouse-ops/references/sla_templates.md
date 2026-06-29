# SLA 定义模板 (SLA Templates)

## SLA 分级体系

### Tier 定义

| 级别 | 名称 | 新鲜度 | 可用率 | 失败率上限 | 响应时间 | 通知方式 |
|------|------|--------|--------|-----------|----------|----------|
| T1 | 核心 | ≤ 4h | ≥ 99.9% | < 1% | 15 min | PagerDuty + 电话 |
| T2 | 重要 | ≤ 8h | ≥ 99.5% | < 3% | 1h | Slack + 邮件 |
| T3 | 常规 | ≤ 24h | ≥ 99.0% | < 5% | 4h | 邮件 |

### T1 核心管道判定标准
- 直接影响面向客户的产品功能
- CEO/VP 级别日报的数据来源
- 财务报告数据源
- 实时风控/反欺诈数据

### T2 重要管道判定标准
- 内部 BI 报表数据源
- 运营日常决策依赖
- 影响多个下游数据集市
- 监管报送（非实时）

### T3 常规管道判定标准
- 探索性数据分析
- 内部临时报表
- 非紧急的数据同步
- 归档/备份任务

## SLA 配置文件格式

```yaml
# sla_config.yaml
sla_tiers:
  tier_1_critical:
    name: "Tier 1 — 核心管道"
    freshness_hours: 4
    uptime_pct: 99.9
    max_failure_rate_pct: 1.0
    response_time_minutes: 15
    notification_channels: ["pagerduty", "slack_alert", "phone"]
    escalation_policy: "escalation_t1"

  tier_2_important:
    name: "Tier 2 — 重要管道"
    freshness_hours: 8
    uptime_pct: 99.5
    max_failure_rate_pct: 3.0
    response_time_minutes: 60
    notification_channels: ["slack_channel", "email"]
    escalation_policy: "escalation_t2"

  tier_3_normal:
    name: "Tier 3 — 常规管道"
    freshness_hours: 24
    uptime_pct: 99.0
    max_failure_rate_pct: 5.0
    response_time_minutes: 240
    notification_channels: ["email"]
    escalation_policy: "escalation_t3"

pipelines:
  - name: "orders_etl"
    tier: "tier_1_critical"
    schedule: "every 15 minutes"
    expected_duration_minutes: 10
    owners:
      - name: "张三"
        email: "zhangsan@company.com"
      - name: "李四"
        email: "lisi@company.com"
    sla_window:
      start: "00:00"
      end: "23:59"
    dependencies:
      - "raw_orders_sync"
      - "customer_dim_refresh"
    quality_checks:
      - "row_count > 0"
      - "amount_sum within 5% of yesterday"

  - name: "daily_report_etl"
    tier: "tier_2_important"
    schedule: "daily at 02:00"
    expected_duration_minutes: 45
    owners:
      - name: "王五"
        email: "wangwu@company.com"
    sla_window:
      start: "02:00"
      end: "06:00"
    dependencies:
      - "orders_etl"
      - "inventory_etl"

alert_rules:
  freshness_violation:
    description: "数据新鲜度超过 SLA 阈值"
    check: "MAX(updated_at) < NOW() - INTERVAL 'SLA_HOURS hours'"
    action: "notify_owner + create_jira_ticket"

  failure_rate_spike:
    description: "失败率较前 7 天均值上升 > 200%"
    check: "failure_rate_24h > avg_failure_rate_7d * 3"
    action: "notify_owner + page_oncall"

  volume_anomaly:
    description: "数据量变化超过 50%"
    check: "ABS(row_count - avg_7d) / avg_7d > 0.5"
    action: "notify_owner"

  consecutive_failures:
    description: "连续失败超过 3 次"
    check: "consecutive_failed_runs >= 3"
    action: "notify_owner + page_oncall"

notification_channels:
  pagerduty:
    service_key: "${PAGERDUTY_KEY}"
  slack_alert:
    webhook_url: "${SLACK_ALERT_WEBHOOK}"
    channel: "#data-alerts"
  slack_channel:
    webhook_url: "${SLACK_CHANNEL_WEBHOOK}"
    channel: "#data-engineering"
  email:
    smtp_host: "smtp.company.com"
    from: "data-platform@company.com"

escalation_policies:
  escalation_t1:
    steps:
      - delay_minutes: 0
        notify: ["pagerduty"]
      - delay_minutes: 30
        notify: ["phone_primary"]
      - delay_minutes: 60
        notify: ["phone_manager"]
  escalation_t2:
    steps:
      - delay_minutes: 0
        notify: ["slack_channel"]
      - delay_minutes: 60
        notify: ["email", "slack_alert"]
  escalation_t3:
    steps:
      - delay_minutes: 0
        notify: ["email"]
      - delay_minutes: 240
        notify: ["slack_channel"]
```

## SLA 仪表板指标

### 必选 KPI
1. **总体 SLA 合规率** — 满足 SLA 的管道占比
2. **数据新鲜度** — 各管道数据的最新时间戳
3. **管道成功率** — 成功运行次数 / 总运行次数
4. **平均运行时长** — 管道执行耗时趋势
5. **失败分布** — 按管道/时间/失败类型的分布

### 告警规则
```yaml
alerts:
  - name: "核心管道延迟"
    condition: "latest_run > SLA_hours AND tier == 'tier_1_critical'"
    severity: "critical"

  - name: "管道连续失败"
    condition: "consecutive_failures >= 3"
    severity: "critical"

  - name: "数据量异常"
    condition: "volume_change_pct > 50 AND tier in ['tier_1_critical', 'tier_2_important']"
    severity: "warning"

  - name: "运行时长恶化"
    condition: "recent_avg_duration > historical_avg * 2"
    severity: "warning"
```

## 管道运行日志 CSV 格式

```csv
pipeline_name,status,start_time,end_time,duration_sec,rows_processed,error_message
orders_etl,success,2025-06-01 02:00:00,2025-06-01 02:08:30,510,152340,
orders_etl,success,2025-06-01 02:15:00,2025-06-01 02:23:45,525,153201,
orders_etl,failed,2025-06-01 02:30:00,2025-06-01 02:32:10,130,0,Connection timeout
daily_report_etl,success,2025-06-01 02:45:00,2025-06-01 03:20:15,2115,8923401,
```

## SLA 周报模板

```markdown
## 数据管道 SLA 周报 (YYYY-MM-DD ~ YYYY-MM-DD)

### 总体概况
- 管道总数: XX
- SLA 合规率: XX.X% (↑/↓ X.X%)
- 总运行次数: X,XXX
- 失败次数: XX

### 异常事件
| 时间 | 管道 | 类型 | 影响 | 处理状态 |
|------|------|------|------|----------|
| ... | ... | ... | ... | ... |

### 趋势分析
- 本周失败率趋势
- 运行时长的变化
- 数据量增长趋势

### 改进项
1. ...
2. ...
```

## 检查清单

- [ ] 所有管道是否分配了 SLA 级别 (T1/T2/T3)？
- [ ] 是否设置了对应的告警规则和通知渠道？
- [ ] 是否有升级策略（无人响应时的自动上报）？
- [ ] SLA 仪表板是否覆盖了核心 KPI？
- [ ] 是否定期（每周）审查 SLA 合规情况？
- [ ] 管道日志是否规范记录（状态/时间/行数/错误信息）？
- [ ] 是否定义了 SLA 违约的 RCA（根因分析）流程？
