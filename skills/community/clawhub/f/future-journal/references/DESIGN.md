# 未来日记 — Design System

> 一套用于「每日三分钟书写」类工具的暖纸手账设计系统。
> 适用交付物：手机优先的单页 Web 应用、可打印手账页、配套 skill 的模板资源。
> 供 AI 编程代理（Cursor / Claude Code / Codex）直接消费。
>
> 结构：**第 1–9 节**是设计系统本体，**附 A** 是无障碍基线（WCAG 2.2 AA）检查清单，
> **附 B** 是不适用场景。
>
> **语言范围**：**默认简体中文（zh-CN）**，字体栈、字重、行高与断行规则按中文排版调校；
> **同时兼容英文排版**——西文回退到栈内的 `Georgia` / `-apple-system`，中英混排不会掉字体。
> 英文说明随包提供（`skill-card.md`）；需要其他语言的界面或句库可向作者提出。
> *Language scope: default locale is zh-CN, with rules tuned for Chinese typesetting;
> the stacks are bilingual and fall back to Georgia / -apple-system for Latin text.
> English documentation ships with the skill; other locales are available on request.*
>
> ⚠ **本文档中的色值必须与 `assets/index.html` 的实现一致。** 第 2 节末尾有变量名对照表
> （文档用 `--color-*` 语义名，实现用 `--ink` / `--accent` 等短名），改色时两处同时改，
> 并重算第 2 节的对比度实测表。

---

## 1. Visual Theme & Atmosphere

**设计哲学**：这不是一个 App，是一本纸。所有视觉决策服从同一个目标——让屏幕上的书写动作，尽可能接近在纸上写字的感觉。任何让人意识到"我在用软件"的元素，都是缺陷。

**视觉基调**：暖纸手账。暖米白纸底、极低对比、单一强调色、零装饰。

**五个核心特征**

1. **纸色而非白色** — `#FBF7EF` 米白，模拟未漂白纸浆。纯白 `#FFFFFF` 全局禁用，它会立刻把页面变成界面。
2. **单一强调色** — 赤陶 `#AD5534`，只用于"需要你注意"的地方：进度、选中态、今天这一格。像一枚印章，全局只此一色。
3. **两档字重** — 仅 400 与 500。禁用 600/700，粗体的重量感会破坏纸面书写的轻。
4. **衬线管内容，无衬线管界面** — 衬线承载"要读的、要写的"（日期、引导句、正文），无衬线承载"要点的"（按钮、标签、说明）。
5. **无渐变、无模糊、无发光** — 阴影仅用于表达纸张的层叠关系，不是装饰。

> 第 6 条（2026-09-19 补充，与上面五条并列）：**可读性优先于氛围。**
> 纸感和低对比之间会打架，打架时纸感让步：正文一律 ≥ 4.5:1，UI 元素 ≥ 3:1。
> 唯一被豁免的是描摹引导字——它的身份是"底稿"不是"正文"，见第 2 节的对比度表。


**光影与质感**：微阴影，多层、极低透明度、暖色偏移（`rgba(64,52,34,…)` 而非纯黑）。全局唯一允许的模糊是底部导航条的 12px 背景模糊——因为它是"浮在纸上的一层玻璃"，需要物理合理性。

**禁止**：玻璃拟态（除导航条）、渐变、拟物纹理贴图、图标库、插画、动效超过 250ms。

---

## 2. Color Palette & Roles

### Paper 纸面（最底层）

| 用途 | HEX | CSS 变量 | 场景 |
|---|---|---|---|
| 纸底 | `#FBF7EF` | `--color-paper` | body 背景 |
| 内嵌纸区 | `#F6F1E5` | `--color-paper-sunken` | 输入框底、描摹画布底、标签底 |
| 纸卡 | `#FFFDF8` | `--color-card` | 所有卡片表面 |

### Ink 墨色（文字）

| 用途 | HEX | CSS 变量 | 场景 |
|---|---|---|---|
| 主墨 | `#2B2925` | `--color-ink` | 标题、正文、手写笔迹 |
| 次墨 | `#5C574E` | `--color-ink-secondary` | 段落正文、副标题 |
| 弱墨 | `#746D60` | `--color-ink-tertiary` | 说明文字、49 格数字、底部 tab |
| 描摹灰 | `#ABA492` | `--color-trace` | 描摹引导字（浅灰印刷） |

> **弱墨从 `#918A7B` 改到 `#746D60` 的原因**：旧值在纸底上只有 **3.04–3.37:1**，
> 而它承担的全是 11.5–13px 的小字（提示语、轨道格数字、tab 文案），
> 属于正文级要求（≥4.5:1），实测不达标。新值不改色相、只压明度，纸感不变。

### Accent 印泥（唯一强调色）

| 用途 | HEX | CSS 变量 | 场景 |
|---|---|---|---|
| 赤陶 | `#AD5534` | `--color-accent` | 进度条、今天格、选中态、主按钮 |
| 赤陶深 | `#8F4425` | `--color-accent-hover` | 主按钮 hover |
| 赤陶浅 | `#FAEFE8` | `--color-accent-soft` | 徽标底、情绪标签选中底 |
| 描边赤陶 | `#E9CFC2` | `--color-accent-line` | 危险按钮边框 |

> **赤陶从 `#C2603A` 改到 `#AD5534` 的原因**：旧值上的白字只有 **4.18:1**，
> 而它是主按钮底色——白色 14px 文字属正文级（≥4.5:1），差一点点。
> 新值同上：保色相、压明度。


### Line 纸线

| 用途 | HEX | CSS 变量 | 场景 |
|---|---|---|---|
| 分隔线 | `#E7E0CF` | `--color-line` | 卡片边框、手账横线、未完成格 |
| 浅分隔线 | `#F0EBDD` | `--color-line-soft` | 极弱分隔 |

### Semantic 语义色

