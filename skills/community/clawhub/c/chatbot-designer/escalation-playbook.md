# Escalation Playbook

## Escalation Philosophy

An escalation is not a failure — it is the chatbot doing its job. The goal is to:
1. Catch the moment when a human is needed
2. Transfer context so the customer doesn't repeat themselves
3. Set an accurate expectation for response time
4. Leave the customer feeling helped, not abandoned

A chatbot with excellent escalation design achieves higher CSAT than one that tries to resolve everything and gets stuck.

## Escalation Trigger Taxonomy

### Tier 1 — Immediate Escalation (within seconds)

| Trigger | Detection method | Queue |
|---|---|---|
| Physical safety mention | Keywords: injury, hurt, damaged, burned, allergic reaction | Emergency / Senior |
| Legal or fraud mention | Keywords: fraud, dispute, chargeback, lawyer, report | Legal / Senior |
| High-value customer | CRM tag: LTV > $[threshold] | Priority |
| Explicit human request | Keywords: human, agent, person, real | General |
| Severe frustration language | Keywords: furious, unacceptable, disgusting, lawsuit | Priority |

### Tier 2 — Escalation After 2 Failed Attempts

| Trigger | Condition | Queue |
|---|---|---|
| Unresolvable intent | Bot attempted twice, no resolution | General |
| Missing order data | Cannot find order after 2 lookups | General |
| Out-of-policy request | Outside return window, discontinued product | General |
| Complex multi-issue | Customer raises 3+ different issues in one session | General |

### Tier 3 — Proactive Escalation (Batched)

| Trigger | Timing | Action |
|---|---|---|
| Unhandled intent | Weekly review | Add to flow build queue |
| Low CSAT bot rating | <3/5 rating given | Review transcript; identify gap |
| Long session with no resolution | Session > 10 min, no confirmation | Flag for quality review |

## Escalation Handoff Protocol

### Step 1 — Signal the transition warmly
Never abruptly transfer. Use a bridging line:
> "Let me get one of our team members to help you with this."
> "This is something I want to make sure our specialists handle for you."
> "I'm connecting you now — you're in good hands."

### Step 2 — Summarize the conversation
Pre-fill the ticket with:
- Customer name and contact
- Order number(s) involved
- Issue summary in 2–3 sentences
- What the bot already tried
- Customer sentiment (frustrated / neutral / positive)
- Any data already collected (return reason, device type, etc.)

**Ticket pre-fill template:**
```
[BOT HANDOFF] Customer: [Name] | Order: #[number]
Issue: [1-sentence summary]
Bot actions taken: [what was attempted]
Data collected: [relevant fields]
Customer sentiment: [frustrated/neutral/satisfied]
Chat transcript: [attached]
```

### Step 3 — Set response time expectation
Never use vague language. Be specific:
- ✅ "Our team will reply within 2 business hours"
- ✅ "You'll hear back by 9am tomorrow"
- ❌ "Someone will be in touch soon"
- ❌ "We'll reply as quickly as possible"

### Step 4 — Confirm and close the bot interaction
> "I've sent everything to our team and you'll receive a reply at [email] by [time]. Your reference number is #[ticket]. Is there anything else I can help with before I hand off?"

## Queue Routing Logic

| Queue | Criteria | Target SLA |
|---|---|---|
| Emergency | Safety, legal, fraud | 30 minutes |
| Priority | LTV > threshold, severe frustration, escalation from chatbot failure | 1 business hour |
| General | Standard escalations | 2–4 business hours |
| After-hours | Outside business hours | By 9am next business day |

## After-Hours Handling

When escalating outside business hours:
1. Acknowledge the timing: "Our team is offline right now (back at [time])."
2. Confirm the ticket is created with a reference number
3. Give a specific "by when" for response — not just "tomorrow"
4. Offer any self-serve options that might help in the meantime

**After-hours script:**
> "Our team is offline right now — we're back at [9am time zone]. I've created a priority ticket for you (#[number]) and someone will reply to [email] by [specific time]. In the meantime, you can check [tracking link / FAQ link] for [relevant self-serve option]."

## CSAT Recovery Protocol

When a customer rates their bot interaction <3/5:
1. Auto-trigger human follow-up within 4 hours
2. Human reviews transcript before reaching out
3. Proactive resolution offer: "I noticed your experience wasn't great — I'd like to make it right."
4. Log the transcript in the quality review queue for flow improvement

## Escalation Metrics to Track

| Metric | Target | Action if off-target |
|---|---|---|
| Escalation rate | <30% | Review top escalated intents; build/fix flows |
| Escalation CSAT | >4.0/5 | Review handoff scripts and response time compliance |
| SLA compliance | >90% | Staffing or routing adjustment |
| Repeat contacts | <10% of escalated cases | Post-resolution follow-up improving |
