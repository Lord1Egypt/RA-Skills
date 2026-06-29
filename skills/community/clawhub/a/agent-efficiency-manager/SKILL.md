# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: agent-efficiency-manager
description: Agent 效率优化与自我进化管理器。定期分析所有 Agent 的 token 使用效率，识别可优化的技能配置，从 skillhub 发现并推荐新技能，自动推送优化建议，长期跟踪效率指标实现自我进化。触发场景：(1) 用户要求"优化 agent"、"降低 token 成本"、"提升效率", (2) 定期效率分析与推送, (3) 发现新技能并评估适用性, (4) 生成效率报告与优化建议
---

# Agent Efficiency Manager

Agent 效率优化与自我进化管理器，通过定期分析、智能推荐和持续跟踪，实现 Agent 长期自我优化。

## Workflow Decision Tree

```
用户请求优化
    ├─ 分析模式 → Run analyze_agent_efficiency.py
    ├─ 推荐模式 → Run fetch_skillhub_skills.py + generate_recommendations.py
    ├─ 跟踪模式 → Run track_metrics.py
    └─ 推送模式 → Run push_notifications.py
```

## Core Capabilities

### 1. 效率分析（analyze_agent_efficiency.py）

扫描 `openclaw.json` 中所有 Agent 配置，计算效率指标：

**指标定义（参见 references/metrics_definitions.md）：**
- `skill_count`：技能数量
- `estimated_tokens`：预估 token 消耗（每个 skill 约 500-1000 tokens）
- `efficiency_score`：效率评分（0-100，基于 skill 相关度）
- `redundancy_count`：重复/无关技能数量

**执行：**
```bash
python3 scripts/analyze_agent_efficiency.py --config ~/.qclaw/openclaw.json --output metrics.json
```

**输出：** JSON 格式效率报告，包含每个 Agent 的详细指标和优化建议。

---

### 2. 技能推荐（fetch_skillhub_skills.py + generate_recommendations.py）

从 skillhub 获取可用技能列表，基于 Agent 角色推荐适配技能：

**执行：**
```bash
# 步骤1：获取 skillhub 技能列表
python3 scripts/fetch_skillhub_skills.py --output available_skills.json

# 步骤2：生成推荐
python3 scripts/generate_recommendations.py --config ~/.qclaw/openclaw.json --available available_skills.json --output recommendations.json
```

**推荐逻辑（参见 references/recommendation_logic.md）：**
- 匹配 Agent 角色与技能描述
- 排除已安装的技能
- 优先推荐高评分、高频使用的技能
- 检测技能冲突（功能重复）

---

### 3. 指标跟踪（track_metrics.py）

长期记录效率指标，生成趋势分析：

**执行：**
```bash
python3 scripts/track_metrics.py --config ~/.qclaw/openclaw.json --history metrics_history.json --output trend_report.md
```

**跟踪内容：**
- Token 消耗趋势（按周/月）
- 技能数量变化
- 效率评分演变
- 优化建议采纳率

---

### 4. 自动推送（push_notifications.py）

通过企微/腾讯文档推送优化建议：

**执行：**
```bash
python3 scripts/push_notifications.py --recommendations recommendations.json --channel wecom --webhook YOUR_WEBHOOK_URL
```

**推送内容：**
- 每周效率报告
- 新技能推荐（附使用场景说明）
- 配置优化建议（具体 skills 增删列表）
- 成本节省预估

---

## Quick Start

### 场景 1：全量效率分析

用户说："分析所有 Agent 的效率，给出优化建议"

**执行流程：**
1. 运行 `analyze_agent_efficiency.py` 生成效率报告
2. 运行 `fetch_skillhub_skills.py` 获取可用技能
3. 运行 `generate_recommendations.py` 生成推荐
4. 输出综合优化建议（Markdown 格式）

### 场景 2：定期监控与推送

用户说："每周一早上 9 点推送效率报告"

**执行流程：**
1. 创建 cron 任务（`qclaw-cron-skill`）
2. 定时运行分析脚本
3. 生成报告并推送（企微/webchat）

### 场景 3：技能发现与评估

用户说："有没有新技能可以提升 Stock 大作手的效果？"

**执行流程：**
1. 运行 `fetch_skillhub_skills.py`
2. 针对 "stock" Agent 运行 `generate_recommendations.py`
3. 输出推荐技能列表（含评分和理由）

---

## Optimization Patterns

常见优化模式（详见 references/optimization_patterns.md）：

| 模式 | 做法 | Token 节省 |
|------|------|-------------|
| **去重** | 移除 `another_them` / `another-them` 重复 | ~1000 |
| **去无关** | 移除跨领域技能（股票 Agent 不留房产技能） | ~500-2000 |
| **精简基础** | 只保留 1-2 个基础配置技能 | ~500-1000 |
| **按需启用** | 一次性工具（如 `qclaw-migration`）不常驻 | ~500 |

---

## Resources

### scripts/

- `analyze_agent_efficiency.py`：效率分析脚本
- `fetch_skillhub_skills.py`：获取 skillhub 技能列表
- `generate_recommendations.py`：生成优化建议
- `track_metrics.py`：跟踪长期指标
- `push_notifications.py`：推送通知

### references/

- `metrics_definitions.md`：效率指标定义与计算方法
- `optimization_patterns.md`：常见优化模式与案例
- `recommendation_logic.md`：技能推荐逻辑详解

### assets/

（本技能无需静态资源）

---

## Notes

- **预估 token 消耗**：每个 skill 的 SKILL.md 约 500-1000 tokens，实际消耗取决于模型和内容长度
- **安全操作**：所有优化建议默认为"建议"模式，需用户确认后才执行 `config.patch`
- **定期运行**：建议每周运行一次完整分析，每日运行快速检查
- **自我进化**：跟踪优化建议的采纳情况，持续改进推荐算法
