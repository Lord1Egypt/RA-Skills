---
name: Chatbot Designer
description: Design customer service chatbot conversation flows for ecommerce — order status, returns, product recommendations, and escalation rules — that reduce ticket volume while maintaining satisfaction scores.
---

# Chatbot Designer

Design customer service chatbot conversation flows for ecommerce including order status inquiries, return requests, product recommendations, and escalation rules that reduce ticket volume while maintaining satisfaction scores. Most chatbot failures come not from the technology but from poorly designed flows — dead ends, missing escalation paths, or responses that feel robotic. This skill produces conversation architecture, intent mapping, and response logic that resolves common queries automatically while seamlessly handing off complex issues to human agents.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Intent coverage | Map top 10 intents from ticket data before writing any flows | Map intents from assumption | Build flows for every possible scenario before launching |
| Escalation design | Graceful escalation after 2 failed responses + any customer frustration signal | Escalation only when explicitly requested | No escalation path — bot loops or dead-ends |
| Tone | Warm, direct, brand-consistent; acknowledges frustration | Neutral corporate tone | Overly casual/emoji-heavy OR stiff formal robospeak |
| Resolution path | Bot resolves or creates ticket — never leaves customer waiting without next step | Resolves common issues, drops others | Gives information without action ("call this number") |
| Order integration | Connected to OMS so bot can pull live order status | Static FAQs about shipping timelines | Cannot access order data at all |
| Return flow | Initiates return label automatically; confirms eligibility in real time | Explains return policy; directs to email | Can't process returns; sends customer elsewhere |
| Measurement | CSAT on bot interactions + containment rate + escalation rate tracked weekly | Track containment rate only | No metrics |

## Solves

- Support team overwhelmed with high-volume, repetitive queries (order status, return requests, shipping ETAs)
- Long first-response times hurting customer satisfaction and review scores
- After-hours support gaps — customers getting no response outside business hours
- Support costs scaling linearly with order volume instead of leveling off
- Inconsistent answers from human agents on standard policy questions
- High ticket volume from customers who can't self-serve on the website
- Returns and exchanges handled manually when they could be automated end-to-end

## Workflow

### Step 1 — Map Your Top 10 Support Intents

Pull 90 days of support ticket data and categorize by intent. Most ecommerce stores find 80% of volume concentrated in 5–7 intents.

**Typical ecommerce intent distribution:**

| Intent | Average % of tickets | Automatable? |
|---|---|---|
| Order status / tracking | 28–35% | ✅ Fully (with OMS integration) |
| Return / exchange request | 18–24% | ✅ Mostly (policy check + label generation) |
| Shipping delay inquiry | 10–15% | ✅ Partially (status pull + proactive message) |
| Product question (pre-purchase) | 8–12% | ✅ Partially (FAQ lookup) |
| Wrong item received | 5–8% | ✅ Partial (initiate replacement flow) |
| Payment / billing issue | 4–7% | ⚠️ Partial (info only; resolution needs human) |
| Discount / promo code issue | 3–5% | ✅ Mostly (validate code, explain terms) |
| Cancellation request | 3–5% | ✅ If pre-fulfillment; ⚠️ if shipped |
| Product defect / damage | 3–5% | ✅ Initiate claim; photo required |
| General feedback | 2–4% | ⚠️ Log and escalate |

Prioritize the top 3–5 intents for chatbot coverage at launch. Build 100% coverage of these before adding lower-volume intents.

### Step 2 — Design the Main Menu Architecture

Every chatbot needs a clear entry point. Design the main menu to match your top intents — never more than 5–6 options.

**Recommended main menu structure:**

```
Hi [name]! How can I help today?
  → 📦 Track my order
  → 🔄 Return or exchange
  → ❓ Product question
  → 💳 Billing or payment
  → 🙋 Talk to a person
```

Rules:
- Always include "Talk to a person" — hiding this frustrates customers and tanks CSAT
- Use icons for scan-ability on mobile
- Keep labels under 4 words
- Offer free-text input alongside menu (some customers prefer to type)

