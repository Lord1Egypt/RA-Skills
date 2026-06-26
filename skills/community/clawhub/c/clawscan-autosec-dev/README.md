<div align="center">

# 🦀 ClawScan

**Security scanning skill for OpenClaw deployments**

[![Version](https://img.shields.io/badge/skill%20version-0.1.3-blue?style=flat-square&logo=semanticrelease)](./references/api-contract.md)
[![API](https://img.shields.io/badge/API-v0.1-informational?style=flat-square&logo=fastapi)](./references/api-contract.md)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey?style=flat-square&logo=linux)](.)
[![Python](https://img.shields.io/badge/python-3.8%2B-yellow?style=flat-square&logo=python)](./scripts)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](.)
[![中文文档](https://img.shields.io/badge/文档-中文版-red?style=flat-square&logo=googletranslate)](./README_zh.md)

*Read this in [中文 (Chinese)](./README_zh.md)*

</div>

---

ClawScan is a **read-only security skill** that performs first-pass threat assessments against a local OpenClaw environment. It connects to the ClawScan cloud service to match your installation against known vulnerability databases, malicious skill hashes, and network exposure patterns — without uploading secrets, prompts, or full file contents.

---

## 🛡️ What Risks Does ClawScan Cover?

| Module | Risk Category | What It Detects |
|---|---|---|
| 🔍 **vulnerability** | CVE / version risk | OpenClaw versions matching known-vulnerable ranges |
| 🧬 **skills-check** | Supply-chain / malware | Installed skill files whose SHA-256 matches the malicious-hash corpus |
| 🌐 **port-check** | Network exposure | Services bound to `0.0.0.0` or `::` that may be reachable beyond localhost |
| 🔄 **update-check** | Outdated tooling | Whether your installed ClawScan skill is behind the latest release |
| ⏰ **scheduled-scan** | Continuous monitoring | All of the above, run automatically on a configurable interval — alerts only when risk is found |

> **Scope note:** ClawScan reports on *known* issues in its corpus. A clean result means no match was found, not that the environment is guaranteed safe.

---

## 📦 Requirements

- **OpenClaw** installed locally
- **Python 3.8+** (for the bundled helper scripts)
- Network access to `https://clawscan.autosec.dev`
- `ss` or `lsof` available on your system (for port scanning)

---

## 🚀 Getting Started

### 1. Install the skill

Place the `clawscan` skill directory inside one of your OpenClaw skill roots:

```bash
# Default skill location
~/.openclaw/skills/clawscan/
```

### 2. Register your client

The first time you use ClawScan, register your client to get a persistent anonymous ID:

```
Ask OpenClaw: "Register my ClawScan client"
```

This creates `~/.openclaw/clawscan/client.json` with a random UUID. No hardware fingerprinting is used.

### 3. Run your first scan

```
Ask OpenClaw: "Run a full ClawScan check"
```

---

## 🔧 Modules & Usage

### 🔍 `vulnerability` — Version Risk Check

Checks whether your installed OpenClaw version falls within any known-vulnerable range.

```
"Is my OpenClaw version vulnerable?"
"Check OpenClaw version risk"
```

**Example report:**

```
Module: vulnerability
Status: ok  |  Risk: HIGH

Finding: OC-2026-001 — Example issue
  Affected: <= 1.2.3  |  Current: 1.2.3  |  Fixed: 1.2.4
  Recommendation: Upgrade to 1.2.4 or later

Scope: This only checks known vulnerable version ranges.
```

---

### 🧬 `skills-check` — Malicious Skill Hash Detection

Computes SHA-256 hashes for every file in your installed skills and submits them against the ClawScan threat corpus. No file contents are uploaded — only hashes.

```
"Check my installed skills for malware"
"Scan skill hashes"
```

You can also run the collector script directly:

```bash
python scripts/collect_skill_hashes.py ~/.openclaw/skills ./skills
```

**Clean result:**

```
No known malicious skill hash was matched.
This does not prove that the installed skills are safe.
```

**Hit result:**

```
⚠️  Known malicious content was matched in the installed skills set.

Skill: foo  |  Risk: HIGH  |  Match type: exact_hash
  File: run.py  →  KnownMaliciousSkill.A
  Recommendation: Disable and remove this skill immediately
```

---

### 🌐 `port-check` — Network Exposure Check

Inspects local TCP listeners via `ss` (preferred) or `lsof` and flags any service bound to a non-loopback address.

```
"Is OpenClaw exposed on the network?"
"Check listening ports"
```

You can also run the listener script directly:

```bash
python scripts/list_listeners.py
```

**Example finding:**

```
Module: port-check
Status: ok  |  Risk: HIGH

Finding: openclaw on 0.0.0.0:3000
  This service is listening on all interfaces, which increases exposure risk.
  Recommendation: Bind to 127.0.0.1 or place behind an authenticated reverse proxy

Scope: Based on local listener state; not a full external reachability test.
```

> ClawScan will never claim `0.0.0.0` means "publicly exposed" — exposure depends on your firewall, NAT, security groups, and network topology.

---

### 🔄 `update-check` — ClawScan Skill Update Check

Checks whether the version of this ClawScan skill you have installed is behind the latest release.

```
"Is my ClawScan up to date?"
```

---

### ⏰ `scheduled-scan` — Automatic Periodic Scanning

Runs a full scan (vulnerability + skills-check + port-check) automatically on a configurable interval. **Only reports when a security risk is found — completely silent if all checks are clean.**

```
"Enable scheduled ClawScan every 60 minutes"
"Set up auto security scan every 30 minutes"
```

**Setup confirmation:**

```
ClawScan scheduled scan enabled.
- Interval: every 60 minutes
- Next run: 2026-03-09T11:00:00Z
- Reporting: only on risk findings
```

**When risks are detected:**

```
[ClawScan scheduled check — 2026-03-09T11:00:00Z]
Security risk detected. Full report follows.

... (standard module reports for each finding)
```

**When everything is clean:** *(no output)*

Schedule state is persisted at `~/.openclaw/clawscan/schedule.json`.

---

## 📂 Project Structure

```
clawscan/
├── SKILL.md                       # Skill definition (English)
├── SKILL.zh-CN.md                 # Skill definition (Chinese)
├── agents/
│   └── openai.yaml                # OpenAI agent interface definition
├── references/
│   └── api-contract.md            # Full API request/response reference
└── scripts/
    ├── collect_skill_hashes.py    # Compute SHA-256 hashes for installed skills
    └── list_listeners.py          # Enumerate TCP listeners via ss / lsof
```

---

## 🔒 Privacy & Data Minimization

ClawScan is designed to share the minimum necessary data:

- ✅ Sends: anonymous client UUID, version strings, file hashes, listener metadata
- ❌ Never sends: file contents, environment variables, prompts, API keys, absolute home-directory paths (unless you explicitly request it)
- 🔑 Client IDs are random UUIDs — no hardware fingerprinting

---

## ⚠️ Limitations

- ClawScan only detects **known** issues covered by its current corpus
- Port check results reflect **local listener state**, not confirmed external reachability
- Vulnerability matching is based on **version ranges**, not runtime behaviour analysis
- A clean scan result means **no known match was found**, not a guarantee of safety

---

## 🗺️ Roadmap

- [ ] `POST /scan` aggregate endpoint support
- [ ] Expanded malicious skill corpus
- [ ] SBOM / dependency risk module
- [ ] Webhook / notification integration for scheduled-scan alerts

---

## 🤝 Contributing

Issues and pull requests are welcome. Please do not include real threat signatures, credentials, or private keys in contributions.

---

<div align="center">

Made for the OpenClaw ecosystem · [中文文档 →](./README_zh.md)

</div>
