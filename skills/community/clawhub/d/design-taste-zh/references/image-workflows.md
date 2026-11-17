# 图像工作流 —— 审美工程与重制配方

用于“把这张照片做成杂志页 / 产品主图 / 海报”、提取配色，以及为图像模型写提示词。配合 `image-aesthetics.md` 在改前改后各打一次分。

## 1. 四步流程

1. **解析** —— 动像素之前先写 3 行：*主体*（必须保持可辨认的东西——人脸、产品、建筑剪影、数据）、*空间*（前景/背景、地平线、空白区域）、*情绪*（一个词）。决定**保留照片**（照片是锚点）还是**提炼照片**（照片只是灵感；输出是一张新插画）。
2. **从源图提取配色** —— 运行 `review_image.py` 取 `palette`。选出：1 个主色（通常是面积最大的中性色）、1 个辅色，以及**一个画面中已经存在的强调色**（招牌、外套、天空）。绝不引入与照片无关的强调色，也不要让强势的物体颜色（红色汽车、夕阳）自动成为整个版面的强调色——比较 2–3 个候选。做系列时，建立一张共享色卡（纸色、文字色、强调色）并复用。
3. **版式与留白规则** —— 先选画布（纸刊/社媒用 3:5 或 4:5 竖版，封面 2:3，电商 1:1，横幅 16:9 / 1.91:1）。然后：一个主构图、一个承载主体的容器、一种材质（+ 最多一种辅材质）、一组角色对比清晰的字体搭配、一个颜色来源、零或一个装饰——且装饰必须有功能。页边距 ≥ 短边的 6%；极简版式让空白纸面占 60–90%，主体占 8–25%。
4. **增强 / 重制** —— 顺序：裁切与校正 → 曝光/白平衡 → 局部对比 → 向色卡调色 → 修图（灰尘、干扰物）→ 仅在必要时放大（如 Real-ESRGAN，BSD-3）→ 最后排字。重新运行 `review_image.py` 对比指标变化；然后再看一遍。

## 2. 配方

| 配方 | 适用场景 | 画布与版式 | 色彩 | 文字 | 不要 |
|---|---|---|---|---|---|
| **极简杂志 / 纸刊** | 安静的旅行/静物照片或一行文字 | 3:5 或 4:5，做旧米白纸，主体小（8–25%），70–90% 留空，对齐到角落或三分点 | 近单色 + 取自画面的**一个**饱和强调色 | 小号衬线或打字机字体图注，档案式元数据（地点 · 日期 · No.） | 加边框、贴纸、渐变；把主体放大到填满 |
| **纸张拼贴（保留照片）** | 真实地点很重要的街头/人物照片 | 照片窗口作锚点；撕纸纤维边缘；从照片线条衍生的抽象形状延伸到纸面 | 区分“照片里的颜色”和“新增的印刷色”；一个自适应专色 | 短标题 + 极小图注 | 让照片里的红色物体渗进每个形状；遮住人脸或关键关系 |
| **照片 + 抽象面板（编辑）** | 建筑、天际线、水面、道路 | 上：原样照片；下：象牙色面板，含 3–5 个从照片空间关系中抽象出的扁平几何标记 | 从照片采样 2–3 色 | 2–5 个词的标题 | 面板中加纹理、颗粒、渐变 |
| **产品主图** | 电商、发布页、广告 | 主体占画面 40–60%，略低于中心或在三分线上；无缝背景；接触阴影 + 柔和倒影让它落地 | 背景取自产品辅色或中性色；产品颜色真实（与参考比对） | 产品名 + 一个卖点，放在产品剪影之外 | 无阴影的漂浮物体；抢焦点的道具；改变产品颜色的彩色轮廓光 |
| **配色重组** | 统一一组照片的品牌感，或从一张图推导网站/海报主题 | — | k-means 配色 → 选主/辅/强调 → 映射到 token（`--bg`、`--fg`、`--accent`、`--muted`）→ 检查文字对比度 ≥ 4.5:1 → 所有图片向色卡调色 | — | 选最饱和的聚类当背景 |
| **编辑封面** | 杂志/报告/书籍/播客封面 | 2:3 或 1:1；刊头区固定；一张图、一套封面文字层级（标题 ≫ 副标题 ≫ 元信息）；主体可以有意地压一次刊头 | 2 色 + 照片 | 标题用有个性的展示字，元信息用中性无衬线 | 五条封面标语、爆炸贴、描边字；标题压在人脸上 |

