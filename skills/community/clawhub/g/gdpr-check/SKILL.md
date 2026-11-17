---
name: gdpr-check
description: |
  GDPR Compliance Check — General Data Protection Regulation (EU) 2016/679 (GDPR).

  Free to install; scoring runs on the CQDev cloud compliance engine.
  No Key? The skill auto-runs an anonymous trial (5 real cloud-scored
  runs, 7-day window) before asking you to register. Covers 12 core items.
  Use when: the user explicitly asks to run the gdpr-check skill (e.g. "run gdpr-check",
  "use the gdpr-check skill"). Do NOT activate on generic mentions of "GDPR" or "EU privacy"
  in ordinary conversation — this skill transmits answers to a third-party cloud and must be
  opted into explicitly by name.
  Trigger (explicit opt-in only): gdpr-check, run gdpr-check, use gdpr-check skill, run the gdpr-check skill
  Pricing: Free skill; cloud scoring is free (anonymous trial 5 runs, then register for a free API Key with 100 calls)
  ⚠️ Cloud scoring sends your answers to compliancehub.cn. The free preview (--non-interactive) fetches the
  latest check items from the cloud rule library but transmits NO answers; if the network is unavailable it
  falls back to the bundled item set. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 Account & free API Key are created on the website (compliancehub.cn) — not in the terminal.
  Open https://compliancehub.cn/account.html?skill=gdpr-check to register and get a Key instantly, then
  provide it via env `COMPLIANCEHUB_API_KEY` or save to ~/.config/compliancehub/gdpr-check.key (mode 0600).
  🌐 Language: bilingual (中文/English). Guidance and recommendations default to Chinese for Chinese-speaking
  compliance teams; legal/regulatory terms keep English originals. Users may request English output at any time.

  💡 Free preview: --non-interactive lists the 12 items without a Key
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 GDPR Compliance Check (GDPR 欧盟隐私合规检查) — Free, Cloud-Scored

## Overview
GDPR 欧盟隐私合规检查 is a **free** 检查 based on 欧盟《通用数据保护条例》（GDPR, Regulation (EU) 2016/679）.
It covers 12 core items. Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* 检查, your responses are
> transmitted to the CQDev cloud at `compliancehub.cn` for scoring. The free `--non-interactive` preview
> fetches the latest check items from the cloud rule library but transmits NO answers; it falls back to the
> bundled item set if the network is unavailable.

- The skill is free to install.
- Check items are served from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (12 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | Material & Territorial Scope | Art. 3 |
| 2 | Lawful Basis for Processing | Art. 6 |
| 3 | Valid Consent | Art. 7 |
| 4 | Transparency & Privacy Notice | Art. 13-14 |
| 5 | Data Subject Rights | Art. 15-17 |
| 6 | Automated Decision-Making | Art. 22 |
| 7 | Data Protection Impact Assessment | Art. 35 |
| 8 | Breach Notification | Art. 33-34 |
| 9 | International Transfers | Art. 44-49 |
| 10 | Security of Processing | Art. 32 |
| 11 | Processor Agreements | Art. 28 |
| 12 | Data Protection Officer | Art. 37-39 |

## Usage
### Free preview (no Key)
```bash
python3 scripts/gdpr-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full 检查 — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
Open https://compliancehub.cn/account.html?skill=gdpr-check in your browser to register and get a free Key instantly.
Then provide it to the skill via env or key file:
```bash
export COMPLIANCEHUB_API_KEY=<your-key>
# or save to ~/.config/compliancehub/gdpr-check.key (mode 0600)
```

### Full 检查 + report
```bash
python3 scripts/gdpr-check.py --format html -o gdpr-check-report.html
```

## Agent guide
When a user asks for a GDPR 欧盟隐私合规检查:
1. Run `--non-interactive` to preview the 12 items (no Key needed).
2. Run the full 检查. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No account in the terminal:** Account creation and free API Key issuance happen on the website
  (compliancehub.cn). This skill never prompts for or transmits your email/password.
- **No persistence by default:** In preview mode (`--non-interactive`) it only reads the public rule library and
  sends NO answers. Scored runs persist only a local random `anon_id` (`~/.config/compliancehub/<slug>.anon_id`,
  0600, carries no personal data) used to continue the anonymous trial; your answers are never stored locally.
- **Where data goes:** Check items are fetched from, and your answers are scored by, the CQDev cloud at
  `https://compliancehub.cn` (the operator's official endpoint). Scoring transmits only your item answers, plus
  either the free API Key (as a Bearer token) when registered, or the local random anon_id during the anonymous trial.
- **API Key storage:** provided via env `COMPLIANCEHUB_API_KEY`, or saved to
  `~/.config/compliancehub/gdpr-check.key` (0600), outside the skill folder.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Not a rogue/autonomous agent:** The stored file is an ordinary API-key (0600), not an auto-start,
  session, or background process. No state is kept beyond that single key file.
- **Preview mode:** `--non-interactive` fetches the public check items from the cloud rule library but
  sends NO answers; it falls back to the bundled item set if the network is unavailable.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.

## License
MIT.
