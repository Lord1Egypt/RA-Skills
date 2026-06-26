---
name: chinese-image-gen
description: "Generate Chinese vertical images (750×1334px) for 微头条/social media using Playwright + Google Fonts CDN. Solves PIL Chinese font glyph bugs. Triggers: 生成图片, 做配图, 微头条图, 数据可视化图, 竖屏图片, Token 消耗图, generate image, make infographic"
---

# 中文竖屏图片生成技能

生成高质量中文竖屏图片（750×1334px），适用于微头条、社交媒体等。

## 技术方案

- **渲染引擎**：Playwright（Python）+ Chromium（不用 snap 版 CLI chromium，有 AppArmor 权限问题）
- **字体**：Google Fonts CDN `Noto Sans SC`（不用系统 Noto Sans CJK，有 glyph bug）
- **样式**：HTML + CSS 内联（不用 PIL 手写坐标）

## Prerequisites

```bash
# Install Playwright (Python)
pip install playwright

# Install Chromium browser (required once)
playwright install chromium
```

## 和 AI 生图的区别

| | 本技能（代码渲染） | AI 生图（Midjourney/DALL-E） |
|---|---|---|
| **文字精度** | 100% — 浏览器渲染真实字体 | 几乎不准确 — AI 在"画"文字 |
| **可控性** | CSS 精确到像素 | 每次结果随机、不可预测 |
| **费用** | 免费（本地 Playwright） | 每张图有 API 费用 |
| **速度** | 约 2 秒/张 | 10-30 秒/张 |
| **最适合** | 数据卡片、对比图、信息图、社交媒体配图 | 插画、艺术图、照片级渲染 |
| **弱点** | 需要写 HTML/CSS | 中文/日文/韩文几乎无法准确渲染 |

**一句话总结：** 图里需要**可读的文字**（尤其是中日韩）→ 用本技能；需要**艺术画面**→ 用 AI 生图。

## 适用场景

**数据展示**
- Token 消耗报表、费用分析
- API 性能仪表盘
- 周/月统计数据汇总

**对比分析**
- 大模型价格对比（如 GPT vs Claude vs DeepSeek）
- 产品参数对比
- 方案优劣分析卡片

**社交媒体配图**
- 微头条 / 小红书竖屏信息图
- 微信公众号头图
- 知识分享卡片（含代码片段）

**任何需要像素级文字精度的场景**
- 图片里有可读文字 → 用本技能
- 纯视觉/艺术图 → 用 AI 生图

## 操作流程

### 1. 编写 HTML

将内容写成 HTML，内联所有 CSS。固定尺寸 750×1334px。

**HTML 模板头部（必加）：**
```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap" rel="stylesheet">
<style>
/* 所有 CSS 内联 */
</style></head><body>
<!-- 内容 -->
</body></html>
```

### 2. 设计规范

**配色体系：**
- 主背景：`linear-gradient(180deg, #1a1220 0%, #0d1b2a 40%, #080e18 100%)`
- 顶部光晕：`radial-gradient(ellipse, rgba(255,140,50,0.5) 0%, rgba(255,100,30,0.15) 40%, transparent 70%)` + `filter:blur(40px)`
- 强调色：电光蓝 `#00d4ff`（主）、活力橙 `#ff6b35`（峰值/重点）、薄荷绿 `#00e5a0`、金色 `#ffc107`

**布局层级（从上到下）：**
1. 头部区：大标题 48px 加粗 + 副标题 16px 灰色
2. 数据卡片：3 列 grid，半透明黑底 `rgba(15,20,40,0.7)` + 细微边框 + 圆角 10px
3. 活跃度行：居中排列，用 `/` 分隔，上下有分隔线
4. 柱状图区：上方加"每日 token 消耗量"小标题，柱子高度等比缩放
5. 底部：虚线分隔 + 说明文字

**安全边距：** 上下左右各 80px

**字体规范：**
- 字重：300（light）、400（regular）、700（bold），都安全
- 标题：`#ffffff`，正文：`#bbbbbb`，辅助：`#999999`，更弱：`#777777`
- 数字格式：中文用"万""亿"，不用 "M""K"

**柱状图规范：**
- 峰值柱：橙色渐变 `#ff8c32 → #cc5500` + box-shadow 发光
- 普通柱：青色渐变 `#00d4ff → #0088aa`
- 柱宽 52px，圆角 8px 8px 4px 4px
- 柱顶标注数值，柱底标注星期+日期

### 3. 渲染截图

将 HTML 写入临时文件，用 Playwright 渲染：

```python
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox'])
    page = browser.new_page(viewport={"width": 750, "height": 1334})
    page.set_content(html_string)
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)  # 等 Google Fonts 加载
    page.screenshot(path="output.png")
    page.close()
    browser.close()
```

### 4. 多图生成

复用同一个 browser 实例，循环生成多张图：

```python
with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox'])
    for html, filename in pages:
        page = browser.new_page(viewport={"width": 750, "height": 1334})
        page.set_content(html)
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        page.screenshot(path=f"{OUT}/{filename}")
        page.close()
    browser.close()
```

### 5. 质量检查

