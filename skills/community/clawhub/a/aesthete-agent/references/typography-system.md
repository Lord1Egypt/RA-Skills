# 排印体系（Typography System）

> 何时读我:写任何含文字的页面之前;或产出"排版合格但无聊"、标题/正文没有张力、中英混排发涩的页面时。
> 最短路径:排印底座一行 CSS→字距字号律→行高对比律→眉题与巨标配方→验收清单。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。与 typescale(字阶生成)配合使用:本文档是语法,typescale 产数值。

排印是把文字本身当视觉材料,不是"把字摆上去"。以下规则全部可直接粘贴;标注【渐进】的在不支持的浏览器里自动降级为普通排印,可以放心写进任何页面。

## 规则一:排印底座(一段 CSS,全页生效)

以上经 Chromium 146 无头实测(2026-10-21):`text-autospace` 生效且数值精确(16px 字号 4 处边界=4px,与理论一致);`text-wrap: balance/pretty` 支持已证,但对 CJK 等宽字的收益未观测到(安全保留)。

```css
:root { -webkit-text-size-adjust: 100%; }
:lang(zh) { text-autospace: normal; }          /* 中西文之间自动 1/4 字距;现代浏览器已支持但默认关闭,必须显式声明 */
:lang(zh) { line-break: strict; }               /* 收紧行首行尾禁则(点号/结束引号禁行首等) */
h1, h2 { text-wrap: balance;  max-inline-size: 18ch; }  /* 标题分行均衡;仅 ≤6 行生效,给宽度约束 */
p          { text-wrap: pretty; }               /* 正文防寡行;不支持的浏览器自动忽略 */
```
说明:`text-autospace` 解决"汉字与西文/数字之间要 1/4 字宽"的混排节奏,是收益最大的一行;作者手工加的空格不受影响。

## 规则二:字距的字号律(方向感错了全页皆输)

- 大字号(≥2× 正文)**收紧**:Latin display `letter-spacing: -0.02em`(区间 -0.015 ~ -0.03);
- 全大写小标签**放宽**:`letter-spacing: 0.08em ~ 0.12em`(字号越小加越多);
- 正文小写:不动;
- **中文方块字任何字号禁止负字距**(笔画碰撞),大标题取 `0 ~ 0.02em`,眉题类取 `0.25 ~ 0.35em`。

```css
.display-latin { letter-spacing: -0.02em; }
.eyebrow       { letter-spacing: 0.1em; }
:lang(zh) h1   { letter-spacing: 0.01em; }
```
配套令牌(typescale 产出):`--track-display:-0.02em; --track-caps:0.1em; --track-zh-display:0.01em;`

## 规则三:行高对比律(层级靠行高差说话)

同一页面强制拉开:巨标 `1.05–1.15` / 导语 `1.5–1.6` / 中文正文 `1.7–1.85`(Latin 正文 1.5–1.6)/ 图注 `1.5`。巨标行高 ≥1.3 即"没有 display 感";中文正文 <1.6 发闷。相邻层级的间距比 ≥1.5 肉眼才可辨;标题的 margin-top ≥ 2× margin-bottom。

## 规则四:CJK 标点与禁则

- 标题与眉题开比例标点:`:lang(zh) :is(h1,h2,h3,.kicker) { font-feature-settings: "palt" 1; }`(全角标点转比例宽;**实测字体依赖:系统字体如微软雅黑无 palt/halt 特性零效果,只有带该 OpenType 特性的字体——如思源 v2——才生效;交付自带字体时才可靠**)。
- 破折号"——"与删节号"……"不可拆行:生成期包 `<span style="white-space:nowrap">——</span>`;
- 行距纪律:段落间距与首行缩进二选一,**不混用**。

## 规则五:可变字体加载纪律

思源系(Noto Sans/Serif SC)只有 wght 轴(无光学尺寸轴,`font-optical-sizing` 对中文无效):

```css
@font-face { font-family: "Noto Serif SC";
             src: url("…woff2") format("woff2-variations");
             font-weight: 200 900; }   /* 必须声明全轴范围,否则 900 档会被合成 */
h1 { font-weight: 900; }               /* 注册轴走 font-weight;勿用 font-variation-settings(低层,会覆盖高层) */
```
中文巨标质感差,八成是字体没加载真字重(合成加粗发虚)。Latin 可另配带 opsz 轴的衬线(`font-optical-sizing: auto`)。

## 规则六:眉题配方(巨标的标配前奏)

```css
.eyebrow { font: 600 12px/1.6 var(--font-sans); letter-spacing: 0.1em;
           text-transform: uppercase; color: var(--accent-ink);
           margin-bottom: 14px; }
```
中文替代配方:小一号(比正文小 2px)+ 字距 `0.25–0.35em` + 同强调色;**眉题文字必须短于主标**;与巨标间距 8–16px。眉题让巨标"有出处",是从"排版"到"编辑设计"的分水岭。

## 规则七:巨标与导语的对仗

```css
h1 { font-size: clamp(2.75rem, 6.5vw, 6rem); font-weight: 900;
     line-height: 1.1; letter-spacing: -0.02em;  /* 中文取 0.01em */
     text-wrap: balance; }
.lede { font-size: 1.3em; font-weight: 400; line-height: 1.55;
        color: var(--ink-muted); max-inline-size: 34ch; }
```
巨标最多两行;中英双语时英文副题 = 中文主标的 0.4–0.5 倍字号、weight 400,形成对仗;导语 = 1.25–1.4× 正文、列宽为正文的 0.8 倍。

## 规则八:数字排印

- 表格列/计时/价格/动态跳数:`font-variant-numeric: tabular-nums`;**正文叙述中的数字保持比例数字**(更好看,勿全局打开);
- Oversized metric(大数字带):数字 = 标签字号的 3–5×、weight 700+、`line-height:1`;单位缩至 `0.4em`/weight 400/muted 色;垂直方向用 baseline 对齐(`align-items: baseline`);

```css
.metric { display: flex; align-items: baseline; gap: 8px; }
.metric__num  { font-size: clamp(3rem, 6vw, 5.5rem); font-weight: 700;
                line-height: 1; font-variant-numeric: tabular-nums; }
.metric__unit { font-size: 0.4em; font-weight: 400; color: var(--ink-muted); }
```

## 规则九:渐进增强三件套(支持则加分,不支持无害)

```css
:lang(zh) { text-spacing-trim: normal; }            /* 标点挤压;实测同 palt——依赖字体 halt/chws,系统字体零效果 */
figcaption { hanging-punctuation: first allow-end; } /* 图注悬挂标点 */
@supports (initial-letter: 3) { .prose > p:first-of-type::first-letter
  { initial-letter: 3 2; font-weight: 700; margin-right: 8px; } }
```

## 排印验收清单(交付前逐项)

- [ ] 排印底座四行在(autospace/strict/balance/pretty)
- [ ] Latin display 字距为负、全大写小标签为正、中文无负字距
- [ ] 行高对比:巨标 ≤1.15,中文正文 ≥1.7,同页拉开
- [ ] 每个巨标有眉题,眉题短于主标;标题 margin-top ≥ 2× margin-bottom
- [ ] 中文正文 30–38 字/行(max-width 66ch 级),行高 1.7–1.85
- [ ] 表格与动态数字 tabular-nums,正文数字比例
- [ ] 可变字体 @font-face 声明全轴范围;巨标是真 900 非合成
- [ ] 跑 aesthete lint/audit 无字号下限与对比度违规
