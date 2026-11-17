# Academic Figures — Pitfalls

> **何时读我**：输出不对劲/怀疑踩了已知坑。
> **最短路径**：Ctrl-F 现象关键词；每条坑都配了 ✅ 替代做法。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

## 反模式 → ✅ 替代（30 秒速查）

| 反模式 | ✅ 替代：怎么做才对 |
|--------|---------------------|
| 红绿编码关键信息 | `--theme okabe-ito`（8% 男性红绿色盲读不到） |
| 柱+误差棒展示原始分布 | box/violin 叠原始点；配对设计用 `paired` |
| 手写显著性星号无检验 | `--stats auto/multi`（引擎做检验并标注方法名） |
| 配对数据当独立样本 | `paired --stats auto`（配对 t/Wilcoxon 自动选） |
| 多组两两比较不校正 | `--stats multi`（Tukey/Dunn+Hochberg 自动） |
| 同一图 7 种以上颜色 | 合并次要组或 `composite` 拆面板 |
| 同一变量跨面板换色 | 跨图固定语义色（color-guide §五） |
| 深底/渐变/3D 装饰 | 引擎强制白底纯色，别对抗它 |
| 流程图白块（白底上隐形） | 用主题配色或任何可见色 |
| 图注不写 SD 还是 SE | errors 给什么画什么，图注必须标明 |

## 排序后标注必须同源索引（v5.1 哑铃图 Δ 错位教训的类级铁律）

凡"先排序、再逐行标注"的图型（dumbbell/swimmer/waterfall/upset…），标注值必须
从**排序后的同一条目**现算（`for row, i in enumerate(order): 用 i`），
⛔禁止用按原序预建的数组按下标 `row` 取用——排序一变，标注配对整体错位且
目检极难发现。锁：TestV50100.test_dumbbell_gap_sort_order 用非对称数据锁
排序-标注配对。

## 会与数据碰撞的浮动元素必须预留带（v4.10 事实框/v5.1 图例两次教训的类级铁律）

图例、事实框、Δ 标注等浮动元素放在数据区内时，**必须用坐标轴预留带**
（`set_ylim` 多留一行/带，如 swimmer 底部事实框带、dumbbell 底部图例带），
⛔禁止默认 `loc="lower right"` 碰运气——gap 排序末行/最短条行的右侧恰好
可能被终点值顶满。预留带是构造性防碰撞（任何数据形态下成立），不是渲染后
目检调参。

## 端点标记必留 pad（v5.1 哑铃图半圆裁切教训的类级铁律）

显式 `set_xlim(极值, 极值)` 会**禁用 matplotlib 自动边距**——数据恰在极值的
标记（dumbbell 端点圆、swimmer 端部箭头、forest 端点 CI 帽）必被轴边界裁半。
规则：凡是**标记中心可落在数据极值**的图型，xlim 必须自留 pad
（如跨度的 4%，或 swimmer 的 `*1.07`）；`set_xlim` 不是可选美化，是标记
完整性的一部分。锁：视觉验收像素自证（内容最左列距画布左缘 >5px）。

## 靠边的文字标注必须向画布内翻（v5.6 Galbraith 右缘标注溢出教训的类级铁律）

annotate/默认 offset 方向固定（如 +6pt 向右）时，**落在最右/最上 10% 区域的
数据点标注会溢出画布被裁**（galbraith 首轮验收：最右研究名被切掉半个字）。
规则：凡是逐点标注的图型，靠近右/上边界的点标注自动换向
（`xytext=(-7,5), ha="right"`）；阈值=轴范围 ×0.90。与上一条同根：
边界区域的装饰元素以画布完整性优先。

## 效应量弧线只对比率尺度有意义（v5.6 galbraith 设计裁决）

Galbraith 径向图的 OR/HR/RR 读数弧线把 y 轴（标准化效应）映射回临床尺度，
前提是**效应本身是对数值**；MD/SMD 等差值尺度画 exp 弧线=单位错标（同类
教训：中位数 auto 单位错标复发）。规则：比率标签默认开弧线、差值标签
自动关并 stderr 告知；用户硬传 `arcs=true` 时引擎自动关闭并 stderr 说明。

## 不要重复烧钱（防重复调用）

输入未变时，不要重复同一分析或重试已被拒绝的调用——渲染是确定性引擎，
同样的输入永远给出同样的结果与同样的报错。重试前先改变一个输入（修数据/
换参数）或先解除阻塞（装依赖/换环境）；连续两次相同失败后，先读报错里的
中文建议与本文档，而不是第三次提交。


