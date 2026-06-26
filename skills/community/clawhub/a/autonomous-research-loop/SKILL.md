---
name: Autonomous Research Loop
slug: autonomous-research-loop
version: 1.0.0
description: 🦞 自主研究无限循环 - 自主生成研究主题、深度研究、创建飞书文档、无限循环运行。
changelog: 初始版本，基于 research_pool.json 的无限研究循环系统。
metadata: {"clawdbot":{"emoji":"🦞","requires":{},"os":["linux"]}}
---

## 概述

🦞 **自主研究无限循环** 是小智的自我驱动研究系统，核心逻辑：

```
生成研究主题 → 深度研究 → 创建飞书文档 → 回到生成主题（无限）
```

## 核心文件

| 文件 | 作用 |
|------|------|
| `research_pool.json` | 主题池（已完成 + 待研究 + 统计） |
| `research_loop.md` | 架构说明文档 |

## 工作流程

```
Cron触发（每5分钟）
    ↓
读取 research_pool.json
    ↓
检查 pending_topics
    ↓
有主题 → 随机选1个
无主题 → 生成3个新主题
    ↓
深度研究 + 创建飞书文档
    ↓
移动到 completed + 生成3个新主题
    ↓
输出简报到飞书
    ↓
异常 → 直接退出（Cron 自动拉起）
```

## 配置文件结构

```json
{
  "completed_topics": ["主题1", "主题2", ...],
  "pending_topics": [{topic: "...", description: "..."}],
  "stats": {
    "total_completed": 21,
    "total_generated": 23,
    "last_completed_at": "2026-04-02T09:00:00+08:00"
  },
  "config": {
    "interval_minutes": 5,
    "max_research_time_minutes": 30,
    "new_topics_per_completion": 3
  }
}
```

## 研究输出格式

每篇研究文档包含：
- **一句话总结**（核心发现）
- **机制拆解**（传导链条）
- **实战要点**（具体可操作）
- **Python代码框架**（可选）
- **翻车点/风险提示**

## 异常处理原则

- 异常 → 直接退出，不重试，不切换模型
- Cron 会自动拉起新任务
- 被系统 kill → 靠 Cron 恢复

## 质量控制原则

- 模型自己解决研究质量问题
- 不等待人工确认
- 靠间隔时间（5分钟）控制频率
- 无每日上限

## 相关文件

- Cron任务：`🦞 自主研究无限循环`（每5分钟触发）
- 配置文件：`/root/.openclaw/workspace/research_pool.json`
- 说明文档：`/root/.openclaw/workspace/research_loop.md`
