# 表现力技法库(Design Techniques)——可组合的惊艳配方

> 何时读我:产出需要"惊艳/有冲击力"的整页时,从这里挑 3-5 个技法自由组合;过闸但被评"平淡"时来补技法。
> 最短路径:选型规则→技法清单(每条含完整代码)→组合建议→验收。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。姊妹篇:expressive-design.md(法则与公式)。

# 选型规则

1. 每页选 **1 个 hero 技法 + 2-3 个结构技法 + 1 个签名动效**,不要贪多——技法堆叠过载比没有更糟;
2. 主题的 voice/signature 决定取舍(如"静"主题不选 marquee);
3. 所有技法零渐变、零外链资产、纯 CSS/SVG 可实现,且都在机械闸覆盖内;
4. 组合示例:夜松页 = R1 暗幕颗粒 hero + R4 幽灵序号 + R9 非对称网格 + R3 滚动揭示。

---

## R1 · 暗幕颗粒 hero(夜幕开场)

近黑大底 + 巨型衬线 + 颗粒噪点 + 出血图形。深色用主题最深色(非纯黑),主字用主题最浅色。

```css
.night-hero{position:relative;min-height:100svh;background:var(--night);color:var(--pale);overflow:hidden}
.night-hero::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.07;pointer-events:none}
.night-hero h1{font-family:var(--serif);font-weight:900;font-size:clamp(56px,11.5vw,148px);line-height:1.06}
.hero-lede{color:var(--mist);font-size:16.5px;max-width:520px}   /* 次字用雾灰级 */
```
```html
<!-- 颗粒噪点(data-URI,零外链) -->
:root{--grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E")}
```
暗幕字色三件套(以 #01161E 底实测):主字=主题最浅色、次字=#9FB3BC 级雾灰(≥4.5:1)、链接=板内浅强调。
**CTA 反转**:深强调色在暗幕禁做字/底,主按钮用浅底深字。

## R2 · 巨字对微字(尺度戏剧)

展示字与正文比 ≥6 倍(clamp 上探 120px+),旁边配 11-12px 加宽字距微标签——对比产生高级感。

```css
.h-giant{font:900 clamp(56px,11.5vw,148px)/1.06 var(--serif)}
.h-micro{font:600 11px var(--sans);letter-spacing:.34em;text-transform:uppercase;color:var(--ink2)}
/* 竖排侧标(编辑感,零成本) */
.side-label{position:absolute;right:26px;writing-mode:vertical-rl;letter-spacing:.5em;font:600 11px var(--sans);color:var(--ink2)}
```

## R3 · 滚动揭示(动效纪律)

```js
document.documentElement.classList.add("js");
const io = new IntersectionObserver((es) => es.forEach((e) => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
}), { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
```
```css
html:not(.js) .reveal{opacity:1}                    /* 无 JS 兜底 */
.reveal{opacity:0;transform:translateY(30px);transition:opacity .9s ease,transform .9s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1!important;transform:none!important}}
```
组内交错:子元素 `transition-delay:.1s/.2s/.3s`,≤3 档。

## R4 · 幽灵序号/幽灵字(零成本记忆点)

```css
.work{position:relative;overflow:hidden}
.work .ghost{position:absolute;right:14px;top:2px;font:900 84px var(--serif);
             color:var(--surface);line-height:1;pointer-events:none}
```
序号/单字压在卡片或节头角上;颜色用底色系(surface/底色加深一档),永远不抢正文。

## R5 · 跑马灯横带(编辑签名动效)

分隔两幕的文字横带,无限匀速滚动。静态、克制、有杂志感。

```css
.marquee{overflow:hidden;background:var(--ink);color:var(--pale);padding:14px 0}
.marquee .track{display:inline-flex;white-space:nowrap;animation:mq 26s linear infinite}
.marquee span{font:700 15px var(--sans);letter-spacing:.24em;padding:0 28px}
@keyframes mq{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.marquee .track{animation:none}}
```
```html
<div class="marquee" aria-hidden="true"><div class="track">
  <span>选料看三年</span><span>开料留余地</span><span>养器交给你</span>
  <span>选料看三年</span><span>开料留余地</span><span>养器交给你</span>
</div></div>
```
内容重复两遍实现无缝循环;`aria-hidden` 因纯装饰。

## R6 · 粘性堆叠幕(章节图钉)

各幕 `position:sticky; top:0`,后幕上滑覆盖前幕——滚动即翻页,结构感极强。

```css
.act{position:sticky;top:0;min-height:100svh}
/* 每幕实高 ≥100svh,后一幕自然覆盖前幕;深浅交替 = 明暗旅程自带 */
```
注意:幕内底部内容会被覆盖,预留 padding-bottom;移动端慎用(浏览器地址栏伸缩干扰 sticky)。

## R7 · 双色调影像(任意图片上主题色)

没有艺术指导的图片,用双色调统一进主题——黑白化后以主题色着色。

```css
.duo{background:var(--accent)}
.duo img{filter:grayscale(1) contrast(1.05);mix-blend-mode:screen;opacity:.92}
/* 亮底版: mix-blend-mode:multiply + 底色用浅强调色 */
```
`<figure class="duo"><img src="..." alt="..."></figure>`
screen 用在暗底(深强调色底),multiply 用在亮底(浅强调色底)。图片照旧是它自己,但颜色是主题的。

## R8 · 悬停揭示卡(作品网格交互)

```css
.work{position:relative;overflow:hidden}
.work .cover{transition:transform .5s ease}
.work:hover .cover{transform:scale(1.05)}
.work .veil{position:absolute;inset:0;background:var(--ink);opacity:0;transition:opacity .3s ease;
           display:flex;align-items:flex-end;padding:20px;color:var(--pale)}
.work:hover .veil{opacity:.88}
```
悬停 = 图片微放大 + 主题深色纱幕淡入 + 一句说明。纱幕用纯色(禁渐变)。

## R9 · 非对称编辑网格(打破三等分)

```css
.works{display:grid;grid-template-columns:repeat(12,1fr);gap:26px}
.work{grid-column:span 4}
.work:nth-child(1){grid-column:span 5}
.work:nth-child(3){grid-column:span 3}
.work:nth-child(2),.work:nth-child(5){transform:translateY(34px)}   /* 错位下沉 */
@media (max-width:900px){.works{grid-template-columns:1fr 1fr}.work{grid-column:auto}
  .work:nth-child(2),.work:nth-child(5){transform:none}}
@media (max-width:600px){.works{grid-template-columns:1fr}}
```
每行跨度合计 12;错位只做一层;窄屏必须重置跨度与位移(不做就散架)。

## R10 · 巨型裁切字符(节水印)

一个超大字符被容器裁切,做节的背景水印。

```css
.sec-mark{position:absolute;right:-2%;top:-8%;font:900 clamp(200px,28vw,420px)/1 var(--serif);
          color:var(--surface);pointer-events:none;user-select:none}
.sec-body{position:relative;z-index:1}
```
一个节只一个字符;颜色=底色系加深一档;正文压在其上(z-index 分层)。

---

## R11 · 数据表静默纹(表格工艺)

数据表不加斑马纹底色,只用发丝线与 tabular-nums;数字右对齐即对齐了个位。

```css
table.grid{width:100%;border-collapse:collapse;font-size:14.5px}
.grid th{background:var(--surface);text-align:left;padding:12px 18px;font-weight:700}
.grid td{padding:12px 18px;border-top:1px solid var(--line)}
.grid td.num{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
```
表头一片 --surface 即可,禁渐变禁重底纹;行高 ≥44px 触控友好;首列不给强调色。

## R12 · 表单的安静秩序(输入件)

输入件是页面最吵的元素,让它安静:实色底、发丝边、聚焦一根强调线。

```css
.field{display:block;margin-bottom:18px}
.field label{display:block;font:600 13px/1.4 var(--sans);margin-bottom:6px}
.field input,.field select,.field textarea{width:100%;background:var(--bg-raised);
  border:1px solid var(--line);border-radius:var(--r-sm,8px);padding:11px 14px;
  font:inherit;color:var(--ink)}
.field :focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.field .hint{font-size:12.5px;color:var(--ink-muted);margin-top:5px}
```
错误态换字色与边线(不要只靠红色底);标签永远可见(禁 placeholder 当标签)。

## R13 · 空状态的体面(留白叙事)

空状态不是放一个插画完事:一句人话 + 一个下一步。

```html
<div class="empty">
  <p class="empty-t">还没有条目</p>
  <p class="empty-s">第一条会出现在这里——先建一个。</p>
  <a class="btn" href="#">建第一个</a>
</div>
```
```css
.empty{text-align:center;padding:72px 24px}
.empty-t{font:700 17px/1.4 var(--serif)}
.empty-s{color:var(--ink-muted);font-size:14px;margin:8px 0 18px}
```
按钮用主行动样式;禁止 emoji 充当插画;空态文案禁"哎呀/呜呜"式卖萌。

## R14 · 仪表盘外壳(一屏一主角)

仪表盘的惊艳来自克制:一张主卡占视觉重心,其余等权小卡靠边。

```css
.dash{display:grid;grid-template-columns:repeat(12,1fr);gap:18px}
.dash-hero{grid-column:span 7;min-height:320px}
.dash-side{grid-column:span 5}
.dash-cell{grid-column:span 4}
@media (max-width:900px){.dash-hero,.dash-side,.dash-cell{grid-column:span 12}}
```
主卡放唯一大数字(巨字对微字:数值 40px+ 配 12px 标签);辅助 KPI 不抢字号;
图表色用 chartpal 派生,禁彩虹——超过 6 个系列先想分组。

---

# 组合建议(按页型)

| 页型 | 组合 |
|---|---|
| 品牌/工坊页 | R1 + R4 + R9 + R3,收尾暗幕 CTA |
| 产品发布页 | R1 + R5 跑马灯分隔 + R7 产品图双色调 + R6 粘性堆叠特性幕 |
| 数据/后台页 | R14 仪表盘外壳 + R11 数据表 + R12 表单 + chartpal 图表色 |
| 内容/社区页 | R9 非对称网格 + R8 悬停揭示卡 + R13 空状态 + R4 幽灵序号 |
| 作品集 | R9 网格 + R8 悬停揭示 + R2 巨字对微字 + R10 节水印 |
| 内容/杂志页 | R2 + R6 粘性章节 + R3 |

# 验收(组合后必跑)

- aesthete_report/evidence PASS(声明色板从页内取)
- lint 无 P0;字号 ≥12px;锚点 scroll-margin-top 防 sticky 遮挡
- 手机 375px 无横向溢出;prefers-reduced-motion 全关
- 五镜快审:一屏一主角、签名唯一、强调剂量 ≤10%
