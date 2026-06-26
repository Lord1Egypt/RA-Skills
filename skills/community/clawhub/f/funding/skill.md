---
name: fund
description: >
  Complete fundraising and investment intelligence system for startups, nonprofits, and
  individuals raising capital. Trigger whenever someone needs to raise money: venture capital,
  angel investment, crowdfunding, nonprofit fundraising, or personal fundraising campaigns.
  Also triggers on phrases like "I need to raise money", "how do I pitch investors",
  "write my fundraising page", "what do VCs look for", "help me close this round", or
  any scenario involving convincing others to commit capital to a cause or venture.
---

# Fund — Complete Fundraising Intelligence System

## What This Skill Does

Raising money is a sales process with specific buyers, specific criteria, and specific
language. The founder who understands what an investor is actually evaluating closes rounds
faster. The nonprofit that understands donor psychology raises more. The crowdfunding campaign
that understands what drives contributions reaches its goal while others stall.

The money is there. The question is always whether you can make the case that it belongs
with you.

---

## Core Principle

Investors and donors are not giving you money. They are making a bet on an outcome. Your
job is to make that bet feel like the most rational and exciting allocation of their capital
or generosity available to them right now. Everything in a successful fundraise is designed
to answer one question: why this, why you, why now.

---

## Workflow

### Step 1: Identify the Fundraising Type
```
FUNDRAISING_TYPES = {
  "venture_capital": {
    "what_they_want":  "10x+ return, large addressable market, scalable model, strong team",
    "check_size":      "$500K to $100M+ depending on stage",
    "decision_factors": ["market_size", "team", "traction", "defensibility", "timing"],
    "timeline":        "3-6 months from first meeting to close"
  },
  "angel_investment": {
    "what_they_want":  "Early bet on founder, interesting problem, some traction",
    "check_size":      "$10K to $250K per angel",
    "decision_factors": ["founder_conviction", "problem_clarity", "early_signal"],
    "timeline":        "Faster than VC — weeks to months"
  },
  "crowdfunding": {
    "reward_based":   "Pre-sell product or offer rewards — Kickstarter model",
    "equity_based":   "Sell small equity stakes to many investors",
    "donation_based": "Raise from believers with no financial return",
    "key_drivers":    ["compelling_story", "clear_reward", "social_proof", "urgency"]
  },
  "nonprofit": {
    "major_donors":   "High-net-worth individuals — relationship and impact driven",
    "foundations":    "Grant applications — mission alignment and outcomes focused",
    "individual":     "Mass fundraising — emotional connection and small ask",
    "corporate":      "Sponsorship and partnership — mutual benefit framing"
  }
}
```

### Step 2: Investor/Donor Psychology
```
INVESTOR_PSYCHOLOGY = {
  "VC_decision_framework": {
    "market":      "Is this market large enough that even a small share is a big company",
    "team":        "Does this team have an unfair advantage in this specific problem",
    "product":     "Is there evidence that people want this and will pay for it",
    "timing":      "Why is now the right moment for this to exist",
    "returns":     "Is there a realistic path to the return profile we need"
  },

  "angel_psychology": {
    "primary_driver": "Angels often invest in founders they believe in personally",
    "secondary":      "Interesting problem in a domain they understand",
    "tertiary":       "Financial return is real but often secondary to participation"
  },

  "donor_psychology": {
    "identity":    "Giving expresses who the donor is and wants to be",
    "impact":      "Donors want to feel their contribution made a specific difference",
    "community":   "Being part of something larger than themselves",
    "recognition": "Acknowledgment appropriate to the gift level",
    "trust":       "Confidence that the organization will use the gift well"
  }
}
```

