# Publish Metadata Proposal

## Recommended initial release metadata

- **Slug:** `benchmark-model-provider`
- **Display name:** `Benchmark Model Provider`
- **Version:** `1.0.0`
- **Tags:** `benchmark,models,providers,ranking,reporting`

## Recommended initial changelog

Initial release: user-specific benchmark spec generation, prompt-only and agent-context benchmark modes, sequential and orchestrated runs, scoring across quality/depth/cost with speed tracking, HTML/PDF reporting, and publish helpers for delivery workflows.

## Publish command template

```bash
clawdhub publish /home/quyt/clawd-dao/skills/benchmark-model-provider \
  --slug benchmark-model-provider \
  --name "Benchmark Model Provider" \
  --version 1.0.0 \
  --changelog "Initial release: user-specific benchmark spec generation, prompt-only and agent-context benchmark modes, sequential and orchestrated runs, scoring across quality/depth/cost with speed tracking, HTML/PDF reporting, and publish helpers for delivery workflows."
```

## Pre-publish checklist

- Confirm ClawdHub login is active (`clawdhub whoami`)
- Review `SKILL.md` description and wording one last time
- Ensure no generated scratch files or caches remain inside the skill folder
- Ensure examples and references are consistent with the actual scripts
- Decide whether to keep version `1.0.0` or bump before first publish
