# Roundtable Logo 设计规范

> 设计师：像素姐 🎨 | 日期：2026-05-21

---

## 设计概念

### 核心意象
**圆桌会议** — 俯视视角的圆桌，6 个 AI Agent 围坐讨论，中央汇聚点代表共识形成。

### 设计语言
- **圆环** = 圆桌 / 平等讨论的平台
- **六边形节点** = 各方 AI Agent（各持不同观点）
- **连线** = Agent 之间的对话与思想流动
- **中心菱形** = 共识收敛点（Convergence）
- **呼吸动画** = 讨论的活跃与生命力（仅 SVG 版）

### 为什么是 6 个节点？
- 3 个太少，不够体现"多方讨论"
- 6 个形成正六边形，几何美感强
- 暗合"六方会谈"的隐喻，多视角碰撞

---

## 配色体系（Tokyo Night）

### 暗色底版本（主力）

| 元素 | 色值 | 说明 |
|------|------|------|
| 主色渐变 | `#7aa2f7` → `#bb9af7` | 蓝→紫渐变，代表 AI 的智慧与想象力 |
| 节点 1 | `#7aa2f7` | Tokyo Blue — 冷静分析 |
| 节点 2 | `#bb9af7` | Tokyo Purple — 创意发散 |
| 节点 3 | `#7dcfff` | Tokyo Cyan — 技术理性 |
| 节点 4 | `#9ece6a` | Tokyo Green — 建设性意见 |
| 节点 5 | `#ff9e64` | Tokyo Orange — 挑战与质疑 |
| 节点 6 | `#c0caf5` | Tokyo Light — 综合视角 |
| 背景节点填充 | `#1a1b26` | Tokyo Night 深底色 |
| 辅助线 | `#565f89` | Tokyo Comment 灰 |

### 亮色底版本

| 元素 | 色值 | 说明 |
|------|------|------|
| 主色渐变 | `#2e7de9` → `#9854d1` | 加深饱和度，确保白底可见性 |
| 节点填充 | `#ffffff` | 白色底取代深色填充 |
| 色彩调整 | 对应暗色版加深 | 保持 Tokyo Night 色系但加深 |

---

## SVG 结构说明

### 文件清单

| 文件 | 用途 |
|------|------|
| `roundtable-logo.svg` | 完整版（含动画），用于网站展示 |
| `roundtable-logo-simple.svg` | 简化版（无动画），用于 PNG 导出 |
| `roundtable-logo-light.svg` | 亮色底版（白底适配配色） |

### 动画元素（仅完整版 SVG）
- 中心收敛环：呼吸脉动动画（r 30→40→30，3s 循环）
- 节点旁活动指示点：闪烁表示 Agent 正在发言
- 所有动画为纯装饰，不影响静态截图效果

---

## PNG 导出规格

### 暗色底版本（png-dark/）

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `roundtable-16x16.png` | 16×16 | favicon、极小图标 |
| `roundtable-32x32.png` | 32×32 | favicon、小图标 |
| `roundtable-64x64.png` | 64×64 | 标签页图标、列表图标 |
| `roundtable-128x128.png` | 128×128 | 社交平台头像 |
| `roundtable-256x256.png` | 256×256 | README 展示 |
| `roundtable-512x512.png` | 512×512 | 高清展示 |
| `roundtable-full-512x512.png` | 512×512 | 完整版（含辉光效果） |

### 亮色底版本（png-light/）

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `roundtable-16x16.png` | 16×16 | 亮色主题 favicon |
| `roundtable-32x32.png` | 32×32 | 亮色主题小图标 |
| `roundtable-64x64.png` | 64×64 | PyPI 项目页等 |
| `roundtable-128x128.png` | 128×128 | 亮色社交头像 |
| `roundtable-256x256.png` | 256×256 | 亮色 README 展示 |
| `roundtable-512x512.png` | 512×512 | 亮色高清展示 |

### Favicon（favicon/）

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `favicon-16x16.png` | 16×16 | 浏览器标签页 |
| `favicon-32x32.png` | 32×32 | 浏览器书签 |

---

## 使用场景指南

### README.md
```markdown
<p align="center">
  <img src="docs/design/assets/png-dark/roundtable-256x256.png" width="128" alt="Roundtable Logo">
</p>
```

### PyPI 项目页（亮色底推荐）
```markdown
<p align="center">
  <img src="docs/design/assets/png-light/roundtable-256x256.png" width="128" alt="Roundtable Logo">
</p>
```

### Favicon（HTML）
```html
<link rel="icon" type="image/png" sizes="32x32" href="docs/design/assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="docs/design/assets/favicon/favicon-16x16.png">
```

### Social Preview / OG 图（GitHub Social Preview）
```html
<!-- 使用 social-preview.html -->
<!-- 在浏览器打开，截图为 1280×640 PNG -->
<!-- 或直接上传 HTML 截图到 GitHub 仓库 Settings > Social preview -->
```

### Favicon SVG（极简版）
```html
<link rel="icon" type="image/svg+xml" href="docs/design/assets/svg/roundtable-favicon.svg">
```

---

## 设计走查清单

- [x] SVG 可正常渲染（3 个版本）
- [x] 暗色底 PNG 6 个尺寸齐全（16/32/64/128/256/512）
- [x] 亮色底 PNG 6 个尺寸齐全（16/32/64/128/256/512）
- [x] Favicon 16x16 和 32x32 可用
- [x] 16x16 清晰可辨认（简化版去除了动画和细线）
- [x] 配色与 Tokyo Night 暗色系协调
- [x] 设计概念体现"圆桌讨论"
- [x] 适合 favicon 和社交分享场景
- [x] Social Preview 1280×640 尺寸精确
- [x] Social Preview 包含项目名和定位语
- [x] Favicon SVG 极简版 16×16/32×32 清晰可辨

---

## 交付物清单

| # | 交付物 | 状态 |
|---|--------|------|
| 1 | SVG 源文件 × 3（完整版/简化版/亮色版） | ✅ |
| 2 | 暗色底 PNG × 7（含完整版） | ✅ |
| 3 | 亮色底 PNG × 6 | ✅ |
| 4 | Favicon PNG × 2 | ✅ |
| 5 | 设计规范文档（本文件） | ✅ |
| 6 | 预览页 preview.html | ✅ |
| 7 | Social Preview HTML (1280×640) | ✅ |
| 8 | Favicon SVG 极简版 | ✅ |

共计 **21 个交付文件** + 本文档 + 预览页。
