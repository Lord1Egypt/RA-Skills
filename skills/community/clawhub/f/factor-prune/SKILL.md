---
name: factor-prune
description: >
  因子筛选（Factor Prune）技能 —— 在 stock-factor 技能产出初始因子清单（IC/IR 评估结果）后，
  对有效因子做贪心前向选择 + 去相关筛选，精选出一组高有效性、低冗余的因子集合。
  算法：汇总所有因子 → 按 |IR|/IC/time_potential 筛选有效 → 按有效性降序 → 贪心提取最优因子
  → 与剩余因子做相关性评估 → 移除高相关冗余 → 提取下一个 → 如此反复直到收敛或达到上限。
  技能提供两套主实现：
  (1) 文件驱动六步法 `prune_flow.py`（推荐）——脚本直连 QuantAll 自己跑完整个循环，临时文件统一在内存外的 state 目录；
  (2) 缓存矩阵法 `prune.py`——保留相关性矩阵缓存，适合换阈值重放（replay）。
  另有「顶/底10% 分侧筛选」`window_opt.py` / `window_prune.py`：以因子分位窗口为优化对象、coverage 分侧门限 + 联合评分。
  触发：用户提到"因子筛选""因子去冗余""因子精选""factor prune""选有效因子""去相关"
  "精选因子""因子压缩""分位筛选"等关键词时。
  本技能依赖 QuantAll（全A解析）MCP 计算引擎和 stock-factor 技能的输出数据。
  边界：本技能只产出「精选因子清单」（已去冗余），不含因子合成 / 策略回测 / 多因子组合——这些由下游另行处理。
agent_created: true
license: MIT
version: 1.0.0
---

# 因子筛选（Factor Prune）技能

> 本技能只做一件事：**把一大池子因子，筛成一小撮高有效、低冗余的精选集合**。
> 因子合成、策略回测、多因子组合等后续工作不在本技能范围内。

---

## 1. 技能定位与上下游

| 角色 | 技能 / 引擎 | 关系 |
|------|------------|------|
| 上游（输入） | `stock-factor` | 产出初始因子清单 `output/*.xlsx`（含 IC/IR/time_potential/coverage 等评估列），本技能的输入 |
| 本技能 | `factor-prune`（本文件） | 有效因子精选 + 去冗余，产出精选因子清单 |
| 计算依赖 | `quantall-mcp`（全A解析） | 相关性计算由 `batch_factor_corr` 完成 |
| 下游（可选） | 因子合成 / 回测技能 | 拿精选清单继续做复合因子、策略回测等 |

**产出边界**：一份「精选因子清单」（xlsx，含 code/IR/IC/time_potential/coverage 等），可直连 QuantAll 使用。本技能不做正交/合成、不做回测。

---

## 2. 筛选算法（贪心前向选择 + 去相关）

### 2.1 流程

```
1. 汇总：读取 stock-factor 的所有 output/*.xlsx，合并为一张总表
2. 筛选有效：保留满足阈值（|IR| / |IC| / time_potential，可任意 AND 组合）的因子
3. 排序：按所选指标（默认 |IR|）降序；低 coverage 因子整体置底
4. 提取第一个（有效性最高的）作为基准
5. 相关性评估：用 QuantAll batch_factor_corr 计算基准因子 vs 所有剩余因子的 IC
6. 去冗余：移除 |IC| > corr_threshold 的候选（被基准"吸走"的同质因子）
7. 提取下一个：从存活因子中选有效性最高的
8. 重复 5-7，直到无候选 或 选中数达 --max-selected
9. 输出：最终精选因子清单（xlsx，含完整指标与来源）
```

### 2.2 核心参数

