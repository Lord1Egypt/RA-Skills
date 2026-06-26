---
name: convert-markdown
version: 1.0.3
description: 文档处理与转换技能，基于 MarkItDown 工具。支持将 PDF、Word、PowerPoint、Excel、图片、音频等多种格式文件批量转换为 Markdown。适用于文档数字化、知识库构建、内容提取等场景。
---

# 文档转换技能 (convert-markdown)

## 概述

MarkItDown 是 Microsoft 开发的多功能文档转换工具，能够将各种文件格式高质量转换为 Markdown 格式。本技能提供完整的文档处理工作流，包括：

- **多格式支持**：PDF、DOCX、PPTX、XLSX、图片、音频、HTML、CSV、JSON、ZIP、EPub、YouTube URLs 等
- **结构化保留**：保持标题、列表、表格、链接等重要文档结构
- **批量处理**：支持目录递归处理和批量转换
- **OCR 能力**：图片和扫描 PDF 的文本识别
- **音频转录**：音频文件的语音转文本
- **可扩展性**：可选依赖组按需安装，适配不同需求场景

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10 或更高版本。建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. 安装 MarkItDown

```bash
# 安装完整功能（推荐）
pip install 'markitdown[all]'

# 或按需安装特定格式支持
pip install 'markitdown[pdf,docx,pptx]'
```

可选依赖组说明：
- `[all]` - 所有格式支持（PDF、Office、图片、音频、HTML 等）
- `[pdf]` - PDF 处理（包含 OCR）
- `[docx]` - Word 文档
- `[pptx]` - PowerPoint
- `[xlsx]` - Excel
- `[image]` - 图片 EXIF 和 OCR
- `[audio]` - 音频转录
- `[html]` - HTML 转换
- `[ytdlp]` - YouTube 下载

### 3. 基本使用

#### NPX CLI 方式（推荐）

本技能提供 NPX CLI 工具，可直接通过 npx 命令调用：

```bash
# 查看帮助
npx convert-markdown

# 转换单个文件
npx convert-markdown convert --input document.pdf --output document.md

# 转换目录
npx convert-markdown convert --input ./docs --output ./markdown

# 批量转换（指定格式）
npx convert-markdown batch --source ./docs --target ./markdown --include .pdf,.docx

# 覆盖已存在文件
npx convert-markdown convert --input document.pdf --output document.md --overwrite
```

**CLI 命令说明：**

| 命令 | 说明 | 参数 |
|------|------|------|
| `convert` | 转换文件或目录 | `--input`, `--output`, `--overwrite` |
| `batch` | 批量转换目录 | `--source`, `--target`, `--include`, `--exclude` |

#### MarkItDown 命令行方式

转换单个文件：
```bash
markitdown document.pdf > document.md
markitdown presentation.pptx -o slides.md
```

批量处理目录：
```bash
# 转换当前目录所有支持文件
markitdown *.pdf *.docx *.pptx

# 递归处理子目录
markitdown ./docs/ --recursive

# 输出到指定目录
markitdown ./source/ -o ./output/
```

#### Python API 方式

```python
from markitdown import MarkItDown

# 创建转换器实例
md = MarkItDown()

# 转换文件
result = md.convert("document.pdf")
print(result.text_content)

# 转换并保存
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

## 常见任务

### 任务 1: 批量转换知识库文档

将大量文档批量转换为 Markdown 格式，便于建立搜索索引：

```bash
# 创建输出目录
mkdir converted_docs

# 批量转换并保存
markitdown ./source_documents/ --recursive -o ./converted_docs/
```

### 任务 2: 处理扫描版 PDF

对于扫描的 PDF 文件，需要安装 OCR 依赖：

```bash
pip install 'markitdown[pdf]'  # 包含 OCR 功能
markitdown scanned_document.pdf -o text.md
```

### 任务 3: 提取表格数据

MarkItDown 能够保留原始表格结构：

```bash
markitdown financial_report.xlsx > report.md
# 输出中的表格将保持 Markdown 表格格式
```

### 任务 4: 处理多媒体文件

支持图片 OCR 和音频转录：

```bash
# 提取图片中的文字
markitdown screenshot.png > extracted_text.md

