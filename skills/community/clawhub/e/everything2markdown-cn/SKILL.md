---
name: everything2markdown-cn
description: 使用 Microsoft MarkItDown 将各种文档格式（PDF/DOCX/PPTX/XLSX/图片/音频等）转换为 Markdown，专为 AGENT 和 LLM 工作流优化
homepage: https://github.com/microsoft/markitdown
metadata:
  emoji: 📝
  author: OpenClaw
  version: "1.0.0"
  category: document-processing
  tags: [markdown, 转换, pdf, docx, ocr, llm, agent, 中文]
  requires:
    bins: [python3, pip3]
    python_packages: [markitdown]
    env: []
  install:
    - id: install-markitdown
      kind: exec
      command: pip3 install 'markitdown[all]'
      label: 安装 MarkItDown 及所有依赖
---

# Everything2Markdown - 万物转 Markdown

专为 AGENT 和 LLM 工作流优化的文档转换工具，基于 Microsoft MarkItDown。

## 核心特性

- ✅ **多格式支持**: PDF, DOCX, PPTX, XLSX, EPUB, HTML
- ✅ **富媒体处理**: 图片(OCR), 音频(转录), YouTube 链接
- ✅ **结构保留**: 标题层级、表格、列表、链接
- ✅ **元数据提取**: 作者、创建时间、页数等
- ✅ **AGENT 优化**: 输出适合 LLM 处理的干净 Markdown

## 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | 完整文本提取，保留结构 |
| Word | .docx, .doc | 保留标题和表格 |
| PowerPoint | .pptx, .ppt | 逐页转换 |
| Excel | .xlsx, .xls | 工作表转表格 |
| EPUB | .epub | 电子书格式 |
| HTML | .html, .htm | 网页转换 |
| 图片 | .png, .jpg | OCR 文字提取 |
| 音频 | .mp3, .wav | 语音转文字 |
| YouTube | URL | 字幕和元数据 |

## 快速开始

### 转换单个文件

```bash
markitdown document.pdf -o output.md
```

### 批量转换目录

```bash
# 转换目录下所有 PDF 和 DOCX
find . -name "*.pdf" -o -name "*.docx" | while read f; do
  out="${f%.*}.md"
  markitdown "$f" -o "$out"
  echo "✓ 已转换: $f → $out"
done
```

### 高级选项

```bash
# 详细输出
markitdown document.pdf -o output.md --verbose

# 保留临时文件
markitdown document.pdf -o output.md --keep-temp

# 指定编码
markitdown document.pdf -o output.md --encoding utf-8
```

## Python API

### 基础用法

```python
from markitdown import MarkItDown

# 初始化
md = MarkItDown()

# 转换文件
result = md.convert("document.pdf")

# 访问内容
print(result.text_content)  # Markdown 文本
print(result.metadata)      # 文档元数据
```

### 高级 API

```python
from markitdown import MarkItDown

# 自定义配置
md = MarkItDown(
    enable_plugins=True
)

# 带选项转换
result = md.convert(
    "document.pdf",
    keep_formatting=True,
    extract_images=True
)

# 访问结构化数据
print(f"标题: {result.metadata.get('title')}")
print(f"作者: {result.metadata.get('author')}")
print(f"页数: {result.metadata.get('pages')}")
print(f"字数: {len(result.text_content.split())}")
```

## AGENT 工作流最佳实践

### 1. 文档预处理管道

```python
import re
from markitdown import MarkItDown

def preprocess_for_llm(file_path):
    """
    为 LLM 预处理文档。
    清理噪声，规范化格式，提取结构。
    """
    # 转换为 Markdown
    md = MarkItDown()
    result = md.convert(file_path)
    
    text = result.text_content
    
    # 清理过度格式化
    text = re.sub(r'\*{4,}', '***', text)  # 限制星号
    text = re.sub(r'\-{4,}', '---', text)  # 规范分隔线
    text = re.sub(r'\n{4,}', '\n\n\n', text)  # 限制空行
    
    # 规范化标题
    text = re.sub(r'^#{7,}', '######', text, flags=re.MULTILINE)
    
    return {
        'content': text,
        'metadata': result.metadata,
        'original_length': len(result.text_content),
        'processed_length': len(text)
    }
```

### 2. 结构化提取

```python
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Section:
    level: int
    title: str
    content: str
    start_line: int
    end_line: int

def extract_sections(md_text: str) -> List[Section]:
    """
    从 Markdown 提取层级章节。
    保留文档结构用于 AGENT 处理。
    """
    lines = md_text.split('\n')
    sections = []
    
    # 查找所有标题
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    headers = []
    
    for i, line in enumerate(lines):
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append({'level': level, 'title': title, 'line': i})
    
    # 提取章节
    for i, header in enumerate(headers):
        start_line = header['line']
        end_line = headers[i + 1]['line'] if i + 1 < len(headers) else len(lines)
        
        content = '\n'.join(lines[start_line + 1:end_line]).strip()
        
        sections.append(Section(
            level=header['level'],
            title=header['title'],
            content=content,
            start_line=start_line,
            end_line=end_line
        ))
    
    return sections
```

### 3. RAG 优化分块

