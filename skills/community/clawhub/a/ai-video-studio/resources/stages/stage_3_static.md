# Stage 3：静态排版构建与验收

### 3.1 创建项目目录

```bash
mkdir -p YYYYMMDD/assets
# 初始化 index.html（手动创建，参考下方 HTML 模板）
```

### 3.2 HTML 基础模板 — 模式 A（强制规范）

> ℹ️ 以下为模式 A（纯图片）的 HTML/CSS 规范。模式 B 请跳转至 §3.2B。
> 完整参考实现见 `template/index.html` 和 `template/style.css`。以下仅列出关键约束。

**根容器必须包含 4 个 data-* 属性（缺一不可）：**
```html
<div id="composition"
     data-composition-id="composition"
     data-width="1920"
     data-height="1080"
     data-duration="{Stage 2.1 获取的音频总时长}">
```

**场景 DOM 结构（由 JS 动态生成，严禁硬编码）：**
```
scene.clip
  ├─ img.bg-fill    ← 背景模糊层（object-fit: cover + blur）
  ├─ img.fg-main    ← 主体图片层
  └─ div.overlay
       └─ div.subtitle  ← 字幕（通过 textContent 写入）
```

**GSAP 铁律：**
```js
const tl = gsap.timeline({ paused: true }); // 永远 paused: true
window.__timelines = window.__timelines || {};
window.__timelines["composition"] = tl; // key 必须与 data-composition-id 一致
```

**图片引用规范：**
- 使用 `assets/${id}.png`（如 `assets/scene1.png`），与 scene 数据的 id 字段一致

### 3.3 CSS 布局规范 — 模式 A（强制）

> ℹ️ 完整实现见 `template/style.css`。以下仅列出核心规则。

**`object-fit` 决策树（根据图片画幅选择）：**

| 图片画幅 | fg-main | bg-fill | 效果 |
|---------|---------|---------|------|
| 16:9 横版（推荐） | `object-fit: cover` | 不需要 | 完美填充，无黑边 |
| 非标画幅（正方形等） | `object-fit: contain` | 需要（blur + cover） | 毛玻璃背景填充黑边 |

```css
/* 背景模糊层（非 16:9 素材时使用） */
.bg-fill {
  position: absolute; inset: 0;
  object-fit: cover;
  filter: blur(20px) brightness(0.4);
  transform: scale(1.1); /* 补偿 blur 边缘虚化 */
}

/* 主体图片层：严禁使用 translate 居中 */
.fg-main {
  position: absolute; inset: 0;
  object-fit: contain; /* 或 cover，见上方决策树 */
  transform-origin: center center;
}
```

### 3.2B HTML 基础模板 — 模式 B（视频 + 文字叠加）

> ℹ️ 以下为模式 B 的 HTML/CSS 规范。参考实现见 `20260518_org_slowdown/index.html` 和 `style.css`。

**根容器（竖屏画幅）：**
```html
<div id="composition"
     data-composition-id="composition"
     data-width="1080"
     data-height="1920"
     data-start="0"
     data-duration="{音频总长}">
```

**⚠️ 视频标签扁平化铁律（最重要的规则）：**

`<video>` 标签**必须**是 `#composition` 的**直接子元素**。严禁将 `<video data-start="...">` 嵌套在任何带有 `data-start` 的 `<div>` 内部，否则 HyperFrames 渲染器无法管理视频播放，**视频将冻结在第一帧**。

```html
<!-- ✅ 正确：视频作为舞台的扁平直接子元素 -->
<video id="v-scene1" class="clip bg-video" src="assets/scene1.mp4" muted playsinline
       data-start="0" data-duration="8" data-track-index="3"></video>
<video id="v-scene2" class="clip bg-video" src="assets/scene2.mp4" muted playsinline
       data-start="8" data-duration="10" data-track-index="3"></video>

<!-- 文字叠加层：独立的场景 div，不含 <video> -->
<div id="scene1" class="clip"
     data-start="0" data-duration="8" data-track-index="1"
     style="z-index: 1;">
  <div class="dim-overlay"></div>
  <div class="bottom-gradient"></div>
  <div class="text-layer text-layer--bottom">
    <div id="s1-line1" class="body-text">旁白文本</div>
    <div id="s1-line2" class="headline">冲击<span class="accent">金句</span>。</div>
  </div>
</div>
```

```html
<!-- ❌ 错误：视频嵌套在带 data-start 的 div 内 → 渲染冻结 -->
<div id="scene1" class="clip" data-start="0" data-duration="8">
  <video class="bg-video" src="assets/scene1.mp4" data-start="0" ...></video>
</div>
```

**视频标签必备属性清单：**

| 属性 | 说明 |
|------|------|
| `id` | 唯一标识，如 `v-scene1`（缺少则渲染冻结） |
| `class="clip bg-video"` | `clip` 让框架管理可见性，`bg-video` 应用视频样式 |
| `muted playsinline` | HyperFrames 接管播放，严禁加 `autoplay` 或 `loop` |
| `data-start` | 视频在时间轴上的起始秒数 |
| `data-duration` | 视频播放时长 |
| `data-track-index` | 设为 `3`（与音频轨 0、场景轨 1/2 错开） |

**全局装饰层（模式 B 推荐）：**
```html
<div class="vignette"></div>      <!-- 暗角 -->
<div class="noise-overlay"></div>  <!-- 胶片噪点 -->
```

### 3.3B CSS 规范 — 模式 B（文字叠加排版）

**核心 CSS 铁律：**
```css
.bg-video {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  opacity: 1; /* 👈 必须！覆盖 .clip 的默认 opacity: 0 */
}

.dim-overlay {
  position: absolute; inset: 0;
  background: rgba(0, 0, 0, 0.55); /* 确保文字可读 */
}

.bottom-gradient {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 600px;
  background: linear-gradient(to top, rgba(10,10,10,0.95) 0%, transparent 100%);
  z-index: 1;
}
```

**文字叠加组件库：**

| 组件 | CSS 类 | 用途 |
|------|--------|------|
| 大标题金句 | `.headline` | 核心冲击句 |
| 超大数字 | `.headline--huge` | 数据对比 |
| 正文旁白 | `.body-text` | 常规叙述 |
| 小字说明 | `.caption-text` | 补充信息 |
| 强调色 | `.accent` | 关键词高亮 |
| 不等号卡 | `.neq` + `.text-card` | 「A ≠ B」对比卡片 |
| 分屏对比 | `.split-compare` | 错误 vs 正确对比 |

**文字定位方式：**
- `.text-layer--bottom`：底部三分之一（大多数叙述场景）
- `.text-layer--center`：垂直居中（金句升华、数字冲击）

### 3.4 静态验收（加入动画前的检查）

用浏览器打开 `index.html`，截图确认：

模式 A：
- [ ] 每张图片完整显示，无裁切，无偏移
- [ ] 图片在 1920×1080 的黑色背景内居中

模式 B：
- [ ] 视频背景可见（非黑屏），文字叠加清晰可读
- [ ] `dim-overlay` 暗化效果适当（文字不被视频干扰）
- [ ] 全屏文字卡（如「A ≠ B」）显示正确

**✅ Stage 3 退出标准：**
- [ ] 纯静态下所有视觉素材（图片或视频）100% 正确显示
- [ ] `data-composition-id`、`data-width`、`data-height` 已正确设置
- [ ] 模式 A：字幕通过 `textContent` 注入；模式 B：文字叠加 DOM 结构完整
- [ ] `npx hyperframes lint .` 报 **0 error(s)**
