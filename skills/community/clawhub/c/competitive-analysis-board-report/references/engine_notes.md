# PPT 流式布局引擎（零重叠 / 零越界）

`scripts/gen_ppt_v3.py` 的 `Page` 类是整套 PPT 能"加内容不叠字、不压页脚"的核心。任何新增页面/段落，**必须走 `Page` 的方法，禁止手动画死坐标**。

## 坐标与尺寸约定
- 幻灯片：13.333 × 7.5 in（16:9）。单位 `Inches`，颜色用 `RGBColor`。
- 页边：左 0.42 / 标题带高 0.62 / 分隔线 y=0.84 / 正文起始 `self.y = 0.99`。
- 页脚安全带：内容底部不得超过 **6.98 in**（`view()` 据此把观点条吸附到底，不压页码区 7.08）。

## 核心机制：自增 y 游标
每个 `Page` 维护 `self.y`，所有 `sec/bul/tbl/box/view/note` 追加内容后**自动下移 y**。不需要算绝对坐标。

```python
class Page:
    def __init__(self, title_text, size=30):
        self.s = prs.slides.add_slide(BLANK)
        self.y = 0.99                      # 正文起始
        # ... 画标题 + 分隔线

    def sec(self, text, size=18, color=C_BLUE, gap=0.14, width=12.4):
        self.y += gap
        h = text_h(text, width, size)      # 按中文宽度估行高
        # 画 section 标题；self.y += h
        return self

    def bul(self, items, size=16, width=12.3, gap=0.09, item_gap=0.055, ...):
        self.y += gap
        for it in items:
            h = text_h("• "+it, width-0.2, size)
            # 画 bullet；self.y += h + item_gap
        self.y -= item_gap
        return self

    def tbl(self, headers, rows, size=13.5, col_w=None, ...):
        # 用 text_h 估算表头行高 + 每行各 cell 最高行高 → total
        # 建表；self.y += total；返回 self
```

## 中文行高估算 `text_h`（关键，避免文字溢出文本框）
python-pptx 不自动算文本框高度，必须自己估。规则：**CJK 全角字宽≈1.0、半角≈0.55**，按字号折行。

```python
def vlen(text):
    w = 0.0
    for ch in text:
        w += 1.0 if ord(ch) > 0x2E80 else 0.55
    return w

def text_h(text, width, size, min_h=0.0):
    cw = size / 72.0                       # 单字宽(in)
    per_line = max(1.0, (width - 0.12) / cw)
    lines = max(1, math.ceil(vlen(text) / per_line))
    return max(min_h, lines * (size * 1.42 / 72.0) + 0.045)
```
- 1.42 是行距系数；0.045/0.12 是上下内边距缓冲。表格 cell 用 `cell_h = sum(text_h(ln, cwid, size))` 累加多行。

## 观点条 `view()` 的防压页脚逻辑（最常踩的坑）
不固定的 `view()` 若直接 `top=self.y+0.18`，内容多时会把观点条推到页脚之下、甚至越界。修正：

```python
def view(self, text, size=15, color=C_RED, fill=..., align_bottom=True):
    h = text_h("◆ "+text, 12.1, size) + 0.12
    top = min(self.y + 0.18, 6.98 - h) if align_bottom else self.y + 0.18
    # 画圆角矩形；self.y = top + h
```
- `6.98 - h` 保证观点条整体落在页脚安全带之上；当上方内容已很满时，它向上吸附而非越界。

## 复用组件（直接调用，传入 slide + top/left/width）
- `kpi_row(sl, [(val,label,color),...], top, left, width, height, size)`：顶部 KPI 四卡。
- `scale_bars(sl, top, left, width)`：竞品规模横向条形图（手动 Rectangle，按 `val/tv` 比例算宽）。
- `month_chart(sl, top, left, width)`：月度收入占比柱状图（12 月，红/黄/蓝配色）。
- `two_col(sl, top, left, width)`：DO/DON'T 双栏（✅绿 / ❌红，固定高 4.35）。
- `matrix_9box(sl, top, left, width)`：九宫格（维度标签列 + 4 列梯队，强/中/弱着色）。
- `rival_map(sl, top, left, width)`：对手地图四层卡片。

## 校验（validate_ppt.py 原理）
遍历每个 shape，取 `left/top/width/height`（EMU），算右/下边界，容忍 0.02in 误差，越界即记录。`EMU_IN = 914400`。

```python
SW, SH = prs.slide_width, prs.slide_height
for sh in slide.shapes:
    l,t,w,h = sh.left, sh.top, sh.width, sh.height
    if l+tol < 0 or t+tol < 0 or (l+w) > SW+tol or (t+h) > SH+tol:
        overflow.append(...)
```

## 适配要点
- 加页面：从 `pg = Page("标题")` 开始，链式 `pg.sec().bul().tbl().view().finish()`。
- 加表格：务必给 `col_w`（英寸数组，和=12.4），否则按列均分易溢出。
- 改字号/字数后重跑 validate_ppt.py；若越界，优先缩减 `item_gap`/`size` 或拆页，不要手动画坐标强塞。
- 文本抽取校验（`text_h` 估高偶发不准）：交付前用 `present_files` 实际打开预览肉眼核对关键页。
