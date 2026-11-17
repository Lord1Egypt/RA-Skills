---
name: car-wash-planner
description: "Work out how often a car needs washing from where it is parked and how it is driven, pick the right level of wash (basic, wash and wax, deep interior, full detail) from the car's condition, and build a dated wash calendar with a cost estimate from the user's own local prices. Use when someone asks how often to wash their car, which wash or detailing service they need, or what a few months of washing will cost."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🚿"
    homepage: https://turboluxurycarwash.ae/
---

# Car wash planner

Instruction-only: no commands, installs or network access. Follow the steps below and do the arithmetic yourself.

## When to use

- "How often should I wash my SUV if it is parked outside all day?"
- "The seats are stained and the AC smells. What kind of wash do I need?"
- "Plan my washes from 1 November for three months and tell me the cost."

## 1. Collect the car profile

Ask only for what is missing. Defaults are in brackets.

- Vehicle: sedan, SUV, premium or sports car (sedan)
- Parking: outdoor, covered or garage (outdoor)
- Driving: city, mixed, or dusty/unpaved roads (city)
- Cabin load: smoker, pets, small children (none)
- Problems: stained seats, AC smell, hazy headlights (none)
- Months since last wax, last deep interior clean, last engine bay clean (unknown)

## 2. Wash interval

| Parking | Base days |
|---|---|
| Outdoor | 7 |
| Covered | 10 |
| Garage | 14 |

Adjust for driving: city 0, mixed -1, dusty or unpaved -3. Also take 2 days off for regular coastal salt air or road salt in winter. Clamp the result to 4-21 days.

## 3. Wash level

Use four levels. Pick the lowest level that covers every trigger found.

| Level | What it covers |
|---|---|
| 0 Basic | Exterior wash, quick interior vacuum and wipe, windows, wheels, mats |
| 1 Wash and wax | Level 0 plus a wax or sealant coat and a deeper interior clean |
| 2 Deep clean | Level 1 plus engine bay cleaning and interior sanitising |
| 3 Full detail | Seat shampoo or extraction, AC vent sanitising, interior restoration, headlight polishing |

Triggers:

- Wax older than 3 months (2 months for premium or sports car paint): level 1
- Smoker, pets or children and the last deep interior clean was 3+ months ago: level 1
- Engine bay not cleaned for 12+ months: level 2
- Pets or smoker and the last deep interior clean was 6+ months ago: level 2
- Stained seats, AC smell, hazy headlights, or no deep interior work for 12+ months: level 3
- No triggers: level 0

Give one short reason for each trigger you used.

## 4. Dated plan

1. Start on the user's start date (today if none).
2. Add one visit every interval until the end of the period (count a month as 30 days).
3. Visit 1 uses the recommended level. After that, use level 0, except visits 5, 9, 13 and so on (every fourth visit after the first), which are level 1 so the wax and interior stay fresh.
4. List each visit as `YYYY-MM-DD  level name`.

## 5. Cost

Ask the user what each level costs where they live, or take a price range they already have. Do not invent local prices. Multiply each visit by its price (keep min and max if they gave ranges), then give the total and the total divided by the number of months. If they have no prices, give the plan with a count of visits per level so they can price it.

## Example

SUV, outdoor parking, dusty roads, pets, stained seats, wax 4 months old. Interval: 7 - 3 = 4 days. Level 3 (stained seats). A 1-month plan from 2026-11-01 gives 8 visits: the 1st is a full detail, the 5th is wash and wax, and the rest are basic washes.

## Notes

- These are rules of thumb, not a quote. A professional may recommend more after seeing the car.
- Never book or message a business for the user. Give them the plan and let them book.

## Links

- Need someone to come to you? [mobile car wash](https://turboluxurycarwash.ae/)
