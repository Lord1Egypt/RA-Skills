# 自我进化Agent - Evolving Agent

基于进化论的混合进化策略，结合达尔文式探索与拉马克式优化，支持种群进化、精英保留、交叉重组。

**English**: Self-evolving agent with hybrid evolutionary strategy: Darwinian exploration + Lamarckian optimization, population evolution, elitism, and crossover.

---

## 🚀 核心特性 - Core Features

| 特性 Feature | 说明 Description |
|------|------|
| **混合进化策略** | 达尔文式探索（发散变异）+ 拉马克式优化（反馈迭代） |
| **五环架构** | 用户层 → 种群层 → 基因库层 → 反思层 → 哨兵层 |
| **种群进化** | 生成3~5个候选方案，交叉重组，竞技场排名 |
| **多目标评估** | 6维度适应度评分（可行性、效果、风险、成本、创新、可回滚） |
| **基因库系统** | 存储Top 100成功模式，跨代遗传 |
| **技能结晶化** | 把反复验证的成功经验变成独立skill |
| **安全第一** | Git自动快照、审计日志、回滚机制、分级确认 |

---

## 🎯 设计灵感 - Design Inspirations

- **经典进化论**: 种群、变异、选择、遗传、交叉、精英保留
- **公开论文**: 自我反思、提示优化、多agent协同

---

## 🏗️ 五环架构 - Five-Ring Architecture

```
┌─────────────────────────────────────────────────┐
│ 用户层（User Layer）- 最终决策者           │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ Ring 3（Population Layer）- 种群层         │
│ - 生成多个候选方案（N=3~5）                     │
│ - 交叉重组（Crossover）                         │
│ - 多目标评估 + 竞技场排名                       │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ Ring 2（Gene Pool Layer）- 基因库层       │
│ - 分级记忆（Hot→Warm→Cold→Forgotten）          │
│ - 精英模式库 + 基因库 + 技能结晶化             │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ Ring 1（Reflection Layer）- 反思层         │
│ - 发散推理 + 收敛验证 + 自我批判                │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ Ring 0（Sentinel Layer）- 哨兵层           │
│ - Git版本控制 + 自动快照 + 回滚机制             │
└─────────────────────────────────────────────────┘
```

---

## 🧬 种群进化流程 - Population Evolution Flow

```
初始状态
    ↓
Ring 1：发散推理（变异）→ 生成3~5个候选方案
    ↓
Ring 3：交叉重组（可选）→ 结合不同方案优点
    ↓
Ring 3：多目标评估（选择）→ 6维度适应度评分 + 竞技场排名
    ↓
用户层：选择确认 → 用户选择最优方案
    ↓
Ring 0：执行进化（需确认）→ Git快照 + 逐行确认高风险操作
    ↓
Ring 2：记忆遗传 → 更新分级记忆 + 基因库 + 精英模式库
```

---

## 📊 多目标适应度评分 - Multi-Objective Fitness Scoring

| 维度 Dimension | 权重 Weight | 说明 Description |
|------|------|------|
| 可行性 Feasibility | 25% | 方案是否能安全执行 |
| 效果预期 Expected Impact | 25% | 预期能带来多大改进 |
| 风险等级 Risk Level | 20% | 低/中/高风险（越低越好） |
| 实现成本 Implementation Cost | 15% | 时间/精力成本（越低越好） |
| 创新性 Novelty | 10% | 是否有新想法/新模式 |
| 可回滚性 Rollback Safety | 5% | 出问题能否轻松回滚 |

---

## 🎯 进化范围 - Evolution Scope

1. **修改自己的配置** - 优化SKILL.md、调整进化参数
2. **创建新的Skill** - 根据需求设计新skill、结晶化成功经验
3. **优化工作流** - 改进任务流程、自动化重复工作、优化prompt
4. **完善和优化Soul** - 更新SOUL.md、调整性格设定
5. **记忆和基因库管理** - 整理记忆、模式提取、基因库更新
6. **能力模块管理** - 评估、搜索、安装、淘汰能力模块

---

## 🛡️ 安全原则 - Safety Principles

1. **透明 Transparency** - 所有操作可见，提供完整预览和解释
2. **可控 Controllability** - 用户可随时取消、修改，高风险操作逐行确认
3. **可逆 Reversibility** - Git自动快照、一键回滚、完整变更历史
4. **渐进 Incrementalism** - 小步迭代、先测试再推广、持续监控
5. **用户主导 User-in-the-Loop** - 用户是最终决策者、提供选择压力
6. **基因库保守 Conservative Gene Pool** - 严格入库标准、定期淘汰低质量基因

---

## 📁 文件结构 - File Structure

```
evolving-agent/
├── SKILL.md              # 完整设计文档
├── README.md             # 本文件 - 项目概述
└── references/           # 参考资料目录
```

---

## 🚀 开始使用 - Getting Started

在OpenClaw中使用本skill，触发词包括：
- "帮我进化一下"、"自我进化"、"优化一下自己"
- "生成3个改进方案"、"进化我的能力"
- "探索新方法"、"优化现有方案"

英文触发词：
- "Help me evolve", "Self-evolve", "Optimize myself"
- "Generate 3 improvement ideas", "Evolve my capabilities"
- "Explore new approaches", "Optimize existing solutions"

---

## 📚 相关资源 - Related Resources

- **protea**: 三环架构、基因库、技能结晶化
- **rotifer**: 模块化能力、竞技场思路
- **进化论经典著作**: 种群、变异、选择、遗传、交叉、精英保留
- **自我优化相关论文**: 自我反思、提示优化、多agent协同

---

## 🤝 贡献 - Contributing

本skill本身也是自我进化的！使用本skill来改进它自己。

---

## 📄 许可证 - License

本项目采用 MIT 许可证。
