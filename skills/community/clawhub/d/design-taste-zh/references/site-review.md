# 网站评审 —— 给任意 URL 打分并美化

当用户要求评审、对标或美化一个线上网站（评审网站 / 主页评审 / 网站美化 / 对标 / website review）时使用。输出一份报告（使用用户的语言；`--lang zh|en`，本中文版默认 `zh`），包含评分、P0/P1/P2 问题和具体到 token 级的修改方案。

## 1. 抓取与测量

```bash
pip install playwright && python3 -m playwright install chromium   # 一次性安装；脚本自身不下载任何东西
python3 scripts/review_site.py https://example.com --out review-example --industry Software/Cloud --mobile
```

- 脚本使用无头 Chromium。它加载页面、等待网络空闲、尝试关闭 cookie 横幅（常见按钮文字以及 OneTrust/TrustArc 选择器），并滚动页面触发懒加载。
- 输出 `fold.png`（1440×900）、`full.png`（整页，最高 8000px）、`mobile.png`（390×844，仅在 `--mobile` 时）、`metrics.json` 和报告骨架 `report.md`。
- `--industry` 取 `scripts/benchmarks.csv` 中的值之一：Pharma、Finance、Internet、Software/Cloud、Semiconductors、Hardware/Devices、Retail、Luxury、Energy、Consumer Goods、Industrial、Aerospace。
- 如果脚本提示页面疑似被拦截（403、“Access Denied”、“Just a moment”），在报告中如实说明。不要尝试绕过反爬保护。请用户提供截图，或改为评审本地/预发布构建。
- 本地或开发服务器同样可用：传入 `http://localhost:3000`。

指标取自承载文字的可见元素的计算样式：不同颜色值（文字/背景/边框）、字体族、至少出现两次的字号、字重、圆角和阴影值、渐变、Hero 标题字号（首屏最大文字）、正文字号（≤20px 文字按字符数加权的众数）、按字符加权的 WCAG 对比度、低于 AA 的文字占比，以及首屏媒体占比。

### 1b. 关键图像（首屏主图）

- 脚本还会把首屏中最大的图片/视频/背景元素（占首屏 ≥ 12%）保存为 `hero.png`，并对其运行 `review_image.py`，输出到 `hero-image/`（metrics.json、palette.png、thirds-overlay.png、report.md）。需要 Pillow + numpy；缺失时会注明跳过。主图分数**仅供参考**，不改变网站指标分。
- 用 `image-aesthetics.md` 评主图（按情况选类型 `photo`、`product` 或 `illustration`）：主体是否清晰、配色是否与品牌 token 同源、压在图上的文字可读性、生成图像的 AI 痕迹清单、分辨率与显示尺寸是否匹配。
- 其他关键图像（产品图块、团队照片、OG/分享图）：截图或下载后运行 `python3 scripts/review_image.py <img> --type product|photo|social`。图像问题写进同一份 P0/P1/P2 清单，标注【图片】。

需要打折扣的已知噪声：轮播、产品色块页（Apple 式分区会抬高颜色数）、没渲染出来的视频、关不掉的弹层。

## 2. 评分

**总分 = 0.45 × 指标分 + 0.55 × 视觉分**，与基准库公式相同，因此分数可直接比较。

指标分（脚本计算）构成：
- 色彩 25%：超过 12 色每多 1 色 −5，超过 3 个渐变每多 1 个 −1.5
- 字号体系 25%：超过 7 档每多 1 档 −10，超过 2 个字体族每多 1 个 −12，超过 3 种字重每多 1 种 −8
- 一致性 15%：超过 3 种圆角每多 1 种 −8，超过 3 种阴影每多 1 种 −10
- 层级 15%：40 + 15 × min(Hero/正文, 4)
- 可访问性 20%：对比度映射到 30–100，−60 × 低于 AA 占比，正文 <14px 再 −15

视觉分由你来打，1–10 再 ×10。依次看 `fold.png`、`full.png`、`mobile.png`：
| 分数 | 含义 |
|---|---|
| 9 | 标杆级（Lilly、Apple）：一个强焦点、标志性字体、无可挑剔的节奏 |
| 8 | 克制且令人记住，有小瑕疵（SpaceX、Inditex、JPMC） |
| 7 | 干净、合格，但普通或略忙 |
| 5–6 | 模板感、模块拥挤、层级弱、弹层问题 |
| 3–4 | 门户或促销墙，没有焦点 |
| ≤2 | 无样式或已损坏 |
评判这些方面：留白与间距节奏、层级清晰度、一致性、标志性元素，以及 AI slop 或杂乱迹象（见 SKILL.md 第 3 步）。移动端检查：无溢出、Hero 仍只有一个信息、点击区至少 44px。

## 3. 对标

- 对照 `benchmarks.md` §2 的目标值填写指标表。脚本已预填 ✅/⚠️。
- 从同行业打法（`benchmarks.md` §3）中选 1–2 个接近的标杆，指出具体差距，如“Hero 48px vs. IBM 54px / Robinhood 72px”。
- 估算排名：`1 + count(benchmarks.csv 中 score > 总分)`。与行业均分一起报告。

## 4. 报告模板

从脚本生成的 `report.md` 开始，替换每个 TODO（传 `--lang en` 可得英文骨架）：

```markdown
# 网站设计评审：<站点>
- URL / 行业 / 视口 / 截图 / 抓取时间（UTC+8）

## 1. 评分
指标分 X（45%）｜视觉分 Y（55%）｜**总分 Z**｜基准库约第 N/147 名，行业均分 M
子分：色彩/字号体系/一致性/层级/可访问性

## 2. 指标 vs 基准（Top 20 中位数）
（脚本生成的表格 + 1–2 句解读：哪些超标是"设计债"，哪些是测量噪音）

## 3. 对标
最接近的 1–2 个标杆，以及具体差距（数字）

## 4. 问题清单
### P0 — 可读性/可用性：低对比正文、弹层遮挡首屏、正文 <14px、移动端溢出、主 CTA 不可见
### P1 — 质感：颜色/字号/圆角/阴影超标、首屏多焦点、AI 模板感、门户化/促销化
### P2 — 打磨：间距节奏、字距/行高、图标风格不一、hover/focus 态缺失
每条写：现象（附数字或截图位置）→ 原因 → 修改方式

## 5. 美化建议
### Token 方案（CSS 变量；颜色 ≤12、字号 ≤7 档、圆角一族 ≤3、阴影 ≤2、渐变 0–1）
### Before → After 表（Hero / 导航 / 卡片 / CTA / 正文 / 页脚）
| 区域 | 现状 | 建议（具体值） |
### 预期收益：按改后的 token 数量重算指标分，作为估算

## 6. 一句话结论
```

建议的规则：
- 每条建议都必须给出数值：`48px → 64px/600，字距 −0.02em`，而不是“调大一点”。
- 保留品牌。强调色取自网站现有品牌色，修正它的用法而不是替换它。
- 按投入产出比排序：先合并 token、处理弹层，最后才动插画或照片。
- 如果用户想要代码，转入 **Redesign** 模式（`redesign.md`）并落地 token 方案。

## 5. 批量 / 竞品模式

要和竞品比较，对每个 URL 各运行一次脚本，把分数放进同一张表，每个站点配一句话点评。未经用户同意，不要抓取超过约 10 个站点。
