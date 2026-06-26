---
name: consulting-methods-toolkit
description: 当用户需要管理咨询分析、诊断框架选择、问题拆解、战略工具应用（如5W2H、5WHY、PDCA、PESTEL、7S、波特五力、SWOT、BSC、波士顿矩阵、GE矩阵、价值链）时使用。基于管理咨询顾问常用的方法和工具，输出结构化分析过程与交付模板。
---

# Consulting Methods Toolkit

本技能已重构为“轻量主入口 + 分模块方法库”。
使用原则：先判断场景，再按需读取对应模块，避免一次性加载全部方法。

## 使用流程

1. 先用 `是什么-为什么-怎么做` 定义问题。
2. 根据场景选择一个“主链路模块”。
3. 只读取该模块文件中的方法卡。
4. 产出“结论 + 证据 + 行动 + 验证指标”。
5. 默认用 `PDCA` 闭环执行。

## 方法路由

### A. 问题定义与结构化拆解

适用：需求不清、问题复杂、需要快速搭分析骨架。  
读取：
- [01-core-thinking-and-structure.md](references/methods/01-core-thinking-and-structure.md)

### B. 分析工具与根因挖掘

适用：需要脑图/鱼骨图/系统展开图/树图进行分解与归因。  
读取：
- [02-analysis-tools.md](references/methods/02-analysis-tools.md)

### C. 战略与组织诊断

适用：战略一致性、组织协同、行业压力与企业能力诊断。  
读取：
- [03-strategy-and-diagnosis.md](references/methods/03-strategy-and-diagnosis.md)
- [03a-external-market-and-competition.md](references/methods/03a-external-market-and-competition.md)
- [03b-internal-strategy-and-organization.md](references/methods/03b-internal-strategy-and-organization.md)

### D. 营销与增长体系

适用：销售困境、市场导向管理、标杆对比与增长策略。  
读取：
- [04-marketing-and-growth.md](references/methods/04-marketing-and-growth.md)

### E. 流程优化与流程再造

适用：流程冗余、跨部门低效、BPR与Bottom-up改造。  
读取：
- [05-process-and-bpr.md](references/methods/05-process-and-bpr.md)

### F. 追问链与决策收敛

适用：5W2H/28问/5WHY深挖与行动收敛。  
读取：
- [06-questioning-and-root-cause.md](references/methods/06-questioning-and-root-cause.md)

## 方法调用规则

1. 每次优先选择 1 个主模块，最多并行 2 个模块。
2. 若出现跨模块冲突，优先以“问题定义模块（A）”和“执行闭环（PDCA）”为准。
3. 不重复输出同类模板，优先复用当前模块模板。
4. 新增方法必须先执行“准入与挂接协议”，再决定新增/合并/子卡化：
   - [00-method-addition-protocol.md](references/methods/00-method-addition-protocol.md)

## 输出格式要求

默认输出 4 段：
1. 问题定义：`是什么/为什么/怎么做`
2. 框架选择：为什么选这些方法
3. 关键发现：3-5条，按影响度排序
4. 执行计划：责任人、里程碑、指标、风险

## 质量标准

1. 不做空泛概念说明，必须给出可执行动作。
2. 结论必须对应证据或验证路径。
3. 至少提供一个低成本先行试点。
4. 若信息不足，先输出“最小数据清单”。

## 来源与检索

- 方法速查：
  - [method-catalog.md](references/method-catalog.md)
- 课程提取文本：
  - [source-extracted.txt](references/source-extracted.txt)

检索建议：
- `rg "5W2H|5WHY|PDCA|PESTEL|7-S|五力|BPR|标杆" references/methods`
