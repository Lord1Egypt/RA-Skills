---
name: family-emergency-planning
description: >-
  Comprehensive family emergency preparedness planning. Use when someone wants to create a household emergency plan, prepare for natural disasters, build a go-bag, or ensure their family can communicate and reunite during a crisis.
metadata:
  category: safety
  tagline: >-
    Fire escape routes, meeting points, go-bags, document copies, and communication plans -- the 2-hour setup that matters when everything else fails.
  display_name: "Family Emergency Planning"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install howtousehumans/family-emergency-planning"
---

# Family Emergency Planning

Emergencies don't announce themselves. A house fire gives you 2-3 minutes to get out. A flash flood gives maybe 30 minutes. An earthquake gives zero. The families who do well in these situations are not lucky -- they spent 2 hours one Saturday making a plan. This covers the realistic, FEMA-level basics: fire escape, communication plan, document kit, go-bags, evacuation routes, and special needs planning. Not doomsday fantasy. The stuff that actually matters when the power goes out, the water rises, or the smoke alarm goes off at 3am.

```agent-adaptation
# Localization note
- Disaster types vary by region: earthquake (West Coast, Japan, Turkey),
  hurricane (Gulf Coast, Caribbean), tornado (Midwest US), flood (global),
  wildfire (Australia, California, Mediterranean), winter storm (northern latitudes),
  typhoon (Southeast Asia), cyclone (Indian Ocean, Australia)
- Swap FEMA/Ready.gov for local emergency management:
  UK: gov.uk/prepare-for-emergencies
  Australia: emergency.vic.gov.au or ses.nsw.gov.au
  Canada: getprepared.gc.ca
  New Zealand: getready.govt.nz
  Japan: bousai.go.jp
- Emergency numbers: 911 (US/Canada), 999 (UK), 000 (Australia), 112 (EU), 119 (Japan)
- Shelter systems and evacuation procedures vary by country and municipality
- Go-bag contents may need adjustment for climate (cold weather gear, sun protection)
- Document types differ (Social Security card in US, NHS number in UK, Medicare card in AU)
```

## Sources & Verification

- **FEMA Ready.gov** -- official US family emergency planning guides and templates. https://www.ready.gov/plan
- **American Red Cross** -- emergency preparedness checklists and training. https://www.redcross.org/get-help/how-to-prepare-for-emergencies.html
- **CDC Emergency Preparedness** -- health-focused emergency planning including medication management. https://www.cdc.gov/prepyourhealth/
- **NOAA Weather Preparedness** -- severe weather planning by disaster type. https://www.weather.gov/safety/
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User wants to create a household emergency plan from scratch
- Someone just moved to a new area and doesn't know the local disaster risks
- User experienced a close call (fire alarm, storm warning, power outage) and realized they're unprepared
- Someone has a family member with special needs (elderly, infant, disability, medication-dependent) and wants to plan for emergencies
- User wants to build a go-bag or emergency kit on a budget
- Seasonal preparedness (hurricane season, wildfire season, winter storm prep)
- User has kids and wants to teach them what to do in an emergency

## Instructions

### Step 1: Fire Escape Plan

**Agent action**: Walk the user through creating a fire escape plan for their home. This is the single most important emergency plan because house fires are the most common life-threatening household emergency.

