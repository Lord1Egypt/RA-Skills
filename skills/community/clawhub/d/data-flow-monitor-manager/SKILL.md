---
name: data-flow-monitor-manager
description: 跨租户数据流监控管理器,数据流图+异常流告警+三级阈值+Prometheus 4项安全指标+每日泄露扫描。触发:数据流监控/泄露扫描/跨租户检测/data-flow/leakage-scan
tools:
  - record_data_flow
  - get_data_flow_graph
  - detect_anomaly_flow
  - get_security_metrics
  - run_leakage_scan
  - get_leakage_alerts
  - set_flow_threshold
  - healthcheck
dependencies: []
metadata:
  layer: infrastructure
  priority: "P0"
  bins: []
  env:
    - PG_DSN
    - PROMETHEUS_URL
  config:
    - config/data_flow_thresholds.yaml
  os: [linux, windows]
---

# data-flow-monitor-manager

跨租户数据流监控管理器。基于v8.0多租户任务编排方案§五SEC-2,实现跨租户数据流监控、数据流图构建、异常流告警、三级阈值(频率/数据量/敏感度)、Prometheus 4项安全指标导出、每日数据泄露扫描。

## 使用场景

1. **跨租户数据流实时监控**: agency-portal-mcp数据流跟踪+rls-guard-mcp违规事件接入,记录每条数据流事件
2. **数据流图可视化**: 自动构建租户间数据流向图(MCP调用链+API调用+DB查询),输出节点+边JSON
3. **异常数据流告警**: 检测跨租户访问/异常大批量导出/非工作时间访问/敏感凭证访问,自动分级L1/L2/L3
4. **三级阈值动态调整**: 频率(100/500次每小时)、数据量(1GB/10GB每日)、敏感度(normal/pii/credential)
5. **Prometheus 4项安全指标**: cross_tenant_access_total/data_export_bytes/anomaly_flow_alerts/leakage_events
6. **每日数据泄露扫描**: 每日凌晨3点扫描所有租户访问日志,检测4种泄露模式,自动创建leakage_alerts
7. **泄露告警历史追溯**: 查询leakage_alerts表追溯历史告警,支持按租户/类型/severity/状态过滤

## 工作流

1. 初始化(健康检查)
   - 执行: `mcp__data-flow-monitor-mcp__healthcheck`
   - 验证: 连接池+阈值配置+data_flow_events/leakage_alerts表+Docker+Gateway状态
   - 检查点: status==healthy或degraded(允许降级,不允许unhealthy)

2. 数据流事件记录(生产链路)
   - 执行: `mcp__data-flow-monitor-mcp__record_data_flow(source_tenant, target_tenant, data_type, volume, flow_type, metadata)`
   - 自动分级: 根据data_type/volume/frequency计算severity(L1/L2/L3)
   - 检查点: L3或跨租户L2自动创建leakage_alert

3. 数据流图查询
   - 执行: `mcp__data-flow-monitor-mcp__get_data_flow_graph(tenant_id, hours, min_severity)`
   - 输出: 节点(nodes)+边(edges),支持按租户/时间窗口/severity过滤
   - 检查点: 返回node_count和edge_count

4. 异常数据流检测
   - 执行: `mcp__data-flow-monitor-mcp__detect_anomaly_flow(hours, tenant_id)`
   - 检测4类: cross_tenant_access/abnormal_export/off_hours_access/sensitive_data_access
   - 检查点: 返回anomalies列表+severity_counts

5. Prometheus安全指标获取
   - 执行: `mcp__data-flow-monitor-mcp__get_security_metrics(hours)`
   - 4项指标: cross_tenant_access_total/data_export_bytes/anomaly_flow_alerts/leakage_events
   - 检查点: 返回metrics数组+tenant_distribution

6. 每日泄露扫描(Cron触发)
   - 执行: `mcp__data-flow-monitor-mcp__run_leakage_scan(days, tenant_id)`
   - 4种模式: cross_tenant_query/bulk_export/credential_access/off_hours_access
   - 检查点: L2/L3 finding自动创建leakage_alert(去重)

7. 泄露告警历史查询
   - 执行: `mcp__data-flow-monitor-mcp__get_leakage_alerts(tenant_id, alert_type, severity, status, limit)`
   - 检查点: 返回alerts列表+severity_summary+status_summary

8. 三级阈值动态调整
   - 执行: `mcp__data-flow-monitor-mcp__set_flow_threshold(threshold_type, level, value, data_types)`
   - 类型: frequency(频率)/volume(数据量)/sensitivity(敏感度)
   - 检查点: 返回old_value和new_value,配置原子写入

## 输入格式

