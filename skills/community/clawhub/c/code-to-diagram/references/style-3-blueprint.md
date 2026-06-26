# Style 3: Blueprint

工程蓝图风格。深蓝底色 + 网格线 + 青色描边，适合正式架构文档和 RFC。

---

## 颜色系统

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景 | `#0a1628` | 深蓝 |
| 网格线 | `#112240` | 微弱网格 |
| 面板填充 | `#0d1f3c` | 暗蓝 |
| 面板描边 | `#00b4d8` | 青色 |
| 主文字 | `#caf0f8` | 浅青 |
| 副文字 | `#90e0ef` | 中青 |
| 标签文字 | `#00b4d8` | 青色 |
| 弱文字 | `#48cae4` | 淡青（60% 不透明） |

### 强调色

| 名称 | 色值 | 用途 |
|------|------|------|
| 青色 | `#00b4d8` / `#48cae4` | 主色调 |
| 白色 | `#ffffff` | 关键标签 |
| 橙色 | `#f77f00` | 警告/告警 |
| 绿色 | `#06d6a0` | 成功/活跃 |

---

## 字体

```
font-family: 'Courier New', 'Lucida Console', 'Microsoft YaHei', 'SimHei', monospace;
```

| 用途 | 大小 | 字重 |
|------|------|------|
| 注释 | 10px | 400 |
| 标签 | 13px | 400 |
| 标题 | 16px | 700 |
| 字距 | `letter-spacing: 0.05em` | — |
| 分区标题 | 大写 + `text-transform: uppercase` | 700 |

---

## 网格背景

```xml
<defs>
  <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#112240" stroke-width="0.5"/>
  </pattern>
</defs>
<rect width="960" height="600" fill="#0a1628"/>
<rect width="960" height="600" fill="url(#grid)" opacity="0.6"/>
```

---

## 节点样式

### 标准技术节点

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" ry="2"
      fill="#0d1f3c" stroke="#00b4d8" stroke-width="1"/>
```

### 虚线框（外部/可选组件）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" ry="2"
      fill="none" stroke="#00b4d8" stroke-width="1" stroke-dasharray="6,3"/>
```

### 角括号风格（备选）

用四个 L 型角落替代完整边框，更具工程图纸感。

---

## 箭头标记

```xml
<defs>
  <marker id="arrow-cyan" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#00b4d8"/>
  </marker>
  <marker id="arrow-orange" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#f77f00"/>
  </marker>
  <marker id="arrow-green" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#06d6a0"/>
  </marker>
</defs>
```

连线使用正交折线（polyline），保持工程图纸感：

```xml
<polyline points="100,50 200,50 200,150 300,150"
          fill="none" stroke="#00b4d8" stroke-width="1.5"
          marker-end="url(#arrow-cyan)"/>
```

---

## 右下角标题栏

```xml
<g transform="translate(700, 530)">
  <rect width="240" height="60" fill="none" stroke="#00b4d8" stroke-width="1"/>
  <line x1="0" y1="15" x2="240" y2="15" stroke="#00b4d8" stroke-width="0.5"/>
  <text x="120" y="12" text-anchor="middle" fill="#caf0f8" font-size="10">ARCHITECTURE DIAGRAM</text>
  <text x="120" y="40" text-anchor="middle" fill="#00b4d8" font-size="13" font-weight="700">{图表标题}</text>
</g>
```

---

## 完整 SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600">
  <style>
    text {
      font-family: 'Courier New', 'Lucida Console', 'Microsoft YaHei', 'SimHei', monospace;
      fill: #caf0f8;
    }
  </style>
  <defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#112240" stroke-width="0.5"/>
    </pattern>
    <marker id="arrow-cyan" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#00b4d8"/>
    </marker>
    <marker id="arrow-orange" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#f77f00"/>
    </marker>
    <marker id="arrow-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#06d6a0"/>
    </marker>
  </defs>

  <!-- 蓝图背景 + 网格 -->
  <rect width="960" height="600" fill="#0a1628"/>
  <rect width="960" height="600" fill="url(#grid)" opacity="0.6"/>

  <!-- 在此放置节点、连线 -->

  <!-- 右下角标题栏 -->
  <g transform="translate(700, 530)">
    <rect width="240" height="60" fill="none" stroke="#00b4d8" stroke-width="1"/>
    <line x1="0" y1="15" x2="240" y2="15" stroke="#00b4d8" stroke-width="0.5"/>
    <text x="120" y="12" text-anchor="middle" fill="#caf0f8" font-size="10">ARCHITECTURE DIAGRAM</text>
    <text x="120" y="40" text-anchor="middle" fill="#00b4d8" font-size="13" font-weight="700">图表标题</text>
  </g>
</svg>
```

---

## 重要规则

- **不要使用 `@import url()`**——rsvg-convert 无法获取外部资源
- 所有字体必须通过内联 `<style>` 声明
- 文字标签必须使用中文
- 保持正交布局（横平竖直），避免对角线连线
