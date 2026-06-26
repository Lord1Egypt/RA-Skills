---
name: auto-improvement-orchestrator
version: 2.0.0
description: >
  Skill 自动评估和改进管线。9 维结构评分（含 LLM-as-Judge）、4 角色加权、
  类别修正系数（tool/knowledge/orchestration/rule）、Pareto front 回归保护
  （security 2%/efficiency 10%/其他 5%）、trace-aware 失败重试。
  包含 11 个管线 skill + 2 个辅助工具 + 2 个验证目标。
  不用于单个 skill 的手动编辑（直接改 SKILL.md）。
  参见 execution-harness（agent 执行可靠性，独立仓库）。
license: MIT
triggers:
  - skill quality
  - skill evaluation
  - auto improvement
  - self improvement
  - 自动改进
  - 评分
  - skill 质量
  - pareto
  - learner
  - orchestrator
author: OpenClaw Team
---

# Auto-Improvement Orchestrator

从评估到改进到验证的完整管线，让 Skill 自动变好。

## When to Use

- 评估一个 skill 的质量（9 维打分 + 4 角色评审）
- 自动改进 SKILL.md（生成候选→打分→执行→门禁）
- 批量改进多个 skill（autoloop 连续运行）
- 从 Claude Code 会话日志提取用户反馈信号
- 对比 skill 改进前后的 Pareto front

## When NOT to Use

- 手动编辑单个 SKILL.md → 直接改文件
- Agent 执行可靠性 → 用 execution-harness（独立仓库）
- 纯文档生成 → 用 doc-gen
- Prompt 优化（token 级）→ 用 DSPy

## Quick Start

```bash
# 打分
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /your/skill --max-iterations 1

# 自动改进 5 轮
python3 skills/improvement-learner/scripts/self_improve.py \
  --skill-path /your/skill --max-iterations 5

# 从会话日志提取反馈
python3 skills/session-feedback-analyzer/scripts/analyze.py \
  --output feedback.jsonl
```

## Architecture

11 个管线 skill 分三层：

- **评估层**: learner（9 维结构评分）、evaluator（执行测试）、session-feedback（用户反馈）
- **改进层**: generator → discriminator → evaluator → executor → gate（6 层门禁）
- **控制层**: autoloop（连续运行）、benchmark-store（Pareto front）、execution-harness（独立仓库）

辅助工具: skill-forge（造 skill）、skill-distill（合并 skill）
验证目标: prompt-hardening、deslop

## Related

- [execution-harness](https://github.com/lanyasheng/execution-harness) — Agent 执行可靠性（38 patterns × 6 axes）