## matplotlib not found in Hermes venv

The hermes-agent runs in its own venv (`~/.hermes/hermes-agent/venv/`), NOT the system python. If `gen_figure.py` fails with `ModuleNotFoundError: No module named 'matplotlib'`, install into the correct venv:

```bash
which python3
python3 -m pip install matplotlib numpy
```

Do NOT use `pip3 install --break-system-packages` — that installs into `/usr/lib/python3/`, which the hermes agent doesn't use.

## SKILL.md File Structure Stale

SKILL.md's File Structure section must match the actual files shipped. The lab-report PDF extraction script was removed in v2.0.1 to keep the skill scoped to chart generation — do not re-add `extract_lab_pdf.py` or `references/chinese-lab-report-extraction.md` without re-running the ClawHub security scan (they triggered a SUSPICIOUS verdict for scope mismatch).

## CJK font detection issues

If `--cjk` flag fails to find fonts, check:
```bash
fc-list :lang=zh | head -5
```
If fonts exist but CJK rendering shows boxes, the venv's matplotlib cache may be stale. Clear it:
```bash
python3 -c "import matplotlib; print(matplotlib.get_cachedir())"
rm -rf <that_path>
```

## Clinical Lab Trend Figures: Never Share Y-Axis Across Magnitudes

When making multi-panel lab parameter figures for case reports, each indicator MUST have its own panel with independent Y-axis. Example failure: mixing CRP (~200 mg/L), Ferritin (~1200 ng/mL), and Hb (~80 g/L) on the same axis produces an unreadable chart. User explicitly rejected such an attempt. See `references/clinical-lab-trends.md` for the correct N-panel grid pattern.

## White background is MANDATORY (zero tolerance)

This skill generates **publication-quality figures for journal submissions** (Nature, Lancet, Science). All output MUST use white background (`facecolor='white'`).

**NEVER add a dark/black theme.** Dark backgrounds are only for presentation slides or tech blogs — NOT academic publications. This rule was violated once (v1.5.0 dev) and the user corrected it firmly. The `save_kwargs["facecolor"]` is hardcoded to `'white'` and must not be changed.

If a user asks for a dark-themed chart, redirect them to the `data-viz` or `creative` skills instead.

## Hatching: ALL bars must have patterns

When `--hatch` is enabled, **every** bar series gets a hatching pattern — not just the second series. The original GLM-5.2 blog figures (the design reference) show hatching on both short and tall bars. This was corrected by the user: "高、矮柱状图都是有斜纹的".

`HATCH_PATTERNS` has NO `None` entry — the first item is `'//'` so even the first series gets hatched. Different patterns (`//`, `\\`, `||`, `--`, `++`, `xx`) distinguish series even in black-and-white print.

**Hatch line color = black (`edgecolor='black'`)**, NOT a darkened version of the fill color. The original reference uses pure black `#000000` hatch lines on colored fills. Do not use `_darken_color()` for this — it produces inconsistent contrast on light fills like yellow.

## Color saturation: prefer muted/elegant over vibrant

The user explicitly rejected vibrant/saturated colors (`#2563EB`, `#F97316`) as "油腻俗气" (greasy/tacky). Publication figures should use **muted, low-saturation tones** — the aesthetic is 素雅 (elegant/underated).

The `glm` theme uses pixel-extracted colors from the GLM-5.2 blog:
- Blue: `#70A0D0` (dusty blue, NOT `#2563EB`)
- Orange: `#D09050` (sandy/khaki orange, NOT `#F97316`)
- Green: `#30B080` (muted teal-green)

When creating new themes or adjusting colors, keep saturation low. A good rule: if a color looks like it belongs on a startup landing page, it's too saturated for an academic figure.

### Cool theme: user's go-to for non-submission work (v1.5.2+)

The user explicitly rejected Okabe-Ito's warm colors (orange `#E69F00`, green `#009E73`, yellow `#F0E442`, vermilion `#D55E00`) as "大红大绿大黄" when generating demo figures. They requested "素雅的冷色调配色" instead.

The `cool` theme was created in direct response:
- All 8 colors in hue range 190-260° (blue-cyan-teal-slate)
- Zero warm colors (no red, orange, yellow, magenta)
- Colorblind-safe (all distinguishable in protanopia/deuteranopia)
- Low-medium saturation (editorial, not startup-y)

