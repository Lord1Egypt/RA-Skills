---
name: deep-research
description: 深度研究技能，用于进行领域调研、文献调研、survey研究。当用户说"做一个survey"、"深度研究一下XX"、"文献调研"、"研究一下XX领域的最新进展"、"帮我调研XX"、"学术调研"时自动触发。支持arXiv、PubMed、PMC、Google Scholar等多个数据源，自动下载PDF并解析全文，生成三层报告（执行摘要、验证清单、完整报告）。
---

# Skill: Adaptive Depth Research v6.0 Universal

> 版本：6.0.0
> 描述：领域无关 | 配置驱动 | 数据源自适应 | 三层输出

---

## 🎯 核心设计原则

1. **数据源自适应**：arXiv/PMC 自动下 PDF，付费期刊自动切摘要模式
2. **领域无关**：提取逻辑不依赖特定术语，靠配置驱动
3. **输出分层**：执行摘要 + 验证清单 + 完整报告，各取所需
4. **一次配置，全领域复用**

---

## 📦 架构图

```
【配置层】
config/research-config.yaml  # 定义领域、关键指标、数据源优先级

      ↓

【检索层】(自动分流)
├─ arXiv → 下载 PDF → 全文解析 → 高可信提取
├─ PMC → 下载 PDF → 全文解析 → 高可信提取
├─ PubMed → 仅摘要 → 方向性提取 + 标注"需验证"
└─ Web → 网页抓取 → 关键结论提取

      ↓

【提取层】(通用 Prompt)
prompts/extract-universal.txt  # 不依赖领域术语

      ↓

【输出层】(三层报告)
├─ reports/executive-summary.md  # 决策者用，≤1 页
├─ reports/validation-checklist.md  # 执行者用，可操作
└─ reports/full-report.md  # 审计用，完整溯源
```

---

## 🚀 触发命令

```bash
# 完整研究流程
bash scripts/run-research.sh "<主题>" --domain "<领域>"

# 示例
bash scripts/run-research.sh "transformer efficiency" --domain "machine learning"
bash scripts/run-research.sh "telemedicine cost savings" --domain "healthcare"
```

---

## 📁 文件结构

```
skills/deep-research/
├── SKILL.md
├── config/
│   └── research-config.yaml      # 领域配置
├── prompts/
│   ├── extract-universal.txt     # 通用提取Prompt
│   ├── cluster-cards.txt         # 卡片聚类
│   └── write-brief.txt           # 主题简报
├── templates/
│   ├── executive-summary.md      # 执行摘要模板
│   ├── validation-checklist.md   # 验证清单模板
│   └── full-report.md            # 完整报告模板
└── scripts/
    ├── run-research.sh           # 完整研究流程
    ├── fetch-and-extract.sh      # 自动分流提取
    ├── extract-from-pdf.py       # PDF解析
    └── check-sourcing.sh         # 溯源验证
```

---

## 🔧 配置说明

### 修改研究领域

编辑 `config/research-config.yaml`:

```yaml
research_domain: "your_domain_here"

key_metrics:
  performance:
    - accuracy
    - AUC
    - F1
  # 添加你的指标...
```

---

## 📊 三层输出说明

### 1. 执行摘要 (executive-summary.md)

- **受众**：决策者
- **长度**：≤1页
- **内容**：
  - 核心结论（已验证 vs 待验证）
  - 可直接行动
  - 需验证后行动

### 2. 验证清单 (validation-checklist.md)

- **受众**：执行者
- **格式**：操作导向
- **内容**：
  - 缺失指标汇总表
  - 具体验证路径
  - 通用验证方法

### 3. 完整报告 (full-report.md)

- **受众**：审计/存档
- **内容**：
  - 方法论说明
  - 已验证结论 + 证据
  - 待验证线索
  - 战略建议（短/中/长期）
  - 完整卡片索引

---

## 🎯 执行流程

### Step 1: 检索

```bash
# 自动检索 arXiv + PubMed
bash scripts/run-research.sh "<主题>"
```

### Step 2: 提取

```bash
# 自动分流提取
bash scripts/fetch-and-extract.sh <source_url>

# 或手动提取
python3 scripts/extract-from-pdf.py card-001 "<pdf_url>"
```

### Step 3: 验证

```bash
# 溯源检查
bash scripts/check-sourcing.sh reports/full-report.md sources/
```

### Step 4: 生成报告

三层报告自动生成在 `reports/` 目录

---

## ✅ 质量门禁

1. **数据完整度标注**：high/medium/low
2. **缺失指标清单**：每个卡片明确列出
3. **验证路径具体**：可操作，非模糊建议
4. **溯源验证**：所有数据可溯源到卡片

---

## 📈 v6.0 vs 之前版本

| 维度 | v5.x | v6.0 Universal |
|------|------|----------------|
| **领域** | 医疗特化 | 领域无关，配置驱动 |
| **数据源** | 固定PubMed | 自适应分流 |
| **提取** | 依赖医疗术语 | 通用Prompt |
| **输出** | 单一报告 | 三层输出 |
| **配置** | 硬编码 | YAML配置 |

---

## 💡 用户只需

1. **修改配置**：改 `research_domain` 和 `key_metrics`
2. **运行命令**：`bash scripts/run-research.sh "<主题>"`
3. **阅读摘要**：5分钟了解核心结论
4. **按清单验证**：30分钟补全关键数据
5. **推进决策**：基于验证结果

---

## 🔑 核心哲学

> **让工具适应人，而不是人适应工具。**  
> 你专注领域知识和商业决策，工具负责广度扫描、结构化整理、诚实标注。

---

*Skill版本：6.0.0 Universal | 最后更新：2026-03-19*

---

## v7.0 融合版 (2026-03-21)

### 新增能力

**Research Claw 桥接**：
- 搜索：arXiv, Google Scholar, PubMed, Semantic Scholar
- PDF解析：使用pymupdf
- 网页读取：Web Reader Tool

### 使用方法

```python
from scripts.research_claw_bridge import ResearchTools

tools = ResearchTools()

# 搜索论文
papers = tools.search_papers("LLM agent", max_results=5)

# 完整流程（搜索+下载+提取）
results = tools.full_research_flow("商保控费")
```

### 文件

- `scripts/research_claw_bridge.py` - 桥接模块
