---
name: esim-travel-setup
description: "Use before international travel — plans connectivity (eSIM type choice local/regional/global, data sizing from usage profile, dual-SIM strategy keeping home number alive for bank OTPs), audits accounts for 2FA lockout risk (bank SMS abroad, new-device login walls, WhatsApp re-verification), compares eSIM vs roaming bundle vs local SIM costs, and generates the T-48h/T-24h/T-0 checklist including country gotchas (China VPN, Brazil IMEI registration)."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [travel, esim, connectivity, 2fa, security, roaming]
---

# eSIM Travel Setup

## Overview
International travel breaks phones in two predictable places: connectivity
(which SIM, how much data, what it costs) and authentication (bank sends an
OTP to a number that just stopped receiving SMS; Google challenges a login
from a "new device" while you're standing in an airport). The second failure
is the expensive one — locked out of money and mail abroad, people lose days.

This skill plans both, before departure:

1. **plan** — destination + days + usage profile → data sizing, eSIM type
   recommendation (local vs regional vs global), dual-SIM strategy, and
   country gotchas (Great Firewall, IMEI registration, VoIP blocks).
2. **twofa** — account-by-account travel-auth risk audit: what breaks, and
   the exact pre-departure fix (backup codes, pre-trusted devices,
   receive-only roaming for the home SIM).
3. **costs** — eSIM vs carrier roaming bundle vs airport SIM, with the
   break-even logic for trip length.
4. **checklist** — printable T-48h / T-24h / T-0 (airport) sequence,
   including the landing failure protocol.

Pure stdlib, offline.

## When to Use
- Any international trip: "what's my connectivity plan?" (2+ weeks out ideal)
- "Should I buy an eSIM or use my carrier's $10/day travel pass?"
- "Will my bank's 2FA work abroad?" (the question people ask too late)
- Multi-country trips (regional eSIM choice)
- "Going to China/Brazil/UAE/Turkey — anything special?" (gotcha database)
- Setting up a family member's phone before their first trip abroad

**Don't use for:** domestic travel (home network, no problem), permanent
expat relocation (residency, local contracts, number porting — different
domain), or corporate MDM-managed devices (your IT department owns the
auth model).

## How It Works — Numbered Steps
1. Size the data honestly:
   ```
   python3 scripts/esim_planner.py plan --destination Japan --days 12 --profile maps-heavy
   ```
   → 4.8 GB, Asia regional group, dual-SIM strategy, Japan notes.
2. Audit the accounts that matter — minimum bank + primary email:
   ```
   python3 scripts/esim_planner.py twofa --bank --email-google --icloud
   ```
   Execute every BEFORE-DEPARTURE line. Print backup codes on paper.
3. Price the three options:
   ```
   python3 scripts/esim_planner.py costs --destination Mexico --days 10 \
       --data-gb 5 --roaming-bundle 10 --roaming-gb 2
   ```
4. Buy and INSTALL the eSIM at T-48h (activation triggers on first connect
   at the destination — installing early is free and removes airport risk).
5. Work the checklist:
   ```
   python3 scripts/esim_planner.py checklist
   ```
   T-48h → T-24h → T-0, including the dual-SIM toggle sequence on landing.
6. On landing: airplane mode off → travel eSIM attaches in ~2 min → home SIM
   stays on for SMS receive. Send one test message; confirm bank app login.

## The Two-SIM Doctrine (core of the skill)
- **Home SIM stays ACTIVE, roaming, receive-only.** Bank OTPs, WhatsApp
  verification, iMessage/RCS re-confirmation all target your number.
  Receiving SMS abroad is free or near-free on major carriers; NOT having
  it can cost you account access.
- **Travel eSIM carries the data.** Default-data line = travel eSIM.
- **Data switching OFF.** Phones love to silently burn the home SIM's
  roaming data at $15/MB when the travel line hiccups.
- **Never swap the home SIM out** on a single-SIM phone — that's what
  airport physical-SIM kiosks still talk people into.

## Common Pitfalls
1. **Buying the eSIM at the airport.** Install at T-48h; airport wifi +
   provider app + activation queues are a bad combo at 6 AM.
2. **Disabling the home SIM "to avoid roaming charges."** The #1
   self-inflicted 2FA lockout. Receive-only SMS is not a charge risk on
   mainstream carriers — verify once with your carrier, then leave it on.
3. **Relying on SMS-only bank auth.** If your bank supports app-based or
   TOTP 2FA, enroll BEFORE the trip; SMS abroad is single-point-of-failure.
4. **No offline backup codes.** Google/iCloud new-device challenges abroad
   can require codes you printed never. Paper, two locations, not photos.
5. **China VPN procrastination.** VPN apps vanish from app stores once your
   device is inside China. Install and test at T-24h.
6. **Brazil IMEI / Turkey registration rules.** Long-stay registration
   rules silently kill foreign phones after a grace period — the gotcha
   database flags both.
7. **iMessage/SMS "activation failed" loops.** Tied to the home number;
   fixed by keeping home SIM reachable. eSIM data alone doesn't cover it.
8. **Testing nothing.** Every MFA method should be exercised on the travel
   device before departure. A TOTP seed that synced to your old phone only
   is a lockout with extra steps.

## Example
```
Trip: 12 days in Japan, bank that uses SMS OTP, WhatsApp-dependent family.

$ plan --destination Japan --days 12 --profile maps-heavy
→ 4.8 GB; Asia regional eSIM if hopping; dual-SIM doctrine printed.

$ twofa --bank --whatsapp
→ [10/10] bank: enroll app-2FA or keep home SIM roaming for SMS;
  [5/10] WhatsApp: number re-verification needs SMS — home SIM stays on.

$ costs --destination Japan --days 12 --data-gb 5 --roaming-bundle 12
→ eSIM ~$23 vs roaming pass ~$144 → eSIM wins 6x.

$ checklist → install eSIM T-48h, codes on paper, bank travel notice,
  landing sequence: airplane off → eSIM attaches → test bank login.
```

## References
- `references/connectivity-guide.md` — eSIM types compared, dual-SIM
  mechanics per platform, data sizing table, country gotcha list expanded.
- `references/2fa-travel-protocol.md` — the full lockout-scenario catalog
  and the pre-departure hardening sequence, account class by account class.
