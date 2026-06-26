# Reader Guide for Non-Engineering Teammates

如果你不打算直接运行脚本，可以按下面顺序阅读仓库产物：

| 先看什么 | 路径 | 用途 |
|---|---|---|
| 周报 | `data/runs/sample-run/weekly_report.md` | 先快速理解本周结论 |
| 指标摘要 | `data/runs/sample-run/summary.json` | 再看结构化数值 |
| Leaderboard | `data/leaderboards/model_leaderboard.md` | 看模型维度趋势 |
| Repair validation | `data/repair-validations/*.json` | 看修复动作如何验证 |

后续如果要扩展为 notebook 或 dashboard，可以直接读取 `summary.json` 与 `metrics.csv` 作为数据源。

