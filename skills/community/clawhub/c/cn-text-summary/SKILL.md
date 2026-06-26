---
slug: cn-text-summary
name: 文本摘要生成器
description: "cn-text-summary。纯Python标准库，无需API Key。"
keywords: text, summary
version: "1.0.0"
author: 千策
---


# 文本摘要提取器

从长文本中智能提取核心内容，生成简洁摘要。

## 功能

- **智能摘要**：自动识别文章核心观点，生成精炼摘要
- **关键词提取**：从文本中提取TOP关键词
- **字数控制**：支持指定摘要长度（短/中/长）
- **多场景**：支持新闻、论文、邮件、产品描述等

## 使用方法

```bash
# 基本摘要
python3 cn_text_summary.py

# 提取关键词
python3 cn_text_summary.py --keywords

# 短摘要模式
python3 cn_text_summary.py --length short
```

## 交互模式

直接输入或粘贴文本，自动生成摘要。

## 依赖

- Python 3.x
- jieba (pip install jieba) - 仅中文分词需要

## 示例

输入：介绍人工智能发展历程的长文
输出：人工智能经历了三次浪潮...（摘要内容）

输入：产品发布会新闻稿
输出：某公司发布新产品...（关键词+摘要）

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
