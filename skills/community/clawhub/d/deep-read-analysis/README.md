# Deep Read

**描述**：基于研究驱动方法，对书籍进行深度分析，生成系统化洞察、核心观点、金句摘录和实际应用指导，并生成关联常青笔记。

## 输入
- `book_title` (string)：书名
- `book_file` (file, 可选)：书籍文件（PDF/EPUB/TXT）
- `user_notes` (list)：用户已录入笔记

## 输出
- author_info: 作者介绍
- creation_context: 创作背景
- book_outline: 大纲及章节结构
- main_content: 主要内容解读
- core_insights: 核心观点
- key_quotes: 金句列表
- application_examples: 实际应用示例
- related_evergreen_notes: 关联常青笔记

## 使用示例
```python
from deep_read_generator import deep_read_analysis

result = deep_read_analysis(
    book_title="原则",
    user_notes=["已读章节摘要", "高亮笔记"]
)

print(result['core_insights'])
print(result['application_examples'])
print(result['related_evergreen_notes'])