**User preference rule**: For journal submissions → `--theme okabe-ito` (colorblind compliance required). For everything else (demos, blog, presentations, video figures) → `--theme cool` is the default. When generating multiple chart types for this user, use `--theme cool` unless they specifically ask for something else.

## How to extract exact colors from a reference image

When a user provides a reference image and asks you to match its color scheme, do NOT guess — extract pixel data:

```python
from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('reference.png')
arr = np.array(img)
# Round to nearest 16 for grouping, find dominant non-white/black colors
pixels = arr[:, :, :3].reshape(-1, 3)
rounded = (pixels // 16 * 16).astype(int)
colors = Counter(map(tuple, rounded))
# Top colors by frequency → actual fill colors used in the chart
```

For hatching detection: scan brightness along a single column through a bar interior. Alternating bright/dark bands = hatching. Check both horizontal and vertical directions to determine if lines are diagonal.

See `references/reverse-engineering-colors.md` for a complete worked example.

## Composite figures: tight_layout conflict

Composite charts (`-t composite`) use GridSpec internally and call `fig.add_subplot()` directly. The main `plt.tight_layout()` call is **skipped** for composite/diagram types (signaled by the generator returning the string `"composite"` or `"diagram"`). If you add new self-managed chart types, ensure they return a sentinel string from the generator function so `main()` skips both `apply_base_style()` and `tight_layout()`.

## KM median_survival: null values crash axvline (fixed v1.5.0+)

If `median_survival` JSON contains a `null` value for a group (e.g., median not reached):
```json
"median_survival": {"Treatment": null, "Control": 22}
```
The original code called `ax.axvline(x=None)` which raises `TypeError: '>' not supported between instances of 'float' and 'NoneType'`.

**Fix (v1.5.0+)**: Added `if med_t is not None` guard before `axvline()`. Either omit the key entirely or set it to `null` — both work now. Only groups with a numeric median get a vertical dotted line.

## KM log_rank.p must be float, not string (v1.5.2+)

If `log_rank.p` is set to a string like `"<0.001"` instead of a float, `gen_km()` crashes:

```
TypeError: '>=' not supported between instances of 'str' and 'float'
```

**Code-level fix (v1.5.2)**: `gen_km()` now coerces `p` to float at read time:
```python
p_val = float(log_rank.get("p", 1.0))  # defensive: handles "0.001" strings too
```

**Data-level rule**: Always use numeric values in JSON: `"p": 0.001` not `"p": "<0.001"`.

Discovered when 4 composite KM panels (c12, c16, c17, c19) failed during a 23-layout demo session.

## Scatter groups array: length must match x/y (fixed v1.5.0+)

In composite panels using scatter, the `groups` array must be the same length as `x`/`y`. If they mismatch (e.g., you built the arrays separately and forgot to extend groups), you get `IndexError: index N is out of bounds`.

**Fix (v1.5.0+)**: Code now truncates `groups` to `min(len(x), len(y))` automatically. But always ensure your JSON data is consistent — validate `len(x) == len(y) == len(groups)` before passing to the generator.

## Diagram coordinate system

The diagram type uses an arbitrary coordinate space (not data coordinates). Block positions (`x`, `y`, `w`, `h`) are in abstract units. The axis limits auto-expand to fit all blocks with 1-1.5 units padding. Arrow connection points are calculated at block edges (midpoint of the facing edge). For complex layouts, plan block positions on paper first.


---

## 配色选择不当的高频退稿原因（审稿人视角，v4.7）

1. **红绿对比编码关键信息。** 约 8% 男性红绿色盲；上调红/下调绿的经典配法=这部分读者读不到结论。改 `--theme okabe-ito`（volcano 内置已是橙/蓝语义）。
2. **单图超过 7 色。** 组再多颜色就无法分辨，审稿人批注常为 "rainbow figure"。合并次要组、或拆分面（composite/pipeline 分图）。
3. **灰度印刷后组间不可分。** 不少期刊印刷灰度版；饱和度相近的两个色转灰后一样深。自检法与对策（`--hatch` 斜纹/明度阶主题）见 `color-guide.md` §四。
4. **同一变量跨面板换色。** Figure 1 的对照组是蓝色、Figure 2 变橙色——审稿人会问"是不是两组东西"。跨图语义色一致规则见 `color-guide.md` §五、组合图统一见 `combo-guide.md` §四。
5. **深底/渐变/3D 装饰。** 多数期刊直接拒收；引擎强制白底纯色（见"设计原则"），无需担心。

## 统计方法误用（图会撒谎的典型场景，v4.7）