### Step 3: Pitch Architecture
```
INVESTOR_PITCH_STRUCTURE = {
  "problem": {
    "goal":     "Establish that the problem is real, large, and currently poorly solved",
    "evidence": "Data on scale, stories that make it human, gap in current solutions",
    "length":   "1-2 slides or 2-3 minutes — do not linger"
  },

  "solution": {
    "goal":     "Show that your approach solves the problem in a way that others have not",
    "format":   "Demo if possible — showing beats telling every time",
    "key":      "Connect directly to the problem — do not make investors work to see the link"
  },

  "market": {
    "TAM_SAM_SOM": {
      "TAM": "Total Addressable Market — everyone who could theoretically buy",
      "SAM": "Serviceable Addressable Market — the portion you can realistically reach",
      "SOM": "Serviceable Obtainable Market — what you will capture in years 1-3"
    },
    "credibility": "Bottom-up calculations from unit economics beat top-down percentages",
    "mistake":     "'1% of a $10B market' is the least convincing slide in every pitch"
  },

  "traction": {
    "goal":     "Evidence that reality is confirming your hypothesis",
    "metrics":  ["Revenue or ARR and growth rate",
                 "User/customer count and retention",
                 "Key partnerships or pilots",
                 "Waitlist or pre-orders if pre-revenue"],
    "framing":  "Show the trajectory, not just the number"
  },

  "team": {
    "goal":     "Why you specifically are the right people to build this",
    "content":  ["Relevant experience — not resume, but why it matters for THIS company",
                 "Domain expertise or unfair advantage",
                 "Previous wins that demonstrate execution",
                 "What is missing and how you will fill it"],
    "mistake":  "Listing credentials without connecting them to why they matter here"
  },

  "business_model": {
    "content":  ["How you make money",
                 "Unit economics — CAC, LTV, payback period",
                 "Why this model is defensible"],
    "key":      "Show that the business works at scale, not just that it can get revenue"
  },

  "ask": {
    "specificity": "Exact amount being raised and what it will be used for",
    "milestones":  "What you will achieve with this capital that makes the next raise easier",
    "terms":       "Valuation, instrument type, and any existing commitments",
    "mistake":     "Vague asks signal unclear thinking about the business"
  }
}
```

### Step 4: Fundraising Materials
```
FUNDRAISING_MATERIALS = {
  "pitch_deck": {
    "length":   "10-15 slides. More signals inability to prioritize.",
    "sequence": ["Problem", "Solution", "Market", "Product", "Traction",
                 "Business Model", "Team", "Financials", "Ask"],
    "design":   "Clean, consistent, data-forward. Visuals support the story."
  },

  "executive_summary": {
    "purpose":  "One-page filter for investors before they request the deck",
    "content":  ["Problem and solution in 2 sentences",
                 "Market size",
                 "Traction headline number",
                 "Team in 2 sentences",
                 "Ask and use of funds"],
    "length":   "One page. If it does not fit in one page, it is not sharp enough."
  },

  "financial_model": {
    "required_tabs": ["P&L projection 3-5 years",
                      "Unit economics",
                      "Headcount plan",
                      "Cash flow and runway calculation",
                      "Key assumptions clearly labeled"],
    "credibility_rules": ["Bottom-up revenue build",
                           "Costs that reflect reality not wishful thinking",
                           "Sensitivity analysis on key assumptions"]
  },

  "data_room": {
    "contents": ["Incorporation documents",
                 "Cap table",
                 "Financial statements or management accounts",
                 "Key contracts",
                 "IP ownership documentation",
                 "Team agreements"]
  }
}
```

### Step 5: Closing the Round
```
CLOSING_FRAMEWORK = {
  "creating_momentum": {
    "principle":   "Investors follow other investors. Lead with your strongest commitment.",
    "tactics":     ["Get a lead investor first — others follow",
                    "Create a close date — open-ended rounds close slowly",
                    "Update all investors simultaneously — FOMO is real",
                    "Never lie about investor interest — it always surfaces"]
  },

  "handling_objections": {
    "market_too_small": "Reframe with bottom-up calculation showing realistic path to $100M+",
    "too_early":        "Acknowledge, pivot to what milestone would change their view",
    "team_gap":         "Acknowledge specifically, show plan to fill including named candidates",
    "valuation":        "Show comparable companies, defend with traction and growth rate"
  },

  "term_sheet_basics": {
    "key_terms":     ["Valuation — pre-money and post-money",
                      "Investment amount and instrument",
                      "Board composition",
                      "Liquidation preference",
                      "Anti-dilution protection",
                      "Pro-rata rights"],
    "principle":     "Optimize for the investor relationship, not just the terms",
    "legal_advice":  "Always have a startup-experienced lawyer review before signing"
  }
}
```

---

## Quality Check Before Delivering

- [ ] Fundraising type matched to appropriate investor or donor psychology
- [ ] Problem framed from investor or donor perspective not founder perspective
- [ ] Market sizing is bottom-up not top-down percentage
- [ ] Traction presented as trajectory not just current number
- [ ] Team section connects experience to this specific problem
- [ ] Ask is specific with use of funds and milestones
- [ ] Financial model assumptions are labeled and defensible
- [ ] Legal review recommended before any term sheet signed
