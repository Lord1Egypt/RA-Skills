# AgentMem — 多Agent记忆+调度系统

> **记忆+调度+跨通道互通的闭环系统**
> 市场上少有的同时管理"Agent记住什么"和"谁该干什么"的开源方案

---

## 🧠 核心能力

### 四层记忆分级
| 层级 | 生命周期 | 用途 |
|------|---------|------|
| **HOT** | 实时，2小时 | 当前会话，跨通道互通 |
| **WARM** | 24小时 | 近期摘要，随手可查 |
| **COLD** | 永久 | 重要事实、决策、用户偏好 |
| **ARCHIVE** | 30天 | 历史归档，可检索 |

### 双引擎检索
- **向量检索** — chroma 语义相似度搜索
- **BM25** — 关键词精准匹配
- **MultiSignalFusion** — 向量+BM25+时间权重融合排序

### 调度+记忆联动
```
用户请求 → 意图识别 → Agent调度 → 执行 → 日志 → 优化下次调度
```
每次调度自动记录：谁在哪个通道发起了什么任务，派给了谁，结果如何。

### 跨通道互通
同一Agent在不同通道（webchat/飞书/Slack/Telegram）的记忆自动共享。
在A通道聊完，B通道的Bot也能接上话。

---

## 📦 快速开始

```bash
pip install -e .

# 写入一条记忆
python -m agent_mem.core.hot_cache write --agent main --channel webchat --text "用户偏好简洁回答" --importance 7

# 查询跨通道记忆
python -m agent_mem.core.hot_cache query --agent main --limit 5

# 记录一次调度
python -m agent_mem.core.dispatch_logger record \
  --from-channel webchat --to-agent advertising-agent \
  --task "优化素材ROI" --result success --duration 5.2

# 查看调度统计
python -m agent_mem.core.dispatch_logger stats

# 运行记忆引擎
python -m agent_mem.core.engine_v2 --mode daily
```

---

## 🏗️ 架构

```
agent_mem/
├── core/                  # 核心组件
│   ├── hot_cache.py       # HOT层实时会话缓存
│   ├── dispatch_logger.py # 调度链路日志
│   ├── dispatch.py        # 调度引擎（意图识别+Agent选择）
│   └── engine_v2.py       # 记忆引擎（提取+分级+图谱）
├── memory/                # 记忆模块
│   ├── memory_recall.py   # BM25 + MultiSignalFusion检索
│   ├── enhanced_extractor.py # 事实提取
│   ├── forgetting.py      # 遗忘机制
│   ├── knowledge_graph.py # 知识图谱
│   ├── contradiction_detector.py # 矛盾检测
│   ├── self_review.py     # 自我审查
│   ├── promoter_v2.py     # 去重+噪音过滤
│   └── ...
├── agents/                # Agent层
│   └── multi_agent_share.py # 多Agent记忆共享/隔离
└── utils/                 # 工具
    └── benchmark.py       # 基准测试
```

---

## 🔧 依赖

- Python 3.10+
- chromadb（向量存储）
- sentence-transformers 或 embedding 模型（可选，内置fallback）

---

## 📊 与市场主流对比

| 能力 | AgentMem | 说明 |
|------|----------|------|
| 四层时间分级 | ✅ | 记忆按HOT→WARM→COLD→ARCHIVE自然衰减 |
| 跨通道互通 | ✅ | 同一Agent多通道记忆自动共享 |
| 调度+记忆联动 | ✅ | 调度决策→执行→记录→优化，自动闭环 |
| 多Agent隔离 | ✅ | 各Agent记忆独立存储，不混淆 |
| 矛盾检测 | ✅ | 自动检测事实矛盾并标记 |
| 知识图谱 | ✅ | 事件→决策→结果因果链自动关联 |
| 遗忘机制 | ✅ | TTL衰减，自动清理 |
| 主动召回 | ✅ | 话题相关历史经验自动推送 |
| 记忆反馈修正 | ✅ | 自然语言修正已存记忆 |
| 自我审查 | ✅ | 自动提炼规律+成功率追踪 |

---

## 📄 许可证

[MIT License](LICENSE)
