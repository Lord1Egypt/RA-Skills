---
name: emergency-financial-triage
description: >-
  Priority-based action plan for financial emergencies. Use when someone can't make rent, is about to be evicted, can't afford food, has utilities about to be shut off, or faces any immediate financial crisis.
metadata:
  category: money
  tagline: >-
    Immediate action plan when you can't make rent, lost your job, or face a financial emergency — what to pay first and who to call
  display_name: "Emergency Financial Triage"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install howtousehumans/emergency-financial-triage"
---

# Emergency Financial Triage

When you can't pay your bills, everything feels equally urgent. It's not. There is a specific order to handle financial emergencies that prevents the worst outcomes. This is the triage protocol — what to pay first, what can wait, and who to call. Programs and phone numbers are US-specific — adapt for your country.

## Sources & Verification

- SNAP program details and eligibility: USDA Food and Nutrition Service ([fns.usda.gov/snap](https://www.fns.usda.gov/snap/supplemental-nutrition-assistance-program))
- LIHEAP program: Office of Community Services, ACF ([acf.hhs.gov/ocs/programs/liheap](https://www.acf.hhs.gov/ocs/programs/liheap))
- Emergency Rental Assistance: US Treasury ([home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program](https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program))
- 211 helpline coverage: United Way Worldwide ([211.org](https://www.211.org/))
- NeedyMeds prescription assistance: ([needymeds.org](https://www.needymeds.org/))
- Payday loan APR data: Consumer Financial Protection Bureau, "Payday Loans and Deposit Advance Products," 2013

## When to Use

- User can't make rent this month
- About to lose utilities (power, water, heat)
- Can't afford food or basic necessities
- Behind on multiple bills and doesn't know where to start
- Facing eviction, repossession, or debt collection
- Just lost income and needs to stretch what they have

## Instructions

### SAFETY CHECK — Read This First

**STOP.** Before proceeding, the agent MUST ask:

> "Before we start, I need to ask: are you safe right now? Are you in a situation where someone is controlling your finances or threatening you?"

- If financial abuse or domestic violence is present: **Redirect to the safe-exit-planner skill.** Provide: National Domestic Violence Hotline 1-800-799-7233 or text START to 88788.
- If having thoughts of self-harm related to financial stress: **Provide 988 Suicide & Crisis Lifeline** (call or text 988) immediately.
- If safe: Proceed to Step 1.

**Agent action**: Ask this question explicitly. Financial crises and abuse overlap frequently.

### Step 1: Triage — pay in this order

Not all bills are equal. Here's the priority order based on consequences:

```
PAYMENT PRIORITY (most urgent first):

1. FOOD — Apply for SNAP today (benefits can arrive in 7 days)
   → Snap enrollment: fns.usda.gov/snap
   → Local food banks: feedingamerica.org/find-your-local-foodbank
   → WIC (for pregnant women/children): fns.usda.gov/wic

2. ESSENTIAL MEDICATION — Don't skip meds
   → NeedyMeds.org — discount drug programs
   → GoodRx.com — prescription price comparison
   → Patient assistance programs (from the drug manufacturer)
   → $4 generic lists at Walmart, Costco (no membership needed for pharmacy)

3. HOUSING — Rent or mortgage
   → Call your landlord BEFORE the due date: "I'm having a financial
     emergency. Can we discuss a payment plan?"
   → Apply for Emergency Rental Assistance: treasury.gov/rental-assistance
   → Call 211 for local housing assistance programs

4. UTILITIES — Power, water, heat
   → Call each provider and ask for a "hardship plan" or "payment arrangement"
   → LIHEAP (Low Income Home Energy Assistance): liheap.org
   → Most states prohibit utility shutoffs in extreme cold/heat

5. TRANSPORTATION — If needed for work
   → Car payment before insurance (can't drive without the car)
   → If facing repossession, call the lender about forbearance

6. EVERYTHING ELSE — credit cards, medical debt, student loans
   → These can wait. They damage your credit but don't take your home.
   → Federal student loans: apply for income-driven repayment or forbearance
   → Credit cards: call and ask for hardship program
   → Medical debt: does not go to collections for 180 days typically
```

### Step 2: Immediate cash sources

```
WHERE TO FIND MONEY THIS WEEK:

□ 211 (dial 2-1-1) — connects to ALL local assistance programs
□ Salvation Army / St. Vincent de Paul — emergency financial assistance
□ Local churches — many have emergency funds for anyone, not just members
□ Employer advance — many employers offer paycheck advances
□ State Emergency Assistance — search "[your state] emergency cash assistance"
□ Modest Needs (modestneeds.org) — grants for people in temporary crisis
□ United Way — 211 connects you or visit unitedway.org

DO NOT:
✗ Take out a payday loan (300-500% APR — will make things worse)
✗ Borrow against your 401k unless truly last resort
✗ Use title loans (you'll lose your car)
```

### Step 3: Call every creditor

The single most important thing: CALL BEFORE YOU'RE LATE. Every creditor has hardship programs they don't advertise.

```
CREDITOR CALL SCRIPT:

"Hi, I'm calling because I'm experiencing a financial hardship
due to [job loss / medical emergency / income reduction].
I want to stay current on my account. Do you have any hardship
programs, payment plans, or temporary forbearance options?"

FOR EACH CREDITOR, ASK:
→ Can payments be deferred?
→ Can late fees be waived?
→ Is there a hardship/forbearance program?
→ Can the due date be moved?
→ GET THE REPRESENTATIVE'S NAME AND CONFIRMATION NUMBER.
```

## If This Fails

If you cannot access the resources above or the situation worsens:

1. **211 not available in your area?** Try [findhelp.org](https://www.findhelp.org) — enter your zip code for local programs.
2. **SNAP application denied?** Appeal within 90 days. Most denials are due to missing documents, not ineligibility. Call 211 for application assistance.
3. **About to be evicted?** Contact legal aid immediately at [lawhelp.org](https://www.lawhelp.org). Many eviction defense services are free.
4. **Utilities already shut off?** Call your utility company and ask for reconnection on a hardship plan. Apply for emergency LIHEAP. Many states prohibit shutoffs during extreme weather.
5. **Cannot afford food today?** Find your nearest food bank: [feedingamerica.org/find-your-local-foodbank](https://www.feedingamerica.org/find-your-local-foodbank) or call 211.
6. **Feeling overwhelmed by financial stress?** Call or text 988. Financial crises are temporary and solvable. Trained counselors can help.

## Rules

- Lead with the triage order — people in crisis need clear priorities, not options
- Food and medication FIRST, always
- Never recommend payday loans, title loans, or high-interest debt
- If someone mentions being unsafe (domestic violence situation affecting finances), redirect to Safe Exit Planner skill

## Tips

- 211 is the most underused resource in America. It connects you to every local program that exists.
- Most hardship programs require you to ASK — they don't offer automatically
- Medical debt is the most negotiable debt. Hospitals would rather get 20% than send it to collections.
- Filing for bankruptcy is not failure — it's a legal protection designed for exactly this situation. Consult a free legal aid attorney.
