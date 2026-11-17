# 边界与限制速查（Limits & Compatibility）

> **何时读我**：参数组合冲突、数据量上限、环境/字体边界。
> **最短路径**：先看「〇、速查表」，再 Ctrl-F 参数名。
> **回 INDEX**：SKILL.md「能力与边界」表。

> 一页说清所有"数字边界"和"参数能不能一起用"，免试错。投稿前建议通读一遍。
> 数值边界由代码强制执行：数据越界时不会出半成品图，而是中文报错并给出修正建议。
参数不适用（如 --stats auto 用于 line）则一律以 [ignored] 前缀显式告知后继续渲染，不静默。

## 〇、速查表（最常撞的硬边界，30 秒版）

**参数冲突集中速查（此前分散于 §一/§二/§六，此处一表收拢；细节仍见对应章节）：**

| 冲突组合 | 行为 | 出口 |
|---|---|---|
| `--journal` × `--width` | `--journal` 锁宽，`--width` 被忽略 | `--height` 仍有效；stderr 报预设 |
| `--stats auto/multi` × 非 box/violin/raincloud | 忽略并 `[ignored]` 告知 | 改用 `--stats cox`（仅 forest/subgroup） |
| `--compare` × 非 roc ／ `--egger` × 非 funnel | 忽略并告知 | — |
| `--hatch` × 非 bar 系 | 忽略并告知 | 品牌斜纹用 `--style glm-hatch`（全图型） |
| composite 面板 × composite/diagram/upset | 渲染前校验拒绝 | 拆分多层组合 |
| `--verify` × 非 PDF 输出 | 跳过并 WARNING | `--multi-format` 含 pdf 时核查该份 |
| `--pub-ready` × 显式 `--theme` | 显式主题优先 | 不被 okabe-ito 覆盖 |
| `--order "A,B"` × 未覆盖全部类别 | 报错列出完整清单 | 补全或改 `--order auto` |

| 图型/能力 | 硬边界 | 越界行为 |
|---|---|---|
| cluster_heatmap | **>1500 行告警 / 3000 行硬顶**（两级） | >1500 渲染时 WARNING 建议降采样；>3000 自动采样到 2000 并告知 |
| pca | ≤200 特征列 | 报错指路降维 |
| venn | 2~4 集合 | 报错；≥5 集合改 upset |
| upset | 2~30 集合；交集展示 top_n 1~50 | 报错；截断交集计入 stderr |
| km | 无硬上限 | — |
| paired / bland_altman | 两组等长 | 报错示长度差 |
| calibration / dca | calibration 值∈[0,1]；dca 阈值严格升序 (0,1) 开区间、1~6 模型 | 报错含具体箱号/序号 |
| nomogram | variables 1~12、outcome_scales 1~3、每尺 ticks 2~12；变量 points_at∈[0,100] | 报错含尺名与首错刻度 |
| rcs | points ≥5 且 value 单调；log_y=true 时 est/ci>0；ref 须在 value 范围内 | 报错含首个坏网格点序号 |
| subgroup | subgroups 1~12、每组 levels 2~8；ci_low≤est≤ci_high；p/p_interaction∈[0,1] | 报错含亚组名/层名 |
| cif | time+event 等长非空；event 须整数 ≥0（0=删失 1=目标事件 ≥2=竞争）；时间 ≥0；至少 1 个事件；单队列（不支持 groups 多臂） | 报错含首个坏项序号；groups 提示改用 `-t km`（AJ 自动模式） |
| 任意图 | 渲染看门狗 30~1800s 预算 | 内存不足自动降级重试 |

细节与完整矩阵见下方 §一~§九。

## 一、数据量边界（代码强制）