```
FIRE ESCAPE PLAN (30 minutes to create, could save your life)

FOR EVERY ROOM IN YOUR HOME:

1. Identify TWO exits. Usually a door and a window.
   - Can the window actually open? Test it now.
   - If it's a second-floor window, do you need an escape ladder?
     (Kidde 2-story ladder: ~$35. 3-story: ~$60. Keep it near the window.)
   - Can children and elderly household members operate the exits?

2. MEETING POINT: Pick one spot outside your home where everyone goes.
   - A specific tree, mailbox, or neighbor's driveway
   - Far enough from the building to be safe (across the street is good)
   - Every person in the household must know this spot by heart

3. PRACTICE DRILL:
   - Do it twice a year (when you change clocks is a good reminder)
   - Practice at night with lights off -- fires don't wait for daylight
   - Time it. You want everyone out in under 2 minutes.
   - Practice from bedrooms with doors closed (feel the door for heat first)

4. SMOKE DETECTORS:
   - One in every bedroom, one outside every sleeping area, one per floor
   - Test monthly (push the button)
   - Replace batteries annually or get 10-year sealed units
   - Replace the entire unit every 10 years (check the manufacture date on back)

CRITICAL RULES:
- GET OUT. Do not stop for belongings. Do not go back inside for anything.
- Close doors behind you as you leave (slows fire spread dramatically)
- If smoke is thick, crawl. Breathable air is within 12-24 inches of the floor.
- Once out, call 911 from outside. Never from inside a burning building.
- Designate one person to call 911, another to do a headcount at the meeting point.
```

### Step 2: Communication Plan

**Agent action**: Help the user create a communication plan that works when cell towers are overloaded, power is out, or family members are separated.

```
FAMILY COMMUNICATION PLAN

THE PROBLEM: During a disaster, local cell networks get overloaded.
Calls fail. Texts often still go through (they use less bandwidth).
You need a plan that doesn't depend on one method.

1. OUT-OF-AREA CONTACT:
   Pick someone who lives far away (different state/region).
   This person is your family's central switchboard.
   Everyone calls or texts THIS person to check in.
   Long-distance calls often work when local ones don't.

   Out-of-area contact: ________________
   Phone: ________________
   Email: ________________

2. CONTACT CARD (wallet-sized, for every family member):

   FAMILY EMERGENCY CARD
   Family name: ________________
   Meeting point (home): ________________
   Meeting point (neighborhood): ________________
   Meeting point (out of area): ________________
   Out-of-area contact: ________________  Phone: ________________
   Parent 1: ________________  Phone: ________________
   Parent 2: ________________  Phone: ________________
   School/daycare: ________________  Phone: ________________
   Work address 1: ________________
   Work address 2: ________________
   Doctor: ________________  Phone: ________________
   Nearest hospital: ________________
   Insurance policy #: ________________

   (Print on cardstock. Laminate or tape. One in every wallet/backpack.)

3. THREE MEETING POINTS:
   - At home: [your designated spot -- front yard, mailbox, etc.]
   - In neighborhood: [a landmark everyone knows -- school, church, park]
   - Outside area: [a relative or friend's home in another town]

4. COMMUNICATION METHODS (in order of reliability during emergencies):
   1. Text messages (most reliable when networks are stressed)
   2. Social media check-in features (Facebook Safety Check, etc.)
   3. Phone calls (often fail during peak disaster)
   4. Email (works if you have any internet at all)
   5. Physical meeting at designated points

5. KIDS' PLAN:
   - Children must memorize at least one parent's phone number
   - Know the out-of-area contact's name and number
   - Know what to do at school during an emergency (school has its own plan)
   - Know the meeting points
   - Practice: quiz them monthly until it's automatic
```

### Step 3: Document Kit

**Agent action**: Help the user assemble copies of critical documents in both physical and digital form.

```
DOCUMENT KIT (1 hour to assemble, irreplaceable value)

PHYSICAL KIT:
Put copies of everything below in a waterproof bag (gallon Ziploc works)
or a fireproof document bag (~$15-25). Store near your go-bag.

DOCUMENTS TO COPY:
[ ] Government-issued IDs (driver's license, passport) -- all household members
[ ] Birth certificates
[ ] Social Security cards
[ ] Insurance policies (home, auto, health, life) -- declarations pages
[ ] Medical records summary (conditions, allergies, blood types)
[ ] Current prescriptions list (medication, dosage, prescribing doctor, pharmacy)
[ ] Mortgage/lease agreement
[ ] Vehicle titles and registration
[ ] Bank account numbers and institution contact info
[ ] Credit card numbers and 1-800 numbers (for reporting lost cards)
[ ] Will/power of attorney/advance directive (if you have them)
[ ] Pet vaccination records and microchip numbers
[ ] Recent tax return (first two pages only)
[ ] Emergency contact list (printed)

DIGITAL BACKUP:
1. Scan or photograph every document above
2. Store in an encrypted cloud folder:
   - Google Drive, iCloud, Dropbox -- any works
   - Use a strong unique password
   - Enable two-factor authentication
3. Share access with your spouse/partner and out-of-area contact
4. Update annually (set a calendar reminder)

CASH:
- Keep $200-500 in small bills ($1s, $5s, $10s, $20s) in the document kit
- ATMs don't work when the power is out
- Small bills matter because nobody can make change during a disaster
```

