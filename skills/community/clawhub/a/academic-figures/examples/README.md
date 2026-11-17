# Examples — 示例数据与预览

每个 `.json` 都是可直接运行的示例数据，配合 `scripts/gen_figure.py` 使用。

## 快速体验（推荐）

```bash
# 一键环境准备（首次使用）
python3 scripts/setup_env.py

# 交互演示：选择图表类型，自动用内置数据出图
python3 scripts/gen_figure.py --demo --style glm-hatch --cjk

# 查看全部配色（终端内色块预览）
python3 scripts/gen_figure.py --list-themes
```

## 逐图示例

| 文件 | 命令 | 说明 |
|------|------|------|
| example_bar.json | `python3 scripts/gen_figure.py -t bar -d examples/example_bar.json -o fig.png --cjk` | 分组柱状图（药物疗效） |
| example_arena.json | `python3 scripts/gen_figure.py -t bar -d examples/example_arena.json -o fig.png --show-values --arena "GPT-4"` | 基准对比竞技场图（OSWorld 论文公开数字） |
| example_box.json | `python3 scripts/gen_figure.py -t box -d examples/example_box.json -o fig.png --cjk` | 组间分布箱线图 |
| example_composite.json | `python3 scripts/gen_figure.py -t composite -d examples/example_composite.json -o fig.png --cjk` | 多面板组合图 |
| example_diagram.json | `python3 scripts/gen_figure.py -t diagram -d examples/example_diagram.json -o fig.png --cjk` | 流程示意图（diagram 自管图型） |
| example_dual.json | `python3 scripts/gen_figure.py -t dual_axis -d examples/example_dual.json -o fig.png --cjk` | 双轴折线图（双单位指标） |
| example_forest.json | `python3 scripts/gen_figure.py -t forest -d examples/example_forest.json -o fig.pdf --cjk` | Meta 分析森林图 |
| example_heatmap.json | `python3 scripts/gen_figure.py -t heatmap -d examples/example_heatmap.json -o fig.png --cjk` | 免疫指标相关热力图 |
| example_km.json | `python3 scripts/gen_figure.py -t km -d examples/example_km.json -o fig.png --cjk` | KM 生存曲线（含风险表） |
| example_line.json | `python3 scripts/gen_figure.py -t line -d examples/example_line.json -o fig.png --cjk` | 多组折线图（临床评分） |
| example_prisma.json | `python3 scripts/gen_figure.py -t prisma -d examples/example_prisma.json -o fig.png --cjk` | PRISMA 文献筛选流程图 |
| example_roc.json | `python3 scripts/gen_figure.py -t roc -d examples/example_roc.json -o fig.png --cjk` | ROC 曲线（含 AUC） |
| example_scatter.json | `python3 scripts/gen_figure.py -t scatter -d examples/example_scatter.json -o fig.png --cjk` | 散点图（含相关趋势） |
| example_stacked.json | `python3 scripts/gen_figure.py -t stacked_bar -d examples/example_stacked.json -o fig.png --cjk` | 构成比堆叠柱状图 |

## 真实科研场景示例（realworld/）

`examples/realworld/`：贴近论文真实形态的场景数据（含样本量、真实基因名/终点命名惯例），
可直接作为你论文图 1/2/3 的起点：

| 文件 | 命令要点 | 场景 |
|------|------|------|
| realworld_rct_response.json | `-t grouped_bar --cjk` | RCT 三臂 48 周应答率（n=240） |
| realworld_omics_volcano.json | `-t volcano` | RNA-seq 差异表达（干扰素通路） |
| realworld_survival_km.json | `-t km --cjk` | IgA 肾病三臂生存曲线（36.5 月随访） |
| realworld_oncology_waterfall.json | `-t waterfall --cjk --show-values` | NSCLC II 期最佳缓解瀑布（RECIST n=26） |
| realworld_immunotherapy_subgroup.json | `-t subgroup --stats cox` | 免疫治疗亚组分析森林图（一键拟合） |
| realworld_bmi_mortality_rcs.json | `-t rcs` | BMI 与全因死亡剂量-反应 RCS 曲线 |
| realworld_hcc_nomogram.json | `-t nomogram` | 肝细胞癌预后列线图 |
| realworld_meta_galbraith.json | `-t galbraith` | Meta 异质性 Galbraith 放射图 |
| realworld_sepsis_calibration.json | `-t calibration` | 脓毒症预后模型校准曲线 |
| realworld_sepsis_dca.json | `-t dca` | 脓毒症模型决策曲线分析 |
| realworld_csle_swimmer.json | `-t swimmer` | 肿瘤治疗持续应答泳道图（Swimmer plot） |
| oncology_colon_rmst.json | `-t rmst` | 结肠癌辅助化疗限制平均生存时间（R survival::colon） |
| hematology_mgus_cif.json | `-t cif` | MGUS 竞争风险累计发生率（R mgus2 队列） |
| cardio_fleiss93_aspirin_labbe.json | `-t labbe` | 阿司匹林预防心梗 L'Abbé 图（Fleiss 1993 七 RCT） |
| evidence_rob1_cochrane_rct.json | `-t rob` | Cochrane RCT 偏倚风险交通灯图（RoB 1） |
| evidence_rob2_metformin.json | `-t rob` | RCT 偏倚风险交通灯图（RoB 2） |
| evidence_robins_nonrandomized.json | `-t rob` | 非随机干预研究偏倚风险（ROBINS-I） |
| evidence_quadas_diagnostic.json | `-t rob` | 诊断准确性研究质量评估（QUADAS-2） |

## GLM 黄蓝斜线风格（招牌风格）

```bash
python3 scripts/gen_figure.py -t bar -d examples/example_bar.json -o fig.png --style glm-hatch --cjk
```

`--style glm-hatch` = `--theme glm --hatch`：素雅莫兰迪配色 + 黑色斜纹填充，
打印/黑白场景同样清晰，色盲安全。

## 配色预览

`previews/swatch_<theme>.png`：7 套配色的色板预览图（glm/classic/okabe-ito/nature/lancet/conservative/cool）。
也可随时用 `--theme-swatch <theme> -o out.png` 重新生成。
