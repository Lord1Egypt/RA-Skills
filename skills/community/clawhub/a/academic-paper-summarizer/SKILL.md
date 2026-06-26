# academic-paper-summarizer

学术论文摘要技能，快速提取论文核心内容。

## 功能
- PDF 解析
- 核心观点提取
- 方法总结
- 结论概括
- 关键数据提取
- 通俗化解释

## 依赖
- Python 3.8+
- pypdf
- pdfplumber

## 使用
```python
# 总结论文
python skills/academic-paper-summarizer/scripts/summarize.py \
  --input paper.pdf \
  --output summary.md \
  --length "medium"

# 批量处理
python skills/academic-paper-summarizer/scripts/batch.py \
  --input-dir papers/ \
  --output-dir summaries/

# 提取关键数据
python skills/academic-paper-summarizer/scripts/extract.py \
  --paper paper.pdf \
  --fields ["method", "results", "conclusion"]
```

## 输出格式
```markdown
# 论文摘要

## 基本信息
- 标题：XXX
- 作者：XXX
- 期刊：XXX
- 年份：2026

## 核心问题
研究要解决什么问题？

## 方法
采用了什么方法？

## 主要发现
关键数据和结论

## 局限性
研究的不足之处

## 通俗解释
用大白话解释研究内容
```

## 注意事项
- 支持中英文论文
- 保持学术严谨性
