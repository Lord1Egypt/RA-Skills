# DrawIO 图表技能

基于开源工程 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) 微调的 DrawIO 图表技能，结合个人绘制风格（配色、形状、字体、排版）做了本地化。

## 功能特性

- 生成 `.drawio` 架构图 / 流程图 / ER 图 / UML / 时序图 / 网络拓扑 / ML 模型图
- 从已有 `.drawio` 文件**确定性提取个人绘制风格**，生成 style preset
- 从单张参考图**分析风格 + 结构**（页面/分组泳道/节点类型/边/布局），供生成新图参考
- 内置 `linlan` 个人风格预设（黑描边 + 浅色填充 + Tahoma + 直角矩形）
- 自动解码压缩格式 drawio 文件
- 导出 PNG / SVG / PDF / JPG（可选 draw.io 桌面版 CLI）

## 快速开始

### 1. 提取个人风格

```bash
# 从目录批量提取，生成 styles/linlan.json
python scripts/extract_style.py "C:\path\to\drawio-files" --name linlan

# 逐文件详细统计（复核用）
python scripts/analyze_style.py "C:\path\to\drawio-files"
```

### 2. 套用风格生成图表

生成 `.drawio` 时按 `styles/linlan.json` 取色：

| 角色 | 色槽 | 填充 | 描边 |
|------|------|------|------|
| 服务 service | primary | `#DAE8FC` | `#000000` |
| 数据库 database | success | `#D5E8D4` | `#000000` |
| 队列 queue | warning | `#FFF2CC` | `#000000` |
| 网关 gateway | accent | `#FFE6CC` | `#000000` |
| 错误 error | danger | `#F8CECC` | `#000000` |
| 外部 external | neutral | `#F5F5F5` | `#000000` |
| 安全 security | secondary | `#E1D5E7` | `#000000` |

字体 `Tahoma`，字号 `12`（标题 `14` 加粗），直角矩形，笔宽 `1`。

### 3. 参考某张图生成新图

```bash
# 分析参考图，产出参考报告（风格 + 结构双模板），供 AI 参考生成新图
python scripts/ref_analyze.py "参考图.drawio" -o ref_report.md
```

报告含：配色/字体/形状、页面尺寸、分组泳道层级、节点类型分布、边方向、布局模式。

### 4. 导出图片（可选）

```bash
# 需要 draw.io 桌面版 CLI
drawio -x -f png -o diagram.png diagram.drawio
drawio -x -f pdf -o diagram.pdf diagram.drawio
```

## 个人风格速查

从 15 张源图提取的个人绘制风格：

- **描边**：黑色 `#000000` 主导（814 次），分组色：红 `#EA6B66` / 绿 `#00994D` / 蓝 `#6666FF` / 深红 `#660000`
- **填充**：留白/透明为主（903 次），浅色 `#F5F5F5` / `#FFFAFA` / `#FFFFFF`
- **字体**：`Tahoma`（架构图）/ `Helvetica`（流程图）
- **字号**：`12` 主 / `10` 次 / `14` 标题
- **圆角**：直角为主（圆角仅约 9%）
- **页面**：1169×827（A4 横向），gridSize=10

## 目录结构

```
drawio-skills/
├── SKILL.md                  # 技能定义（AI 使用）
├── README.md                 # 用户文档（本文）
├── scripts/
│   ├── extract_style.py      # 风格提取（确定性）
│   ├── analyze_style.py      # 逐文件风格统计
│   └── ref_analyze.py        # 参考图分析（风格+结构）
├── styles/
│   ├── schema.json           # preset 结构定义
│   └── linlan.json           # 个人风格预设
└── style_report.json         # 风格分析报告
```

## 已知限制

- **黑描边+留白风格** 无法完全进 preset（schema 要求 fillColor 为 `#RRGGBB`），近似为浅色填充
- **自定义 stencil 形状** 无法保留（非标准 shape 关键词），颜色/标签/边仍可捕获
- **导出图片** 需 draw.io 桌面版 CLI，未装则只产出 `.drawio`

## 相关项目

- [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) - 参考开源工程（MIT）
- [linlan-skills](https://gitee.com/linlannet/linlan-skills) - 本技能所属仓库
