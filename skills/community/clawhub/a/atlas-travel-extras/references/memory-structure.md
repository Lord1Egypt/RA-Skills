# Memory Structure - Detailed Overview

## Directory Structure

```
~/atlas-travel-extras/
├── memory.md              # Overview & active reminders
├── wishlist/              # Dream destinations
│   └── {destination}.md   # e.g. japan.md, new-zealand.md
├── trips/                 # Active & planned trips
│   └── {year}-{destination}/
│       ├── overview.md    # Summary
│       ├── itinerary.md   # Daily planning
│       ├── budget.md      # Budget & expenses
│       ├── bookings.md    # Bookings (flight, hotel, etc.)
│       └── checklist.md   # Packing list & todo
├── history/               # Completed trips
│   └── {year}-{destination}/
│       ├── overview.md
│       ├── diary.md       # Diary entries
│       ├── recommendations.md  # Recommendations for others
│       └── final-budget.md   # Actual costs
├── documents/             # Travel documents
│   ├── passports.md       # Passports & validity
│   ├── visas.md           # Visas & validity
│   ├── insurance.md       # Travel insurance
│   └── health.md          # Vaccinations, medications
└── templates/             # Reusable templates
    ├── packing-template.md
    ├── budget-template.md
    └── weekend-trip-template.md
```

## Detailed Descriptions

### wishlist/{destination}.md

Dream destinations with all relevant info:

```markdown
# Japan - Dream Destination

## Priority: 1 (Must visit!)

- **Continent:** Asia
- **Best time to travel:** March-April (cherry blossom)
- **Recommended duration:** 14-21 days

## Budget Estimate

| Category | Amount |
|----------|--------|
| Flight | €800-1,200 |
| Accommodation | €1,000-2,000 |
| **TOTAL** | **€3,300-5,100** |

## Highlights
- Tokyo, Kyoto, Osaka
- Cherry blossom or autumn

## Open Questions
- [ ] Does JR Pass make sense?
- [ ] Plan ryokan experience?

**Planned for:** 2027
```

### trips/{year}-{destination}/overview.md

Main overview of a planned trip:

```markdown
# Portugal 2026 - Overview

| Attribute | Value |
|-----------|-------|
| **Destination** | Portugal |
| **Period** | 15.09. - 29.09.2026 |
| **Travelers** | 2 people |
| **Budget** | €3,500 |
| **Status** | 🟡 In Planning |

## Route
Lisbon → Porto → Algarve

## To-Dos
- [ ] Book flights
- [ ] Search hotels
```

### trips/{year}-{destination}/budget.md

Budget planning and daily tracking:

```markdown
# Budget - Portugal 2026

## Overview

| Category | Planned | Actual |
|----------|---------|--------|
| Transport | €1,200 | €_____ |
| Accommodation | €1,000 | €_____ |
| **TOTAL** | **€3,500** | **€_____** |

## Daily Tracking

| Date | Food | Activities | Other | Total |
|------|------|------------|-------|-------|
| 15.09 | €_____ | €_____ | €_____ | €_____ |
```

### documents/passports.md

Document tracking with reminders:

```markdown
# Passports

## Passport (Christian)
- **Number:** DE-XXX-XXX
- **Valid until:** 2030-01-14
- **Status:** 🟢 Valid

### Reminders
- [ ] 2029-07-15 → Apply for new passport (6 months before expiry)
```

### documents/visas.md

Visa tracking:

```markdown
# Visas

## USA ESTA
- **Number:** ...
- **Valid until:** 2026-03-01
- **Status:** 🟢 Valid
- **Reminder:** 2026-02-01 (1 month before expiry)
```

## Reminder System

### Weekly Check (e.g. Sunday)

Check for:
- **Passports:** Validity < 6 months?
- **Visas:** Validity < 1 month?
- **Insurance:** Expiring soon?
- **Planned trips:** Bookings needed?

### Template for memory.md

```markdown
# Atlas Travel Extras - Overview

## 🔔 Active Reminders

### Documents
- [ ] **Passport (Christian)** - Expires: 2030-01-14 → New passport by 2029-07
- [ ] **USA ESTA** - Expires: 2026-03-01 → Renew by 2026-02

## 🗺️ Active Trips
- **Portugal 2026** (15.09. - 29.09.) - Status: 🟡 In Planning

## 📋 Next Steps
- [ ] Portugal: Book flights
- [ ] Portugal: Search hotels

## 💡 Statistics
- **Planned trips:** 1
- **Completed trips:** 0
- **Dream destinations:** 1 (Japan)
```

---

*This file is referenced from SKILL.md*
