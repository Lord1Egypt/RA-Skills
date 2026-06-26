# Style 2: Dark Terminal

霓虹暗底黑客美学。适合 GitHub README、技术博客、开发者面向文档。

---

## 颜色系统

### 基础色

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景起点 | `#0f0f1a` | 近黑色 |
| 背景终点 | `#1a1a2e` | 深蓝黑 |
| 面板填充 | `#0f172a` | slate-950 |
| 面板描边 | `#334155` | slate-700 |

### 文字层级

| 用途 | 色值 | 说明 |
|------|------|------|
| 主文字 | `#e2e8f0` | slate-200 |
| 副文字 | `#94a3b8` | slate-400 |
| 弱文字 | `#475569` | slate-600 |

### 强调色

| 名称 | 主色 | 亮色 | 用途 |
|------|------|------|------|
| 紫色 | `#7c3aed` | `#a855f7` | AI/ML 节点 |
| 橙色 | `#ea580c` | `#f97316` | 计算/API 节点 |
| 蓝色 | `#1d4ed8` | `#3b82f6` | 网络/网关 |
| 绿色 | `#059669` | `#10b981` | 存储/数据库 |
| 金色 | `#eab308` | — | 警告/高亮 |
| 红色 | `#dc2626` | `#ef4444` | 错误/关键 |

### 主题化面板填充

| 功能 | 填充 | 描边 |
|------|------|------|
| AI/ML 节点 | `#1e1b4b` | `#7c3aed` |
| 计算/API | `#1c1917` | `#ea580c` |
| 存储/数据库 | `#052e16` | `#059669` |
| 网络/网关 | `#1e3a5f` | `#3b82f6` |

---

## 字体

```
font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', 'JetBrains Mono',
             'Courier New', 'Microsoft YaHei', 'SimHei', monospace;
```

| 用途 | 大小 | 字重 |
|------|------|------|
| 标签 | 13px | 400 |
| 副标签 | 11px | 400 |
| 标题 | 15px | 700 |
| 字距 | `letter-spacing: 0.02em` | — |

---

## 节点样式

### 标准面板

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6"
      fill="#0f172a" stroke="#334155" stroke-width="1"/>
```

### 主题化强调面板

```xml
<!-- AI/ML 节点示例 -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6"
      fill="#1e1b4b" stroke="#7c3aed" stroke-width="1.5"/>
```

---

## 发光效果（可选，用于关键节点）

```xml
<defs>
  <filter id="glow-purple" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur"/>
    <feFlood flood-color="#a855f7" flood-opacity="0.4" result="color"/>
    <feComposite in="color" in2="blur" operator="in" result="glow"/>
    <feMerge>
      <feMergeNode in="glow"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<!-- 使用发光效果的节点 -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" ry="6"
      fill="#1e1b4b" stroke="#a855f7" stroke-width="1.5"
      filter="url(#glow-purple)"/>
```

---

## 箭头标记

```xml
<defs>
  <marker id="arrow-purple" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#7c3aed"/>
  </marker>
  <marker id="arrow-orange" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#ea580c"/>
  </marker>
  <marker id="arrow-blue" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#1d4ed8"/>
  </marker>
  <marker id="arrow-green" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#059669"/>
  </marker>
</defs>
```

箭头颜色规则：箭头使用源节点主题对应的强调色。

---

## 背景渐变

```xml
<defs>
  <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0f0f1a"/>
    <stop offset="100%" stop-color="#1a1a2e"/>
  </linearGradient>
</defs>
<rect width="960" height="600" fill="url(#bg-grad)"/>
```

---

## 完整 SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600">
  <style>
    text {
      font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', 'JetBrains Mono',
                   'Courier New', 'Microsoft YaHei', 'SimHei', monospace;
      fill: #e2e8f0;
    }
  </style>
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f0f1a"/>
      <stop offset="100%" stop-color="#1a1a2e"/>
    </linearGradient>
    <filter id="glow-purple" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur"/>
      <feFlood flood-color="#a855f7" flood-opacity="0.4" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow-purple" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-orange" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#ea580c"/>
    </marker>
    <marker id="arrow-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#059669"/>
    </marker>
  </defs>

  <!-- 渐变背景 -->
  <rect width="960" height="600" fill="url(#bg-grad)"/>

  <!-- 在此放置节点、连线和图例 -->
</svg>
```

---

## 重要规则

- **不要使用 `@import url()`**——rsvg-convert 无法获取外部资源
- 所有字体必须通过内联 `<style>` 声明
- 文字标签必须使用中文
- 箭头颜色应匹配源节点的主题色
