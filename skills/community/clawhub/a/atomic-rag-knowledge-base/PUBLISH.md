# 🎓 Atomic RAG Knowledge Base Builder | 原子化RAG知识库构建器

> **学来学去学习社专属工具** | The Exclusive Tool of XueLaiXueQu Learning Community

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-green.svg)]()
[![Education](https://img.shields.io/badge/Education-STEM%20Optimized-orange.svg)]()

---

## 🌍 一句话介绍 | One-Line Introduction

**中文**: 让AI真正"学会"一本书而非只是"看过"——采用原子化方法构建RAG知识库，使AI能够理解、融会贯通、举一反三。

**English**: Make AI truly "learn" a book rather than just "read" it — Build RAG knowledge bases using atomic methods, enabling AI to understand, synthesize, and apply knowledge flexibly.

---

## 🎯 为什么创建这个工具？| Why We Built This?

### 传统RAG的四大痛点 | Four Pain Points of Traditional RAG

| 痛点 Pain Point | 传统方法 Traditional | 我们的方案 Our Solution |
|----------------|-------------------|------------------------|
| 1. **硬切问题 Hard Cut** | 按600-800字机械分割，知识点断裂 | 按知识完整性原子化拆分 |
| 2. **U型注意力 U-shaped Attention** | 100万上下文只记住10%，精华丢失 | 精准加载相关原子单元 |
| 3. **知识≠能力 Knowledge≠Ability** | AI能复述概念但不会解决问题 | 提炼方法论，知识转化为能力 |
| 4. **理工农医盲区 STEM Blind Spots** | 公式、图表、推导被忽略 | 专业解析器完整保留 |

---

## ✨ 核心特性 | Core Features

### 🇨🇳 中文介绍

- 🔬 **原子化拆分** - 按知识完整性而非字数硬性切割
- 📚 **方法论提炼** - 从描述性内容提取可执行方法，知识转化为能力
- 🧮 **理工农医特化** - 数学公式LaTeX、物理模型、化学反应式、医学诊断逻辑专业处理
- 🔍 **多路召回** - 向量检索 + 关键词检索 + 知识图谱三重保障
- 🔄 **HERMES集成** - 支持动态学习循环，使用越多越精准
- 📖 **教育场景优化** - 专为学习场景设计，支持难度分级、前置知识关联

### 🇬🇧 English Introduction

- 🔬 **Atomic Chunking** - Split by knowledge integrity, not word count
- 📚 **Methodology Extraction** - Extract executable methods from descriptive text
- 🧮 **STEM Specialized** - LaTeX formulas, physics models, chemical equations, medical diagnosis logic
- 🔍 **Multi-Recall** - Vector + Keyword + Knowledge Graph triple retrieval
- 🔄 **HERMES Integration** - Dynamic learning loop, improves with usage
- 📖 **Education Optimized** - Designed for learning scenarios with difficulty levels and prerequisite mapping

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
git clone https://github.com/xuelai-xuequ/atomic-rag-knowledge-base.git
cd atomic-rag-knowledge-base
pip install -r requirements.txt
```

### 基础用法 | Basic Usage

```python
from atomic_rag import AtomicRAGBuilder

# 初始化构建器（数学领域）| Initialize builder (Math domain)
builder = AtomicRAGBuilder(domain="math")

# 处理PDF | Process PDF
atoms = builder.process_pdf(
    file_path="高等数学.pdf",
    metadata={
        "title": "高等数学",
        "author": "同济大学",
        "subject": "数学"
    }
)

# 存储到向量数据库 | Store to vector DB
builder.store_to_vector_db(atoms, collection_name="math_kb")

print(f"✅ 已构建 {len(atoms)} 个知识原子 | Built {len(atoms)} knowledge atoms")
```

### RAG问答 | RAG Q&A

```python
from atomic_rag import MultiRecallRAG

rag = MultiRecallRAG()

# 中文提问 | Chinese Query
answer = rag.ask("如何求解一元二次方程？")

# 英文提问 | English Query
answer = rag.ask("How to solve quadratic equations?")

print(answer)
```

---

## 📚 原子化五步法 | The Atomic Five-Step Method

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 格式转化 Format Conversion                      │
│  Step 2: 语义分段 Semantic Chunking                      │
│  Step 3: 方法论提炼 Methodology Extraction               │
│  Step 4: 元数据提取 Metadata Extraction                  │
│  Step 5: 向量化存储 Vector Storage                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎓 理工农医专业处理 | STEM Specialized Processing

### 数学 Mathematics
- ✅ LaTeX公式提取与解析
- ✅ 证明步骤识别与结构化
- ✅ 定理/定义/公理自动标注

### 物理 Physics
- ✅ 物理模型提取（理想气体、简谐运动等）
- ✅ 公式推导过程完整保留
- ✅ 适用条件与临界值标注

### 化学 Chemistry
- ✅ 化学反应式识别（→ = ⇌）
- ✅ 反应机理解析（中间体、过渡态）
- ✅ 反应条件记录（温度、压力、催化剂）

### 医学 Medicine
- ✅ 诊断逻辑提取（症状→体征→检查→诊断）
- ✅ 治疗方案结构化（药物/剂量/疗程）
- ✅ 鉴别诊断标注

---

## 💡 适用场景 | Use Cases

| 场景 Scenario | 应用 Application |
|--------------|-----------------|
| 📖 **个人知识库** Personal KB | 将阅读过的书籍转化为可检索知识 |
| 🏢 **企业知识管理** Enterprise KM | SOP、手册、培训资料原子化管理 |
| 🎓 **教育内容建设** Education | 教材、题库个性化学习 |
| 🔬 **研究资料整理** Research | 论文、专利核心方法提取 |
| 📚 **在线教育平台** EdTech | 构建智能答疑系统 |
| 🤖 **AI Agent开发** AI Agents | 为Agent注入专业知识 |

---

## 📊 性能指标 | Performance Metrics

| 指标 Metric | 目标值 Target | 说明 Description |
|------------|--------------|-----------------|
| 原子提取完整率 | >95% | 知识点不丢失 |
| 方法论提炼准确率 | >90% | 正确识别可执行方法 |
| 检索召回率 | >85% | 相关知识能找回 |
| 回答准确率 | >80% | 基于知识库的回答正确 |
| 处理速度 | 50页/分钟 | PDF处理效率 |

---

## 🏗️ 项目结构 | Project Structure

```
atomic-rag-knowledge-base/
├── 📄 README.md                    # 项目说明
├── 📄 SKILL.md                     # 技能定义文档
├── 📄 PUBLISH.md                   # 发布文档
├── 📄 requirements.txt             # Python依赖
│
├── 🔧 atomic_rag/                  # 核心代码
│   ├── __init__.py
│   ├── builder.py                  # 知识库构建器
│   ├── rag.py                      # RAG检索引擎
│   └── processors/                 # 领域处理器
│       ├── __init__.py
│       ├── math.py                 # 数学处理器
│       ├── physics.py              # 物理处理器
│       ├── chemistry.py            # 化学处理器
│       └── medicine.py             # 医学处理器
│
├── 📖 examples/                    # 使用示例
│   ├── math_example.py
│   └── physics_example.py
│
└── 🧪 tests/                       # 测试
    └── test_builder.py
```

---

## 🔑 关键词 | Keywords

### 中文关键词
RAG知识库、原子化拆分、PDF解析、向量数据库、知识图谱、教育AI、智能学习、理工农医、数学公式、化学方程式、医学诊断、方法论提炼、语义分段、HERMES学习循环、学来学去

### English Keywords
RAG, Knowledge Base, Atomic Chunking, PDF Parser, Vector Database, Knowledge Graph, Educational AI, Intelligent Learning, STEM, LaTeX Formula, Chemical Equation, Medical Diagnosis, Methodology Extraction, Semantic Chunking, HERMES Learning Loop, XueLaiXueQu

### 技术栈关键词
Python, LangChain, OpenAI, Milvus, Chroma, Pinecone, Embeddings, NLP, OCR, Text Processing, Machine Learning

---

## 🤝 谁在使用？| Who's Using It?

- 🎓 **学来学去学习社** - 中小学AI智能学习平台
- 📚 **个人知识管理** - 将阅读书籍转化为可检索知识库
- 🏢 **企业培训** - 内部知识库构建
- 🔬 **学术研究** - 论文专利核心方法提取

---

## 🛣️ 路线图 | Roadmap

- [x] v1.0.0 - 基础功能：PDF解析、原子化拆分、向量存储
- [x] v1.0.0 - 领域特化：数学/物理/化学/医学处理器
- [x] v1.0.0 - RAG检索：多路召回、上下文组装
- [ ] v1.1.0 - 知识图谱：自动构建知识图谱
- [ ] v1.2.0 - HERMES集成：动态学习循环
- [ ] v1.3.0 - 多语言支持：英文PDF优化
- [ ] v2.0.0 - 可视化界面：Web UI管理后台

---

## 👥 团队 | Team

**学来学去学习社** | XueLaiXueQu Learning Community

- 🌸 **菲菲老师** - 教育心理学专家、亲子教育专家
- 🔬 **浩云学长** - STEM教育专家、AI技术负责人
- 💹 **西蒙斯** - 系统架构师、量化策略专家
- ⚙️ **贾维斯** - 首席代码工程师

---

## 📜 许可证 | License

MIT License - 自由使用，欢迎贡献！

---

## 🌟 贡献指南 | Contributing

欢迎提交Issue和PR！让我们一起打造**全网最好的开源专属知识库建立技能**！

---

## 📞 联系我们 | Contact

- 📧 Email: contact@xuelaixuequ.com
- 🌐 Website: https://xuelaixuequ.com
- 💬 WeChat: 学来学去学习社

---

*Made with ❤️ by 学来学去学习社AI团队*

**让AI真正学会一本书，而非只是看过。**
*Make AI truly learn a book, rather than just read it.*
