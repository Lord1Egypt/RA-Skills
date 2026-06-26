# clawpolicy-publish

Publish-ready ClawHub skill wrapper for the public `DZMing/clawpolicy` project.

## Folder contents

- `SKILL.md` — publishable skill entry
- `references/` — upstream project references copied for review
- `scripts/verify_install.sh` — local smoke verification against PyPI

## Intended publish command

```bash
clawhub publish ./skills/clawpolicy-publish \
  --slug clawpolicy \
  --name "ClawPolicy" \
  --version 3.0.1 \
  --tags latest,policy,automation,governance \
  --changelog "Initial ClawHub release for ClawPolicy 3.0.1"
```
