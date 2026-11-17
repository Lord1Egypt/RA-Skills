---
name: ccpa-check
description: |
  CCPA/CPRA Compliance Check — based on the California Consumer Privacy Act (CCPA)
  and the CPRA amendment, covers 12 core compliance checks for businesses subject to
  California privacy law. Free to install; scoring runs on the CQDev cloud
  compliance engine. No Key? The skill auto-runs an anonymous trial (5 real
  cloud-scored runs, 7-day window) before asking you to register.
  Use when: the user explicitly asks to run the CCPA Check skill, or asks for a
  CCPA/CPRA (California) compliance assessment / California consumer privacy review.
  Trigger: ccpa-check, run ccpa check, CCPA compliance check, California CCPA/CPRA assessment
  Pricing: Free skill; cloud scoring is free (anonymous trial 5 runs, then register for a free API Key with 100 calls)
  ⚠️ Cloud scoring sends your 12 answers to compliancehub.cn; use --non-interactive for a fully offline preview that never contacts the cloud. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 API Key: get a free API Key (100 free calls) at compliancehub.cn/account.html (register in the browser; the Key is shown instantly). Provide it via the COMPLIANCEHUB_API_KEY environment variable, or save it to ~/.config/compliancehub/ccpa-check.key (mode 0600). Registration is done on the website — the terminal no longer collects credentials.
  💡 Free preview: --non-interactive lists the 12 check items without a Key
  Locale: zh-CN（交互默认中文，英文可按需提供）（交互与提示以中文为主，法律条款名称保留英文原文以确保准确）。
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 CCPA Check — Free Compliance Check (Cloud-Scored)

## Overview
CCPA Check is a **free** compliance self-check for businesses subject to the California
Consumer Privacy Act (CCPA) and the CPRA amendment. It covers 12 core checks across
applicability, consumer rights, opt-out, service providers, records, and security.
Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* check, your responses to the
> 12 compliance questions are transmitted to the CQDev cloud at `compliancehub.cn`
> for scoring. Those answers can cover sensitive details — consumer-data practices, service
> providers, security controls, and legal exposure. Only proceed if you are comfortable sending
> them to `compliancehub.cn`. Run `--non-interactive` for a fully **offline** preview that never
> contacts the cloud.

- The skill is free to install.
- Check items: the free `--non-interactive` preview uses the bundled item set and **never contacts the cloud**; a scored run fetches the latest items from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (12 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | Business Applicability | CCPA §1798.140(d) |
| 2 | Privacy Notice at Collection | CCPA §1798.100(b) |
| 3 | Consumer Rights Fulfillment | CCPA §1798.100/105/106 |
| 4 | Identity Verification | CCPA §1798.145(i) |
| 5 | Response Timeliness | CCPA §1798.130(a)(2) |
| 6 | Non-Discrimination | CCPA §1798.125 |
| 7 | Right to Opt-Out | CCPA §1798.120 |
| 8 | Sensitive PI Handling | CPRA §1798.121 |
| 9 | Sale/Sharing of PI | CCPA §1798.140(t)/115 |
| 10 | Service Provider Contracts | CCPA §1798.140(ag) |
| 11 | Record Keeping | CCPA §1798.130(a) |
| 12 | Reasonable Security | CCPA §1798.81.5 |

## Usage

### Free preview (no Key)
```bash
python3 scripts/ccpa-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full check — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
1. Open https://compliancehub.cn/account.html?skill=ccpa-check in your browser and register (the Key is shown instantly after registration).
2. Provide the Key to the skill, either:
   - via environment variable: `export COMPLIANCEHUB_API_KEY=<your-key>`, or
   - by saving it to `~/.config/compliancehub/ccpa-check.key` (mode 0600).
Then run the check below; no terminal login is needed.

### Full check + report
```bash
python3 scripts/ccpa-check.py --format html -o ccpa-report.html
```
Answer 12 yes/no questions; the cloud scores and returns an HTML report.

## Agent guide
When a user asks for a CCPA/CPRA compliance check:
1. Run `--non-interactive` to preview the 12 items (no Key needed).
2. Run the full check. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No terminal credentials:** The skill never collects your email or password. Registration and Key issuance happen on the website (compliancehub.cn/account.html); the skill only consumes the resulting API Key. This removes any credential-handling path from the CLI.
- **Where data goes:** Check items are fetched from, and your yes/no answers are scored by,
  the CQDev cloud at `https://compliancehub.cn` (the operator's official endpoint,
  pinned in code and **not** overridable by environment variable). Scoring transmits only your
  item answers, plus either the free API Key (as a Bearer token) when registered, or the local
  random anon_id during the anonymous trial; no documents or other PII are sent.
- **Anonymous trial id:** A local random `anon_id` (`~/.config/compliancehub/ccpa-check.anon_id`,
  0600, carries no personal data) persists only to continue the anonymous trial; your answers
  are never stored locally.
- **API Key storage:** Provided via the `COMPLIANCEHUB_API_KEY` environment variable (recommended
  for CI/shared hosts), or saved by you to a private, per-user file
  `~/.config/compliancehub/ccpa-check.key` with `0600` permissions — **outside** this skill
  folder, so it is never committed to source control or shared with the workspace.
- **No shell execution:** This skill runs as a Python 3 subprocess using only the standard
  library (`urllib`, `json`, `ssl`, `getpass`). It does **not** spawn a shell, does not run
  arbitrary OS commands, and does not execute external binaries.
- **Not a rogue/autonomous agent:** Writing the Key to `~/.config/compliancehub/` is ordinary
  API-key persistence for your convenience — not agent installation, not auto-start, and not
  self-modification. The skill does nothing unless you invoke it from the terminal.
- **Preview without cloud:** `--non-interactive` lists the 12 items and never contacts the cloud.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**.
Consult qualified counsel for formal opinions. Laws change; verify against official sources.

## License
MIT.
