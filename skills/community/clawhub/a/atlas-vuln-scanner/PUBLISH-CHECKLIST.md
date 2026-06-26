# Publish Checklist — Atlas Vuln Scanner v0.1

## Package
- [x] Skill definition: `SKILL.md`
- [x] Runnable scanner: `scripts/atlas_vuln_scanner.py`
- [x] Safe demo contract: `demo/contracts/VulnerableVault.sol`
- [x] Generated sample outputs: `demo/results/`
- [x] Listing copy: `listing/clawhub-listing.md`
- [x] ZIP package: `../atlas-vuln-scanner-clawhub-v0.1.zip`

## Validation run
```bash
python3 scripts/atlas_vuln_scanner.py --target demo/contracts --output demo/results
python3 -m py_compile scripts/atlas_vuln_scanner.py
python3 -m zipfile -l ../atlas-vuln-scanner-clawhub-v0.1.zip
```

Result: PASS — demo scans 1 Solidity file and emits 9 heuristic flags plus report/candidates/exec summary.

## Spy research: ClawHub process
Sources reviewed by Spy:
- https://clawhub.ai
- https://github.com/openclaw/clawhub
- https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
- https://github.com/openclaw/clawhub/blob/main/docs/cli.md
- https://github.com/openclaw/clawhub/blob/main/docs/http-api.md
- https://github.com/openclaw/clawhub/blob/main/docs/auth.md

Findings:
- ClawHub is a public OpenClaw skill registry for `SKILL.md` plus supporting files.
- Skills publish through web UI (`/publish-skill`), CLI (`clawhub publish <path>`), or HTTP API (`POST /api/v1/skills`).
- Publish target should be the folder, not the ZIP, for the documented CLI path.
- Login is GitHub OAuth; CLI uses API tokens after login.
- Skill packages must include `SKILL.md` or `skill.md` and text-based supporting files.
- Server extracts YAML frontmatter metadata from `SKILL.md`.
- ClawHub runs static/security/moderation scans.
- Published ClawHub skills are MIT-0.
- ClawHub explicitly does **not** support paid skills, per-skill pricing, paywalls, revenue sharing, seller onboarding, Stripe, payouts, or KYC.

## ClawHub listing fields
- Slug: `atlas-vuln-scanner`
- Display name: `Atlas Smart Contract Vulnerability Pattern Scanner`
- Version: `0.1.0`
- Tags: `latest`, `security`, `smart-contracts`
- Changelog: `Initial release`
- License acceptance: MIT-0 required by ClawHub

## Publish command
```bash
clawhub login

clawhub publish /Users/natemacdaddy/.hermes/workspace/atlas-security-skills/atlas-vuln-scanner \
  --slug atlas-vuln-scanner \
  --name "Atlas Smart Contract Vulnerability Pattern Scanner" \
  --version 0.1.0 \
  --tags latest,security,smart-contracts \
  --changelog "Initial release"
```

## Approval gates before external publish
- [ ] N8 approval to publish this as free MIT-0 on ClawHub.
- [ ] Confirm ClawHub CLI is installed/logged in or publish manually via https://clawhub.ai/publish-skill.
- [ ] Accept ClawHub MIT-0 license terms during publish.
- [ ] Do not include price metadata in `SKILL.md`.
- [ ] Do not publish exploit claims. Use demo contract only.
- [ ] Do not mention live target vulnerabilities.

## Monetization path
Because ClawHub currently does not support paid skills:
- Use ClawHub as free distribution/discovery.
- Monetize externally through Atlas robust scans, audit-prep packets, private/pro scanner workflows, or an external paid bundle.