| 维度 | 上限 | 超出行为 |
|---|---|---|
| km / survival 每组样本 | 无硬上限（5 万行实测 3s 渲染） | — |
| cluster_heatmap 行数 | **1500 警告线 / 3000 硬顶（两级）** | >1500 输出 WARNING 建议降采样；>3000 自动等距采样到 2000 行并显著告知（`--downsample N` 可自定行数） |
| PDF 文本层 CJK 提取 | matplotlib 字体子集的 ToUnicode 差异使 CJK 字符在部分环境的 PDF 文本层不可提取（PNG 渲染不受影响） | 读屏/复制/检索场景用 `--alt` 替代文本与 PNG；图内关键结论勿只依赖 PDF 文本层 |
| 散点数据量 >50K 点 | PDF/SVG 体积爆炸、渲染缓慢 | **v7.8 起自动分层栅格化**：数据层栅格化（rasterized）、坐标轴/文字保持矢量（stderr 提示）；与 cluster_heatmap `--downsample` 互补——降采样改数据、栅格化改渲染层；点密度过高时优先降采样，栅格兜底 |
| pca 特征列数 | **200 列** | 友好报错：请先降维/筛选 |
| pca 最少样本 | 3 行 | 报错提示 |
| venn 集合数 | **2~4 个**（4 集合为椭圆布局；区域计数需恰 15 键） | 报错提示 |
| upset 集合数 | **2~30 个**（≥5 集合最见长；展示交集数 top_n 1~50，默认 12） | 超限报错；未展示交集计入 stderr 事实行 |
| paired / bland_altman | 两组**等长**数据 | 报错提示实际长度差 |
| calibration / dca | calibration 全值 **[0,1]**；dca 阈值 **(0,1) 开区间**严格升序、1~6 个模型 | 报错含首个越界箱号；dca 指明 t=0/1 无定义 |
| heatmap 矩阵 | 无硬上限；>200×200 建议 PNG/SVG（TIFF 会很大） | — |
| Shapiro 正态检验 | 每组 n>5000 自动跳过（视为正态） | stderr 提示 |
| --stats multi 括号绘制 | 最多画 8 对显著对比 | stderr 提示（完整结果仍在） |
| paired 配对检验 | n≥6 才做统计标注 | stderr 提示"效力不足" |

## 二、参数兼容矩阵（谁能和谁一起用）

| 参数 | 适用图型 | 其他图型上传入时 |
|---|---|---|
| `--stats auto` / `--stats multi` / `--stats bootstrap` | 仅 box / violin / raincloud | 其他图型 → `[ignored]` 显式告知（stderr） |
| `--compare`（DeLong） | 仅 roc，且需 `labels` + 各曲线 `scores` | 只有 fpr/tpr 时 stderr 提示无法检验 |
| `--egger` | 仅 funnel（≥3 研究） | 其他图型 → `[ignored]` 显式告知 |
| `--no-risk-table` / `--risk-times` | 仅 km（原始 `[时间,事件]` 格式） | 预计算曲线格式时 stderr 提示 |
| `--hatch` | bar 系（bar/grouped_bar/hbar/stacked_bar） | 其他图型 → `[ignored]` 显式告知 |
| `--cmap` / `--vmin` / `--vmax` | heatmap / cluster_heatmap | [ignored] 显式告知（stderr 提示，不静默）。`--vmax` 高于数据上限=合法压标度技巧：colorbar 如实显示 [vmin, vmax] 标度（数据端点外色带无采样格属预期，可把连续色阶压进最亮段） |
| `--annot on\|auto\|off` / `--cell-edge` / `--discrete` | heatmap | 其他图型 → `[ignored]` 显式告知。auto=超 30 行/列自动隐藏格内数值；--discrete=有序离散阶梯映射+离散色标；格内数值颜色按格底亮度自动反色（WCAG） |
| `--palette "#hex,..."` | 全图型（通用） | 分类图=按序替换主题系列色；热图=按给定顺序构建连续色阶（浅端对齐低值）；非法 hex → exit 3 |
| `--trend` / `--no-trend` | scatter | [ignored] 显式告知（stderr 提示，不静默） |
| `--sheet` | 仅 `--data *.xlsx` | CSV/JSON → `[ignored]` 显式告知 |
| `--show-ratio` / `--ratio-base` | grouped_bar | [ignored] 显式告知（stderr 提示，不静默） |
| `--lang zh` | prisma（中文标准措辞版） | [ignored] 显式告知（stderr 提示，不静默） |
| `--horizontal` | bar（等同 hbar） | — |
| `--annotate "x,y:文字"` | 所有图型（组合图自动选面板） | 坐标越界/类别不匹配 → 中文报错 exit 1 |
| `--legend-loc` / `--legend-outside` | 有图例的图型；组合图 outside=共享图例 | 无图例时 stderr 提示未生效 |
| `--stats cox` | 仅 forest / subgroup（其他图型 → `[ignored]` 显式告知后继续渲染） | — |
| `--arena` | 仅单系列竖向 bar（横向/多系列 → `[ignored]` 告知）；**v7.7 起默认启用**（冠军=最高柱，stderr 提示） | 负面指标（最高=最差）用 `--arena off` 关闭；`--arena "标签"` 指定冠军；未匹配自动回落最高柱并告知；基线关键词柱（人类/baseline 等）若为最高柱会被自动加冕（stderr 提示），非预期时用 `--arena "名称"` 改指数据柱 |
| `--order` | bar 系 / box / violin / line（box/violin 重排系列键） | 其他图型 → `[ignored]` 显式告知；显式列表须覆盖全部标签（多/少/重复=exit 1） |
| `--normalize` | 仅 bar 系 / line（分布图不做均值归一） | 其他图型 → `[ignored]` 显式告知 |
| `--doctor` | 全图型可用；只报告不改退出码 | 省 `-o` 纯体检（exit 1=有发现） |
| `--area` | 仅 venn | 其他图型 → `[ignored]` 显式告知（v3.7 起不再致命） |

