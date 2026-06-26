---
name: apollo-overview
description: >
  给你一张完整的方法论地图，告诉你从想法到成品每步该做什么。
---

# Apollo 方法论套件

Apollo是一套**结构化AI编码方法论**，让AI coding agent变成严谨的工程师而不是盲目写代码的助手。

## 套件组成

| Skill | 作用 |
|-------|------|
| **apollo-workflow** | 核心Pipeline入口（ brainstorming→plan→subagent→review→finish） |
| **apollo-brainstorming** | 苏格拉底式提问，搞清楚"真正要做什么" |
| **apollo-planning** | 把设计拆成2-5分钟的小任务 |
| **apollo-parallel** | 并行派发多个子任务同时工作 |
| **apollo-verification** | 证据先行——说"完成了"之前必须跑验证命令 |
| **apollo-debugging** | 四阶段调试：根因→模式→假设→验证 |
| **apollo-mode** | 开启/关闭严格工程模式 |
| **apollo-state-machine** | 状态机驱动，支持随时打断恢复 |
| **apollo-research-synthesis** | 多人并行研究，最后自己汇总 |
| **apollo-timeout** | 超时容错，不卡死整个流程 |
| **apollo-multi-round** | 复杂任务多轮确认，不闷头跑到底 |
| **apollo-dream** | 像睡觉做梦一样整理记忆 |

## 核心原则

1. **Spec-first** — 先写规格，再写代码
2. **TDD** — 先写失败测试，再写实现
3. **Subagent驱动** — 并行执行，小步迭代
4. **证据说话** — 说"完成了"必须有验证结果

## 使用方式

当用户说"开发新功能"、"修bug"、"写计划"、"开始项目"时触发。
