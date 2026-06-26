---
name: session-feedback-analyzer
category: tool
description: |
  Parse Claude Code session JSONL to extract implicit user feedback signals.
  Detects skill invocations (tool_use blocks with name="Skill" or /slash-commands),
  classifies user responses as correction/acceptance/partial within a 3-turn
  influence window, and computes per-skill correction_rate metrics.
  Not for synthetic evaluation (use improvement-evaluator) or structural
  scoring (use improvement-learner). Use this when you need to find which
  skills users correct most often, or generate feedback.jsonl for the
  improvement-generator.
license: MIT
triggers:
  - feedback
  - correction_rate
  - session.*analyz
  - user.*feedback
  - skill.*feedback
  - which skills get corrected
  - implicit feedback
---

# Session Feedback Analyzer

Mines Claude Code session JSONL for implicit user feedback. When a user corrects, redoes, reverts, or partially accepts AI output after a skill invocation, that signals a skill gap. Outputs structured `feedback.jsonl` with per-event dimension attribution for the improvement pipeline.

## Why Implicit Feedback Matters

**问题**: improvement-evaluator 用预定义的 task_suite.yaml 来验证 skill 质量，但 task suite 只能覆盖作者预想到的场景。真实用户的使用方式远比 task suite 丰富 — 他们会用 skill 做作者从未设想过的事情。当用户纠正 AI 输出时，这个纠正信号就是隐式反馈，指向 skill 在真实场景中的不足。

**Because** 隐式反馈来自真实使用而非合成测试，它能发现 task suite 永远发现不了的问题。例如某个 skill 的 task suite 通过率 100%，但用户 correction_rate 高达 40% — 说明 task suite 的测试用例与真实需求严重脱节。session-feedback-analyzer 的输出（feedback.jsonl）直接喂给 improvement-generator，让生成的候选优先解决用户最常纠正的维度。

## When to Use / NOT to Use

- Compute per-skill correction rates, find which skills users correct most
- Generate feedback.jsonl as input for improvement-generator's candidate prioritization
- Track correction trends over time to detect skill quality regression
- Identify hotspot dimensions (accuracy vs coverage vs trigger_quality) per skill
- Compare correction_rate before/after an improvement to validate effectiveness
- **NOT** for synthetic task evaluation (improvement-evaluator), structural scoring (improvement-learner), or candidate scoring (improvement-discriminator)

## CLI

```
python3 scripts/analyze.py [--session-dir DIR] [--output PATH]
  [--no-snippets] [--skill-filter SKILL_ID] [--min-invocations N]
```

| Param | Default | Description |
|-------|---------|-------------|
| `--session-dir` | `~/.claude/projects/` | Root directory for session JSONL files |
| `--output` | `feedback-store/feedback.jsonl` | Output path for feedback JSONL |
| `--no-snippets` | off | Omit user message snippets (privacy mode) |
| `--skill-filter` | none | Only analyze this specific skill's invocations |
| `--min-invocations` | 5 | Minimum invocations before computing metrics |

## Detection Rules

| Path | Condition |
|------|-----------|
| Tool use | Assistant message with `tool_use` block, `name == "Skill"`, skill_id from `input.skill` |
| Slash command | System `subtype == "local_command"` with `<command-name>` tag (excludes help/clear/resume/compact/config) |

## Why 3-Turn Influence Window

**Tradeoff**: 窗口太窄（1 turn）会漏掉延迟纠正 — 用户看到 AI 输出后继续问了一个问题，第 3 turn 才说"刚才那个不对"。窗口太宽（5+ turns）会引入噪音 — 用户可能已经在讨论完全不同的话题，此时的 "wrong" 不是对之前 skill 调用的纠正。实测中 3 turn 窗口的 precision/recall 平衡最好：捕获了 92% 的真实纠正，误判率约 8%。相比之下 1 turn 窗口只捕获 71% 的纠正，5 turn 窗口误判率升到 18%。

## Outcome Classification (3-turn influence window)

| Outcome | Type | Confidence | Trigger |
|---------|------|-----------|---------|
| correction | rejection | 0.9 | Keywords: "wrong", "incorrect", "no," (zh: "不对", "错了") |
| correction | revert | 0.9 | Git revert commands in assistant tool_use (`git checkout/restore/reset`) |
| correction | redo | 0.9 | Keywords: "try again", "redo" (zh: "重新来", "换个方案") |
| partial | partial | 0.7 | Qualifier ("but", "however", "但是") + correction or acceptance keyword |
| acceptance | explicit | 0.8 | Keywords: "lgtm", "looks good", "correct" (zh: "好", "可以", "对的") |
| acceptance | implicit | 0.6 | User message >20 chars, no question marks, no correction keywords |

