# Prompt: Retargeting Ad Copy Generator

## Instructions for Claude

Generate retargeting ad copy for three stages of the buyer journey: Abandoned Cart, Past Visitor Win-Back, and Upsell/Cross-Sell. Each stage gets 3 angle variants based on proven psychological triggers (Cialdini: urgency/scarcity, social proof, and objection removal).

---

## Input Variables

```
PRODUCT_NAME: [Name of product or service]
PRODUCT_CATEGORY: [e.g., SaaS tool / e-commerce product / online course / service]
CORE_BENEFIT: [The #1 outcome]
PRICE: [Price point or price range]
OBJECTION_1: [Most common reason they didn't buy — e.g., "too expensive", "not sure it works for me"]
OBJECTION_2: [Second most common objection]
GUARANTEE: [Money-back period, free trial length, or "no guarantee" if none]
SOCIAL_PROOF: [Reviews, customer count, case study result]
UPSELL_PRODUCT: [Product to upsell or cross-sell after purchase, or "N/A"]
UPSELL_BENEFIT: [Why the upsell is the logical next step]
BRAND_VOICE: [Conversational / Professional / Playful / Empathetic / Urgent]
```

---

## Prompt

```
You are a conversion rate optimization specialist and direct response copywriter.

Product: {{PRODUCT_NAME}} ({{PRODUCT_CATEGORY}})
Benefit: {{CORE_BENEFIT}}
Price: {{PRICE}}
Top Objections: {{OBJECTION_1}}, {{OBJECTION_2}}
Guarantee: {{GUARANTEE}}
Social Proof: {{SOCIAL_PROOF}}
Brand Voice: {{BRAND_VOICE}}

Generate retargeting copy for 3 buyer journey stages. Each stage gets 3 angle variants.

---

**STAGE 1: ABANDONED CART / STARTED BUT DIDN'T FINISH**
(Audience: visited pricing page or added to cart but didn't purchase — last 1–7 days)

Angle A — Urgency/Scarcity:
[Create legitimate urgency — limited offer, price increase, seats filling]
Hook (125 chars): 
Body (100–150 words):
Headline (40 chars):
CTA: 

Angle B — Social Proof:
[Show them others made the same decision and are getting results]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

Angle C — Objection Removal:
[Address {{OBJECTION_1}} head-on — turn the hesitation into reassurance]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

---

**STAGE 2: PAST VISITOR WIN-BACK**
(Audience: visited the site 8–30 days ago but never converted — they've gone cold)

Angle A — New Information/Urgency:
[Give them a reason to re-evaluate — new feature, new offer, or time-sensitive hook]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

Angle B — Pain Point Amplification:
[Remind them the problem they came looking to solve is still unsolved]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

Angle C — Guarantee/Risk Reversal:
[Make the decision feel zero-risk — address {{OBJECTION_2}}]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

---

**STAGE 3: POST-PURCHASE UPSELL/CROSS-SELL**
(Audience: existing customers — bought within last 30–90 days)
Upsell Product: {{UPSELL_PRODUCT}}
Upsell Benefit: {{UPSELL_BENEFIT}}

Angle A — Logical Next Step:
[Frame the upsell as the obvious progression — they've already proven they want results]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

Angle B — Exclusive/Loyalty:
[Make them feel valued as a customer — special offer, insider access]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

Angle C — FOMO/Community:
[Show that other customers at their stage are already using the upsell]
Hook (125 chars):
Body (100–150 words):
Headline (40 chars):
CTA:

---

**RETARGETING CAMPAIGN STRUCTURE RECOMMENDATION**
- Recommended audience window per stage (days)
- Frequency cap recommendation (impressions/day per person)
- Budget split across the 3 stages (% of total retargeting budget)
- Which variant to test first and why
```

---

## Expected Output

- 9 complete ad units (3 stages × 3 angles)
- Campaign structure recommendation

---

## Example Run

**Inputs:**
```
PRODUCT_NAME: TaskFlow Pro
PRODUCT_CATEGORY: SaaS tool
CORE_BENEFIT: Cut project delays by 40%
PRICE: $49/month
OBJECTION_1: Too expensive for my team size
OBJECTION_2: We already use [competitor] — switching is a headache
GUARANTEE: 30-day money-back guarantee
SOCIAL_PROOF: 10,000+ teams, 4.8★ on G2 (847 reviews)
UPSELL_PRODUCT: TaskFlow Enterprise (SSO, admin controls, priority support)
UPSELL_BENEFIT: Removes the bottleneck when you scale past 25 team members
BRAND_VOICE: Conversational
```

**Sample Stage 1, Angle A (Urgency):**
Hook: "You were this close. Our 30% launch discount expires Friday — don't leave it on the table."

**Sample Stage 2, Angle B (Pain Point):**
Hook: "Still missing deadlines? You visited TaskFlow Pro last month. The problem didn't fix itself."

**Sample Stage 3, Angle A (Logical Next Step):**
Hook: "You cut delays by 40%. Now scale without the chaos — TaskFlow Enterprise is the next move."
