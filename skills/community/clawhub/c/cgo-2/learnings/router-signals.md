# Router Signal Table

> 版本：3.0 | 最后更新：2026-06-12
> 本文件可随使用动态扩展。SKILL.md 的 Router Logic 读取此表。

## 核心信号（初始）

| Input Signal | Route To | Confidence Threshold |
|-------------|----------|---------------------|
| "low conversion", "high churn", "traffic dropping", "bottleneck", "not growing" | **Diagnoser** | 0.8 |
| "how can AI help", "opportunities", "what should we do", "new ideas" | **Designer** (opportunity) | 0.8 |
| "build", "design", "automate", "create a system", "workflow" | **Designer** (workflow) | 0.8 |
| "improve", "optimize", "audit", "fix", "make better", "revamp" | **Optimizer** | 0.8 |
| Mix of multiple signals | **Diagnoser** (default) | 0.5 |

## 新增信号

<!-- 由 Evolution Engine 在检测到新模式时提议添加 -->

（暂无新增，随使用自动积累）

## 废弃信号

<!-- 由 Evolution Engine 在信号长期未命中时标记 -->

（暂无废弃）
