# 场景卡片（Scenario Cards）——一张卡跑通一个完整场景

> **何时读我**：知道要做什么分析，但不想跨多个文档拼参数——每张卡 = 场景 + 完整可跑命令 + 参数逐项说明 + 常见变体，复制即用。
> **最短路径**：Ctrl-F 你的场景关键词（生存/Meta/诊断/预测模型/组学/投稿…）。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」；参数全集见 `cheatsheet.md`，冲突见 `limits.md` §〇。


## 卡1 随机对照基线表图（三组均值±误差棒+显著性）

```bash
python3 scripts/gen_figure.py -t bar -d data.json -o fig1.png \
  --sig-bracket --hatch --title "图1 基线特征对比"
```
`-t bar` 柱状图｜`--sig-bracket` 数据携带 `comparisons:[{a,b,p}]`（p 值你已算好）时自动画分层括号星号——bar 是聚合数据（均值±误差棒），引擎不做自动检验｜
`--hatch` 黑色斜纹（黑白打印可区分系列）｜数据格式：`{"labels":[组名], "series":{系列: [值]}, "errors":{...}}`。
变体：分组更细用 `-t grouped_bar --show-ratio`；要看完整分布换 `-t violin`（同 schema）。

## 卡2 KM 生存曲线（含风险表与 log-rank）

```bash
python3 scripts/gen_figure.py -t km -d survival.json -o fig2.pdf --theme okabe-ito --verify
```
原始逐例数据 `[time, event]` 自动出风险表+log-rank+中位生存 95%CI｜`--verify` 投稿 PDF 像素级重叠门禁｜
竞争风险（events≥2）自动切 Aalen-Johansen｜变体：`--no-median` 关中位生存、`--risk-times 6,12,24` 自定风险表时间。

## 卡3 诊断试验 ROC（多模型对比）

```bash
python3 scripts/gen_figure.py -t roc -d roc.json -o fig3.pdf --compare
```
`--compare` 多模型 AUC 配对 DeLong 检验（需各曲线原始 `scores`）｜`auc`/`label` 每曲线可给。
变体：单模型直接 `-t roc`；预测模型整套见卡 6。

## 卡4 临床预测模型四件套（ROC+校准+DCA+列线图）

```bash
python3 scripts/gen_figure.py -t roc         -d pred.json -o fig4a.pdf --verify
python3 scripts/gen_figure.py -t calibration -d pred.json -o fig4b.pdf --verify
python3 scripts/gen_figure.py -t dca         -d pred.json -o fig4c.pdf --verify
python3 scripts/gen_figure.py -t nomogram    -d nomo.json -o fig4d.pdf --verify
```
calibration：分箱预测 vs 观测+理想对角线（8~10 箱每箱≥30 例，hl_p 标注）｜
dca：净收益 vs 阈值（`prevalence` 给患病率画理论参照；获益区间自动着色）｜
nomogram：列线图查表尺（points 来自你已拟合的模型，引擎不拟合）｜
非线性剂量反应用卡 5 的 rcs。四件套均**只可视化不拟合**——统计结论以你的模型输出为准。

## 卡5 暴露-结局非线性（RCS 限制性立方样条）

```bash
python3 scripts/gen_figure.py -t rcs -d rcs.json -o fig5.pdf --cjk --verify
```
`points=[{value,est,ci_lo,ci_hi}]` 来自你拟合的样条模型（R rms::rcs 等）≥5 网格点｜
默认对数轴（HR/OR）+`ref` 参照竖线+底部 rug；差值尺度传 `"log_y": false`（参照水平线默认 y=0）。
解释口径：置信带与参照水平相交=无统计学差异区。

## 卡6 Meta 分析（森林图+漏斗图+Galbraith 径向图）

```bash
python3 scripts/gen_figure.py -t forest -d meta.json -o fig6a.pdf --theme okabe-ito --verify
python3 scripts/gen_figure.py -t funnel -d meta.json -o fig6b.pdf --egger
python3 scripts/gen_figure.py -t galbraith -d meta.json -o fig6c.pdf
```
forest：效应值+CI+权重气泡+总效应菱形+I²｜`--stats cox` 原始逐例数据直接建模（PH 检验自动）｜
funnel：DL 合并线+`--egger` 不对称检验（<5 研究不可靠，引擎会警告）｜
galbraith（v5.6）：精度 1/SE×标准化效应径向图——带外研究=异质性/离群嫌疑（stderr 逐个报名）；效应取 log 值时默认画 OR 弧线读数｜
敏感性：`forest --sensitivity` 留一法。三件套分工：forest 看合并效应、funnel 看小样本不对称（发表偏倚）、galbraith 看谁是异质性来源。

## 卡7 组学差异表达（火山图+聚类热图）

```bash
python3 scripts/gen_figure.py -t volcano -d de.json -o fig7a.pdf
python3 scripts/gen_figure.py -t cluster_heatmap -d mat.json -o fig7b.pdf --downsample 2000
```
volcano：`fc_cut/p_cut` 阈值线+Top 基因自动标注（-log10(0)=inf 先截断）｜
cluster_heatmap：Ward 重排，>1500 行告警、>3000 行强制降采样｜集合交并：2~4 集 `venn --area`，≥5 集 `upset`。

