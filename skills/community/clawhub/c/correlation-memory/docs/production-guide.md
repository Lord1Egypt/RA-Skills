# OpenClaw Correlation Plugin — Production Guide

This guide supplements the [README](./README.md) with lessons from live production deployments. If you're running the correlation plugin in anger, these notes will save you time.

---

## 1. Overview

The README covers the what and why. This guide covers the **how in practice**:
- How to integrate correlation surfacing into your heartbeat loop
- How to tune confidence thresholds without drowning in noise
- How to manage the rule lifecycle without making a mess
- What actually goes wrong in production, and how to debug it

---

## 2. Heartbeat Integration

The correlation plugin shines when it surfaces context *proactively*, not just when you remember to ask. The recommended integration point is your OpenClaw heartbeat.

### Pattern: Surfacing on every N heartbeats

In your `HEARTBEAT.md`, add a periodic check that looks at what you're currently working on and surfaces related contexts:

```bash
# HEARTBEAT.md

## Periodic Tasks

### Correlation Surfacing (every 5 heartbeats)
When working on a topic, check correlation rules to surface related contexts:
bash scripts/correlation-surfacing.sh "<current topic keywords>"
```

The `correlation-surfacing.sh` script reads your current context (passed as argument), matches it against `memory/correlation-rules.json`, and outputs what else you should know.

**Script location:** Place the script in your OpenClaw workspace scripts directory (e.g., `~/.openclaw/workspace/scripts/correlation-surfacing.sh`). The script is available in the plugin repository under `scripts/`.

```bash
# Example invocation
bash scripts/correlation-surfacing.sh "config change"
```

Output:
```json
{
  "context": "config change",
  "matched": 1,
  "rules": [{
    "id": "cr-001",
    "trigger": "config-change",
    "fetches": ["backup-location", "rollback-instructions", "recent-changes"]
  }]
}
```

**Why every 5 heartbeats and not every one?** Correlation surfacing fires a memory search per matched rule. On busy systems, every heartbeat is too aggressive. Every 5 gives you regular enrichment without token burn.

### What to pass as context

The script accepts natural language. Good context strings:
- `"config change"` — fires the config-safety rules
- `"error 400 gateway"` — fires error-debugging + gateway rules
- `"plugin install"` — fires plugin-management rules

Bad context strings (too generic, fire too often):
- `"help"` — no rule should trigger on this
- `"status"` — too broad

---

## 3. Tuning Confidence Thresholds

Confidence (`0.0`–`1.0`) controls how strongly a rule's correlation is weighted. Getting this right is the difference between useful surfacing and noise.

### Practical guide

| Confidence | When to use | Example |
|------------|-------------|---------|
| `0.95–0.99` | Critical operations where getting this wrong is expensive | Config changes, gateway restarts, plugin installs |
| `0.85–0.90` | High-value patterns that reliably indicate the context | Backup operations, error debugging |
| `0.70–0.80` | Useful correlations but with some false-positive risk | Session recovery, git operations |
| `< 0.70` | Exploratory rules or very niche patterns | Almost never needed in practice |

### The mistake everyone makes at first

Setting everything to `0.95` because "high confidence sounds better." This causes **signal drowning**: your high-confidence rules dominate every search, and you never see the lower-confidence correlations that might actually be relevant to the current situation.

**Rule of thumb:** Only use `0.95+` for operations where the cost of missing the correlation is *catastrophic* (gateway down, data loss). Everything else `0.70–0.90`.

### Tuning procedure

1. Deploy a new rule with `lifecycle.state: "testing"` and confidence `0.70`
2. Run your heartbeat for a few days, watch how often it fires
3. If it fires on every unrelated query → lower confidence or narrow keywords
4. If it never fires when it should → widen keywords or raise confidence
5. When stable, move to `validated`

---

## 4. Lifecycle Management

Rules are not static. They have a lifecycle from idea to retirement.

```
proposal → testing → validated → promoted → retired
```

### What each state means

**`proposal`** — A new idea for a correlation rule. Written with lower confidence (`0.60–0.75`), deployed in testing mode only. Not active by default unless you explicitly enable proposal rules.

**`testing`** — The rule is live but being evaluated. You'll see it fire but it won't auto-surface until validated. Set confidence based on how sure you are.

**`validated`** — The rule fires correctly and the signal-to-noise ratio is acceptable. It is now active.

**`promoted`** — The rule is rock-solid. High confidence (`0.90+`), well-tested, and you want it to always be available. Only promoted rules should have confidence `0.99`.

**`retired`** — The rule is obsolete. Maybe the pattern it detected no longer exists, or it was replaced by a better rule. Keep it in the file (with `retired`) rather than deleting it — this preserves the `learned_from` history.

### Practical workflow

When you discover a new correlation pattern:

1. Add rule as `proposal` with `confidence: 0.70`
2. After a week of testing, move to `testing`
3. After validation (noise acceptable), move to `validated`
4. After 30+ firings with no issues, consider `promoted`

Don't rush promotion. A premature `promoted` rule with `0.99` confidence that fires inappropriately is hard to undo because people trust it.

