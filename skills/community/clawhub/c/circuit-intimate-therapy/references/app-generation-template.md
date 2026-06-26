# 回答末尾 HTML App 的生成手册

## 使用方式

**每次本 skill 启用并实际回答时(见 SKILL.md "## 回答末尾的 HTML app 生成"中的跳过条件),回答最后一段必须用 Write 工具生成一个新的 HTML app**,然后用一行注明路径让用户用浏览器打开。

本份是 agent 端的"生成手册"。读取场景:
- 即将动手生成 app
- 不确定该选哪种原型
- 需要确认可用的 common.css class / common.js 函数清单
- 需要复制一份骨架开始改

不要把整份给用户看;它是 agent 自用的工具书。

---

## 路径与命名

```
~/circapps/generated/<kebab-name>.html
```

- 必须是 `circapps/generated/` 目录(与 12 个 canonical app 物理隔离)
- 文件名 kebab-case,反映本次生成的核心概念(不要含日期):
  - 好:`zener-threshold-tuner.html` / `volatile-to-validator.html` / `dismissing-attachment-trace.html`
  - 不好:`app13.html` / `demo.html` / `2026-05-08-test.html`
- 同名直接覆盖(用户连续问同主题就在迭代同一个 app)
- 父目录用 Write 工具会自动创建,不必预先 mkdir

回答末尾**完整**这样写:

> 演示:`~/circapps/generated/<file>.html`(浏览器双击打开)。简短一句话说这个 app 演示什么、关键控件是什么。

---

## 强制骨架(每个生成的 app 必须有)

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Gen · <短标题></title>
<link rel="stylesheet" href="../common.css">
</head>
<body>

<div class="nav">
  <a href="../index.html">← 索引</a>
  <span class="nav-sep">|</span>
  <span class="nav-title">Gen · <短标题></span>
</div>

<div class="container">
<h1><完整标题></h1>
<p class="subtitle"><一两句:这个 app 演示什么、和本次对话哪个概念对应></p>

<!-- 控件区 + canvas 区,用 .layout-2col 或 .layout-3col -->

</div>

<script src="../common.js"></script>
<script>
// 不要调 setNav() —— 它写死 href="index.html" 在子目录里会 404,上面已经手写了 nav

// 你的代码
</script>
</body>
</html>
```

**关键差异**(与 canonical app 比):
- 路径都加 `../`(`../common.css`、`../common.js`、`../index.html`)
- **不调 `setNav()`**;手写 nav

---

## 五种 app 原型(挑一种作为基础)

每条都标注:**何时选** + **借鉴哪个 canonical app** + **核心代码模式**。

### 原型 A:RLC 时域模拟器

**何时选**:用户讨论某种压力输入下情绪如何演化、谐振、阻尼、DC vs AC、过零判据。**最常用的原型。**

**借鉴**:`app01-rlc-response.html`(完整模板),`app06-damping.html`(特征根)

**核心模式**:
```js
const dt = 0.02, T_WIN = 30;
let state = [0, 0]; // [q, i]
let t = 0, history = [];

function vSource(t) { /* 根据 inputMode 返回 V */ }

function step() {
  const R = +rSlider.value, L = +lSlider.value, C = +cSlider.value;
  const deriv = (s, tt) => {
    const [q, i] = s;
    const V = vSource(tt);
    return [i, (V - R*i - q/C) / L];   // 串联 RLC: L i'' + R i' + i/C = V
  };
  state = rk4Step(state, t, dt, deriv);
  t += dt;
  history.push({t, q: state[0], i: state[1]});
  while (history.length && history[0].t < t - T_WIN) history.shift();
}

