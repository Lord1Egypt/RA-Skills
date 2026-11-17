# 常见问题 FAQ（高频问题速答）

> **何时读我**：遇到报错/安装/投稿问题要快答。
> **最短路径**：Ctrl-F 报错关键词或退出码。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 按场景分组。没找到答案时：`--explain <图型>` 看单图型说明，或翻 `pitfalls.md`（深度避坑）。

## 分类索引（先定位，再查答案）

| 问题类别 | 覆盖内容 | 本页章节 | 深度文档 |
|---|---|---|---|
| **数据类** | 格式选择、报错解读、长表转换、数据量上限 | 数据与格式 · 报错信息速查 | data-formats.md · limits.md |
| **参数类** | 图型选择、参数冲突、统计标注、批量命令 | 参数与图型选择 · 参数冲突与边界 | cheatsheet.md · --explain |
| **投稿类** | 格式/DPI、重叠检查、图注、配色合规、多图统一 | 输出与投稿 | color-guide.md · combo-guide.md · audit_pdf.py |
| **环境类** | 安装、中文字体、离线运行、依赖 | 安装与环境 | setup_env.py |

## 安装与环境

**Q：需要装什么？**
Python 3.8+ 和 matplotlib/numpy/scipy。跑一次 `python3 scripts/setup_env.py` 自动配齐并检测中文字体。

**Q：中文显示成方框？**
`--cjk` 自动探测系统字体；仍不行用 `--cjk-font /path/to/字体.ttf` 指定。`--journal cma/cn-core` 会自动开中文，无需手动加。

**Q：不联网能用吗？**
能。渲染全程本地，数据不出本机。仅首次装依赖需要网络。

## 数据与格式

**Q：CSV 能画哪些图？误差棒怎么加？**
CSV 适合 bar/line/box/scatter 等常规图。误差棒 v6.0 起 CSV 直接支持：主列旁加后缀列即可（`weight` 配 `weight_sd`/`weight_se`/`weight_sem`/`weight_err`，自动配对画误差棒；`weight_sd`+`weight_n` 自动换算 SEM）；显著性标记仍是 JSON 专属（`significance` 字段）。

**Q：KM 生存数据报「检测到长表结构」？**
你的表是 time/event/group 各占一列（一行记录一名患者），这种长表画不了生存曲线。请转成分组格式：
`{"groups": {"对照组": [[12, 1], [24, 0]], "处理组": [[10, 1], [30, 0]]}}`（每组一个数组，元素是 [时间, 事件 1/0]）。字段详解见 `data-formats.md` §KM。

**Q：xlsx 怎么指定工作表？**
`--data 文件.xlsx --sheet 表名`。默认取活动工作表。

**Q：数据量有上限吗？**
无统一上限，分图型限制：cluster_heatmap >3000 行自动等距采样到 2000 行（v3.1）、pca ≤200 特征列、venn 2~4 集合、km 无硬上限（5 万行实测 3 秒）。完整表见 `limits.md`。超限中文报错+给修正建议，不出废图（v3.1 起 cluster_heatmap 超限自动降采样）。

**Q：报错里有英文单词（如 KeyError/BadZipFile）怎么办？**
那是底层库的原始异常名。中文部分已说明哪里错、怎么改；英文关键词可直接搜索，或对照下方「报错信息速查」与 `pitfalls.md` 的同款案例。

## 参数与图型选择

**Q：论文一组 6~8 张图，要敲 8 次命令吗？**
不用。`--pipeline analysis.yaml`：`defaults` 写全局默认（主题/DPI/格式），`figures` 列出每张图的 type/data/out，一条命令批量渲染并生成 `.batch-report.json` 报告。YAML 需 `pip install pyyaml`；不想装就写 JSON（免依赖）。

**Q：投稿要同时交 TIFF 和 PDF，得跑两遍？**
`--multi-format tiff,png,pdf` 一条命令全出，文件名同源（`-o fig1` → fig1.tiff/fig1.png/fig1.pdf）。可与 `--pipeline` 组合，逐图指定不同格式组合。

**Q：森林图的无效参考线画在哪？**
缺省按效应尺度自动：OR/RR/HR（比率尺度）画在 1.0，MD/SMD（差值尺度）画在 0.0。数据若是 log 尺度请显式传 `"ref_line": 0`。（v2.5.x 及以前默认恒为 0，会把自然尺度 OR 的显著性判读画错位置。）

**Q：--stats auto 和 multi 有什么区别？**
auto=各组对第一组（两组就能用）；multi=全两两（需 ≥3 组，正态用 Tukey，否则 Dunn+Hochberg）。仅 box/violin 有效。

