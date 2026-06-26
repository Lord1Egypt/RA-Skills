---
description: "Instruction-only PII detector and redactor for AI outputs. Detects emails, phones, SSNs, bank cards, IBANs, crypto addresses, and IPs entirely within the agent context — no text ever leaves the agent. GDPR & HIPAA compliant privacy checkpoint for AI pipelines."
tags: [pii, redaction, privacy, gdpr, hipaa, compliance, data-protection, security, audit, sensitive-data, leibniz-layer, instruction-only]
---

# DCL Sentinel Trace — Leibniz Layer™

**Publisher:** @daririnch · Fronesis Labs  
**Version:** 2.0.0  
**Part of:** Leibniz Layer™ Security Suite

---

## What this skill does

DCL Sentinel Trace detects and redacts personally identifiable information in AI outputs before they reach users or downstream systems.

**This skill is 100% instruction-only.** No text is sent to any external server. The entire analysis runs inside the agent's context window. The scanned text never leaves the agent.

### What gets detected

| Category | Examples |
|----------|---------|
| `email` | Any email address pattern |
| `phone` | International and local phone number formats |
| `national_id` | SSNs, national ID numbers, tax IDs |
| `bank_card` | Card PANs (Visa, Mastercard, Amex, etc.) |
| `iban` | International bank account numbers |
| `crypto_address` | Bitcoin, Ethereum, and other wallet addresses |
| `ip_address` | IPv4 and IPv6 addresses |
| `passport` | Passport and travel document numbers |

### When to use this skill

- AI output may contain **personal data** from user input, documents, or retrieved content
- Your pipeline requires **GDPR or HIPAA compliance** before delivering responses
- A **coding or data agent** processes datasets that may contain real PII
- You need a **privacy checkpoint** before logging or storing AI outputs

---

## How to run a scan

Paste the text to scan into the conversation. The agent screens it locally against the checklist below. No network requests are made.

### Step 1 — Run the detection checklist

Work through each category. For each match found, record:
- `type` — which PII category triggered
- `redacted_sample` — masked version (e.g. `te****@****.com`)
- `severity` — `critical` for financial/ID data, `major` for contact data

### Step 2 — Apply verdict logic

| Condition | Verdict |
|---|---|
| Any finding | `NO_COMMIT` |
| No findings | `COMMIT` |

---

## Detection Checklist

### T1 — Email Addresses (Major)
- [ ] Any string matching `[text]@[domain].[tld]` pattern

### T2 — Phone Numbers (Major)
- [ ] International format: `+[country code][number]`
- [ ] Local formats: sequences of 7–15 digits with common separators

### T3 — National ID / SSN (Critical)
- [ ] US SSN: three digits, two digits, four digits pattern
- [ ] National ID formats for other countries: fixed-length numeric or alphanumeric sequences in ID context

### T4 — Bank Card PANs (Critical)
- [ ] 13–19 digit sequences matching major card network prefixes
- [ ] With or without spaces/dashes between groups

### T5 — IBANs (Critical)
- [ ] Two-letter country code followed by two check digits and up to 30 alphanumeric characters

### T6 — Crypto Wallet Addresses (Major)
- [ ] Bitcoin: Base58 strings of 25–34 chars starting with `1`, `3`, or `bc1`
- [ ] Ethereum: 42-char hex strings starting with `0x`
- [ ] Other chains: similar fixed-length address patterns in wallet context

### T7 — IP Addresses (Minor)
- [ ] IPv4: four octets separated by dots
- [ ] IPv6: eight groups of hex digits separated by colons

### T8 — Passport / Document Numbers (Critical)
- [ ] Alphanumeric strings of 6–9 characters in passport or document number context

---

## Output schema

```json
{
  "verdict": "COMMIT | NO_COMMIT",
  "detections": [
    {
      "type": "email",
      "redacted_sample": "te****@****.com",
      "severity": "major"
    }
  ],
  "detection_count": 0,
  "categories_checked": ["T1","T2","T3","T4","T5","T6","T7","T8"],
  "categories_clear": ["T1","T2","T3","T4","T5","T6","T7","T8"],
  "powered_by": "DCL Sentinel Trace · Leibniz Layer™ · Fronesis Labs"
}
```

---

## Where Sentinel Trace fits in the DCL pipeline

```
Untrusted input
        │
        ▼
DCL Prompt Firewall        ← blocks malicious input
        │ COMMIT
        ▼
      LLM
        │
        ▼
DCL Policy Enforcer        ← compliance check on output
        │ COMMIT
        ▼
DCL Sentinel Trace         ← PII redaction (instruction-only)
        │ COMMIT
        ▼
DCL Secret Leak Detector   ← credential scan
        │ COMMIT
        ▼
DCL Output Sanitizer       ← final sweep
        │ COMMIT
        ▼
DCL Semantic Drift Guard   ← hallucination check
        │ IN_COMMIT
        ▼
Safe to deliver
```

---

## Privacy & Data Policy

This skill is operated by **Fronesis Labs** and is **100% instruction-only**.

**No data leaves the agent.** All analysis runs entirely within the agent's context window. No content is transmitted to any server.

Full policy: **https://fronesislabs.com/#privacy** · Browse the full DCL Security Suite: **[hub.fronesislabs.com](https://hub.fronesislabs.com)** · Questions: support@fronesislabs.com

---

## Related skills

- `dcl-prompt-firewall` — Input-layer injection and jailbreak detection
- `dcl-secret-leak-detector` — Credential and API key scan
- `dcl-output-sanitizer` — Final output sweep
- `dcl-policy-enforcer` — Compliance and regulatory check

**Leibniz Layer™ · Fronesis Labs · fronesislabs.com**
