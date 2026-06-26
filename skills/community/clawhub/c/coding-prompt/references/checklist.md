## 1. Prompt Diagnosis Checklist

Use this checklist in **Mode 1 (explicit optimization)**. Run through each item and report only the signals that clearly fire — when in doubt, skip it.

| # | Signal | What to check |
|---|--------|---------------|
| D1 | **No background** | Is there enough project context for an AI unfamiliar with the codebase to understand the task? |
| D2 | **No constraints** | Are there clear "must NOT" boundaries? Vague "should" without hard limits will drift. |
| D3 | **No deliverable** | Is the expected output format and quality standard explicitly stated? |
| D4 | **No scenario** | Is the requirement described from the user's perspective, or only in technical terms? |
| D5 | **No validation** | Does the prompt ask AI to diagnose current state before acting? (See principles 2.4) |
| D6 | **No questioning** | For non-trivial features, does the user ask AI to question whether the feature is needed? (See principles 2.5) |
| D7 | **No priority** | Does the prompt contain 3+ requirements without explicit priority ordering? |
| D8 | **No output control** | Is the expected response format unspecified? (code only? explanation? table?) |
| D9 | **No dependency** | Does the task rely on unfinished work that isn't declared as a prerequisite? |
| D10 | **Stale context** | Has the conversation exceeded ~10 turns since key constraints were last stated? |
| D11 | **Rule-based bias** | Is AI choosing hardcoded rules/regex/scoring when LLM-native approach would be simpler and better? |
| D12 | **Fake completion** | Did AI claim "done" but deliver stubs, TODOs, placeholder returns, or sample data? |

**Note**: D11 and D12 are also used in **Mode 2 (active monitoring)** for proactive alerts. The rest are only reported upon explicit request.
