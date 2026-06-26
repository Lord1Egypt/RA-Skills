# HVAC Operations Manager

> AI-powered operational assistant for HVAC contractors — dispatch, maintenance scheduling, seasonal prep, and customer follow-up.

## When to Use
- Scheduling service calls and dispatching technicians
- Managing preventive maintenance programs
- Seasonal transition planning (heating ↔ cooling)
- Customer follow-up and retention campaigns
- Warranty tracking and parts inventory alerts
- Generating service estimates and proposals

## Inputs Required

Before running, gather:
1. **Service area** — zip codes or city/radius you cover
2. **Team size** — number of technicians and their certifications (EPA 608, NATE, etc.)
3. **Software stack** — ServiceTitan, Housecall Pro, Jobber, or manual scheduling?
4. **Season** — current season affects priority workflows
5. **Business goals** — growth target, average ticket size, close rate

## Workflow 1: Daily Dispatch Optimization

### Morning Routine (run at 6:30 AM)
1. Pull today's scheduled jobs from your dispatch board
2. Check technician availability and certifications vs job requirements
3. Route jobs geographically to minimize drive time
4. Flag any jobs missing equipment or parts
5. Send tech briefings: job history, customer notes, upsell opportunities

### Output Format
```
DISPATCH BOARD — [DATE]
━━━━━━━━━━━━━━━━━━━━━
TECH: [Name] | Cert: [EPA/NATE] | Vehicle: [#]
  8:00  → [Address] — AC tune-up (residential) | Est: 1.5hr
  10:30 → [Address] — Furnace no-heat call | Est: 2hr | ⚠️ Parts needed: ignitor
  1:30  → [Address] — Duct cleaning | Est: 3hr
  DRIVE TIME: ~45 min total

UNASSIGNED: [List any overflow jobs]
PARTS ALERT: [Items to pick up before routes]
```

## Workflow 2: Preventive Maintenance Program

### Setup
1. Export customer list with equipment install dates and last service
2. Classify by equipment type: furnace, AC, heat pump, mini-split, commercial RTU
3. Set maintenance intervals:
   - Residential AC: Spring tune-up (Mar-Apr)
   - Residential furnace: Fall tune-up (Sep-Oct)
   - Commercial: Quarterly inspections
   - Heat pumps: Twice yearly

### Automated Outreach Sequence
- **60 days before due:** Email reminder with online booking link
- **30 days before due:** SMS reminder + limited-time discount offer
- **14 days before due:** Phone call from CSR (flag in CRM)
- **Day of service:** Appointment confirmation + tech ETA
- **3 days after:** Review request + referral program mention

### Tracking Metrics
- Maintenance agreement renewal rate (target: 80%+)
- Average maintenance ticket value
- Upsell conversion from maintenance visits
- Customer lifetime value by agreement tier

## Workflow 3: Seasonal Transition Playbook

### Spring (Cooling Season Prep) — February through April
1. **Inventory audit:** Refrigerant stock (R-410A, R-22 phase-out status), filters, capacitors, contactors
2. **Marketing push:** "AC tune-up special" campaigns — email blast + door hangers in service area
3. **Training:** New refrigerant handling, updated EPA regulations, heat pump installs
4. **Hiring:** Assess if summer demand requires seasonal techs
5. **Pricing review:** Adjust rates for peak season, update flat-rate book

### Fall (Heating Season Prep) — August through October
1. **Inventory audit:** Heat exchangers, ignitors, flame sensors, thermocouples
2. **Marketing push:** "Furnace safety check" campaigns — target homes 10+ years old
3. **Carbon monoxide awareness:** Partner with local fire dept for co-branded safety content
4. **Emergency protocol:** Update after-hours dispatch rotation and response SLAs

## Workflow 4: Service Estimate Generator

### For Replacement Proposals
1. Collect: square footage, insulation quality, window count, duct condition, current system age/model
2. Run Manual J load calculation (or use ACCA-approved software)
3. Generate good/better/best options:
   - **Good:** Standard efficiency (14 SEER2) — lowest upfront
   - **Better:** High efficiency (16-17 SEER2) — utility rebate eligible
   - **Best:** Variable speed / heat pump (18+ SEER2) — max comfort + savings
4. Include: equipment cost, labor, permits, warranty terms, financing options
5. Show 10-year cost of ownership comparison (purchase price + estimated energy costs)

### Estimate Template
```
HVAC REPLACEMENT PROPOSAL — [Customer Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Home: [sqft] | Current System: [model, age] | Condition: [rating]

OPTION A — Standard Comfort
  Equipment: [Brand Model] | 14 SEER2 | 80% AFUE
  Price: $X,XXX installed | Warranty: 10yr parts
  Est. Annual Energy: $X,XXX

OPTION B — Enhanced Efficiency ⭐ RECOMMENDED
  Equipment: [Brand Model] | 16 SEER2 | 96% AFUE
  Price: $X,XXX installed | Warranty: 10yr parts + 2yr labor
  Est. Annual Energy: $X,XXX | Rebate: $XXX
  10-Year Savings vs Option A: $X,XXX

OPTION C — Premium Performance
  Equipment: [Brand Model] | 18+ SEER2 | Variable Speed
  Price: $X,XXX installed | Warranty: 12yr parts + 5yr labor
  Est. Annual Energy: $X,XXX | Rebate: $X,XXX
  10-Year Savings vs Option A: $X,XXX

FINANCING: [Terms available]
```

## Workflow 5: Customer Retention & Review Management

### Post-Service Follow-Up
1. **Same day:** Automated "How did we do?" text with 1-5 star rating
2. **If 4-5 stars:** Request Google/Yelp review with direct link
3. **If 1-3 stars:** Alert office manager for immediate callback
4. **7 days later:** Maintenance agreement offer if not already enrolled
5. **90 days later:** "How's your system running?" check-in

### Referral Program
- Offer $50 credit per referred customer who books service
- Track referral sources in CRM
- Quarterly drawing for top referrers (free tune-up or smart thermostat)

## Key Metrics Dashboard

Track weekly:
- **Revenue:** Total, average ticket, revenue per tech
- **Operations:** Jobs completed, callback rate, on-time arrival %
- **Sales:** Close rate on replacements, maintenance agreement signups
- **Customer:** NPS score, Google review average, referral count
- **Inventory:** Parts turnover, stockout incidents, van inventory accuracy

## Integration Notes

Works with common HVAC business platforms:
- **ServiceTitan** — dispatch, invoicing, reporting
- **Housecall Pro** — scheduling, estimates, payments
- **Jobber** — quoting, CRM, route optimization
- **QuickBooks** — accounting sync
- **Podium/Birdeye** — review management

---

**Want this running 24/7 without lifting a finger?** AfrexAI manages AI agents for your business — setup, monitoring, and optimization included. Book a free consultation: https://afrexai.com/book
Learn more: https://afrexai.com