```python
from typing import List, Dict
import hashlib

def chunk_for_rag(
    md_text: str,
    max_chunk_size: int = 1500,
    overlap: int = 200,
    preserve_headers: bool = True
) -> List[Dict]:
    """
    分块 Markdown 用于最优 RAG 检索。
    保留语义边界并提供丰富元数据。
    """
    chunks = []
    current_chunk = []
    current_size = 0
    chunk_index = 0
    
    # 按自然边界分割
    paragraphs = md_text.split('\n\n')
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # 检查是否超过限制
        if current_size + para_size > max_chunk_size and current_chunk:
            # 保存当前块
            chunk_text = '\n\n'.join(current_chunk)
            chunks.append(create_chunk_dict(
                chunk_text, chunk_index, md_text
            ))
            
            # 重叠开始新块
            if overlap > 0:
                overlap_text = '\n\n'.join(current_chunk[-2:]) if len(current_chunk) >= 2 else chunk_text[-overlap:]
                current_chunk = [overlap_text, para]
                current_size = len(overlap_text) + para_size
            else:
                current_chunk = [para]
                current_size = para_size
            
            chunk_index += 1
        else:
            current_chunk.append(para)
            current_size += para_size + 2  # +2 for newlines
    
    # 别忘了最后一块
    if current_chunk:
        chunk_text = '\n\n'.join(current_chunk)
        chunks.append(create_chunk_dict(
            chunk_text, chunk_index, md_text
        ))
    
    return chunks

def create_chunk_dict(text: str, index: int, source: str) -> Dict:
    """创建带元数据的块字典。"""
    return {
        'index': index,
        'text': text,
        'length': len(text),
        'hash': hashlib.md5(text.encode()).hexdigest()[:8],
        'source_length': len(source),
        'percent_start': 0 if index == 0 else round((sum(len(c) for c in source[:text]) / len(source)) * 100, 1)
    }
```

### 4. 文档分析管道

```python
from typing import Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class DocumentAnalysis:
    """AGENT 消费的完整文档分析。"""
    file_path: str
    file_type: str
    word_count: int
    char_count: int
    section_count: int
    heading_levels: Dict[int, int]  # level -> count
    has_tables: bool
    has_images: bool
    has_links: bool
    estimated_reading_time: int  # minutes
    summary: str
    keywords: list
    metadata: Dict[str, Any]

class DocumentAnalyzer:
    """AGENT 工作流的文档分析器。"""
    
    def __init__(self):
        self.md = MarkItDown()
    
    def analyze(self, file_path: str) -> DocumentAnalysis:
        """完整文档分析。"""
        # 转换为 Markdown
        result = self.md.convert(file_path)
        text = result.text_content
        
        # 基础统计
        word_count = len(text.split())
        char_count = len(text)
        
        # 章节分析
        sections = extract_sections(text)
        section_count = len(sections)
        
        # 标题层级
        heading_levels = {}
        for s in sections:
            heading_levels[s.level] = heading_levels.get(s.level, 0) + 1
        
        # 特性检测
        has_tables = '|' in text and '---' in text
        has_images = '![' in text
        has_links = 'http' in text or '[' in text
        
        # 阅读时间（平均 200 字/分钟）
        reading_time = max(1, word_count // 200)
        
        # 提取关键词（简单方法）
        words = re.findall(r'\b[A-Za-z][a-z]{4,}\b', text)
        word_freq = {}
        for w in words:
            w = w.lower()
            if w not in ['would', 'could', 'should', 'there', 'their', 'about']:
                word_freq[w] = word_freq.get(w, 0) + 1
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 生成摘要
        summary = self._generate_summary(text, sections)
        
        return DocumentAnalysis(
            file_path=file_path,
            file_type=file_path.split('.')[-1].lower(),
            word_count=word_count,
            char_count=char_count,
            section_count=section_count,
            heading_levels=heading_levels,
            has_tables=has_tables,
            has_images=has_images,
            has_links=has_links,
            estimated_reading_time=reading_time,
            summary=summary,
            keywords=[k[0] for k in keywords],
            metadata=result.metadata
        )
    
    def _generate_summary(self, text: str, sections: List[Section]) -> str:
        """生成文档摘要。"""
        if not sections:
            return text[:500] + "..." if len(text) > 500 else text
        
        # 获取主要章节
        main_sections = [s for s in sections if s.level <= 2]
        if main_sections:
            section_list = ", ".join([s.title for s in main_sections[:5]])
            return f"文档包含: {section_list}"
        
        return text[:300] + "..." if len(text) > 300 else text
```

## 高级功能

### 处理图片（OCR）

```bash
# 提取图片中的文字
markitdown image.png --ocr-enabled
```

### 处理音频（转录）

```bash
# 音频转文字
markitdown recording.mp3 --speech-transcription
```

### 处理 YouTube

```bash
# 提取 YouTube 视频字幕和元数据
markitdown "https://youtube.com/watch?v=..."
```

## 故障排除

### 安装问题

```bash
# 确保安装完整依赖
pip install 'markitdown[all]'

# 或使用 Conda
conda install -c conda-forge markitdown
```

### 转换失败

```bash
# 启用详细日志
markitdown file.pdf -o out.md --verbose

# 检查文件权限
file file.pdf
ls -la file.pdf
```

### 中文乱码

```bash
# 确保使用 UTF-8
export LANG=en_US.UTF-8
markitdown chinese.pdf -o output.md
```

## MCP 服务器集成

MarkItDown 提供 MCP (Model Context Protocol) 服务器，可用于 Claude Desktop 等工具：

```bash
pip install markitdown-mcp
```

配置 Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "python",
      "args": ["-m", "markitdown_mcp"]
    }
  }
}
```

## 相关链接

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [MCP Server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- [OpenClaw Skills 文档](https://docs.openclaw.ai/guide/skills)

---

**提示**: 此 Skill 专为 AGENT 和 LLM 工作流优化，输出的 Markdown 格式干净、结构清晰，非常适合 RAG 系统和 AI 处理管道使用。