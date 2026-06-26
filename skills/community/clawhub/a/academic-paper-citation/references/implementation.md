# 学术论文引用处理工具 - 实现细节

## 核心算法说明

### 1. 参考文献提取算法

使用正则表达式匹配参考文献列表：

```python
# 匹配 [数字] 开头的引用
ref_pattern = r'参考文献\s*\n(.*?)(?=致谢|$)'
ref_lines = re.findall(r'\[(\d+)\]\s*(.+?)(?=\[\d+\]|$)', ref_section, re.DOTALL)
```

支持的文献类型检测：
- `[J]` - 期刊论文
- `[M]` - 专著
- `[D]` - 学位论文
- `[C]` - 会议论文
- `[R]` - 研究报告
- `[Z]` - 标准

### 2. 引用标记插入算法

基于关键词匹配的智能插入：

```python
# 定义引用映射规则
citation_rules = [
    {'keywords': ['核心系统', 'Core Banking'], 'ref_ids': [2, 3, 4, 5]},
    {'keywords': ['DevOps', '持续交付'], 'ref_ids': [9, 10, 11, 12]},
    # ...
]
```

插入策略：
1. 扫描论文正文，识别关键概念
2. 匹配相关文献
3. 在句子末尾插入引用标记
4. 避免重复插入

### 3. 字数统计算法

```python
def count_words(text):
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return chinese_chars + english_words
```

中文字符数 + 英文单词数 = 总字数

### 4. Markdown转Word算法

使用docx-js库生成Word文档：

1. 解析Markdown为结构化数据
2. 识别标题层级（H1-H4）
3. 处理引用标记为上标格式
4. 生成符合OOXML标准的.docx文件

## 文件格式说明

### references.json 结构

```json
[
  {
    "id": 1,
    "raw": "作者. 标题[J]. 期刊, 年份(期): 页码.",
    "type": "journal",
    "authors": "作者",
    "title": "标题",
    "year": 2023
  }
]
```

### abstracts.json 结构

```json
[
  {
    "id": 1,
    "raw": "原始引用",
    "type": "journal",
    "citation_count": 5,
    "contexts": ["引用上下文1", "引用上下文2"],
    "keywords": ["关键词1", "关键词2"]
  }
]
```

## 扩展方法

### 添加新的引用规则

在 `insert_citations_enhanced.py` 中的 `citation_rules` 列表添加：

```python
{'keywords': ['新关键词'], 'ref_ids': [文献ID1, 文献ID2]}
```

### 修改扩充内容

在 `expand_paper.py` 中的 `expansion` 变量修改或添加附录内容。

### 自定义Word样式

在 `md_to_docx_final.py` 中修改 `generate_docx_js` 函数中的样式配置。

## 常见问题

### Q: 引用标记插入位置不准确？

A: 可以调整 `citation_rules` 中的关键词，或手动在Markdown中插入 `[n]` 标记。

### Q: 字数扩充后内容重复？

A: 修改 `expand_paper.py` 中的扩充内容，添加更多原创性内容。

### Q: Word格式与学校要求不符？

A: 修改 `md_to_docx_final.py` 中的样式配置，包括字体、字号、行距等。

## 性能优化建议

1. 对于大型论文（>10万字），建议分段处理
2. 参考文献超过200条时，考虑使用数据库存储
3. 批量处理多篇论文时，可使用并行处理
