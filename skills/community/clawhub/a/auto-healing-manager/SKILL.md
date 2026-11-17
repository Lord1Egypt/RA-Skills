---
name: auto-healing-manager
version: "1.0.0"
description: "五阶段故障自愈闭环管理器v1.0,检测→诊断→修复→验证→回归完整闭环,30天无人值守期间故障自愈率80%。触发:故障自愈/自动修复/自愈管理/auto-healing/fault-healing/混沌工程/故障预案"
tools:
  - trigger_healing
  - diagnose_fault
  - execute_repair
  - verify_repair
  - run_regression
  - get_healing_history
  - healthcheck
dependencies: []
metadata:
  layer: infrastructure
  priority: P0
  category: infra-ops
  openclaw:
    emoji: "🔧"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env:
        - PG_DSN
        - REDIS_URL
      config:
        - config/fault_playbook.yaml
        - mcp.servers.resilience-mcp
---

> **核心功能**: 本技能提供器v1等能力。


# 五阶段故障自愈闭环管理 v1.0 (ARCH-8)

检测→诊断→修复→验证→回归完整闭环,30天无人值守期间故障自愈率从0%提升至80%。

## 使用场景

1. Prometheus指标异常触发自愈(检测阶段已由外部完成) 2. 容器崩溃自动重启 3. 磁盘满自动清理 4. LLM Provider限流自动切换 5. Cookie过期自动刷新 6. Gateway无响应自动重启 7. 故障后业务回归验证 8. 自愈历史查询与成功率统计 9. 混沌工程故障注入测试 10. 30天无人值守期间故障自动处置

## 核心概念

**五阶段闭环**: 检测(阶段1,接收fault_event)→诊断(阶段2,根因分析)→修复(阶段3,执行预案)→验证(阶段4,健康检查)→回归(阶段5,业务验证)。任一阶段失败则停止后续阶段并记录,避免级联错误。

**故障预案库**: config/fault_playbook.yaml定义11个常见故障预案(PG连接池耗尽/Docker容器停止/Cookie过期/LLM 429/磁盘满/Gateway无响应/MCP超时/Redis失败/网络分区/CPU高/内存泄漏),每个预案包含检测条件/诊断规则/修复步骤/验证方法/回滚方案。

**冷却机制**: 同一fault_type在300秒内不重复触发(可通过force=true强制覆盖),防止修复风暴。

**并发控制**: 最大3个并发自愈(asyncio.Semaphore),防止资源争用。

**PG持久化**: auto_healing_events表(event_id/fault_type/diagnosis/repair_action/verification_result/created_at),ThreadedConnectionPool(minconn=1,maxconn=5),PG不可用时降级到文件持久化。

## 工作流

### 流程A: 触发完整五阶段自愈(推荐)
1. 调用trigger_healing(fault_type, fault_context, force=false)
2. 阶段1检测: 接收fault_event,创建event_id
3. 阶段2诊断: 调用diagnose_fault逻辑,匹配预案库,输出根因候选与置信度
4. 阶段3修复: 调用auto_repair逻辑,执行预案中的修复步骤(支持{placeholder}替换与重试)
5. 阶段4验证: 调用health_checks(Docker/Gateway/磁盘),确认故障已消除
6. 阶段5回归: 调用business_regression逻辑,验证EP-01~EP-05链路完整性
7. 全部通过→status=completed;任一失败→status=failed并记录error
8. 持久化到PG(auto_healing_events表)与文件(data/auto_healing/state.json)

### 流程B: 独立诊断(不修复)
1. 调用diagnose_fault(fault_type, fault_context)
2. 加载预案库,匹配fault_type
3. 评估诊断规则,输出根因候选与置信度
4. 不执行修复,仅返回诊断结果(用于人工确认)

### 流程C: 独立修复(干跑模式)
1. 调用execute_repair(fault_type, fault_context, dry_run=true)
2. 加载预案,替换{placeholder}变量
3. dry_run=true仅打印命令不执行(用于预览修复动作)
4. dry_run=false执行修复命令(带重试,单步最多2次)

### 流程D: 独立验证
1. 调用verify_repair(fault_type, fault_context)
2. 执行健康检查: Docker/Gateway/磁盘
3. 至少2/3项通过则验证通过

### 流程E: 独立回归
1. 调用run_regression(fault_type, fault_context, full=false)
2. 验证EP-01~EP-05核心链路: PG/Docker/Gateway/磁盘可写/磁盘空间
3. 核心检查全过则ep_chain_ok=true

### 流程F: 查询历史
1. 调用get_healing_history(limit=50, fault_type="", status="")
2. 返回历史自愈事件列表(按created_at降序)
3. 可按fault_type与status过滤

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| fault_type为空 | INVALID_ARG | 返回错误,提示必填 |
| fault_context非合法JSON | INVALID_JSON | 返回错误,提示格式 |
| 冷却中 | COOLDOWN_ACTIVE | 返回剩余秒数,提示用force=true强制 |
| 预案未找到 | PLAYBOOK_NOT_FOUND | 返回可用fault_type列表 |
| 阶段2诊断失败 | STAGE2_FAILED | 记录并停止,不执行修复 |
| 阶段3修复失败 | STAGE3_FAILED | 记录并停止,不执行验证 |
| 阶段4验证失败 | STAGE4_FAILED | 记录并停止,不执行回归 |
| 阶段5回归失败 | STAGE5_FAILED | 记录,EP链路可能受影响 |
| PG不可用 | (降级) | 自动降级到文件持久化,不报错 |
| MCP不可用 | TRIGGER_ERROR | 返回异常信息,记录日志 |

