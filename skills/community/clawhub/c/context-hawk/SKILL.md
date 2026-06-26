# 🦅 Context-Hawk — AI 记忆守护者

> **纯 Python 记忆包，零外部依赖，零 API Key，直接 import 就能用**

*让任何 Python 项目或 AI Agent 拥有记忆能力——跨会话、跨话题、跨时间。*

---

## 定位

**纯 Python 包，可独立使用**

- 不需要 OpenClaw，不需要 API Key
- `pip install` 后直接 `from hawk.memory import MemoryManager`
- 可嵌入任何 Python 项目（AI Agent、脚本、爬虫等）

**配合 hawk-bridge 使用时**，hawk-bridge 负责 autoCapture/autoRecall Hook，context-hawk 提供底层 Python 核心。

---

## 核心模块

| 模块 | 功能 | API Key |
|------|------|---------|
| `MemoryManager` | 四层记忆衰减（Working/Short/Long/Archive） | ❌ |
| `ContextCompressor` | 上下文压缩，按 token 限制 | ❌ |
| `Config` | 配置管理 | ❌ |
| `SelfImproving` | 自我反思，错误模式学习 | ❌ |
| `VectorRetriever` | 向量语义检索（LanceDB） | ❌* |
| `MarkdownImporter` | 导入 .md 记忆文件 | ❌* |
| `Extractor` | 记忆提取（6类分类） | ⚠️ 可选 |
| `Governance` | 系统巡检指标 | ❌ |

*VectorRetriever 和 MarkdownImporter 需要 LanceDB（免费本地）*

---

## 安装

```bash
pip install lancedb
```

不需要任何 API Key，纯本地运行。

---

## 快速开始

```python
from hawk.memory import MemoryManager

# 创建记忆管理器
mm = MemoryManager()

# 存入记忆
mm.store("用户喜欢简洁的回复风格", category="preference")
mm.store("公司叫趣近团队", category="entity")
mm.store("老板决定用Go语言重构", category="decision")

# 检索记忆
results = mm.recall("老板的风格偏好")
for r in results:
    print(f"{r.layer}: {r.text}")

# 查看统计
print(mm.get_stats())
# {'working': 2, 'short': 1, 'long': 0, 'archive': 0, 'total': 3, 'avg_importance': 0.65}
```

---

## MemoryManager — 四层记忆

```
Working → Short → Long → Archive
  ↑                    ↓
  ←──── Weibull 衰减 ←←←
```

```python
from hawk.memory import MemoryManager

mm = MemoryManager()

# 存入，指定重要程度（0.0-1.0）
mm.store("这是重要决策", category="decision", importance=0.9)
mm.store("普通信息", category="fact", importance=0.4)

# 触发衰减（清理低价值记忆）
mm.decay()

# 访问记忆（更新计数器，可能触发层级升级）
item = mm.access("memory_id")
print(f"访问次数: {item.access_count}")
```

---

## VectorRetriever — 向量语义检索

需要先设置 `OPENAI_API_KEY`（可选，用于 embedding）

```python
from hawk.vector_retriever import VectorRetriever

retriever = VectorRetriever(top_k=5, min_score=0.6)

# 检索相关记忆
chunks = retriever.recall("老板之前部署过哪些服务")
print(retriever.format_for_context(chunks))
```

**输出：**
```
🦅 [记忆检索结果]
[entity] (85%相关): 趣近团队的服务器部署在阿里云
[fact] (72%相关): 生产环境用 Docker Compose 管理
```

---

## MarkdownImporter — 导入 .md 记忆文件

一键把已有的 `.md` 记忆文件导入向量库：

```python
from hawk.markdown_importer import MarkdownImporter

importer = MarkdownImporter(memory_dir="~/.openclaw/memory")

# 扫描预览
chunks = importer.scan()
print(f"发现 {len(chunks)} 个记忆块")

# 一键导入（增量，已导入的打标签跳过）
result = importer.import_all()
print(f"导入完成: {result['files']} 个文件, {result['chunks']} 个块")
```

**CLI：**
```bash
python3.12 -m hawk.markdown_importer --dry-run   # 预览
python3.12 -m hawk.markdown_importer             # 实际导入
```

---

## ContextCompressor — 上下文压缩

按 token 限制压缩对话历史：

```python
from hawk.compressor import ContextCompressor

compressor = ContextCompressor(max_tokens=4000)

conversation = [
    {"role": "user", "content": "我们要做XX项目"},
    {"role": "assistant", "content": "好的，我来规划"},
    # ... 100 轮对话
]

result = compressor.compress(conversation)
print(f"压缩率: {result['compression_ratio']}")
print(result['compressed'])
```

---

## Extractor — 记忆提取

**零 API 模式（关键词提取，完全离线）：**
```python
from hawk.extractor import extract_memories

text = "用户说他喜欢用Go语言，公司叫趣近团队，决定用Docker部署"
memories = extract_memories(text, provider="keyword")
# 不需要任何 API Key
```

