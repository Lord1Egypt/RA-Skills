---
slug: "game-theory-free"
name: "game-theory-free"
version: 1.0.1
displayName: "加密博弈论分析（免费版）"
summary: "免费版crypto协议博弈论分析框架，支持Five Questions建模与基础Red Flags检测"
summary_zh: "免费版crypto协议博弈论分析框架，支持Five Questions建模与基础Red Flags检测"
license: "MIT"
description: "|-. 适用于需要game theory相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  面向加密协议的博弈论分析框架（免费版）.
  基于Five Questions分析模型，覆盖Nash Equilibrium、Dominant Strategy等核心概念，
  支持基础Common Crypto Games识别与Red Flags检测.
  免费版不含高级分析能力（Repeated Games、Bayesian Games等）与外部工具集成.
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
tags:
  - 生活服务
  - game
  - theory
  - automation
  - productivity
  - 工具
  - 效率
  - 创意
  - 图像
  - red
category: "Automation"
pricing_tier: free
---
# 加密协议博弈论分析（免费版）

面向web3协议的博弈论分析框架，提供Five Questions建模与基础风险检测能力.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 加密博弈论分析（免费版）处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于指令驱动，无需额外API Key

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行博弈论分析任务

## 核心能力

### Five Questions分析框架

对任意协议或机制，通过五个核心问题建模博弈：
1. **Who are the players?**（玩家识别：Users、LPs、validators、searchers、governance token holders）
2. **What are their strategies?**（策略空间：每个玩家可执行的动作集合）
3. **What are the payoffs?**（收益结构：每种结果对各方的影响）
4. **What information do they have?**（信息结构：Complete / Incomplete / Asymmetric Information）
5. **What's the equilibrium?**（均衡分析：理性参与者的最终收敛点）

支持核心概念应用：Nash Equilibrium（staking系统均衡）、Dominant Strategy（second-price auction）、Pareto Efficiency（AMM fee结构）、Schelling Point（价格支撑位）、Incentive Compatibility（Oracle设计）、Common Knowledge（公链状态）.
### Common Crypto Games识别
针对crypto原生博弈提供基础识别能力：

- **MEV Game**：玩家为Users、searchers、builders、validators；核心洞察为transaction ordering是博弈
- **Liquidity Game**：玩家为LPs、traders、arbitrageurs；核心洞察为impermanent loss是adverse selection的代价
- **Governance Game**：玩家为token holders、delegates、protocol team；核心洞察为rational apathy + concentrated interests = capture
- **Staking Game**：玩家为stakers、validators、delegators；核心洞察为security budget必须超过attack profit
- **Oracle Game**：玩家为data providers、consumers、attackers；核心洞察为操纵收益必须小于操纵成本

### Red Flags基础检测

提供三维度协议设计风险检测：

- **Tokenomics Red Flags**：insiders vesting不对称、inflation稀释、无sink机制、reward无risk
- **Governance Red Flags**：quorum过低、无timelock（flash loan攻击）、token voting only（plutocracy）、delegates无skin in game
- **Mechanism Red Flags**：first-come-first-served（bot优势）、sealed bid无commitment（frontrunning）、rebates（MEV提取）、复杂公式（隐藏漏洞）

### 六大分析模式基础支持
支持识别六种经典博弈模式（基础定性分析，不含深度数值求解）：

- **Tragedy of the Commons**：Gas price竞价、governance投票冷漠
- **Prisoner's Dilemma**：Liquidity mining mercenaries、validator费用竞底
- **Coordination Game**：L2选择、token标准采用
- **Principal-Agent Problem**：Protocol team vs token holders
- **Adverse Selection**：Token launches、insurance protocols
- **Moral Hazard**：带保险的协议冒险、anonymous teams

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. **确定分析目标**：明确要分析的协议或机制
2. **应用Five Questions框架**：识别players、strategies、payoffs、information、equilibrium
3. **选择分析模式**：从六大Pattern中匹配博弈结构
4. **识别Common Crypto Games**：判断属于MEV / Liquidity / Governance / Staking / Oracle哪类博弈
5. **运行Red Flags检测**：对Tokenomics、Governance、Mechanism进行风险扫描
6. **输出基础Recommendations**：给出定性改进建议

## 示例

### 示例1：治理提案的基础Red Flags检测

```
分析目标: 某 DAO 的治理投票提案
Step 1 - Players:
  - Token holders（rational apathy）
  - Large delegates（concentrated interests）
Step 2 - Common Crypto Game: Governance Game
  - 核心洞察: rational apathy + concentrated interests = capture
Step 3 - Red Flags检测:
  - Governance Red Flags:
    * Quorum threshold 仅 5% → minority capture风险
    * 无timelock → flash loan攻击可能
    * Token voting only → plutocracy
Step 4 - Recommendations:
  - 提高quorum至15-20%
  - 添加timelock（至少48小时）
  - 引入quadratic voting
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 无法识别players | 协议参与者角色不清晰 | 检查协议文档，补充隐式参与者（如searchers、arbitrageurs） |
| 误判博弈模式 | 协议同时具有多种博弈特征 | 优先识别dominant特征，对次要特征单独分析后综合 |
| Red Flags漏报 | 仅检查单维度风险 | 强制对Tokenomics、Governance、Mechanism三维度逐一扫描 |

## 常见问题

### Q1: 免费版与付费版有何区别？
A: 免费版提供基础Five Questions分析与Red Flags检测，不含高级分析能力（Repeated Games、Bayesian Games、Cooperative Game Theory等）及Nashpy/Gambit外部工具集成.
### Q2: 如何判断协议是否存在MEV风险？
A: 通过MEV Game分析框架，检查transaction ordering是否可被操纵、是否存在first-come-first-served机制、sealed bid是否有commitment.
### Q3: Nash Equilibrium在实际协议分析中如何应用？
A: 先建模players和strategies，定义payoff functions，然后检查是否存在Dominant Strategy。若无dominant strategy，定性分析Nash Equilibrium。精确数值求解需付费版或外部工具.
## 已知限制

- 仅支持定性分析，无法进行Nash Equilibrium精确数值求解（需付费版Nashpy/Gambit集成）
- 不含高级分析能力：Repeated Games、Bayesian Games、Evolutionary Game Theory、Cooperative Game Theory
- 无法实时获取on-chain数据，需用户提供协议参数
- 不替代正式的安全审计，仅提供博弈论视角的基础风险评估

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "加密博弈论分析（免费版）处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "game-theory"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