---

## 5. Common Pitfalls

### Pitfall 1: Keywords that fire too often

`trigger_keywords: ["error"]` will fire on almost every message in a development channel. This makes the rule useless because it always fires but rarely means anything.

**Fix:** Be specific. `["error", "400", "crash"]` — require 2+ keywords to co-occur, or use a specific phrase as the `trigger_context`.

### Pitfall 2: Fetching non-existent contexts

A rule that says `must_also_fetch: ["recovery-procedures"]` but there's no file at `memory/recovery-procedures.md` silently does nothing. The plugin doesn't warn you.

**Fix:** Always verify that every context in `must_also_fetch` actually exists in your memory directory.

### Pitfall 3: Overlapping rules

Rule A triggers on `["config"]`, Rule B triggers on `["change"]`. Both fire on `"config change"`. Now you get duplicate surfacing.

**Fix:** Before adding a rule, search existing rules for keyword overlap. Use distinct `trigger_context` values to keep rules distinguishable.

### Pitfall 4: Confidence theft

Rule A (`confidence: 0.99`) always fires on your context. Rule B (`confidence: 0.85`) would also be relevant but Rule A's results dominate.

**Fix:** If a `0.99` rule fires on every config operation, ask: does it need to be that high? Reduce to `0.90` and let lower rules breathe.

### Pitfall 5: No `learned_from`

Rules without `learned_from` are impossible to audit. When the rule fires incorrectly in 6 months, you won't remember why you created it.

**Fix:** Every rule needs a `learned_from` that names the incident, pattern, or lesson that prompted it. Keep it descriptive but concise.

---

## 6. Debugging

### Using `correlation_check`

The plugin provides a debug tool to check which rules match a given context:

```bash
openclaw exec correlation_check --context "config change"
```

This shows:
- Which rules matched
- Why they matched (which keywords fired)
- What contexts they would fetch

### Tracing a specific rule

```bash
openclaw exec correlation_check --rule-id cr-001 --context "openclaw.json edit"
```

### Reading the output

If a rule **should** fire but doesn't:
1. Check that your keywords appear in the context string
2. Check that `trigger_context` matches the semantic domain
3. Check the rule's lifecycle state — `proposal` rules need explicit enabling

If a rule fires **when it shouldn't**:
1. The keywords are too broad → narrow them
2. Confidence too high → lower it
3. Context is wrong → the same keyword can mean different things in different contexts

---

## 7. Troubleshooting

### Rule fires but fetches nothing

Most common cause: one or more contexts listed in `must_also_fetch` don't exist as files in your memory directory.

**Fix:** Run `ls memory/` and verify every referenced context has a corresponding file. Create missing ones or remove the reference.

### Rule doesn't fire when it should

1. Check that your `trigger_keywords` actually appear in the context string you're passing
2. Verify the rule's `lifecycle.state` — `proposal` rules need explicit opt-in
3. Try the `correlation_check` tool directly:
   ```bash
   openclaw exec correlation_check --context "your context here"
   ```
4. If keywords overlap with another higher-confidence rule, the lower-confidence rule's results may be buried

### Getting duplicate results

Two rules firing on the same context and fetching overlapping contexts. 

**Fix:** Review both rules' `must_also_fetch` lists for overlap. Narrow keywords on one of the rules, or reduce its confidence so the other dominates.

### Too much noise after adding a rule

The rule fires on almost every query.

**Fix:** Raise the confidence threshold, or narrow the keyword list. A rule with `confidence: 0.70` that fires constantly should probably be `0.50` or removed.

### Rule worked fine, then started causing noise

`usage_count` is high but signal-to-noise has degraded. This usually means the operational pattern changed (new tool, new workflow) and the rule's keywords are now triggering in unrelated contexts.

**Fix:** Narrow the keywords, or set `lifecycle.state: "testing"` to stop auto-surfacing while you recalibrate.

---

## 8. When NOT to Use Correlation Rules

Correlation rules are powerful but not universal. Avoid them when:

**1. The relationship is 1:1, not N:M**
If "when X happens, always do Y" — that's automation, not correlation. Write a script.

**2. The keyword is too common**
Words like "help", "check", "status", "info" fire on almost everything. They'll generate noise, not signal.

**3. The contexts don't exist**
If you reference `memory/recovery-procedures.md` but never created that file, the correlation silently fails. Only reference contexts you actually maintain.

**4. The pattern is genuinely one-off**
If it happened once and won't happen again, don't write a rule. Just document it.

**5. You need exact precision**
Correlation is probabilistic. If you need guaranteed checks (e.g., security compliance), use deterministic rules or scripts, not correlation confidence scoring.

---

## Appendix: Minimal Rule Checklist

Before deploying a new rule, verify:

- [ ] Keywords are specific enough not to fire on every message
- [ ] All `must_also_fetch` contexts exist in memory/
- [ ] `confidence` is appropriate (not everything needs 0.95)
- [ ] `learned_from` describes why this rule exists
- [ ] `lifecycle.state` is set (default to `testing` for new rules)
- [ ] No existing rule has significant keyword overlap