| 用途 | HEX | CSS 变量 | 场景 |
|---|---|---|---|
| 完成（苔绿） | `#48704D` | `--color-success` | 已写格数字、已实现愿望边框 |
| 完成底 | `#E8F0E6` | `--color-success-soft` | 已写格背景 |
| 完成线 | `#CBDCC6` | `--color-success-line` | 已写格边框 |
| 警示 | `#8F4425` | `--color-warning` | 过去时提示文字（复用赤陶深） |

> 完成色从 `#4F7A54` 改到 `#48704D`：旧值在 `--color-success-soft` 上只有 4.25:1。

### 对比度实测表（WCAG 2.2 AA）

阈值：正文/小字 **4.5:1**，大字（≥24px 或 ≥18.66px 粗）与 UI 组件 **3:1**。
下表是**从实现里读出的真实色值**算的，不是设计意图值——改任何颜色后必须重算这一张表。

| 配对 | 实测 | 阈值 | 结果 |
|---|---|---|---|
| 主墨 on 纸底 | 13.59:1 | 4.5 | ✅ |
| 主墨 on 卡片 | 14.28:1 | 4.5 | ✅ |
| 次墨 on 纸底 | 6.71:1 | 4.5 | ✅ |
| 弱墨 on 纸底 | 4.79:1 | 4.5 | ✅ |
| 弱墨 on 沉纸 | 4.55:1 | 4.5 | ✅ |
| 弱墨 on 卡片 | 5.04:1 | 4.5 | ✅ |
| 赤陶 on 纸底（今天格数字/描边） | 4.76:1 | 3 | ✅ |
| 赤陶 on 沉纸（今天格数字） | 4.52:1 | 3 | ✅ |
| 白字 on 赤陶（主按钮） | 5.09:1 | 4.5 | ✅ |
| 白字 on 赤陶深（hover） | 6.95:1 | 4.5 | ✅ |
| 完成色 on 完成底 | 4.87:1 | 4.5 | ✅ |
| 描摹灰 on 沉纸 | **2.20:1** | — | ⚠ 刻意 |

**为什么描摹灰允许只有 2.20:1**

它不是给人"读"的，是给人"盖着描"的底稿。真按 4.5:1 做成深灰，描上去的笔迹（`#2B2925`）
和底稿就分不清了——描摹这个动作本身就失效了。等价性由另一条路径保证：

- 想读这句引导句的人，正文区（`.type-target`）用的是 `--color-ink-tertiary`（4.55:1），达标
- 键盘 / 读屏用户走「照着打一遍」，灰字同时以可访问文本形式暴露
- `file://` 打印版把描摹字加深到可读（打印不走这条豁免）

**不要在别处复用 `--color-trace`。** 它是一个有单一用途的色值，不是"第四档墨色"。

### 暗色底（toast）反色配对

toast 是全局唯一的反色浮层：`--color-ink` 底 + `--color-paper` 字，实测 **13.59:1**。达标。

### 变量命名对照（文档 ↔ 实现）

本文档用 `--color-*` 语义名，`assets/index.html` 里用的是短名。**两套名字必须同时改。**

| 文档名 | 实现名 | 文档名 | 实现名 |
|---|---|---|---|
| `--color-paper` | `--paper` | `--color-ink` | `--ink` |
| `--color-paper-sunken` | `--paper-2` | `--color-ink-secondary` | `--ink-2` |
| `--color-card` | `--card` | `--color-ink-tertiary` | `--ink-3` |
| `--color-line` | `--line` | `--color-trace` | `--trace` |
| `--color-line-soft` | `--line-soft` | `--color-accent` | `--accent` |
| `--color-success` | `--ok` | `--color-success-soft` | `--ok-soft` |

`--accent-2` = `--color-accent-hover`，`--accent-soft` = `--color-accent-soft`。
`--r`（10px）/ `--r-lg`（16px）是圆角变量，`--sh-1` / `--sh-2` 是两档阴影。

> **canvas 拿不到 CSS 变量。** 描摹画布里的颜色必须写成字面量，且要和 `:root` 保持一致——
> 实现里集中在 `var INK = '#2B2925', GUIDE = '#ABA492';` 两个常量，改色时两处一起改。


### Shadow 阴影色

| 用途 | 值 | 变量 |
|---|---|---|
| 阴影基色 | `rgba(64,52,34,0.05)` | `--shadow-color-1` |
| 阴影强化 | `rgba(64,52,34,0.08)` | `--shadow-color-2` |
| 阴影深层 | `rgba(64,52,34,0.16)` | `--shadow-color-3` |

> 阴影色必须是暖褐（`64,52,34`），不是黑。用纯黑会让卡片像 UI 浮层而不是纸。

---

## 3. Typography Rules

### Font Family

```css
--font-serif: "Songti SC", "STSong", "Source Han Serif SC",
              "Noto Serif SC", Georgia, serif;
--font-sans:  -apple-system, BlinkMacSystemFont, "PingFang SC",
              "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
```

**分配规则**：衬线用于内容层（日期、引导句、用户书写内容、网格数字）；无衬线用于界面层（按钮、标签、说明、导航）。混用会立刻让页面"不像手账"。

**语言范围 / Language scope**：字体栈按**中英双语**定义，不是中文单语栈 ——
中文默认走 `Source Han Serif SC` / `PingFang SC`，**西文自动回退到栈内的 `Georgia`（衬线）
与 `-apple-system` / `BlinkMacSystemFont`（无衬线）**，中英混排不会掉字体。
界面文案默认简体中文，英文说明见 `skill-card.md`；用户如需其他语言的界面或句库可向作者提出。
The stacks are bilingual: Chinese text resolves to the SC families, Latin text falls
back to Georgia / -apple-system in the same declaration. Default UI locale is zh-CN;
English documentation ships with the skill; other locales are available on request.

### Type Scale

