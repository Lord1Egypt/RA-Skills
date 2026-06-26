# Database Performance Diagnosis Knowledge Base

## Performance Diagnosis Metric System

### 1. SQL Performance Metrics

| Metric Name | Description | Healthy Threshold | Optimization Suggestion |
|---------|------|---------|---------|
| Average Execution Time (aveExecTime) | SQL average execution time | < 100ms | Consider adding indexes or optimizing SQL if exceeds threshold |
| Maximum Execution Time (maxExecTime) | SQL maximum execution time | < 1000ms | Investigate slow SQL, analyze execution plan |
| Execution Count (number) | SQL execution frequency | - | Focus on high-frequency SQL optimization |
| Total Execution Time (totalExecTime) | Cumulative execution time | - | Identify resource-intensive queries |
| Average Lock Wait Time (aveLockWaitTime) | Average lock wait time | < 10ms | Check lock contention and transaction isolation level |
| Maximum Lock Wait Time (maxLockWaitTime) | Maximum lock wait time | < 100ms | Investigate deadlocks and long transactions |

### 2. Database Monitoring Metrics

| Metric Name | Description | Healthy Threshold | Optimization Suggestion |
|---------|------|---------|---------|
| QPS (Queries Per Second) | Queries per second | Based on business | Watch for sudden spikes or drops |
| TPS (Transactions Per Second) | Transactions per second | Based on business | Monitor transaction processing capacity |
| Connections | Current connections | < 80% of max connections | Check connection pool configuration |
| Active Connections | Connections currently executing | < 50% of total connections | Watch for connection leaks |

### 3. Host Resource Metrics

| Metric Name | Description | Healthy Threshold | Optimization Suggestion |
|---------|------|---------|---------|
| CPU Usage | Database server CPU | < 70% | Consider scaling up or optimizing SQL if exceeds threshold |
| Memory Usage | Database server memory | < 80% | Check memory configuration and cache hit rate |
| Disk IO Usage | Disk IO utilization | < 70% | Optimize slow SQL, consider SSD upgrade |
| Disk Throughput | Amount of data read/write per second | Based on disk | Watch for IO bottleneck |
| Network Traffic | Network send/receive rate | Based on bandwidth | Watch for network latency |

## AAS (Average Active Sessions) Analysis

### AAS Metric Interpretation

- **AAS < 1**: System load is normal
- **1 ≤ AAS < 5**: Medium system load, needs attention
- **AAS ≥ 5**: High system load, immediate optimization required

### AAS Composition Analysis

| Component | Description | Meaning of High Value |
|------|------|---------|
| **ON CPU** | Sessions executing on CPU | CPU bottleneck |
| **IO Wait** | Sessions waiting for IO | Disk bottleneck |
| **Lock Wait** | Sessions waiting for locks | Severe lock contention |
| **Network Wait** | Sessions waiting for network | Network latency |

## Slow SQL Analysis Methodology

### 1. Identifying Slow SQL

- SQL with execution time exceeding threshold (default >100ms)
- SQL with high execution frequency but fast single execution (large cumulative time)
- SQL with long lock wait times

### 2. Analysis Dimensions

- **Execution Plan**: Whether indexes are used, whether full table scans exist
- **Data Distribution**: Table data volume, index selectivity
- **Concurrency**: Whether lock contention exists
- **Resource Consumption**: CPU, IO, memory usage

### 3. Optimization Strategies

1. **Index Optimization**
   - Add appropriate indexes
   - Optimize composite index order
   - Remove redundant indexes

2. **SQL Rewrite**
   - Avoid subqueries, use JOIN instead
   - Reduce bookmark lookup operations
   - Use covering indexes

3. **Architecture Optimization**
   - Partition table optimization
   - Read-write separation
   - Cache optimization

## Root Cause SQL Identification

### Root Cause SQL Characteristics

1. Abnormally high execution frequency
2. Long single execution time
3. High resource consumption percentage
4. Triggering chain reactions (lock waits, connection pool exhaustion)

### Identification Methods

- **Correlation Analysis**: Correlate slow SQL with AAS and resource metrics
- **Time Window**: Analyze within the time period when performance issues occurred
- **Impact Scope**: Evaluate SQL's impact on overall system

## Standard Performance Diagnosis Flow

```
1. Information Collection Phase
   └─ Get instance basic information
   └─ Collect performance metrics for specified time period
   └─ Extract slow SQL and root cause SQL

2. Analysis Diagnosis Phase
   └─ Analyze AAS metrics, identify bottleneck type
   └─ Analyze resource metrics, identify resource bottleneck
   └─ Analyze slow SQL, identify optimization points

3. Optimization Recommendation Phase
   └─ SQL optimization suggestions (indexes, rewrite)
   └─ Configuration optimization suggestions (connection pool, cache)
   └─ Architecture optimization suggestions (read-write separation, sharding)
```

## Common Diagnosis Time Ranges

| Time Range | Applicable Scenario | Calculation Method |
|---------|---------|---------|
| Last 1 hour | Real-time issue troubleshooting | now - 3600 |
| Last 6 hours | Recent performance trend | now - 21600 |
| Last 24 hours | Daily performance analysis | now - 86400 |
| Last 7 days | Periodic performance issues | now - 604800 |

## Related Tools (Actual Existing API Endpoints)

### Comprehensive Diagnosis Tools
- `performance_diagnosis` - Comprehensive performance diagnosis (recommended)
  - Calls: /drapi/ai/instance/info、/drapi/ai/getSlowSqlByTime、/drapi/ai/getAbnormalSqlByTime、/drapi/ai/activeSession/statistics、/drapi/ai/getResourceMetricsInNL

### Single Diagnosis Tools
- `get_slow_sql` - Get slow SQL list (/drapi/GetsSlowSqlDigest)
- `get_slow_sql_by_time` - Get slow SQL by time (diagnosis version) (/drapi/ai/getSlowSqlByTime)
- `get_related_sql_info` - Get root cause SQL (/drapi/ai/getAbnormalSqlByTime)
- `get_aas_info` - Get AAS active session statistics (/drapi/ai/activeSession/statistics)
- `get_basic_monitor_info` - Get database monitoring metrics (/drapi/ai/getResourceMetricsInNL)
- `get_host_resource_info` - Get host resource metrics (/drapi/ai/getResourceMetricsInNL)
- `get_instance_info` - Get instance detailed information (/drapi/ai/instance/info)
- `get_db_parameter_info` - Get database parameters (/drapi/ai/getDBParamsInNL)