- 放大查看每个汉字（尤其"复""繁""赢"等笔画多的字）
- 确认无重叠、无裁切、无变形
- 确认对比度足够
- 确认整体布局均匀，没有大片空白

## ⚠️ 踩过的坑

| 问题 | 原因 | 解决 |
|------|------|------|
| "复"字右边被裁切 | Noto Sans CJK Bold glyph bug | 用 Google Fonts CDN 的 Noto Sans SC |
| 部分汉字乱码 | Noto Serif CJK Bold glyph 问题 | 不用 Serif 字体 |
| 截图写文件失败 | snap 版 chromium AppArmor 权限限制 | 用 Playwright 而非 CLI chromium |
| 柱子遮挡文字 | overflow 控制不当 | 容器加 overflow:hidden 或控制柱高 |
| 排版大片空白 | flex:1 撑空间 | 用固定 margin 控制间距 |
| 数字格式不统一 | 用 "M""K" 不符合中文习惯 | 统一用"万""亿" |

## 自定义尺寸

默认 750×1334（竖屏微头条）。如需其他尺寸，在 viewport 和 HTML body 上同时修改。

## 完整示例：Token 消耗周报图

以下是经过验证的完整 HTML 模板，直接可用：

```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  width:750px; height:1334px;
  background:linear-gradient(180deg, #1a1220 0%, #0d1b2a 40%, #080e18 100%);
  font-family:"Noto Sans SC",sans-serif;
  color:#fff; padding:80px;
  display:flex; flex-direction:column;
  position:relative; overflow:hidden;
}
.glow {
  position:absolute; top:-120px; left:50%; transform:translateX(-50%);
  width:500px; height:280px;
  background:radial-gradient(ellipse, rgba(255,140,50,0.5) 0%, rgba(255,100,30,0.15) 40%, transparent 70%);
  filter:blur(40px); z-index:0;
}
.header { text-align:center; position:relative; z-index:1; padding-top:20px; margin-bottom:28px; }
.label { font-size:13px; color:#777; letter-spacing:4px; text-transform:uppercase; margin-bottom:10px; }
.main-num { font-size:48px; font-weight:700; color:#fff; margin-bottom:4px; letter-spacing:-1px; }
.unit { font-size:16px; color:#999; }
.stats { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; position:relative; z-index:1; margin-bottom:24px; }
.stat { background:rgba(15,20,40,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:16px; }
.stat-label { font-size:12px; color:#777; margin-bottom:6px; }
.stat-val { font-size:20px; font-weight:700; }
.stat-pct { font-size:12px; color:#666; margin-top:2px; }
.activity { display:flex; justify-content:center; gap:30px; padding:18px 0; margin-bottom:28px; border-top:1px solid rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.06); position:relative; z-index:1; }
.act-item { text-align:center; }
.act-num { font-size:22px; font-weight:700; color:#fff; }
.act-label { font-size:12px; color:#888; margin-top:2px; }
.chart-header { position:relative; z-index:1; display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; margin-top:70px; }
.chart-title { font-size:14px; color:#888; letter-spacing:2px; }
.chart-hint { font-size:12px; color:#555; }
.chart-area { position:relative; z-index:1; }
.chart { display:flex; align-items:flex-end; justify-content:space-between; height:360px; }
.col { display:flex; flex-direction:column; align-items:center; flex:1; }
.val { font-size:15px; font-weight:700; color:#00d4ff; margin-bottom:8px; white-space:nowrap; }
.val.peak { color:#ff6b35; }
.bar { width:52px; border-radius:8px 8px 4px 4px; background:linear-gradient(180deg, #00d4ff 0%, #0088aa 100%); }
.bar.peak { background:linear-gradient(180deg, #ff8c32 0%, #cc5500 100%); box-shadow:0 8px 25px rgba(255,120,40,0.3); }
.day { font-size:12px; color:#777; margin-top:10px; text-align:center; }
.day span { color:#555; font-size:10px; }
.footer { text-align:center; margin-top:24px; padding-top:16px; border-top:1px dashed rgba(255,255,255,0.1); font-size:13px; color:#666; position:relative; z-index:1; }
.footer span { color:#ff6b35; }
</style></head><body>
<div class="glow"></div>
<div class="header">
  <div class="label">Week Token Usage</div>
  <div class="main-num">12,345,678</div>
  <div class="unit">tokens · 03-01 ~ 03-07 · weekly total 1,235 万</div>
</div>
<div class="stats">
  <div class="stat"><div class="stat-label">Input</div><div class="stat-val" style="color:#ff6b35;">456 万</div><div class="stat-pct">37%</div></div>
  <div class="stat"><div class="stat-label">Output</div><div class="stat-val" style="color:#00e5a0;">123 万</div><div class="stat-pct">10%</div></div>
  <div class="stat"><div class="stat-label">Cache Read</div><div class="stat-val" style="color:#00d4ff;">656 万</div><div class="stat-pct">53%</div></div>
</div>
<div class="activity">
  <div class="act-item"><div class="act-num">800</div><div class="act-label">Messages</div></div>
  <div class="act-item" style="color:#333;font-size:24px;align-self:center;">/</div>
  <div class="act-item"><div class="act-num">750</div><div class="act-label">Replies</div></div>
  <div class="act-item" style="color:#333;font-size:24px;align-self:center;">/</div>
  <div class="act-item"><div class="act-num">500</div><div class="act-label">Tool Calls</div></div>
</div>
<div class="chart-header"><div class="chart-title">Daily Token Usage</div><div class="chart-hint">▲ Peak</div></div>
<div class="chart-area"><div class="chart">
  <div class="col"><div class="val">120 万</div><div class="bar" style="height:40px;"></div><div class="day">Sat<br><span>03-01</span></div></div>
  <div class="col"><div class="val">180 万</div><div class="bar" style="height:60px;"></div><div class="day">Sun<br><span>03-02</span></div></div>
  <div class="col"><div class="val">210 万</div><div class="bar" style="height:70px;"></div><div class="day">Mon<br><span>03-03</span></div></div>
  <div class="col"><div class="val peak">300 万 ⚡</div><div class="bar peak" style="height:340px;"></div><div class="day">Tue<br><span>03-04</span></div></div>
  <div class="col"><div class="val">150 万</div><div class="bar" style="height:50px;"></div><div class="day">Wed<br><span>03-05</span></div></div>
  <div class="col"><div class="val">135 万</div><div class="bar" style="height:45px;"></div><div class="day">Thu<br><span>03-06</span></div></div>
  <div class="col"><div class="val">140 万</div><div class="bar" style="height:47px;"></div><div class="day">Fri<br><span>03-07</span></div></div>
</div></div>
<div class="footer">Peak day: <span>batch operation triggered spike</span></div>
</body></html>
```

