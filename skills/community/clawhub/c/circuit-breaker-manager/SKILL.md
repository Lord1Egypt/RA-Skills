---
name: circuit-breaker-manager
version: "1.0.0"
description: "MCP依赖图与熔断器管理器v1.0,注册MCP依赖关系并拓扑排序,管理熔断器状态机(closed/open/half_open)与Bulkhead隔离舱,自动失败计数与恢复探测。触发:依赖注册/熔断检查/状态查询/熔断重置/级联故障分析/部署后验证"
tools: [read, memory_search]
dependencies: []
metadata:
  layer: infrastructure
  priority: P0
  category: infra-ops
  openclaw:
    emoji: "🛡️"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["JUEJIN_HOME"]
      config: ["mcp.servers.resilience-mcp"]
---

> **核心功能**: 本技能提供/部署后验证、器v1等能力。


# MCP依赖图与熔断器管理 v1.0 (ARCH-10)

注册MCP依赖关系并拓扑排序,管理熔断器状态机与Bulkhead隔离舱,自动失败计数与恢复探测。

## 使用场景

1. 部署后注册MCP依赖关系,生成启动拓扑序 2. MCP调用失败时记录失败,触发熔断保护 3. MCP调用成功时记录成功,触发熔断恢复 4. 请求前检查熔断器是否放行 5. 手动重置熔断器(故障排查后) 6. 查询Bulkhead隔离舱并发状态 7. 级联故障分析(依赖图+熔断状态) 8. 健康检查与运维监控

## 核心概念

**依赖图**: MCP间的依赖关系有向图,Kahn算法拓扑排序,DFS检测循环依赖。依赖项需先启动。

**熔断状态机**: closed(正常) → open(熔断,拒绝请求) → half_open(探测) → closed/open。阈值5次失败,60秒恢复,半开最多1个探测请求。

**Bulkhead隔离舱**: 每MCP独立asyncio.Semaphore,最大并发10,排队等待30秒,防止故障MCP耗尽线程资源。

## 工作流

### 流程A: 注册MCP依赖关系
1. 调用resilience-mcp的register_mcp_dependency(mcp_name, depends_on)
2. 自动检测循环依赖,有环则回滚并返回CYCLE_DETECTED
3. 返回拓扑排序结果(依赖项在前,被依赖项在后)
4. 持久化到data/circuit_breaker/state.json

### 流程B: 调用前熔断检查(check_circuit)
1. 调用前先check_circuit(mcp_name)
2. 返回allowed=true → 放行请求; allowed=false → 拒绝并返回降级建议
3. closed状态直接放行; open状态等待recovery_timeout后转half_open; half_open仅放行1个探测

### 流程C: 调用后记录结果
1. 调用成功 → record_success(mcp_name),half_open状态下探测成功则恢复到closed
2. 调用失败 → record_failure(mcp_name, error_type),连续5次失败触发熔断(open)
3. 状态变更后自动持久化

### 流程D: 手动重置熔断器
1. 故障排查后调用reset_circuit(mcp_name)
2. 强制重置为closed状态,清空失败计数
3. 记录操作日志

### 流程E: 隔离舱状态查询
1. 调用get_bulkhead_status(mcp_name)
2. 返回active_calls/queued_calls/total_rejected统计
3. active_calls>=max_concurrent表示MCP过载

### 流程F: 依赖图与级联分析
1. 调用get_dependency_graph获取完整图与拓扑序
2. 结合get_circuit_state分析级联故障(被依赖MCP熔断→依赖方受影响)
3. critical=true的MCP熔断需触发降级(记录待执行任务)

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| mcp_name为空 | INVALID_ARG | 返回错误,提示必填 |
| depends_on非列表 | INVALID_ARG | 返回错误,提示类型 |
| 检测到循环依赖 | CYCLE_DETECTED | 回滚注册,返回环路径 |
| MCP不可用 | MCP_UNAVAILABLE | 重启resilience-mcp |
| 状态持久化失败 | PERSIST_ERROR | 记录日志,内存状态仍有效 |
| 隔离舱排队超时 | QUEUE_TIMEOUT | 返回降级建议,统计rejected |

## 输入格式

```json
{
  "action": "register|graph|state|record_failure|record_success|check|reset|bulkhead|healthcheck",
  "mcp_name": "content-publisher",
  "depends_on": ["multi-publisher-mcp", "device-operations-mcp"],
  "error_type": "timeout"
}
```

字段说明:
- `action`: 操作类型(register注册/graph依赖图/state熔断状态/record_failure记录失败/record_success记录成功/check检查/reset重置/bulkhead隔离舱/healthcheck健康检查)
- `mcp_name`: MCP服务名(除graph/healthcheck外必填)
- `depends_on`: 依赖MCP列表(仅register使用)
- `error_type`: 错误类型(仅record_failure使用,如timeout/connection_error/http_5xx)

## 输出格式

```json
{
  "success": true,
  "data": {
    "name": "content-publisher",
    "state": "closed",
    "failure_count": 0,
    "success_count": 25,
    "failure_threshold": 5,
    "recovery_timeout_sec": 60,
    "half_open_max_calls": 1,
    "last_failure_time": null,
    "last_success_time": 1730908800.0,
    "opened_at": null,
    "last_error_type": null
  },
  "error": null,
  "code": null
}
```

字段说明:
- `state`: 熔断状态(closed正常/open熔断/half_open半开探测)
- `failure_count`: 连续失败次数(达failure_threshold触发熔断)
- `success_count`: 累计成功次数
- `opened_at`: 进入open状态的时间戳(null表示非open)
- `last_error_type`: 最近错误类型(用于故障分类)

## 示例

### 示例1: 注册依赖并获取拓扑序
1. 调用register_mcp_dependency(mcp_name="content-publisher", depends_on=["multi-publisher-mcp","sensitive-word-mcp"])
2. 返回: `{success:true, data:{registered:true, topo_order:["sensitive-word-mcp","multi-publisher-mcp","content-publisher"]}}`

### 示例2: 熔断触发与恢复
1. 对xianyu-agent-mcp连续调用record_failure 5次 → state变为open
2. 调用check_circuit → allowed=false, 原因"open(剩余60s)"
3. 等待60秒后调用check_circuit → allowed=true, 状态转为half_open
4. 调用record_success → state恢复closed, failure_count=0

### 示例3: 循环依赖检测
1. 调用register_mcp_dependency("A", ["B"]) → 成功
2. 调用register_mcp_dependency("B", ["A"]) → 失败, code=CYCLE_DETECTED, error="检测到循环依赖: A -> B"

## 验证标准

| 验证项 | 标准 |
|:-------|:-----|
| 依赖图拓扑排序 | Kahn算法,无环时返回完整序 |
| 循环依赖检测 | DFS检测,有环时回滚并返回路径 |
| 熔断阈值 | failure_count>=5触发open |
| 恢复超时 | open后60秒转half_open |
| 探测限制 | half_open仅放行1个请求 |
| 探测成功恢复 | half_open+success → closed |
| 探测失败回退 | half_open+failure → open |
| Bulkhead并发 | 每MCP最大10并发,超限排队 |
| 排队超时 | 等待30秒未获槽位则拒绝 |
| 状态持久化 | 原子写入data/circuit_breaker/state.json |

## 变更历史

| 版本 | 日期 | 变更内容 |
|:-----|:-----|:---------|
| v1.0 | 2026-07-07 | ARCH-10初始版本:依赖图+熔断器+Bulkhead |
