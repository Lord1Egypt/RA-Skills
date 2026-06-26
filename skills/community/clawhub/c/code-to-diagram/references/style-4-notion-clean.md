# Style 4: Notion Clean

极简白底风格。单一蓝色强调、无阴影、无图标装饰，适合 Notion 嵌入和 Wiki 文档。

---

## 颜色系统

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景 | `#ffffff` | 纯白 |
| 面板填充 | `#f9fafb` | gray-50 |
| 面板描边 | `#e5e7eb` | gray-200 |
| 主文字 | `#111827` | gray-900 |
| 副文字 | `#374151` | gray-700 |
| 弱文字 | `#9ca3af` | gray-400 |
| 标签文字 | `#6b7280` | gray-500 |
| 强调色（箭头） | `#3b82f6` | blue-500 |
| 分割线 | `#d1d5db` | gray-300 |

**蓝色仅用于箭头**——节点、文字、边框一律不使用彩色。

---

## 字体

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial,
             'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
```

| 用途 | 大小 | 字重 | 其他 |
|------|------|------|------|
| 标题 | 18px | 500 | — |
| 节点标签 | 14px | 500 | — |
| 类型标签 | 11px | 500 | `text-transform: uppercase; letter-spacing: 0.08em` |
| 正文 | 14px | 400 | — |

---

## 设计原则

- **纯几何**——仅用 rect、circle、diamond，不使用装饰图标
- **无阴影**——完全扁平
- **大留白**——面板内部至少 24px padding，面板间至少 40px 间距
- **单色箭头**——所有连线统一使用蓝色
- **大写标签**——分区标题和类型标签使用全大写

---

## 节点样式

### 标准节点

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4"
      fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>
<text x="{cx}" y="{cy}" text-anchor="middle" fill="#111827"
      font-size="14" font-weight="500">{标签}</text>
```

### 类型标签（节点上方）

```xml
<text x="{x}" y="{y-8}" fill="#9ca3af" font-size="11" font-weight="500"
      letter-spacing="0.08em">DATABASE</text>
```

### 分组容器（虚线框）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4"
      fill="none" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="4,3"/>
```

---

## 尺寸规范

| 元素 | 尺寸 |
|------|------|
| 节点最小 | 120×40px |
| 节点推荐 | 160×48px |
| 水平间距 | ≥80px |
| 垂直间距 | ≥60px |
| 标题位置 | 左上角，距边缘 32px |
| 画布默认 | 960×560 |

---

## 箭头标记

```xml
<defs>
  <marker id="arrow-blue" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#3b82f6"/>
  </marker>
  <marker id="arrow-gray" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#d1d5db"/>
  </marker>
</defs>
```

### 主连线

```xml
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
```

### 次要/可选连线

```xml
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
      stroke="#d1d5db" stroke-width="1" stroke-dasharray="4,3"
      marker-end="url(#arrow-gray)"/>
```

---

## 完整 SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" width="960" height="560">
  <style>
    text {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial,
                   'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
      fill: #111827;
    }
  </style>
  <defs>
    <marker id="arrow-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#3b82f6"/>
    </marker>
    <marker id="arrow-gray" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#d1d5db"/>
    </marker>
  </defs>

  <!-- 白色背景 -->
  <rect width="960" height="560" fill="#ffffff"/>

  <!-- 在此放置节点、连线 -->
</svg>
```

---

## 重要规则

- **不要使用 `@import url()`**——rsvg-convert 无法获取外部资源
- 所有字体必须通过内联 `<style>` 声明
- 文字标签必须使用中文
- 保持极简——不加阴影、不加渐变、不加装饰
- 图例仅在有 2 种以上连线类型时添加
