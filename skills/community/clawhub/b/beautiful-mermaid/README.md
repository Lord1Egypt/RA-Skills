# Beautiful Mermaid Skill 使用指南

## 项目地址

| 说明 | 地址 |
|------|------|
| 本 Skill | [https://github.com/chouraycn/beautiful-mermaid](https://github.com/chouraycn/beautiful-mermaid) |
| 上游项目 | [https://github.com/lukilabs/beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) |

## 快速开始

### 1. 安装依赖

```bash
cd beautiful-mermaid
npm install
```

### 2. 交互式预览 (推荐)

```bash
# 在浏览器中打开样式定制预览工具
open assets/preview.html
```

**预览工具功能**：

- 15 个内置主题即时预览，点击切换
- 9 种图表类型：流程图、序列图、状态图、类图、ER 图、柱状图、折线图、组合图、水平柱状图
- 节点样式：背景色、圆角、边框、阴影
- 连线样式：粗细、颜色、箭头、圆角
- 5 种预设风格：默认、现代简约、渐变、线条轮廓、毛玻璃
- 一键导出带完整样式的 SVG 文件
- 使用 beautiful-mermaid 库渲染，与 CLI 输出一致

### 3. 运行示例

```bash
# 流程图
node scripts/render.js assets/examples/flowchart-basic.mmd -o flowchart-basic.svg

# 序列图
node scripts/render.js assets/examples/sequence-diagram.mmd -o sequence-diagram.svg

# 状态图
node scripts/render.js assets/examples/state-diagram.mmd -o state-diagram.svg

# ER 图
node scripts/render.js assets/examples/er-diagram.mmd -o er-diagram.svg

# 类图
node scripts/render.js assets/examples/class-diagram.mmd -o class-diagram.svg

# XY 柱状图
node scripts/render.js assets/examples/xychart-bar.mmd -o xychart-bar.svg

# XY 折线图
node scripts/render.js assets/examples/xychart-line.mmd -o xychart-line.svg

# XY 组合图
node scripts/render.js assets/examples/xychart-combo.mmd -o xychart-combo.svg
```

### 4. 使用不同主题

```bash
# 使用 dracula 主题
node scripts/render.js assets/examples/flowchart-basic.mmd -t dracula -o flowchart-dracula.svg

# 使用 catppuccin-mocha 主题
node scripts/render.js assets/examples/flowchart-basic.mmd -t catppuccin-mocha -o flowchart-catppuccin.svg

# 使用 github-light 主题 (亮色)
node scripts/render.js assets/examples/flowchart-basic.mmd -t github-light -o flowchart-light.svg
```

### 5. 渲染为 PNG (高清位图)

```bash
# 标准尺寸 PNG (1200px)
node scripts/render.js assets/examples/flowchart-basic.mmd -f png -o flowchart.png

# 2K 高清 PNG (2400px)
node scripts/render.js assets/examples/flowchart-basic.mmd -f png -w 2400 -o flowchart-hd.png

# 2x 缩放 PNG
node scripts/render.js assets/examples/flowchart-basic.mmd -f png -s 2 -o flowchart-2x.png

# 4K 超清 PNG (4800px)
node scripts/render.js assets/examples/flowchart-basic.mmd -f png -s 4 -o flowchart-4k.png

# 印刷质量 (300 DPI)
node scripts/render.js assets/examples/flowchart-basic.mmd -f png --dpi 300 -o flowchart-print.png
```

### 6. 渲染为 ASCII (终端输出)

```bash
node scripts/render.js assets/examples/flowchart-basic.mmd -f ascii
```

### 7. 自定义颜色 (Mono 模式)

```bash
# 自定义背景和前景色
node scripts/render.js assets/examples/flowchart-basic.mmd \
  --bg '#1a1b2e' \
  --fg '#e0e0e0' \
  --accent '#ff6b6b' \
  -o flowchart-custom.svg
```

### 8. XY 图表交互式 tooltip

```bash
# 启用鼠标悬停 tooltip
node scripts/render.js assets/examples/xychart-bar.mmd --interactive -o chart-interactive.svg
```

## 示例文件说明

| 文件 | 说明 |
|------|------|
| `flowchart-basic.mmd` | 基础流程图示例 |
| `sequence-diagram.mmd` | 序列图示例 |
| `state-diagram.mmd` | 状态图示例 |
| `er-diagram.mmd` | 实体关系图示例 |
| `class-diagram.mmd` | 类图示例 |
| `xychart-bar.mmd` | XY 柱状图示例 |
| `xychart-line.mmd` | XY 折线图示例 |
| `xychart-combo.mmd` | XY 组合图示例 |
| `system-architecture.mmd` | 复杂系统架构图 |
| `erp-*.mmd` | ERP 业务流程图 |

## 可用主题列表

| 主题 | 类型 | 说明 |
|------|------|------|
| tokyo-night | 暗色 | 东京之夜 |
| tokyo-night-storm | 暗色 | 东京之夜·暴风雨 |
| catppuccin-mocha | 暗色 | Catppuccin Mocha |
| nord | 暗色 | Nord 蓝 |
| dracula | 暗色 | 德古拉红 |
| github-dark | 暗色 | GitHub 暗色 |
| one-dark | 暗色 | One Dark |
| solarized-dark | 暗色 | Solarized 暗色 |
| zinc-dark | 暗色 | Zinc 暗色 |
| github-light | 亮色 | GitHub 亮色 |
| solarized-light | 亮色 | Solarized 亮色 |
| nord-light | 亮色 | Nord 亮色 |
| zinc-light | 亮色 | Zinc 亮色 |
| catppuccin-latte | 亮色 | Catppuccin Latte |
| tokyo-night-light | 亮色 | 东京之夜·亮色 |

## 提示

1. **交互式预览**：使用 `open assets/preview.html` 打开可视化样式定制工具
2. **SVG 输出**：适合嵌入网页、PPT 或文档中，支持透明背景和内联样式
3. **PNG 输出**：适合文档嵌入、PPT 演示，支持自定义尺寸 (默认 1200px，缩放 0.5-4x，DPI 72-600)
4. **ASCII 输出**：适合在终端、聊天界面或 Markdown 文档中展示
5. **透明背景**：设置 `transparent: true` 可以生成透明背景的 SVG
6. **主题选择**：暗色主题适合开发文档，亮色主题适合正式文档
7. **样式预设**：5 种预设风格（默认、现代简约、渐变、线条轮廓、毛玻璃）
8. **XY 图表**：使用 `xychart-beta` 语法，支持柱状图、折线图、组合图
9. **交互式图表**：使用 `--interactive` 参数为 XY 图表添加鼠标悬停 tooltip