function loop() { step(); draw(); requestAnimationFrame(loop); }
loop();
```

并联 LC + 串联 R 在 common.js 没现成 ODE,自己写:
```js
// 并联 LC,源串联 R 给到节点
// 节点电压 v(L 上 = C 上),iL 流过 L,iC = C dv/dt
// 状态 [v, iL]:dv/dt = (i_R - iL)/C, diL/dt = v/L, i_R = (V - v)/R
```

### 原型 B:频率响应曲线

**何时选**:用户讨论 ω₀、敏感频段、共振峰、Q 值、扫频对比串/并。

**借鉴**:`app02-resonance.html`,`app05-conjugate.html`

**核心模式**:
```js
function drawResponse() {
  clearCanvas(ctx, W, H);
  const wMin = 0.1, wMax = 10;
  const p = makePlotter(W, H, {xMin: wMin, xMax: wMax, yMin: 0, yMax: 5});
  drawAxes(ctx, p, {});

  const points = [];
  for (let i = 0; i < 400; i++) {
    const w = wMin + (wMax - wMin) * i / 400;
    const Z = ZSeriesRLC(R, L, C, w);   // 或 ZParallelLC_withSeriesR
    points.push([w, Cx.abs(Z)]);
  }
  plotLine(ctx, points, p, {color: '#60a5fa'});

  // 标 ω₀
  const w0 = 1 / Math.sqrt(L * C);
  ctx.strokeStyle = '#f59e0b';
  ctx.setLineDash([4,4]);
  ctx.beginPath();
  ctx.moveTo(p.x2px(w0), p.padY); ctx.lineTo(p.x2px(w0), p.padY + p.plotH);
  ctx.stroke(); ctx.setLineDash([]);
}
```

### 原型 C:Z 平面定位

**何时选**:用户在做"我们家在哪一型"诊断 / 拖动 Z 向量 / Gottman 四区域。

**借鉴**:`app03-zvector.html`(必读)

**核心模式**:
- 复平面坐标:横 R,纵 X = ωL - 1/(ωC)
- 拖动黄点 → 反推 R / X → (固定 ω 时) 反推 L 或 C
- 按区域上色五种家庭:① 室友(R 大 X≈0)② 惯性(X 上)③ 隐忍(X 下)④ 燃烧(R≈0 X≈0)⑤ 健康(中心区)
- 按 Gottman 四类型加预设按钮
- 实时显示 |Z|、φ(角度)

### 原型 D:I-V 曲线

**何时选**:用户讨论二极管(阈值 / Zener / 整流 / Stonewalling I-V 形状)。

**借鉴**:`app07-diode-iv.html`

**核心模式**:
```js
function diodeI(V, type, params) {
  const Vt = params.Vt || 0.5;        // 正向阈值
  const Vz = params.Vz || -2;         // Zener 击穿
  const Is = params.Is || 1e-3;
  if (type === 'normal')   return V > Vt ? Is * (Math.exp((V-Vt)*5) - 1) : 0;
  if (type === 'zener')    return V > Vt  ? Is * (Math.exp((V-Vt)*5) - 1)
                                          : V < Vz ? -Is * (Math.exp((Vz-V)*5) - 1) : 0;
  if (type === 'led')      return V > Vt * 1.5 ? Is * (Math.exp((V-Vt*1.5)*5) - 1) : 0;
  if (type === 'rectify')  return Math.abs(V) > Vt ? Math.sign(V) * Is * (Math.exp((Math.abs(V)-Vt)*5)-1) : 0;
  return 0;
}
```

### 原型 E:多面板对比

**何时选**:同一刺激下对比 N 种依恋/Gottman/响应风格;**重点是让对比一目了然**。

**借鉴**:`app04-attachment.html`(四依恋类型),`app09-capitalization.html`(四响应风格)

**核心模式**:
- 一个共享的"输入"控件区
- N 个并列 canvas,每个独立模拟参数固定
- 标题用对比色(secure 蓝 / preoccupied 紫 / dismissing 灰 / fearful 红)

---

## common.css 速查(可直接用的 class)

| Class | 用途 |
|---|---|
| `.container` | 主容器,max 1400px,padding 20 |
| `.layout-2col` | grid 280px + 1fr |
| `.layout-3col` | grid 260px + 1fr + 280px |
| `.card` | 暗色卡片容器 |
| `.card-title` | 卡片标题(monospace,uppercase 12px) |
| `.controls` `.control-group` | 滑块组容器 |
| `.button-group` | 横向按钮组(自动 wrap) |
| `button.active` | 选中态按钮(蓝底) |
| `.metric-row` | 双栏指标行(label / value) |
| `.metric-label` `.metric-value` | 配 .metric-row |
| `.insight` | 蓝色信息框(默认 strong 蓝色) |
| `.warn` | 红色警示框 |
| `.good` | 绿色"好结果"框 |
| `.tag` | 小标签(monospace 10px) |

颜色变量(给 canvas 用):
```css
--accent: #60a5fa     /* 蓝 - 主体 */
--accent-2: #06b6d4   /* 青 - 副 */
--positive: #22c55e   /* 绿 - 正向 */
--negative: #ef4444   /* 红 - 负向 */
--warning: #f59e0b    /* 橙 - 警告/V 源 */
--inductor: #a78bfa   /* 紫 - L */
--capacitor: #fbbf24  /* 黄 - C */
--resistor: #f97316   /* 橙 - R */
--diode: #ec4899      /* 粉 - 二极管 */
```

---

## common.js 速查(可直接用的函数)

### 数值方法
```js
rk4Step(state, t, dt, deriv)   // RK4 一步;deriv: (state, t) => 同维数组
```

### 复数 / 阻抗
```js
Cx.c(re, im)  Cx.add(a,b)  Cx.sub(a,b)  Cx.mul(a,b)  Cx.div(a,b)
Cx.abs(z)     Cx.arg(z)    Cx.inv(z)    Cx.scale(z, s)
ZSeriesRLC(R, L, C, w)              // 串联 R + jωL + 1/(jωC)
ZParallelLC_withSeriesR(R, L, C, w) // R 串(L 并 C)
ZParallelLC(L, C, w)                // 纯并联 LC
```

### 绘图
```js
setupCanvas(canvas, w, h)            // HiDPI 配置,返回 ctx
clearCanvas(ctx, w, h, color?)       // 默认背景色清屏
makePlotter(w, h, {xMin,xMax,yMin,yMax,padX,padY}) // 返回 {x2px, y2px, ...}
drawAxes(ctx, p, {showZeroX, showZeroY, gridColor, textColor})
plotLine(ctx, points, p, {color, width})        // points: [[x,y], ...]
plotLineSigned(ctx, points, p, {posColor, negColor, threshold})  // 按符号变色
drawDashedHLine(ctx, yVal, p, {color, dash})
drawLabel(ctx, text, x, y, {color, font, align})
```

### UI
```js
bindSlider(id, valueId, fmt?)  // 滑块 + 显示值,返回 slider element
// 不要调 setNav() —— 在 generated/ 子目录里会指向错误的 index.html
```

---

## 决策树:从对话上下文 → 选哪种原型

| 对话主题 | 推荐原型 | 借鉴 app |
|---|---|---|
| 单个元件意义、压力输入响应、谐振 / 阻尼基础 | A 时域 | app01, app06 |
| ω₀ 是什么、敏感频段、扫频 | B 频响 | app02, app05 |
| 串联 vs 并联、灵魂伴侣、燃烧 vs 健康 | A 或 B 双栏对比 | app05 |
| Gottman 四类型 / 五种家庭 / "我们在哪一型" | C Z 平面 | app03 |
| 依恋四类型 / 同一刺激不同反应 | E 多面板 | app04 |
| 二极管(stonewalling / 阈值 / Zener / 整流) | D I-V 曲线 | app07, app10 |
| Demand-Withdraw 死循环 | A + 二极管(自定义节点) | app08 |
| Capitalization / 配对响应风格 | E 多面板 + 增益对比 | app09 |
| Forgiveness / 背叛 / Reactance | A + Zener | app10 |
| 混合多种(沙盒)/ "把电路调健康" | A + 综合评分 | app11 |
| 长程演化 / VSA / 蒙特卡洛 | A + 时间线漂移 | app12 |

---

## 上下文嵌入清单(让 app 真的"和本次对话相关")

**生成的 app 不该是泛化模板,要在 5 处嵌入本次对话的具体上下文:**

| 嵌入点 | 怎么做 |
|---|---|
| 标题 + subtitle | 写明本次讨论的具体问题 / 案例 / 来访者代号 |
| 默认参数值 | 用本次诊断推出的 R/L/C/DC 起始值,而非 canonical default |
| 预设按钮 | 加"当前态" / "目标态" / "X 个月后预测",值来自对话 |
| 诊断文字(.insight) | 引用对话里的具体语句、依恋类型、Gottman 类别 |
| 案例标签 | 如果是案例咨询,在某处显眼放"为 [来访者代号 / 主题] 定制" |

**反例**(不要这样做):
- 直接复制 app01 改个标题
- 滑块默认值 0.4/1.0/1.0(完全是 app01 的 default)
- 诊断文字泛化成"看 DC 和 AC 的关系"

**正例**:
- 用户案例是 18 年隐忍夫妻,生成的 app 默认 C=2.5(大), R=0.3(小), DC=0.2(弱正接近 0)
- 加预设按钮"当前(C 充电中)" / "假性翻篇" / "目标:R↑ + 泄洪"
- 诊断文字引用对话里"D 已经 18 年没主动提了"这一具体细节

---

## 质量清单(交付前必过)

- [ ] 文件路径在 `~/circapps/generated/` 下
- [ ] 引用 `../common.css` 和 `../common.js`
- [ ] **没**调用 `setNav()`,而是手写了 `<a href="../index.html">← 索引</a>` 的 nav
- [ ] 标题、subtitle、默认值、预设按钮、诊断文字至少有 3 处嵌入了本次对话的具体上下文
- [ ] canvas 用 `setupCanvas` 而不是直接 `getContext`(否则在 HiDPI 屏上糊)
- [ ] 至少有一段 `.insight` / `.warn` / `.good` 文字给来访者读
- [ ] 单页 HTML,无外部依赖(除 common.css/js)
- [ ] **回答的最后一行**给用户路径 + 一句话说明
- [ ] 不要把生成的 HTML 长源码贴在对话里;Write 工具就行,对话里只给路径

---

## 极简骨架(可直接复制改)

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Gen · 占位标题</title>
<link rel="stylesheet" href="../common.css">
</head>
<body>

<div class="nav">
  <a href="../index.html">← 索引</a>
  <span class="nav-sep">|</span>
  <span class="nav-title">Gen · 占位标题</span>
</div>

<div class="container">
<h1>占位标题(嵌入本次对话主题)</h1>
<p class="subtitle">占位副标题(嵌入本次对话具体问题)</p>

<div class="layout-2col">
  <div>
    <div class="card">
      <div class="card-title">参数</div>
      <div class="controls">
        <div class="control-group">
          <label>R <span class="value" id="rVal"></span></label>
          <input type="range" id="r" min="0" max="3" step="0.05" value="0.4">
        </div>
        <!-- ... 加更多滑块 ... -->
      </div>
    </div>

    <div class="card">
      <div class="card-title">预设</div>
      <div class="button-group">
        <button data-preset="current" class="active">当前态</button>
        <button data-preset="target">目标态</button>
      </div>
    </div>
  </div>

  <div>
    <div class="card">
      <div class="card-title">主图</div>
      <canvas id="main" width="900" height="320"></canvas>
    </div>
    <div class="insight">
      <strong>诊断:</strong> <span id="diag">...</span>
    </div>
  </div>
</div>
</div>

<script src="../common.js"></script>
<script>
const ctx = setupCanvas(document.getElementById('main'), 900, 320);
const rSlider = bindSlider('r', 'rVal', v => v.toFixed(2));
// ... 其他滑块

// 预设
const presets = {
  current: { r: 0.4, /* ... */ },
  target:  { r: 0.8, /* ... */ },
};
document.querySelectorAll('[data-preset]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-preset]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const p = presets[btn.dataset.preset];
    rSlider.value = p.r; rSlider.dispatchEvent(new Event('input'));
    // ...
  });
});

function draw() {
  clearCanvas(ctx, 900, 320);
  // ... 画图
}
function loop() { draw(); requestAnimationFrame(loop); }
loop();
</script>
</body>
</html>
```
