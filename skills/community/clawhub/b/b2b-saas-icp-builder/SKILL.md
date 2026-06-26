---
name: icp-builder
description: >
  B2B SaaS ICP (Ideal Customer Profile) and buyer persona builder.
  Use this skill whenever the user wants to define, refine, or document their ideal customer profile,
  buyer personas, target segments, pain points, or jobs-to-be-done (JTBD).
  Trigger for phrases like "who is my ICP", "define my target customer", "build a persona",
  "who should we target", "what are our buyers pain points", "jobs to be done", "customer segments",
  "who are we selling to", "ideal customer", "target audience for B2B", "firmographics",
  or any request to understand, document, or sharpen who the company's best customers are.
  Also trigger when the user is starting go-to-market planning, repositioning, or says they're not
  sure who to focus on. This skill produces a complete, structured ICP document ready for use in
  sales, marketing, and product decisions.
---

# ICP Builder — B2B SaaS

**Purpose:** Build a clear, actionable Ideal Customer Profile that aligns sales, marketing, and product around the same target buyer.

---

## Step 1: Gather Context

If any of the following are missing, ask before proceeding:

- **Product:** What does your product do? (one sentence)
- **Current customers:** Who are your best 3-5 customers today? What do they have in common?
- **Problem solved:** What specific problem do you eliminate or reduce?
- **Stage:** Seed / Series A / Growth / Scale?
- **Data available?** CRM data, churned accounts, win/loss notes?

---

## Step 2: Firmographic Profile

```
FIRMOGRAPHIC PROFILE
├── Industry verticals (primary + secondary)
├── Company size — employees (range)
├── Company size — revenue (range)
├── Geography / markets
├── Business model (B2B SaaS / marketplace / services / enterprise)
├── Growth stage (startup / scale-up / enterprise)
├── Funding stage (if relevant)
└── Exclusion criteria (who NOT to target)
```

**Tier system:**
- **Tier 1:** Perfect fit — highest likelihood of close + expand
- **Tier 2:** Good fit — worth pursuing with some customization
- **Tier 3:** Possible fit — opportunistic only

---

## Step 3: Technographic Profile

```
TECHNOGRAPHIC SIGNALS
├── Tools they already use (integrations, adjacent products)
├── Tech stack indicators (cloud provider, CRM, data tools)
├── Digital maturity level (early adopter / pragmatist / laggard)
├── Buying signal: intent data categories to watch
└── Disqualifying tech (signs they won't need you)
```

---

## Step 4: Buyer Personas

For each key buying role:

```
PERSONA: [Title / Role]
├── Decision role: Economic Buyer / Champion / User / Blocker
├── Seniority: C-level / VP / Director / Manager / IC
├── Core responsibilities
├── What success looks like for them
├── Top 3 pain points (specific, in their words)
├── What they fear / what would get them fired
├── How they discover new tools
└── Objections they typically raise
```

Build at least 2-3 personas: the **Champion**, the **Economic Buyer**, and a **User**.

---

## Step 5: Pain Points & Buying Triggers

```
PAIN POINTS
├── [Pain 1] — in customer language
│   ├── Business impact (cost, time, risk)
│   └── Current workaround
├── [Pain 2]
└── [Pain 3]

BUYING TRIGGERS
├── Internal (new hire, team growing, failed project, audit)
├── External (regulation change, competitive pressure, funding)
└── Technology (old tool deprecated, integration needed)
```

---

## Step 6: Jobs-to-Be-Done

```
JTBD: [Persona]
├── Functional: "When [situation], I want to [action] so I can [outcome]"
├── Emotional: How they want to feel / avoid feeling
└── Social: How they want to be seen by peers/management
```

---

## Output Format

```
# ICP Document — [Company Name]
Last updated: [date]

## Executive Summary (2-3 sentences)
## Firmographic Profile
## Technographic Signals
## Buyer Personas (one section per persona)
## Pain Points & Buying Triggers
## Jobs-to-Be-Done (one per key persona)
## Who NOT to Target (exclusion criteria)
## How to Use This Document
  - Sales: qualify accounts against Tier criteria
  - Marketing: use pain points + JTBD for copy, content, emails
  - Product: use JTBD for roadmap prioritization
```