| 工具 | 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|:-----|
| record_data_flow | source_tenant | str | 是 | 源租户ID |
| record_data_flow | target_tenant | str | 是 | 目标租户ID |
| record_data_flow | data_type | str | 否 | 数据类型(默认normal) |
| record_data_flow | volume | int | 否 | 数据量字节(默认0) |
| record_data_flow | flow_type | str | 否 | 流类型query/export/api_call/db_query |
| record_data_flow | metadata | str | 否 | JSON字符串元数据 |
| get_data_flow_graph | tenant_id | str | 否 | 过滤特定租户 |
| get_data_flow_graph | hours | int | 否 | 时间窗口,默认24 |
| get_data_flow_graph | min_severity | str | 否 | 最低severity,默认L1 |
| detect_anomaly_flow | hours | int | 否 | 检测窗口,默认1 |
| detect_anomaly_flow | tenant_id | str | 否 | 过滤特定租户 |
| get_security_metrics | hours | int | 否 | 时间窗口,默认24 |
| run_leakage_scan | days | int | 否 | 扫描天数,默认1 |
| run_leakage_scan | tenant_id | str | 否 | 过滤特定租户 |
| get_leakage_alerts | tenant_id | str | 否 | 按租户过滤 |
| get_leakage_alerts | alert_type | str | 否 | 按类型过滤 |
| get_leakage_alerts | severity | str | 否 | L1/L2/L3 |
| get_leakage_alerts | status | str | 否 | open/resolved/false_positive |
| get_leakage_alerts | limit | int | 否 | 默认100,最大1000 |
| set_flow_threshold | threshold_type | str | 是 | frequency/volume/sensitivity |
| set_flow_threshold | level | str | 是 | L1/L2/L3 |
| set_flow_threshold | value | int | 是 | 阈值(frequency=次/小时,volume=字节) |
| set_flow_threshold | data_types | str | 否 | sensitivity时逗号分隔类型 |

## 输出格式

所有工具统一返回:
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "code": "FLOW_RECORDED"
}
```

错误时:
```json
{
  "success": false,
  "data": {},
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

## 异常处理

1. **连接池不可用**: 返回 code=NO_DRIVER, error="psycopg2未安装" → 安装psycopg2-binary
2. **参数缺失**: 返回 code=PARAMS_REQUIRED, error="source_tenant和target_tenant必填" → 补全参数
3. **标识符不合法**: 返回 code=INVALID_PARAM → 检查tenant_id格式(字母/数字/下划线/连字符)
4. **severity非法**: 返回 code=INVALID_SEVERITY → 使用L1/L2/L3
5. **阈值类型非法**: 返回 code=INVALID_TYPE → 使用frequency/volume/sensitivity
6. **配置文件错误**: 返回 code=CONFIG_INVALID → 检查config/data_flow_thresholds.yaml
7. **健康检查失败**: 返回 code=HEALTHCHECK_ERROR → 检查Docker/Gateway/PG连接/表存在
8. **L3数据流阻断**: record_data_flow返回blocked=true → 审查数据流是否合规

## 示例

### 示例1: 记录跨租户数据流
```
mcp__data-flow-monitor-mcp__record_data_flow(
  source_tenant="tenant_001",
  target_tenant="tenant_002",
  data_type="pii",
  volume=5242880,
  flow_type="api_call",
  metadata='{"endpoint":"/api/export"}'
)
```
输出:
```json
{
  "success": true,
  "data": {
    "event_id": 101,
    "source_tenant": "tenant_001",
    "target_tenant": "tenant_002",
    "data_type": "pii",
    "volume": 5242880,
    "flow_type": "api_call",
    "severity": "L2",
    "blocked": false,
    "cross_tenant": true,
    "alert_id": 55,
    "timestamp": "2026-07-07 10:30:00+08:00"
  },
  "error": null,
  "code": "FLOW_RECORDED"
}
```

### 示例2: 获取24小时数据流图
```
mcp__data-flow-monitor-mcp__get_data_flow_graph(tenant_id="", hours=24, min_severity="L2")
```
输出:
```json
{
  "success": true,
  "data": {
    "nodes": [{"id": "tenant_001", "label": "tenant_001"}, {"id": "tenant_002", "label": "tenant_002"}],
    "edges": [{"source": "tenant_001", "target": "tenant_002", "data_type": "pii", "severity": "L2", "event_count": 5, "total_volume": 26214400, "blocked": false}],
    "node_count": 2,
    "edge_count": 1,
    "hours": 24,
    "min_severity": "L2"
  },
  "error": null,
  "code": "GRAPH_OK"
}
```

### 示例3: 获取Prometheus 4项安全指标
```
mcp__data-flow-monitor-mcp__get_security_metrics(hours=24)
```
输出:
```json
{
  "success": true,
  "data": {
    "metrics": [
      {"name": "cross_tenant_access_total", "type": "counter", "value": 42, "description": "跨租户数据访问总次数"},
      {"name": "data_export_bytes", "type": "counter", "value": 5368709120, "description": "数据导出字节数"},
      {"name": "anomaly_flow_alerts", "type": "counter", "value": 8, "description": "异常数据流告警数"},
      {"name": "leakage_events", "type": "gauge", "value": 2, "description": "数据泄露事件数(severity=L3)"}
    ],
    "hours": 24
  },
  "error": null,
  "code": "METRICS_OK"
}
```

## 来源标注

- **v8.0多租户任务编排方案§五SEC-2**: 跨租户数据流监控+泄露每日扫描设计
- **05文档§七风控安全**: 三级阈值+安全合规要求
- **04部署文档**: PG端口5432/MCP端口18809/路径d:\JueJin\mcps\data-flow-monitor-mcp\
- **统一入口规则R18**: db_logger / atomic_write / health_checks
- **config/data_flow_thresholds.yaml**: 三级阈值(频率100/500, 数据量1GB/10GB, 敏感度normal/pii/credential)

## 历史记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-07-07 | 初始版本,实现8个MCP工具+SEC-2 跨租户数据流监控+泄露每日扫描 |
