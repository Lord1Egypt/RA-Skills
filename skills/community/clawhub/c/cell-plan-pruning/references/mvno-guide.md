# MVNO Reference — US Market Map & Porting Mechanics

> Prices are typical ranges; MVNO market moves monthly. Use as the decision map and verify
> current pricing at switch time.

## What an MVNO actually is

A reseller buying wholesale capacity from one of the three US networks (Verizon, T-Mobile,
AT&T — plus US Cellular regionally). Your coverage and speeds are the **host network's**,
with two caveats:

1. **Deprioritization**: during congestion (stadiums, airports, city rush hour), host-network
   customers get bandwidth first. For everyday use, most people never notice.
2. **Data ceilings / hotspot caps**: "unlimited" MVNO plans often deprioritize heavily or cap
   hotspot at 5–10 GB. Read the plan's line, not the banner.

## Host-network quick map (typical, verify current)

| Host | Known MVNO brands (examples) | Notes |
|---|---|---|
| T-Mobile | Mint Mobile, Metro by T-Mobile (owned), Tello, Google Fi (also US Cellular) | Strong urban/suburban; good int'l roaming rates on some |
| Verizon | Visible, US Mobile (Verizon option), Straight Talk (multi), Total Wireless | Best rural coverage; Visible = flat pricing |
| AT&T | Cricket (owned), Boost Mobile (post-2023 AT&T-based options), Consumer Cellular | Good coverage; AARP-friendly brands |

## Plan-shape decision table

| Your line's 3-mo avg data | Plan shape to buy | Typical all-in |
|---|---|---|
| <2 GB | capped small plan (Tello-style) | $8–$15 |
| 2–5 GB | 5 GB capped | $15–$25 |
| 5–15 GB | 10–15 GB or small unlimited | $25–$40 |
| 15–30 GB | unlimited with hotspot cap | $40–$55 |
| 30+ GB / heavy tether | premium unlimited (postpaid or top MVNO tier) | $55–$80 |

## Porting mechanics (where people break things)

1. **Never cancel the old line first.** The port-out process cancels it automatically; a manual
   cancel first can release your number into limbo.
2. What you need from the old carrier: **account number** + **transfer PIN** (postpaid carriers
   generate this in-app or via support; they sometimes "retain" you — the PIN request is the
   retention trigger, decide before you call).
3. The **NEW carrier initiates the port** during signup (eSIM: usually minutes to 2 hours;
   physical SIM: same day). Keep the old phone on until the port completes.
4. **Installment balances** come due on the next bill after porting; promo credits stop.
   Group lines: port one line first as a test, then the rest.
5. **Locked phones**: carrier-locked until paid off (and sometimes 60 days post-payoff).
   Check: Settings → About → Carrier Lock (iPhone) / OEM unlock status (Android).

## Insurance & protection reality check

| Coverage | Typical cost | Deductible | Verdict pattern |
|---|---|---|---|
| Carrier device protection | $9–$25/mo | $29–$299 | Worth it only in year 1 of a flagship |
| OEM care (AppleCare+/Samsung Care+) | $8–$20/mo | $29–$99 | Better terms; still drop after year ~2 |
| Credit-card phone protection | free w/ card | — | Requires paying the bill with that card — the cheapest real coverage |

Self-insurance math: after month 24, the expected-loss × deductible structure makes "premium in
a jar" strictly better for phones worth under ~$400. Put the $17/mo into the same account as the
phone fund.

## Taxes/fees reality

- Postpaid: taxes/fees stack ~15–25% on top of sticker depending on state/locality
- Prepaid/MVNO: often tax-inclusive or near-flat; some states differ
- **Always compare all-in monthly totals** — the script's `--bill` mode takes both plans' tax
  rates and models the real delta

## When NOT to switch

- You're mid-promo with bill credits that outvalue the MVNO delta (rare but real)
- You need premium hotspot (30+ GB tether) — postpaid tiers still win there
- You live in a deprioritization-sensitive spot (apartment on one congested tower) — test with
  a friend on the host network first
- Your phone is locked with a long balance left — run the exit-cost math first