### Step 3 — Design Each Intent Flow

For each priority intent, design a complete flow with: entry points, required data collection, decision branches, resolution, and escalation exit.

**Flow template structure:**

```
1. TRIGGER: Intent detected (menu selection or keyword match)
2. ACKNOWLEDGE: "Let me pull that up for you."
3. DATA COLLECT: What does the bot need? (order number, email, product name)
4. LOOKUP / CHECK: Connect to data source or apply policy rules
5. RESOLUTION BRANCH A: Can resolve → confirm resolution, offer next step
6. RESOLUTION BRANCH B: Cannot resolve → explain why + escalate gracefully
7. ESCALATION: Create ticket with full context pre-filled; set expectation ("Team will reply in 2–4 hours")
8. CONFIRMATION: Always confirm what happened before ending conversation
```

**Order Status Flow example:**

```
Bot: "To track your order, I'll need your order number or the email you used to order."
Customer: [provides order #12345]
Bot: [looks up OMS] → "Order #12345 was shipped on June 3rd via FedEx.
     Estimated delivery: June 7th.
     Tracking: [link]
     Is there anything else you'd like to know about this order?"
     → Yes → return to order menu
     → No → "Thanks! If your package doesn't arrive by June 8th, come back and I'll help you file a claim."
```

### Step 4 — Design the Return / Exchange Flow

Returns are the highest-value flow to automate — they're high-volume, rule-based, and automatable.

**Return eligibility check decision tree:**

```
Customer: "I want to return my order"
Bot: "I can help with that. What's your order number?"
→ [Order number lookup]
→ Check: Is order within return window? (e.g., 30 days from delivery)
   → YES: "Great — this order is eligible. What's the reason for your return?"
           → [Reason menu: wrong size / doesn't meet expectations / damaged / wrong item]
           → [Generate return label or RMA number]
           → "Your prepaid return label has been sent to [email]. Please drop off within 7 days."
   → NO: "This order was delivered on [date] — our 30-day window closed on [date].
           I'm not able to process this automatically, but I'll connect you with our team
           who can review exceptions."
           → [Create ticket: late return request, order details pre-filled]
```

### Step 5 — Design Escalation Protocols

Escalation design is where most chatbots fail. Build these rules:

**Automatic escalation triggers:**
- Customer uses frustration signals: "this is ridiculous," "never again," "unacceptable," "worst," "furious"
- Bot fails to resolve the same intent after 2 attempts
- Customer types "human," "agent," "real person," "help me"
- Issue involves fraud, legal threat, or physical safety
- High-value customer (flag via CRM/LTV tag) — route to priority queue

**Escalation experience requirements:**
1. Never apologize for failing — transition warmly: "Let me get someone on our team to help with this."
2. Pre-fill the ticket with full conversation transcript so customer doesn't repeat themselves
3. Set a specific response time expectation: "Our team will reply by [time] — typically within 2–4 business hours."
4. Offer async confirmation: "You'll get a notification at [email] when we respond."

**Escalation quality test:**
Go through every flow yourself and try to trigger frustration or dead-ends. If you can get the bot stuck or leave without a resolution, fix it before launch.

### Step 6 — Write Response Copy

Bot copy must feel human without pretending to be human. Guidelines:

**Tone principles:**
- Acknowledge before acting: "I'll take a look at that for you" not "Order number required."
- Use contractions: "I'll" not "I will"; "you're" not "you are"
- Be specific: "Your order ships in 3–5 business days" not "orders ship soon"
- Validate frustration without over-apologizing: "I understand that's frustrating — let me help fix it" not "I'm SO sorry for this terrible experience!!!!"
- Avoid robotic completions: "Is there anything else I can help you with today?" → "Anything else on your mind?" is warmer

**Response length:**
- Confirmations: 1–2 sentences
- Policy explanations: 3–4 sentences max, then offer human if still confused
- Error messages: Always include what to do next, never just what failed

### Step 7 — Measure and Iterate

