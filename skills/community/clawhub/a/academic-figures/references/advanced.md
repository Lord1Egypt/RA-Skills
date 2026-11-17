# Advanced Usage / 深水区进阶

> **何时读我**：要统计深用：Cox/bootstrap/Meta/敏感性分析。
> **最短路径**：Ctrl-F 功能名（cox / egger / sensitivity）。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 从主文档外移的进阶内容：统计深水区与投稿精修。主文档保持精简，按需查阅本文件。

## Statistics Deep-Dive (v2.3)

- **KM auto risk table + log-rank**: raw `[time, event]` data with >=2 groups now
  auto-renders a "Number at risk" table under the plot and auto-runs a
  Mantel-Haenszel log-rank test (annotated in-plot). `--no-risk-table` opts out;
  `--risk-times T1,T2,...` sets custom display times. Precomputed survival curves
  are now detected and drawn correctly.
- **`--stats multi`** (box/violin): all-pairs comparisons — ANOVA+Tukey HSD when
  all groups pass Shapiro, otherwise Kruskal-Wallis + Dunn with Hochberg adjust.
- **ROC `--compare`**: paired DeLong test between >=2 model AUCs (needs `labels`
  plus per-curve raw `scores`; fpr/tpr-only curves cannot be DeLong-tested).
- **New chart types**: `-t funnel` (Meta funnel, DL pooled line, `--egger`),
  `-t galbraith` (v5.6 Meta heterogeneity radial: precision 1/SE × standardized
  effect, pooled fixed-effect line, ±1.96 band, per-study outlier stderr report;
  same schema as funnel — use both together: funnel for small-study asymmetry,
  Galbraith to name the heterogeneity sources),
  `-t bland_altman` (LoA), `-t pca` (scores + group ellipses + top-5 loadings),
  `-t paired` (before-after lines + paired test), `-t venn` (2-3 sets, exact
  region counts; `--area` for area-proportional Euler mode), `-t cluster_heatmap`
  (Ward-reordered matrix, <=3000 rows).

## Submission Polish (v2.5)

- **`--annotate "x,y:text"`** — reviewer-request tweaks on the exact data point:
  arrow annotation at data coordinates, repeatable, with automatic declutter
  (texts repel + spring back to anchor; arrows follow). Category axes accept
  tick labels instead of numbers:
  ```bash
  python3 scripts/gen_figure.py -t scatter -d d.json -o f.png \
      --annotate "3.2,5.1:p=0.01" --annotate "6.0,7.4:outlier"
  python3 scripts/gen_figure.py -t bar -d d.json -o f.png --annotate "高剂量,4.2:显著上调"
  ```
  Coordinates must land inside the plotted range (or match a tick label);
  otherwise the CLI exits 1 listing the valid ranges/labels.
- **`--legend-loc LOC`** — explicit legend position (best/upper right/.../center);
  **`--legend-outside`** — moves the legend outside the plot area; on composite
  figures it merges all panels' legends into one shared figure legend
  (duplicate entries deduped).
- **venn `--area`** (Euler mode) — circles sized so areas match region counts
  (default mode stays equal-circle with exact numbers). 2 sets: exact analytic
  layout; 3 sets: least-squares fit of centers+radii (circles cannot realize
  every region combination exactly — achieved fit is reported on stderr).
  Region counts now also accept a dedicated `"regions"` key:
  `{"regions": {"A": 30, "B": 25, "AB": 9}}` (2 sets, exactly 3 keys) or all
  7 keys for 3 sets. (The numeric form of `"sets"` documented in v2.3 never
  parsed — fixed in v2.5.)
- **NEJM / Science color themes** — official-style palettes joining lancet;
  `--journal nejm|science` auto-selects the matching theme (see Color Themes).
- Library exception Chinese mapping expanded 9 → 18 (ParserError → "CSV 解析失败",
  MemoryError → "数据规模超出可用内存", InvalidFileException → "不是有效的 xlsx", ...).

## 统计深水区（中文）

## 统计深水区（v2.3）

- **KM 自动风险表 + 自动 log-rank**：原始 `[时间, 事件]` 数据且 >=2 组时，自动在图下渲染
  "Number at risk" 风险表、自动做 Mantel-Haenszel log-rank 检验并图内标注；
  `--no-risk-table` 关闭；`--risk-times 2,6,10` 自定义显示时间点。预计算生存曲线格式自动识别正确绘制。
