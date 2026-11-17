<div align="center">

# 商业数据分析师

**把业务问题转成可靠分析、清晰决策与可验证行动。**

面向增长、转化、留存、收入、运营与市场研究的分析方法、参考资料和轻量意图路由工具。

[![Version](https://img.shields.io/github/package-json/v/phoenixlucky/business-data-analyst-skill?style=flat-square&label=version)](https://github.com/phoenixlucky/business-data-analyst-skill/blob/main/package.json)
[![Stars](https://img.shields.io/github/stars/phoenixlucky/business-data-analyst-skill?style=flat-square&label=stars)](https://github.com/phoenixlucky/business-data-analyst-skill/stargazers)
[![Forks](https://img.shields.io/github/forks/phoenixlucky/business-data-analyst-skill?style=flat-square&label=forks)](https://github.com/phoenixlucky/business-data-analyst-skill/forks)
[![Issues](https://img.shields.io/github/issues/phoenixlucky/business-data-analyst-skill?style=flat-square&label=issues)](https://github.com/phoenixlucky/business-data-analyst-skill/issues)
[![Last commit](https://img.shields.io/github/last-commit/phoenixlucky/business-data-analyst-skill?style=flat-square&label=updated)](https://github.com/phoenixlucky/business-data-analyst-skill/commits/main)
![Node.js 18+](https://img.shields.io/badge/Node.js-%E2%89%A518-339933?style=flat-square&logo=nodedotjs&logoColor=white)

[快速开始](#快速开始) · [分析能力](#分析能力) · [意图路由](#意图路由) · [项目结构](#项目结构) · [边界说明](#边界说明)

</div>

---

## 项目简介

本项目帮助分析者沿着一条清晰的经营分析主线工作：**定义问题与指标口径 → 检查数据质量 → 拆解业务驱动 → 评估影响 → 形成行动 → 验证效果**。

仓库包含可供 AI 宿主使用的分析技能说明、模型手册、报告与市场研究指南，以及一个不依赖外部库的 Node.js 关键词路由器。它提供分析方法和问题路由，不连接业务数据源，也不代替分析者核验数据与结论。

## 快速开始

### 将分析技能用于宿主环境

从 [SKILL.md](SKILL.md) 开始。根据任务再读取 `references/` 中对应专题，避免一次加载全部材料。分析所需的数据、计算能力及网页搜索由宿主环境提供。

### 在 Node.js 中调用意图路由

要求 **Node.js 18 或更高版本**。路由器只分析输入文本并返回场景提示，不查询数据或执行业务分析。

```js
const { routeSkillIntent } = require("./src");

const result = routeSkillIntent("最近续费率下降，帮我定位原因并给动作建议");

console.log(result.intent);     // retention_analysis
console.log(result.promptHint); // 优先做 cohort、续费和流失阶段拆解。
```

也支持对象形式：

```js
const result = routeSkillIntent({
  message: "请分析注册到支付的转化漏斗",
});
```

## 分析能力

| 领域 | 覆盖内容 |
| --- | --- |
| 经营诊断 | 指标口径、数据质量、趋势和结构拆解、驱动因素与业务影响 |
| 增长与客户 | 增长、漏斗、留存、复购、续费、流失和 cohort 分析 |
| 收入与效率 | 收入利润、贡献毛利、单位经济、产能与运营效率 |
| 市场与竞争 | 市场规模、行业趋势、竞争格局、客户需求与证据评估 |
| 报告与决策 | 商业报告、WBR/MBR/QBR、指标体系、方案比较、行动优先级与验证指标 |

### 可复用的分析模型

- **差异桥接与量价拆解**：解释实际结果相对预算、目标或基准期的变化。
- **单位经济与贡献毛利**：评估客群、产品、订单、渠道或门店的边际经济性。
- **情景与敏感性分析**：比较假设、约束、方案结果和关键变量影响。
- **帕累托与集中度分析**：检查贡献结构、关键依赖和组合风险。
- **统计推断与因果评估**：报告差异的不确定性，设计实验或适用的准实验。
- **指标树与资源优先级**：连接结果、驱动和护栏指标，按增量价值与约束比较方案。

每个模型均说明适用条件、所需数据与误用边界，避免只罗列框架名称。

### 尉缭子商业分析框架（现代转译）

通过“**制 → 称 → 权 → 分 → 备 → 胜 → 行 → 验**”串联问题定义、资源与约束、外部比较、重点分群、行动准备、方案评估、执行和效果验证。它是现代经营分析转译，**不是《尉缭子》原书已有的商业模型**；其中“验”是补充的数据验证环节。

详见[框架说明](references/wei-liaozi-business-framework.md)。

## 意图路由

路由器支持以下分析场景：

| 场景 | 路由标识 | 示例问题 |
| --- | --- | --- |
| 增长分析 | `growth_analysis` | 新增、活跃或销售增长为何变化？ |
| 漏斗分析 | `funnel_analysis` | 注册到激活或支付的转化在哪一步流失？ |
| 留存分析 | `retention_analysis` | 续费率、复购或留存为什么下降？ |
| 收入利润分析 | `revenue_analysis` | 收入、毛利或客单价由什么驱动？ |
| 运营效率分析 | `efficiency_analysis` | 人效、库存或履约效率如何改善？ |
| 经营诊断 | `business_diagnosis` | 经营结果偏离目标的主要原因是什么？ |
| 市场调研 | `market_research` | 市场规模、行业趋势或竞争格局如何？ |

## 项目结构

```text
.
├── SKILL.md
├── src/                           # Node.js 意图路由器
├── test/                          # 路由测试
├── references/
│   ├── business-reporting.md      # 商业报告与交付检查
│   ├── examples.md                # 分析案例
│   ├── market-research.md         # 市场研究方法
│   ├── metric-playbook.md         # 指标口径、推断、评估与方案比较
│   ├── router-design.md           # 路由规则与接口说明
│   └── wei-liaozi-business-framework.md # 端到端经营决策框架
├── agents/                        # Agent 元数据
├── package.json
└── CHANGELOG.md
```

## 本地检查

```bash
npm test
npm run lint
```

## 边界说明

- 不连接业务数据源，不自行运行 SQL 或统计分析。
- 不自行执行网页搜索；市场研究需要宿主提供搜索工具。
- 路由置信度是关键词匹配的启发式分数，不是经校准的概率。
- 分析结论应基于可追溯数据，并区分事实、推断、假设与风险。

## 版本

当前版本 **1.7.0**。变更记录见 [CHANGELOG.md](CHANGELOG.md)。
