---
name: content-pregenerator
version: "1.0.0"
description: "内容预生成器,凌晨低谷期(01:00-05:00)为所有租户预生成当天内容,复用content-orchestrator的15条管道执行'生成+质检'(跳过发布),结果缓存到PG content_pre_cache表,发布时直接取已生成内容实现秒级发布。DRR三阶段公平调度确保多租户Jain≥0.8。分层降级:PL-VIDEO→PL-IMAGE→TEXT→E0兜底。触发:预生成/内容预生成/凌晨生成/批量生成内容/pregenerate 不触发:实时发布/内容生成/单条生成/客服回复/数据分析"
tools: [read, exec]
dependencies: [content-orchestrator]
metadata:
  layer: product
  priority: P1
  category: content-creation
  openclaw:
    emoji: "🌅"
    color: "#0d9488"
    vibe: "professional"
    os: ["win32", "linux", "darwin"]
    exec_scripts: ["content_pregenerator.py"]
    requires:
      bins: ["python"]
      config: ["mcp.servers.agency-portal-mcp", "mcp.servers.postgres-mcp"]
      env: ["DATABASE_URL"]
---

> **核心功能**: 本技能提供秒级发布、+质检'(跳过发布)等能力。


# 内容预生成器 (Content Pregenerator)

> **来源**: 73_蚕食式系统修复总计划v1.2 Task 6.1 | ADR-004预生成阶段插入决策
> **关联规则**: R72.3(公平调度) | R37(重构抽象-复用现有管道) | R20(赚钱链路完整性) | R74.4(降级三条件) | R25(内容发布验证)

## 使用场景

- **凌晨预生成**: Cron任务每日01:00触发,为所有活跃租户预生成当天内容
- **批量补生成**: 预生成窗口超时后,对timeout/generate_failed任务补生成
- **手动触发**: 用户指定租户手动预生成内容
- **降级生成**: 视频生成失败时降级为图文,图文失败降级为纯文本

## 工作流

1. **初始化**
   - 读取当日daily_plan: `SELECT * FROM daily_plan WHERE plan_date=CURRENT_DATE AND status='pending'`
   - 过滤内容任务: `WHERE task_type IN ('content_video','content_image','content_article')`
   - 检查daily_plan是否存在,不存在则等待5分钟重试(最多3次)
2. **DRR公平排序**
   - 复用task-dispatcher三阶段调度逻辑(保障→公平→竞争)
   - 保障阶段: 每租户至少1个内容任务
   - 公平阶段: JOIN fair_schedule_checkpoint ORDER BY deficit DESC
   - 竞争阶段: ORDER BY priority DESC, scheduled_at ASC
   - 租户级并发上限=2(与pipeline-orchestrator一致)
3. **批量预生成**
   - 对每个任务调用content-orchestrator执行管道(PL-VIDEO/PL-IMAGE等)
   - **跳过发布步骤**: 管道执行到"质检完成"即停止,不执行"多平台发布"
   - 生成结果写入content_pre_cache表(status=ready)
   - 失败任务标记status=generate_failed+fail_category
4. **质量门控**
   - 营销注入门控: market-copywriter失败+降级也失败→拦截(MARKETING_GATE_FAILED)
   - 吸引力评分: LLM 5维评分<60分→拦截,重新生成
   - 差异化检查: 24h内同主题相似度>70%→拦截
5. **失败重试与降级**
   - LLM失败: 指数退避5s/15s/45s,最多3次
   - 引擎不可用: 自动降级kling→pixelle→mpt
   - 生成超时(>5分钟/个): 重试1次,仍失败返回中间产物
   - 内容类型降级: PL-VIDEO→PL-IMAGE→TEXT→E0兜底
   - 降级时设置downgraded=true+downgraded_from+downgraded_to字段(R74.4)
6. **完成报告**
   - 计算Jain公平性指数(≥0.8合格,低于则告警)
   - 输出预生成摘要: 总任务数/成功数/失败数/降级数/超时数
   - 写入db_logger日志+content_pre_cache记录

## 输入格式

```json
{
  "mode": "batch",
  "tenant_id": "",
  "plan_date": "",
  "max_concurrent": 2,
  "timeout_seconds": 14400
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "total_tasks": 15,
    "generated": 12,
    "failed": 2,
    "downgraded": 1,
    "timeout": 0,
    "jain_index": 0.87,
    "tenants_served": 5,
    "duration_ms": 1800000
  },
  "error": null,
  "code": null
}
```

## 异常处理

| 异常码 | 场景 | 处理 | 降级 |
|:-------|:-----|:-----|:-----|
| DAILY_PLAN_NOT_FOUND | 当日daily_plan不存在 | 等待5分钟重试,最多3次 | 跳过预生成,告警 |
| DAILY_PLAN_EMPTY | daily_plan无内容任务 | 记录日志,正常退出 | 无 |
| PIPELINE_EXECUTION_FAILED | 管道执行失败 | 记录fail_category,重试3次 | PL-VIDEO→PL-IMAGE→TEXT |
| GENERATION_TIMEOUT | 单任务生成超时(>5分钟) | 重试1次 | 返回中间产物或降级 |
| PREGEN_WINDOW_TIMEOUT | 预生成窗口超时(>4小时) | 未完成任务标记timeout | dispatcher-cycle补生成 |
| QUALITY_GATE_FAILED | 质量门控未通过 | 重新生成(最多2次) | 降级内容类型 |
| ENGINE_UNAVAILABLE | 生成引擎不可用 | 自动切换备选引擎 | kling→pixelle→mpt |
| PERMANENT_FAILED | 连续3次失败 | 标记permanent_failed | 告警+人工介入 |
| PG_CONNECTION_FAILED | PG连接失败 | 重试3次,间隔10秒 | 跳过预生成,告警 |

## 示例

### 批量预生成(Cron触发)
```bash
python skills/content-pregenerator/scripts/content_pregenerator.py --mode batch
```

### 指定租户预生成
```bash
python skills/content-pregenerator/scripts/content_pregenerator.py --mode batch --tenant t001
```

### 补生成失败任务
```bash
python skills/content-pregenerator/scripts/content_pregenerator.py --mode retry --max-retries 3
```

## Fitness Functions

| # | 不变量 | 验证方法 | 失败响应 |
|:--|:-------|:---------|:---------|
| FF-3 | 发布时content_pre_cache中被发布的内容status必须为ready | 查询publish_log关联content_pre_cache | 阻断发布 |
| FF-4 | 多租户预生成公平性Jain≥0.8 | 预生成完成后计算各租户生成数量Jain指数 | 告警+补偿 |
| FF-5 | 预生成-发布时间预算≥30分钟 | 预生成必须在05:00前完成 | 告警 |

## 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| 1.0.0 | 2026-07-31 | 初始版本(73_蚕食式系统修复总计划v1.2 Task 6.1) |
