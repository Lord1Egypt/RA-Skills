# DevTool Answer Monitor 新手上手（5 分钟版）

> 目标：你不需要先理解全部概念，也可以先跑出第一份可读结果。

## 你会得到什么

跑完后，先看这 3 个文件。

| 文件 | 说明 |
|---|---|
| `data/runs/quickstart-run/raw_responses.jsonl` | quickstart 生成的原始回答证据 |
| `data/runs/sample-run/weekly_report.md` | 仓库内样例摘要重放出的周报快照 |
| `assets/leaderboard-sample.png` | 默认多模型对比图 |

## 0. 准备条件

请先确保本机至少有以下环境。

| 需要项 | 说明 |
|---|---|
| `git` | 用来克隆仓库 |
| `python3` | 建议 3.9+ |
| 终端 | macOS Terminal、iTerm 或 Linux shell |

如果你不确定本机环境是否齐全，先运行：

```bash
make doctor
```

## 1. 安装

```bash
git clone https://github.com/veeicwgy/devtool-answer-monitor.git
cd devtool-answer-monitor
bash install.sh
```

## 2. 一条命令跑通

```bash
bash quickstart.sh
```

这一步会用仓库内样例数据跑完整演示流程，不需要你先配置 API key。

## 3. 看结果

### A. 周报

打开：`data/runs/sample-run/weekly_report.md`

你会看到四个核心指标。

| 指标 | 含义 |
|---|---|
| Mention Rate | 是否被提到 |
| Positive Mention Rate | 被提到时是否偏正向 |
| Capability Accuracy | 对产品能力的描述是否准确 |
| Ecosystem Accuracy | 对生态、集成与关系的描述是否准确 |

### B. 图表

打开：`assets/leaderboard-sample.png`

这是模型维度的对比快照，用来先理解“不同模型怎么看这个项目”。

### C. 原始回答

打开：`data/runs/quickstart-run/raw_responses.jsonl`

这是 quickstart 过程中采集到的原始证据，后续做标注、复盘和修复时都会用到。

## 4. 我该走哪种模式

| 如果你现在的情况是 | 该用什么 |
|---|---|
| 没有 API key，只想先看流程 | `bash quickstart.sh` |
| 已经收集了一批手工回答，想导入评估 | manual mode |
| 要做持续、真实、多模型监控 | API mode |

## 5. 常见问题

| 问题 | 修复建议 |
|---|---|
| `python` not found | 改用 `python3`，并确认系统已安装 Python |
| 脚本权限报错 | 运行 `chmod +x install.sh quickstart.sh scripts/doctor.sh` 后重试 |
| 图没有生成 | 先确认 `bash quickstart.sh` 已成功执行，再检查 `assets/` 是否可写 |
| 看不懂四个指标 | 先读 `docs/metric-definition.md`，不用一次全部理解 |

## 6. 下一步

建议按这个顺序继续。

| 顺序 | 下一步 |
|---|---|
| 1 | 复制一份你自己的 Query Pool 到 `data/query-pools/` |
| 2 | 用 manual mode 导入你自己的回答样本 |
| 3 | 对比第 1 次和第 2 次周报差异 |
| 4 | 再进入 repair loop（T+7 / T+14） |

> 如果你只记住一句话：先跑通，再理解；先复现，再优化。
