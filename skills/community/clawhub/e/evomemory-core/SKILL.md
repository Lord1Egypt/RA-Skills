# EvoMemory Core - Evolutionary Local Memory System
## Skill Metadata
- **Name**: EvoMemory Core - Evolutionary Local Memory System
- **Version**: 1.0.0
- **Author**: Evolution Memory Team
- **Description (English)**: Full-stack evolutionary local memory system for AI Agents, supports dual backend (ChromaDB/LanceDB), hybrid RAG retrieval, semantic deduplication, auto-classification, 100% offline operation.
- **Description (中文)**: 面向AI Agent的全栈进化版本地记忆系统，支持ChromaDB/LanceDB双后端、混合RAG检索、语义去重、自动分类，100%离线运行。
- **Category**: memory, system, rag, core
- **Tags**: memory-system, local-memory, evolutionary, evo, rag, hybrid-search, offline, openclaw
- **Compatibility**: OpenClaw >= 2026.3.22
- **License**: MIT
- **Homepage**: https://clawhub.ai/lulan3954-a11y/evomemory-core

## Features (English)
- 🧬 Full evolutionary memory system architecture, not just a single vector store
- 🔄 Dual backend support (ChromaDB/LanceDB), switch freely according to needs
- 🎯 Triple hybrid RAG retrieval (keyword + semantic + knowledge graph), accuracy improved by 40%
- 🧹 Built-in semantic deduplication, auto-classification, incremental sync capabilities
- 💻 GPU accelerated BGE-M3 Chinese semantic vector optimization, Chinese retrieval accuracy +30%
- ⚡ One-click deployment, zero configuration, out of the box
- 🔒 100% offline operation, no third-party API required, all data stored locally
- 📤 Compatible with OpenClaw native memory interface, zero code migration for existing projects

## 功能特性 (中文)
- 🧬 完整进化型记忆系统架构，不仅仅是单一向量存储
- 🔄 双后端支持(ChromaDB/LanceDB)，可根据需求自由切换
- 🎯 三重混合RAG检索(关键词+语义+知识图谱)，准确率提升40%
- 🧹 内置语义去重、自动分类、增量同步能力
- 💻 GPU加速BGE-M3中文语义向量优化，中文检索准确率+30%
- ⚡ 一键部署，零配置开箱即用
- 🔒 100%离线运行，无需第三方API，所有数据本地存储
- 📤 兼容OpenClaw原生记忆接口，现有项目零代码迁移

## Usage
### Installation
```bash
# Windows
install.bat

# Linux/macOS
chmod +x install.sh && ./install.sh
```

### Quick Start
1. After installation, memory system is enabled by default
2. Use `evomemory help` to view all available commands
3. Run `evomemory migrate` to import existing memory data
4. Configure advanced options in `config.yaml`

## Dependencies
- chromadb >= 0.4.0
- lancedb >= 0.5.0
- sentence-transformers >= 2.2.0
- pyyaml >= 6.0
- jieba >= 0.42.1