- **KM 自动中位生存（v2.4）**：每组自动计算中位生存时间及 95%CI（Greenwood log-log 法），与 log-rank 同框标注；`--no-median` 关闭。曲线未降到 50% 时如实标注"未到达"。
- **forest --sensitivity（v2.4）**：留一法敏感性分析——自动省略每项研究重新合并，13+N 行画在同一图下方；需 se_list 或对称 CI。
- **`--stats multi`**（box/violin）：全两两比较——全组过 Shapiro→ANOVA+Tukey HSD；
  否则 Kruskal-Wallis+Dunn（Hochberg 校正）。
- **ROC `--compare`**：>=2 个模型 AUC 的配对 DeLong 检验（需 labels + 各曲线原始 scores）。
- **新图型**：`-t funnel`（Meta 漏斗，DL 合并线，`--egger` 不对称检验）、`-t galbraith`
  （v5.6 Meta 异质性径向图：精度 1/SE×标准化效应、过原点合并线、±1.96 同质带、离群逐个报名；
  与 funnel 同 schema——漏斗看小样本不对称，径向图点名异质性来源）、`-t bland_altman`
  （一致性界值）、`-t pca`（得分+分组椭圆+载荷 top5）、`-t paired`（配对前后线+配对检验）、
  `-t venn`（2~3 集合精确区域计数；`--area` 面积比例 Euler 模式）、`-t cluster_heatmap`（Ward 聚类重排，行数上限 3000）。
- **`--pipeline analysis.yaml`**（v2.6）多图流水线：defaults 全局默认 + figures 逐图清单，
  一篇论文全部图表一条命令出齐（YAML 需 pyyaml，JSON 免依赖；原 --batch 保留）；
  **`--multi-format tiff,png,pdf`**（v2.6）一次渲染多格式导出，文件名同源；
  **`--batch figures.json`** 批量出图（逐项独立进程，输出 .batch-report.json 汇总）；
  **`--caption`** 生成中英双语期刊式图注（<输出名>.caption.txt）。
- 极端输入统一友好报错（中文提示+修正建议，绝不裸 traceback）；写出失败自动重试一次。

## 投稿精修（中文）

## 投稿精修（v2.5）

- **`--annotate "x,y:文字"`**——审稿改稿第一刚需：在数据坐标处画箭头注释，可重复使用；
  文字自动防重叠（互斥+锚点回弹，箭头跟随）。类别轴可直接写刻度标签：
  ```bash
  python3 scripts/gen_figure.py -t scatter -d d.json -o f.png \
      --annotate "3.2,5.1:p=0.01" --annotate "6.0,7.4:离群点"
  python3 scripts/gen_figure.py -t bar -d d.json -o f.png --annotate "高剂量,4.2:显著上调"
  ```
  坐标须落在图内数据范围（或匹配刻度标签），否则 exit 1 并列出可用范围/标签。
- **`--legend-loc 位置`**——图例九宫格定位（best/upper right/…/center）；
  **`--legend-outside`**——图例移到绘图区外侧；组合图自动合并为全图共享图例（同名去重）。
- **venn `--area`**（Euler 面积比例模式）——圆的大小与交集面积按区域计数比例
  （默认仍为等圆示意+精确数字）。2 集合解析解精确；3 集合圆心+半径联合最优拟合
  （圆无法精确实现任意区域组合，实际拟合偏差在 stderr 如实报告）。
  区域计数也可用独立键：`{"regions": {"A": 30, "B": 25, "AB": 9}}`（2 集合恰 3 键，
  3 集合恰 7 键）。（v2.3 文档承诺的数字型 `"sets"` 从未可用，v2.5 修复。）
- **NEJM / Science 配色主题**——与 lancet 并列的官方风色板；
  `--journal nejm|science` 自动联动同款配色（见配色方案）。
- 库异常中文映射 9 → 18 条（ParserError→"CSV 解析失败"、MemoryError→"数据规模超出
  可用内存"、InvalidFileException→"不是有效的 xlsx" 等）。

## 临床预测模型评价三件套（v5.0~v5.2 深水区）

预测模型论文（Logistic/Cox/机器学习）审稿人默认要看三件事，对应三种图：

| 问题 | 图型 | 图上看什么 |
|---|---|---|
| 分得开吗（判别） | `-t roc`（`--compare` 多模型配对 DeLong） | AUC 及其 CI；两模型 AUC 差的 p |
| 概率准吗（校准） | `-t calibration`（v5.2） | 各箱点贴对角线=校准好；系统性偏上=预测低估、偏下=高估 |
| 用了有收益吗（临床效用） | `-t dca`（v5.2） | 模型曲线在哪个阈值区间同时压过「全部干预」与「不干预」 |

