# 表现力语法(惊艳法则)——从"过闸"到"被记住"

> 何时读我:用户要"惊艳/有冲击力/高级感"的整页产出时;产出过闸但被评"平淡/凑合"时。
> 最短路径:惊艳公式→明暗旅程→巨字法则→质感配方→揭示动效→签名唯一→验收。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

# 为什么需要这一页

机械闸(对比度/色盲/slop/评分)保证"不难看、可读、不撞 AI 味",但**过闸 ≠ 被记住**。
"高雅"的安全解(浅底+衬线+留白)会收敛成"精致但平淡"——这是 AI 审美的第二个收敛陷阱
(第一个是紫渐变俗艳)。惊艳是可拆解的工艺,不是玄学:

## 惊艳公式(获奖级单页的公共因子)

**暗幕质感 hero + 巨字对微字 + 明暗旅程 + 滚动揭示 + 一个大胆强调 + 一个签名母题。**

## 一、明暗旅程(最容易缺的一幕)

全页至少一次**暗/亮幕转换**。单语域浅底页 = 平淡的第一根因。
- 深色(#0A1418 级近黑色,不是灰黑)可做:hero、引文幕、CTA 收尾幕;
- 暗幕文字三件套(以 #01161E 底实测):主字用最浅底色(16.7:1)、次字 #9FB3BC 级雾灰(8.5:1)、
  链接用板内浅强调色(9.9:1);**深强调色在暗幕不可做字**(1.8:1)——CTA 反转为浅底深字;
- 幕与幕之间就是"旅程":夜→晨→夜→夜,呼吸感来自明暗对撞,不是来自留白。

## 二、巨字法则(尺度戏剧)

- 展示级标题与正文的字号比 ≥6 倍,上限探 `clamp(56px, 11.5vw, 148px)`;
- **巨字配微字**:11-12px 加宽字距(.3em+)的 mono/sans 标签,贴在巨字附近——对比产生高级感;
- 巨字允许出血、被图形裁切、第二行换色(次级色 4-8:1 即可,巨字 ≥3:1 达标);
- 幽灵序号(84-120px,底色系)压在卡片角上是零成本的记忆点。

## 三、质感配方(颗粒,不是渐变)

暗幕必须叠颗粒,否则"平":
```css
--grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
.dark-act::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.07;pointer-events:none}
```
- 渐变仍是 P0 禁令;质感 = 噪点 + 平色分层 + 出血图形,三件套足够;
- 主题相关的"材质母题"用纯 SVG 平色画(木=年轮同心环,纸=噪点,山=剪影折线)。

## 四、滚动揭示(动效纪律)

```js
const io = new IntersectionObserver((es) => es.forEach((e) => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
}), { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
```
```css
.reveal{opacity:0;transform:translateY(30px);transition:opacity .9s ease,transform .9s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1!important;transform:none!important}}
```
- 每节 1-2 个 reveal 单元;卡片组可整体作为一个单元(组内交错用 transition-delay,≤3 档);
- 无 JS 兜底:html.js 类门控,.reveal 默认可见。

## 五、签名唯一(母题,不是装饰)

- 每页**只一个**被记住的视觉母题(年轮章/时间窗/幽灵数字……),可重复出现但主次分明
  (hero 大版=主签名,局部小版=品牌记号);
- 母题优先从**主题的 signature 字段**取;纯 SVG 平色实现,零外链。

## 六、构图勇气

- 12 列网格 + 不对称跨度(5+4+3/4+4+4)+ 相邻卡错位下沉(translateY 34px)——比三等分网格
  高级感立增;≤900px 折双列、≤600px 折单列时**必须重置跨度与位移**;
- 竖排标签(writing-mode:vertical-rl + letter-spacing .5em)贴暗幕右缘,零成本编辑感;
- 巨型图形出血(右缘 -16vw)比居中完整图形更有张力。

## 验收清单(发稿前逐项)

- [ ] 全页存在至少一次暗/亮幕转换
- [ ] 展示字/正文 ≥6 倍;有微字标签与巨字配对
- [ ] 暗幕叠颗粒;全页零渐变
- [ ] 滚动揭示存在且 reduced-motion 全关;无 JS 时内容可见
- [ ] 签名母题唯一且来自主题 signature
- [ ] 全对对比度达标(暗幕对用暗幕色表单独验);report/evidence PASS
- [ ] 手机 375px 无横向溢出;锚点跳转无 sticky 遮挡(scroll-margin-top)
