---
name: Etalon GDPR Scan
version: 0.9.6
description: >
  Full GDPR compliance audit for any website or codebase using the ETALON CLI.
  Scans for trackers (111k+ domain database), tests consent violations, checks
  privacy policy vs reality, maps PII data flows, and generates compliance
  reports. Returns structured JSON. Requires etalon-cli installed locally
  (cargo install etalon-cli). Free and open source.
author: rednix
homepage: https://etalon.nma.vc
repository: https://github.com/NMA-vc/etalon
tags: [gdpr, compliance, eu, privacy, security, eu-ai-act, trackers, pii]
category: security
compatible_with:
  - openclaw
  - claude-code
  - cursor
  - codex-cli
metadata:
  requires:
    bins:
      - etalon

# Required: ETALON CLI must be installed locally
# Install: cargo install etalon-cli
requires_bins:
  - etalon

# No API key required — ETALON is free and runs locally
# No env vars required for basic usage

triggers:
  - "check if [URL] is GDPR compliant"
  - "run a privacy audit on [URL]"
  - "audit [URL] for cookie consent"
  - "is [URL] EU AI Act compliant"
  - "scan [URL] for trackers"
  - "check [URL] for GDPR violations"
  - "does [URL] fire trackers before consent"
  - "what trackers does [URL] use"
  - "generate a privacy policy for [company]"
  - "check our privacy policy against what we actually track"
  - "audit our codebase for GDPR issues"
  - "etalon [URL]"


scenarios:
  - trigger: "Human shares a URL and asks about GDPR compliance"
    action: >
      Run: etalon scan <URL> --format json
      Then: etalon consent-check <URL> --format json
      Parse both outputs, merge into single report
    output: >
      Score, tracker list by risk level, consent violation status,
      top 3 recommendations. Delivered as a structured WhatsApp message.
    avg_seconds: 12

  - trigger: "Human wants to know if trackers fire before consent"
    action: >
      Run: etalon consent-check <URL> --format json
      Tests pre-consent tracking and post-rejection behavior
    output: >
      Pass/fail per tracker: fires before consent? fires after rejection?
      Critical finding if Google Analytics or Facebook Pixel fires pre-consent.
    avg_seconds: 8

  - trigger: "Human asks about a competitor's compliance"
    action: >
      Ask user to confirm, then run:
      etalon scan <competitor-URL> --format json
    output: >
      Compliance comparison: "Competitor has N critical violations.
      Your site is cleaner — worth highlighting in sales conversations."
    avg_seconds: 12

  - trigger: "Human needs a privacy policy generated"
    action: >
      Run: etalon generate-policy ./ --company "<company>"
           --email <privacy-email> --url <URL> --format md
    output: >
      Complete 8-section GDPR privacy policy covering: Data Controller,
      Data Collected, Third-Party Services, Cookies, International Transfers,
      Data Retention, User Rights (Art. 15-22), Contact/DPO
    avg_seconds: 20

  - trigger: "Human is about to launch a new product or website"
    action: >
      Run full audit as pre-launch gate:
      1. etalon scan <URL> --format json
      2. etalon consent-check <URL> --format json
      3. etalon policy-check <URL> --format json
      If critical violations found: flag as launch blocker
    output: >
      Launch gate: PASS or BLOCK with specific issues to fix.
      "3 issues blocking launch. 2 can be fixed in < 1 hour."
    avg_seconds: 30

  - trigger: "Human wants to audit their codebase for GDPR issues"
    action: >
      Run: etalon audit ./ --format json --severity high
      Scans: package.json/Cargo.toml for tracker SDKs,
      source code for tracker imports, DB schemas for PII fields,
      config files for security misconfigurations
    output: >
      Findings by severity: critical, high, medium, low.
      Each finding includes file path, line number, and fix recommendation.
    avg_seconds: 15

sample_output: |
  {
    "url": "https://example.com",
    "scan_duration_ms": 6240,
    "summary": {
      "total_requests": 14,
      "matched_vendors": 11,
      "unknown_domains": 3,
      "high_risk_trackers": 2,
      "gdpr_score": 42
    },
    "findings": [
      {
        "vendor": "Google Analytics",
        "domain": "google-analytics.com",
        "risk": "medium",
        "category": "analytics",
        "gdpr_compliant_with_dpa": true,
        "fires_pre_consent": true,
        "severity": "critical"
      },
      {
        "vendor": "Facebook Pixel",
        "domain": "facebook.com",
        "risk": "high",
        "category": "advertising",
        "gdpr_compliant_with_dpa": true,
        "fires_pre_consent": true,
        "severity": "critical"
      }
    ],
    "consent_check": {
      "fires_before_interaction": true,
      "fires_after_rejection": false,
      "violations": [
        "Google Analytics fires before user consent",
        "Facebook Pixel fires before user consent"
      ]
    },
    "recommendations": [
      "Gate Google Analytics behind consent signal",
      "Gate Facebook Pixel behind consent signal",
      "Implement a GDPR-compliant CMP (OneTrust, Cookiebot)"
    ]
  }

