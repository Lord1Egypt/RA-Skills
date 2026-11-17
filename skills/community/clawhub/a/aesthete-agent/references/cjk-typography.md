# 中文排印法则（CJK Typography Rules）

> 何时读我:产出中文页面/双语页面,或中文态排印不如英文态精致时。
> 最短路径:字体栈→大标题三铁律→字重子集→标点混排→验收清单。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

中文页面达不到英文态的精致度，问题从来不是"字体不好看"，而是四件可修的事：
断行、字重、标点、混排。本文件是机械可执行的规则 + 直接可粘的 CSS 模式。
调研底座：W3C CLREQ、Chrome 官方 i18n 公告、MDN、Adobe/Google Fonts 官方字重表；
体积数字为本引擎实测（fonttools 4.62，Noto Serif CJK SC Bold 24.3MB → 标题子集 67KB）。

## 规则一：字体栈必须显式列全 CJK

缺失 CJK 声明时，中文掉进系统默认黑体——笔画生硬，与衬线版式气质断裂（用户可感知的"变丑"）。

```css
:root{
  --sans:system-ui,-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif;
  --serif:Georgia,"Times New Roman","Songti SC","STSong","SimSun",serif;
}
body{font-family:var(--sans); line-height:1.7}   /* 中文正文行高 1.65-1.8 */
```

- 标题用 `--serif`（西文走 Georgia，中文递进到宋体族）——同一规则下中英文获得同构的衬线气质。
- 正文永远 `--sans`；宋体不做正文（屏幕上发虚）。

## 规则二：中文大标题三条铁律

1. **受控断行，禁寡字**。衬线大标题必须手动 `<br>` 控制断点，断成字数平衡的两行（如 6/7）；
   绝不允许自然断行产生 ≤2 字的尾行（孤行寡字 = 中文排版第一眼丑）。
2. **合成字重**。宋体族没有粗字重，`font-weight:900` 单独无效。用描边合成：

```css
body[data-lang="zh"] .hero h1{
  font-family:var(--serif); font-weight:900;
  letter-spacing:0.05em; line-height:1.18;
  -webkit-text-stroke:0.9px currentColor;   /* 62px 级大标题 0.9px；30px 级 h2 用 0.5px；更大则 1.2px */
}
```

   过大（>1.5px）会糊。有条件时优先规则三的真字重，描边是零依赖兜底。
3. **kicker/眉题中英混排统一字距**（0.18em 级），并去掉 `text-transform:uppercase`
   ——中文没有大写，混排段以中文节奏为准。

## 规则三：标题真字重 = 思源宋体子集（推荐，离线可用）

思源宋体（Source Han Serif / Noto Serif SC，OFL-1.1 可自由嵌入）共 7 字重，
Heavy 对应 `font-weight:900`，专为标题设计。完整字体 24.3MB 不可上网页；
**标题字符集子集化后仅 67KB woff2（本引擎实测，约 190 字符）**——一次加载，缓存永续。

```bash
# 可选依赖：pip install fonttools brotli
python scripts/make_cjk_subset.py --text "让每一处配色，都经得起评审。看它渲染工作原理安装" \
    --weight Bold --out cjk-title.woff2
```

```css
@font-face{
  font-family:"CJK Serif Title";
  src:url("cjk-title.woff2") format("woff2");
  font-display:swap; font-weight:900;
}
body[data-lang="zh"] .hero h1{font-family:"CJK Serif Title",var(--serif); font-weight:900}
```

- `font-display:swap`：加载前显示宋体 fallback（同为衬线，不跳风格）；加载后无缝换成粗宋。
- 只对**标题**用子集（字符集小、体积可控）；正文永远系统字体。
- 标题文案变更后必须重新生成子集（字符没进子集会回退宋体，不算坏损但字重不齐）。
- CDN 路线（有外网保证时才用）：Google Fonts `Noto+Serif+SC`（wght 200-900 可变字体）、
  npm `@fontsource-variable/noto-serif-sc`；国内可达镜像 fonts.loli.net / fonts.google.cn。
  本引擎默认自托管子集——离线可用是铁律，不引入外部 CDN 依赖。

## 规则四：标点与混排（2025 起 CSS 原生）

```css
.zh-body{
  text-autospace: normal;        /* 中西文之间自动 1/8em 间隙（Baseline 2025，全主流浏览器）；
                                    内容已有空格时不重复加——对存量内容无损 */
  text-spacing-trim: normal;     /* CJK 标点挤压（行内连续标点+行缘）；仅 Chromium 123+，
                                    其他浏览器忽略即降级，可安全前置 */
}
```

- 手写排版仍推荐在 CJK/西文交界处敲一个空格（发布系统可能不经过这两条属性）。
- 行尾全角标点的空隙：受控断行让它落在语义点即可，不必强行悬挂。

## 规则五：中文页面字号与密度

- 正文 15–17.5px（下限 12px），行高 1.65–1.8，字距 `letter-spacing:0.01em`；
- 标题字距 0.02–0.05em（宋体标题加字距更见排印感；黑体标题不加）；
- 大标题字号维持英文体系的倍率（h1 ≈ 3.3× 正文），宋体灰度低靠字号与描边补重量；
- 行长：中文正文每行 35–42 字（约 max-width 660px @17px），与英文 60-75ch 对应。

## 验收清单（中文交付物过这五条）

1. 字体栈显式含 PingFang SC / Microsoft YaHei / Noto Sans SC；
2. 大标题断行手动控制，无 ≤2 字尾行；
3. 标题字重：真字重子集或 text-stroke 合成，二选一必有；
4. 中英混排间隙：text-autospace 或手敲空格，二选一必有；
5. 正文行高 1.65–1.8、行长 35–42 字。