**Q：--journal 和 --width 为什么冲突？**
期刊预设锁定栏宽（这是预设的意义）。`--height` 仍可调；要自由尺寸就别用 `--journal`。

**Q：KM 的风险表能不能关掉？**
`--no-risk-table` 关闭；`--risk-times 2,6,10` 自定义显示时间点。预计算生存曲线格式无原始数据，不自动出风险表（stderr 会提示）。

**Q：ROC 想比较两个模型 A 谁更准？**
`--compare` 配对 DeLong 检验。需要 `labels`（0/1）+ 每条曲线的原始 `scores`；只有 fpr/tpr 曲线无法做 DeLong（会提示）。

**Q：组合图（composite）里能嵌组合图吗？**
不能。面板支持除 composite/diagram/upset 外的所有图型（composite/diagram/upset 为自管图型，内部自建坐标轴），布局参考 `references/composite-layouts.md`。

**Q：能在自己的 Python 代码里调用吗？**
能。subprocess 调 CLI（功能全）或 import 引擎函数级嵌入（load_data/validate_data/gen_*），示例代码见 `references/python-api.md`。

## 输出与投稿

**Q：投稿用哪个格式？**
矢量优先 PDF/EPS（期刊排版可缩放）；位图 PNG/TIFF 默认 600dpi（线条图）。TIFF 自动 LZW 压缩。

**Q：怎么确认没有文字重叠、字号达标？**
`--verify`（PDF 像素级重叠检查，发现重叠退出码 2；`--multi-format` 中含 PDF 时自动核查那份）；期刊预设会打印最小字号提示，配套 `scripts/audit_pdf.py --min-size 6` 复核。

**Q：图注/无障碍描述能自动生成吗？**
`--caption` 生成中英双语期刊式图注；`--alt` 生成无障碍描述，均为旁车文件，不覆盖图片。

**Q：配色怎么选？期刊对色盲安全有要求怎么办？**
投稿通用 `--theme okabe-ito`（Nature Methods 金标准色盲安全）；跟期刊色板用 `--theme nature/lancet/nejm/science`；黑白打印加 `--hatch` 斜纹冗余编码。系统化的「数据语义→色序→主题→灰度自检」流程见 `color-guide.md`。

**Q：多张图（Figure 1/2/3）怎么保持风格统一？**
两个层级：单张多面板用 `composite`（A/B/C 角标+跨行跨列拼版）；多文件批产用 `--pipeline`（`defaults` 锁主题/DPI/格式，产出 `.batch-report.json` 核对）。选择口诀与一致性纪律见 `combo-guide.md`。

**Q：集合关系画 venn 还是 upset？**
2~4 集合用 `venn`（4 集合椭圆布局）；≥5 集合用 `upset`（交集按大小降序点阵展示，venn 画不了）——`--suggest` 也会按集合数自动推荐。

## 报错信息速查

校验消息已全部中文化（报错原因 + 怎么改直接写在消息里），高频条目对照：

| 报错（节选） | 什么意思 | 怎么改 |
|---|---|---|
| 系列 'X' 的值全部相同（恒为 …） | 该列所有值一样，图会是一条平线 | 多半取错了列，换列或确认数据本意 |
| 系列 'X' 里有 N 个非数值项 | 源数据混入 NA/—/文字 | 清洗源数据；这些项会被跳过 |
| 'series' 里这些系列没有数据 | 空系列无法画 | 删掉空系列或补数据 |
| labels 有 N 个组名但 series 有 M 组 | box/violin 组名和数据对不齐 | 每组恰好一个名字，检查错位 |
| km: 检测到长表结构 | CSV 一行一患者的长表 | 转 JSON groups 分组格式（见上） |
| km: …必须是 [时间, 事件(1/0)] 成对列表 | groups 值是普通数组不是对 | 改成 [[时间, 事件], ...] |
| prisma 数字自洽校验失败 | 流程图各步人数加总不平 | 复核识别/筛选/排除/纳入人数 |
| 不支持的数据格式 | 扩展名不在支持列表 | 改用 .json / .csv / .tsv / .xlsx |
| No module named 'xxx'（ImportError） | 缺少依赖库（环境侧，退出码 4） | 按提示 pip install；核心功能只需 matplotlib/numpy/scipy |
| 内存不足（MemoryError） | 数据量超出可用内存（退出码 6=自动降级重试仍失败） | 减少行数/列数；cluster_heatmap 可加 --downsample 2000 |
| 渲染看门狗超时（退出码 5） | 图表未在预算时间内完成，被强制中断并给出建议；默认自动重试一次（预算放宽 ×1.5） | 瘦身数据，或 --timeout 600 调大预算 / --retries 3 加多次数；--timeout 0 仅关自适应预算（保留硬保险） |
| 退出码 1/3/4 怎么区分 | 1=参数或校验错误，3=数据或格式问题，4=环境或依赖问题 | 按报错里的中文建议逐条处理；AF_DEBUG=1 看完整细节 |

