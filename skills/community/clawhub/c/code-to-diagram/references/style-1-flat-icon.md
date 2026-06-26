# Style 1: Flat Icon（默认）

灵感来源于 draw.io 默认风格和 Apple 文档美学。白底、清晰、专业，适合文档、博客和演示文稿。

---

## 颜色系统

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景 | `#ffffff` | 纯白 |
| 面板填充 | `#ffffff` | 白色 |
| 面板描边 | `#d1d5db` | gray-300 |
| 主文字 | `#111827` | gray-900 |
| 副文字 | `#6b7280` | gray-500 |

### 语义箭头色

| 流类型 | 色值 | 说明 |
|--------|------|------|
| 主数据流 | `#2563eb` | blue-600 |
| 错误/备选路径 | `#dc2626` | red-600 |
| 数据存储/成功 | `#16a34a` | green-600 |
| 异步/事件 | `#9333ea` | purple-600 |

### 图标强调色（浅色/深色对）

| 颜色 | 浅色底 | 深色底 |
|------|--------|--------|
| 蓝色 | `#eff6ff` | `#dbeafe` |
| 红色 | `#fef2f2` | `#fee2e2` |
| 绿色 | `#f0fdf4` | `#dcfce7` |
| 紫色 | `#faf5ff` | `#ede9fe` |
| 橙色 | `#fff7ed` | `#fed7aa` |
| 青色 | `#f0fdfa` | `#ccfbf1` |

---

## 字体

```
font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
```

| 用途 | 大小 | 字重 |
|------|------|------|
| 标签 | 14px | 400 |
| 副标签 | 12px | 400 |
| 标题 | 16px | 600 |

---

## 节点样式

### 标准节点

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" ry="8"
      fill="#ffffff" stroke="#d1d5db" stroke-width="1.5"/>
```

### 强调节点（带色底）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" ry="8"
      fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
```

### 圆角半径

所有矩形节点：`rx="8"` `ry="8"`

---

## 箭头标记

在 `<defs>` 中为每种颜色定义 marker：

```xml
<defs>
  <marker id="arrow-blue" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>
  </marker>
  <marker id="arrow-red" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#dc2626"/>
  </marker>
  <marker id="arrow-green" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#16a34a"/>
  </marker>
  <marker id="arrow-purple" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#9333ea"/>
  </marker>
</defs>
```

连线示例：

```xml
<line x1="100" y1="50" x2="300" y2="50"
      stroke="#2563eb" stroke-width="1.5"
      marker-end="url(#arrow-blue)"/>
```

---

## 图例

当使用 2 种以上箭头颜色时，必须在左下角添加图例：

```xml
<g transform="translate(20, 540)">
  <text x="0" y="0" fill="#111827" font-size="12" font-weight="600">图例</text>
  <line x1="0" y1="14" x2="30" y2="14" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
  <text x="36" y="18" fill="#6b7280" font-size="12">主数据流</text>
  <line x1="0" y1="30" x2="30" y2="30" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arrow-red)"/>
  <text x="36" y="34" fill="#6b7280" font-size="12">错误/备选</text>
  <line x1="0" y1="46" x2="30" y2="46" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arrow-green)"/>
  <text x="36" y="50" fill="#6b7280" font-size="12">数据写入</text>
  <line x1="0" y1="62" x2="30" y2="62" stroke="#9333ea" stroke-width="1.5" marker-end="url(#arrow-purple)"/>
  <text x="36" y="66" fill="#6b7280" font-size="12">异步事件</text>
</g>
```

---

## 完整 SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600">
  <style>
    text {
      font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC',
                   'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
      fill: #111827;
    }
  </style>
  <defs>
    <marker id="arrow-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>
    </marker>
    <marker id="arrow-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#dc2626"/>
    </marker>
    <marker id="arrow-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#16a34a"/>
    </marker>
    <marker id="arrow-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#9333ea"/>
    </marker>
  </defs>

  <!-- 白色背景 -->
  <rect width="960" height="600" fill="#ffffff"/>

  <!-- 在此放置节点、连线和图例 -->
</svg>
```

---

## 重要规则

- **不要使用 `@import url()`**——rsvg-convert 无法获取外部资源
- 所有字体必须通过内联 `<style>` 声明
- 文字标签必须使用中文
- viewBox 根据实际内容调整大小
