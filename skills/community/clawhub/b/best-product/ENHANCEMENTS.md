# best-product Skill Enhancements

## Implemented

- v1.0.3 (2026-03-24): Updated sources list (Xataka ES, Benchmark.pl PL, Komputer Świat PL added), improved regional retailer tables, enhanced link verification workflow
- v1.0.2 (2026-03-23): Fixed language rule (bilingual support for NL/BE), clarified output format (price • retailer), updated Google Search URL per region
- v1.0.1 (2026-03-09): Added Link Verification rules, fixed markdown link format

---

## Planned

### Alternatives Feature

**Priority:** High

**Problem:** Top pick often out of stock or unavailable. Users need instant fallback.

**Proposed Implementation:**

```
🏆 TOP PICK
Philips Airfryer XXL — €149
[summary]
🔗 https://google.nl/...
❌ Out of stock at Coolblue, MediaMarkt

💎 ALTERNATIVE
 Ninja Foodi Max — €139
[summary, slightly different specs]
🔗 https://google.nl/...
✅ In stock at Coolblue

💶 ALTERNATIVE
Cosori Air Fryer — €99
[summary, budget alternative]
🔗 https://google.nl/...
✅ In stock at Amazon NL
```

**Data Sources:**
- Stock: Kieskeurig (has "voorraad" status), Coolblue API if available
- Alternatives: Find by price bracket + category similarity

**Technical approach:**
1. After finding top pick, check stock at major retailers via Kieskeurig
2. If out of stock → find similar-priced alternatives from same category
3. Flag with ✅/❌ stock status

---

### Price Alerts (Future)

- Store threshold in `~/.openclaw/cache/alerts.json`
- Daily cron checks Kieskeurig/Tweakers/Keepa
- Notify when price drops below threshold
