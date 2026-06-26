# 🧠 Enterprise Async Memory Engine
### OpenClaw 企业级长期记忆中间件 (v1.1.1)

[![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-green.svg)]()
[![Framework](https://img.shields.io/badge/framework-OpenClaw-orange.svg)]()

**Enterprise Async Memory Engine** 是专为 OpenClaw 架构设计的 RAG (Retrieval-Augmented Generation) 增强插件。通过高性能异步向量检索技术，该引擎旨在突破大语言模型 (LLM) 上下文窗口的物理限制，赋予 Agent 具备**持久化**、**语义化**与**自我进化**能力的长期记忆中枢。

---

## ✨ 核心特性 (Core Features)

### 🚀 高性能检索架构 (Retrieval Engine)
*   **⚡ 异步非阻塞 (Async-First)**: 基于线程池的计算分离机制，确保向量 Embedding 与相似度计算不阻塞 OpenClaw 主逻辑，完美支持高并发对话场景。
*   **🧬 深度语义匹配 (Semantic RAG)**: 集成 `Sentence-modules` 与 `BGE` 顶级模型，利用余弦相似度 (Cosine Similarity) 实现跨语境的语义关联，有效抑制模型幻觉。
*   **🎯 智能上下文注入 (Context Injection)**: 通过 `get_context()` 接口实现动态 Context 组装，精准地将最相关的知识片段（Chunks）实时注入 LLM Prompt。

### 🧠 智能记忆管理 (Memory Management)
*   **📦 轻量化持久化**: 采用高效序列化机制，实现记忆的“随聊随存，重启不丢”，极低地维护成本。
*   **🧹 自适应容量控制 (Self-Evolving)**: 内置**权重淘汰策略**，基于置信度与时间戳动态清理低价值条目，确保向量库始终保持高信息密度。
    $$\text{Priority} = \alpha \cdot \text{Confidence} + \beta \cdot \text{Recency}$$
*   **🔒 高置信度写入机制**: 引入阈值校验（Threshold Validation），仅允许高置信度知识沉淀入库，从源的头防止噪声污染。

### 🛠️ 开发者友好 (Developer Experience)
*   **📝 零侵入式指令集**: 原生支持 `[MEMORY: {...}]` JSON 格式指令，LLM 即可通过自然语言实现知识的增、删、改。
*   **⚙️ 配置热驱动 (Hot-Reload)**: 支持 `memory_config.yaml` 运行时动态加载，无需重启服务即可实时调整检索阈值或模型参数。
*   **🇨🇳 中文生态优化**: 深度适配 `BAAI/bge-small-zh-v1.5` 等中文语义模型，在中文语义理解上具备卓越表现。

---

## 📂 项目结构 (Project Structure)

```text
enterprise-memory-skill/
├── config.json                # 插件入口配置文件 (OpenClaw 识别用)
├── memory_config.yaml         # 记忆引擎运行时超参数 (阈值、容量、模型)
├── prompts.md                 # 记忆指令的系统提示词规范 (LLM Instruction Set)
├── main_skill.py              # 核心执行逻辑 (OpenClaw 接口层)
├── vectorstorage.py           # 核心引擎 (向量计算、RAG 检索、持久化)
├── __init__.py                # 模块导出声明
└── README.md                  # 项目说明文档
```

---

## ⚙️ 安装与部署 (Installation & Setup)

### 1. 环境要求
*   **Python**: 3.11 或 3.12 (推荐)
*   **依赖库**: `sentence-transformers`, `torch`, `numpy`, `pyyaml`

### 2. 部署流程
1.  **放置插件**: 将整个 `enterprise-memory-skill` 文件夹拷贝至 OpenClaw 工作空间的 `skills/` 目录下。
2.  **安装依赖**:
    ```bash
    pip install sentence-layers torch numpy pyyaml
    ```
3.  **激活插件**: 在 OpenClaw 终端执行命令：
    ```bash
    /reload_skills
    ```
    > **验证成功标志**: 若日志显示 `✅ VectorStorage initialized successfully.` 则表示部署成功。

---

## 🛠️ 配置指南 (Configuration)

通过修改 `memory_config.yaml` 实现对记忆行为的精细化调控：

```yaml
# --- 检索策略 (Retrieval Strategy) ---
storage_confidence: 0.7      # 知识入库的最低置信度阈值 (0-1)
retrieint_threshold: 0.82    # 检索召回的最低相似度阈值
retrieval_top_k: 5           # 每次检索返回的最相关条目数

# --- 容量管理 (Capacity Management) ---
max_memory_entries: 2000     # 向量库最大容量限制 (触发自动清理)
max_history_entries: 20      # 短期对话上下文保留条数

# --- 存储与模型 (Storage & Model) ---
db_path: "data/memory/vectors.db"           # 向量数据库持久化路径
embedding_model_name: "BAAI/bge-small-zh-v1.5" # 推荐使用中文 BGE 模型
enable_logging: true
```

---

## 📖 使用场景 (Usage)

### 模式一：Agent 自动记忆 (推荐/零代码)
无需编写额外代码。只需在 Agent 的 `[MAIN_AGENT_PROMPT]` 末尾添加 `prompts.md` 中的指令集。LLM 会在对话中自动识别关键信息并触发 JSON 指令。

*   **新增知识**:
    `[MEMORY: {"action": "ADD_MEMORY", "content": "OpenClaw 支持插件化扩展", "confidence": 0.95}]`
*   **纠错/清理**:
    `[MEMORY: {"action": "REJECT_MEMORY", "content": "旧的错误观点", "reason": "用户已更新配置"}]`

### 模式二：API 程序化调用 (集成开发)
您可以直接在 OpenClaw 的其他自定义 Skill 或 Hook 中调用引擎接口。

```python
# 1. 自动化注入长期记忆
memory_skill.execute_action("remember", {
    "text": "项目截止日期是 2//24 年 12 月 31 日。",
    "confidence": 0.98,
    "metadata": {"category": "project_deadline"}
})

# 2. 语义化检索上下文
# 传入用户问题，返回最相关的历史记忆片段
context = memory_skill.get_context("项目什么时候结束？")
```

---

## 🛡️ 健壮性与降级策略 (Robustness)

*   **自动降级 (Auto-Fallback)**: 若 Embedding 模型加载失败或显存不足，系统将自动切换至 **"空检索模式"**，确保主对话流程不中断，仅作为普通文本处理。
*   **异常拦截 (Error Interception)**: 所有的向量计算异常（如维度不匹配）均会被捕获并记录至系统日志，防止导致 OpenClaw 核心进程崩溃。
*   **数据校验 (Data Integrity)**: 在执行写入操作前，强制进行 **JSON Schema 校验**，确保记忆数据的结构完整性与类型安全。

---
