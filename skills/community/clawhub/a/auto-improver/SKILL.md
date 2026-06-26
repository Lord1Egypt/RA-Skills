---
name: auto-improver
description: Auto-improving AI agent that learns from every execution, extracts patterns, and continuously optimizes itself. 17-minute autonomous loop with confidence scoring and skill evolution.
origin: meta-skill
version: 1.0.0
tags:
  - self-improvement
  - learning
  - automation
  - pattern-extraction
  - meta-skill
tools:
  - Read
  - Write
  - Bash
  - Exec
model: sonnet
---

# Auto-Improver - 自动改进代理

**版本**：v1.0.0  
**定位**：L3 进化层 - 自进化 AI 代理引擎

---

## 📖 技能说明

Auto-Improver 是一款自进化 AI 代理引擎，通过 17 分钟自主执行循环（观察→检测→提取→聚合），自动从每次执行中学习、提取模式、持续优化自身。核心价值：让 AI 越用越聪明，自动捕获用户反馈、识别高效模式、生成改进建议并执行优化。是构建自进化 AI 系统的核心基础设施。

**与 self-improving-agent 的区别**：
- ✅ 更快的执行循环（17 分钟 vs 30 分钟）
- ✅ 更智能的置信度模型（六维评估 + 时间衰减）
- ✅ 更强大的模式提取（支持 8 种模式类型）
- ✅ 更灵活的聚合机制（Skill/Command/Agent 三级聚合）

---

## 🎯 使用场景

| 场景 | 描述 |
|------|------|
| **自进化 AI 系统** | 「让 AI 自动从历史会话中学习」- 自动提取 Instinct，持续优化 |
| **模式提取** | 「从过去 7 天的执行中提取可复用模式」- 识别高效工作流 |
| **用户反馈分析** |「分析用户确认/反对的反馈」- 调整置信度，优化行为 |
| **技能进化** |「将成熟的 Instinct 进化为新技能」- 自动创建可发布技能 |
| **性能优化** |「识别执行瓶颈并优化」- 分析执行数据，生成优化建议 |

---

## 💰 定价方案

| 版本 | 价格 | 功能 | 适用对象 |
|------|------|------|----------|
| **个人版** | ¥199/年 | 基础自进化循环、10 次提取/月、基础模式提取 | 个人开发者、研究者 |
| **商业版** | ¥1999/年 | 个人版 + AI 建议生成、100 次提取/月、效果追踪、A/B 测试 | 小型团队、创业公司 |
| **企业版** | ¥19999/年 | 商业版 + 无限提取、私有部署、定制模型、专属支持、SLA 保障 | 中大型企业、知识密集型团队 |

---

## ❓ FAQ（常见问题）

**Q1: Auto-Improver 如何学习？**
A: 通过 4 阶段 Pipeline（观察→检测→提取→聚合）自动学习。观察阶段捕获执行数据，检测阶段识别模式，提取阶段生成 Instinct，聚合阶段聚合成 Skill/Command/Agent。

**Q2: 置信度如何计算？**
A: 置信度 = 基础置信度（基于观测次数）+ 用户反馈调整 + 时间衰减。观测≥10 次且反馈正面可达 0.85+。

**Q3: 支持多少技能的进化？**
A: 个人版 10 个技能，商业版 100 个技能，企业版无限。支持技能批量导入和导出。

**Q4: 17 分钟循环如何工作？**
A: 观察（5 分钟）→ 检测（3 分钟）→ 提取（5 分钟）→ 聚合（4 分钟）= 17 分钟完整循环。支持并行执行和中断恢复。

**Q5: 如何保护数据隐私？**
A: 所有数据本地加密存储，支持敏感信息自动识别和脱敏。企业版支持私有部署和数据访问审计。

---

## 🚀 快速开始

```bash
# 安装
clawhub install auto-improver

# 启动自进化循环
auto-improver start --interval=17m

# 查看学习进度
auto-improver status

# 提取的模式
auto-improver instincts list

# 导出的技能
auto-improver skills list
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 循环时间 | 17 分钟 |
| 模式识别准确率 | 92% |
| 置信度上限 | 0.95 |
| 支持模式类型 | 8 种 |
| 支持聚合级别 | 3 级（Skill/Command/Agent） |

---

**文件版本**：v1.0.0  
**创建时间**：2026-04-01  
**上架时间**：2026-04-01  
**上架用户**：pagoda111king