| 层级 | 字号 | 字重 | 行高 | 字距 | 用途 |
|---|---|---|---|---|---|
| Display Hero | 34px / 2.125rem | 400 | 1.35 | 0.06em | 封面主标题（未启用） |
| Display | 26px / 1.625rem | 400 | 1.45 | 0.04em | 立愿页问句（未启用） |
| H1 / Date | 22px / 1.375rem | 400 | 1.5 | 0.02em | 页面主标题、当天日期 |
| Trace | 20px / 1.25rem | 400 | 1.95 | 0.05em | 描摹引导句（**唯一大行高**） |
| H2 | 17px / 1.0625rem | 400 | 1.6 | 0.02em | 区块标题 |
| Body L | 16px / 1rem | 400 | 1.75 | 0.01em | 输入框文字（**不可小于 16px**） |
| Body | 15px / 0.9375rem | 400 | 1.75 | 0 | 正文、卡片正文 |
| Body S | 13.5px / 0.84rem | 400 | 1.7 | 0 | 次要正文、按钮 |
| Caption | 12px / 0.75rem | 400 | 1.65 | 0.06em | 区块标签、说明、导航 |
| Micro | 11.5px / 0.72rem | 400 | 1.5 | 0.04em | 49 格数字、统计标签 |
| Nano | 11px / 0.69rem | 500 | 1.4 | 0.08em | 极弱标注 |

### 排版哲学

- **行高按用途分三档**：书写区 1.95（给手写的宽松感）、正文 1.75（可读）、界面 1.4–1.65（紧凑）。不要统一行高。
- **字距只在衬线正文上开**：`.02em–.06em`。中文衬线在屏幕上有压缩感，需要轻微字距回补；无衬线不加字距。
- **输入框字号硬锁 16px**：低于 16px 会触发 iOS Safari 自动缩放，页面会跳。这条不可协商。
- **书写区行高必须与横线背景的周期对齐**：`line-height: 32px` 对应 `repeating-linear-gradient` 的 32px 周期。改行高必须同步改横线周期。

---

## 4. Component Stylings

### Buttons

```css
/* Base */
.btn {
  font-family: var(--font-sans); font-size: 14px;
  border: 1px solid var(--color-line);
  background: var(--color-card); color: var(--color-ink-secondary);
  border-radius: 10px; padding: 11px 16px;
  transition: background .15s, border-color .15s, opacity .15s;
}
.btn:hover  { border-color: var(--color-ink-tertiary); }
.btn:active { background: var(--color-paper-sunken); }

/* Primary — 每屏最多一个 */
.btn.primary {
  background: var(--color-accent); border-color: var(--color-accent); color: #fff;
}
.btn.primary:hover { background: var(--color-accent-hover); border-color: var(--color-accent-hover); }

/* Ghost — 次级动作 */
.btn.ghost { background: transparent; }

/* Small — 卡片内动作 */
.btn.small { font-size: 12.5px; padding: 9px 13px; border-radius: 8px; }

/* Wide — 全宽主行动 */
.btn.wide { width: 100%; display: block; margin-top: 18px; padding: 14px; }

/* Danger */
.btn.danger { color: var(--color-accent-hover); border-color: var(--color-accent-line); }

.btn[disabled] { opacity: .4; cursor: default; }
```

**焦点环（全局必加，不可省）**

```css
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 8px;
}
input:focus-visible, textarea:focus-visible {
  outline: 2px solid var(--color-accent); outline-offset: 1px;
}
/* 强调色底上的焦点环要换色，否则赤陶描边压在赤陶按钮上等于没有 */
.btn.primary:focus-visible, .chip.on:focus-visible { outline-color: var(--color-ink); }
```

规则：

- **焦点环必须是一层"额外的描边"，不能只靠改边框色。** 只换颜色在触屏和低对比屏上完全不可见（WCAG 2.4.7）。
- `outline-offset` 必须是正数，让描边落在元素**外面**——`offset: 0` 会盖住 1px 边框。
- 焦点环颜色在纸底上是 4.76:1，满足 SC 1.4.11 非文字对比 3:1。
- **不要写 `outline: none`。** 需要去掉默认样式时，同时给出自定义焦点样式。


### Cards

```css
.card {
  background: var(--color-card);
  border: 1px solid var(--color-line);
  border-radius: 16px;
  padding: 20px;
  margin-top: 16px;
  box-shadow: 0 1px 2px rgba(64,52,34,.05), 0 1px 1px rgba(64,52,34,.04);
}
.card.tight { padding: 16px 18px; }
```

卡片堆叠间距固定 `16px`（`margin-top`）。不要用 `gap` 打破节奏。

### Inputs

```css
input[type=text], input[type=date], textarea {
  width: 100%; font-family: var(--font-sans); font-size: 16px;
  color: var(--color-ink);
  background: var(--color-paper-sunken);
  border: 1px solid var(--color-line);
  border-radius: 10px; padding: 11px 13px; outline: none;
  transition: border-color .15s, background .15s;
}
input:focus, textarea:focus {
  border-color: var(--color-accent);
  background: var(--color-card);
}
::placeholder { color: var(--color-ink-tertiary); }

/* 手账横线书写区 */
textarea {
  line-height: 32px; min-height: 128px; resize: vertical;
  background-image: repeating-linear-gradient(
    to bottom, transparent 0, transparent 31px,
    var(--color-line) 31px, var(--color-line) 32px);
  background-position: 0 11px;
}
```

**每个输入框必须有可访问名。** `placeholder` 不是标签——它一输入就消失，
读屏在"正在填写"这个最需要提示的时刻反而读不到。两条合规写法：

```html
<!-- 有可见文字标签：用 for / id 关联 -->
<label for="inpStart" class="hint">从哪天开始</label>
<input type="date" id="inpStart">

<!-- 视觉上不需要独立标签：用 aria-labelledby 指向别处的可见文字 -->
<p id="writeLabel" class="hint">用过去时写下今天希望发生的一件事</p>
<textarea id="inpWrite" aria-labelledby="writeLabel" aria-describedby="tenseHint"></textarea>
```

`aria-labelledby`（名字）和 `aria-describedby`（补充说明）是两件事，可以同时存在。


### Navigation（底部标签条）

