---
name: completion-report-generator
version: "1.0.0"
description: "每日完成报告生成器,聚合task_result+daily_completion_report表+30天WelcomeBackCard摘要+待处理事项+租户完成率统计。触发:每日23:00 Cron(completion-report-generator)。不触发:实时查询(用task-dispatcher)"
tools: [read, exec]
dependencies: []
metadata:
  layer: plugin
  priority: P1
  category: orchestration
  openclaw:
    emoji: "📊"
    color: "#27ae60"
    vibe: "professional"
    os: ["win32", "linux", "darwin"]
    exec_scripts: ["report_generator.py"]
    requires:
      bins: ["python"]
      config: []
      env: ["PG_DSN"]
---

# Completion Report Generator 每日完成报告生成器

**版本**: v1.0.0 | **优先级**: P1（任务编排报告层） | **所属层**: 产品层(Layer 5 报告层)

## 使用场景

- 每日23:00自动生成当日完成报告(Cron触发)
- 用户30天未登录后首次回归,展示WelcomeBackCard(30天摘要+待处理事项)
- 管理员查看租户完成率统计

## 工作流

1. 聚合当日任务结果
   - 查询task_result表统计当日完成/失败/跳过数量
   - 按租户维度分组统计完成率
   - 计算Jain公平性指数(从fair_schedule_checkpoint读取)

2. 生成daily_completion_report记录
   - 写入daily_completion_report表
   - 包含: plan_date/tenant_id/total_tasks/completed_tasks/failed_tasks/skipped_tasks/fairness_index/note

3. 生成WelcomeBackCard数据(30天摘要)
   - 聚合最近30天daily_completion_report
   - 生成30天完成总数/失败总数/平均完成率
   - 生成待处理事项列表(deferred_task中未处理的)
   - 生成建议(基于完成率: <60%建议加配额/60-80%正常/>80%优秀)

4. 推送通知(可选)
   - 写入tenant_notification表
   - 严重失败(P0任务失败)→即时推送

## 输入格式

```json
{
  "report_date": "2026-07-08",
  "tenant_filter": null
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "report_date": "2026-07-08",
    "tenants_reported": 20,
    "total_completed": 45,
    "total_failed": 3,
    "average_completion_rate": 0.94,
    "fairness_index": 0.87,
    "welcome_back_cards_generated": 5
  },
  "error": null,
  "code": null
}
```

## 异常处理

- DB未连接: 返回模拟报告+CODE=DB_NOT_CONNECTED
- 无任务数据: 生成空报告+标记no_data
- 聚合超时(>60秒): 部分聚合+标记partial

## R72保护声明

本Skill属于R72.1保护: completion-report-generator Cron不可删除。
报告数据来源于R72.2保护的daily_completion_report表。