**Core chatbot KPIs:**

| Metric | Definition | Target |
|---|---|---|
| Containment rate | % of conversations bot resolves without human escalation | >60% at 3 months |
| Escalation rate | % of conversations handed to human | <30% |
| CSAT (bot interactions) | Customer satisfaction score post-bot conversation | >3.8 / 5 |
| First contact resolution | % of issues resolved in the first interaction | >50% |
| Drop-off rate | % leaving conversation without resolution or escalation | <15% |
| Top unhandled intents | Intents with no matching flow | Review weekly |

Review unhandled intent logs weekly for the first 3 months — these are your next flows to build.

## Examples

### Example 1 — Fashion Brand (Shopify + Gorgias Chatbot)

**Setup:** 450 support tickets/week; top intents: order status (34%), returns (21%), sizing questions (14%)  
**Tool:** Gorgias with Shopify integration  
**Flows built at launch:** Order tracking, return initiation, size guide lookup

**Order tracking flow performance:**
- 89% of order status queries resolved by bot without human
- Average resolution time: 8 seconds (vs. 4-hour human response time)
- CSAT on bot interactions: 4.1/5

**Return flow:**
- 74% of eligible returns processed end-to-end by bot
- Average time to label generation: 2 minutes
- Support ticket volume down 31% within 60 days of launch

---

### Example 2 — Electronics Accessories (WooCommerce + Tidio)

**Challenge:** High volume of pre-purchase compatibility questions that required manual lookup  
**Solution:** Product compatibility decision tree built in Tidio, connected to product specs database

**Flow:**
```
"What device are you trying to use this with?"
→ [Device selection menu: iPhone 15 / iPhone 14 / Samsung S24 / Other]
→ "The [product] is fully compatible with [device]. It includes [cable type] in the box.
   Want to add it to your cart?"
```

**Result:**
- Pre-purchase conversion increased 8% (buying confidence from instant compatibility confirmation)
- Compatibility-related support tickets down 44%
- Human agents redirected from answering repetitive compatibility questions to handling escalations and complex issues

## Common Mistakes

1. **Building flows from assumption instead of ticket data** — Designing 20 flows for hypothetical scenarios while missing the 3 intents that make up 60% of actual ticket volume.

2. **No escalation path** — The single most damaging mistake. A bot that loops or dead-ends when it can't resolve an issue destroys trust faster than no bot at all.

3. **Pretending to be human** — Customers who discover they're talking to a bot after believing it was a person feel deceived. Be transparent: "Hi! I'm [BrandName]'s virtual assistant."

4. **Copy-pasting canned responses** — Bot responses that sound like they came from a 2005 helpdesk FAQ kill the experience. Write for conversation, not documentation.

5. **Launching without OMS integration** — A chatbot that can't actually look up order data can only answer generic shipping questions, not the specific question the customer has.

6. **Ignoring mobile UX** — Most customer service chatbot interactions happen on mobile. Long menus, small tap targets, and text-heavy responses that require scrolling kill completion rates.

7. **No metrics review schedule** — Bots built and forgotten miss the unhandled intents that accumulate weekly. Review intent logs every week for the first 3 months.

8. **Over-qualifying before helping** — Asking for order number, email, AND phone number before providing any assistance feels like an interrogation. Collect the minimum needed for each specific flow.

9. **CSAT survey fatigue** — Sending a satisfaction survey after every bot interaction annoys customers. Survey 20–30% of interactions randomly, or only after escalation.

10. **Trying to handle everything at launch** — 5 well-designed flows that cover 70% of volume outperform 20 incomplete flows covering 100% of scenarios with gaps and dead ends.

## Resources

- [Output Template](references/output-template.md) — Chatbot flow design document
- [Intent Library](references/intent-library.md) — Pre-built intent patterns and response templates
- [Escalation Playbook](references/escalation-playbook.md) — Escalation trigger rules and handoff scripts
- [Quality Checklist](assets/quality-checklist.md) — Pre-launch chatbot review checklist