```css
.tabbar {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 20;
  background: rgba(251,247,239,.94);
  backdrop-filter: saturate(180%) blur(12px);
  -webkit-backdrop-filter: saturate(180%) blur(12px);
  border-top: 1px solid var(--color-line);
  padding-bottom: env(safe-area-inset-bottom);
}
.tab {
  font-size: 12px; color: var(--color-ink-tertiary);
  padding: 11px 2px 12px; background: transparent; border: none;
  min-height: 48px;                       /* 触控目标，见第 8 节 */
}
.tab.on { color: var(--color-accent); }
```

当前页用 `aria-current="true"` 标注，且**同一时刻只能有一个**：

```html
<button type="button" class="tab on" data-v="today" aria-current="true">今日</button>
<button type="button" class="tab"    data-v="track">轨道</button>
```

`.tab` 的未选中文字用的是 `--color-ink-tertiary`（弱墨），改弱墨时必须重算这一处（现 4.79:1）。


### Badges / Chips

```css
.pill {                              /* 进度徽标 */
  font-family: var(--font-serif); font-size: 13px;
  color: var(--color-accent); background: var(--color-accent-soft);
  border-radius: 999px; padding: 4px 13px;
}
.chip {                              /* 情绪标签 */
  font-size: 13.5px; padding: 7px 15px; border-radius: 999px;
  border: 1px solid var(--color-line);
  background: var(--color-paper-sunken); color: var(--color-ink-secondary);
}
.chip.on { background: var(--color-accent); border-color: var(--color-accent); color: #fff; }
```

**选中态不能只靠颜色。** chip 是"单选且可取消"，视觉上是底色的变化，
读屏完全读不出来。所以每个 chip 都要带 `aria-pressed`，切换时同步更新：

```html
<button type="button" class="chip on" aria-pressed="true">感恩</button>
<button type="button" class="chip"    aria-pressed="false">安心</button>
```

`.chip.on` 的白字在赤陶上是 5.09:1，达标。

### 描摹区与打字区

两种「过一遍」的方式，共用同一位置：默认显示浅灰引导句，二选一切换。

```css
/* 灰字底（两种方式共用同一套字） */
.trace-static, .type-target {
  font-family: var(--font-serif); font-size: 20px;
  line-height: 1.95; letter-spacing: .05em;
  color: var(--color-trace);
}

/* 描摹画布 */
.trace-canvas { position: relative; background: var(--color-paper-sunken); border-radius: 10px; overflow: hidden; }
.trace-canvas canvas { display: block; touch-action: none; }

/* 打字回显：打对的字变深，打错的标赤陶下划线，当前待打的字用 2px 底边提示 */
.type-target span.hit  { color: var(--color-ink); }
.type-target span.miss { color: var(--color-accent); border-bottom: 1px solid var(--color-accent); }
.type-target span.cur  { border-bottom: 2px solid var(--color-accent); }
```

**画布是可访问性的死胡同，必须显式给出替代路径**

`<canvas>` 里的内容读屏读不到、键盘也进不去。它不能是唯一的路：

```js
cv.setAttribute('role', 'img');
cv.setAttribute('aria-label',
  '描摹区：用触控笔沿着浅灰字描一遍。没有触控笔请用下面的「照着打一遍」。');
```

`aria-label` 里要把**替代方案指出来**——只说"这是描摹区"等于告诉用户"此路不通"。

**拿不到 2D 上下文时必须降级，不能崩**

`canvas.getContext('2d')` 会返回 `null`（浏览器禁用画布、或同时存在的画布上下文超出上限——
iOS Safari 内存吃紧时会）。原实现直接 `.font = …` 赋值，抛 `TypeError`，
表现为**点了「用笔描」毫无反应**，用户完全不知道发生了什么。

```js
// 先探一次，拿不到就原地退回打字模式 —— 注意要在动 DOM 之前探，
// 否则会留下一个"描摹区已展开但是空的"半截界面
var probe = document.createElement('canvas').getContext('2d');
if (!probe) {
  toast('这台设备开不了描摹区，用下面的「照着打一遍」一样算写完了。');
  openTyping();
  return;
}
```

**凡是可能返回 null 的能力探测，都要在改动 DOM 之前做，并且给一句人话。**


**为什么必须有两种方式**：触控板/鼠标描摹是手眼分离——眼看屏幕、手动在别处，
实测无法控制，用户第三天就会放弃。触控笔（`pointerType === 'pen'`）没有这个问题。
所以按设备能力分流，而不是强行统一。

**画布参数（不可随意改）**

| 参数 | 值 | 原因 |
|---|---|---|
| 笔迹平滑 | 中点二次贝塞尔 | 直线连接在触控板上是锯齿，完全不可用 |
| 采样距离阈值 | `0.00006`（归一化区间平方） | 太小画毛刺，太大丢转折 |
| 线宽 | 2.6px | 要能盖住 20px 灰字的笔画 |
| 坐标存储 | 归一化 0–1 | 换设备 / 换屏后笔迹不错位 |
| 触控笔优先 | 检测到 pen 后忽略 touch | 防手掌误触，平板书写的必需项 |
| 采样点 | `getCoalescedEvents()` + fallback | 取触控笔原生高频点，线条才跟手 |

### 49 格轨道

```css
.grid49 { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.cell {
  aspect-ratio: 1; border-radius: 8px; padding: 0;
  border: 1px solid var(--color-line); background: var(--color-paper-sunken);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 11.5px; color: var(--color-ink-tertiary);
  appearance: none;                      /* 必须清掉，否则 button 会带上系统灰底 */
}
.cell.done   { background: var(--color-success-soft); border-color: var(--color-success-line); color: var(--color-success); }
.cell.today  { border: 2px solid var(--color-accent); color: var(--color-accent); font-weight: 500; }
.cell.future { opacity: .58; cursor: default; }
```

三种状态互斥且可叠加（`.done.today`）。`today` 用 2px 边框——这是全局唯一允许的 2px 边框。

**为什么是 `<button>` 而不是 `<div>`**

