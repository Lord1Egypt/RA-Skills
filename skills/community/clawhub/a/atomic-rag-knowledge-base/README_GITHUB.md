# 🎓 Atomic RAG Knowledge Base Builder

> **The Best Open-Source Atomic Knowledge Base Builder for RAG**  
> Make AI truly *learn* a book, rather than just *read* it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-green.svg)]()
[![STEM](https://img.shields.io/badge/STEM-Math%20Physics%20Chemistry%20Medicine-orange.svg)]()

[中文介绍](#中文介绍) | [English](#english-introduction)

---

## 🎯 One-Line Introduction

**中文**: 让AI真正"学会"一本书而非只是"看过"——采用原子化方法构建RAG知识库，使AI能够理解、融会贯通、举一反三。

**English**: Make AI truly "learn" a book rather than just "read" it — Build RAG knowledge bases using atomic methods, enabling AI to understand, synthesize, and apply knowledge flexibly.

---

## 📖 Why We Built This?

### The 4 Pain Points of Traditional RAG

| Pain Point | Traditional Method | Our Atomic Solution |
|------------|-------------------|---------------------|
| **Hard Cut** | Split by 600-800 chars, breaking knowledge | Split by knowledge integrity |
| **U-shaped Attention** | LLMs only remember 10% of 1M context | Load only relevant atoms |
| **Knowledge≠Ability** | AI can recite but can't solve problems | Extract executable methodologies |
| **STEM Blind Spots** | Formulas, charts, derivations ignored | Specialized parsers for STEM |

---

## ✨ Core Features

### 🇨🇳 中文特性

- 🔬 **原子化拆分** - 按知识完整性而非字数硬性切割
- 📚 **方法论提炼** - 从描述性内容提取可执行方法
- 🧮 **理工农医特化** - 数学公式LaTeX、物理模型、化学反应式、医学诊断逻辑专业处理
- 🔍 **多路召回** - 向量检索 + 关键词检索 + 知识图谱三重保障
- 🔄 **HERMES集成** - 支持动态学习循环，使用越多越精准

### 🇬🇧 English Features

- 🔬 **Atomic Chunking** - By knowledge integrity, not word count
- 📚 **Methodology Extraction** - Extract executable methods from text
- 🧮 **STEM Specialized** - LaTeX formulas, physics models, chemical equations, medical diagnosis
- 🔍 **Multi-Recall** - Vector + Keyword + Knowledge Graph
- 🔄 **HERMES Integration** - Dynamic learning loop

---

## 🚀 Quick Start

```python
from atomic_rag import AtomicRAGBuilder

# Initialize builder (Math domain)
builder = AtomicRAGBuilder(domain="math")

# Process PDF
atoms = builder.process_pdf("calculus.pdf")

# Store to vector DB
builder.store_to_vector_db(atoms, collection_name="math_kb")

print(f"✅ Built {len(atoms)} knowledge atoms")
```

### RAG Q&A

```python
from atomic_rag import MultiRecallRAG

rag = MultiRecallRAG()
answer = rag.ask("How to solve quadratic equations?")
print(answer)
```

---

## 📚 The Atomic Five-Step Method

```
Step 1: Format Conversion (Eliminate visual blind spots)
Step 2: Semantic Chunking (By knowledge integrity)
Step 3: Methodology Extraction (Keep methods, remove stories)
Step 4: Metadata Extraction (Multi-dimensional tags)
Step 5: Vector Storage (Ready for retrieval)
```

---

## 🎓 STEM Specialized Processing

### Mathematics
- ✅ LaTeX formula extraction
- ✅ Proof step recognition
- ✅ Theorem/definition annotation

### Physics
- ✅ Physics model extraction
- ✅ Formula derivation preservation
- ✅ Applicable conditions annotation

### Chemistry
- ✅ Chemical equation recognition
- ✅ Reaction mechanism analysis
- ✅ Condition parameter recording

### Medicine
- ✅ Diagnosis logic extraction
- ✅ Treatment plan structuring
- ✅ Differential diagnosis annotation

---

## 💡 Use Cases

| Scenario | Application |
|----------|-------------|
| 📖 Personal Knowledge Base | Convert books to searchable knowledge |
| 🏢 Enterprise KM | Atomic management of SOPs and manuals |
| 🎓 Education | Personalized learning with textbooks |
| 🔬 Research | Extract core methods from papers |
| 🤖 AI Agents | Inject professional knowledge |

---

## 📊 Performance Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Atom Extraction | >95% | No knowledge loss |
| Methodology Accuracy | >90% | Correct executable methods |
| Retrieval Recall | >85% | Relevant knowledge found |
| Processing Speed | 50 pages/min | PDF processing efficiency |

---

## 🔗 Related Links

- 🌐 **ClawHub Skill**: [Search "atomic-rag" on ClawHub](https://clawhub.io)
- 📚 **Documentation**: [SKILL.md](./SKILL.md)
- 🎓 **Education Platform**: [XueLaiXueQu](https://xuelaixuequ.com)

---

## 👥 Team

**XueLaiXueQu Learning Community** - Making AI truly learn

---

## 📜 License

MIT License - Free to use, welcome contributions!

---

*Made with ❤️ by XueLaiXueQu AI Team*