**calibration 分箱实践**：外部分验证集优先；8~10 箱、每箱 ≥30 例是常见惯例
（本引擎不做自动分箱——分箱口径属于方法学决策，须写入你的统计方法段）。
`hl_p` 的解读注意：大样本下 Hosmer-Lemeshow 几乎必然显著，p>0.05 不能单独
证明校准好，必须配合图形判读一起报告。误差棒=观察率 95%CI（你可用 Wilson
近似自算后随箱给出，见 templates/calibration.json）。

**DCA 解读**：纵轴净收益=每 100 人中净真阳性数（Vickers 定义，受益-受害加权）。
横轴阈值必须取自临床决策点（「预测概率高于多少才干预」），不是统计网格；
报告时写出获益区间（如 0.20~0.65）并与两参照策略对照。`prevalence` 用验证
队列真实患病率；模型间区分度小时净收益曲线会贴近，别用轴缩放放大视觉差异。

三件套同队列出图的推荐命令骨架：

```bash
python3 scripts/gen_figure.py -t roc          -d pred.json -o fig_roc.png --cjk
python3 scripts/gen_figure.py -t calibration  -d pred.json -o fig_cal.png --cjk
python3 scripts/gen_figure.py -t dca          -d pred.json -o fig_dca.png --cjk
# 或一步投稿包（自动 verify+色盲安全+pdf/png 双格式+复跑包）：
python3 scripts/gen_figure.py -t calibration -d pred.json -o fig_cal.png --pub-ready --cjk
```

## 多面板组合配方（composite 深水区）

- **语法**：`panels: [{type, data, title, span?}, ...]`；`span:[rows,cols]`
  让某面板占多格（跨格冲突会在渲染前报错，具体到面板序号）。
- **典型论文图式**：A=原始分布（box/violin/raincloud）+ B=个体走向
  （paired/slope）+ C=汇总统计（bar/forest）；审稿人最认「原始+个体+汇总」
  三位一体，单柱状图被打回时优先补 A/B 两层。
- **面板间一致性**：同一变量跨面板必须同色（配色方案 §四语义色一致规则）；
  组合图图例可用 `--legend-outside` 合并为全图共享图例（同名自动去重）。
- **禁嵌套**：composite/diagram/upset 不能再作为面板类型嵌套（校验会拦截）。

## 统计标注决策树（--stats 怎么选）

```text
两组比较 → --stats auto   （Shapiro 过→配对/独立 t；不过→Wilcoxon/Mann-Whitney，自动选择并标注方法名）
多组两两  → --stats multi （全组正态→ANOVA+Tukey HSD；否则 Kruskal-Wallis+Dunn+Hochberg 校正）
配对数据  → paired -t + --stats auto（n>=6 才标注，不足时 stderr 提示效力不足）
自跑检验  → JSON significance 键直接给 "组: p 值"（引擎只标注不计算，可溯源）
```

铁律：SD 与 SE 误差棒在 JSON `errors` 里给什么画什么，图注必须写明是哪种；
显著性星号必须有对应检验（自己编星号=造假边缘）。

## 投稿一键包与数字溯源（v5.0~v5.2）

**`--pub-ready` 一条命令展开五件套**：`--verify`（PDF 像素级重叠门禁）+
色盲安全主题（默认 okabe-ito，`--pub-ready theme,NAME` 换）+ 多格式导出
（pdf 矢量+png 600dpi）+ **复跑交付包** `<输出>.repro/`（v5.2 合流）+
数字对账侧车。包内逐文件：

| 文件 | 用途 |
|---|---|
| `command.txt` | 逐字可复跑的精确命令 |
| 数据副本 | 与原始输入逐字节一致 |
| 成图副本 | 全部导出格式（pdf+png）逐字节一致 |
| `audit.json` | 描述统计由输入**独立重算**（纯计数零推断）+输入 sha256 指纹 |
| `README_REPRODUCE.md` | 双语复跑说明 |

审稿人问「图上的数怎么来的」时，把 `.repro/` 整目录作为补充材料提交即可；
确定性引擎保证同输入+同命令=同字节输出。verify FAIL（exit 2）时不会产出
复跑包——复跑包里的图必然已过重叠门禁。

**投稿前自检清单**：尺寸用 `--journal nature|lancet|science|nejm|cma|cn-core`
预设（栏宽/字号下限/字体按各刊作者指南）；灰度印刷自检加 `--hatch`（黑白
打印同色深浅难分时靠斜纹区分系列）；最小字号不低于目标期刊下限（nature 5pt /
lancet 6pt，引擎按预设自动把守）；最终交付 PDF 走 `--verify`，位图走 600dpi。
