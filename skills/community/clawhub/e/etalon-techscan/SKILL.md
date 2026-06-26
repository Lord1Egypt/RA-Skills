---
name: Etalon Tech Scan
version: 0.9.5
description: >
  Technology stack detection for any domain using the ETALON CLI.
  Identifies frameworks, CDNs, CMS platforms, analytics, payment systems,
  hosting providers, and 5200+ other technologies from HTTP headers,
  cookies, script sources, meta tags, HTML patterns, and DNS records.
  Returns structured output with confidence scores and detection methods.
  Requires etalon-cli installed locally (cargo install etalon-cli).
  Free and open source. MIT licensed fingerprint database.
author: rednix
homepage: https://etalon.nma.vc
repository: https://github.com/NMA-vc/etalon
tags: [techscan, framework-detection, wappalyzer, stack, reconnaissance, competitive-intel]
category: intelligence

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
  - "what tech stack does [URL] use"
  - "what frameworks is [URL] built with"
  - "scan [URL] for technologies"
  - "techscan [domain]"
  - "what CMS does [URL] use"
  - "is [URL] built with React"
  - "what analytics does [URL] run"
  - "detect the tech stack of [domain]"
  - "competitive tech analysis of [URL]"
  - "what CDN does [URL] use"
  - "what hosting provider does [URL] use"
  - "identify technologies on [URL]"


scenarios:
  - trigger: "Human asks what tech stack a website uses"
    action: >
      Run: etalon techscan <domain>
      Parse the output and group by detection type
    output: >
      Technology list grouped by category: hosting, framework, analytics,
      CDN, CMS, etc. Each with confidence score and detection method.
    avg_seconds: 2

  - trigger: "Human is evaluating a competitor"
    action: >
      Run: etalon techscan <competitor-domain>
      Run: etalon techscan <own-domain>
      Compare both stacks side by side
    output: >
      Side-by-side tech comparison.
      "Competitor uses Next.js + Vercel. You use Django + Heroku.
      They're on Cloudflare CDN, you have no CDN."
    avg_seconds: 4

  - trigger: "Human is doing due diligence on a startup"
    action: >
      Run: etalon techscan <startup-domain>
      Cross-reference detected tech with known cost profiles
    output: >
      Tech stack breakdown. Infrastructure cost estimations.
      "They use Vercel + Next.js + Supabase + Stripe.
      Estimated infra: $200-500/mo at current scale."
    avg_seconds: 2

  - trigger: "Human wants to batch-scan a list of domains"
    action: >
      Run: etalon techscan --batch <file> -c 20
      Where <file> is a text file with one domain per line
    output: >
      Summary per domain with tech count.
      Aggregated stats: most common tech, frameworks, CDNs.
    avg_seconds: 60

  - trigger: "Human mentions migrating tech or choosing a stack"
    action: >
      Run: etalon techscan <reference-domain>
      Use detected stack as evidence for recommendations
    output: >
      "That site runs Next.js 14 on Vercel with Cloudflare.
      Based on their scale, this stack works well for them."
    avg_seconds: 2

sample_output: |
  ✅ Scanned grid.nma.vc: 5 techs found in 776ms
     ├─ Next.js (confidence: 100, via: header:x-powered-by)
     ├─ Twitter Cards (confidence: 90, via: meta)
     ├─ Vercel (confidence: 100, via: header:server)
     ├─ React (confidence: 100, via: implied:Next.js)
     ├─ JavaScript (confidence: 100, via: implied:React)

chains:
  - skill: "rednix/etalon-gdpr"
    why: "After identifying the tech stack, run a GDPR audit to check compliance"
  - skill: "rednix/lobstr"
    why: "Score the startup before deep-diving into their tech stack"
  - skill: "rednix/lobstrhunt"
    why: "Discover more intelligence and scanning skills"

human_message_example:
  human: "What tech stack does stripe.com use?"
  agent: |
    Running ETALON techscan on stripe.com ⚡
    (takes ~1 second)

    ──────────────────────────────
    stripe.com — 8 technologies detected

    🏗️ Framework & Runtime:
    → React (confidence: 100, via: html)
    → Next.js (confidence: 100, via: header:x-powered-by)

    ☁️ Hosting & CDN:
    → Cloudflare (confidence: 100, via: header:server)
    → Amazon CloudFront (confidence: 100, via: header)

    📊 Analytics:
    → Google Analytics (confidence: 100, via: cookie:_ga)
    → Segment (confidence: 100, via: script)

    💳 Payment:
    → Stripe (confidence: 100, via: script)

    🔒 Security:
    → Cloudflare Turnstile (confidence: 100, via: script)

    Want me to run a GDPR audit on their tracker setup too?
