---
name: english-phonetics-batch
description: 批量为英文单词添加、检查和标注美式国际音标（IPA）。支持从文本文件批量导入单词，自动查询每个单词的美式发音音标，验证现有音标正确性，并输出格式化结果。
---

# English Phonetics Batch - 英文单词批量音标标注工具

**当以下情况时使用此 Skill：**

- 需要批量给英文单词列表添加**美式国际音标（IPA）**
- 需要检查现有单词表中的音标是否正确
- 需要将纯单词列表转换为带音标的词汇表
- 需要验证修复高考/四级/六级/雅思/托福等词汇表中损坏的音标
- 需要从编码损坏的文档中恢复问号占位的音标

## Features

- ✅ 自动查询每个单词的美式发音国际音标
- ✅ 支持批量处理从几十到几千个单词
- ✅ 检查现有音标正确性，标记并修复错误音标（自动修复问号占位符）
- ✅ **自动重试** - 指数退避重试网络错误和限流
- ✅ **统计报告** - 显示成功率和处理摘要
- ✅ 输出多种格式：纯文本、Markdown、CSV
- ✅ 美式发音优先，自动优先选择美式音标
- ✅ 处理结果包含单词 + 音标 + 词性
- ✅ 使用免费 API，不需要 API 密钥
- ✅ 可配置延迟和重试次数，灵活适应不同大小列表

## Quick Start

### Command Line

```bash
# Basic bulk processing (one word per line)
cd scripts/
python english_phonetics_batch.py input_words.txt output_with_phonetics.txt

# Check and fix existing file with corrupted phonetics (question marks from encoding errors)
python english_phonetics_batch.py input.txt output.txt --check

# Output as CSV for spreadsheets
python english_phonetics_batch.py words.txt output.csv --format csv

# Large vocabulary list - increase delay for safety, more retries
python english_phonetics_batch.py words.txt output.txt --delay 500 --retries 5
```

### Python API

```python
import sys
sys.path.insert(0, 'path/to/english-phonetics-batch/scripts')
from english_phonetics_batch import PhoneticsBatch

processor = PhoneticsBatch()
results = processor.process_words(["apple", "banana", "cherry"])
processor.save_results(results, "output.txt", format="text")
```

## Documentation

- **[Usage Examples](references/usage-examples.md)** - Complete examples for common use cases
- **[API Notes & IPA Reference](references/api-notes.md)** - Technical details about the API and American IPA symbols

## Output Formats

### Text format (default):
```
apple /ˈæpl/ noun
banana /bəˈnænə/ noun
cherry /ˈtʃeri/ noun
```

### CSV format (for spreadsheets):
```csv
word,phonetic_american,part_of_speech,is_valid
apple,/ˈæpl/,noun,True
banana,/bəˈnænə/,noun,True
```

### Markdown format:
| Word | American IPA | Part of Speech |
|------|--------------|----------------|
| apple | /ˈæpl/ | noun |
| banana | /bəˈnænə/ | noun |

## Requirements

- Python 3.6+
- `requests` library (`pip install requests`)
- Internet connection (for dictionary API queries)

## Installation

```bash
pip install requests
```

No other installation required - just clone and use.

## Author

Created for bulk English vocabulary phonetic transcription with American English IPA.
