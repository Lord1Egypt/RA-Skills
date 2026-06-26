---
name: book-library-scanner
description: 扫描本地电子书库，自动提取元数据、分类整理、联网搜索书籍简介，生成Obsidian笔记的完整工作流。支持EPUB/MOBI/AZW3/PDF格式。
---

# Book Library Scanner - 书库扫描入库技能

将本地电子书库扫描、分类整理、搜索简介、导入Obsidian的完整工作流。

## 触发场景

当用户提到以下需求时使用此技能：
- 扫描电子书库、整理书库
- 给书籍补充简介、搜索书籍信息
- 导入Obsidian、建立书库目录
- book library, scan books, organize ebooks

## 工作流程

### 1. 扫描书库目录

```python
# 扫描指定目录，提取epub/mobi/azw3/pdf格式的书籍元数据
# 支持读取书名、作者、分类等信息
```

**关键函数**：
- `scan_book_directory(book_dir)` - 扫描书库目录
- `extract_metadata(filepath)` - 提取单本书的元数据

### 2. 分类整理

**分类规则**：
- 根据书名/作者中的国家标注分类：如"(美)"、"(德)"、"(英)"、"(法)"等
- 默认分类：文学、历史、心理学、哲学、经济、科学技术、其他
- 目录结构：`分类/国家/作者/书名.md`

### 3. 搜索书籍简介

**API调用**：
使用元宝搜索API搜索书籍简介，每个请求间隔2秒避免限流。

**Windows编码处理**：
- PowerShell子进程传中文参数时，用UTF-8编码
- Python读取输出时用 `decode('utf-8', errors='ignore')`

### 4. 生成Obsidian笔记

每本书生成一个Markdown文件，包含：
- 书名、作者、分类、国家、格式
- 内容简介（从网络搜索获取）
- 来源链接

## 配置参数

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `book_dir` | 书库源目录 | 必填 |
| `output_dir` | 输出目录 | Required |
| `batch_size` | 每批处理数量 | 500 |
| `delay_seconds` | API请求间隔 | 2 |
| `save_every` | 每...本保存一次 | 100 |

## 文件结构

```
书库/
├── 书库索引.json        # 主索引（含全部书籍信息）
├── 书库总目录.md         # 总览文档
├── 文学/               # 分类文件夹
│   ├── 中国/           # 国家文件夹
│   │   ├── 鲁迅/       # 作者文件夹
│   │   │   ├── 呐喊.md
│   │   │   └── ...
│   └── ...
└── ...
```

## 索引文件格式

```json
{
  "version": "1.0",
  "scan_date": "2026-04-18",
  "books": [
    {
      "title": "书名",
      "author": "作者",
      "category": "文学",
      "country": "中国",
      "format": "EPUB",
      "filename": "原文件名.epub",
      "filepath": "原文件路径",
      "introduction": "内容简介",
      "intro_source": "来源URL"
    }
  ]
}
```

## 技术要点

### Windows编码问题

Python调用PowerShell传递中文参数时：
```python
result = subprocess.run(
    ['powershell', '-File', script_path, '-Keyword', keyword],
    capture_output=True,
    timeout=30
)
output = result.stdout.decode('utf-8', errors='ignore').strip()
```

### 文件名安全处理

```python
import re
safe_name = re.sub(r'[<>:"/\\|?*]', '', original_name)[:50]
```

### 批量处理检查点

每批完成后保存进度，支持断点续传：
```python
checkpoint = {
    'last_batch': batch_num,
    'total_found': found_count,
    'last_index': last_processed_index,
    'timestamp': datetime.now().isoformat()
}
```

## 已知问题

1. **拼音书名**：部分书籍元数据提取失败时，会使用文件夹拼音名作为书名。需要后续人工处理或更复杂的转换逻辑。

2. **搜索成功率**：后续批次的搜索成功率可能下降（80-99%），因为冷门书籍的搜索结果较少。

3. **API限流**：每请求间隔2秒，批量处理时需要较长时间（每500本约35-45分钟）。

## 示例用法

```
用户: 帮我扫描 D:\LWbook 书库，整理后导入 Obsidian

执行步骤:
1. 扫描 D:\LWbook 目录
2. 提取书籍元数据
3. 按分类→国家→作者整理
4. 搜索每本书的简介
5. 生成 Obsidian Markdown 笔记
6. 建立索引文件
```

## 相关文件

- `scripts/book_scanner.py` - 书库扫描脚本
- `scripts/batch_search.py` - 批量搜索简介脚本
- `scripts/generate_notes.py` - 生成Obsidian笔记脚本
- `scripts/search_book.ps1` - PowerShell搜索封装
