# 模板库（v2.6 全图型覆盖）

41 个端到端模板 = 场景数据 JSON + 推荐命令 + 图注说明，**覆盖全部 41 种图型**（v5.7 增 cif，v5.9 增 rmst，v6.1 增 rob，v7.8 增 hero-panel composite）。用法：

```bash
cp templates/01-meta-forest.json my_data.json
# 编辑 my_data.json，把示例数字换成你的真实数据
python3 scripts/gen_figure.py -t forest -d my_data.json -o forest.pdf --theme okabe-ito --verify
```

## 场景模板（01–16）

| 模板 | 场景 | 图型 | 推荐命令要点 |
|---|---|---|---|
| 01-meta-forest | 荟萃分析 | forest | enhanced 格式：权重气泡+events 列+异质性脚注 |
| 02-rct-baseline-bar | RCT 结局对比 | bar | +journal jama；significance 手工标注 |
| 03-survival-km | 生存分析 | km | 风险表+log-rank 自动标注 |
| 04-diagnostic-roc | 诊断试验 | roc | 多曲线 AUC 自动标注 |
| 05-correlation-heatmap | 变量相关 | heatmap | RdBu_r ±1 |
| 06-prisma-review | 系统综述筛选 | prisma | 算术自检，对不上拒绝出图 |
| 07-dose-response-line | 剂量-反应 | line | 误差带 |
| 08-panel-composite | 期刊主图 | composite | A/B/C 面板；--alt 生成图注描述 |
| 09-survey-stacked | 构成比 | stacked_bar | 百分比 + 总数 |
| 10-cn-journal-hbar | 中文期刊横柱 | hbar | --journal cn-core 自动开中文；--alt |
| 11-rct-grouped-bar | 两组×多时点对比 | grouped_bar | 误差棒+显著性标注 |
| 12-dose-response-scatter | 浓度-反应分组散点 | scatter | groups 分色+趋势线 |
| 13-qol-box | 评分分布比较 | box | --stats auto 显著性括号 |
| 14-cytokine-violin | 分布形状对比 | violin | --stats multi 全两两 |
| 15-lab-trend-dual-axis | 双轴指标趋势 | dual_axis | 左右轴各一系列 |
| 16-study-design-diagram | 研究设计/CONSORT | diagram | blocks+arrows 定位 |

## 图型速查模板（按图型命名，覆盖其余 21 种）

| 模板 | 图型 | 模板 | 图型 |
|---|---|---|---|
| bland_altman.json | bland_altman 一致性 | pca.json | pca 得分图 |
| cluster_heatmap.json | cluster_heatmap 聚类热图 | paired.json | paired 配对变化 |
| funnel.json | funnel 漏斗图 | venn.json | venn 韦恩/欧拉图 |
| slope.json | slope 斜率图（两时点） | upset.json | upset 集合交集图（v4.7） |
| waterfall.json | waterfall 肿瘤缓解瀑布图（v4.8） | raincloud.json | raincloud 雨云图（v4.9） |
| swimmer.json | swimmer 游泳图（v4.10） | ridgeline.json | ridgeline 山脊图（v5.0） |
| dumbbell.json | dumbbell 哑铃图（v5.1） | calibration.json | calibration 校准曲线（v5.2） |
| dca.json | dca 决策曲线（v5.2） | nomogram.json | nomogram 列线图（v5.3） |
| rcs.json | rcs 非线性剂量反应（v5.4） | subgroup.json | subgroup 亚组森林图（v5.5） |
| galbraith.json | galbraith Galbraith 径向图（v5.6） | cif.json | cif 竞争风险累计发生率（v5.7） |
| volcano.json | volcano 火山图 | | |

> v2.6 起模板与图型一一对应（v4.9 增 raincloud）；不确定用哪个图型可对数据跑
> `python3 scripts/gen_figure.py --suggest -d 你的数据.json`。

每个 JSON 顶部有 `_scene/_chart_type/_command/_caption_template` 元字段，渲染时会被忽略。
示例数字仅示意，发表前请替换为真实数据。
