---
name: gauntletscore
version: 5.1.5
description: Trust verification for AI output — verify any document or code before you act on it
author: genstrata
license: proprietary
homepage: https://gauntletscore.com
api_base: https://api.gauntletscore.com
tags:
  - verification
  - trust
  - hallucination-detection
  - multi-agent
  - enterprise
  - security
  - code-safety
  - fact-checking
  - compliance
metadata:
  clawdbot:
    config:
      requiredEnv:
        - GAUNTLET_API_KEY
      example: |
        config = {
          env = {
            GAUNTLET_API_KEY = "gsk_your_key_here";
          };
        };
---

# GauntletScore — Trust Verification for AI Output

Verify any AI-generated document or code before you trust it. Seven AI personas from five independent model providers independently analyze your content, verify every checkable claim against authoritative sources, and produce a cryptographically signed trust score.

## What It Does

Submit a document or code and get:

- **Gauntlet Score** (0-100) with letter grade (A-F)
- **Claim-by-claim verification** against CourtListener (legal), eCFR (regulatory), PubMed (scientific), EDGAR (SEC), and computational math verification
- **Code safety analysis** detecting reverse shells, credential theft, prompt manipulation, data exfiltration, and obfuscated payloads
- **Unanimous vote** from 7 independent AI agents (PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED)
- **Cryptographic certificate** proving the score is genuine and untampered
- **Full debate transcript** showing every agent's reasoning

## Quick Start

Free tier includes 3 analyses per month. Get an API key at [gauntletscore.com](https://gauntletscore.com).

### Verify a document by pasting content:
```
POST https://api.gauntletscore.com/v1/analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "document": "Your document text here...",
  "topic": "Verify the claims in this document"
}
```

### Verify a ClawHub skill by URL:
```
POST https://api.gauntletscore.com/v1/analyze
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "source_url": "https://clawhub.ai/skills/gauntlet-validate/SKILL.md",
  "topic": "Evaluate the safety of this ClawHub skill before installation"
}
```

### Check results:
```
GET https://api.gauntletscore.com/v1/jobs/{job_id}
Authorization: Bearer YOUR_API_KEY
```

Results include score, grade, vote, verified claims, and a cryptographic certificate.

## What It Catches

### In documents:
- Fabricated legal citations (hallucinated case law)
- Misapplied regulations (wrong CFR section for the situation)
- Mathematical errors (wrong totals, incorrect percentages)
- Internal contradictions
- Unsupported conclusions

### In code:
- Reverse shells and remote code execution
- Credential theft and data exfiltration
- Download-and-execute attacks (curl | bash)
- Prompt manipulation attempts (instructions designed to override agent behavior)
- Documentation-vs-behavior mismatches (code does things the README doesn't mention)
- Dangerous operation combinations that pass individual checks

## How It Works

Seven AI personas from five independent model providers independently analyze your submission:

1. **Round 0** — Each agent conducts independent research, verifying claims against authoritative databases
2. **Rounds 1-3** — Structured adversarial debate where agents challenge each other's findings
3. **Round 4** — Final positions and votes
4. **Knowledge Graph** — Every verified and debunked claim is stored in a persistent knowledge graph. Subsequent analyses benefit from prior verifications, reducing cost and increasing accuracy over time.
5. **Bayesian Calibration** — Confidence scores are computed using Bayesian inference across multiple evidence sources, not simple vote counting. The score reflects calibrated probability, not consensus.
6. **Scoring** — Six-component rubric produces the Gauntlet Score
7. **Certification** — Ed25519 cryptographic signature proves the result is genuine

All analysis is **read-only**. Submitted code is never executed. Documents are processed in memory and not stored.

## Pricing

| Tier | Price | Credits |
|------|-------|---------|
| Free | $0 | 3 runs / month |
| Starter | $29 | 5 analyses |
| Pro | $79 | 15 analyses |
| Business | $149 | 30 analyses |
| Enterprise | Custom | Unlimited |

One credit = one analysis, regardless of document length. No subscriptions.
See [gauntletscore.com/pricing](https://gauntletscore.com/pricing) for details.
Sovereign Edition: [sales@genstrata.com](mailto:sales@genstrata.com)

## Verify a Certificate

Anyone can verify a Gauntlet Score is genuine:
```
GET https://api.gauntletscore.com/v1/verify/{certificate_id}
```

No authentication required.

## Links

- [API Documentation](https://gauntletscore.com/docs)
- [Terms of Service](https://gauntletscore.com/terms)
- [Privacy Policy](https://gauntletscore.com/privacy)
- [Acceptable Use Policy](https://gauntletscore.com/acceptable-use)

## About

GauntletScore is built by [Genstrata, Inc.](https://genstrata.com) The Gauntlet's adversarial multi-agent verification architecture is patent-pending (USPTO #63/967,169).

For organizations that cannot send data to cloud services, the **Sovereign Edition** runs entirely on your hardware with zero data egress. Contact [sales@genstrata.com](mailto:sales@genstrata.com).