原来用的是 `<div>`，键盘用户完全够不到这 49 格（WCAG 2.1.1）。但反过来，
49 个都当作 tab 停靠点又太多——按 49 次 Tab 才能走出这个网格是另一种不可用。折中：

- 标签统一用 `<button type="button">`，**但不进 tab 顺序的格子用 `disabled`**
  （`disabled` 的元素仍会被读屏读到，只是跳过）
- 只有「有内容的过去」和「今天」可聚焦，其余 disabled → 实测 2 个停靠点而不是 49 个
- 每格必须有 `aria-label`，把状态说全：

```
第 1 天，已写：今天的活一件件推进了，我很安心。
第 2 天（今天）
第 8 天，还没到
```

**读屏读不出"颜色深浅"**，所以已写 / 今天 / 未来三种状态必须落到文字或 `disabled` 上，
不能只靠底色和透明度。

`.cell.future` 的 `opacity` 从 `.42` 调到 `.58`：禁用态虽然不受对比度约束，
但没必要虚到看不清数字——用户需要知道"还有几天"。


### Modals / Dialogs

本系统**不使用模态弹窗**。所有确认走浏览器原生 `confirm()` 与 toast。理由：模态会打断"每天三分钟"的连续感，且需要额外的遮罩层与动画，与"一本纸"的隐喻冲突。

toast 规范：

```css
.toast {
  position: fixed; left: 50%; bottom: calc(84px + env(safe-area-inset-bottom));
  transform: translateX(-50%);
  background: var(--color-ink); color: var(--color-paper);
  font-size: 13px; padding: 9px 18px; border-radius: 999px;
  opacity: 0; transition: opacity .25s; z-index: 60;
}
.toast.on { opacity: .94; }
```

toast 是**唯一的反馈通道**（本系统不用模态），所以它必须是 live region，
否则读屏用户永远不知道刚才那一下成功了没有：

```html
<div class="toast" id="toast" role="status" aria-live="polite"></div>
```

- `role="status"` + `aria-live="polite"`：礼貌播报，不打断用户当前操作
- **不要用 `aria-live="assertive"`**。手账没有"必须立刻知道"的错误，打断反而烦
- 文案写**结果**，不写命令。✅「已自动存好，想改随时改」 ❌「请点击保存」


### 同步卡片与登录表单

同步是**可选**功能，视觉上必须**低于主线内容**——不能让它看起来像必填项。

```css
.card.sync { background: var(--color-paper-sunken); border-style: dashed; }
.sync .tabs { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 14px; }
.sync .tabs > * {
  font-size: 12.5px; padding: 5px 11px; border-radius: 999px;
  border: 1px solid var(--color-line); background: var(--color-card);
  color: var(--color-ink-secondary); cursor: pointer;
}
.sync .tabs > .on {
  background: var(--color-accent); border-color: var(--color-accent);
  color: var(--color-card);
}
.sync input { font-size: 16px; }   /* 同输入框规范：16px 防 iOS 缩放 */
```

| 状态 | 谁渲染 | 主文案（不要改语气） |
|---|---|---|
| 未填配置串 | `renderSyncCard()` | 「可选功能：登录后可以把这本日记在多台设备之间同步。」 |
| `file://` 打开 | `renderSyncCard()` | 「当前是从本地文件打开的，联网同步要在发布后的网址上用。」 |
| 已填配置、未登录 | `authHTML()` | 四个 tab：密码登录 / 验证码登录 / 注册 / 忘记密码 |
| 已登录、未设同步密码 | `renderSyncCard()` | 「已登录。现在设一个**同步密码**——它只用来加密这本日记，不会上传。」 |
| 已连接 | `renderSyncCard()` | 「已连接，本机加密。上次同步：{时间}」 |
| 还没开始这一轮（新设备） | `renderSettings()` | 从落地页的「去开启同步」进来。此时底部 tab 栏不出现（`tabbar.hidden = !S`），所以设置页顶部给「← 回到开始这一页」；备份 / 打印 / 这一轮三张卡片整张隐藏 |

文案硬规则：

- **同步密码必须解释「丢了会怎样」**：固定一句「密码丢了，云端那份就解不开了，本机的记录不受影响。」
- 不写「注册账号」「开启云同步」这类命令式措辞——用户不点头就不该出现
- 「忘了密码」tab 重设成功后**直接进主界面**（SDK 会自动登录），不要求用户再用新密码登一次
- 注册时若邮箱已存在，**不给「这个邮箱已经注册过」**，只说「请用密码登录。」——不暴露账号是否存在

---

## 5. Layout Principles

### Spacing System

基数 **4px**。允许值：`4 / 6 / 8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 28 / 32 / 48`（px）。

| 用途 | 值 |
|---|---|
| 卡片之间 | 16px |
| 卡片内 padding | 20px（紧凑态 16px 18px） |
| 标签到内容 | 12px |
| 行内元素间距 | 8px |
| 段落间距 | 10px |
| 页面左右留白 | 16px |

### Container

```css
.wrap { max-width: 520px; margin: 0 auto; padding: 0 16px 112px; }
```

- `max-width: 520px` — 手账是单页纸，宽屏不铺开。超出后居中留白，不改变字号。
- `padding-bottom: 112px` — 为固定底栏（约 56px）+ safe-area 预留，避免最后一张卡片被遮住。

### Grid System

单列流式。唯一的网格是 49 格轨道的 `repeat(7, 1fr)`。**不使用多列卡片栅格**——除统计区 `repeat(3, 1fr)`。

### 留白哲学

**卡片内松、卡片间也松，但页面边缘紧。** 具体：页边 16px（紧），卡片之间 16px，卡片内 20px（松）。