**渲染代码：**
```python
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox'])
    page = browser.new_page(viewport={"width": 750, "height": 1334})
    page.set_content(html_above)
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)
    page.screenshot(path="output.png")
    page.close()
    browser.close()
```

**调整间距技巧：**
- 柱状图位置靠 `chart-header` 的 `margin-top` 控制（当前 70px）
- 各区块间距用固定 `margin-bottom`（24px / 28px）
- 不要用 `flex:1` 撑空间，会导致大片空白
- 柱状图高度 `height:360px`，峰值柱 `340px`，普通柱等比缩放

## 通用对比卡片图模板

适用于任何多项目对比场景（费用对比、产品对比、方案对比等）。

### 布局结构

```
顶部：标题 + 描述
┌─────────────────────────┐
│  标题                    │
│  副标题（数据来源/范围）   │
│  ═══ 概览条 ═══         │ ← 可选：构成条/比例条
└─────────────────────────┘

卡片区：每项一张卡片（从上到下排列）
┌─────────────────────────┐
│ │ 名称          ¥2.6/周 │ ← 左侧色条 + 名称 + 核心数字
│ │ 副标题         ¥81/月  │ ← 副标题 + 次要数字
│ │ 标签1  标签2   标签3  │ ← 价格/属性标签
│ │ 公式/详情...          │ ← 可展开的计算公式或说明
└─────────────────────────┘

底部：可视化对比
┌─────────────────────────┐
│ 名称 ████████████ $100  │ ← 横向条形图
│ 名称 ████ $25           │    宽度按数值比例缩放
└─────────────────────────┘
```

### 设计要点

- **排序**：从优到差排列（最便宜/最快/最高分在最上面）
- **左侧色条**：4px 宽，每个项目用不同品牌色或强调色区分
- **核心数字**：右侧大字显示（22px 加粗），次要信息小字灰色
- **标签行**：用 `background:rgba(255,255,255,0.04)` 的小圆角标签
- **公式区**：monospace 字体 + 半透明黑底，可折叠
- **底部条形图**：宽度按比例，最便宜项为 100%，其余等比缩放
- **最小条宽**：60px（`min-width:60px`），避免最短项看不到
- **国旗/图标**：emoji 在部分设备显示异常，用纯文字标签替代

### CSS 骨架

```css
.card { background:rgba(15,20,40,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:18px 20px; margin-bottom:12px; position:relative; overflow:hidden; }
.card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; }  /* 左侧色条 */
.card-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.card-name { font-size:18px; font-weight:700; }
.card-cost { text-align:right; }
.card-week { font-size:22px; font-weight:700; }  /* 核心数字 */
.card-month { font-size:11px; color:#888; }
.card-prices { display:flex; gap:12px; margin-bottom:10px; font-size:12px; color:#999; }
.card-prices span { background:rgba(255,255,255,0.04); padding:3px 8px; border-radius:4px; }
.card-formula { font-size:12px; color:#777; background:rgba(0,0,0,0.2); padding:8px 12px; border-radius:6px; font-family: monospace; line-height:1.5; }
.bar-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.bar-label { width:100px; font-size:13px; text-align:right; color:#aaa; }
.bar-track { flex:1; height:24px; background:rgba(255,255,255,0.04); border-radius:4px; }
.bar-fill { height:100%; border-radius:4px; display:flex; align-items:center; justify-content:flex-end; padding-right:8px; font-size:11px; font-weight:700; }
```