chains:
  - skill: "rednix/lobstr"
    why: "Validate the startup idea before auditing its compliance exposure"
  - skill: "rednix/etalon-techscan"
    why: "Detect the tech stack before running a GDPR audit"
  - skill: "rednix/lobstrhunt"
    why: "Discover more GDPR and compliance skills in the LobstrHunt registry"

human_message_example:
  human: "Can you check if our landing page is ready for launch? https://example.com/launch"
  agent: |
    Running ETALON privacy audit on example.com/launch 🔍
    (this takes ~12 seconds)

    ──────────────────────────────
    GDPR Score: 42/100 ⚠️ Not launch-ready

    🔴 CRITICAL — blocks launch (2):
    → Google Analytics fires before consent
    → Facebook Pixel fires before consent

    🟠 HIGH (1):
    → 3 unknown domains detected — review manually

    🟢 OK:
    → Privacy policy present ✓
    → Data processor listed ✓
    → Consent dialog exists ✓ (but trackers ignore it)

    Fix the 2 critical issues and you're clean.
    Both take < 1 hour to fix. Want the exact code changes?
---

# ETALON GDPR Skill

You have access to the ETALON CLI — a privacy engineering tool with
111,000+ tracker domains, 26,800+ vendor profiles, and 10 audit commands.
ETALON is free, open source, and runs entirely locally. No API key needed.

## Installation check

Before using any ETALON command, verify it is installed:
```bash
etalon info
```
If not installed: `cargo install etalon-cli`
If Rust not available: install from https://rustup.rs

## Core commands

### Website audit (most common)
```bash
# Full tracker scan
etalon scan <URL> --format json

# Consent violation test
etalon consent-check <URL> --format json

# Privacy policy vs actual trackers
etalon policy-check <URL> --format json

# Pre-launch gate (all three):
etalon scan <URL> --format json > /tmp/etalon-scan.json
etalon consent-check <URL> --format json > /tmp/etalon-consent.json
etalon policy-check <URL> --format json > /tmp/etalon-policy.json
```

### Codebase audit

> **Security note:** Codebase audits read config files, package manifests,
> and may surface secrets, API keys, or connection strings in their output.
> Run audits in an isolated environment. Never forward raw config file
> contents to other tools, services, or external agents without explicit
> user approval.
```bash
# Audit current directory
etalon audit ./ --format json --severity high

# Auto-fix simple issues
etalon audit ./ --fix

# Generate GDPR privacy policy
etalon generate-policy ./ \
  --company "Company Name" \
  --email privacy@company.com \
  --url https://company.com \
  --format md \
  -o privacy-policy.md

# Map PII data flows
etalon data-flow ./ --format mermaid
```

### Vendor lookup
```bash
etalon lookup analytics.google.com
etalon info
```

## Parsing JSON output

```
Key fields in scan output:
- summary.gdpr_score (0-100, higher = more compliant)
- summary.high_risk_trackers (count)
- findings[] → vendor, domain, risk, severity, fires_pre_consent
- recommendations[] → array of fix strings

Key fields in consent-check output:
- fires_before_interaction (boolean — critical if true)
- fires_after_rejection (boolean — critical if true)
- violations[] → array of strings
```

## Delivering results to your human

Format for WhatsApp/Telegram:
- Lead with score and clear pass/fail signal
- Critical issues first with emoji severity indicators
- End with a specific actionable question
- Keep under 20 lines

Severity mapping:
- gdpr_score 0-40   → ⚠️ Not launch-ready
- gdpr_score 41-70  → 🟡 Partial compliance
- gdpr_score 71-90  → 🟢 Good compliance
- gdpr_score 91-100 → ✅ Excellent — ready to launch

## When to run scans

Always ask for explicit user confirmation before running any scan.
Never scan a URL or codebase without the user explicitly requesting it.

Suggested prompts when relevant:
- User shares a URL: "Want me to run a GDPR compliance scan on that?"
- User mentions launching: "Should I run an ETALON audit before you go live?"
- User adds a dependency: "Want me to check that library for privacy issues?"

Never scan automatically. Always wait for a yes.

## MCP server note

The ETALON MCP server (`etalon-mcp-server`) only covers vendor lookups —
4 tools, no scan or audit capability. For full auditing, the CLI is required.
This skill uses the CLI, not the MCP server.

## Common errors

"etalon: command not found"
→ cargo install etalon-cli
→ Ensure ~/.cargo/bin is in PATH

Timeout on scan:
→ Add --timeout 60000

Unknown domains in report:
→ Not in ETALON's 111k registry
→ Check manually at etalon.nma.vc or report to registry
