# Atlas Vuln Scanner Package

One-day launch package for the Atlas Smart Contract Vulnerability Pattern Scanner.

## Validate locally

```bash
python3 scripts/atlas_vuln_scanner.py --target demo/contracts --output demo/results
```

## Package contents

- `SKILL.md` — ClawHub/OpenClaw skill definition
- `scripts/atlas_vuln_scanner.py` — runnable heuristic scanner
- `demo/contracts/VulnerableVault.sol` — safe intentionally vulnerable demo input
- `demo/results/` — generated sample output after validation
- `listing/clawhub-listing.md` — ClawHub listing copy and publish command
- `MONETIZATION-PLAN.md` — free ClawHub lead magnet + paid Atlas skill cart strategy
- `PUBLISH-CHECKLIST.md` — publishing notes, gates, and validation evidence

## ClawHub publish status

Ready for ClawHub submission as a free MIT-0 skill, pending N8 approval and ClawHub login.

Public ClawHub docs currently show no native paid-skill/seller flow. Monetization should happen externally through Atlas robust scans, audit prep, private/pro workflows, or a separate paid bundle.

## Documented publish path

```bash
clawhub login

clawhub publish /Users/natemacdaddy/.hermes/workspace/atlas-security-skills/atlas-vuln-scanner \
  --slug atlas-vuln-scanner \
  --name "Atlas Smart Contract Vulnerability Pattern Scanner" \
  --version 0.1.0 \
  --tags latest,security,smart-contracts \
  --changelog "Initial release"
```
