---
name: ai-sales-closing-offer-generator
description: >
  Generates closing messages, objection handling responses, pricing strategies,
  offer designs, and upsell scripts to help salespeople convert prospects into
  paying customers. Trigger this skill whenever the user wants to close a deal,
  handle a customer objection, design a pricing offer, write a follow-up to a
  stalled prospect, create an upsell pitch, or asks anything like "how do I
  close this deal", "the customer said it's too expensive", "help me write an
  offer", "they're not responding", "how do I upsell", or "write me a closing
  message" — even when phrased casually.
license: MIT-0
user-invocable: true
disable-model-invocation: false
compatibility:
  - claude-sonnet-4-20250514
  - claude-opus-4-20250514
  - claude-haiku-4-5-20251001
argument-hint: >
  Provide: product or service name, customer type (e.g. SMB founder, enterprise
  procurement, individual consumer), the customer's last message or objection
  (paste it directly), your price or pricing structure, and your goal
  (e.g. close today, book a call, get a reply, upsell to annual plan).
  Optionally add deal context such as how long the conversation has been going,
  what objections have already been raised, and what the customer cares most about.
metadata:
  category: Sales & Marketing
  subcategory: Sales Closing
  version: 1.0.0
  author: ClawHub Skill Publisher
  language: en
  tags:
    - sales-closing
    - objection-handling
    - offer-design
    - pricing
    - upsell
    - B2B
    - conversion
    - persuasion
    - GTM
    - revenue
---

# AI Sales Closing & Offer Generator

Turn stalled deals into signed contracts. Generate closing messages,
objection responses, irresistible offer designs, and upsell scripts —
all written to sound like a seasoned human salesperson, not a chatbot.

---

## What This Skill Does

Given a product, customer type, customer message, price, and goal,
this skill generates:

- **Closing Message** — a short, direct message to send right now that
  moves the deal forward
- **Objection Handling** — word-for-word responses to the customer's
  specific objection, with three tone variants
- **Pricing Strategy** — how to present, frame, and defend your price
  to maximize perceived value
- **Offer Design** — how to structure your offer so it feels irresistible
  (anchoring, bonuses, guarantees, urgency)
- **Upsell / Cross-sell Script** — how to upgrade existing customers or
  add adjacent products without feeling pushy

---

## Skill Files

```
ai-sales-closing-offer-generator/
├── SKILL.md       ← You are here
├── manifest.json  ← Deployment metadata
├── prompt.txt     ← Core generation logic
├── config.json    ← Input field definitions
└── README.md      ← End-user documentation
```

---

## When to Trigger This Skill

Trigger immediately when the user says anything like:

- "help me close this deal" / "write a closing message"
- "the customer said it's too expensive" / "they're not sure"
- "they ghosted me" / "no response for a week"
- "how do I handle this objection" / "they want to think about it"
- "design me an offer" / "how should I price this"
- "I want to upsell my customer" / "how do I sell the upgrade"
- "they said they need to talk to their boss" / "not the right time"
- "write a proposal" / "help me negotiate"

---

## Required Inputs

Collect all required fields in a **single ask** — do not ask one at a time.

| Field | Required | Description |
|---|---|---|
| `product_service` | ✅ | What you are selling |
| `customer_type` | ✅ | Who the buyer is |
| `customer_message` | ✅ | Their last message or objection (paste it) |
| `price` | ✅ | Your price or pricing structure |
| `goal` | ✅ | What you want to happen next |
| `deal_context` | Optional | How long in the deal, prior objections |
| `customer_priority` | Optional | What the customer cares most about |
| `competitor` | Optional | Who they are comparing you to |
| `tone` | ✅ | Closing style (see presets) |

### Tone Presets

| Value | Description |
|---|---|
| `confident_direct` | Assumptive close. Bold. Built for decisive buyers. **(Default)** |
| `warm_consultative` | Empathetic. Trust-first. Built for relationship-driven sales. |
| `logical_roi` | Data and ROI-led. Built for analytical or procurement buyers. |
| `urgency_scarcity` | Creates a reason to act now. Built for fence-sitters. |

---

## Output Sections

```
💬 CLOSING MESSAGE      ← Send this to the customer right now
🛡️ OBJECTION HANDLING   ← 3 tone variants to handle their specific pushback
💰 PRICING STRATEGY     ← How to frame and defend your price
🎁 OFFER DESIGN         ← Structure the deal so it feels irresistible
📈 UPSELL / CROSS-SELL  ← Upgrade or expand the relationship post-close
```

---

## Example

**Input:**
```
Product: Annual SaaS subscription, AI writing tool, $1,200/year
Customer Type: Marketing manager at a 50-person company
Customer Message: "It looks interesting but $1,200 is a lot.
  We're using a free tool right now. Can you do anything on price?"
Price: $1,200/year ($100/month)
Goal: Close today or get a commitment this week
Tone: Warm & Consultative
```

**Sample Closing Message:**

> Hey [Name] — totally fair, and I appreciate you being upfront.
>
> Here's the honest math: if this saves your team 5 hours a month
> (most users save 8–10), that's 60 hours a year. At even $30/hour,
> that's $1,800 in time back — for a $1,200 investment.
>
> I can lock in this year's rate for you today and add a free
> onboarding call so your team actually uses it from day one.
>
> Want me to send over a quick start link?

**Sample Objection Response (Price):**

> "Completely understand — and honestly, most of our best customers
> said the same thing before they started. The free tools are great
> for basic use. Where they fall short is [specific gap]. That's
> exactly what [Product] solves. Want to see the before/after from
> someone in a similar role to you?"

---

## Works Best With

Use **AI Lead Generation & Prospect Finder** to find and qualify prospects,
**AI Cold Email & LinkedIn Outreach Generator** to open conversations,
then this skill to close the deals.

---

## Limitations

- Generates copy and strategy only — does not send messages automatically.
- Closing effectiveness depends on the quality of inputs. Paste the
  customer's actual message for best results.
- Always review before sending. Adapt tone to match your relationship
  with the specific customer.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-03-22 | Initial release |
