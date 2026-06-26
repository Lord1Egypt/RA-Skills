# Veterinary Clinic Operations Agent

## Description
Operational assistant for veterinary clinics — appointment scheduling optimization, patient follow-up workflows, inventory management for medications/supplies, and client communication templates. Reduces no-shows, prevents stockouts, and improves client retention.

## Use When
- Optimizing appointment scheduling and reducing no-shows
- Managing medication and supply inventory with reorder alerts
- Creating client follow-up sequences (post-surgery, vaccination reminders, wellness checks)
- Generating end-of-day reports and revenue tracking
- Drafting client communications (appointment reminders, treatment plans, aftercare instructions)

## Not For
- Veterinary medical diagnosis or treatment decisions
- Controlled substance tracking (use DEA-compliant systems)
- Insurance claims processing

## Inputs Required
- `clinic_name` — Name of the veterinary practice
- `services` — List of services offered (wellness, surgery, dental, emergency, boarding, grooming)
- `staff_count` — Number of veterinarians and vet techs
- `daily_appointment_slots` — Typical daily capacity
- `current_no_show_rate` — Estimated percentage (if known)

## Workflow

### 1. Appointment Optimization
Analyze scheduling patterns and generate recommendations:

```
APPOINTMENT OPTIMIZATION — {{clinic_name}}

Current Setup:
- Daily slots: {{daily_appointment_slots}}
- Staff: {{staff_count}} vets, {{tech_count}} techs
- No-show rate: {{current_no_show_rate}}%

Recommendations:
□ Implement 24h + 2h reminder sequence (SMS/email)
□ Add 10-15% overbooking buffer for high no-show slots
□ Block surgery mornings (Mon/Wed/Fri AM) — highest-value procedures
□ Reserve 2 daily slots for urgent/same-day cases
□ Schedule wellness exams in 20-min blocks, surgeries in 60-90 min
□ Stagger check-in times by 10 min to reduce lobby congestion

Expected Impact:
- No-show reduction: 30-50% with dual reminders
- Revenue recovery: ${{estimated_recovery}}/month from filled gaps
```

### 2. Client Follow-Up Sequences

Generate automated follow-up templates:

**Post-Surgery (Day 1, 3, 7, 14):**
```
Day 1: "Hi {{owner_name}}, {{pet_name}} had their {{procedure}} today.
Watch for: [specific signs]. Normal: [expected behavior].
Call us at {{clinic_phone}} if concerned. — {{clinic_name}}"

Day 3: "Checking in on {{pet_name}}! How is recovery going?
Reminder: keep the e-collar on and limit activity.
Reply YES if all good, or call us with concerns."

Day 7: "{{pet_name}}'s one-week check-in. Suture removal is
scheduled for {{date}}. Any questions before then?"
```

**Vaccination Reminders (30 days, 7 days, day-of):**
```
30 days: "{{pet_name}} is due for {{vaccine}} on {{date}}.
Book online: {{booking_link}} or call {{clinic_phone}}."

7 days: "Reminder: {{pet_name}}'s {{vaccine}} appointment is
{{date}} at {{time}}. Reply C to confirm or R to reschedule."
```

**Wellness/Annual Check (11 months post-visit):**
```
"It's almost time for {{pet_name}}'s annual wellness exam!
Early detection saves lives (and money). Book before {{date}}
for {{discount_offer}}. {{booking_link}}"
```

### 3. Inventory Management

Track medication and supply levels with reorder alerts:

```
INVENTORY CHECK — {{date}}

⚠️ REORDER NOW (below minimum):
- Rimadyl 75mg: 12 tablets left (min: 50) → Order 200
- 3-0 Suture (Monocryl): 3 packs left (min: 10) → Order 20
- Rabies vaccine (1yr): 8 doses left (min: 25) → Order 50

📋 WATCH LIST (2-week supply):
- Cerenia 16mg: 28 tablets (usage: ~2/day)
- Clavamox 250mg: 45 tablets (usage: ~3/day)

✅ WELL STOCKED:
- Frontline Plus (all sizes): 60+ units
- Microchips: 40 units

Monthly Supply Cost Trend:
- This month: ${{current_cost}}
- Last month: ${{last_cost}}
- 3-month avg: ${{avg_cost}}
```

### 4. End-of-Day Report

```
DAILY REPORT — {{clinic_name}} — {{date}}

Appointments: {{seen}}/{{scheduled}} ({{no_shows}} no-shows)
Revenue: ${{daily_revenue}} (avg ${{per_visit}}/visit)
New Clients: {{new_clients}}
Surgeries: {{surgery_count}} ({{surgery_revenue}})

Top Services Today:
1. {{service_1}} — {{count_1}} (${{rev_1}})
2. {{service_2}} — {{count_2}} (${{rev_2}})
3. {{service_3}} — {{count_3}} (${{rev_3}})

Follow-Ups Scheduled: {{followup_count}}
Reminders Sent: {{reminder_count}}
Callbacks Needed: {{callback_list}}

Notes: {{daily_notes}}
```

### 5. Client Retention Metrics

```
CLIENT HEALTH — {{month}} {{year}}

Active Clients (visit in 12mo): {{active}}
At-Risk (no visit 6-12mo): {{at_risk}} → send re-engagement
Lapsed (12mo+): {{lapsed}}

Retention Rate: {{retention}}%
Avg Client Lifetime Value: ${{ltv}}
Avg Visits/Year: {{visits_per_year}}

Top Re-Engagement Actions:
□ Send "We miss {{pet_name}}" to {{at_risk_count}} clients
□ Offer dental month discount (Feb) to overdue dental clients
□ Birthday cards for pets with birthdays this month: {{birthday_count}}
```

## Tips
- Pair SMS reminders with email for highest confirmation rates
- Track no-show patterns by day/time — some slots consistently underperform
- Dental cleanings are highest-margin — promote February dental month
- New puppy/kitten packages lock in 12-18 months of visits
- Google Reviews after positive visits — ask at checkout, not by email

---

**Want this running 24/7 without lifting a finger?** AfrexAI manages AI agents for your business — setup, monitoring, and optimization included. Book a free consultation: https://afrexai.com/book
Learn more: https://afrexai.com
