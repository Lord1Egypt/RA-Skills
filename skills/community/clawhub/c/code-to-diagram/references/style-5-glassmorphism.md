# Style 5: Glassmorphism

毛玻璃卡片 + 暗色渐变背景。适合产品展示、发布会 keynote、营销页面。

---

## 颜色系统

### 背景

对角线性渐变，三段色：

| 位置 | 色值 |
|------|------|
| 0% | `#0d1117` |
| 50% | `#161b22` |
| 100% | `#0d1117` |

### 毛玻璃卡片

| 属性 | 值 |
|------|-----|
| 填充 | `rgba(255,255,255,0.06)` |
| 描边 | `rgba(255,255,255,0.15)` |
| 描边宽度 | 1px |
| 圆角 | 12px |
| 顶部高光线 | `rgba(255,255,255,0.25)` 1px |

### 文字

| 用途 | 色值 |
|------|------|
| 主文字 | `#f0f6fc` |
| 副文字 | `#8b949e` |
| 英雄标签 | 渐变文字（见下方模板） |

### 强调发光色

| 名称 | 色值 | RGBA (0.3 alpha) |
|------|------|-------------------|
| 蓝色 | `#58a6ff` | `rgba(88,166,255,0.3)` |
| 紫色 | `#bc8cff` | `rgba(188,140,255,0.3)` |
| 绿色 | `#3fb950` | `rgba(63,185,80,0.3)` |
| 橙色 | `#f78166` | `rgba(247,129,102,0.3)` |

---

## 字体

```
font-family: 'Inter', -apple-system, 'SF Pro Display', 'PingFang SC',
             'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
```

| 用途 | 大小 | 字重 |
|------|------|------|
| 副标签 | 12px | 400 |
| 标签 | 14px | 600 |
| 英雄标题 | 20px | 700 |

---

## 背景层

```xml
<defs>
  <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0d1117"/>
    <stop offset="50%" stop-color="#161b22"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <radialGradient id="glow-blue" cx="30%" cy="40%" r="40%">
    <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="#58a6ff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow-purple" cx="70%" cy="60%" r="35%">
    <stop offset="0%" stop-color="#bc8cff" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="#bc8cff" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="960" height="600" fill="url(#bg)"/>
<rect width="960" height="600" fill="url(#glow-blue)"/>
<rect width="960" height="600" fill="url(#glow-purple)"/>
```

---

## 毛玻璃卡片构造

SVG 无法实现真正的 backdrop-filter，通过三层叠加模拟：

```xml
<!-- 层 1: 微弱内阴影 -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"
      fill="rgba(255,255,255,0.03)" stroke="none"/>
<!-- 层 2: 毛玻璃主体 -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
<!-- 层 3: 顶部高光线 -->
<line x1="{x+12}" y1="{y+0.5}" x2="{x+w-12}" y2="{y+0.5}"
      stroke="rgba(255,255,255,0.25)" stroke-width="1"/>
```

---

## 渐变文字（英雄标签）

```xml
<defs>
  <linearGradient id="text-grad-blue" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#58a6ff"/>
    <stop offset="100%" stop-color="#bc8cff"/>
  </linearGradient>
</defs>
<text fill="url(#text-grad-blue)" font-weight="700" font-size="20">
  AI Pipeline
</text>
```

---

## 箭头标记

```xml
<defs>
  <marker id="arrow-blue" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#58a6ff"/>
  </marker>
  <marker id="arrow-purple" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#bc8cff"/>
  </marker>
  <marker id="arrow-green" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#3fb950"/>
  </marker>
</defs>
```

连线使用半透明发光描边：

```xml
<path d="M 100,50 L 300,50" stroke="#58a6ff" stroke-width="1.5"
      fill="none" opacity="0.8" marker-end="url(#arrow-blue)"/>
```

---

## 完整 SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600">
  <style>
    text {
      font-family: 'Inter', -apple-system, 'SF Pro Display', 'PingFang SC',
                   'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
      fill: #f0f6fc;
    }
  </style>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <radialGradient id="glow-blue" cx="30%" cy="40%" r="40%">
      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#58a6ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow-purple" cx="70%" cy="60%" r="35%">
      <stop offset="0%" stop-color="#bc8cff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#bc8cff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="text-grad-blue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58a6ff"/>
      <stop offset="100%" stop-color="#bc8cff"/>
    </linearGradient>
    <marker id="arrow-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#58a6ff"/>
    </marker>
    <marker id="arrow-purple" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#bc8cff"/>
    </marker>
    <marker id="arrow-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#3fb950"/>
    </marker>
  </defs>

  <!-- 背景层 -->
  <rect width="960" height="600" fill="url(#bg)"/>
  <rect width="960" height="600" fill="url(#glow-blue)"/>
  <rect width="960" height="600" fill="url(#glow-purple)"/>

  <!-- 在此放置毛玻璃卡片、连线 -->
</svg>
```

---

## 重要规则

- **不要使用 `@import url()`**——rsvg-convert 无法获取外部资源，不能引入 Google Fonts
- 所有字体必须通过内联 `<style>` 声明，Inter 字体回退到 system-ui
- 文字标签必须使用中文
- 毛玻璃效果通过多层半透明 rect 叠加实现，不依赖 backdrop-filter
