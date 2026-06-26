# Deep Read

**显示名称**: Deep Read  
**版本**: 1.0.0  
**描述**: 基于研究驱动方法，对书籍进行深度分析，提炼核心观点、金句，并生成实际应用指导和关联常青笔记。  
**作者**: Zhu Bao

## 输入参数
- `book_title` (string, 必填)：书名
- `book_file` (file, 可选)：书籍文件（PDF/EPUB/TXT）
- `user_notes` (list, 可选)：用户已录入的笔记，用于生成关联常青笔记

## 输出参数
- `author_info` (string)：作者介绍（生平、教育、主要著作、影响等）
- `creation_context` (string)：创作背景（时间、社会环境、动机、评论等）
- `book_outline` (string)：章节结构、大纲及核心观点
- `main_content` (string)：书籍主要内容解读与分析
- `core_insights` (string)：书籍最重要思想和见解
- `key_quotes` (list)：引人深思的金句及分析
- `application_examples` (list)：生活、学习和工作中的应用指导
- `related_evergreen_notes` (list)：基于用户笔记生成的常青笔记标题及链接

## 标签
#deep-reading #knowledge-management #research-driven #book-analysis #insights

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
