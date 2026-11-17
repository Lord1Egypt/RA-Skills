# 速查卡（Cheat Sheet）

> **何时读我**：已经知道图型，要一条能跑的命令骨架。
> **最短路径**：Ctrl-F 图型名 → 复制命令行 → 换数据文件。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 一页速查：41 种图型命令骨架、全量参数、退出码、边界 Top 5。
> 细节：`--explain <类型>`；数据格式 `references/data-formats.md`；参数交互 `references/limits.md`。

## 一、图型命令骨架（通用格式）

```bash
python3 scripts/gen_figure.py -t <类型> -d <数据.json> -o <输出.png> [参数]
```

| 类型 | 常用追加参数 |
|------|-------------|
| bar | `--stats auto`（显著性）；`--hatch`（黑白印刷） |
| hbar / stacked_bar | `--horizontal`（等同 hbar）；构成比标签默认开 |
| box / violin | `--stats auto`；配对数据改用 paired |
| paired | 两组前后等长数据 |
| scatter | `--trend`（趋势线，默认开） |
| line / dual_axis | 多系列 JSON；dual 左右轴字段见 data-formats |
| heatmap | `--cmap NAME --vmin --vmax` |
| cluster_heatmap | `--downsample 2000`（>1500 行建议） |
| forest | `--stats cox`（多因素 HR）；Meta 加 `--egger`（funnel 才有） |
| km | 原始 [时间,事件] 格式才有风险表/log-rank |
| roc | `--compare`（多模型 DeLong） |
| venn | `--area`（面积比例 Euler，2~4 集合） |
| upset | `sets{}` 元素列表（≥5 集合）；`top_n`/`sort`/`min_size` 控制交集展示（v4.7） |
| waterfall | `change[]` 每例最佳缓解%；`group` RECIST 着色、`pr_cut/pd_cut` 阈值线（v4.8） |
| raincloud | schema 同 violin（labels+datasets）；`jitter`/`cloud_scale` 可调（v4.9） |
| swimmer | `end[]` 每例时长必填(>0)；`start/names/group/milestones/ongoing/ref_lines` 可选；`sort=duration|input`（v4.10） |
| ridgeline | schema 同 violin（labels+datasets）；`overlap` 0~0.95、`sort=median`；单值组退化告知（v5.0） |
| dumbbell | `from[]`+`to[]` 等长必填；`labels/from_label/to_label` 可选；`sort=gap|input|to`、`show_values/show_gap`（v5.1） |
| calibration | `bins[]` 或 `predicted/observed[]` 平行数组；`ci_lo/ci_hi/n/hl_p/smooth` 可选（v5.2） |
| dca | `thresholds[]` 严格升序 (0,1)+`models[{name,net_benefit}]`；`prevalence` 或 `treat_all` 参照、`show_none` 可关（v5.2） |
| nomogram | `variables[{name,ticks,points_at?}]` 1~12 + `outcome_scales[{label,ticks,points_at}]` 1~3；`total_points_max` 可选（v5.3） |
| rcs | `points[{value,est,ci_lo,ci_hi}]` ≥5；`ref/log_y/hline_at/hist` 可选（v5.4） |
| subgroup | `subgroups[{name,p_interaction?,levels[{name,est,ci_low,ci_high,p?}]}]` 1~12×2~8；`overall` 可选（v5.5） |
| bland_altman | 两组等长 |
| pca | ≤200 特征列；groups 可选 |
| funnel | `--egger`（≥3 研究） |
| galbraith | 数据同 funnel（studies name/effect/se，效应 log 尺度）；≥3 研究；`est_label`=OR/HR/RR 默认画效应量弧线、MD/SMD 自动关（v5.6） |
| cif | `time`+`event` 两等长数组（0=删失 1=目标事件 ≥2=竞争编号）；`cause_labels`/`percent`/`time_unit`/`compare_km`（auto=有竞争才画 1−KM 对照）；单队列，多臂用 km（v5.7） |
| composite | panels 内除 composite/diagram/upset 外任意图型；不可嵌套 |
| volcano | log2fc+pvalue 数组；fc_cut/p_cut/top 数据键；阈值线+Top 标注 |
| slope | 两时点 [左值, 右值]；`panel_labels`/`left_floor` 等 + `--peak-label` 峰值注记（v4.2） |
| diagram | blocks/arrows 字段 |
| prisma | `lang=zh` 中文标准措辞；数字必须自洽 |

