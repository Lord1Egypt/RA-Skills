## User Feedback Loop (Design)

### Problem

The existing evaluator measures skill effectiveness via synthetic task suites -- predefined prompts with mechanical judges. This catches structural gaps but misses real-world failure modes that only surface during actual use. A skill might pass all 7 task suite tests yet consistently produce output that users correct in practice.

We need a feedback signal derived from **actual user behavior** in Claude Code sessions.

### Architecture

```
~/.claude/projects/**/*.jsonl          distill (existing)
         |                                  |
         v                                  v
  +------------------+              +----------------+
  | session-analyzer |              | pattern-index  |
  | (new component)  |              | (distill's DB) |
  +--------+---------+              +-------+--------+
           |                                |
           v                                |
  +-----------------+                       |
  | feedback-store  |  <--------------------+
  | feedback.jsonl  |    distill can write
  +--------+--------+    correction patterns
           |              into the same store
           v
  +--------------------+
  | correction_rate    |--- per-skill metric
  | by skill+dimension |
  +--------+-----------+
           |
           v
  +-------------------+       +-------------------+
  | improvement-      |       | autoloop-         |
  | generator         |       | controller        |
  | (existing Stage 1)|       | (existing)        |
  +-------------------+       +-------------------+
  reads correction_rate        uses correction_rate
  to prioritize which         as termination signal
  dimensions to fix           (plateau = users
                              stopped correcting)
```

### Data Collection

#### Source: Claude Code session JSONL

Each session is a file at `~/.claude/projects/{project-hash}/{session-id}.jsonl`. Lines are JSON objects with these relevant fields:

```jsonc
// Skill invocation (assistant turn)
{
  "type": "assistant",
  "message": {
    "content": [{
      "type": "tool_use",
      "name": "Skill",             // <-- skill trigger signal
      "input": { "skill": "cpp-expert", "args": "..." },
      "id": "toolu_xxx"
    }]
  },
  "uuid": "aaa-bbb",
  "timestamp": "2026-04-04T08:00:00Z"
}

// Slash-command skill invocation (system entry)
{
  "type": "system",
  "subtype": "local_command",
  "content": "<command-name>/code-review</command-name>...",
  "uuid": "ccc-ddd",
  "timestamp": "..."
}

// User message (potential correction or acceptance)
{
  "type": "user",
  "message": { "role": "user", "content": "不对，应该用X而不是Y" },
  "uuid": "eee-fff",
  "parentUuid": "aaa-bbb",     // links to prior assistant turn
  "timestamp": "..."
}
```

#### Skill trigger detection

A "skill invocation event" is detected when either:

1. An assistant message contains `tool_use` with `name == "Skill"` -- extract `input.skill` as the skill name.
2. A system message with `subtype == "local_command"` contains a `<command-name>` matching a known skill slash-command.

Both produce an `invocation_id` (the message UUID) and a `skill_id`.

#### Correction vs. acceptance detection

After a skill invocation, scan forward through subsequent messages in the same session to classify the outcome. The "influence window" extends from the skill invocation until 3 user turns later or the next skill invocation, whichever comes first.

**Correction signals** (negative -- user overrides AI output):

| Pattern | Detection | Confidence |
|---------|-----------|------------|
| Explicit rejection | User message contains negation keywords: "不对", "错了", "wrong", "no", "不是这样" | High |
| Direction override | User rewrites the AI's output via their own edit (detectable when next user message contains code/text that contradicts the AI's prior output) | Medium |
| Immediate redo request | User says "重新来", "redo", "try again", "换个方案" within 1 turn | High |
| Revert signal | `git checkout`/`git restore` in a Bash tool_use within 2 turns after AI made file edits | High |
| Partial correction | User accepts some output but corrects specific parts: "这个可以，但是X应该改成Y" | Medium (counted as 0.5 correction) |

**Acceptance signals** (positive -- user proceeds without correction):

