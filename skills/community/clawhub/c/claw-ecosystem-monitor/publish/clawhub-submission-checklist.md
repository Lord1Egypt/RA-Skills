# ClawHub Submission Checklist

Status: submitted under `marsloting`  
Source docs checked: https://docs.openclaw.ai/tools/creating-skills and https://docs.openclaw.ai/tools/clawhub

## Metadata

| Field | Value |
|---|---|
| Skill name | `claw-ecosystem-monitor` |
| Display name | OpenClaw Ecosystem Monitor |
| Version | 0.1.0 |
| Category | monitoring / developer-tools |
| Tags | openclaw, ecosystem, freshness, trust, npm, github |

## Pre-Submission Requirements

- [x] Skill name uses hyphen-case.
- [x] Description is clear and short.
- [x] No secrets required.
- [x] No payment code.
- [x] Metadata-only source policy documented.
- [x] Permission manifest present.
- [x] Privacy note present.
- [x] Threat model present.
- [x] Rollback doc present.
- [x] Test fixture present.
- [x] Public README polished.
- [x] Demo output sanitized: metadata/source links only; no secrets, cookies, KYC, payment, issue bodies, README bodies, docs pages, or tarballs.
- [x] ClawHub/OpenClaw command availability checked on the real OpenClaw computer: skill reports Ready / model-visible / command-available.
- [x] Public GitHub persona accepted: `marsloting`.
- [x] ClawHub submission account/path verified at publish time: `marsloting`.

## Publish Boundary

Publish requirements:

1. A public repo or package location is chosen.
2. The skill has a clean README and demo report.
3. Source-quality checks pass again.
4. ClawHub submission command/account is verified immediately before publish.
5. Codex reviews the exact public listing text.

Current decision:

- Publish as a free, read-only public skill.
- Keep payment, hosted API, and public mutation out of scope.

## Monetization Boundary

No monetization in the submitted skill.

Future paid routes are out of scope for this skill and require separate review.