## 输入格式

```json
{
  "action": "trigger|diagnose|repair|verify|regression|history|healthcheck",
  "fault_type": "docker_container_stopped",
  "fault_context": "{\"container_name\":\"redis\"}",
  "force": false,
  "dry_run": false,
  "full": false,
  "limit": 50,
  "status": "completed"
}
```

字段说明:
- `action`: 操作类型(trigger触发/diagnose诊断/repair修复/verify验证/regression回归/history历史/healthcheck健康检查)
- `fault_type`: 故障类型标识(除history/healthcheck外必填)
- `fault_context`: 故障上下文JSON字符串(用于{placeholder}替换)
- `force`: 是否强制触发忽略冷却(仅trigger)
- `dry_run`: 干跑模式(仅repair)
- `full`: 全量验证(仅regression)
- `limit`: 历史条数(仅history,默认50)
- `status`: 按状态过滤(仅history,如completed/failed)

## 输出格式

```json
{
  "success": true,
  "data": {
    "event_id": "a1b2c3d4-...",
    "fault_type": "docker_container_stopped",
    "stages": {
      "stage1_detection": {"status": "detected", "passed": true},
      "stage2_diagnosis": {"status": "diagnosed", "passed": true, "diagnosis": {...}},
      "stage3_repair": {"status": "repaired", "passed": true, "repair": {...}},
      "stage4_verification": {"status": "verified", "passed": true, "verification": {...}},
      "stage5_regression": {"status": "regressed", "passed": true, "regression": {...}}
    },
    "status": "completed",
    "ep_chain_ok": true
  },
  "error": null,
  "code": null
}
```

字段说明:
- `event_id`: 自愈事件唯一ID(UUID)
- `stages`: 五阶段执行结果(stage1~stage5)
- `status`: 事件最终状态(completed/failed)
- `ep_chain_ok`: EP-01~EP-05链路是否完整(阶段5结果)

## 示例

### 示例1: Docker容器停止自愈
1. 调用trigger_healing(fault_type="docker_container_stopped", fault_context='{"container_name":"redis"}')
2. 阶段2诊断: 匹配预案,根因候选=["容器崩溃","OOM被杀","手动停止"]
3. 阶段3修复: 执行`docker start redis`,等待healthy
4. 阶段4验证: Docker健康=true, Gateway=true, 磁盘=true → 通过
5. 阶段5回归: PG/Docker/Gateway/磁盘全过 → ep_chain_ok=true
6. 返回: `{success:true, data:{status:"completed", ep_chain_ok:true}}`

### 示例2: 磁盘满自愈(冷却中)
1. 300秒内再次调用trigger_healing(fault_type="disk_full")
2. 返回: `{success:false, data:{cooldown_remaining_sec:180}, error:"冷却中", code:"COOLDOWN_ACTIVE"}`
3. 需用force=true强制触发

### 示例3: 干跑模式预览修复
1. 调用execute_repair(fault_type="llm_provider_429", dry_run=true)
2. 返回: `{success:true, data:{steps_executed:2, steps_succeeded:2, details:[{action:"switch_provider", dry_run:true}]}}`
3. 未实际执行命令,仅打印预览

### 示例4: 查询历史自愈事件
1. 调用get_healing_history(limit=10, status="failed")
2. 返回: `{success:true, data:{events:[...], count:3}}`
3. 返回最近10条失败的 自愈事件

## 验证标准

| 验证项 | 标准 |
|:-------|:-----|
| 五阶段闭环 | trigger_healing单次调用完整执行5阶段 |
| 阶段失败停止 | 任一阶段失败不执行后续阶段 |
| 预案库覆盖 | ≥10个常见故障预案(当前11个) |
| 冷却机制 | 同fault_type 300秒内不重复触发 |
| 并发控制 | 最大3个并发自愈 |
| PG持久化 | auto_healing_events表,ThreadedConnectionPool(1,5) |
| 文件降级 | PG不可用时降级到data/auto_healing/state.json |
| EP链路回归 | 阶段5验证PG+Docker+Gateway+磁盘4项核心 |
| 变量替换 | {placeholder}替换为context值 |
| 修复重试 | 单步最多2次重试 |
| 历史查询 | 支持按fault_type与status过滤 |
| 健康检查 | 返回预案数/PG状态/自愈统计 |

## 变更历史

| 版本 | 日期 | 变更内容 |
|:-----|:-----|:---------|
| v1.0 | 2026-07-07 | ARCH-8初始版本:五阶段闭环+11预案+PG持久化 |