**有 API Key 时（LLM 6类分类，更精准）：**
```python
# 设置环境变量
import os
os.environ["OPENAI_API_KEY"] = "sk-xxx"
# 或
os.environ["MINIMAX_API_KEY"] = "sk-cp-xxx"

memories = extract_memories(text, provider="openai")
# 或
memories = extract_memories(text, provider="minimax",
                            api_key="sk-cp-xxx",
                            model="MiniMax-M2.7",
                            base_url="https://api.minimaxi.com/anthropic")
```

**输出示例：**
```python
[
  {"text": "喜欢用Go语言", "category": "preference", "importance": 0.8, "abstract": "用户偏好Go", "overview": "[preference] 喜欢用Go语言"},
  {"text": "公司叫趣近团队", "category": "entity", "importance": 0.9, "abstract": "公司名称", "overview": "[entity] 公司叫趣近团队"},
  {"text": "决定用Docker部署", "category": "decision", "importance": 0.95, "abstract": "部署决策", "overview": "[decision] 决定用Docker部署"}
]
```

---

## SelfImproving — 自我反思

```python
from hawk.self_improving import SelfImproving

si = SelfImproving()

# 记录错误
si.learn_from_error(
    error_type="recall_miss",
    context={"query": "老板上次说的项目", "results": []},
    correction="改进了检索关键词策略"
)

# 获取统计
print(si.get_stats())
# {'total': 1, 'resolved': 0, 'unresolved': 1, 'by_type': {'recall_miss': 1}}

# 获取未解决的问题
unresolved = si.get_unresolved()
for u in unresolved:
    print(f"待解决: {u.error_type} - {u.context}")
```

---

## Governance — 系统巡检

```python
from hawk.governance import Governance

gov = Governance()

# 记录指标
gov.log_extraction(total=10, stored=3, skipped=7)
gov.log_noise_filter(filtered_count=2, total=10)
gov.log_recall(hits=2, total=5)

# 查看24小时统计
stats = gov.get_stats(hours=24)
print(stats)
# {'extractions': 10, 'noise_filtered': 2, 'recalls': 5, 'recall_hits': 2, ...}
```

---

## HawkContext — autoCapture + autoRecall 包装器

HawkContext 是一个 Python 上下文管理器，包装 LLM 调用，自动实现：
- **autoRecall**：对话开始时自动检索相关记忆并注入上下文
- **autoCapture**：对话结束时自动提取记忆存入 LanceDB

```python
from hawk import HawkContext

# 初始化（自动从环境变量读取配置）
hawk = HawkContext(
    provider="minimax",      # minimax | openai | groq | ollama | keyword
    api_key="sk-cp-xxx",
    model="MiniMax-M2.7"
)

# 对话开始时自动 recall
# 对话结束时（with 块退出时）自动 capture
with hawk:
    response = hawk.chat(
        "老板之前用什么技术栈？",
        system_prompt="你是一个助手"
    )
    print(response)

# 也可以手动控制
hawk.recall("用户的项目偏好")
hawk.capture()
```

**自动 recall 机制：**
- `hawk.recall()` 在 `hawk.chat()` 内部被调用
- 检索当前用户消息相关的记忆
- 结果自动插入 LLM 消息中

**支持 provider：**
| provider | API Key | 说明 |
|----------|---------|------|
| minimax | 需要 | MiniMax-M2.7（推荐） |
| openai | 需要 | GPT-4o 等 |
| groq | 不需要 | 免费 Llama-3 |
| ollama | 不需要 | 本地模型 |
| keyword | 不需要 | 纯规则提取 |

**配置优先级：**
1. 显式传参 > 环境变量 > 默认值

---

## 与 hawk-bridge 的关系

| | context-hawk | hawk-bridge |
|---|---|---|
| **定位** | 纯 Python 包 | OpenClaw Hook 插件 |
| **触发方式** | 手动调用 / 脚本 | 自动 Hook |
| **API Key** | 可选（keyword模式不需要） | 需要 |
| **用途** | 任何 Python 项目 | OpenClaw 用户 |

**推荐组合：**
- 独立 Python 项目 → 只装 context-hawk
- OpenClaw 用户 → 装 hawk-bridge（内置 context-hawk 核心）

---

## 目录结构

```
context-hawk/
├── SKILL.md               ← 本文档
├── hawk/
│   ├── __init__.py
│   ├── memory.py           ← 四层记忆 + 衰减
│   ├── compressor.py       ← 上下文压缩
│   ├── config.py           ← 配置管理
│   ├── self_improving.py   ← 自我反思
│   ├── vector_retriever.py ← 向量检索
│   ├── markdown_importer.py ← .md 导入
│   ├── extractor.py        ← 记忆提取（keyword / LLM）
│   └── governance.py        ← 巡检指标
└── scripts/
    └── install.sh          ← 一键安装脚本
```
