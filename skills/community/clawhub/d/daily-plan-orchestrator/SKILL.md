---
name: daily-plan-orchestrator
version: "1.0.0"
description: "每日计划编排器,daily_plan表PG持久化,从task_template实例化每日计划,carryover上限30天(R72.5保护),每日0:00 DRR状态重置+熔断HALF_OPEN,跨日Pipeline支持。触发:daily-plan-generator Cron每日0:00/手动生成计划。不触发:单次任务执行(用task-dispatcher)"
tools: [read, exec]
dependencies: []
metadata:
  layer: product
  priority: P0
  category: orchestration
  openclaw:
    emoji: "📅"
    color: "#4ecdc4"
    vibe: "professional"
    os: ["win32", "linux", "darwin"]
    exec_scripts: ["orchestrator.py"]
    requires:
      bins: ["python"]
      config: []
      env: ["PG_DSN"]
---

# Daily Plan Orchestrator 每日计划编排器

**版本**: v1.0.0 | **优先级**: P0（任务编排核心） | **所属层**: 产品层(Layer 2计划层)

## 使用场景

- daily-plan-generator Cron每日0:00触发
- 手动生成当日计划: `python scripts/orchestrator.py --plan-date 2026-07-08`
- 跨日carryover: 前一日未完成任务carryover到次日(上限30天)
- DRR状态重置: 每日0:00重置fair_schedule_checkpoint表

## 工作流

1. 加载激活的任务模板
   - 查询task_template表 WHERE is_active=TRUE
   - 按租户分组

2. 实例化daily_plan
   - 为每个租户+每个模板创建daily_plan记录
   - 设置quota_total=模板.quota_daily+carryover

3. carryover处理(R72.5保护: 上限30天)
   - 查询前一日daily_plan中status≠completed的任务
   - 计算missed_quota_carryover(上限max_carryover_per_day=5)
   - 创建deferred_task记录(上限30天)
   - 超过30天的任务标记为expired

4. DRR状态重置
   - 更新fair_schedule_checkpoint表reset_date=CURRENT_DATE
   - served_count=0, deficit保留(跨日补偿)

5. 熔断状态扫描
   - 查询tenant级熔断OPEN状态
   - 转换为HALF_OPEN(允许试探性执行)

## 输入格式

```json
{
  "plan_date": "2026-07-08",
  "tenant_filter": null,
  "trigger": "cron"
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "plans_created": 5,
    "tenants_served": ["tenant-1", "tenant-2"],
    "carryover_count": 3,
    "deferred_count": 1,
    "expired_count": 0,
    "drr_reset": true,
    "circuit_breaker_reset": 2
  },
  "error": null,
  "code": null
}
```

## 异常处理

- PG连接失败: 记录错误+返回PG_UNAVAILABLE
- 模板不存在: 跳过该租户+记录WARNING
- carryover超过30天: 标记expired+记录tenant_notification

## 示例

```bash
# Cron触发(每日0:00)
python skills/daily-plan-orchestrator/scripts/orchestrator.py --trigger cron --plan-date 2026-07-08

# 手动生成指定租户
python skills/daily-plan-orchestrator/scripts/orchestrator.py --plan-date 2026-07-08 --tenant tenant-1
```

## R72保护声明

本Skill属于R72.1保护的8个核心编排Cron之一(daily-plan-generator)，禁止删除。
daily_plan表属于R72.2保护的20张PG表之一，禁止删除。
carryover上限30天属于R72.5保护，禁止改回3天。