理由是模仿真实笔记本：纸的边界就是页面边界，所以页边要窄；而笔记本里的每一页是完整的一块，所以块与块之间要呼吸。页边若给到 24px 以上，会失去"一整张纸"的连续感。

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-paper: none;
--shadow-xs:  0 1px 2px rgba(64,52,34,.05), 0 1px 1px rgba(64,52,34,.04);
--shadow-sm:  0 2px 4px rgba(64,52,34,.06), 0 1px 2px rgba(64,52,34,.04);
--shadow-md:  0 4px 14px rgba(64,52,34,.08), 0 1px 3px rgba(64,52,34,.05);
--shadow-lg:  0 10px 28px rgba(64,52,34,.10), 0 2px 6px rgba(64,52,34,.06);
--shadow-xl:  0 18px 48px rgba(64,52,34,.12), 0 4px 10px rgba(64,52,34,.06);
--shadow-2xl: 0 32px 72px rgba(64,52,34,.16), 0 8px 18px rgba(64,52,34,.08);
```

默认卡片用 `--shadow-xs`。纸质媒介的层叠感极弱——**阴影不是用来表达高度的，是用来表达"这张纸压在下面那张上"的**。所以宁可更淡。

### Surface Layers

| 层 | 变量 | 值 | 用途 |
|---|---|---|---|
| 0 底 | `--color-paper` | `#FBF7EF` | body |
| 1 沉 | `--color-paper-sunken` | `#F6F1E5` | 输入框、未完成格、chip |
| 2 面 | `--color-card` | `#FFFDF8` | 卡片 |
| 3 浮 | `rgba(251,247,239,.94)` + blur | — | 底部标签条 |
| 4 覆 | `--color-ink` | `#2B2925` | toast（反色浮层） |

**层与层之间明度差极小（L* 差值 < 4%）。** 这是刻意的：纸张叠在一起不会有强烈明暗差，靠 1px 边框和微阴影区分。

### Z-index Scale

| 值 | 用途 |
|---|---|
| 0 | 默认流 |
| 10 | 描摹画布覆盖层 |
| 20 | 底部标签条 |
| 60 | toast |

**不使用 100 以上。** 全站只有 4 个层级。

### Backdrop Effects

```css
backdrop-filter: saturate(180%) blur(12px);
```

仅用于底部标签条。参数固定 `saturate(180%) blur(12px)`——饱和度必须带上，否则纸色在模糊后会发灰。

---

## 7. Do's and Don'ts

### Do's

1. **纸色打底，纯白只用来做"卡片"这一层的提亮。** 卡片的 `#FFFDF8` 与纸底 `#FBF7EF` 的差值就是全部的"层次感"。
2. **书写区行高与横线周期严格对齐**（`line-height` = 横线 `repeating-linear-gradient` 周期）。
3. **输入框字号锁 16px**，避免 iOS 自动缩放。
4. **衬线承载内容，无衬线承载界面**。按钮和标签绝不用衬线。
5. **每屏最多一个 primary 按钮**。赤陶是印章，不是装饰。
6. **49 格用三种状态说清所有事**：已写（苔绿）/ 今天（赤陶 2px 边）/ 未来（58% 不透明 + `disabled`）。不额外加图标。
7. **过渡统一 150ms**（背景/边框），250ms 上限（透明度）。手账不该"弹"。
8. **所有内容默认只存本地**，涉及数据安全的操作（导出/重置）必须给明文说明。

### Don'ts

1. **不用纯白 `#FFFFFF` 做页面背景** — 立刻变成界面。
2. **不用 600 / 700 字重** — 会破坏纸面书写的轻。
3. **不用黑色阴影** — `rgba(0,0,0,…)` 让卡片像 UI 浮层。必须用暖褐 `rgba(64,52,34,…)`。
4. **不用渐变、发光、玻璃拟态**（底部标签条除外）。
5. **不用图标库、插画、emoji 做装饰** — 手账上的图形应该是用户自己画的。
6. **不用模态弹窗** — 打断连续性，走 toast + 原生 confirm。
7. **不做超过 300ms 的动效**，不做弹跳/回弹曲线。
8. **不在同屏出现两个强调色** — 赤陶和苔绿可以共存（不同语义），但不要引入第三个彩色。

---

## 8. Responsive Behavior

### Breakpoints

| 名称 | 范围 | 行为 |
|---|---|---|
| Mobile S | 320–374px | 单列，页边 16px，49 格 gap 4px |
| Mobile L | 375–519px | 单列，页边 16px，49 格 gap 6px（默认） |
| Tablet | 520–767px | 容器锁 520px 居中，两侧留白，字号不变 |
| Desktop | 768px+ | 容器锁 520px 居中，页面上下加 32px 呼吸空间，字号不变 |

**字号在任何断点都不缩放。** 手账是固定尺寸的纸，放大等于换了张纸。

### Touch Targets（含键盘）

- 最小点击目标 **24×24 CSS px**（WCAG 2.2 SC 2.5.8 硬门槛），舒适区 **44×44px**（iOS HIG）。
- `.cell` 用 `aspect-ratio: 1` 自动撑满，520px 容器下每格约 68px；320px 下约 38px。
- `.tab` 高度锁 `min-height: 48px` + safe-area。
- `.btn.small` 视觉高 33px（`padding: 9px 13px`），配合父容器间距达到 44px 命中区。
- `.wish-del`（删除愿望）加了 `min-width/min-height: 44px` —— 它原来只有 19px 高，
  是全站唯一明确不达标的触控目标。

**键盘可达（WCAG 2.1.1）**

- 所有可操作元素用 `<button>` / `<input>`，**不用 `<div onclick>`**
- 可聚焦的元素必须能进 tab 顺序（`tabIndex >= 0`），除非用 `disabled` 明确排除
- 焦点必须可见 —— 见第 4 节的 `:focus-visible`
- **纯指针操作要有键盘等价路径**：描摹区只能用笔 → 必须提供「照着打一遍」
- 49 格原来全是用 `<div>` 做的，键盘一个都够不到；现在只有 2 个停靠点，其余 `disabled`

**子区块的组合语义**

- 愿望列表容器 `role="group"` + `aria-labelledby`
- 进度条容器 `role="progressbar"` + `aria-valuenow/min/max`
- 装饰性图形（`.dot` 之类）加 `aria-hidden="true"`，避免读屏念出无意义的字符