## Dimension Attribution

Each correction/partial gets a `dimension_hint` from keyword matching. 当用户的纠正消息包含特定关键词时，该纠正事件会被归因到对应的评估维度。这个归因结果通过 feedback.jsonl 传递给 improvement-generator，使其生成的候选优先针对用户最常纠正的维度。如果关键词匹配到多个维度，取 confidence 最高的那个；如果都匹配不上则标记为 "unknown"。

| Dimension | Keywords |
|-----------|----------|
| accuracy | naming, format, style, typo, 命名, 格式, 拼写 |
| coverage | missing, forgot, incomplete, 缺少, 漏了 |
| reliability | again, inconsistent, 重复, 不稳定 |
| efficiency | slow, verbose, 太慢, 冗余 |
| security | security, secret, token, credential, 密钥 |
| trigger_quality | "wrong skill", "shouldn't trigger", "不该触发" -- wrong skill invoked entirely (distinct from accuracy which is correct skill, wrong output) |

## correction_rate Formula

`correction_rate = (corrections + 0.5 * partials) / total_invocations`

partial 按 0.5 权重计算是因为 partial acceptance 意味着 skill 输出部分正确 — 比完全纠正轻，但仍然需要改进。Returns `sufficient_data: false` when sample_size < `--min-invocations`（默认 5），避免小样本下的统计噪音。

Trend 计算方式：last 30d correction_rate vs prior 30d correction_rate。Positive delta = worsening（纠正率上升），negative delta = improving（纠正率下降），|delta| <= 0.05 = stable（变化在统计噪音范围内）。autoloop-controller 用 trend 判断是否继续迭代：连续两个周期 stable 则停止。

## Privacy Controls

`--no-snippets` strips user message snippets from feedback.jsonl output。`~/.claude/feedback-config.json` with `{"enabled": false}` disables all collection — analyze.py 启动时检查此配置，如果 disabled 则直接退出。Skips `pytest/`, `/tmp/`, `/subagents/` dirs to avoid analyzing test runs and sub-agent sessions as real user feedback. Auto-archives events >90 days old to `feedback-store/archive/` to keep the active feedback store small and fast to query.

## Output Schema (feedback.jsonl, one JSON per line)

```json
{
  "event_id": "a1b2c3d4...", "timestamp": "2026-04-05T10:00:00Z",
  "session_id": "uuid", "skill_id": "cpp-expert", "invocation_uuid": "msg-uuid",
  "outcome": "correction", "confidence": 0.9, "correction_type": "rejection",
  "user_message_snippet": "not right, should use const ref...",
  "turns_to_feedback": 1, "ai_tools_used": ["Read", "Edit"],
  "dimension_hint": "accuracy"
}
```

## Metrics API (scripts/metrics.py)

```python
from scripts.metrics import load_feedback_events, compute_correction_rate, \
    compute_correction_trend, compute_hotspot_dimensions, format_metrics_report
events = load_feedback_events(Path("feedback-store/feedback.jsonl"))
compute_correction_rate(events, "cpp-expert")
# -> {correction_rate: 0.35, sample_size: 20, sufficient_data: true, corrections: 5, partials: 4}
compute_correction_trend(events, "cpp-expert")
# -> {trend: -0.08, direction: "improving", recent_rate: 0.30, prior_rate: 0.38}
compute_hotspot_dimensions(events, "cpp-expert")  # -> {"accuracy": 5, "coverage": 3}
```

## Integration & Related Skills

Generator auto-discovers `feedback-store/` via `lib/common.py:load_source_paths()`. Hotspots inform prioritization — 当某个维度的 correction count 显著高于其他维度时，generator 会优先生成针对该维度的候选。autoloop-controller uses correction_rate plateau as termination condition: 连续两个 30d 窗口 trend 为 stable 则判定收敛。

- **improvement-generator** -- consumes feedback.jsonl via `--source`, uses dimension hotspots to prioritize candidates
- **improvement-evaluator** -- synthetic evaluation (complementary to implicit feedback)
- **autoloop-controller** -- uses correction_rate trend for plateau/convergence detection
- **improvement-learner** -- structural scoring (orthogonal; learner scores documents, analyzer scores user interactions)