## 三、参数组合的注意事项

- `--journal` 与 `--width`：journal 预设**锁定宽度**（单/双栏），`--width` 会被覆盖；`--height` 仍生效。要自定义尺寸就别用 `--journal`，改 `--width/--height`。
- `--journal cma / cn-core` 自动启用中文字体，无需再加 `--cjk`（加了也不冲突）。
- `--stats multi` 与 `--stats auto` 互斥（后者被忽略）；**两组数据请用 auto**（multi 会提示需 ≥3 组）。
- `--verify` 仅对 PDF 输出有意义（像素级文字重叠检查，发现重叠退出码 2）。
- `--demo` 不需要 `--data`；`--suggest` 需要 `--data`。
- 组合图（composite）的 panels 子图支持除 composite/diagram/upset 外的所有图型；**面板内不能再嵌套 composite/diagram/upset**（自管图型，v4.7 起前置拦截）。
- `--journal nejm|lancet|science|nature` 未显式给 `--theme` 时自动联动同款配色；显式 `--theme` 优先。
- venn `--area`：2 集合精确；3 集合为最优拟合（圆无法精确实现任意 7 区域面积），拟合偏差在
  stderr 如实报告；0 计数区域无面积、图中省略数字（stderr 说明）。

## 四、输出格式边界

| 格式 | 说明 |
|---|---|
| png / tiff | 位图；默认 DPI：线条图 600、照片类 300（`--dpi` 覆盖，建议 72–600） |
| pdf / svg / eps | 矢量，DPI 不适用；**投稿矢量图优先 PDF/EPS** |
| tiff | 自动 LZW 无损压缩 |
| 中文 | 任何格式均可；`--cjk` 自动探测，或 `--cjk-font` 指定字体文件 |

## 五、数据格式入口

各图型字段要求见 `references/data-formats.md`；十场景+六新图型的可运行示例在
`templates/`（每个 JSON 头部带 `_command`，复制即可跑）；组合图布局见
`references/composite-layouts.md`。PRISMA 数字自洽校验规则见 `--explain prisma`。

## 六、输出与默认行为交互（v2.9 收拢：易忽略的参数交互）

### 期刊预设明细（自 SKILL.md 下沉 v5.4；9 预设栏宽/字号/字体/最小字号/DPI——数值来自各刊作者指南，唯一权威源 `scripts/journal/*.json`）

| Journal | Single | Double | Font | Min Text | Family | DPI |
|---------|--------|--------|------|----------|--------|-----|
| `nature` | 89mm | 183mm | 7pt | **5pt** | Helvetica | 600 |
| `lancet` | 85mm | 183mm | 8pt | **6pt** | Arial | 600 |
| `science` | 55mm | 120mm | 7pt | 5pt | Helvetica | 600 |
| `cell` | 85mm | 176mm | 8pt | 6pt | Arial | 300 |
| `nejm` | 89mm | 190mm | 8pt | 6pt | Helvetica | 300 |
| `jama` | 89mm | 183mm | 8pt | 6pt | Arial | 600 |
| `ieee` | 89mm | 181mm | 8pt | 6pt | Times New Roman | 600 |
| `cma` | 80mm | 170mm | 8pt | 6pt | Arial (+CJK) | 600 |
| `cn-core` | 80mm | 170mm | 9pt | 6pt | Arial (+CJK) | 300 |