### 折叠策略

| 元素 | 折叠方式 |
|---|---|
| 卡片 | **不折叠**。所有卡片始终可见，垂直滚动。**例外**：设置页里依赖「已经有一轮」的三张卡（备份 / 打印 / 这一轮）在还没开始时整张 `hidden` —— 那不是折叠，是空状态：它们要显示的数据此刻不存在。 |
| 49 格 | **不折叠**。7×7 是这套方法的核心视觉，必须完整呈现。 |
| 长文字 | 输入框 `resize: vertical`，默认 4 行高（128px）。 |
| 统计区 | `repeat(3, 1fr)` 在 320px 下仍保持 3 列（每列约 90px）。 |

### Font Scaling

- 尊重系统字号设置（不使用 `-webkit-text-size-adjust: none`）。
- 设置 `-webkit-text-size-adjust: 100%` 防止横屏时被放大。
- 描摹画布内的字号**不随系统缩放**——它被绘制进 canvas，尺寸由 `wrapText()` 按容器宽度计算。

### Safe Area

```css
padding-bottom: env(safe-area-inset-bottom);   /* 底部标签条 */
padding: 0 16px 112px;                          /* 内容区 */
```

iOS 全面屏必须处理，否则底部会压到 Home Indicator。

### Reduced Motion（不可省）

前庭功能障碍的用户会因为过渡和动画不适。系统级偏好必须被尊重：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: .01ms !important;
    animation-duration: .01ms !important;
  }
}
```

用 `.01ms` 而不是 `0s`：有些浏览器会跳过 0s 的 transition，
导致依赖 `transitionend` 的逻辑不触发。`!important` 在这里是正当的——
它是用户级偏好，优先级应当高于任何组件样式。

### 动效规范

- 只动画 `transform` 与 `opacity`（GPU 合成，不触发重排）
- 时长：背景/边框 **150ms**，透明度 **250ms**，**上限 300ms**
- 按压反馈用 `transform: scale(.97)`，不用改宽高（会重排）
- **不要**弹跳 / 回弹曲线。手账不该有弹性

---

## 9. Agent Prompt Guide

### Quick Reference

```
色板:  纸 #FBF7EF / 沉 #F6F1E5 / 卡 #FFFDF8 / 线 #E7E0CF
墨:    #2B2925 / #5C574E / #746D60 / 描摹灰 #ABA492
强调:  赤陶 #AD5534 (hover #8F4425, soft #FAEFE8)
语义:  完成 #48704D (soft #E8F0E6)
字体:  内容 Songti SC/STSong/Georgia; 界面 PingFang SC/system-ui
字重:  只有 400 和 500
圆角:  10px 控件 / 16px 卡片 / 999px 徽标
阴影:  0 1px 2px rgba(64,52,34,.05), 0 1px 1px rgba(64,52,34,.04)
容器:  max-width 520px, 页边 16px
间距:  4px 基数, 卡片间 16px, 卡片内 20px
过渡:  150ms（透明度 250ms，上限 300ms）
对比:  正文 ≥4.5:1 / UI ≥3:1（描摹灰是唯一豁免，2.20:1）
焦点:  :focus-visible 2px 赤陶描边 + 2px offset，永不 outline:none
可达:  可点元素用 <button>；输入框必须有 label 或 aria-labelledby；
       状态不能只靠颜色（aria-pressed / aria-current / disabled / 文字）
禁用:  纯白背景 / 600+字重 / 黑阴影 / 渐变 / 图标库 / 模态弹窗 / outline:none
```


### Component Prompts

> 以下 prompt 可直接粘贴给 AI 编程代理。每个都假设代理已读到本文档。

**1. 新增一个内容卡片**

```
按 DESIGN.md 的 Card 规范，做一个"每周主题"卡片：显示周序号（衬线 13px 赤陶）、
主题名（衬线 17px 主墨）、一句 focus 说明（无衬线 12px 弱墨）。
背景 --color-card，边框 1px --color-line，圆角 16px，padding 20px，
阴影用 --shadow-xs。不要加图标。
```

**2. 新增一个状态标签**

```
按 DESIGN.md 的 Chips 规范做一组可多选的标签。未选中：背景 --color-paper-sunken，
边框 1px --color-line，文字 --color-ink-secondary。选中：背景与边框均为 --color-accent，
文字白色。圆角 999px，padding 7px 15px，字号 13.5px。过渡 150ms。
```

**3. 做一个进度指示**

```
按 DESIGN.md 做一个线性进度条：轨道高 3px，背景 --color-line，圆角 2px；
填充高 3px，背景 --color-accent，圆角 2px，宽度随进度变化，过渡 400ms ease。
不要加百分比数字，数字放卡片右上角的 pill 里。
容器加 role="progressbar" 与 aria-valuenow / aria-valuemin / aria-valuemax，
否则读屏读到的是「一组没有语义的 div」。
```

**4. 做一个数据网格**

```
用 7 列网格展示 49 个格子（gap 6px），每格 aspect-ratio 1、圆角 8px、
边框 1px --color-line、背景 --color-paper-sunken、衬线 11.5px 弱墨（--color-ink-tertiary）。
三种状态：已完成（背景 --color-success-soft，边框 --color-success-line，字色 --color-success）、
今天（2px --color-accent 边框，字色 --color-accent，字重 500）、未来（opacity .58）。
每格必须是 <button type="button"> 并带 aria-label 说明「第几天 + 状态」；
不可点的格子用 disabled（不要只是长得像按钮）。
```

**5. 做一张可打印的手账页**

```
按 DESIGN.md 做 A5 打印版手账页。@media print 下隐藏所有按钮、导航、提示文字；
body 背景改纯白（打印不需要纸色）；卡片去掉阴影、边框改 #ddd、break-inside: avoid；
每页容纳一天：日期（衬线 22px）+ 描摹句（衬线 20px）+ 8 行横线书写区
+ 情绪词行。页脚右下角放页码。
注意：屏幕上的描摹灰（#ABA492，2.20:1）是为「盖着描」刻意留淡的，
印到纸上要加深到 --color-ink-secondary，否则印出来读不了。
```

**6. 加一个 toast 提示**

```
按 DESIGN.md 的 toast 规范：固定定位在底部标签条上方 84px + safe-area，
水平居中，背景 --color-ink，文字 --color-paper，字号 13px，圆角 999px，
padding 9px 18px，opacity 从 0 到 .94 过渡 250ms，2200ms 后自动消失。
不要用模态弹窗。
```

### Iteration Guide

1. **先改色，后改布局。** 这套系统的性格 80% 在纸色和墨色的对比度上。如果页面"不像纸"，先检查是不是混进了纯白。
2. **任何新增元素先问：它在纸上对应什么？** 答不出来就不该有。
3. **不要为了"信息更全"加图形。** 这套系统的克制是特性不是缺陷。
4. **衬线/无衬线的分配错了，整个页面会散。** 内容 = 衬线，界面 = 无衬线，没有例外。
5. **检查阴影颜色。** 出现 `rgba(0,0,0,…)` 一律改成 `rgba(64,52,34,…)`。
6. **检查字重。** 出现 600/700 一律降回 400 或 500。
7. **输入框字号必须是 16px。** 在 iOS 上实测过才能改。
8. **描摹画布的坐标必须归一化存储**（0–1 区间），否则换设备后笔迹会错位。
9. **动效保持"慢半拍"。** 手账不该有弹性曲线和快速反馈，150ms 是最快的。
10. **改完在手机上横竖屏各看一次。** 桌面浏览器看不出这个系统的问题。
11. **改了任何颜色，重算第 2 节的对比度表。** 眼睛判断"够不够深"极不可靠——
    实测过 `#918A7B` 看着"只是稍浅的灰"，实际只有 3.04:1。
