## Critic Agent Configuration Reference

### Skill Metadata
- **Skill Slug**: `critic-agent`
- **Version**: 1.0.0
- **Location**: `skills/critic-agent/`

### Files
| File | Purpose |
|------|---------|
| `SKILL.md` | Full documentation |
| `_meta.json` | Skill metadata (version, slug) |
| `scripts/compute-score.js` | Compute weighted score from dimension scores |
| `scripts/critic-system-prompt.txt` | System prompt template for critic agent |
| `scripts/test-critic.sh` | Test scenario demonstration |
| `references/patterns.md` | Integration patterns and best practices |

### Configuration Options

When invoking critic (in agent code or workflow):

```json
{
  "critic": {
    "enabled": true,
    "model": "openrouter/anthropic/claude-3.5-sonnet",
    "thresholds": {
      "pass": 70,
      "needsRevision": 50,
      "fail": 0
    },
    "autoRetry": false,
    "maxRetries": 3,
    "onCriticError": "pass"
  }
}
```

#### Parameter Details

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | true | Master switch to enable/disable critic integration |
| `model` | string | agent's default | Model ID to use for critique (overrides default) |
| `thresholds.pass` | number | 70 | Minimum score to auto-approve delivery |
| `thresholds.needsRevision` | number | 50 | Minimum score to trigger auto-retry (if enabled) |
| `autoRetry` | boolean | false | If true, automatically regenerate when below `pass` |
| `maxRetries` | number | 3 | Maximum retry attempts before giving up |
| `onCriticError` | string | "pass" | Behavior on critic failure: `"pass"` (deliver anyway), `"reject"` (treat as fail), `"fail-safe"` (use heuristic fallback) |
| `temperature` | number | 0 | Temperature for critic model (0 recommended for deterministic scoring) |
| `timeout` | number | 30 | Timeout in seconds for critic API call |

### Input Schema (for script invocation)

When calling `compute-score.js` or spawning a critic:

```json
{
  "task": "string (the original prompt/task)",
  "agentOutput": "string (the content to critique)",
  "context": {
    "requirements": ["array of strings"],
    "constraints": ["array of strings"],
    "successCriteria": ["array of strings"]
  }
}
```

### Output Schema

Critic agent response (JSON):

```json
{
  "score": 85.5,
  "feedback": {
    "correctness": "...",
    "clarity": "...",
    "completeness": "...",
    "safety": "..."
  },
  "overall": "...",
  "suggestions": ["...", "..."],
  "dimensionScores": {
    "correctness": 85,
    "clarity": 80,
    "completeness": 70,
    "safety": 90
  }
}
```

### Using compute-score.js

```bash
# Input: JSON with dimension scores
echo '{"correctness":85,"clarity":80,"completeness":70,"safety":90}' | \
  node skills/critic-agent/scripts/compute-score.js

# Output:
# {
#   "score": 81.5,
#   "verdict": "good",
#   "breakdown": { ... }
# }
```

### Integration with AGENTS.md

Add rule to AGENTS.md:

```
## Critic Agent Integration

Before delivering final outputs:
1. Call critic using: openclaw agent --local -m "$(cat skills/critic-agent/scripts/critic-system-prompt.txt | template ...)" --json > critique.json
2. Parse score: SCORE=$(jq -r .score critique.json)
3. If SCORE >= 70: proceed
   Else if SCORE >= 50: auto-revise (max 2 retries)
   Else: reject and restart
4. Log all critiques to memory/critic-log.json
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | API key for LLM provider (required for --local agent calls) |
| `CRITIC_DEFAULT_MODEL` | Override default model (optional) |
| `CRITIC_LOG_PATH` | Path to critique log (default: `memory/critic-log.json`) |

### Troubleshooting Configuration

**Problem**: Critic always returns low scores
- **Check**: Is task description clear? Add more context.
- **Fix**: Adjust prompt to be more lenient or calibrate expectations.

**Problem**: Critic times out
- **Check**: Model endpoint reachable? API key valid?
- **Fix**: Set a lower `timeout`; use faster model; truncate long outputs.

**Problem**: Scores vary widely between runs
- **Check**: Temperature > 0? Model non-deterministic?
- **Fix**: Set `temperature: 0` in configuration.

**Problem**: Critic misses obvious errors
- **Check**: Model capability; prompt may need domain-specific instructions.
- **Fix**: Switch to more capable model; add explicit evaluation criteria to prompt.