| Pattern | Detection |
|---------|-----------|
| Silent continuation | User's next message changes topic or gives new task (no correction of prior output) |
| Explicit approval | "好", "可以", "looks good", "对的", "继续" |
| Build on output | User takes AI output and extends it (references AI's generated names/code in their next request) |

**Ambiguous (excluded from metrics)**:

- User asks clarifying question (neither acceptance nor correction)
- Session ends immediately after skill invocation (no signal)
- AI self-corrects before user responds (not a user feedback signal)

### Extracted Event Schema

```jsonc
// Written to feedback-store/feedback.jsonl (append-only)
{
  "event_id": "sha256-of-session+invocation_uuid",
  "timestamp": "2026-04-04T08:05:00Z",
  "session_id": "90d58f86-...",
  "project": "NanoCompose",
  "skill_id": "cpp-expert",
  "invocation_uuid": "aaa-bbb",
  "outcome": "correction",        // "correction" | "acceptance" | "partial"
  "confidence": 0.9,              // how sure we are about the classification
  "correction_type": "rejection", // "rejection" | "override" | "redo" | "revert" | "partial"
  "user_message_snippet": "不对，应该...",  // first 200 chars, for debugging
  "turns_to_feedback": 1,         // how many user turns after invocation
  "ai_tools_used": ["Read", "Edit", "Bash"],  // what AI did after skill load
  "dimension_hint": null          // optional: which quality dimension was corrected
}
```

### Metrics

#### Primary metric: `correction_rate`

```
correction_rate(skill) = (corrections + 0.5 * partials) / total_invocations
```

Where `total_invocations` = corrections + partials + acceptances (excludes ambiguous).

#### Edge cases

| Edge case | Handling |
|-----------|----------|
| Skill triggered but not used (loaded then ignored) | If AI makes no tool calls after skill load within 3 turns, exclude from metrics. Detectable: no `Read`/`Edit`/`Bash` tool_use between skill invocation and next user message. |
| Multi-turn corrections | Only count the first correction signal within the influence window. Subsequent corrections about the same topic count as one event. |
| Multiple skills in one turn | Attribute correction to the most recently invoked skill before the correction. If ambiguous, attribute to all active skills with `confidence *= 0.5`. |
| Skill invoked by subagent | Subagent sessions live in `{session-id}/subagents/agent-*.jsonl`. Process identically but tag `context: "subagent"`. Subagent corrections are from the orchestrator (not the user) -- lower weight (0.3x). |
| Very low sample size | Do not compute `correction_rate` until a skill has >= 5 invocations with signal. Below that threshold, report "insufficient data". |

#### Derived metrics

```
correction_trend(skill, window=30d) = correction_rate(last_30d) - correction_rate(prior_30d)
                                      // positive = getting worse
                                      // negative = improving

hotspot_dimensions(skill) = group corrections by dimension_hint
                            // e.g., "cpp-expert: 60% of corrections are about naming"
```

### Dimension attribution

When a correction occurs, attempt to classify which of the 6 evaluator dimensions it maps to:

| Correction content pattern | Dimension |
|---------------------------|-----------|
| Naming, formatting, style complaints | accuracy |
| "Missing X", "didn't consider Y" | coverage |
| Repeated similar corrections across sessions | reliability |
| "Too slow", "too many steps", "too verbose" | efficiency |
| Security-related corrections | security |
| Wrong skill triggered, wrong workflow chosen | trigger_quality |

This attribution is heuristic (keyword + LLM classification on the 200-char snippet). When unsure, set `dimension_hint = null`.

### Integration with Improvement Pipeline

#### 1. As generator input signal

The improvement-generator already reads "feedback signals" from files. Add `feedback-store/feedback.jsonl` as a new source:

```
improvement-generator --target /path/to/skill --source feedback-store/feedback.jsonl
```

The generator reads corrections for the target skill, groups by dimension, and prioritizes improvement candidates that address the most-corrected dimensions.

#### 2. As evaluator dimension

Add `user_correction_rate` as a 7th dimension to the benchmark-store Pareto front:

```
Existing:  accuracy, coverage, reliability, efficiency, security, trigger_quality
New:       + user_correction_rate (weight: 25%, sourced from feedback-store)
```

The Pareto front's regression gate then enforces: an "improvement" that increases task suite pass rate but worsens user correction rate is rejected.

**Bootstrap problem**: New/changed skills have no user feedback yet. Use the existing 6-dimension score as a proxy until >= 5 real invocations accumulate. `user_correction_rate` weight ramps linearly from 0% (0 invocations) to 25% (>= 20 invocations).

#### 3. As autoloop-controller signal

Add a new termination condition to autoloop-controller:

```python
# New condition: user feedback plateau
# If correction_rate has not decreased over the last N improvement iterations,
# the autoloop is not helping real users -- stop and flag for human review.
def detect_user_feedback_plateau(feedback_store, skill_id, iterations):
    rates = [compute_correction_rate(skill_id, after=iter.timestamp)
             for iter in iterations[-3:]]
    return all(r >= rates[0] * 0.95 for r in rates[1:])
```

Also: autoloop-controller should prefer improving skills with the **highest correction_rate** when choosing which skill to target next in batch mode.

#### 4. Integration with distill

distill already watches `~/.claude/projects/**/*.jsonl` and extracts patterns. Two integration options:

**Option A (preferred): distill writes to feedback-store directly.** distill's pattern extraction already identifies repeated user corrections. Add a distill output mode that writes correction events in the schema above to `feedback-store/feedback.jsonl`. The session-analyzer component becomes optional -- distill handles the parsing.

**Option B: Independent processing.** session-analyzer runs as a separate cron job, parses JSONL independently of distill. Simpler to implement but duplicates the JSONL parsing work that distill already does.

### Privacy and Scope

- **Local only**: All data stays in `~/.claude/` and the project's `feedback-store/` directory. No external telemetry, no network calls.
- **User message snippets**: Capped at 200 characters, used only for dimension attribution debugging. Can be disabled with `--no-snippets` flag.
- **No PII extraction**: The analyzer never extracts full user messages, file contents, or code. Only metadata (skill name, outcome, timestamp) and short snippets.
- **Opt-out**: A `.claude/feedback-config.json` with `{"enabled": false}` disables all collection.
- **Data retention**: feedback.jsonl entries older than 90 days are archived to `feedback-store/archive/` and excluded from active metrics.

### Key Design Decisions

**Why not use the existing evaluator task suites for this?** Task suites test known scenarios. User feedback catches unknown scenarios -- the gap between what we tested and what users actually do. They are complementary, not substitutes.

**Why append-only JSONL (not SQLite)?** Matches the session log format. Easy to grep, tail, and debug. distill already processes JSONL. SQLite adds a dependency for no benefit at the expected scale (~100-1000 events per skill per month).

**Why a 3-turn influence window?** Empirically observed in our session logs: corrections almost always come within 1-2 user turns. By turn 3, the user has typically moved on to a new topic. A wider window would increase false positives (attributing unrelated complaints to the skill).

**Why 0.5 weight for partial corrections?** A partial correction means the skill got the direction right but missed details. This is less severe than a full rejection but still indicates room for improvement. The 0.5 weight prevents partial corrections from dominating the metric while still counting them.

