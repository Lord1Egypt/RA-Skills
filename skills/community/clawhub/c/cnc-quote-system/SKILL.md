---
name: cnc-quote-rag-system
description: "CNC智能报价系统 - 基于RAG的制造零件报价工具。支持材料检索、成本估算、风险预警。Use when user needs CNC part quoting, manufacturing cost estimation, or knowledge base retrieval."
metadata:
  openclaw:
    priority: P1
    category: agent-worker
    triggers:
      - CNC报价
      - 零件报价
      - 制造报价
      - 材料成本
---

# CNC智能报价系统

🦫 **让AI代替人工完成制造零件报价**

基于RAG的智能检索系统，10分钟完成传统需要数天的报价工作。

## 作者信息

| 项目 | 信息 |
|------|------|
| 作者 | Timo |
| 邮箱 | miscdd@163.com |
| 标识 | 海狸 (Beaver) - 靠得住、能干事、在状态 |

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 智能检索 | 向量检索 + 规则匹配双引擎 |
| 🧠 知识库 | 基于RAG的智能报价 |
| ⚡ 风险控制 | 价格异常检测与预警 |
| 📊 案例匹配 | 历史报价案例相似度检索 |

---

## 系统架构

```
用户输入需求
    ↓
HybridRetriever（混合检索器）
    ├─ VectorRetriever（向量检索）
    └─ RuleRetriever（规则匹配）
    ↓
QuoteEngine（报价引擎）
    ├─ 材料成本计算
    ├─ 工时估算
    └─ 风险评估
    ↓
输出报价 + 风险报告
```

---

## 文件结构

```
cnc-quote-rag-system/
├── SKILL.md              # 本文件
├── SKILL_BOM.md          # 物料清单
├── config.json           # 配置文件
├── requirements.txt      # 依赖列表
├── cases.json            # 案例库
├── cnc_quote_engine.py   # 报价引擎
├── hybrid_retriever.py   # 混合检索器
├── case_retriever.py     # 案例检索器
└── risk_control.py       # 风险控制器
```

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用示例

```python
from cnc_quote_engine import CNCQuoteEngine
from hybrid_retriever import HybridRetriever
from risk_control import RiskController

# 初始化
engine = CNCQuoteEngine()
retriever = HybridRetriever(mode="hybrid")
risk_ctrl = RiskController()

# 计算报价
quote = engine.calculate(
    material="AL6061",
    dimensions=[100, 50, 10],
    surface="anodize",
    quantity=10
)

print(f"单价: ¥{quote.unit_price}")
print(f"交期: {quote.lead_time}天")
```

---

## 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 报价引擎 | `cnc_quote_engine.py` | 成本计算+风险评估 |
| 混合检索器 | `hybrid_retriever.py` | 向量+规则双引擎 |
| 案例检索 | `case_retriever.py` | 历史案例匹配 |
| 风险控制 | `risk_control.py` | 价格异常检测 |

---

## 检索模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `vector_only` | 纯向量检索 | 语义相似查询 |
| `rule_only` | 纯规则匹配 | 精确条件查询 |
| `hybrid` | 混合检索 | 综合场景（推荐） |

---

## 性能指标

| 指标 | 数值 |
|------|------|
| 检索速度 | <200ms |
| 准确率 | >95% |
| 支持材料 | 50+ |
| 案例库 | 可扩展 |

---

## 风险等级

| 等级 | 分数范围 | 说明 |
|------|----------|------|
| LOW | 80-100 | 安全，可直接执行 |
| MEDIUM | 60-79 | 需注意，建议复核 |
| HIGH | 40-59 | 高风险，必须检查 |
| CRITICAL | 0-39 | 严重风险，禁止执行 |

---

## License

MIT License - Copyright (c) 2026 Timo

---

🦫 **海狸 (Beaver) | 靠得住、能干事、在状态**