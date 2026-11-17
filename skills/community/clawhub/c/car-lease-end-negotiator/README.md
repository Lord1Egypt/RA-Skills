# Car Lease-End Negotiator

**The three-way lease-end decision computed honestly — return vs buyout vs buy-and-sell — plus wear-bill line-item defense and the negotiation card for turn-in day.**

## The problem
A lease ending is three transactions wearing one parking-lot appointment. Used-market swings since 2020 have made residuals routinely wrong in BOTH directions: lessees with $2,000-$5,000 of equity have handed it back by signing the turn-in papers, while lessees at 2022-peak residuals returned cars worth far less than the buyout — the rare case where walking is the win. On top sit four negotiable stacks almost nobody contests: disposition fees, excess-mileage rates, third-party wear adjudication, and pull-ahead "offers." The default decision — whatever the dealer suggests on maturity day — is the most expensive default in personal car finance.

## What this skill does
- `decide` — three-path cost table (return / buyout / buy-and-sell) from residual, market, mileage, fees, and tax; verdict names the path and the dollar difference
- `wear` — line-item audit of the inspection letter vs independent-shop pricing, with the contest-it-vs-fix-it split
- `sheet` — printable negotiation card: what's waivable, what's fixed, what's contestable, call order (captive before credit union before dealer)
- `--demo` — an equity-positive over-mileage lease, a $912 inspection letter, and the card

## Quick example
```bash
python3 scripts/lease_end.py --demo
```
Demo 1: residual $18,000 vs market $20,500, 7,500 miles projected over — returning costs ~$2,575 in fees; buy-and-sell nets ~$700+ instead. The verdict flips the parking-lot script.

## Who needs this
- ~3-4M US lease maturities per year, each facing this exact decision
- Over-mileage lessees deciding between paying the bill and buying out
- Anyone holding an inspection letter with a wear bill
- Anyone offered a "pull-ahead" or "loyalty" lease termination

## Install
Python 3.9+, stdlib only:

```bash
python3 scripts/lease_end.py --demo
```

## License
MIT © Denis Voronin
