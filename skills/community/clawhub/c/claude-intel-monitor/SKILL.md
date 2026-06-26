---
name: claude-intel-monitor
description: Detect intelligence degradation in Claude, GPT, and DeepSeek using 30 standardized Chinese benchmark questions across Math, Reasoning, and Code. Born from real "降智" (degradation) signals reported by Chinese developer communities.
version: 1.1.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [AI, Claude, GPT, DeepSeek, Benchmark, Model-Evaluation, Quality-Monitoring, Degradation-Detection]
    homepage: https://github.com/minirr890112-byte/claude-intel-monitor
prerequisites:
  commands: [claude-intel-monitor]
---

# claude-intel-monitor — AI 降智检测工具

Detect intelligence degradation in AI models with standardized benchmarks. 30 curated Chinese questions across Math, Reasoning, and Code — designed around real degradation patterns from the Chinese developer community.

## 痛点来源 (Pain Signal Origins)

"Claude/GPT 降智" was a top-3 hot topic during April-May 2026 Chinese developer community scans:
- CSDN: Multiple quantified analyses demonstrating Claude Opus 4.6 reasoning degradation (-67% depth, +98% hallucination)
- V2EX `claudecode` node: 12-reply hot thread on Claude Code behavior changes
- V2EX `deepseek` node: 4 posts on frequent service disruptions

## Quick Start

```bash
pip install claude-intel-monitor

# Test a model
claude-intel-monitor test --model claude-sonnet-4 --provider anthropic

# Set baseline for degradation detection
claude-intel-monitor baseline --model claude-sonnet-4

# View history
claude-intel-monitor history

# Continuous watch mode
claude-intel-monitor watch --model claude-sonnet-4 --provider anthropic --interval 6h
```

## Benchmark Structure

30 questions, 3 dimensions:

| Dimension | Count | Weight | Detection Target |
|-----------|-------|--------|------------------|
| Math | 10 | 1.0x | Mathematical reasoning, hallucination tendency |
| Reasoning | 10 | 1.2x | Logical reasoning, reduced safety awareness |
| Code | 10 | 1.3x | Code quality, architectural degradation |

All Chinese. Each answer validated by deterministic `check` functions (no AI grading bias).

## Featured Baseline: DeepSeek 91.1%

```
🧠 Testing deepseek-chat via deepseek — 30 questions

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      91.1%  ██████████████████░░  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📊 DeepSeek first live baseline: 27/30 (91.1%)
```

## Related Tools

- **[cursor-doctor](https://github.com/minirr890112-byte/cursor-doctor)** — Cursor IDE 错误诊断修复工具
- **[HermesMade](https://github.com/minirr890112-byte/HermesMade)** — 自动化痛点扫描平台