| 交互/默认 | 事实 | 建议 |
|---|---|---|
| `--journal` × `--width` | journal 预设锁定宽度，`--width` 被覆盖（`--height` 仍生效） | 要自定义尺寸就不加 `--journal` |
| PDF 重叠检测 | 仅 PDF 输出有意义，且**必须显式 `--verify`**（发现重叠→退出码 2，不落盘）；不加则不做像素级检查 | 投稿 PDF 一律加 `--verify` |
| 默认 DPI | 线条图 600、照片类 300（`--dpi` 72–600 覆盖） | 期刊成品保持默认即可 |
| 渲染看门狗 | 默认自适应 30–1800s；`--timeout N` 覆盖；`--timeout 0` 禁用自适应预算（保留 7200s 硬保险，负数报错）；瞬时失败自动重试 `--retries N`（默认 1，仅超时/内存） | 超大图适当调大；重试对确定性错误不生效 |
| journal × theme | `--journal nejm/lancet/science/nature` 未显式 `--theme` 时自动联动同款配色 | 显式 `--theme` 优先 |
| `--stats multi` × `auto` | 互斥（multi 优先）；两组数据用 auto（multi 需 ≥3 组） | 两组比较选 auto |
| `--order` | 显式列表须恰好覆盖全部标签（多/少/重复=exit 1）；significance 列索引自动改写；box/violin 重排系列键 | 类别有天然顺序（时间点/剂量）时显式列表 |
| `--normalize` | 仅 bar 系/line（分布图不做均值归一）；baseline=÷第一系列均值，pct100=÷自身首点×100；误差棒同步缩放 | 原始数值保留源数据文件 |
| `--doctor` | 只报告不改退出码；带 `-o` 体检后继续渲染，省略 `-o` 纯体检（exit 1=有发现） | 新参数组合先跑一次体检 |
| `--demo` / `--suggest` | `--demo` 不需要 `--data`；`--suggest` 需要 | — |

## 七、运行环境边界

- **无显示环境（CI/容器/SSH）**：引擎已内置 `matplotlib.use('Agg')`，无需 display/X11，开箱即跑。
- **中文字体**：`--cjk` 自动探测系统字体；`scripts/setup_env.py` 一键检测/修复；
  `--journal cma|cn-core` 自动启用中文（无需 `--cjk`，加了也不冲突）。
- **import 嵌入调用**：作为库使用时需自行 `matplotlib.use('Agg')`（见 `references/python-api.md` 方式二）。
- **输出目录**：必须可写；输出文件被占用（如 PDF 阅读器开着）会 PermissionError——
  换目录或关闭占用程序后重试。
- **cluster_heatmap 行数**：>1500 行渲染时即输出建议降采样的 WARNING（硬上限 3000 行，
  层次聚类内存随行数平方增长）——提前预判，不等超限报错。

## 八、性能参考表（实测，2026-09 v3.0/v3.1 基线）

| 场景 | 实测 |
|---|---|
| km 原始数据 5 万行 | ~3 秒（无硬上限） |
| cluster_heatmap 3000 行 | 内存护栏内（层次聚类 O(n²)，超限自动采样） |
| 200 图连跑压测 | 162 秒全成（15 图型轮转） |
| 22 模板带 CJK 全量渲染 | 全部通过（v3.0 扫描基线） |
| 输出 600dpi TIFF | 单图 0.1~0.6MB（LZW 压缩） |

数值随机器而异，此处为 82 开发机（RTX A5000/24GB）实测口径。

## 九、--stats bootstrap（v3.5 新增）

| 项 | 说明 |
|---|---|
| 方法 | percentile bootstrap（Efron 1979 经典方法），默认 5000 次重采样 |
| 输出 | 每组均值 95%CI 误差棒 + 组间均值差 95%CI 括号（CI 含 0 明示） |
| 确定性 | 固定种子（AF_BOOTSTRAP_SEED 可覆盖），同输入同 CI |
| 对拍口径 | 自研实现 + scipy.stats.bootstrap 与正态解析 CI 双对拍（测试锁定） |
| 适用 | box / violin；偏态/小样本/不满足正态假设时的稳健推断 |

## 十、调试开关与临时目录（自 SKILL.md 安全声明下沉）

- `AF_DEBUG=1`：异常时输出完整 traceback（默认只给中文三段诊断）。
- `AF_WIZARD_FORCE=1`：--wizard 非交互模式（自动化管道用）。
- `AF_NO_WATCHDOG=1`：禁用渲染看门狗（排查看门狗本身时用）。
- 三者均为进程级环境变量，仅用户手动设置生效，skill 不读任何远端配置。
- `--demo` 的演示数据写入系统临时目录 `af_demo_*` 前缀文件夹，可随时删除。
