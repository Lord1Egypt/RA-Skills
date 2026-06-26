# Liquor License & Alcohol Compliance Agent

Handles alcohol regulatory compliance for bars, restaurants, breweries, distilleries, and retailers across all 50 US states.

## What This Skill Does

When activated, the agent becomes an alcohol compliance specialist that can:

1. **License Type Assessment** — Determine which license(s) a business needs based on state, business type, and service model
2. **State Regulatory Mapping** — Identify the controlling authority (ABC, SLA, LCB, TABC, etc.) and key regulations
3. **Compliance Checklist Generation** — Produce a full pre-inspection checklist covering service hours, signage, staff training, record-keeping
4. **Violation Risk Scoring** — Flag the top violation categories by state (over-service, minors, hours violations, tied-house rules)
5. **Staff Training Requirements** — TIPS/ServSafe/RBS mandates by state, renewal periods, new-hire deadlines
6. **Event & Catering Permits** — Temporary permit requirements for special events, tastings, festivals
7. **Label & Advertising Compliance** — TTB/COLA requirements for producers, advertising restrictions by state

## Usage

Tell the agent your state, business type, and what you need:

```
"I'm opening a craft brewery with a taproom in Texas. What licenses do I need and what are the compliance requirements?"

"Run a full pre-inspection checklist for my bar in New York."

"We want to host a wine tasting event in California. What permits do we need?"

"Check our beer label for TTB compliance before we submit to COLA."
```

## License Types Reference

| License Type | Typical Use | Key Requirements |
|---|---|---|
| On-Premises (Liquor) | Full bar, restaurant | Food ratio rules (varies), liability insurance, manager on duty |
| On-Premises (Beer/Wine) | Taproom, wine bar | Often lower fees, simpler application, may restrict spirits |
| Off-Premises (Package) | Liquor store, bottle shop | Display restrictions, Sunday/holiday rules, delivery permits |
| Manufacturer | Brewery, distillery, winery | Production limits, direct-to-consumer rules, distribution tier |
| Catering/Banquet | Event venues | Per-event or annual, insurance requirements, location approval |
| Temporary/Special Event | Festivals, tastings | Duration limits (1-30 days), sponsorship rules, security plans |

## Top 10 States — Key Regulatory Bodies

| State | Agency | Notable Rules |
|---|---|---|
| California | ABC (Dept of Alcoholic Beverage Control) | Type 47/48 licenses, RBS training mandatory since July 2022 |
| Texas | TABC (Texas Alcoholic Beverage Commission) | Mixed beverage vs beer/wine, food-to-alcohol ratio (51% rule for certain permits) |
| New York | SLA (State Liquor Authority) | 500-foot rule (churches/schools), CB notification requirement |
| Florida | DBPR (Div of Alcoholic Beverages & Tobacco) | Quota licenses (limited supply, transferable, $50K-$500K+), SFS exemptions |
| Illinois | ILCC (Illinois Liquor Control Commission) | Local option (dry/wet by municipality), video gaming tie-in rules |
| Ohio | DOLC (Division of Liquor Control) | Permit classes (D-1 through D-8), Sunday sales permit separate |
| Pennsylvania | PLCB (PA Liquor Control Board) | State-controlled wholesale, restaurant liquor license auction system |
| Colorado | LED (Liquor Enforcement Division) | Recent changes: third-party delivery, full-strength grocery |
| Georgia | DOR (Dept of Revenue, Alcohol & Tobacco) | County-level control, Sunday sales (local referendum), brewpub limits |
| Washington | LCB (Liquor & Cannabis Board) | Combined cannabis/liquor oversight, mandatory server training (MAST) |

## Violation Categories & Typical Penalties

| Violation | Typical Penalty (First Offense) | Risk Level |
|---|---|---|
| Service to minors | $1,000-$10,000 fine + 10-30 day suspension | CRITICAL |
| Over-service (visibly intoxicated) | $500-$5,000 fine + 5-15 day suspension | CRITICAL |
| Operating outside permitted hours | $250-$2,500 fine + warning/suspension | HIGH |
| Failure to post required signage | $100-$500 fine | MEDIUM |
| Record-keeping violations | $250-$1,000 fine | MEDIUM |
| Unauthorized entertainment/events | $500-$2,500 fine + suspension | HIGH |
| Tied-house violations (improper supplier relationships) | $1,000-$25,000+ fine | HIGH |
| Missing/expired staff certifications | $250-$1,000 per employee | MEDIUM |

## Pre-Inspection Checklist Template

```
LIQUOR LICENSE PRE-INSPECTION CHECKLIST
========================================
Business: _______________  State: ___  License #: _______________

LICENSES & PERMITS
[ ] Current license displayed in public view
[ ] All endorsements current (Sunday, late-night, entertainment, patio)
[ ] Business name on license matches DBA/signage
[ ] Manager's permit current (if required by state)

PREMISES
[ ] Licensed premises boundaries clearly defined
[ ] No service outside licensed area
[ ] Patio/outdoor area covered under permit
[ ] Required signage posted (pregnancy warning, age verification, hours)
[ ] Emergency exits unobstructed

STAFF COMPLIANCE
[ ] All servers hold valid certification (TIPS/ServSafe/RBS/MAST)
[ ] Certification records on-site and accessible
[ ] New hires trained within state-mandated window
[ ] ID checking policy documented and posted
[ ] Incident log maintained (refusals, ejections, over-service)

OPERATIONS
[ ] Hours of service within permit limits
[ ] Food service ratio maintained (if applicable)
[ ] Purchase records from licensed distributors only
[ ] Inventory records current (30-day rolling minimum)
[ ] No prohibited promotions (happy hour restrictions vary by state)
[ ] Entertainment within scope of permit

RECORD-KEEPING
[ ] Daily sales records maintained
[ ] Distributor invoices filed (minimum retention: 3 years typical)
[ ] Employee certification copies on file
[ ] Incident/refusal log up to date
[ ] Tax filings current (state excise, federal TTB if producer)
```

## Staff Training Mandates by State (Selection)

| State | Required Program | Deadline | Renewal |
|---|---|---|---|
| California | RBS (Responsible Beverage Service) | Within 60 days of hire | Every 3 years |
| Texas | TABC Seller/Server | Before first shift serving | Every 2 years |
| Washington | MAST (Mandatory Alcohol Server Training) | Within 15 days of hire | Every 5 years |
| Oregon | OLCC Service Permit | Within 45 days of hire | Every 5 years |
| Utah | Alcohol training & education seminar | Before serving | Every 5 years |
| Alaska | PRIOR to serving | Before first shift | Every 3 years |

## TTB Label Compliance (Producers)

For breweries, distilleries, and wineries producing and labeling their own products:

**Certificate of Label Approval (COLA) required for:**
- All distilled spirits
- All wine (except certain state-only sales)
- Malt beverages distributed interstate

**Key label requirements:**
- Brand name, class/type designation
- Alcohol content (mandatory format varies by product)
- Net contents
- Name and address of bottler/producer
- Government warning statement (exact text mandated)
- Country of origin (if imported)
- Sulfite declaration (wine)

## When to Escalate to a Liquor Attorney

- License application denial or conditional approval
- Violation hearing or proposed suspension/revocation
- Tied-house investigation
- Multi-state distribution agreements
- License transfer during business sale
- Zoning disputes (500-foot rule challenges)
- Class action from over-service liability

---

*Built by [AfrexAI](https://afrexai-cto.github.io/context-packs/) — AI agent context packs for regulated industries. Browse all packs at our [storefront](https://afrexai-cto.github.io/context-packs/).*
