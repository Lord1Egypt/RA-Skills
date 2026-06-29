---
name: chart-to-image
version: 1.0.0
description: 交互式图表转PNG/JPG/SVG图片，支持批量导出和多尺寸预设
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

前面几个 Skill 生成的交互式 HTML 图表在网页上很好用，但当需要嵌入 PPT、Word、邮件，或分享到飞书、微信等不支持 HTML 的平台时，就需要静态图片了。手动截图分辨率低、比例不对、操作繁琐，批量导出时更痛苦。

本 Skill 作为上述图表技能族的配套工具，通过 Canvas API 将交互式图表/表格/甘特图等 HTML 渲染为 PNG / JPG / SVG 图片。支持单张导出、批量转换、多种尺寸预设（社交、PPT、打印），满足不同的分享和存档需求。

---

# Chart to Image — 图表转图片 Skill

> 将交互式图表/表格/甘特图等转换为可下载的 PNG / JPG / SVG 图片。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **输入图表 HTML**：粘贴图表的 HTML 代码、SVG 代码，或提供 Canvas 绘制代码
2. **选择输出格式**：PNG（透明背景）、JPG（白色背景）、SVG（矢量保留）
3. **选择尺寸预设**：标准、社交媒体、PPT 适配、打印高分辨率
4. **配置参数**：分辨率、质量、背景色等
5. **生成图片**：输出指定格式的图片文件供下载

### 输入格式建议

- 粘贴完整的 HTML 文件内容（含 SVG/Canvas）
- 或仅粘贴 SVG 代码段
- 或粘贴 Canvas 绘制 JavaScript 代码

## 场景-模式映射表

| 使用场景 | 推荐格式 | 尺寸预设 | 特点 |
|---------|---------|---------|------|
| 网页/App 嵌入 | png-export（PNG） | 原始尺寸 | 透明背景，保留透明度 |
| PPT / Keynote | presentation（PPT 适配） | 16:9 / 4:3 | 白色背景，适配幻灯片 |
| 微信/飞书分享 | social-size（社交媒体） | 1200×628 | 社交媒体推荐尺寸 |
| 打印/存档 | print-ready（打印高分辨率） | 300 DPI | 高清 300 DPI 以上 |
| 矢量编辑需要 | svg-export（SVG 保留） | 矢量无限 | 保留可编辑性 |
| 批量归档 | batch-export（批量导出） | 混合 | 多图表一次输出 |
| 文档插图 | jpg-export（JPG） | 适中尺寸 | 文件小，白色底色 |

## 配色方案库

### 背景色选项
- **透明背景**：适合嵌入网页 / App
- **白色背景**：适合文档 / PPT / 邮件
- **暗色背景**：适合深色模式展示

### 分辨率预设
| 预设 | 宽度 | 高度 | 适用 |
|------|------|------|------|
| 标准 | 800px | 自适应 | 通用 |
| 社交 | 1200px | 628px | 微信/公众号/微博 |
| PPT 16:9 | 1920px | 1080px | 演示文稿 |
| PPT 4:3 | 1440px | 1080px | 旧版演示文稿 |
| 高清打印 | 2400px | 自适应 | 300 DPI 打印质量 |
| 超高清 | 3840px | 自适应 | Retina 屏幕 |

## 交互增强包列表

### 基础交互
- 格式选择（PNG / JPG / SVG）
- 尺寸调整（宽度 + 自动高度，或固定宽高）
- 质量设置（JPEG 压缩率）
- 背景色切换

### 高级交互
- 批量处理（多图表队列导出）
- 水印添加（文字水印 / Logo）
- 预览对比（原图 vs 设置后）
- 裁剪（自定义区域选择）

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **渲染引擎**：使用 Canvas API 进行渲染和位图转换
- **SVG 导出**：直接输出原始 SVG 代码，无需 Canvas 渲染
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：预览区域自适应

## 命令定义

### `/chart-to-image`
主入口命令。输入图表 HTML 或 SVG 代码，选择输出格式和尺寸后生成图片。

### `/chart-batch`
批量转换多个图表。支持一次性输入多个图表，按统一配置批量输出。

## 文件结构

```
skills/chart-to-image/
├── SKILL.md
├── patterns/
│   ├── png-export.json      # PNG 导出（透明背景）
│   ├── jpg-export.json      # JPG 导出（白色背景）
│   ├── svg-export.json      # SVG 保留（矢量）
│   ├── batch-export.json    # 批量导出
│   ├── social-size.json     # 社交媒体尺寸
│   ├── presentation.json    # PPT 适配尺寸
│   └── print-ready.json     # 打印高分辨率
└── templates/
    ├── base.html
    ├── png-export.html
    ├── jpg-export.html
    ├── svg-export.html
    ├── batch-export.html
    ├── social-size.html
    ├── presentation.html
    └── print-ready.html
```
