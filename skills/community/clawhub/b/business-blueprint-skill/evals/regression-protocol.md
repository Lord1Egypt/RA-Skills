# Eval Regression Protocol

Run this protocol after any change to SKILL.md, description, or references files.

## When to run

- After modifying SKILL.md description
- After modifying SKILL.md body structure
- After modifying any references file referenced by SKILL.md
- Before merging to master

## Steps

### 1. File existence check

```bash
grep -oE 'references/[^ `)+"'\'']+' SKILL.md | sort -u | while read f; do
  if [ -f "$f" ]; then echo "OK   $f"; else echo "MISS $f"; fi
done
```

All must be OK. If any MISS, stop and fix before proceeding.

### 2. Routing baseline

Read `evals/routing-baseline.json`. For each query, check:

- **hero_queries**: Must route to `kai-business-blueprint`. Check `expected_industry` and `expected_command` if specified.
- **negative_queries**: Must NOT route to `kai-business-blueprint`. Check `confused_with` field for which skill might incorrectly capture.
- **boundary_queries**: Check `desired_behavior`. "ambiguous" entries should trigger a clarification question.

Record results:

| Query ID | Pass/Fail | Notes |
|----------|-----------|-------|
| hero-01 | | |
| ... | | |

### 3. Reference integrity

For each hero query, verify the AI reads the correct references:

| Query | Should read | Should NOT read |
|-------|-------------|-----------------|
| hero-01 | entities-schema.md, systems-schema.md, blueprint-schema.md | domain-knowledge-extraction.md |
| hero-02 | domain-knowledge-extraction.md, knowledge-entities-schema.md | architecture-design-system.md |
| hero-03 | route-eligibility.md | entities-schema.md, blueprint-schema.md |
| hero-05 | architecture-design-system.md, microservices.md | domain-knowledge-extraction.md |

### 4. Token audit

Estimate total token load for each hero query scenario:

```
SKILL.md tokens + sum of references read for that scenario
```

Compare against baseline (old SKILL.md = ~278 lines ≈ 4000-5000 tokens loaded unconditionally).

## Report format

Save to `reports/eval-YYYYMMDD.md`:

```markdown
# Eval Report YYYY-MM-DD

## Changes tested
- [description of change]

## Results
- File existence: X/6 OK
- Hero queries: X/10 pass
- Negative queries: X/8 pass
- Boundary queries: X/6 pass
- Reference integrity: X/5 correct reads

## Regressions
- [list any failures]

## Token comparison
- Old: ~4500 tokens (278 lines unconditional)
- hero-01: [SKILL.md + refs read] = N lines ≈ M tokens
- hero-02: [SKILL.md + refs read] = N lines ≈ M tokens
```