| 参数 | 默认值 | 含义 | 调整建议 |
|------|--------|------|----------|
| `ir_threshold` | `prune_flow` prescreen 默认 0.3；`prune.py` run 默认 0.5 | 因子有效性阈值，\|IR\| > 此值才保留 | 实测 \|IR\| 分布自然断点在 0.4→0.5：>0.3 有 542 个、>0.5 仅 121 个。**推荐 0.5**（候选少、跑得快） |
| `corr_threshold` | `prune_flow` run 默认 0.5；`prune.py` run 默认 0.35 | 冗余阈值，\|IC\| > 此值视为冗余 | ⚠️ 0.8 在 540 因子上几乎无效（\|IC\| 中位数仅 0.22，超 0.8 不足 0.6%）。**推荐 0.35~0.5**（明确去冗余又不误杀） |
| `feature_days` | 5 | 未来收益天数（与上游一致） | 与 stock-factor 保持一致 |
| `max-selected` | 50 | 最终选中上限 | 控量用；设大则尽量多留 |
| `coverage-floor` | 0.4 | 低于此 coverage 的因子整体置底 | 应对停牌/上市晚/退市；分侧筛选用 0.07 |
| `per-file` | 60 | 单文件预筛保留 top-N | 控制聚合规模，便于因子家族扩展 |
| `aggregate-keep` | 200 | 聚合后保留 top-M 进入去相关 | 控制轮次上限 |
| `metric` | `abs_IR` | 排序主指标 | 可选 `IC` / `time_potential` |

> **默认推荐（prune_flow）**：`prescreen --ir-threshold 0.3 --per-file 60` → `init`（聚合保留 top-200）→
> `run --corr-threshold 0.5 --max-selected 50`。即初步放宽多候选、相关性要求适中、最终控 50 个。

### 2.3 coverage（有效数据比例）感知排序

- 因子 xlsx 含 `coverage` 列（取值 0~1，= 有效数据点数 / 全样本×全市场点数）。停牌、上市晚、退市会拉低它；财报类因子因 NaN 填充略高属正常。
- **排序规则**：`coverage < --coverage-floor` 的因子整体排到末尾；其余按所选指标降序。满足"有效数据大的因子往前排、覆盖率偏低的置底"。
- 若该列缺失：用 `start_date/end_date/stock_count` 推算 proxy（≈1.0，仅作安全占位，无区分度）。要启用真实 coverage 排序需重导数据（让 QuantAll 把 coverage 写入 xlsx）。

### 2.4 time_potential 基线（时间稳定性）

- 随机白噪声的 time_potential ≈ 1/√5 ≈ **0.447**（见 `time_potential_baseline.py`）。
- 真实因子 time_potential 仅 ≈0.45 时与随机噪声无异；**建议阈值 ≥0.55~0.6** 才视为有真实时间结构。

### 2.5 为什么这样设计

- **贪心而非穷举**：N 因子组合是 O(2^N)，贪心每轮一次 `batch_factor_corr` 是 O(N²)，通常 20–50 轮即收敛。
- **按有效性降序选**：优先保留预测力最强的"锚因子"，被移除的冗余因子可替代性高。
- **中间状态可追溯**：每轮选中/移除都记录，可审计、可中断恢复。

---

## 3. 依赖与数据准备

### 3.1 前置依赖

1. **stock-factor 技能**：已完成因子 IC/IR 评估（其 `output/*.xlsx` 已生成）。
2. **QuantAll（全A解析）引擎**：已安装并启动（8686 端口可连）。
3. **Python 环境**：需 pandas + numpy + openpyxl。推荐直接用 QuantAll 的 venv：
   ```
   <QuantAll>/scripts/.venv/Scripts/python.exe <script>.py <command>
   ```
   或自行 `pip install pandas numpy openpyxl`。

### 3.2 输入因子库

将 stock-factor 的 `output/*.xlsx` 放进本技能的 `scripts/output/`（当前已内置 7 个家族，合计 1012 个因子）：

| 文件 | 因子数 | 来源 |
|------|--------|------|
| `facotr-Qlib_alpha158.xlsx` | 158 | Qlib Alpha158 |
| `facotr-Qlib_alpha360.xlsx` | 360 | Qlib Alpha360 |
| `factor-Alpha101.xlsx` | 101 | WorldQuant Alpha101 |
| `factor-GTJA_Alpha191.xlsx` | 191 | 国泰君安 Alpha191 |
| `factor-stock_daily.xlsx` | 12 | 基础量价/估值因子 |
| `factor-stock_report.xlsx` | 105 | 财务质量/成长/偿债因子 |
| `factor-TA_Indicators.xlsx` | 85 | TA-Lib 技术指标 |