## 二、全量参数速查

| 参数 | 用途 |
|------|------|
| `--title "主标题 / 副标题"` / `--xlabel` / `--ylabel` | 标题与轴标签（含空格或以 - 开头用等号形式） |
| `--width N` / `--height N` / `--size 16:9` | 尺寸英寸 / 画幅预设 |
| `--format F` / `--multi-format tiff,png,pdf` | 指定格式 / 一次多格式 |
| `--pipeline analysis.yaml` / `--batch FIGURES.json` | 整篇论文批量 |
| `--dpi N` | 覆盖 DPI（默认线条图 600、照片 300） |
| `--show-values` / `--show-ratio` | 数值标签 / 组间比率标注 |
| `--hatch` / `--style glm-hatch` / `--alternate` | 斜纹 / GLM 签名风格 / 交替配色 |
| `--arena [名称|off]` | 基准对比竞技场风格（bar 单系列，v7.7 默认启用）：异质填充+冠军皇冠；负面指标用 `--arena off` |
| `--stats auto\|multi\|cox\|bootstrap` | 显著性 / Tukey·Dunn / Cox 多因素 |
| `--order "C,A,B" \| auto` | 类别顺序（bar/box/violin/line；auto=值/中位数降序） |
| `--normalize baseline\|pct100` | 归一化（对照=1 / 首点=100；误差棒同步） |
| `--doctor` | 渲染前参数/环境体检（省略 -o 只体检） |
| `--subtitle "副标题"` / `--source "来源注"` | 标题层级第二行 / 图底右对齐来源注（v4.0） |
| `--cmap NAME` / `--vmin --vmax` | 热图色阶与范围 |
| `--sheet NAME` | Excel 工作表 |
| `--cjk` / `--cjk-font PATH` | 中文字体（数据含中文自动检测） |
| `--journal NAME` / `--column single\|double` | 9 种期刊预设 / 栏位（⚠ 锁宽度） |
| `--verify` | PDF 像素级重叠验证（exit 2） |
| `--timeout N` / `--downsample N` | 看门狗秒数（0 禁用）/ 降采样 |
| `--annotate "x,y:文字"` / `--legend-loc` / `--legend-outside` | 注释 / 图例定位 / 外置图例 |
| `--area` | 仅 venn 面积比例 |
| `--alt` / `--caption` | 无障碍描述侧车 / 期刊图注侧车 |
| `--suggest` / `--wizard` / `--demo` / `--explain T` | 选图三件套与演示 |
| `--theme NAME` | 配色主题（默认 glm-brand 品牌；okabe-ito 色盲安全等 9 套） |

## 三、退出码

| 码 | 含义 |
|----|------|
| 0 | 成功 |
| 1 | 参数/数据校验致命错（中文报错+修正建议） |
| 2 | `--verify` 检出重叠 / `--batch`·`--pipeline` 部分条目失败 |
| 3 | 数据或格式错误 |
| 4 | 环境或依赖错误 |
| 5 | 渲染看门狗超时 |
| 6 | 内存护栏拒绝（自动降级重试仍败） |

## 四、典型场景参数组合

| 场景 | 一条命令骨架 |
|---|---|
| 期刊投稿单图 | `-t bar … --pub-ready`（=verify+色盲安全主题+pdf,png） |
| 多组显著性比较 | `-t box --stats multi`（≥3 组；正态→Tukey，否则 Dunn+Hochberg） |
| 偏态/小样本推断 | `-t violin --stats bootstrap`（均值+中位数 95%CI，固定种子） |
| 相对表达量/指数化 | `-t bar --normalize baseline --order auto`（对照=1+按值排序） |
| 新参数组合先体检 | `--doctor`（省略 -o 纯体检，exit 1=有发现） |

## 五、边界 Top 5

1. cluster_heatmap：>1500 行建议 `--downsample`（硬上限 3000 行）。
2. pca：≤200 特征列。
3. venn：2~4 集合；upset：2~30 集合。
4. `--journal` 锁定图宽（`--width` 被覆盖）；投稿 PDF 加 `--verify`。
5. composite 面板内不可嵌套 composite/diagram/upset（自管图型）。