## 付费版

**Q：免费版和 Pro 什么关系？**
同一渲染引擎。Pro 是云端服务（无需 Python，上传数据即出图，¥3/次，金额以支付账单为准），见 SkillHub `academic-figures-pro`。本地能用免费版就够，团队/无环境场景选 Pro。

## 参数冲突与边界 FAQ（v3.2 扩充）

**Q：`--journal` 和 `--width` 一起给会怎样？**
`--journal` 锁定图宽，`--width` 被忽略（stderr 以 `[auto]` 明示）；`--height` 仍生效。
要自定义尺寸就别加 `--journal`。

**Q：`--verify` 对 PNG/TIFF 输出有效吗？**
无效——仅 PDF 输出生效（像素级文字重叠检查）。非 PDF 输出时 stderr 会以 `[auto]` 提示。
矢量投稿图建议 PDF + `--verify`。

**Q：`--stats auto` 能用在折线图/散点图上吗？**
不能——仅 box/violin（其他图型 stderr 以 `[ignored]` 显式告知，不静默）。两组前后配对数据请用 `-t paired`。

**Q：`--compare`（DeLong）能用在没有 scores 的 ROC 数据上吗？**
不能——需各曲线提供 `scores`（原始打分）；只有 fpr/tpr 时无法做配对检验（stderr 提示）。

**Q：`--egger` 能用在森林图上吗？**
不能——仅 funnel（≥3 研究）。森林图的 Meta 功能是 `--stats cox`（多因素回归）。

**Q：漏斗图和 Galbraith 径向图（v5.6）怎么选？**
同一份数据（studies name/effect/se）两者都吃：漏斗图看**小样本不对称**（发表偏倚线索，配 `--egger` 检验）；Galbraith 径向图看**谁是异质性来源**（±1.96 同质带外的研究 stderr 逐个报名，配森林图权重交叉核对）。审稿人常要求两者齐备。注意效应请给 log 值（OR/HR/RR 尺度）——径向图的效应量弧线按 est_label 读回临床尺度，MD/SMD 自动关弧线。

**Q：composite 多面板同一变量的 y 轴范围差很大，审稿人误读怎么办？**
v5.6 起在 composite 数据加 `"share_y": true`——同 ylabel 的面板自动统一 y 轴（含 log 尺度同步），stderr 报统一范围；`--doctor` 预检发现范围差 >5 倍时也会提示这一出口。

**Q：`--hatch` 和 `--style glm-hatch` 什么区别？**
`--hatch` 仅 bar 系（柱状填充斜纹）；`--style glm-hatch` 是主题级开关（glm 配色+全图斜纹风格）。

**Q：cluster_heatmap 超过 3000 行会失败吗？**
v3.1 起不会——自动等距采样到 2000 行并显著告知（`AUTO-DOWNSAMPLE`）；`--downsample N`
可指定其他行数。

**Q：组间比较的星号括号（bracket）怎么画？**
数据加 `comparisons` 字段+`--sig-bracket`：`{"a":"ctrl","b":"trt2","p":0.049}` 这样一组比较对，自动画分层 bracket+星号（bar/grouped_bar/box/violin）。p 值用你自己跑的检验结果；引擎只可视化不替你选检验。

**Q：CSV 能带误差棒吗？**
能——v6.0 起 CSV 后缀列自动配对：主列 `weight` 旁放 `weight_sd`/`weight_se`/`weight_sem`/`weight_err` 即自动画误差棒（`weight_sd`+`weight_n` 自动换算 SEM；`--csv-no-errors` 可关闭识别）。JSON 的 `errors` 对象写法仍可用。详见 data-formats.md 的 JSON/CSV 能力对照表。

**Q：投稿一键出图怎么做？**
`--pub-ready`（v3.8）：一条 flag 自动展开 `--verify`（PDF 重叠门禁）+ 色盲安全主题 + pdf,png
多格式（语义糖，显式传参优先）。等价于手动四件套，投稿图组一条命令。

**Q：想让柱状图按数值大小/时间点排序？**
`--order auto`（按第一系列值降序；box/violin 按各组中位数降序）或显式列表
`--order "T0,T1,T2"`（须覆盖全部标签，多/少/重复=exit 1）。系列/误差数组同步重排，
significance 列索引自动改写。仅 bar 系/box/violin/line。