经 \|IR\|>0.3 筛选后约 540+ 个有效因子。

---

## 4. 使用流程

### 4.1 方式 A（推荐）：prune_flow.py 文件驱动六步法

> 设计目标：临时文件统一在一个目录管理、脚本自己直连 QuantAll 跑完循环、AI 几乎零负担。

```bash
VENV="<QuantAll>/scripts/.venv/Scripts/python.exe"
$VENV scripts/prune_flow.py prescreen --ir-threshold 0.3 --per-file 60   # 单文件预筛（可扩展新家族）
$VENV scripts/prune_flow.py init                                        # 聚合 + 全局 coverage 排序 + 加编号
$VENV scripts/prune_flow.py run --corr-threshold 0.5 --max-selected 50  # 直连 QuantAll，跑完自动 finalize
$VENV scripts/prune_flow.py status                                      # 查看中间信息（含 coverage 分布）
$VENV scripts/prune_flow.py finalize                                    # 仅重新生成最终 xlsx
$VENV scripts/prune_flow.py reset                                       # 清空临时文件，重跑
```

六步 ↔ 命令映射：

| 步骤 | 命令 | 说明 |
|------|------|------|
| 0 单文件预筛 | `prescreen` | 对 `output/` 下每个 xlsx 单独预筛，取每文件 top-N → 中间文件。新家族只需补这一份 |
| 1-2 聚合+降序+编号 | `init` | 聚合 → 全局 coverage 感知排序 → 降序 → name 加前缀 |
| 3-5 循环去相关 | `run` | 取首行作基准 → 生成相关性任务 → QuantAll 执行 → 移除高相关 → 回写，直到达上限或池空 |
| 6 输出 | （`run` 结束自动 `finalize`） | 去前缀 → `scripts/factor-pure.xlsx` |

最终输出：`scripts/factor-pure.xlsx`（含 code/IR/IC/time_potential/coverage/source_file）。

### 4.2 方式 B：prune.py 缓存矩阵法

> 保留相关性矩阵缓存（`corr_matrix.json`），适合换阈值重放，不重复计算已算过的配对。

```bash
$VENV scripts/prune.py run  --ir-threshold 0.5 --corr-threshold 0.35   # 全自动：直连 QuantAll 跑完循环
$VENV scripts/prune.py step --ir-threshold 0.5 --corr-threshold 0.35   # 一步一停，便于人工监控
$VENV scripts/prune.py replay --save                                  # 仅用缓存重放贪心（不调 QuantAll）
```

最终输出：`scripts/output/pruned_factors.xlsx`（精选因子）+ `scripts/output/pruned_removed.xlsx`（被移除因子，含 `removed_by` / `corr_IC`）。

### 4.3 命令速查

| 脚本 | 命令 | 用途 |
|------|------|------|
| `prune_flow.py` | `prescreen` / `init` / `run` / `status` / `finalize` / `reset` | 六步法全流程（推荐） |
| `prune.py` | `run` / `step` / `replay` / `init` / `update` / `status` / `finalize` / `reset` / `config` | 缓存矩阵法 / AI 编排 |

### 4.4 输出说明

**`factor-pure.xlsx`（prune_flow 最终输出）** / **`pruned_factors.xlsx`（prune.py 输出）**：

| 列 | 含义 |
|----|------|
| `rank` / `name` | 精选排名（1=最先被选，有效性最高）/ 因子名 |
| `code` | 因子的 QuantAll 代码（可直接复制使用） |
| `IR` / `IC` | 信息比率 / 信息系数 |
| `abs_IR` | \|IR\|（排序依据） |
| `time_potential` | 时间稳定性 |
| `coverage` | 有效数据比例 |
| `source_file` | 来源 xlsx |
| `round` | 第几轮被选中 |

**`pruned_removed.xlsx`（prune.py）**：`name` / `removed_by`（被哪个已选因子判定冗余）/ `corr_IC` / `round` / `source_file`。

---

## 5. 顶/底10% 分侧筛选（window_opt.py / window_prune.py）