1. **SD 与 SE 误差棒混用且不标注。** 同一篇文章两图一个 SD 一个 SE 又都不写=审稿必问。引擎不替你决定：errors 字段你给什么画什么，**图注必须写明 SD 还是 SE**。
2. **用 bar+误差棒展示原始分布。** 柱+棒隐藏了分布形态与离群值（同数据常可画出一样的柱）。分布比较用 box/violin（可叠原始点），配对设计用 `paired`。
3. **无检验的显著性星号。** 手写 `*` 却没有对应检验=造假边缘。引擎路径：`--stats auto`（引擎做 t/Mann-Whitney 并标注）/`--stats multi`（ANOVA+Tukey）/自己跑统计后在 JSON `significance` 里给"组: p 值"——两条路都可溯源。
4. **配对数据当独立样本检验。** 前后测量用两样本 t 检验会低估效力。配对数据用 `paired --stats auto`（配对 t/Wilcoxon 自动选择）。
5. **多组两两比较不做校正。** 6 组两两比 = 15 次检验，不校正的"显著"多为假阳性。多组用 `--stats multi`（正态→ANOVA+Tukey HSD；非正态→Kruskal-Wallis+Dunn，Hochberg 校正，自动选择并标注方法名）。
6. **生存曲线不标删失。** 删失点不标=读者无法判断随访质量。km 自动带删失标记与风险表，不要用 `--no-median` 类参数把信息关掉（除非确有理由）。

# 以下章节自 SKILL_ZH.md 外移（v2.8 文档瘦身；内容随 v2.0~v2.7 沉淀）

## 边界情况（来自回归测试）

1. **Box/Violin 的 `labels` = 组名。** `labels` 按**系列/组数**校验，不是按数值个数。`{"labels": ["A","B"], "series": [[..],[..]]}` 正确；逐值标签列表会校验失败。
2. **ROC AUC 逐条曲线检查边界。** `curves[].auc` 必须在 [0,1]；检查覆盖每条模型曲线，不只看顶层 `auc`。
3. **组合图图例绝不重复句点。** 图例文字恰好以一个 `.` 结尾（`_fmt_n` 格式化器自带句点——不再追加）。
4. **字典键中的中文。** `series`/`groups` 中的中文键通过键扫描触发 CJK 字体加载；否则系列标签在图例中渲染成方块乱码。
5. **CJK 补充平面。** 极罕见的中文表意文字在 Ext-B..G 区段（如 㐀、𠀀）也能检测；发布前用 `detect_cjk_font.py` 验证字形覆盖。

## 设计原则

1. **白底不可妥协。** 本技能面向期刊投稿（Nature、Lancet、Science）。`save_kwargs["facecolor"]` 硬编码为 `'white'`。永不添加深色主题支持。
2. **斜纹 = 彩色填充上的黑线。** `--hatch` 激活时斜纹线为黑色，保证任何填充色上都可见。每个系列循环不同图案以便黑白打印区分。
3. **glm 为默认，okabe-ito 用于投稿。** 默认主题 `glm`（素雅、色盲安全）；期刊投稿始终推荐 `--theme okabe-ito`。

## CJK 陷阱

1. **CJK 字体可能缺少 Unicode 上下标。** 如 `⁹` (U+2079)、`³` (U+00B3)、`²` (U+00B2) 常触发 Noto Sans CJK 的 "Glyph X missing" 警告。改用纯文本写法：`10^9/L` 代替 `×10⁹/L`。发布前用 `detect_cjk_font.py` 检查字形覆盖。

## 流程图陷阱

1. **块颜色绝不使用 `#FFFFFF`** —— 白块在强制白底上不可见。用主题配色或任何可见十六进制色。
2. **同一轴线上两个相连块之间不要放中间块** —— 箭头路由算法按中心坐标选最近边。夹在垂直相连两块之间的块会导致箭头连错目标。改为把旁注并入目标块的 `sublabel`。
3. **CONSORT式排除框**应从主垂直流程水平偏移（同Y不同X），用水平箭头连接。

## Agent 用 Python 出图时（非 CLI）守则

