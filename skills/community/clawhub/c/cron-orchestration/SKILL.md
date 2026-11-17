---
name: cron-orchestration
description: "Cron 调度与互斥规范：主协调器/团队广播/侧线采集职责分离，每轮单任务，5分钟间隔，锁文件防并发。"
version: 1.0.0
author: Michael + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, orchestration, serial, lock, openclaw]
    related_skills: [teamwork, vault-data-governance]
---

# Cron Orchestration：定时任务调度规范

## 职责分离

| cron 名称 | 职责 | 扫描范围 | 调度 |
|---|---|---|---|
| `side-research phase0 push` | **主协调器**：处理 pending 任务并派发子 agent | `task-p*-phase0.json` + `task-tech-advance-*.json` | 每 5h：03/08/13/18/23 |
| `团队自动推进-XX` | **团队广播**：分发 broadcast_tasks.md，不碰 task 文件 | `/root/.openclaw/workspace_teams/*/broadcast_tasks.md` | 每日 1 次 |
| `side_research_runner` | **侧线日采集**：生成侧线日采集报告 | `keywords.md` + `by-country/` + `算电/国内/政策/` | 每 2h |
| `audit_wind_daily.sh` | **审计脚本**：检查同步/MOC/分支/错误/任务完成率 | vault 全目录 | 03:00 |
| `daily_pipeline_06.sh` | **日报流水线**：MOC + 日报 + push | vault 全目录 | 06:00 |
| `daily_policy_fetch.sh` | **政策抓取**：23:00 政策抓取与解读 | 外部 + vault/算电/国内/政策/ | 23:00 |

## 主协调器规则

- 每轮处理所有 `status=pending` 的任务
- **同一轮内**，各个任务之间间隔 **5 分钟**再启动下一个，禁止并发轰炸
- 同一 `assigned_to` 的任务串行执行，不并发
- 产物必须立即 git commit + push
- 任务产出写入 `output_docs` 指定的 vault 相对路径，确保 Gitee 可见

## 任务排序规则

1. **按依赖关系拓扑排序**：先执行无依赖的任务；有 `depends_on` 的任务，必须等依赖任务完成后才能执行。
2. **按优先级排序**：同一层级按 `priority` 排序：P0 > P1 > P2。
3. **按截止日期排序**：同一优先级内，deadline 越早越优先。

## 钉钉通知规则

- 通知映射表：`.agent-coordination/team-notify-map.json`
- 任务完成后发送钉钉消息给 `assigned_to` 对应负责人；找不到时 fallback 到 `michael`
- 完成消息格式：【{task_id}】{标题} 已完成/阻塞。产出：{output_docs}。下一步：{依赖或建议}
- 阻塞消息格式：【{task_id}】{标题} 阻塞。原因：{原因}。建议：{绕行方案}。需要：{所需支持}
- 钉钉仅通知人类，不用于 agent 间通信；agent 间通信只通过 `.agent-coordination/` 文件

## 团队广播规则

- 只分发 broadcast_tasks.md，不扫描 `.agent-coordination/tasks/`
- 不调用 web_search/web_extract
- 识别新增/更新项，同步到对应子 agent

## 互斥锁

- 锁文件：`.cron-context/shared/.cron.lock`
- 启动时检查：锁存在且 5 分钟内未过期 → 直接退出
- 获取锁：写入 PID + 时间戳
- 释放锁：执行完毕后删除
- 异常退出时清理锁

## 串行执行

- 同一 `assigned_to` 的任务串行执行，不并发
- 同一轮内不同任务间隔 5 分钟再启动下一个
- 禁止并发轰炸子 agent

## 上下文隔离

- 每个 cron 轮次有独立工作上下文
- 执行日志写入独立目录：`.agent-coordination/scratch/cron-03/`、`cron-08/` 等
- 不同轮次不共享中间状态，避免上下文污染

## 实际执行结果（2026-08-13 验证）

| 轮次 | 执行时间 | 结果 |
|---|---|---|
| 13:00 | 2026-08-13 13:05 | `[SILENT]` — 无 pending 任务（旧脚本已批量改 completed） |
| 13:49 手动触发 | 2026-08-13 13:49 | 16 完成 / 3 阻塞 / 钉钉通知未发送 |

**已验证功能：**
- 拓扑排序 + 优先级 + 截止日期排序 ✅
- 文件锁 `.cron-context/shared/.cron.lock` ✅
- 产出文件写入 `output_docs` 指定路径 ✅
- git commit + push ✅

**待修复：**
- 钉钉通知：未找到 webhook/发送脚本，需配置通知发送机制
- 依赖任务执行：T2/T7 依赖 P5/P6 完成，但本轮仍被一起执行，需强制等待依赖完成
- 旧脚本 `side_research_run.sh` 仍在运行，与新 cron 职责需明确分离
