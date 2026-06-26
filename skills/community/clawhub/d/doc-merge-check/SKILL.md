---
name: doc-merge-check
version: 1.0.0
description: "通用文档合并与检查工具。将多个Word文档按指定顺序合并，统一格式（字体/字号/行距），并检查每个文档是否包含所需的板块。适用于作业收集、报告整合等场景。使用场景：(1) 合并多个学生的作业文档；(2) 检查文档是否包含指定板块；(3) 统一文档格式后整合；(4) 生成缺失报告。"
metadata: {"clawic":{"emoji":"📑"}}
---

## When to Use

当用户需要以下操作时使用：
- 合并多个Word文档（.docx）为一个
- 检查每个文档是否包含指定的板块/内容
- 统一多个文档的格式（字体、字号、行距等）
- 生成缺失板块的报告
- 收集作业、报告、论文等需要整合的场景

## Core Functions

### 1. 合并文档

将多个.docx文档按指定顺序合并成一个。

**调用方式**：
```python
from scripts.merge_and_check import merge_documents

# 基本用法
merge_documents(
    input_files=["成员1.docx", "成员2.docx", "成员3.docx"],
    output_file="合并结果.docx",
    member_order=["张三", "李四", "王五"]  # 可选
)
```

### 2. 检查板块完整性

检查每个文档是否包含指定的板块。

**调用方式**：
```python
from scripts.merge_and_check import check_sections

result = check_sections(
    files=["成员1.docx", "成员2.docx"],
    required_sections=["作业内容介绍", "作业截图", "个人电子签"]
)
# 返回：{'member1.docx': ['作业截图'], 'member2.docx': []}  # 缺失的板块
```

### 3. 统一格式

统一多个文档的字体、字号、行距等格式。

**调用方式**：
```python
from scripts.merge_and_check import format_document

format_document(
    input_file="input.docx",
    output_file="output.docx",
    font_config={
        "chinese_font": "宋体",      # 中文字体
        "english_font": "Times New Roman",  # 英文字体
        "body_size": 12,            # 正文字号（磅）
        "title_size": 15,          # 标题字号（磅）
        "line_spacing": 1.5,       # 行距倍数
        "margin_top": 2.54,         # 上边距（厘米）
        "margin_bottom": 2.54,      # 下边距
        "margin_left": 3.17,        # 左边距
        "margin_right": 3.17         # 右边距
    }
)
```

### 4. 一键执行完整流程

合并 + 检查 + 格式化 一起执行。

**调用方式**：
```python
from scripts.merge_and_check import process_homework

result = process_homework(
    input_folder=r"D:\作业文件夹",
    output_file="整合结果.docx",
    required_sections=["作业内容介绍", "作业截图", "个人电子签"],
    member_order=["张三", "李四", "王五"],
    font_config={
        "chinese_font": "宋体",
        "english_font": "Times New Roman",
        "body_size": 12,
        "line_spacing": 1.5
    }
)
# 返回：{'success': True, 'missing_report': {...}, 'merged_file': '整合结果.docx'}
```

## User Guidance

用户使用时请提供：

### 必须信息
1. **要合并的文档** - 文件路径或所在文件夹
2. **要检查的板块** - 如 ["作业内容介绍", "作业截图", "个人电子签"]

### 可选信息
3. **成员顺序** - 如 ["张三", "李四", "王五"]，留空则按文件名排序
4. **字体设置** - 如果需要统一格式
5. **输出文件名** - 默认为 "整��结果.docx"

### 用户指令示例

> "合并这个文件夹里的作业文档，检查每个人是否有作业内容介绍、作业截图和个人电子签"

> "把同学们的实验报告整合成一篇，按张三、李四、王五的顺序，字体改成小四宋体，行距1.5倍"

> "检查这篇论文是否包含摘要、引言、方法、结果、讨论、参考文献这几个部分"

## Default Config

默认格式配置（如用户不指定则使用）：

```python
DEFAULT_FONT_CONFIG = {
    "chinese_font": "宋体",
    "english_font": "Times New Roman",
    "body_size": 12,           # 小四
    "title_size": 15,            # 三号
    "line_spacing": 1.5,        # 1.5倍行距
    "margin_top": 2.54,        # 2.54cm = 1英寸
    "margin_bottom": 2.54,
    "margin_left": 3.17,
    "margin_right": 3.17
}
```

## Common Errors

- **文件找不到**：确保文件路径正确，使用绝对路径
- **板块检测不准**：有些文档可能用图片或表格代替文字，建议人工复核
- **格式不生效**：某些特殊样式可能需要手动调整

## Related Skills

- `word-docx` - Word文档详细处理（当需要更精细的控制时使用）