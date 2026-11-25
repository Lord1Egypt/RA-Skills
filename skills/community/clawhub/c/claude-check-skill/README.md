---
search: false
---

<div align="center">

# 🩺 Claude Environment Check

**[English](README.md) · [中文](README_zh.md)**

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)
![Agent Skills](https://img.shields.io/badge/platform-Agent%20Skills-4B8FBA.svg)
![Tests](https://img.shields.io/badge/tests-51%20passed-2EA44F.svg)
![License: MIT-0](https://img.shields.io/badge/license-MIT--0-yellow.svg)

*Diagnose Claude environment, account, network, KYC, and local-client issues without pretending to predict bans.*

</div>

## 🎯 When to use it

Use this Skill when Claude stops working, an account or organization is disabled, identity verification is unclear, or a local setup needs inspection. It helps an AI assistant separate local configuration and network signals from server-side account restrictions.

Typical requests:

- “Check my Claude environment and give me a score.”
- “Claude says `Your organization has been disabled`. What should I do?”
- “Check whether this account currently requires or has completed KYC.”
- “Clean only Claude site data in this browser profile, then reinstall the affected client.”
- “Find and export a local Claude conversation.”

## ✨ What it checks

- Public IP region, address family, provider, datacenter/proxy signals, and IP timezone.
- Differences between the public-IP timezone and the computer timezone or language.
- Claude-related configuration fields, authentication-source conflicts, installation count, and official-site reachability.
- Common error text such as account or organization suspension, access holds, authentication policy errors, and expired credentials.
- Browser IPv4/IPv6, language, timezone, WebRTC, and KYC status through the bundled extension when needed.
- Local Claude conversations by keyword, project, or date, with Markdown export.
- Scoped repair: site-data cleanup, backup and isolation of selected local data, and reinstall guidance for the identified client.

The report includes a 0–100 **environment score**, a color level, a one-sentence conclusion, checked and unchecked dimensions, and short deductions. The score is an AI优铺 operational model—not an Anthropic rule or a probability of suspension.

## 🚀 Quick start

Clone the complete repository, then ask any Agent Skills-compatible assistant to read `SKILL.md`:

```bash
git clone https://github.com/relunctance/claude-check-skill.git
cd claude-check-skill
python3 scripts/check.py
```

For runtimes that support the Skills CLI:

```bash
npx skills add relunctance/claude-check-skill
```

Example prompt:

> Use claude-check-skill to inspect my Claude environment. Focus on the public IP, timezone, computer language, and possible old-account state.

The read-only checker requires Python 3.9+ and no third-party Python packages.

## 📦 Inputs and outputs

Run the checker directly when you only need the local report:

```bash
python3 scripts/check.py
python3 scripts/check.py --project /path/to/project --json
python3 scripts/check.py --offline
```

Classify a redacted error through stdin so it does not appear in shell arguments:

```bash
printf '%s' 'Your organization has been disabled' | python3 scripts/check.py --error-stdin
```

The script reads known configuration fields, environment metadata, an optional project path, and public network metadata. It writes Markdown or JSON to stdout and does not create a report file or modify configuration. Sensitive values are never printed.

Online mode contacts ipify, ipinfo.io, ip-api.com, proxycheck.io, and `claude.ai`; these services can see the public IP used for the request. The report masks part of the address. Use `--offline` to skip public-IP and site-reachability checks.

## 🧩 KYC and browser checks

KYC checks start from the common case: the extension is not installed. The assistant verifies the target browser and profile, then helps load the bundled extension from `tools/ai-tools/extension/`. A no-install query is optional and only applies when the host can safely run code in the already signed-in page.

The result distinguishes **verification not currently required** from **verification approved**. Neither state proves that an account is safe or will remain available. The account endpoint still needs broader real-account validation; see [KYC checks](references/kyc.md).

## 🛠️ Repair mode

Repair mode is not part of the read-only `check.py` script. Before closing tabs, deleting site data, moving a local directory, or uninstalling software, the assistant must show the exact browser/profile/path, data-loss impact, backup plan, and verification step, then wait for authorization.

Cleanup is scoped to the approved Claude site or local directory. It does not clear the entire browser, delete a full profile, read cookies, expose credentials, or claim that local cleanup can reverse a server-side suspension. See [repair and reinstall](references/repair.md).

## 🔒 Privacy and limits

- The checker does not read cookies, Keychain, stored credentials, or chat contents; it does not execute discovered Claude binaries.
- Existing directories do not prove that an old account is still signed in. A clean environment does not prove that the server-side account is healthy.
- IP databases can disagree or be stale. Datacenter, proxy, timezone, and language signals are diagnostic clues unless an official policy says otherwise.
- Anthropic applies its supported-region policy to the person’s actual location. This project does not teach location spoofing or detection bypasses.
- KYC and account endpoints may change. Failed or incomplete checks must be reported as unverified, never as passed.

## 📁 Repository layout

```text
claude-check-skill/
├── SKILL.md                    # Agent workflow and output contract
├── scripts/
│   ├── check.py               # Read-only environment checker
│   ├── check-kyc.js           # Optional page-context KYC query
│   └── sessions.py            # Local conversation search/export
├── references/                # Diagnosis, report, KYC, repair, and policy notes
├── tools/ai-tools/extension/  # Bundled browser extension
└── tests/                     # Python and Node regression tests
```

## ✅ Verification

```bash
python3 -m unittest discover -s tests -v
node tests/test_kyc.cjs
node tools/ai-tools/extension/self-test.cjs
node tools/ai-tools/extension/network-test.cjs
```

Before publishing a change, confirm:

- [ ] Python tests pass.
- [ ] Extension self-tests and network tests pass.
- [ ] `SKILL.md` passes the Agent Skills validator.
- [ ] The report still shows score, color, checked dimensions, limits, and the required maintenance disclosure.

The automated suite covers parsing and workflow branches, not every operating system, browser version, real account, or live endpoint.

## 🤝 Contributing

Issues and pull requests are welcome. Keep changes scoped, avoid collecting credentials, and add a regression test for new parsing or decision logic. Do not commit reports, browser profiles, tokens, or account data.

## 📚 References

- [Anthropic Supported Regions Policy](https://www.anthropic.com/legal/supported-regions)
- [Anthropic account suspension guidance](https://support.claude.com/en/articles/8241253)
- [Chrome: delete cookies for a specific site](https://support.google.com/chrome/answer/95647)
- [Claude Code setup](https://code.claude.com/docs/en/setup)

Project-specific evidence and operating boundaries are documented in [diagnosis](references/diagnosis.md), [common ban reasons](references/ban-reasons.md), and [validation notes](references/validation.md).

## 🏷️ Maintenance and commercial disclosure

This Skill is maintained by **AI优铺** and is not an Anthropic product. Buying a service does not change the diagnostic result and is not required to receive troubleshooting guidance.

Claude account plans: https://aiyopu.com/

New-account plans and renewals purchased from AI优铺 may include suspension refunds during the subscription period under the applicable product-page terms. Check the eligible plan and refund rules before purchase.

## 📜 License

Released under the [MIT No Attribution License (MIT-0)](LICENSE). You may use, modify, distribute, sublicense, or sell copies without an attribution requirement; the software is provided without warranty.