## 卡8 分布比较三件套（箱线/小提琴/雨云）

```bash
python3 scripts/gen_figure.py -t raincloud -d dist.json -o fig8.pdf --stats multi
```
`--stats multi` 多组两两比较（ANOVA+Tukey 或 Kruskal-Wallis+Dunn-Hochberg 自动）｜
雨云=半小提琴云+箱线+原始点雨；分布逐组移动全景用 `-t ridgeline`；逐条目差距用 `-t dumbbell`。

## 卡9 肿瘤疗效（瀑布图+游泳图）

```bash
python3 scripts/gen_figure.py -t waterfall -d response.json -o fig9a.pdf --show-values
python3 scripts/gen_figure.py -t swimmer  -d followup.json -o fig9b.pdf --cjk
```
waterfall：RECIST 着色+PR/PD 阈值线+计数事实框｜swimmer：逐例时长+里程碑+持续中箭头。

## 卡10 中文期刊投稿（一图多格式+复跑包）

```bash
python3 scripts/gen_figure.py -t bar -d data.json -o fig10 --pub-ready \
  --journal cn-core --cjk
```
`--pub-ready` 一条命令=--verify 门禁+色盲安全主题+pdf/png 双格式+复跑交付包 `<输出>.repro/`｜
`--journal cn-core` 中文核心预设（自动 CJK+字号下限把守）｜复跑包给审稿人=数字可逐项对账。

## 卡12b 生存疗效对比（RMST，PH 违背/曲线交叉时）

```bash
python3 scripts/gen_figure.py -t rmst -d rmst.json -o fig12b.pdf --cjk --verify
```

`groups={组名: [[时间,事件(1/0)],...]}` 恰好两臂｜`tau` 缺省自动（最小最大随访之半，`--rmst-tau` 钉临床 τ）｜注释框报每臂 RMST(95%CI)与 ΔRMST 差值（Greenwood 方差）｜
> 适用：PH 检验提示违背或曲线交叉时，单一 HR 会掩盖时变效应——RMST 给绝对差。

## 卡13 疗效亚组分析（亚组森林图+P 交互）

> v5.8 快捷方式：手里是原始逐例数据？跳过手拼 JSON——`-t subgroup --stats cox -d raw.csv --treatment trt --subgroup-vars celltype --cut age@60` 一步出图（引擎拟合，stderr 报全表）。

```bash
python3 scripts/gen_figure.py -t subgroup -d subgroups.json -o fig13.pdf --cjk --verify
```
`subgroups=[{name, p_interaction?, levels=[{name, est, ci_low, ci_high, n?, p?}]}]`
每亚组变量 2~8 层｜`overall` 给总效应（底部菱形）｜方块实心=层内 P<0.05｜
P 交互<0.05 红色提示效应异质（交互检验须来自含交互项的多因素模型，逐层检验不代替）｜
差值尺度传 `"est_label": "MD"`（无效线自动取 0）。

## 卡11 不确定用什么图（三件套向导）

```bash
python3 scripts/gen_figure.py --suggest -d data.json   # 数据结构自动推荐
python3 scripts/gen_figure.py --wizard                # 四问生成完整命令
python3 scripts/gen_figure.py --doctor -t composite -d panel.json   # 渲染前体检（含跨面板共享尺度预检）
python3 scripts/gen_figure.py --explain dca           # 单图型用法+边界
```

## 卡12 组合图（期刊主图 A+B+C）

```bash
python3 scripts/gen_figure.py -t composite -d panels.json -o fig12.pdf --verify --legend-outside
```
`panels=[{type,data,title,span?}]`，`panel_labels:true` 自动角标｜面板不可嵌套 composite/diagram/upset｜
同变量跨面板务必同色+同尺度（--doctor 会预检范围悬殊）。

## 卡14 基准对比竞技场图（模型/方法多方案同指标对比）

```bash
python3 scripts/gen_figure.py -t bar -d arena.json -o fig14.png \
  --show-values --style sketch   # 竞技场风格 v7.7 起默认启用（负面指标 --arena off）
```
`-t bar` 单系列柱状图｜竞技场风格 v7.7 起默认启用：每根柱异质填充循环（橙白斜线/蓝白点纹/紫白斜纹），冠军柱（=最高柱）自动深青绿+柱顶金色皇冠+数值加粗高亮｜负面指标（最高=最差，如错误率/不良事件率）加 `--arena off` 关闭；`--arena "名称"` 按类别标签指定冠军｜榜单手绘风加 `--style sketch`（Balsamiq Sans/霞鹜文楷）；仅单系列竖向 bar；多面板对比用 composite 两面板各 bar（share_y 统一尺度）｜
数据：`{"labels":["模型A","模型B"],"series":{"得分":[分,分]}}`；真实样例见 `examples/example_arena.json`（OSWorld 基准论文公开数字）。
榜单图数据纪律：用当期时点快照（聚合榜收录有滞后，逐源标注更新时间）+来源上图（`--source`，composite 用 `source_note` 字段）。
