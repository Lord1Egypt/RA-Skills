---
name: climbing-gym-ops
description: Operational assistant for independent climbing gyms and bouldering studios — membership management, churn reduction, route-setting coordination, youth program scheduling, safety compliance, and revenue optimization. Built for single-location gyms with 200-1,000 members.
---

# Climbing Gym Operations

Autonomous operations assistant for independent climbing gyms and bouldering studios.

## What It Does

### Membership & Churn Management
- Track active members, plan types, billing dates, and visit frequency
- Flag at-risk members: no visit in 14+ days, declining frequency, payment failures
- Generate re-engagement outreach (email/SMS templates) for at-risk members at 14/21/30 day marks
- Track churn rate monthly (industry avg: 3-5%/mo) — alert when trending above baseline
- Intro class → membership conversion tracking: who visited trial, who converted, follow-up sequence
- Monthly membership growth report: new joins, cancellations, net change, revenue impact

### Route Setting & Facility
- Route-setting rotation calendar: track wall sections, last set date, grade distribution
- Alert when a section hasn't been reset in 6+ weeks (staleness = member boredom = churn)
- Grade distribution audit: ensure balanced spread across V0-V10 / 5.6-5.13 for member mix
- Track setter hours and cost per reset
- Facility maintenance schedule: holds washing, mat cleaning, HVAC filters, wall inspections
- Equipment inventory: rental shoes, harnesses, belay devices — track condition and replacement cycle

### Youth Programs & Events
- Youth team practice schedule management with coach assignments
- Birthday party booking pipeline: inquiry → deposit → confirmation → day-of checklist → follow-up
- Summer camp session planning: capacity, waitlist, staffing ratios (1:8 recommended)
- Competition calendar: local/regional comp dates, registration deadlines, team logistics
- Corporate event pipeline: inquiry → quote → booking → setup → invoice → feedback

### Safety & Compliance
- Waiver tracking: flag expired/missing waivers for active members
- Belay certification management: who's certified, expiration dates, re-certification reminders
- Incident/accident log: track falls, injuries, near-misses with severity rating
- Annual safety audit checklist: auto-belay inspection, anchor testing, hold torque checks, mat condition
- Insurance renewal tracking with premium history
- Staff certification tracking: first aid, CPR, climbing instructor certs

### Financial Operations
- Monthly P&L by revenue stream: memberships (target 70%), day passes (15%), youth (15%), retail, events
- Day pass vs membership conversion rate tracking
- Revenue per square foot benchmarking (industry: $24-38/sqft)
- Payroll as % of revenue monitoring (target: 30-40%)
- Gear rental ROI tracking (80%+ margin expected)
- Seasonal revenue patterns: flag slow months, suggest promotions

### Marketing & Community
- Social media content calendar tied to route-setting (new routes = photo ops = posts)
- Member milestone celebrations: 100th visit, 1-year anniversary, grade breakthrough
- NPS survey automation: quarterly pulse, track score over time
- Review monitoring: Google, Yelp alerts when new reviews post
- Referral program tracking: who referred whom, reward fulfillment
- Local climbing community event calendar (outdoor meetups, film screenings, clinics)

## Reference Files

### references/safety-compliance-checklist.md
Complete safety audit checklist covering auto-belay systems, anchor points, hold integrity, mat condition, belay device inspection, emergency procedures, and staff certification requirements.

### references/revenue-optimization-playbook.md
Revenue diversification strategies for independent climbing gyms with benchmarks from the $682M US industry. Covers membership tier design, day pass conversion funnels, youth program scaling, corporate events, retail optimization, and seasonal promotion templates.

## Example Interactions

**User:** "Our churn spiked to 7% this month. What's going on?"
**Agent:** Pulls visit frequency data for cancelled members. Identifies pattern (e.g., 80% hadn't visited in 21+ days before cancelling). Cross-references with route-setting calendar — finds the bouldering area hasn't been reset in 8 weeks. Recommends immediate reset + re-engagement campaign to at-risk members with "new routes just dropped" messaging.

**User:** "We have a corporate event inquiry for 30 people next Friday."
**Agent:** Generates quote ($1,200-1,500 for 30 pax based on $40-50/person), creates event checklist (staff needed: 3 belayers + 1 coordinator, harness/shoe inventory check, waiver pre-send, catering options), drafts confirmation email with liability waiver link, and schedules follow-up for day-after feedback + rebooking.

**User:** "How are we doing on youth programs this quarter?"
**Agent:** Pulls enrollment vs capacity for each program (team, camps, birthday parties). Shows revenue contribution, compares to 15% target. Flags if summer camp registration is behind last year's pace. Suggests early-bird pricing deadline to drive urgency.

## Who This Is For
- Independent climbing gym owners (single location)
- Gym managers responsible for day-to-day operations
- Small climbing gym chains (2-5 locations)
- Bouldering studio operators

## Industry Context
- US climbing gym market: $682M (2025), 611 commercial facilities, 10.5% CAGR
- Average member: age 28-35, $100K+ household income, 72% college-educated
- Olympic effect driving 25% of new climbers since 2020
- Insurance costs rising ~20% over 3 years — safety compliance is increasingly critical
