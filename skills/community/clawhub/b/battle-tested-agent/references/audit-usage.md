# Audit Usage

## Run the audit

```bash
bash scripts/audit.sh ~/workspace
```

Or point it at any workspace:

```bash
bash scripts/audit.sh /path/to/workspace
```

The script checks for all **19** patterns and prints:
- what is present
- what is missing
- a total score
- the first missing pattern to address next

## Suggested rollout order

1. Fix missing **starter** patterns first
2. Add **intermediate** patterns for recurring operational work
3. Add **advanced** patterns only when the workspace actually orchestrates other agents or needs recurrence tracking

## Optional bootstrap snippets

If starting from scratch, copy the included assets into a workspace and then merge or customize them deliberately:

```bash
cp assets/AGENTS-additions.md ~/workspace/   # Review and merge into AGENTS.md
cp assets/QA-gates.md ~/workspace/QA.md
mkdir -p ~/workspace/.learnings
cp assets/learnings-template.md ~/workspace/.learnings/LEARNINGS.md
cp assets/errors-template.md ~/workspace/.learnings/ERRORS.md
cp assets/features-template.md ~/workspace/.learnings/FEATURE_REQUESTS.md
```

## What good looks like

- `SKILL.md` stays lean and discoverable
- the audit script remains the fast entrypoint
- detailed pattern content lives in `references/`
- assets stay optional and reusable
- teams implement only the patterns they actually need

## Notes

- This skill is not an onboarding wizard or persona pack
- Do not cargo-cult every pattern into every agent
- The point is fewer production failures, not more ceremony