**Q：相对表达量（对照=1）/指数化时序（T0=100）怎么归一？**
`--normalize baseline`（各系列÷第一系列均值）或 `--normalize pct100`（各系列÷自身首点×100）。
误差棒同步缩放；仅 bar 系/line——分布图不做均值归一（`[ignored]` 提示）。原始数值保留源数据。

**Q：参数太多怕组合错？**
`--doctor`（v3.9）：渲染前参数/环境体检报告（组合冲突/数据 schema/依赖/输出目录）。
带 `-o` 体检后照常出图；省略 `-o` 纯体检不渲染（exit 1=有发现）。

**Q：volcano 的 p=0 点为什么报错？**
-log10(0) 无定义。全转录组数据常见 p 值下溢为 0——请替换为该数据集的最小可表示值
（如 1e-300）；引擎会在校验层以中文报错列出越界数量。

**Q：volcano 支持多重校正（padj/FDR）吗？**
当前 p_cut 作用于原始 p 值（y 轴=-log10(p)）。若要用 FDR 阈值，请先在数据侧换算好
再传入 pvalue 数组（阈值线语义随之为准），并在图注说明校正方法。

**Q：slope（斜率图）能画三次以上的时间点吗？**
不能——slope 是两时点（pre/post）专用形态，每项恰好 [左值, 右值]。三次及以上
测量请用 line（多系列折线）；选型口诀：两时点比变化用 slope，看趋势用 line。

**Q：composite 用了 `panel_labels:true`，角标会和我手写的 Panel A 标题重复吗？**
缺省关闭——只有显式传 `"panel_labels": true` 才自动加角标。手写标题的既有图
保持原样；开了之后建议把面板 title 里的 "Panel A:" 前缀删掉，避免双重标注。

**Q：dual_axis 给了 `right_floor` 会不会把数据"裁"出图外？**
下限只影响坐标轴起点，数据点不会被裁掉；但轴下限以下的部分（若有）会落在
可视区外——投稿图建议在图注声明轴起点（如"右轴自 35 起"），避免读者误读比例。
`--summary` 同理只输出计数事实（n/组数/事件数），不做任何统计推断。

**Q：数据不满足正态/样本量小，--stats auto 可信吗？**
`--stats bootstrap`（v3.5）：非参数 bootstrap 置信区间——每组均值 95%CI + 组间均值差 CI
括号（CI 含 0 明示，不给误导性星号）。确定性输出（固定种子）。仅 box/violin。


## 图型专属易错点速答（v5.3；评分反馈：图型专属坑此前散落未集中）

**Q：forest --stats cox 出 HR 前要注意什么？**
Cox 比例风险假定（PH）——引擎自动做 PH 检验并在 stderr 提示；PH 不满足时改用时依协变量
或报告分层 Cox，图上星号不代表 PH 成立。原始长表（time/event/协变量列）才是 `--stats cox`
的输入，预计算 HR 表不需要它。

**Q：upset 的 top_n 截断后总数对不上？**
默认只画前 12 大交集（`top_n` 1~50）；被截断的交集**不会消失**，全部计入 stderr 事实行。
`sort=size|degree` 与 `min_size` 过滤后再截断——对账请以 stderr 行为准，别用图上柱子求和。

**Q：venn `--area` 模式区域面积能完全按比例吗？**
2 集合解析解精确；3 集合是圆心+半径联合最优拟合（圆无法实现任意区域组合），
实际拟合偏差在 stderr 如实报告。精确计数展示请用默认等圆模式。

**Q：dca 的阈值能取 0 或 1 吗？**
不能——净收益公式 t/(1-t) 在端点无定义；引擎强制 (0,1) 开区间严格升序并报错指明。
阈值应取自临床决策点而非统计网格。

**Q：calibration 分箱有什么惯例？**
8~10 箱、每箱 ≥30 例是常见做法；引擎**不做自动分箱**（分箱口径属方法学决策）。
大样本下 Hosmer-Lemeshow p 几乎必然显著，p>0.05 不能单独证明校准好，须配图判读。

**Q：nomogram 的 points 分数是引擎算的吗？**
不是——引擎只做可视化；points/points_at 必须来自你已拟合的模型（R rms::nomogram、
Python 统计包输出等）。方法学表述（变量单位、计分区间、结局时点）写入统计方法段。

**Q：swimmer 的 ongoing 箭头会被裁掉吗？**
不会——引擎自动在右侧留端部箭头位（xlim 右缘 7% pad）。里程碑可晚于条端（真实随访习惯）。

**Q：raincloud 零方差组会怎样？**
该组 KDE 云退化为基线标记线并 stderr 告知（零静默）；箱线五数照常绘制。