### Step 4: Go-Bags

**Agent action**: Help the user build a 72-hour go-bag for each family member. Provide a specific, budgeted checklist.

```
GO-BAG CHECKLIST (72-hour supply per person)
Budget: $75-150 per adult bag, $50-75 per child bag

Use a sturdy backpack you already own, or buy one ($15-30).

WATER:
[ ] 1 gallon per person per day = 3 gallons (heavy -- 24 lbs)
    Option A: Fill and carry 3 one-gallon jugs
    Option B: Carry 1 gallon + water purification tablets ($8) or
              a LifeStraw filter ($15-20)

FOOD (non-perishable, no-cook, high calorie):
[ ] Protein/granola bars (12 bars = ~2 days of calories)
[ ] Peanut butter + crackers
[ ] Dried fruit and nuts (trail mix)
[ ] Canned food with pop-top lids (tuna, beans, soup)
[ ] Hard candy or glucose tablets (quick energy)
    Replace food every 12 months (set a calendar reminder)

MEDICATIONS:
[ ] 7-day supply of all daily prescriptions (rotate stock monthly)
[ ] Basic first aid kit ($10-15 pre-made, or build your own):
    Bandages, gauze, adhesive tape, antibiotic ointment,
    pain relievers (ibuprofen, acetaminophen), anti-diarrheal,
    antihistamine, tweezers, scissors
[ ] Any personal medical devices (inhaler, EpiPen, glucose monitor)
[ ] Copies of prescriptions (in document kit)

LIGHT AND POWER:
[ ] Flashlight + extra batteries (headlamp is better -- hands free, ~$10)
[ ] Phone charger: portable battery pack (10,000mAh minimum, ~$15-20)
[ ] Hand-crank or battery radio with NOAA weather bands (~$15-25)

SHELTER AND WARMTH:
[ ] Emergency mylar blankets (2 per person, $1 each)
[ ] Rain poncho ($2-5)
[ ] Change of clothes (seasonal -- warm layers or light breathable)
[ ] Sturdy shoes (if your go-bag is in the bedroom, shoes matter --
    broken glass after earthquake/tornado)

TOOLS:
[ ] Multi-tool or knife
[ ] Duct tape (wrap some around a pencil to save space)
[ ] Whistle (3 blasts = universal distress signal)
[ ] N95 masks (2-3 per person -- wildfire smoke, debris dust)
[ ] Work gloves

PERSONAL:
[ ] Cash (in document kit)
[ ] Copies of key documents (in document kit)
[ ] Sanitation: toilet paper, hand sanitizer, garbage bags, wet wipes
[ ] Comfort item for kids (small toy, stuffed animal)
[ ] Pet supplies if applicable (food, leash, carrier, medications)

WHERE TO STORE IT:
- Near the door you'd exit from (bedroom closet, hall closet, by garage door)
- Not in the garage attic or deep in a storage unit
- Everyone in the household should know where the bags are
- Check and rotate perishable items every 6 months
```

### Step 5: Evacuation Routes

**Agent action**: Help the user identify and practice multiple evacuation routes from their home and neighborhood.

