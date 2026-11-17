# Connectivity Guide — eSIMs, Dual-SIM, Data, Country Gotchas

## eSIM product types
| Type | Coverage | $/GB | Best for |
|---|---|---|---|
| Local (single country) | 1 | best (often $2-5/GB) | one-country trips |
| Regional (Europe/Asia/SEA...) | 5-15 | middle | multi-country itineraries |
| Global | 120-190 | worst per GB | 3+ region hops, frequent travelers |

Rules of thumb:
- One country, any length → local eSIM (carrier direct or marketplace).
- 2-6 adjacent countries → regional.
- Round-the-world or US→EU→Asia → global, or stack locals.
- Buying at the destination airport = highest price + queue + registration
  hassle; buying from your carrier at home = roaming prices. Pre-purchase.

## Where to buy (categories, not endorsements)
- Marketplace apps: Airalo, Saily, Nomad, Holafly (unlimited tiers at a
  price premium), Ubigi (car-maker ties).
- Carrier-direct eSIMs: often the best $/GB (e.g. Japan KDDI/au tourist
  products, Hong Kong CSL, Germany's Blau/Telekom prepaid).
- Your home carrier's "travel pass": convenient, 3-10x the price; fine for
  1-3 days, poor for a week+.

## Dual-SIM mechanics
Modern phones hold 1 physical SIM + 1-5 eSIM profiles (2 active lines
typically). The travel setup:

```
Line 1 (home SIM):  ON, roaming, SMS receive — NO data
Line 2 (travel):    ON, default data — YES
"Allow cellular data switching": OFF
```

iOS: Settings → Cellular → set travel line as default; turn OFF data on the
home line. iMessage stays registered to home number.
Android: Settings → Network → SIMs — same pattern; disable "auto switch
data".

WhatsApp binds to your NUMBER, not your SIM — it keeps working over the
eSIM's data, but re-verification (new phone, re-install) sends SMS to the
home number. Keep it reachable.

## Data sizing table (per day)
| Profile | GB/day | Typical behavior |
|---|---|---|
| light | 0.15 | messaging, mail, occasional maps |
| maps-heavy | 0.40 | all-day navigation, lookups, social, music |
| heavy | 0.80 | video calls, laptop hotspot, streaming |
| work | 1.20 | full workdays on LTE, cloud IDE, big files |

Multipliers: navigation-heavy group trips where you're the navigator +30%;
video-call home nightly +0.2-0.5 GB/call-hour; offline maps downloaded
beforehand −20-40% of maps load.

Sanity check: your phone's Settings → Cellular → data usage history is the
ground truth. Past 30 days ÷ 30 = your real profile.

## Country gotchas (expanded)
| Country | Gotcha |
|---|---|
| China | Great Firewall blocks Google/WhatsApp/Instagram/many VPN endpoints; install + test a VPN BEFORE arrival — app stores delist VPNs inside China. eSIMs work; the filter is the issue. |
| Japan | Sparse public wifi; eSIM strongly advised; clean Internet. |
| Brazil | ANATEL IMEI registration for foreign phones; unregistered devices lose cellular after ~15 days. Register at airport or operator kiosk early. |
| Turkey | Phones used with foreign SIMs >120 days must be registered (a tax); short tourist trips unaffected. Tourist SIM prices are high — eSIM ahead. |
| UAE | Standard VoIP (WhatsApp/Meet audio) blocked on consumer plans; SMS/data fine. |
| Russia | SMS to foreign numbers unreliable; foreign cards don't work — cash + connectivity planning both. |
| India | eSIM works on major carriers; physical-SIM kiosks need passport + photo, 1-2h process. |
| USA | Foreign numbers may pay per-received-SMS on prepaid home plans; T-Mobile/AT&T prepaid can't roam at all — eSIM before departure. |
| Thailand | Easy tourist SIMs (AIS/dtac at airport); eSIM equivalents exist and skip the queue. |
| Iran | Connectivity itself is the risk; sanctioned payment rails; specialized prep required. |

## Landing sequence (works everywhere)
1. Airplane mode OFF with BOTH lines on.
2. Travel eSIM attaches to a local network in ~30-120s.
3. If no attach in 5 min: toggle airplane mode 15s; verify eSIM line is ON;
   try manual network selection.
4. Confirm home line shows signal (for SMS receive).
5. Send a test message; log into your bank app once — while standing in the
   airport with wifi as fallback — to surface any challenge NOW.

## Failure protocol
- eSIM dead after 10 min → airport wifi → provider app diagnostics
  (activation usually needs internet once) → if unrecoverable, buy a
  day-pass roaming add-on for today and dispute the eSIM later.
- Never let the failure cascade into "so I turned off my home SIM" — that
  converts a connectivity problem into an authentication problem.
