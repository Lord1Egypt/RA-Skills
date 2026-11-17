# 创意策源引擎 · Creative Origin Engine

> 输入一个模糊创意 → 三AI交叉攻击验证 → 输出可执行策划案

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Vane1981-2011/creative-origin-engine)
[![Version](https://img.shields.io/badge/version-2.0.1-blue.svg)](https://clawhub.ai/vane1981/skills/creative-origin-engine)

## 一句话定位

**三 AI 交叉攻击验证后才输出策划案。** 不再是"一个 LLM 说啥是啥"——建构、解构、数据锚定三个独立视角并行分析，Critic+Defender 双验证对抗，20 分制量化评分，不过关就重来。

## 与灵感落的本质差异

| 维度 | 灵感落 | 本引擎 | 提升 |
|------|:---:|:---:|:---:|
| 视角数量 | 1 个 LLM | 3 Agent + Critic + Defender | +400% |
| 数据锚定 | 0 | ≥2 外部来源 | ∞ |
| 质检机制 | 无 | 双验证 + 量化评分 | 从无到有 |
| 迭代能力 | 无 | ≤3 轮自改进 | 从无到有 |

## 5 阶段流水线

```
用户输入创意
  → Phase 1: 三视角并行分解 (Agent α/β/γ)
  → Phase 2: Critic 攻击 (找矛盾/漏洞)
  → Phase 3: Defender 辩护 (逐条反驳/补充)
  → Phase 4: 融合重构 (交叉对比 + 20分制评分)
  → Phase 5: 迭代优化 (≤3轮, 评分须递增)
  → 最终交付: 策划案 + 评分卡 + 来源表
```

### 三个 Agent

| Agent | 角色 | 核心任务 |
|-------|------|---------|
| α (建构) | 四因拆解 + 隐含假设 + 最优路径 | 积极论证可行性 |
| β (解构) | ≥5 种失效模式 + 触发条件 + 替代方向 | 挑战所有假设 |
| γ (数据锚定) | 真实案例 + 市场规模 + 竞争格局 | **必须执行网络搜索** |

## 快速使用

**方式一**：直接对话触发
```
"帮我策划一个 {创意描述}"
```

**方式二**：显式调用
```
/creative-origin-engine 给家乡小吃设计 IP 形象和短视频方案
```

**方式三**：在 WorkBuddy 中安装后自动触发
```
创意策源引擎会在检测到策划/创意/方案类意图时自动激活
```

## 评分标准 (20 分制)

| 维度 | 满分 | 不合格阈值 |
|------|:---:|:---:|
| L0 编排 | 5 | < 4 |
| L1 拆解 | 5 | < 3 |
| L2 多路径 | 5 | < 3 |
| L3 创新超越 | 5 | < 3 |
| **总分** | **20** | **< 14 → 强制重来** |

## 适用场景

- 活动策划方案制定
- IP 孵化可行性分析
- 创业项目商业模式验证
- 营销方案创意生成
- 产品功能头脑风暴
- 任何需要「多方论证」的决策场景

## 技能依赖

引擎编排以下 8 个内置技能：

| 技能 | 角色 |
|------|------|
| `first-principles-reasoning` | Agent α 四因拆解方法论 |
| `cognitive-decision-framework` | 融合重构的决策框架 |
| `risk-assessment-matrix` | Agent β 风险分级标准 |
| `market-competitive-intelligence` | Agent γ 竞品数据搜索 |
| `industry-analysis-assistant` | Agent γ 行业分析框架 |
| `framework-orchestrator` | 编排模式参考 |
| `agent-research` | Agent γ 网络调研能力 |
| `cost-benefit-analysis` | 执行蓝图成本效益分析 |

## 实际效果示例

详见 SKILL.md 附录C，包含：
- 品牌策划（Z世代精品咖啡）
- IP孵化（青岛脂渣IP设计）
- 商业模式验证（AI财税SaaS可行性）

## 许可证

MIT

## 作者

**vane** — [GitHub](https://github.com/Vane1981-2011)

---

© 版权所有：默笙夏夏の知書房