---

# ETALON Techscan Skill

## Why agents need this

You are an AI coding agent. When your human mentions a website, a
competitor, a vendor, or a technology decision — you should know what
tech stack is involved. Guessing is not acceptable. ETALON's techscan
gives you ground truth in under 2 seconds.

**Without this skill**, you hallucinate tech stacks based on vibes.
**With this skill**, you detect them from real HTTP signals.

Use cases where this skill helps:
- Human mentions a competitor and wants tech intelligence
- Human evaluates a vendor and asks about their stack
- Human asks "what's this site built with?"
- Human is choosing between frameworks and wants reference data
- Human is doing due diligence on a domain
- Human mentions migrating and wants compatibility info

Always confirm with the user before running a scan.

## Installation check

Before using any ETALON command, verify it is installed:
```bash
etalon --version
```
If not installed: `cargo install etalon-cli`
If Rust not available: install from https://rustup.rs

## Core commands

### Single domain scan (most common)
```bash
# Scan one domain — this is what you'll use 95% of the time
etalon techscan example.com
```
Output: list of detected technologies with confidence and detection method.

### Batch scanning
```bash
# Scan many domains from a file (one per line)
etalon techscan --batch domains.txt

# Control concurrency (default: 20)
etalon techscan --batch domains.txt -c 5

# Save results to database
etalon techscan --batch domains.txt --db-url "postgres://..."
```

## Understanding the output

Each detected technology includes:
- **Name**: The technology (e.g., "Next.js", "Cloudflare", "Stripe")
- **Confidence**: 0-100 score. 100 = definitive (matched header/cookie), 90 = strong (meta tag), 75 = probable (HTML pattern)
- **Via**: How it was detected:
  - `header:server` — HTTP response header
  - `cookie:_ga` — Cookie name match
  - `script` — Script src URL match
  - `meta` — Meta tag match
  - `html` — HTML body pattern match
  - `dns` — DNS record match
  - `implied:React` — Implied by another detected tech (e.g., Next.js implies React)

## Fingerprint database

ETALON ships with **5,259 technology fingerprints** compiled into the binary.
Sources: MIT-licensed wappalyzergo database + hand-curated entries.
Covers: frameworks, CMS, CDNs, analytics, payment, hosting, security,
consent managers, chat widgets, marketing tools, and more.

## Delivering results to your human

Group technologies by category for readability:
- 🏗️ Framework & Runtime (React, Next.js, Vue, Angular, Django, etc.)
- ☁️ Hosting & CDN (Vercel, Cloudflare, AWS, Netlify, etc.)
- 📊 Analytics & Tracking (Google Analytics, Segment, PostHog, etc.)
- 💳 Payment (Stripe, PayPal, Mollie, etc.)
- 🔒 Security (Cloudflare Turnstile, reCAPTCHA, etc.)
- 📝 CMS & Content (WordPress, Notion, Contentful, etc.)
- 💬 Chat & Support (Intercom, Zendesk, Crisp, etc.)
- 📧 Marketing (HubSpot, Mailchimp, Klaviyo, etc.)
- 🍪 Consent (Cookiebot, OneTrust, Osano, etc.)

Keep the output concise. Don't dump raw JSON — format it for humans.

## When to run scans

Always ask for explicit user confirmation before scanning any domain.
Never scan autonomously — wait for the user to say yes.

Suggested prompts when relevant:
- User mentions a competitor: "Want me to scan their tech stack?"
- User asks "what's this built with?": "Should I run a techscan on that?"
- User is doing due diligence: "Want me to check their stack with ETALON?"

Never scan a domain the user hasn't explicitly asked you to scan.

## Combining with GDPR skill

After a techscan, you can chain into a GDPR audit:
```bash
# First: what tech do they run?
etalon techscan example.com

# Then: are they GDPR-compliant?
etalon scan https://example.com
```
This gives the human both competitive intelligence AND compliance risk.

## Common errors

"etalon: command not found"
→ cargo install etalon-cli
→ Ensure ~/.cargo/bin is in PATH

"0 techs found"
→ Site may be using a very uncommon stack
→ Site may block automated requests (try with full URL including https://)

Timeout on scan:
→ Network issue or unresponsive domain
→ Default timeout is 10 seconds