## 3. 重制循环

打分 → 选出最大的 1–3 个问题（P0 优先）→ 套用一个配方 → 重新打分。报告指标变化（如“显著色 9 → 4，饱和 p95 0.97 → 0.82，重心到三分点 0.21 → 0.06”），并前后并排展示。

## 4. 科研配图（Nature 风格）清单

1. **先立约定**：一句话结论；哪个分图证明它（主分图）；证据链 a → b → c。
2. **工具**：Matplotlib/Seaborn（Python）或 ggplot2/patchwork（R）——选一个后端并坚持。
3. **尺寸**：按最终尺寸制作（单栏约 89 mm，双栏约 183 mm）；该尺寸下文字 5–7 pt；线宽 ≥ 0.5 pt。
4. **字体**：Arial/Helvetica，句首大写，不用彩色文字；分图标号小写粗体 **a、b、c**，位于每个坐标区左上角，偏移处处一致。
5. **色彩**：色盲友好（分类用 Okabe-Ito；顺序用 viridis/cividis；发散型中点为中性色）；绝不只靠红 vs 绿编码；不用 rainbow/jet；同一方法在所有分图中用同一色相族；基线用灰色，“我们的方法”用强调色。
6. **诚实**：柱状图坐标轴从零开始；给出 n、误差线定义和检验方法；不选择性裁剪凝胶/印迹图；保留原始数据。
7. **布局**：同一行分图等宽、坐标轴边缘对齐、间距一致；直接标注 > 图例；去掉图表垃圾（外框、非必要网格线、3-D、阴影、图标）。
8. **导出**：矢量 PDF/SVG/EPS，嵌入字体（pdf.fonttype 42），位图部分 ≥ 300 dpi（线稿 600–1200）。
9. **质检**：以 100% 印刷尺寸和 50% 查看；灰度测试；色盲模拟；检查重叠和裁切。

## 5. 避开 AI slop 的提示词模板

每条提示词按 **主体 → 构图 → 光线 → 配色 → 媒介/镜头 → 质感 → 负面约束** 组织。要具体；禁用默认套路。多数图像模型对英文提示词更稳定，以下模板保留英文，按需替换方括号内容。

**Photo-real**
```
[subject + action, specific age/material/brand-neutral], [shot type: 35mm eye-level medium shot / 85mm close-up / top-down],
subject on the left third, horizon on the lower third, generous negative space on the right,
[light: soft overcast window light from camera-left / low golden side light / single hard key with deep shadow],
palette limited to [#hex dominant], [#hex support], small accent of [#hex] from [object],
natural skin texture with pores, realistic imperfections, slight film grain, true-to-life color, no HDR,
avoid: centered symmetric composition, glowing rim light, teal-orange grade, bokeh balls, lens flare, text, watermark, extra fingers
```

**Product hero**
```
[product] on a seamless [color] sweep, three-quarter view, product occupies 50% of frame slightly below center,
large softbox key from top-left, white bounce fill, soft contact shadow and faint reflection,
exact product color [#hex], crisp label edges, no props, no floating, no text, no glow, no gradient background
```

**Minimal zine poster**
```
3:5 vertical aged off-white paper, 80% empty space, a single small [subject] placed near the lower-left thirds point,
one saturated accent color [#hex taken from source photo], everything else muted warm greys,
risograph texture, quiet editorial layout; leave the top-right area empty for type (type added later),
avoid: frames, stickers, gradients, multiple accents, centered subject, generated text
```

**Scientific schematic / graphical abstract**
```
clean flat vector schematic of [mechanism], left-to-right flow in [3] stages, white background,
Okabe-Ito palette, thin uniform strokes, no 3-D, no shadows, no glow, no decorative icons, labels as blank boxes (text added in vector editor later)
```

规则：**不带文字**生成，之后再排版；要求 **2–4 个变体**，差异在构图而非仅随机种子；指定画幅比例；整个系列复用同一组 hex 配色；生成后、交付前先跑一遍 `image-aesthetics.md` 中 §4 的 AI 检查清单。
