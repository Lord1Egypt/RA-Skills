# Verification Patterns

Every agent should verify its output before delivering. Verification quality directly correlates with output quality.

## Principle

Don't trust first-pass output. Run it through a check. This can be a script, a checklist, or both. The point is: systematic validation catches what eyeballing misses.

## Implementation Options

### Option 1: Scripts in `agents/[name]/scripts/`
Automated checks that run on output files. Best for repeatable, measurable criteria.

### Option 2: Checklist in `agents/[name]/references/verification-checklist.md`
Manual checklist the agent reads before delivering. Best for subjective or context-dependent criteria.

### Option 3: Both
Use scripts for objective checks, checklist for subjective ones. This is the recommended approach.

## Verification by Role

### Research Agent
**Objective (scriptable):**
- Source count >= minimum threshold (from config.json)
- All URLs are reachable
- No source older than max_source_age_days
- No duplicate sources

**Subjective (checklist):**
- Multiple perspectives represented (not single-source bias)
- Key claims are attributed to specific sources
- Gaps in evidence are flagged, not hidden

### Content Agent
**Objective (scriptable):**
- Word count within target range
- No prohibited words/phrases
- Character count for tweets/threads
- Format matches template (headers, sections present)

**Subjective (checklist):**
- Tone matches target audience
- Hook is compelling (would you stop scrolling?)
- Call to action is clear
- No unintentional controversy

### Dev Agent
**Objective (scriptable):**
- Build passes
- Linter returns clean
- Tests pass (no regressions)
- No secrets in code

**Subjective (checklist):**
- Code change matches the requested scope (no scope creep)
- Error handling covers edge cases
- Performance implications considered

### Finance Agent
**Objective (scriptable):**
- All calculations verified with two methods
- Currency and units are consistent
- Percentages sum correctly where applicable
- Numbers are sourced (not hallucinated)

**Subjective (checklist):**
- Assumptions are stated explicitly
- Risk factors are mentioned
- Comparison baseline is fair

### Ops Agent
**Objective (scriptable):**
- Dates and times are valid and in correct timezone
- Recipients/contacts exist
- No scheduling conflicts

**Subjective (checklist):**
- Tone appropriate for recipient
- Priority level is correct
- Follow-up actions are clear

## Integration with SOUL.md

Add to every agent's Self-Improvement section:
```
5. Run verification before delivering output (see `references/verification-checklist.md`)
```

## Verification Failures

When verification fails:
1. Fix the issue before delivering
2. If the fix changes the substance of the output, note what changed
3. Log recurring verification failures in `.learnings/ERRORS.md`