1. 任何标签可能含中文时，先调用 `detect_cjk_font()`
2. 所有含中文的文本调用都使用 `fontproperties=font_prop`
3. 设置 `plt.rcParams['axes.unicode_minus'] = False`（防止负号变方框）
4. **多类别图使用 Okabe-Ito 配色**
5. 验证输出：多标签图文件 >20KB 说明字体已加载
6. 首选输出：投稿用 **PDF**，预览用 600 DPI PNG
7. **斜纹偏好**：斜纹线为**黑色**（`edgecolor='black'`）。斜纹激活时不要手动覆盖 `edgecolor`——由 `gen_bar` 处理。
8. **强制白底**：所有输出必须白底。深色/黑色背景**永不接受**。
9. **校验**：渲染前运行 `validate_data(data, chart_type)` 并检查致命信息（与 CLI 同一套门禁）。
10. **验证**：交付任何 PDF 前运行 `verify_overlap_pixel.py`。

## 像素级重叠验证：为什么不信任 PyMuPDF bbox 相交报告

PyMuPDF 的 span/char bbox 采用字体行高模型（Noto CJK 2.856em、DejaVu 1.695em），对旋转文本/竖排标签**系统性高估**（45° 时 fs=9 报 32.3pt，真实墨迹仅 16.8pt）。两个 bbox 相交 ≠ 真实重叠——在本工具的输出上，此类报告 100% 是假阳性。验证器用三级流程消除误报：

1. 全页渲染 → 连通分量（网格线/矢量图的大分量被过滤）
2. 分量质心归属到 char bbox
3. 候选对 600dpi 局部重渲染 → 最小墨迹距离（> 0.05pt 即判定分离）

若验证器报出真实重叠>0，说明图确实坏了——应修机制，不要逐图特判。


## Edge Cases (learned from regression tests; moved from SKILL.md, v2.8 doc slim-down)

1. **Box/Violin `labels` = group names.** `labels` is validated against the **number of series**,
   not the number of values. `{"labels": ["A","B"], "series": [[..],[..]]}` is correct; a per-value
   label list will fail validation.
2. **ROC AUC bounds are checked per curve.** `curves[].auc` must be in [0,1]; the check covers each
   model curve, not only a top-level `auc`.
3. **Composite legends never double the period.** Legend text ends in exactly one `.`
   (the `_fmt_n` formatter already appends a period).
4. **CJK in dict keys.** A Chinese key in `series`/`groups` triggers CJK font loading via key scan;
   without it the series label renders as tofu boxes in the legend.
5. **CJK supplementary planes.** Rare CJK ideographs in Ext-B..G blocks (e.g. 㐀, 𠀀) are detected;
   verify glyph coverage with `detect_cjk_font.py` before publishing.

## Agent Python (non-CLI) rules (moved from SKILL.md, v2.8)

1. Call `detect_cjk_font()` first if any label may contain CJK
2. Use `fontproperties=font_prop` on all text-setting calls with CJK content
3. Set `plt.rcParams['axes.unicode_minus'] = False` (prevents minus sign boxes)
4. Use Okabe-Ito colors for any multi-category plot
5. Verify output: file size > 20KB for multi-label charts indicates font loaded
6. Preferred output: **PDF** for submissions, PNG at 600 DPI for previews
7. Hatch lines are **black** (`edgecolor='black'`); do NOT manually override `edgecolor` when hatching is active — `gen_bar` handles it
8. White background mandatory: all output must use `facecolor='white'`; never add dark themes
9. Validate: run `validate_data(data, chart_type)` and check fatal messages before rendering (same gates as the CLI)
10. Verify: run `verify_overlap_pixel.py` on any PDF before delivery

## Why PyMuPDF bbox overlap reports are false positives here (moved from SKILL.md, v2.8)

PyMuPDF span/char bboxes use the font line-height model (Noto CJK 2.856em, DejaVu 1.695em), which
systematically OVERESTIMATES rotated text (at 45°, fs=9 reports 32.3pt vs 16.8pt real ink).
Two bboxes intersecting does NOT mean real overlap — on this generator's output such reports are
100% false positives. The verifier resolves this with 3 stages:

1. Full-page render → connected components (large components = gridlines/vector art, filtered)
2. Component centroid assignment to char bboxes
3. For candidate pairs: 600dpi local re-render → min ink distance (separated if > 0.05pt)

If the verifier ever reports 真实重叠>0, the figure is genuinely broken — fix the mechanism, do
not special-case the figure.

## 历史功能披露（诚实档案）

- **Lab Report PDF 提取**（v2.0.1 移除）：早期版本曾支持从检验报告 PDF 提取数据，
  因 PDF 版式差异导致的提取错误率不可接受而移除。需要同类能力时，建议先将报告
  数据手工转录为 CSV/JSON（data-formats.md），再用标准管线渲染。
