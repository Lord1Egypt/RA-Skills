# Code To Mindmap

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将源代码转换为可视化的思维导图、节点图和树状图 — 使用 Mermaid 语法

## 解决什么问题

代码结构从原始文本很难把握——类层次结构、函数关系和模块依赖在扁平文件中是不可见的。这个技能解析源代码并生成可视化图表，一目了然地展示架构。

**触发条件：** 源代码 + 可视化/思维导图/流程图意图。

## 功能特性

- **多语言支持** — 解析 Python、JavaScript/TypeScript、Go 及通用类/函数结构
- **层级可视化** — 将模块 → 类 → 方法 → 嵌套逻辑显示为树状结构
- **智能图表选择** — 类密集型文件用思维导图，导入依赖用图表，目录结构用树状图
- **区分外部库** — 将导入的标准库/包与项目内部调用区分标记

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install code-to-mindmap

# 或手动复制
cp -r code-to-mindmap ~/.openclaw/skills/
```

### 使用方法

```
/code-to-mindmap
```

粘贴源代码，要求可视化为思维导图。

```
/code-to-mindmap/hierarchy
```

仅显示项目文件/文件夹结构，不分析导入关系。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/code-to-mindmap` | 解析代码，输出 Mermaid 思维导图或图表 |
| `/code-to-mindmap/hierarchy` | 仅显示文件/文件夹结构，不分析导入 |

## 示例

| 场景 | 图表 |
|------|------|
| 单个 Python 类 | 中心 = 类名，方法作为子节点 |
| 多文件项目 | 每个模块多个子图表，导入关系用边表示 |
| 匿名/lambda 函数 | 标记为"anonymous / lambda"节点 |
| 20+ 节点的代码库 | 拆分为多个子图表，先显示顶层结构 |

## 目录结构

```
code-to-mindmap/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Mermaid 语法指南、解析模式
├── scripts/          # render.py — Mermaid 转 PNG/SVG
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。