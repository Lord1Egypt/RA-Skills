# Getting Started with DevTool Answer Monitor

**DevTool Answer Monitor** 是一个面向 **开发者工具、API、SDK 与开源项目** 的答案监控工具包。它的重点不是通用营销文案生成，而是把 **Query Pool、LLM answer monitoring、四指标打分、repair loop、activation 分析、T+7/T+14 回归验证** 串成可复现的团队工作流。

## Read This First

如果你是第一次接触这个仓库，建议先看 `docs/for-beginners.md`。那份文档是 5 分钟路径；本文档是长版说明。

## What You Can Do in the First 30 Seconds

如果你只想先看到“这个仓库跑完后到底会产出什么”，按下面顺序执行即可。

```bash
git clone https://github.com/veeicwgy/devtool-answer-monitor.git
cd devtool-answer-monitor
bash install.sh
make doctor
bash quickstart.sh
```

运行后，你会同时看到两类结果：一类是新的多模型手工演示 run，另一类是基于仓库内样例摘要重放出来的报告与可视化产物。

| Output | Path | Why it matters |
|---|---|---|
| Raw responses | `data/runs/quickstart-run/raw_responses.jsonl` | 查看每个 query 被哪个模型如何回答 |
| Score draft | `data/runs/quickstart-run/score_draft.jsonl` | 进入人工标注与复核前的草稿层 |
| Run manifest | `data/runs/quickstart-run/run_manifest.json` | 保留本次 run 的输入与记录数 |
| Weekly report | `data/runs/sample-run/weekly_report.md` | 快速理解可交付给团队的周报长什么样 |
| Sciverse sample summary | `data/runs/sciverse-sample-run/summary.json` | 查看 scientific API 场景下的 funnel-stage 切片 |
| Leaderboard snapshot | `assets/leaderboard-sample.png` | 查看默认多模型对比快照 |
| Repair trend snapshot | `assets/repair-trend-sample.png` | 查看修复动作后的时间序列改善 |

## Which Entry Should You Use

| Entry | Command | Best for |
|---|---|---|
| Install | `bash install.sh` | 一键安装依赖并准备本地环境 |
| Doctor | `make doctor` | 先检查环境、样例文件和目录是否完整 |
| Quickstart | `bash quickstart.sh` | 首次体验、30 秒看懂产物、零 API 成本演示 |
| Make target | `make quickstart` | 已熟悉 Make 工作流的团队 |
| Sciverse sample report | `make sample-report-sciverse` | 直接重建 scientific API 样板的 summary 与周报 |
| CLI | `python -m devtool_answer_monitor ...` | 接入自己的 Query Pool、模型配置与运行目录 |

> 兼容说明：旧 CLI 别名仍然保留，方便兼容已有自动化。

## Default Runtime Modes

| Mode | Inputs | Outputs | Use when |
|---|---|---|---|
| Quickstart replay | `data/models.multi.sample.json` + `data/manual.multi.sample.json` | `quickstart-run` 产物 + 默认报告快照 | 想先看结果，不想先配 API |
| Manual paste mode | Query Pool + manual response JSON | `raw_responses.jsonl` + `score_draft.jsonl` | 需要把外部聊天结果导入仓库打分 |
| API collection mode | Query Pool + model config + API key | `raw_responses.jsonl` + `score_draft.jsonl` + 后续汇总 | 做真实批量监控 |

## Sample Files You Can Reuse

| File | Purpose |
|---|---|
| `data/query-pools/mineru-example.json` | 默认开发者工具 Query Pool 示例 |
| `data/query-pools/sciverse-api-integration-example.json` | scientific API / agent workflow Query Pool 示例 |
| `data/runs/sample-run/weekly_report.md` | complete developer-tool weekly report 示例 |
| `data/runs/sciverse-sample-run/weekly_report.md` | complete scientific API weekly report 示例 |
| `data/models.sample.json` | 最小单模型配置 |
| `data/models.multi.sample.json` | 默认多模型演示配置 |
| `data/manual.sample.json` | 最小手工回答样例 |
| `data/manual.multi.sample.json` | 多模型手工回答样例 |

## Start By Goal

如果你不是只想“看一个 demo”，而是想把 AI visibility 用在真实增长目标上，可以按目标选择入口。

| Goal | First file to open | Why |
|---|---|---|
| 提高模型提及和推荐质量 | `docs/metric-definition.md` | 先把 4 个核心指标跑通 |
| 提高下载和安装 | `docs/activation-metrics.md` | 把“提及”延伸到“可执行下一步” |
| 提高 API 调用和 agent 调用 | `playbooks/agent-readiness.md` | 先修最影响调用成功率的 surfaces |
| 面向 MinerU / Sciverse / scientific discovery | `playbooks/scientific-product-visibility.md` | 直接使用 scientific product 的场景框架 |

## Recommended Team Workflow

| Stage | What to do | Primary artifact |
|---|---|---|
| Day 1 | 建立 Query Pool，确认品牌、能力、生态与负向问题四类查询 | Query Pool JSON |
| Day 2 | 对目标模型执行首轮监控并保留原始回答 | `raw_responses.jsonl` |
| Day 3 | 完成四指标打分并汇总为报告 | `summary.json` + `weekly_report.md` |
| Day 4-5 | 分类问题来源并安排修复动作 | repair validation JSON |
| Day 7 / Day 14 | 用同一组 query 回跑并比较变化 | delta report + trend chart |

## Business Fit

这个仓库最适合下列团队。

| Team type | Why it fits |
|---|---|
| Developer tools | 需要监控模型是否正确提及能力、安装方式、生态兼容性 |
| Open-source maintainers | 需要修复错误认知、陈旧回答与竞品插入 |
| API / SDK teams | 需要建立稳定 Query Pool，长期观察模型认知变化 |
| Product marketing + DevRel | 需要一套可以协同、复盘、回归验证的 AI 可见性中台 |

## Read Next

| Topic | Path |
|---|---|
| Metric definition | `docs/metric-definition.md` |
| Activation metrics | `docs/activation-metrics.md` |
| Agent readiness | `playbooks/agent-readiness.md` |
| Surface priority | `playbooks/developer-tool-surface-priority.md` |
| Scientific product visibility | `playbooks/scientific-product-visibility.md` |
| Benchmark method | `benchmark/README.md` |
| Notebook / reader guide | `notebooks/README.md` |
| Repair template | `templates/repair-validation.md` |
| Weekly report template | `templates/weekly-report.md` |
| Release notes | `release-notes/v0.3.0.md` |

## Positioning

请把这个仓库理解为：

> **Answer Monitoring Workflow for Developer Tools**
>
> 它关注的是 **监控、打分、修复、activation 与回归验证**，而不是泛化的营销内容生成。
>
> 如果你更想直接进入 agent workflow，可以从仓库根目录的 [`SKILL.md`](../SKILL.md) 开始。
