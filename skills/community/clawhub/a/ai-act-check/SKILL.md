---
name: ai-act-check
description: |
  EU AI Act Compliance Check — based on Regulation (EU) 2024/1689 (欧盟《人工智能法案》),
  覆盖 4 大维度 12 项核心合规检查（高风险 AI 系统核心要求/文档与质量管理/提供者义务/
  透明度与通用目的模型义务，含深度伪造与 AI 生成内容披露）。免费安装；评分运行于
  CQDev 云端合规引擎。无 Key 时自动匿名试用（5 次真实云端评分 / 7 天窗口），额度用尽后引导注册。
  Use when: the user explicitly asks to run the EU AI Act Check skill, or asks for a
  欧盟《人工智能法案》(EU AI Act) 合规评估 / AI 法案合规检查.
  Trigger: ai-act-check, EU AI Act check, AI Act compliance check, 人工智能法案检查, AI 法案合规评估
  Pricing: Free skill; cloud scoring is free (anonymous trial 5 runs, then register for a free API Key with 100 calls)
  ⚠️ Cloud scoring sends your 12 answers to compliancehub.cn; use --non-interactive for a fully offline preview that never contacts the cloud. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 API Key: get a free API Key (100 free calls) at compliancehub.cn/account.html (register in the browser; the Key is shown instantly). Provide it via the COMPLIANCEHUB_API_KEY environment variable, or save it to ~/.config/compliancehub/ai-act-check.key (mode 0600). Registration is done on the website — the terminal no longer collects credentials.
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

# 🤖 EU AI Act Check — 欧盟《人工智能法案》合规检查（免费 · 云端评分）

## Overview
EU AI Act Check 是面向提供或部署 AI 系统主体的**免费**合规自检（云端评分），
覆盖 4 大维度 12 项核心检查：高风险 AI 系统核心要求、文档与质量管理体系、提供者义务、
透明度与通用目的模型义务。评分运行于 CQDev 云端合规引擎。

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
| 1 | Risk Management System (Art. 9) | Art. 9 |
| 2 | Data and Data Governance (Art. 10) | Art. 10 |
| 3 | Transparency and Provision of Information (Art. 13) | Art. 13 |
| 4 | Human Oversight (Art. 14) | Art. 14 |
| 5 | Accuracy, Robustness & Cybersecurity (Art. 15) | Art. 15 |
| 6 | Technical Documentation (Art. 11) | Art. 11 |
| 7 | Record-Keeping / Logging (Art. 12) | Art. 12 |
| 8 | Quality Management System (Art. 16) | Art. 16 |
| 9 | Conformity Assessment & CE Marking (Art. 22) | Art. 22 |
| 10 | Obligations of Providers & Manufacturers (Art. 26) | Art. 26 |
| 11 | Transparency Obligations for Certain AI Systems (Art. 50) | Art. 50 |
| 12 | General-Purpose AI Model Obligations (Art. 25) | Art. 25 |

## Usage

### Free preview (no Key)
```bash
python3 scripts/ai-act-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full check — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
1. Open https://compliancehub.cn/account.html?skill=ai-act-check in your browser and register (the Key is shown instantly after registration).
2. Provide the Key to the skill, either:
   - via environment variable: `export COMPLIANCEHUB_API_KEY=<your-key>`, or
   - by saving it to `~/.config/compliancehub/ai-act-check.key` (mode 0600).
Then run the check below; no terminal login is needed.

### Full check + report
```bash
python3 scripts/ai-act-check.py --format html -o pipl-report.html
```
逐项回答 12 个问题；云端评分并返回 HTML 报告（含风险等级与整改建议）。

## Agent guide
When a user asks for an EU AI Act compliance check:
1. Run `--non-interactive` to preview the 12 items (no Key needed).
2. Run the full check. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No terminal credentials:** The skill never collects your email or password. Registration and Key issuance happen on the website (compliancehub.cn/account.html); the skill only consumes the resulting API Key. This removes any credential-handling path from the CLI.
- **Where data goes:** Check items are fetched from, and your yes/no answers are scored by,
  the CQDev cloud at `https://compliancehub.cn` (the operator's official endpoint,
  pinned in code and **not** overridable by environment variable). Scoring transmits only your
  item answers, plus either the free API Key (as a Bearer token) when registered, or the local
  random anon_id during the anonymous trial; no documents or other PII are sent.
- **Anonymous trial id:** A local random `anon_id` (`~/.config/compliancehub/ai-act-check.anon_id`,
  0600, carries no personal data) persists only to continue the anonymous trial; your answers
  are never stored locally.
- **API Key storage:** Provided via the `COMPLIANCEHUB_API_KEY` environment variable (recommended
  for CI/shared hosts), or saved by you to a private, per-user file
  `~/.config/compliancehub/ai-act-check.key` with `0600` permissions — **outside** this skill
  folder, so it is never committed to source control or shared with the workspace.
- **No shell execution:** This skill runs as a Python 3 subprocess using only the standard
  library (`urllib`, `json`, `ssl`). It does **not** spawn a shell, does not run
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
