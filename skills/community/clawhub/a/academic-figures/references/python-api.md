# Python 编程调用（Python API）

> **何时读我**：在 Python 代码/服务里调引擎。
> **最短路径**：先读「subprocess 推荐」节再写代码。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 两种调用方式：**subprocess 命令行**（推荐——功能最全，自动中文/自动统计标注）
> 与 **import 函数级嵌入**（把引擎当库用，适合集成到你自己的脚本）。
> 两者都 100% 本地运行，数据不出机。

## 方式一：subprocess（推荐）

CLI 是全部功能的完整入口（主题/期刊预设/统计标注/KM 风险表/多格式导出只在这里生效）：

```python
import subprocess, sys, os

SCRIPTS = os.path.join("/path/to/academic-figures", "scripts")
r = subprocess.run(
    [sys.executable, os.path.join(SCRIPTS, "gen_figure.py"),
     "-t", "bar", "-d", "data.json", "-o", "fig1",
     "--multi-format", "tiff,png,pdf",   # v2.6：一次导出多格式
     "--dpi", "300"],
    capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr)                       # 中文报错，含修正建议
print(r.stderr.strip().splitlines()[-1])  # "已保存: ..."
```

退出码约定：`0` 成功；`1` 数据/参数问题（stderr 有中文原因+怎么改）；
`2` `--batch`/`--pipeline` 部分条目失败（详见 .batch-report.json）。

一篇论文 6~8 张图，别逐张调——写成流水线一次出全套（v2.6）：

```python
r = subprocess.run(
    [sys.executable, os.path.join(SCRIPTS, "gen_figure.py"),
     "--pipeline", "analysis.yaml"],     # YAML/JSON 均可
    capture_output=True, text=True)
```

## 方式二：import 函数级嵌入

引擎是纯 Python 模块。最小通路三步：`load_data` → `validate_data` → `gen_*`：

```python
import sys
sys.path.insert(0, "/path/to/academic-figures/scripts")

import matplotlib
matplotlib.use("Agg")                    # 无显示环境必须
import matplotlib.pyplot as plt
import gen_figure as gf

theme = gf.THEMES[gf.resolve_theme("glm")]          # 9 套主题
data = gf.load_data("data.json", chart_type="bar")  # JSON/CSV/TSV/XLSX
fatal, warns = gf.validate_data(data, "bar")        # 统一校验层
assert not fatal, fatal                # fatal 非空 = 不能画（含中文修正建议）
for w in warns:
    print("WARNING:", w)               # 能画但数据可疑

fig, ax = plt.subplots(figsize=theme["figsize"])
gf.apply_base_style(ax, theme)
gf.gen_bar(data, ax, theme, None)      # 最后一个参数是中文字体，无中文传 None
fig.tight_layout()
fig.savefig("fig1.png", dpi=300, bbox_inches="tight", facecolor="white")
```

### 中文文本必读（嵌入路径与 CLI 的唯一差异）

CLI 会自动探测中文并挂字体；嵌入路径要手动补一步，否则中文显示为方框：

```python
cjk_fp, cjk_name = gf.load_cjk_font(None)   # 自动探测系统中文字体
if cjk_name:
    plt.rcParams["font.sans-serif"] = [cjk_name, "DejaVu Sans"] + plt.rcParams["font.sans-serif"]
plt.rcParams["axes.unicode_minus"] = False  # 负号正常显示
# 之后再创建图并把 cjk_fp 传给 gen_*：
gf.gen_bar(data, ax, theme, cjk_fp)
```

### gen_* 函数速查（签名统一：`gen_*(data, ax, theme, cjk_fp, **kwargs)`）

| 函数 | 图型 | data 结构 |
|---|---|---|
| gen_bar | bar / grouped_bar / hbar | {labels, series, errors?, significance?} |
| gen_stacked_bar | stacked_bar | {labels, series} |
| gen_line / gen_scatter | line / scatter | line: {labels, series}；scatter: {x, y, groups?} |
| gen_heatmap | heatmap | {matrix, rows?, cols?} |
| gen_box / gen_violin | box / violin | {labels(组名), series: {组: [原始值]}} |
| gen_raincloud | raincloud 雨云图 | {labels?, datasets: {组: [原始值]}, jitter?, cloud_scale?} |
| gen_slope / gen_volcano | slope / volcano | {items} / {log2fc, pvalue, names?} |
| gen_upset / gen_waterfall | upset / waterfall | {sets} / {change, names?, group?} |
| gen_forest | forest | {labels, estimates, ci_low, ci_high, weights?} |
| gen_km | km | {groups: {组名: [[时间, 事件(1/0)], ...]}} |
| gen_roc | roc | {curves: [{name, fpr, tpr, auc?}]} |
| gen_dual_axis | dual_axis | {labels, left: {}, right: {}} |
| gen_composite | composite | {panels: [...]} |
| gen_diagram / gen_prisma | diagram / prisma | 见 data-formats.md |
| af_v23_charts：gen_funnel / gen_bland_altman / gen_pca / gen_paired / gen_venn / gen_cluster_heatmap | 同名图型 | 见 data-formats.md |

字段权威定义以 `references/data-formats.md` 为准；每个图型的可用 kwargs 见
`--explain <图型>` 输出。

### 常用辅助函数

| 函数 | 用途 |
|---|---|
| load_data(path, chart_type=None, sheet=None) | 读 JSON/CSV/TSV/XLSX；scatter/box 的 CSV 长表自动转换 |
| validate_data(data, chart_type) | 返回 (fatal, warns)，消息全中文带修正建议 |
| resolve_theme(name) / THEMES / THEME_ORDER | 主题解析与色板清单 |
| apply_base_style(ax, theme) | 统一底样式（轴线/网格/字号） |
| load_cjk_font(font_path=None) | 返回 (FontProperties, 字体名)；找不到返回 (None, "") |
| fix_tick_overlaps(fig) | 渲染后调用：检测并消除坐标轴刻度文字重叠 |
| generate_alt_text(chart_type, data, title) | 无障碍描述文本（即 --alt 的内容） |
| af_v23_charts.make_caption(chart_type, data, title) | 中英双语图注（即 --caption 的内容） |

### 嵌入路径的边界（这些请退回 subprocess）

以下能力由 CLI 的 main() 编排，函数级复刻成本高——直接用命令行更省事：

- KM 自动风险表（主图+表轴双子图布局）与自动中位生存标注
- `--stats auto/multi` 显著性括号自动标注、`--compare` DeLong、`--egger`
- composite 面板编排 / 图例合并、prisma 自管布局
- `--journal` 期刊预设（栏宽/字号/最小字号联动）、`--verify` PDF 重叠门禁

经验法则：**单张图嵌入用函数级；成套论文图或要统计标注，走 subprocess / --pipeline。**
