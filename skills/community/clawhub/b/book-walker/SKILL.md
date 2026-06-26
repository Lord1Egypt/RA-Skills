---
name: book-walker
description: 交互式 PDF 逐行阅读器。当用户想要阅读 PDF 文档、控制阅读进度（下一页、上一页、跳转第 X 页）、搜索内容、添加书签、整理 PDF 列表时使用此 skill。支持「开始读」「下一句」「去第 X 页」「搜索」「书签」等自然语言指令。适用于长文档分块阅读、定位特定章节、关键词搜索等场景。
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires":
          {
            "bins": ["python3"]
          },
        "install":
          [
            {
              "id": "venv",
              "kind": "shell",
              "label": "Create venv and install dependencies",
              "command": "cd ~/.openclaw/workspace-e/skills/book-walker && python3 -m venv .venv && .venv/bin/pip install pdfplumber pypdfium2"
            },
          ],
      },
  }
---

# Deep Reading Skill

交互式PDF逐行阅读器，支持块级/行级翻页、跳转、搜索、书签等功能。

## 触发方式

当用户想要阅读PDF文档、通过指令控制阅读进度时使用此skill。

## 功能

- 📖 **打开PDF**: 加载PDF文件并开始阅读
- ➡️ **下一句**: 读取下一块/行内容
- ⬅️ **上一句**: 返回上一块/行
- 🔄 **重读**: 重新读取当前内容
- 📑 **跳转**: 支持页码跳转、块跳转
- 🔍 **搜索**: 关键词全文搜索
- 🔖 **书签**: 添加和管理书签
- 📊 **进度**: 显示阅读进度

## 指令列表

| 指令 | 说明 | 示例 |
|------|------|------|
| `开始读 <文件>` | 打开PDF文件 | `开始读 /path/to/file.pdf` |
| `模式 text` / `模式 ocr` | 切换提取模式 | `模式 ocr` |
| `下一句` / `继续` | 读取下一块 | `下一句` |
| `上一句` / `后退` | 返回上一块 | `上一句` |
| `重读` / `再念一遍` | 重读当前块 | `重读` |
| `去第X页` | 跳转到指定页 | `去第10页` |
| `跳到第X块` | 跳转到指定块 | `跳到第5块` |
| `跳到第X行` | 跳转到指定行 | `跳到第50行` |
| `搜索 <关键词>` | 搜索关键词 | `搜索 机器学习` |
| `书签` | 查看书签列表 | `书签` |
| `书签 添加 <备注>` | 添加书签 | `书签 添加 重要` |
| `模板 列表` | 列出可用模板 | `模板 列表` |
| `模板 使用 <名>` | 切换当前模板 | `模板 使用 原文翻译解读` |
| `模板 定义 <名> <内容>` | 定义/覆盖模板 | `模板 定义 简洁 请逐句翻译` |
| `列出PDF` / `列表` | 扫描 workspace 下所有 PDF 并建立索引 | `列出PDF` |
| `进度` | 显示阅读进度 | `进度` |
| `暂停` | 暂停阅读 | `暂停` |
| `关闭` | 关闭当前PDF | `关闭` |
| `帮助` | 显示帮助 | `帮助` |

## 使用示例

```
用户: 列出PDF
助手: 📚 当前 Workspace 可读 PDF 索引
     路径: /path/to/workspace-e
     ━━━━━━━━━━━━━━━━━━━━━━━━
     共 3 个 PDF：
      1. docs/report.pdf
      2. papers/paper.pdf
     💡 使用「开始读 1」或「开始读 report.pdf」打开

用户: 开始读 /home/docs/report.pdf
助手: 📄 第1页 · 块1/50 · [██░░░░░░░] 4%
     ━━━━━━━━━━━━━━━━━━━━━━━━
     第一章 项目概述
     
     本报告主要介绍...

用户: 下一句
助手: 📄 第1页 · 块2/50 · [██░░░░░░░] 6%
     ━━━━━━━━━━━━━━━━━━━━━━━━
     
     1.1 项目背景...

用户: 去第5页
助手: 📄 第5页 · 块20/50 · [████░░░░░] 40%
     ━━━━━━━━━━━━━━━━━━━━━━━━
     第二章 技术方案...
```

## 实现细节

### 核心模块

```
pdf-reader/
├── __init__.py         # 主入口
├── reader/
│   ├── types.py        # 类型定义
│   ├── exceptions.py   # 异常类
│   ├── blocks.py       # 数据类
│   ├── parser.py       # PDF解析引擎
│   ├── state.py        # 状态管理
│   └── cache.py        # 缓存管理
├── commands/
│   └── navigation.py   # 导航指令
└── ui/
    └── formatter.py   # 输出格式化
```

### MVP 范围

- ✅ 可搜索PDF（非扫描件）
- ✅ 单栏布局
- ✅ 无页数限制（按需解析+落盘）
- ✅ 块级翻页
- ✅ 页码跳转
- ✅ 进度显示
- ✅ 书签（按 PDF 持久化）

### 技术依赖

- pdfplumber: 文本/表格提取
- PyMuPDF: 图片提取

### 模板与 Agent LLM 加工

- **块级导航**：`下一句` 按块（paragraph）推进
- **模板**：用户可 `模板 定义`、`模板 使用`，skill 不调用 LLM
- **Structured Payload**：当使用非默认模板时，skill 在输出末尾附加 `[PDF_READER_TEMPLATE_PAYLOAD]` 块，内含 `template_prompt`、`original`、`page`、`block_id`
- **Agent 职责**：解析该 payload 后，**由 Agent 调用 LLM** 按 `template_prompt` 对 `original` 加工（如 原文/翻译/解读），将 LLM 输出呈现给用户

### 存储结构

每个 PDF 有独立目录（`~/.cache/pdf-reader/{hash}/`），包含：
- `index.json` - 索引（total_pages, page_offsets）
- `p1.json`, `p2.json` ... - 各页块数据
- `state.json` - 阅读进度
- `bookmarks.json` - 书签

## 注意事项

1. MVP版本不支持扫描件PDF（需要OCR）
2. MVP版本不支持多栏布局
3. 大文件可能需要较长的初始加载时间
4. 书签与解析结果、进度均按 PDF 分目录保存，切换 PDF 即切换目录

## PDF 文本提取说明

### 提取模式

PDF Reader 支持两种文本提取模式：

| 模式 | 命令 | 说明 |
|------|------|------|
| 文本模式 | `模式 text` | 默认，使用 pdfplumber 直接提取 PDF 文本 |
| OCR 模式 | `模式 ocr` | 将页面转为图片后用 tesseract 识别 |

### 文本模式
- 适用于：大多数正常 PDF
- 优点：速度快
- 问题：部分 PDF（老版本 LaTeX 生成）文本流没有空格

### OCR 模式
- 适用于：扫描件PDF、文本提取有问题的 PDF
- 优点：识别准确
- 缺点：速度较慢
- **需要安装 tesseract**：
  ```bash
  # macOS
  brew install tesseract
  
  # Ubuntu
  sudo apt install tesseract-ocr
  ```

### 使用示例
```
用户: 模式 ocr
助手: ✅ 已切换到 ocr 模式

用户: 开始读 xxx.pdf
助手: (使用 OCR 提取文本...)
```

### 技术实现
- `text_enhance.py`：文本后处理模块
  - `enhance_text()` - 智能添加空格
  - `is_scanned_pdf()` - 检测是否为扫描件
- `parser.py`：
  - `_extract_blocks()` - 文本提取
  - `_extract_blocks_ocr()` - OCR 提取
