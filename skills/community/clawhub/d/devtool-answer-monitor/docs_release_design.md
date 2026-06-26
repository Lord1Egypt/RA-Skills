# Release Upgrade Design for v0.2.0

## 版本目标

`v0.2.0` 的目标不是引入大型新系统，而是把现有仓库从“能跑”推进到“像一个可发布、可协作、可演示的开源项目”。因此本轮设计遵循两个原则：第一，所有新增内容都围绕 **首次访问体验** 与 **使用门槛降低**；第二，优先把已有样例、脚本和数据组织成更容易理解的产品化表层。

## 版本范围

| 模块 | 设计动作 | 预期产物 |
|---|---|---|
| Release | 新增 `CHANGELOG.md` 与 `release-notes/v0.2.0.md` | 可发布版本说明 |
| README | 增加徽章、Quick Demo、预期输出、截图、sample snapshot 导览 | 更强的首屏说服力 |
| Sample artifacts | 补全 `data/runs/sample-run/` 的 raw + score draft + summary + report | 完整快照 |
| CLI | 增加 `geo_monitor` 包与 `python -m geo_monitor` 入口 | 更低使用门槛 |
| Leaderboard | 新增模型维度的轻量趋势汇总与图像输出 | 结果可视化证据 |
| Repair loop | 补充 2-3 个 T+7 / T+14 案例 | 闭环证明 |
| Collaboration | 新增 issue templates 与 `CONTRIBUTING.md` | 更清晰的协作入口 |
| GitHub presentation | 准备 About 描述、Topics、Release 文案 | 更好站内检索与信任感 |

## README 改造设计

README 顶部应优先解决三个问题：这个项目是否在维护、怎么最快跑起来、跑完会看到什么。因此首页信息顺序应调整为：项目标题 → 徽章 → 一段定位描述 → Quick Demo → 预期输出截图 → 核心能力说明。

建议加入三类徽章：

| 徽章 | 含义 |
|---|---|
| CI | 展示工作流存在且仓库可校验 |
| Release | 展示已有正式版本 |
| Python | 展示建议 Python 版本 |

Quick Demo 以 `make sample-report` 为主入口，并直接展示输出路径：`summary.json`、`metrics.csv`、`weekly_report.md`、`leaderboard.md/png`。

## CLI 设计

当前仓库有多个脚本，但入口分散。为降低使用门槛，新增包结构：

```text
geo_monitor/
├── __init__.py
├── __main__.py
└── cli.py
```

CLI 首版只封装三个子命令即可：

| 子命令 | 对应脚本 | 作用 |
|---|---|---|
| `run` | `scripts/run_monitor.py` | 生成 raw responses 与 score draft |
| `report` | `scripts/score_run.py` + `scripts/generate_weekly_report.py` | 生成 summary、metrics、weekly report |
| `validate` | `scripts/validate_data.py` | 校验 schema 与样例数据 |

调用形式建议统一为：

```bash
python -m geo_monitor run ...
python -m geo_monitor report ...
python -m geo_monitor validate
```

## Leaderboard 设计

轻量 leaderboard 不追求复杂前端，而是优先做成 **Markdown + PNG 双产物**。输入为 `data/runs/*/summary.json`，输出为：

| 文件 | 作用 |
|---|---|
| `data/leaderboards/model_leaderboard.csv` | 结构化汇总 |
| `data/leaderboards/model_leaderboard.md` | README 可直接引用的表格 |
| `assets/leaderboard-sample.png` | 用于 README 展示的可视化证据 |

首版趋势定义为：对每个模型统计最近若干次 run 的四项指标均值与最新值，并给出 `delta_vs_previous`。如果只有单次 run，则以 `NA` 表示趋势。

## Repair Loop 案例设计

现有 repair validation 只有单条示例，缺乏“动作到变化”的说服力。本轮补三类案例：

| 案例类型 | 目标 |
|---|---|
| 错误信息修复 | 展示通过文档更正与渠道覆盖带来的能力准确率提升 |
| 过时信息修复 | 展示通过文档更新与 changelog 分发带来的生态准确率提升 |
| 竞品植入修复 | 展示通过对比页与实体覆盖带来的提及率与正向率变化 |

每个案例都应包含 `baseline_run_id`、`action_date`、`t_plus_7_run_id`、`t_plus_14_run_id`、`metric_delta` 和 `decision`。

## Collaboration 设计

GitHub 协作入口至少需要三个 issue 模板：

| 模板 | 目的 |
|---|---|
| Bug report | 运行失败、schema 不匹配、样例错误 |
| Feature request | runner、scorer、report、CLI 功能建议 |
| Query pool request | 请求新增行业/产品/语言场景样例 |

`CONTRIBUTING.md` 重点写清“如何新增一个行业样例”：复制模板、填写 query pool、补 schema 校验、生成 sample artifacts、更新 README 索引。

## GitHub About 与 Release 设计

建议为仓库准备以下 About 文案：

> GEO monitoring toolkit for developer tools and open-source projects, with query pools, scoring rubrics, repair loops, CLI, and sample reports.

建议 topics 包括：`geo`、`generative-engine-optimization`、`llm-evaluation`、`developer-tools`、`open-source`、`query-pool`、`content-ops`、`monitoring`。

Release `v0.2.0` 建议突出三项新增能力：

1. executable monitoring workflow；
2. reproducible scoring and schemas；
3. collaboration and release-ready repository surface。