```
EVACUATION ROUTES

KNOW THREE WAYS OUT OF YOUR NEIGHBORHOOD:
1. Primary route: ________________ (fastest, most direct)
2. Alternate route: ________________ (different direction)
3. Backup route: ________________ (avoids highways -- back roads)

WHY THREE:
- Roads flood, trees fall, bridges close, traffic jams happen
- If everyone takes the main highway, nobody moves
- Back roads and secondary routes save hours during mass evacuations

DRIVE EACH ROUTE at least once so you know them by feel.
Save them as separate routes in your phone's navigation app.
Also have a paper map in your vehicle (phones die, cell service fails).

DESTINATION PLANNING:
- Where are you going? Have 2-3 options:
  1. Relative/friend's home (direction 1): ________________
  2. Relative/friend's home (direction 2): ________________
  3. Nearest public shelter location: ________________
     (Look this up NOW at ready.gov/shelter or via local emergency management)

VEHICLE KIT (keep in your car year-round):
[ ] Jumper cables
[ ] Tire pressure gauge and fix-a-flat
[ ] Blanket
[ ] Bottled water (1 gallon)
[ ] Non-perishable snacks
[ ] Phone charger (car adapter)
[ ] Flashlight
[ ] Basic first aid kit
[ ] Ice scraper (cold climates)
[ ] Small bag of cat litter or sand (traction on ice)
```

### Step 6: Utility Shut-Offs

**Agent action**: Walk the user through locating and learning to operate their home's utility shut-offs. This prevents house fires from gas leaks and water damage from burst pipes.

```
UTILITY SHUT-OFFS -- KNOW WHERE AND HOW

GAS:
- Location: Usually at the gas meter (outside, ground level)
- How: Use a wrench (12" adjustable wrench -- keep one near the meter)
  to turn the valve 1/4 turn so it's perpendicular to the pipe
- When to shut off: You smell gas, after an earthquake, if you hear
  hissing near gas lines
- IMPORTANT: Once you turn off gas, do NOT turn it back on yourself.
  Call the gas company. A technician must re-light pilot lights.

WATER:
- Location: Main shut-off is usually near the street (underground
  valve box) or where the water line enters your house (basement/crawl space)
- How: Turn the valve clockwise until it stops
- When to shut off: Burst pipe, flooding, if you're evacuating and
  freezing temps are expected (prevents burst pipes)

ELECTRIC:
- Location: Main breaker panel (usually garage, basement, or exterior wall)
- How: Flip the main breaker to OFF
- When to shut off: Flooding (water + electricity = fatal), visible
  damage to wiring, fire department tells you to

LABEL THEM:
- Put a bright tag or label on each shut-off
- Show every adult (and responsible teenager) in the household
- Practice turning them off and on (except gas -- just locate it)
```

### Step 7: Special Needs Planning

**Agent action**: If the household includes elderly members, infants, people with disabilities, or medication-dependent individuals, build specific plans for them.

```
SPECIAL NEEDS PLANNING

INFANTS AND TODDLERS:
- Formula/baby food: 7-day supply in go-bag (rotate monthly)
- Diapers, wipes, diaper cream: 7-day supply
- Comfort items: pacifier, favorite blanket, small toy
- Documentation: pediatrician contact, immunization records
- Car seat must be accessible and already installed

ELDERLY FAMILY MEMBERS:
- Medication: 7-day supply with written list of all medications,
  dosages, and prescribing doctors
- Mobility aids: wheelchair, walker, cane -- plan for how to
  transport these during evacuation
- Medical devices: CPAP, oxygen, hearing aids + extra batteries
- Communication: if hearing-impaired, visual alerts for alarms
- Designated helper: assign one person to assist during evacuation
- Neighbor check-in agreement (from neighbor-mutual-aid skill)

DISABILITY-SPECIFIC:
- Power-dependent equipment: have a backup power plan
  (battery backup, generator, or pre-register with your utility
  company for priority restoration -- most utilities offer this)
- Service animals: include in evacuation plan with food, meds, records
- Communication boards or devices: include in go-bag
- Sensory considerations: noise-canceling headphones, familiar
  comfort items for sheltering situations

MEDICATION-DEPENDENT:
- Keep a current medication list in document kit and go-bag
- 7-day emergency supply (ask your pharmacist about emergency refills)
- Know your pharmacy's emergency/disaster policy
- Refrigerated medications: have a small cooler and ice packs ready
- Medical alert bracelet if applicable
- Register with local fire department if oxygen is in the home
```

