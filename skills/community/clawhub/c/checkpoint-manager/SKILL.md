---
name: checkpoint-manager
version: "1.0.0"
description: "工作流检查点管理器v1.0(ARCH-5),PG为唯一权威源,SQLite为本地可丢失缓存,支持崩溃后从PG重建。8工具:save_checkpoint保存检查点到PG+异步缓存SQLite/get_checkpoint从PG权威源读取/list_checkpoints列出工作流检查点/cache_to_sqlite显式缓存/get_cached_state快速读取(缓存未命中回退PG并回填)/rebuild_sqlite_cache从PG重建SQLite/verify_checkpoint_integrity一致性验证/healthcheck。触发:检查点保存/崩溃恢复/缓存重建/一致性验证/工作流状态持久化"
tools: [read, memory_search]
dependencies: []
metadata:
  layer: infrastructure
  priority: P0
  category: infra-ops
  openclaw:
    emoji: "💾"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["JUEJIN_HOME", "DATABASE_URL"]
      config: ["mcp.servers.checkpoint-mcp"]
---

> **核心功能**: 本技能提供器v1等能力。


# 工作流检查点管理 v1.0 (ARCH-5 PG为主+SQLite为缓存)

PG为唯一权威源,SQLite仅本地缓存可丢失,崩溃后从PG重建。取消v7.0双写Saga,简化一致性保证。

## 使用场景

1. 工作流每步执行后保存检查点(崩溃可恢复) 2. 工作流重启时从PG读取最后检查点恢复 3. 高频读取用SQLite缓存加速(缓存未命中自动回退PG) 4. SQLite损坏/丢失后从PG重建缓存 5. 定期一致性验证(比对PG与SQLite) 6. 多租户检查点隔离与按租户重建 7. 健康检查与运维监控

## 核心概念

**PG权威源**: workflow_checkpoints表,UNIQUE(workflow_id, step_id),所有检查点以PG为准。写入用INSERT ON CONFLICT DO UPDATE(upsert)。

**SQLite缓存**: data/checkpoint_mcp/cache.db,checkpoint_cache表,PRIMARY KEY(workflow_id, step_id)。可丢失,失败不影响业务。WAL模式提升并发。

**写入路径**: state_data → PG(同步,权威源) → SQLite(异步,缓存,可丢失)。PG成功即返回成功。

**读取路径**: SQLite(快速) → 未命中/过期 → PG(权威源) → 回填SQLite。缓存TTL默认300秒。

**不再双写**: 取消v7.0 Saga补偿事务+event sourcing replay,PG单点负责一致性。

## 工作流

### 流程A: 保存检查点(save_checkpoint)
1. 调用checkpoint-mcp的save_checkpoint(workflow_id, step_id, state_data, tenant_id)
2. PG同步写入(INSERT ON CONFLICT DO UPDATE),返回id/created_at/updated_at
3. SQLite异步缓存(fire-and-forget,失败不影响业务)
4. 返回success=true + authority_source="pg" + cache_written

### 流程B: 从PG权威源读取(get_checkpoint)
1. 调用get_checkpoint(workflow_id, step_id)
2. 直接从PG读取,保证数据一致性(崩溃恢复/最终确认场景)
3. 返回checkpoint完整信息(id/tenant_id/state_data/created_at/updated_at)
4. 不存在时返回found=false(非错误)

### 流程C: 快速读取(get_cached_state)
1. 调用get_cached_state(workflow_id, step_id)
2. 优先从SQLite缓存读取(快速),命中且未过期(TTL内)返回source="sqlite"
3. 缓存未命中/过期 → 从PG权威源读取,返回source="pg" + backfilled=true
4. 异步回填SQLite缓存(下次读取命中)
5. PG和SQLite均无 → 返回found=false + source="none"

### 流程D: 列出工作流检查点(list_checkpoints)
1. 调用list_checkpoints(workflow_id, tenant_id="")
2. 从PG权威源列出该工作流所有检查点(按updated_at降序)
3. tenant_id非空时按租户过滤
4. 返回checkpoints列表 + count

### 流程E: 显式缓存(cache_to_sqlite)
1. 调用cache_to_sqlite(workflow_id, step_id, state_data)
2. 同步写入SQLite缓存(不写PG,仅缓存场景)
3. 返回written=true/false + cached_at + lossy=true

### 流程F: 崩溃恢复重建(rebuild_sqlite_cache)
1. SQLite丢失/损坏时调用rebuild_sqlite_cache(tenant_id="default")
2. 从PG读取该租户所有检查点(最多10000条)
3. 清空SQLite中相关workflow的缓存条目
4. 批量写入SQLite缓存
5. 返回pg_read_count/deleted_before/rebuilt_count/elapsed_sec

