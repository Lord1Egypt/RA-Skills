---
name: cnc-quote-workflow
version: 2.0.2
description: "CNC智能报价Workflow - 多Agent协作闭环。从黑盒24h到白盒10min。主赛道Workflow Hacker + 副赛道Agent Worker。"
author:
  name: Timo
  email: miscdd@163.com
  alias: 海狸 (Beaver)
license: MIT
metadata:
  openclaw:
    priority: P0
    category: workflow
    main_track: Workflow Hacker
    sub_track: Agent Worker
    triggers:
      - CNC报价
      - 智能报价
      - 制造报价Workflow
    stability:
      mode: production
      enable_uniskill: false
      rule_only_fallback: true
---

# 🦫 CNC智能报价Workflow

**一句话故事**: "10年制造业老师傅用 ClawHub 已发布的 CNC Quote Skill + OpenClaw Workflow，实现从黑盒24h 到白盒10min 的智能报价闭环"

---

## 作者信息

| 项目 | 信息 |
|------|------|
| 作者 | Timo |
| 邮箱 | miscdd@163.com |
| 标识 | 海狸 (Beaver) - 靠得住、能干事、在状态 |

---

## 参赛信息

| 项目 | 值 |
|------|-----|
| **主赛道** | Workflow Hacker |
| **副赛道** | Agent Worker |
| **核心Skill** | cnc-quote-system |
| **版本** | v2.0.2 |

---

## Workflow架构

```
用户输入
    ↓
┌─────────────────────────────────────┐
│ Agent1: 输入解析                    │
│ - 解析材料/尺寸/表面/数量           │
│ - 结构化查询输出                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Agent2: RAG检索                     │
│ - 案例检索（历史数据）              │
│ - 风险评估                          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Agent3: 元认知审核                  │
│ - 自我辩论                          │
│ - 行业分析                          │
│ - 生成白盒报价报告                  │
└─────────────────────────────────────┘
    ↓
输出: 报价报告 + 风险预警
```

---

## 核心优势

| 优势 | 说明 |
|------|------|
| ⚡ **速度** | 10分钟（行业平均24h+） |
| 📊 **透明** | 白盒报价，完整成本分解 |
| 🧠 **智能** | 3个Agent协作，自我辩论 |
| 🏆 **效率** | 效率提升144倍 |

---

## 文件结构

```
cnc-quote-workflow/
├── SKILL.md              # Skill文档
├── workflow.yaml         # Workflow定义
├── agent1_parser.py      # Agent1: 输入解析
├── agent2_rag.py         # Agent2: RAG检索
├── agent3_meta.py        # Agent3: 元认知审核
├── workflow_engine.py    # Workflow编排引擎
├── rule_only.py          # Rule-Only兜底引擎
├── config.json           # 配置文件
└── requirements.txt      # 依赖列表
```

---

## 快速开始

### 安装依赖

```bash
pip install pyyaml
```

### 运行Workflow

```python
from workflow_engine import WorkflowEngine

# 创建引擎
engine = WorkflowEngine()

# 执行报价
result = engine.execute("铝合金6061，100x50x10mm，表面阳极氧化，10件")

# 生成报告
report = engine.generate_report(result)
print(report)
```

---

## 测试用例

| 输入 | 单价 | 交期 |
|------|------|------|
| 铝合金6061，100x50x10mm，阳极氧化，10件 | ¥85.62 | 7天 |
| 不锈钢304，200x100x5mm，镀铬，50件 | ¥141.05 | 7天 |
| 45号钢，80x40x8mm，淬火，1件 | ¥80.15 | 5天 |

---

## 行业对比

| 平台类型 | 平均报价时间 | 透明度 | 我们的优势 |
|------|----------|--------|-----------|
| A类平台 | 24h | 黑盒 | 效率提升144倍 |
| B类平台 | 48h | 黑盒 | 效率提升288倍 |
| C类平台 | 12h | 半透明 | 效率提升72倍 |
| **我们的系统** | **10min** | **白盒** | - |

---

## 元认知特色

**自我辩论流程**：

1. 🤖 **正方**: 检索到X个案例，置信度Y%
2. 🤖 **反方**: 置信度<80%，建议人工复核
3. ⚖️ **仲裁**: 自动通过/条件通过/需人工审核

---

## 工业稳定设计

| 模式 | 说明 |
|------|------|
| **Rule-Only兜底** | 纯规则计算，100%稳定 |
| **UniSkill可选** | 默认关闭，可配置启用 |
| **自动降级** | 失败时自动切换兜底模式 |

---

## License

MIT License - Copyright (c) 2026 Timo

---

🦫 **海狸 (Beaver) | 靠得住、能干事、在状态**