把优化对象从"整体 IC"换成因子的**两个分位窗口**：`top10%`（因子值最高的 10% 股票）与 `bottom10%`（最低的 10%）。每侧各有 IC/IR/time_potential/coverage 指标（来自 QuantAll factor_analysis）。

**分侧 coverage 门限**：某侧 `coverage < 0.07` → 该侧有效性置 0（放弃该侧），但**整行保留不删因子**；只有两侧都 <0.07 才整因子无贡献，自然排到池尾。
**联合评分**：`score = |top10%_IR_eff| + |bottom10%_IR_eff|`（放弃侧已置 0）。

| 脚本 | 模式 | 输出 |
|------|------|------|
| `window_opt.py` | 离线（不碰 QuantAll），纯分侧门限 + 联合评分排序 | `scripts/factor-window-opt.xlsx`（不覆盖其它） |
| `window_prune.py` | 接上 QuantAll 逐对去相关（score 最高作基准，移除 \|corr\|>阈值 的候选） | `scripts/factor-pure-topbottom.xlsx`（不覆盖其它） |

> 命名约定：分侧方案输出**换名不覆盖** `factor-pure.xlsx`，多套结果可并存对比。

---

## 6. 分析评估工具（筛选配套）

| 脚本 | 用途 | 产出 |
|------|------|------|
| `factor_heatmaps.py` | 单因子热力图：X=因子十分位, Y=5日收益十分位, 权重=5日收益（需先有 `factor-pure.xlsx`） | 每因子 rank-IC / 十分位差 |
| `factor_pairs.py` | 双因子热力图：X/Y=两个不同因子十分位, 权重=5日收益；遍历所有无序因子对 | 因子相关性冗余度 / 对角收益差 |
| `probe_heatmap.py` | 单因子热力图快速探查 | 同上 |
| `time_potential_baseline.py` | 随机数 time_potential 基线标定（白噪声/AR(1)/随机游走对比） | 基线结论（≈0.447） |

> 双因子热力图价值：看两因子**如何共同**预测收益，以及是否冗余（密度图对角条纹 = 高相关 = 组合无增量）。

---

## 7. QuantAll 运维红线（单实例 + 忙锁）

- **核心事实**：QuantAll 只能跑**单个实例**，内部用一把"单任务锁"串行处理请求（返回"有其它任务在执行"即忙）。
- **两类事件**：
  1. **进程自退（合法重启）**：长任务结束后端口 8686 关闭、新连接被拒。此时需重启单实例（`quantall/scripts/.venv/Scripts/python.exe Start_QuantAll.py` 后台）。
  2. **重复实例抢锁（须避免）**：误起第二个 `Start_QuantAll.py` → 两实例抢同一锁/端口 → 永久 busy。**修复**：杀掉多余实例，只留一个 PID 监听 8686。
- **纪律**：连接**已有**实例，绝不自己再起一个；忙时退避重试（如 `sleep 15s × N`），不新起进程、不盲目查杀。
- **非 OOM**：busy 来自锁竞争或长任务占用，不是内存溢出；单次任务几小时内稳定。

---

## 8. 版本说明

### v1.0.0
- **整理首版**：从旧 `factor-prune`（曾含多因子组合/回测等后续分析内容）清理而来，**只保留因子筛选**。
- 保留：筛选主流程 `prune_flow.py`（六步法，推荐）、`prune.py`（缓存矩阵法）、顶/底10% 分侧筛选 `window_opt.py` / `window_prune.py`、评估工具 `factor_heatmaps.py` / `factor_pairs.py` / `probe_heatmap.py` / `time_potential_baseline.py`、数据 `data/db_translate.json`、启动入口 `Start_QuantAll.py`、输入因子库 `scripts/output/*.xlsx`。
- 移除：多因子合成（M3 公式）、"排雷器"策略用法、因子批量线性组合工具（run_codes/multifact2）、市场分析/回测等所有后续分析脚本与产物、运行态 `state/` 与日志。
- 技能边界明确为「产出精选因子清单」，不含因子合成 / 策略回测 / 多因子组合。