### 流程G: 一致性验证(verify_checkpoint_integrity)
1. 调用verify_checkpoint_integrity(workflow_id="")
2. 从PG和SQLite分别读取检查点
3. 比对差异:cache_only(SQLite有PG无)/pg_only(PG有SQLite无)/data_mismatch(数据不同)
4. 生成报告(原子写入reports目录)
5. 返回consistent布尔 + mismatches详情 + report_path

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| workflow_id/step_id为空 | INVALID_ARG | 返回错误,提示必填 |
| state_data非dict | INVALID_ARG | 返回错误,提示类型 |
| DATABASE_URL未配置 | DB_NOT_CONFIGURED | 提示配置PG连接串 |
| PG写入失败 | PG_WRITE_ERROR | 记录日志,返回错误,SQLite未写 |
| PG读取失败 | PG_READ_ERROR | 记录日志,返回错误 |
| PG列表失败 | PG_LIST_ERROR | 记录日志,返回错误 |
| SQLite缓存写入失败 | (非关键) | 记录debug日志,业务不受影响 |
| SQLite缓存读取失败 | (降级) | 自动降级到PG读取 |
| 一致性验证失败 | VERIFY_FAILED | 记录日志,返回错误 |
| 重建失败 | REBUILD_FAILED | 记录日志,返回错误 |

## 输入格式

```json
{
  "action": "save|get|list|cache|cached_get|rebuild|verify|healthcheck",
  "workflow_id": "wf_20260707_001",
  "step_id": "step_collect_materials",
  "tenant_id": "default",
  "state_data": {"progress": 50, "last_url": "https://...", "items": [1,2,3]}
}
```

字段说明:
- `action`: 操作类型(save保存/get PG读取/list列表/cache显式缓存/cached_get快速读取/rebuild重建/verify验证/healthcheck健康检查)
- `workflow_id`: 工作流ID(除healthcheck外必填)
- `step_id`: 步骤ID(save/get/cache/cached_get必填)
- `tenant_id`: 租户ID(默认"default",save/list/rebuild使用)
- `state_data`: 状态数据(save/cache必填,任意JSON结构)

## 输出格式

```json
{
  "success": true,
  "data": {
    "workflow_id": "wf_20260707_001",
    "step_id": "step_collect_materials",
    "tenant_id": "default",
    "id": 42,
    "created_at": "2026-07-07T10:00:00+08:00",
    "updated_at": "2026-07-07T10:05:30+08:00",
    "cache_written": true,
    "authority_source": "pg"
  },
  "error": null,
  "code": null
}
```

字段说明:
- `authority_source`: "pg"(权威源)/"sqlite"(缓存命中)/"none"(不存在)
- `cache_written`: SQLite缓存是否写入成功(可丢失语义)
- `backfilled`: 缓存未命中时是否从PG回填SQLite(快速读取场景)
- `consistent`: 一致性验证是否通过(verify场景)
- `lossy`: SQLite缓存是否可丢失(true)

## 示例

### 示例1: 保存检查点并快速读取
1. 调用save_checkpoint(workflow_id="wf_001", step_id="step_1", state_data={"progress":30}, tenant_id="default")
2. 返回: `{success:true, data:{id:1, authority_source:"pg", cache_written:true}}`
3. 调用get_cached_state(workflow_id="wf_001", step_id="step_1")
4. 返回: `{success:true, data:{found:true, source:"sqlite", state_data:{"progress":30}, backfilled:false}}`

### 示例2: 缓存未命中回退PG
1. 删除SQLite缓存文件(模拟崩溃)
2. 调用get_cached_state(workflow_id="wf_001", step_id="step_1")
3. SQLite未命中 → 从PG读取 → 返回source="pg" + backfilled=true
4. 再次调用get_cached_state → 命中SQLite,返回source="sqlite"

### 示例3: 崩溃恢复重建
1. SQLite文件损坏/丢失
2. 调用rebuild_sqlite_cache(tenant_id="default")
3. 从PG读取100条检查点,清空旧缓存,重建100条
4. 返回: `{success:true, data:{pg_read_count:100, deleted_before:0, rebuilt_count:100, elapsed_sec:0.5}}`

### 示例4: 一致性验证
1. 调用verify_checkpoint_integrity(workflow_id="wf_001")
2. 比对PG(5条)与SQLite(4条),发现pg_only=1条
3. 返回: `{success:true, data:{consistent:false, pg_count:5, sqlite_count:4, mismatches:{pg_only:[{workflow_id:"wf_001",step_id:"step_3"}]}}}`
4. 调用rebuild_sqlite_cache修复不一致

## 验证标准

| 验证项 | 标准 |
|:-------|:-----|
| PG权威源写入 | INSERT ON CONFLICT DO UPDATE,upsert语义 |
| SQLite异步缓存 | fire-and-forget,失败不影响业务 |
| 缓存TTL | 默认300秒,过期自动回退PG |
| 缓存回填 | 未命中时从PG读取后异步回填SQLite |
| 崩溃恢复 | SQLite丢失后rebuild_sqlite_cache从PG重建 |
| 一致性验证 | 比对PG与SQLite,3类不一致检测 |
| 多租户隔离 | tenant_id字段,按租户重建缓存 |
| 不再双写 | 无Saga补偿事务,PG单点一致性 |
| 数据一致性 | 99.9%(从v7.0的95%提升) |

## 变更历史

| 版本 | 日期 | 变更内容 |
|:-----|:-----|:---------|
| v1.0 | 2026-07-07 | ARCH-5初始版本:PG为主+SQLite为缓存,取消双写Saga |