# 转换音频为文字记录
markitdown podcast.mp3 > transcript.md
```

### 任务 5: 集成到自动化流程

在 Python 脚本中使用：

```python
from pathlib import Path
from markitdown import MarkItDown

def convert_directory(input_dir, output_dir):
    """批量转换目录中的所有支持文件"""
    md = MarkItDown()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for file_path in input_path.rglob("*"):
        if file_path.is_file():
            try:
                result = md.convert(str(file_path))
                rel_path = file_path.relative_to(input_path)
                output_file = output_path / rel_path.with_suffix('.md')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(result.text_content, encoding='utf-8')
                print(f"✓ {file_path} -> {output_file}")
            except Exception as e:
                print(f"✗ {file_path}: {e}")

# 使用示例
convert_directory("./raw_docs/", "./markdown_docs/")
```

## 高级配置

### 自定义转换选项

```python
from markitdown import MarkItDown, StreamConverter

# 使用流式转换（处理大文件）
with open("large_file.pdf", "rb") as f:
    md = MarkItDown()
    result = md.convert_stream(f)
    print(result.text_content)
```

### 插件系统

MarkItDown 支持自定义转换器插件。如需扩展支持特殊格式，可开发自定义 DocumentConverter：

```python
from markitdown import DocumentConverter

class CustomConverter(DocumentConverter):
    def convert(self, file_stream, **kwargs):
        # 实现自定义转换逻辑
        pass

# 注册插件
md = MarkItDown(converters=[CustomConverter()])
```

### MCP 服务器集成

MarkItDown 提供 Model Context Protocol (MCP) 服务器，可与 Claude Desktop 等 LLM 应用集成：

```bash
# 安装 MCP 服务器
pip install markitdown[all,mcp]

# 配置 Claude Desktop 使用
# 在 claude_desktop_config.json 中添加：
# "mcpServers": {
#   "markitdown": {
#     "command": "python",
#     "args": ["-m", "markitdown.mcp"]
#   }
# }
```

## 最佳实践

1. **安装策略**：生产环境推荐 `[all]` 以确保格式兼容性；资源受限环境可按需安装
2. **内存管理**：处理超大文件时使用 `convert_stream()` 避免内存溢出
3. **错误处理**：转换可能失败（损坏文件、不支持的格式），应捕获异常并记录
4. **编码统一**：始终使用 UTF-8 编码读写 Markdown 文件
5. **文件组织**：输出目录结构与输入目录保持一致，便于维护和追踪
6. **性能优化**：批量转换时可并行处理（多进程/多线程）提高效率

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| `ModuleNotFoundError` | 依赖未安装 | 重新运行 `pip install 'markitdown[all]'` |
| OCR 不工作 | 缺少 Tesseract | 安装 Tesseract OCR 引擎 |
| 图片转换失败 | PIL/Pillow 缺失 | `pip install pillow` |
| YouTube 失败 | yt-dlp 未安装 | `pip install yt-dlp` |
| 内存不足 | 文件太大 | 使用 `convert_stream()` 或分批处理 |

## 资源目录说明

本技能包含以下资源目录：

- **scripts/** - 可执行脚本（示例和工具）
- **references/** - 参考文档和详细 API
- **assets/** - 模板和配置文件（当前为空）

## 相关链接

- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [GitHub 仓库](https://github.com/microsoft/markitdown)
- [MCP 服务器文档](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)

## 更新日志

- 2026-03-12 - v1.0.3 版本：
  - 修复：修正 CLI 脚本中指向 convert_markonverter.py 的路径错误
  - 优化：更新版本号，保持与 package.json 一致
  - 维护：清理冗余的 Node.js 包装器配置

- 2026-03-09 - 初始版本，基于 MarkItDown 0.1.0+ 创建技能模板