12. **状态不能只靠颜色。** 新增任何"选中 / 完成 / 禁用"的视觉差异时，同时给出
    语义出口：`aria-pressed` / `aria-current` / `disabled` / 文字说明。
13. **别写 `outline: none`。** 要去默认样式就同时给自定义焦点环。
14. **能力探测要在动 DOM 之前做。** 拿到 `null` 就退回可用路径并给一句人话，
    不要留一个"点了没反应"的按钮。

---

## 附 A：无障碍基线（WCAG 2.2 AA）

这套系统承诺的最小集。**每次改动后逐条过一遍**，不要凭印象。

### 感知

- [ ] 正文 / 小字（< 18.66px 粗或 < 24px）对比度 **≥ 4.5:1**
- [ ] 大字与 UI 组件（边框、图标、焦点环）对比度 **≥ 3:1**
- [ ] **唯一豁免**：`.trace-static` / `.type-target` 的描摹灰（2.20:1）——
      它是"盖着描"的底稿，且已有等价路径（打字模式 / 打印版加深），见第 2 节
- [ ] 不靠单一颜色传达信息（已写 / 今天 / 未来三种状态都有文字或 `disabled` 兜底）
- [ ] 页面放大到 200% 不丢内容（容器 `max-width: 520px`，字号不随断点缩放）
- [ ] 文本不被图片/图形截断

### 可操作

- [ ] 所有功能**纯键盘可完成**（Tab 走到、Enter/Space 触发）
- [ ] 焦点始终可见（`:focus-visible`，2px 描边 + 2px offset）
- [ ] 焦点顺序与视觉顺序一致（DOM 顺序 = 阅读顺序，不用 `tabindex` 正数）
- [ ] 触控目标 ≥ **24×24 CSS px**（SC 2.5.8）
- [ ] 49 格网格的 tab 停靠点数量合理（实测 2 个，不是 49 个）
- [ ] 指针独占的操作（描摹）有键盘等价路径（照着打一遍）
- [ ] 系统 `prefers-reduced-motion` 被尊重

### 可理解

- [ ] 输入框都有可访问名（`label[for]` 或 `aria-labelledby`）
- [ ] 标题层级正确（`h1` → `h2`，不跳级）
- [ ] 状态变化有播报（toast 用 `role="status"` + `aria-live="polite"`）
- [ ] 错误提示说明**怎么修**，不只说"出错了"（如「密码至少 8 位」）
- [ ] 不用命令式措辞催用户（「请立即开启同步」这类一律不写）

### 健壮

- [ ] 浏览器能力缺失时有降级路径 + 人话提示（如 `getContext('2d')` 返回 `null`）
- [ ] 表单控件有正确的 `type` / `inputmode` / `autocomplete`
       （邮箱 `autocomplete="email"`，验证码 `inputmode="numeric"`）
- [ ] 用语义化 HTML 优先，`role` 只用于补语义（不要给 `<button>` 再加 `role="button"`）
- [ ] 装饰性元素加 `aria-hidden="true"`

### 三个最容易做错的地方

1. **`placeholder` 当标签用** —— 一输入就消失，读屏在填写过程中读不到。
2. **只用颜色表示选中** —— 视觉用户看得懂，读屏用户听到的是"感恩 按钮"，不知道选没选。
3. **能力探测失败时静默失败** —— 点了没反应是最差的结果，比报错还差。
   必须给替代路径 + 一句可读的说明。

### 回归测试

`scripts/test-journal.js` 覆盖了上面的大部分条目（键盘可达、aria 属性、
降级路径、数据不丢）。**这是仓库内的维护者工具，不随 ClawHub 发布包分发**，
而且在 ClawHub 包里不该出现——它会引用一个包里不存在的文件。改页面后跑：

```bash
NODE_PATH=<node 工作区>/node_modules node scripts/test-journal.js
```

退出码 `0` 才算通过。

---

## 附 B：不适用场景

这套设计系统服务于"低信息密度、高仪式感、手机优先的单页书写工具"。
以下场景不要套用：数据密集的仪表盘、多人协作界面、需要强反馈的游戏类交互、
暗色模式优先的产品。

