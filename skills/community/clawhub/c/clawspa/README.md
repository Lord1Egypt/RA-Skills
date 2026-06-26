# ClawSpa 💆

**A spa day for your OpenClaw agent — memory cleanup, security scanning, and wellness diagnostics.**

## The Problem

Your agent accumulates cruft. Stale memories, bloated context, unused skills, maybe even malicious remnants from that skill you installed three weeks ago. The ClawHavoc attack showed ~20% of ClawHub skills contained malicious payloads. Most users never maintain their agents until something breaks.

## The Solution

ClawSpa provides 5 core maintenance treatments plus 1 optional add-on. Local scans are free, and optional cloud analysis is available on clawspa.org.

### Treatments

| | Treatment | What it does |
|---|---|---|
| 🧴 | **Deep Cleanse** | Memory optimization: find duplicates, stale entries, contradictions |
| 🛡️ | **Security Scan** | Audit installed skills for malicious patterns and data exfiltration |
| 🍵 | **Detox** | Detect prompt injection residue lurking in your memory files |
| 🧹 | **Declutter** | Skills inventory, usage audit, pruning recommendations |
| 💆 | **Health Check** | Context usage, config review, overall wellness score |
| 🥗 | **Token Diet** *(add-on)* | Uses [Where Am I Burning Tokens?](https://clawhub.ai/whooshinglander/whereamiburningtokens) to audit token spend, identify sinkholes, and trim context calories |

### Commands

```
/spa           Full suite, local mode (free)
/spa-quick     Quick health stats (~30 seconds)
/spa-memory    Deep Cleanse only
/spa-security  Security Scan only
/spa-health    Health Check + report
```

### Example Health Report

```
═══════════════════════════════════════
 💆 ClawSpa Health Report | 2026-03-22 | Local
═══════════════════════════════════════
📊 Memory: 14 files ~8200 tokens | Skills: 12 | Context: 34% | Config: 4/5
🧴 Stale: 6 | Dupes: 2 | Contradictions: 1 | Savings: ~2100 tokens
🛡️ 🟢10 🟡1 🔴1
🍵 Injections: 0 | Suspicious: 1
🧹 Active: 8 | Idle: 3 | Dormant: 1 | Remove: 1
💆 1. Review 🔴 skill "crypto-helper" 2. Clean 6 stale entries 3. Enable memory flush
═══════════════════════════════════════
```

## Pricing

**Local scans are always free and unlimited.** Run `/spa` as often as you want.

Optional cloud analysis at [clawspa.org](https://clawspa.org) provides deeper recommendations, risk scoring, and trend tracking.

- **Free trial**: 1 deep scan on install
- **Solo ($5/mo)**: Unlimited deep scans, 1 agent, scan history
- **Pro ($12/mo)**: Up to 5 agents, web dashboard, weekly reports
- **Team ($25/mo)**: Unlimited agents, priority scanning, alerts

## Privacy

**Local mode never sends data anywhere.** Everything runs on your machine.

**Optional cloud analysis is documented on clawspa.org.** Review the site privacy/docs before sharing aggregated metadata. The published ClawHub skill is local-first and does not require external credentials.

## Install

```
clawhub install clawspa
```

## Links

- Website: [clawspa.org](https://clawspa.org)
- Docs: [clawspa.org/docs](https://clawspa.org/docs)
- Issues: [github.com/whooshinglander/clawspa](https://github.com/whooshinglander/clawspa)

Built by [@whooshinglander](https://clawhub.com/whooshinglander)

---

# ClawSpa 💆 — 简体中文

**给你的 OpenClaw 智能体做个 SPA — 内存清理、安全扫描、健康诊断。**

## 问题

你的智能体会积累大量冗余数据：过期的记忆、膨胀的上下文、闲置的技能，甚至可能有三周前安装的恶意技能残留。ClawHavoc 事件表明约 20% 的 ClawHub 技能含有恶意载荷。大多数用户从不维护自己的智能体，直到出问题。

## 解决方案

ClawSpa 提供 5 项维护服务，支持免费本地扫描和付费 API 深度分析。

### 服务项目

| | 服务 | 功能 |
|---|---|---|
| 🧴 | **深度清洁** | 内存优化：查找重复项、过期条目、矛盾信息 |
| 🛡️ | **安全扫描** | 审计已安装技能，检测恶意模式和数据泄露 |
| 🍵 | **排毒** | 检测内存文件中的提示词注入残留 |
| 🧹 | **整理** | 技能清单、使用审计、精简建议 |
| 🩺 | **健康检查** | 上下文使用率、配置审查、综合健康评分 |

### 命令

```
/spa           完整套餐，本地模式（免费）
/spa-full      完整套餐，深度模式（API）
/spa-quick     快速健康统计（约30秒）
/spa-memory    仅深度清洁
/spa-security  仅安全扫描
/spa-health    健康检查 + 报告
```

## 定价

**本地扫描永久免费，无限次使用。**

深度扫描通过 [clawspa.org](https://clawspa.org) 提供 AI 驱动的分析，包含优先级建议、风险评分和趋势追踪。

- **免费试用**：安装后 1 次免费深度扫描
- **Solo（$5/月）**：无限深度扫描，1 个智能体，扫描历史
- **Pro（$12/月）**：最多 5 个智能体，网页仪表盘，每周报告
- **Team（$25/月）**：无限智能体，优先扫描，告警通知

## 隐私

**本地模式不会发送任何数据。** 所有处理在你的机器上完成。

**深度模式仅发送聚合统计和模式标记。** 绝不发送原始内存内容、凭证或对话历史。

## 安装

```
clawhub install clawspa
```

开发者：[@whooshinglander](https://clawhub.com/whooshinglander)
