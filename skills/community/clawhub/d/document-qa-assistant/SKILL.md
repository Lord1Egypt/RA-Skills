---
name: document-qa-assistant
description: 文档问答助手。基于本地文档（PDF/Word/Markdown/TXT）回答问题，支持知识库检索和多文档交叉验证。当用户需要：从文档中查找答案、基于文档回答问题、跨多个文档综合查询、验证信息一致性、生成文档摘要时使用此技能。
---

# Document QA Assistant

文档问答助手。基于本地文档回答问题，支持多文档检索和交叉验证。

## 核心能力

1. **文档解析** — 支持 PDF、Word、Markdown、TXT、CHM
2. **语义检索** — 基于内容理解回答问题，不依赖关键词匹配
3. **多文档交叉** — 跨多个文档综合答案
4. **答案溯源** — 指出答案来自哪个文档的第几部分

## 快速开始

### 问答

```bash
python3 scripts/doc_qa.py --docs "./docs/" --question "这个产品的价格是多少"
```

### 批量索引文档

```bash
python3 scripts/index_docs.py --dir "./knowledge-base/" --output ./index.json
```

## 脚本说明

### scripts/doc_qa.py

基于文档回答问题。

```bash
python3 scripts/doc_qa.py --docs <文档路径> --question "<问题>" [--context-len <行数>]
```

**参数：**
- `--docs`: 文档文件或目录路径
- `--question`: 要回答的问题
- `--context-len`: 参考上下文行数（默认 20）

### scripts/index_docs.py

批量索引文档供后续检索。

```bash
python3 scripts/index_docs.py --dir <目录> --output <输出索引文件>
```

## 典型场景

### 从知识库中查找答案
```bash
python3 scripts/doc_qa.py \
  --docs "./knowledge-base/metaworks/" \
  --question "微应用开发需要哪些前置条件"
```

### 生成文档摘要
```bash
python3 scripts/doc_qa.py \
  --docs "./docs/product-guide.pdf" \
  --question "请用100字总结这份文档的核心内容"
```

### 跨文档验证信息
```bash
python3 scripts/doc_qa.py \
  --docs "./docs/v1/,./docs/v2/" \
  --question "两个版本的配置方式有什么不同"
```

## 输出格式

```json
{
  "answer": "答案内容...",
  "sources": [
    {
      "file": "文档路径",
      "relevance": 0.95,
      "excerpt": "相关段落..."
    }
  ],
  "confidence": "high|medium|low"
}
```
