# Battery Bank Travel Allocator

**The problem:** a "20000 mAh" power bank delivers ~60–65% of that to your devices — the rating is at 3.7 V cell voltage, delivery is at 5 V (×0.74), conversion and cable heat eat another 15%, and every year of age costs ~4% more. On the demand side, 5 hours of navigation drains a phone 3.5× faster than 5 hours of light use. So the two questions every traveler gets wrong — "will this bank keep my phone alive?" and "which banks should I pack?" — are answered with sticker faith instead of math, and people either carry a brick they never needed or run dry at 4 PM with photos still to take.

**What this does:** stdlib-only Python running the honest energy budget:

- **Bank reality** — rated mAh → deliverable Wh after voltage, conversion, age (4%/yr) and cycle (~8%/500) derating
- **Device demand** — battery library (phone/tablet/camera/watch/earbuds/drone/laptop) × screen hours × activity multipliers (navigation ×3.5, photos ×1.6, hotspot ×2.8, gaming ×4) + idle drain
- **Stop-charge ceilings** — 85% for phones: the last 15% of a charge is the least efficient transfer when a bank is the source
- **Verdicts** — OVER-PROVISIONED (leave the big bank home; pocket space is the scarce resource), FITS (charge priority first), SHORTFALL (named fixes: airplane mode + offline maps = −60% phone drain, lunch-stop wall plug, drop lowest-priority device)
- **Solar reality check** — 50% derate even in the optimistic midday case; backpack panels average 10–25% of sticker

```bash
python3 scripts/power_budget.py plan --banks 20000:2 \
  --devices phone:5:80:navigation phone-big:3:100:photos earbuds:0:40 --hours 12
# total deliverable: 58 Wh | total demand: 19.0 Wh
# VERDICT: OVER-PROVISIONED — leave the biggest bank home
```

## Who needs this

Travelers, hikers, festival-goers, conference attendees, photographers, drone pilots — anyone whose day depends on devices and who owns a drawer of banks of unknown real capacity. Also: anyone about to buy a bank, since the size table shows what each class actually delivers.

## License

MIT
