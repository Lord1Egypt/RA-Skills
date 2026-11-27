# Vetting Report: api-proxy
**Date:** 2026-09-13 08:11 EDT
**Vetter:** JARVIS (skill-vetter skill)
**Source:** local (/home/jarvis/.openclaw/workspace)
**Verdict:** PASS
**Risk score:** 8/100

## Findings

### Critical
- (none)

### Warnings
- 2 network URLs
- No description in frontmatter

### Notes
- (none)

## Permission footprint
- Tools requested: exec process read write 

## Network footprint
https://api.openai.com/v1/chat/completion
https://attacker.com/api?provider=openai` will NOT receive the key becau

## Side effects
- Reads: SKILL.md
- Writes: VET-REPORT.md (this file)
- Network: 2 distinct hosts

## Verdict rationale
Score 8/100 with 0 critical findings and 2 warnings.
