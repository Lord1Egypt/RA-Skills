---
name: atlas-travel-extras
slug: atlas-travel-extras
version: 1.0.0
description: Personal travel assistant for Atlas - dream destinations, planning, history, documents, budget, checklists and reminders
author: Nova (based on personal-travel concept)
tags: travel, planning, budget, documents, reminders
triggers:
  - "plan a trip"
  - "dream destination"
  - "where should I go"
  - "packing list"
  - "passport expires"
  - "visa"
  - "travel budget"
  - "book flight"
  - "find hotel"
  - "accommodation"
  - "weather"
  - "documents"
  - "insurance"
  - "how much does it cost"
  - "route"
  - "sightseeing"
---

# Atlas Travel Extras

Personal travel assistant for Atlas with 7 core features:

| Feature | Description |
|---------|-------------|
| **Dream Destinations** | Wishlist with priorities, budget estimates, travel time recommendations |
| **Planning** | Routes, budget, sightseeing, transport options |
| **History** | Past trips with dates, impressions, recommendations, costs |
| **Documents** | Track passport (validity), visas, insurance |
| **Budget** | Plan travel budget & track expenses |
| **Checklists** | Packing lists, pre-departure reminders |
| **Reminders** | Automatic alerts: "Passport expires in N months", "Visa ending soon" |

## When to Use

- Planning a trip or managing dream destinations
- Need packing lists or document checklists
- Track budget or document past trips
- Reminders for document renewals (passport, visa)

## Memory Structure

```
~/atlas-travel-extras/
├── memory.md              # Overview & active reminders
├── wishlist/              # Dream destinations
├── trips/                 # Active & planned trips
├── history/               # Completed trips
├── documents/             # Travel documents
└── templates/             # User templates (ref: references/)
```

**Note:** `templates/` is for local user copies. Reference templates remain in `references/`.

**Details:** See [memory-structure.md](references/memory-structure.md)

## Workflow & Code Examples

### Input: Plan a Trip

```markdown
## Portugal 2026
- **Period:** 15.09. - 29.09.2026
- **Travelers:** 2 people
- **Budget:** €3,500
- **Status:** 🟡 Planning
```

**Output:** Trip folder with templates

```
trips/2026-portugal/
├── overview.md      # Summary
├── itinerary.md     # Day-by-day plan
├── budget.md        # Expense tracking
├── bookings.md      # Confirmation numbers
└── checklist.md    # Pre-departure tasks
```

### Tools & Actions

| Action | Command | Creates |
|--------|---------|---------|
| Add destination | Create `wishlist/{name}.md` | Dream entry |
| Start trip planning | Create `trips/{folder}/` | Trip workspace |
| Copy templates | Copy from `references/*.md` | Ready-to-use files |
| Check reminders | Read `documents/*.md` | Active alerts |
| Show packing list | Display `references/packing-*.md` | Customized list |

## References

| File | Content |
|------|---------|
| **Planning** ||
| [memory-structure.md](references/memory-structure.md) | Detailed memory structure |
| [trip-kanban-template.md](references/trip-kanban-template.md) | Trip Kanban board |
| **Packing** ||
| [packing-template.md](references/packing-template.md) | General packing list |
| [packing-beach.md](references/packing-beach.md) | Beach items |
| [packing-hiking.md](references/packing-hiking.md) | Hiking gear |
| [packing-business.md](references/packing-business.md) | Business travel |
| [packing-winter.md](references/packing-winter.md) | Winter/ski items |
| **Tools** ||
| [budget-template.md](references/budget-template.md) | Budget planner |
| [document-checklist.md](references/document-checklist.md) | Document checklist |
| [weekend-trip-template.md](references/weekend-trip-template.md) | Weekend trips |
| [flight-price-template.md](references/flight-price-template.md) | Price tracking |
| [statistics-template.md](references/statistics-template.md) | Travel stats |
| [emergency-card-template.md](references/emergency-card-template.md) | Emergency card |

## Examples

| File | Shows |
|------|-------|
| [examples/wishlist/japan.md](examples/wishlist/japan.md) | Dream destination |
| [examples/trips/2026-portugal/overview.md](examples/trips/2026-portugal/overview.md) | Trip planning |
| [examples/documents/passports.md](examples/documents/passports.md) | Document tracking |

---

**Created:** 2026-04-08
**Author:** Nova
**Version:** 1.0.0