## If This Fails

- If you can't afford go-bags, start with just the document kit and communication plan. Those cost almost nothing and cover the most likely scenarios.
- If your family won't participate in drills, make it a game for kids and frame it as "15 minutes now could matter later" for adults. Don't nag -- do it once, do it well.
- If you rent and can't modify the space (escape ladders, shut-off access), talk to your landlord. Most will cooperate on safety measures.
- If you have a family member with complex medical needs, call your local fire department's non-emergency line. Most will do a free home safety assessment.
- If the plan feels overwhelming, do one step per weekend. In 7 weeks you're fully prepared.

## Rules

- Treat fire escape as the highest priority -- it's the most common household emergency
- Never store go-bags somewhere that requires going deeper into the house to retrieve them
- Update all plans and supplies at least annually -- set a calendar reminder
- Plans that aren't practiced are plans that won't work. Drill at least twice a year.
- Don't skip the communication plan. Separated family members is the most stressful part of any emergency.
- Cash in the go-bag is not optional. Power outages kill all electronic payment systems.

## Tips

- The family emergency card (wallet-sized) is the single most useful thing on this list. Print it today.
- Take a video walkthrough of your entire home and possessions. Store it in the cloud. This is invaluable for insurance claims.
- "When you change the clocks" is the best reminder to check smoke detectors and do a fire drill.
- Rotate go-bag food into your regular pantry and replace it. Don't let it expire in the bag.
- Kids who have practiced a fire drill 2-3 times will execute it calmly during a real emergency. Kids who haven't will panic.
- Your phone's emergency SOS feature (hold side button on iPhone, power button on Android) can call 911 and share your location even without cell service through satellite in newer models.
- The $15-25 hand-crank NOAA radio is the single best emergency purchase. It works when everything else is dead.

## Agent State

```yaml
emergency_plan:
  fire_escape:
    plan_created: false
    meeting_point: null
    drill_completed: false
    smoke_detectors_checked: false
    last_drill_date: null
  communication:
    out_of_area_contact: null
    contact_cards_printed: false
    meeting_points_set: false
    kids_memorized_numbers: false
  document_kit:
    physical_assembled: false
    digital_backup_created: false
    cash_stored: false
    last_updated: null
  go_bags:
    bags_built: 0
    bags_needed: 0
    last_rotation_check: null
  evacuation:
    routes_identified: false
    routes_driven: false
    destinations_confirmed: false
    vehicle_kit_ready: false
  utility_shutoffs:
    gas_located: false
    water_located: false
    electric_located: false
    household_trained: false
  special_needs:
    applicable: false
    plans_created: false
    medications_stocked: false
  overall_status: null
```

## Automation Triggers

```yaml
triggers:
  - name: fire_drill_reminder
    condition: "fire_escape.plan_created IS true"
    schedule: "every 6 months"
    action: "Time for your semi-annual fire drill. Practice at night with the lights off. Time it -- everyone should be out and at the meeting point in under 2 minutes. Also test your smoke detectors."

  - name: go_bag_rotation
    condition: "go_bags.bags_built > 0"
    schedule: "every 6 months"
    action: "Time to rotate your go-bag supplies. Check expiration dates on food, water, and medications. Replace batteries. Swap seasonal clothing. Verify cash is still there."

  - name: annual_plan_review
    condition: "overall_status IS NOT null"
    schedule: "annually"
    action: "Annual emergency plan review. Update contact numbers, verify evacuation routes are still passable, refresh document copies, check that all household members still know the plan. Confirm medication supplies are current."

  - name: seasonal_disaster_prep
    condition: "overall_status IS NOT null"
    schedule: "seasonal (region-dependent)"
    action: "Seasonal preparedness check. Review disaster risks for the upcoming season in your area and confirm your plan covers them. Check weather radio batteries. Verify go-bag has appropriate seasonal gear."
```
