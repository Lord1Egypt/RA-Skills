---
title: "Building an AI Agent That Saves Your SaaS Revenue"
published: false
description: "How I built an OpenClaw skill that monitors Creem webhooks and uses Claude AI to prevent churn automatically"
tags: ai, saas, typescript, opensource
cover_image:
---

What if your payment system could detect a churning customer, figure out their lifetime value, and auto-apply a retention discount — all before you finish your morning coffee?

That's what I built. An OpenClaw skill that plugs into [Creem](https://creem.io) (a Merchant of Record for SaaS) and turns webhook events into intelligent, autonomous actions. Here's how it works and why it matters.

## The Problem: You Find Out Too Late

Most SaaS founders discover churn in their monthly metrics. By then the customer is gone, the feedback window closed, and the revenue lost.

Creem already sends webhook events for every subscription change — cancellations, payment failures, disputes. But those events just sit in a log unless you build something to act on them.

I wanted something that:
- Alerts me instantly when money is at risk
- Analyzes *why* the customer is leaving
- Takes action autonomously when it's confident enough
- Asks me for approval when it's not

## The Solution: Creem Store Agent

An [OpenClaw](https://openclaw.dev) skill that receives Creem webhooks and runs them through a decision pipeline:

```
Creem Webhook
    |
    v
HMAC-SHA256 Verify -> Dedup -> Classify
    |                              |
    v                              v
Simple events              Churn events
(format + alert)     (fetch context + AI analysis)
    |                              |
    v                              v
Telegram alert         Claude Haiku decides:
                       - CREATE_DISCOUNT (20-40%)
                       - SUGGEST_PAUSE
                       - NO_ACTION
                            |
                    confidence >= 80%?
                     /              \
                   yes               no
                    |                 |
              auto-execute    Telegram buttons
                             [Apply] [Pause] [Skip]
```

It handles all 13 Creem webhook events — from `checkout.completed` to `dispute.created` — and routes cancellations through AI analysis while sending simple formatted alerts for everything else.

## The Interesting Parts

### Webhook Security

Creem signs every webhook with HMAC-SHA256. The handler verifies signatures with timing-safe comparison to prevent timing attacks, then deduplicates events by ID (Creem retries failed deliveries):

```typescript
export function verifySignature(
  body: string, signature: string, secret: string
): boolean {
  const expected = createHmac("sha256", secret)
    .update(body).digest("hex");
  if (expected.length !== signature.length) return false;
  return timingSafeEqual(
    Buffer.from(expected), Buffer.from(signature)
  );
}
```

Nothing fancy here, but I've seen too many webhook handlers skip `timingSafeEqual`. Don't be that person.

### The LLM Prompt

When a cancellation event arrives, the agent fetches context from Creem (subscription history, customer tenure, total revenue) and builds a prompt:

```typescript
export function buildChurnPrompt(ctx: ChurnContext): string {
  return `You are a SaaS retention analyst.
A customer is about to churn. Analyze and recommend ONE action.

Customer: ${ctx.customerEmail}
Plan: ${ctx.productName} ($${ctx.price}/mo)
Tenure: ${ctx.tenureMonths} months
Total Revenue: $${ctx.totalRevenue}
Cancel Reason: ${ctx.cancelReason || "not provided"}

Available actions:
- CREATE_DISCOUNT: Retention discount. Params: { percentage, durationMonths }
- SUGGEST_PAUSE: Pause instead of cancel. Params: {}
- NO_ACTION: Let them go. Params: {}

Rules:
- High-value (>$500 total or >6 months): prefer CREATE_DISCOUNT 20-40%
- Low-tenure (<2 months) or low-value: prefer NO_ACTION
- Medium cases: consider SUGGEST_PAUSE

Respond in JSON only:
{"action": "...", "reason": "...", "confidence": 0.0-1.0, "params": {...}}`;
}
```

Claude Haiku responds in ~200ms with a structured decision. The parser handles code blocks, validates the response shape, and clamps confidence to 0-1. If anything goes wrong — API timeout, unparseable response — a rule-based fallback takes over with confidence 0.5 (never auto-executes).

### Autonomous Actions with a Safety Net

The confidence threshold is the key design decision. At 80%+, the agent auto-executes: creates a retention discount or pauses the subscription through the Creem SDK. Below 80%, it sends a Telegram message with inline buttons:

```
[Apply Discount] [Pause Instead] [Skip]
```

This means high-confidence, high-value saves happen instantly (before the customer moves on), while borderline cases get human judgment. The inline keyboard in Telegram makes approval a single tap.

The actual execution is clean — `creem.discounts.create()` for retention discounts, `creem.subscriptions.pause()` for pauses:

```typescript
case "CREATE_DISCOUNT": {
  const discount = await creem.discounts.create({
    name: `Retention ${percentage}% off`,
    type: "percentage",
    percentage,
    duration: "repeating",
    durationInMonths: months,
    appliesToProducts: [ctx.productId],
  });
  return {
    success: true,
    action: "CREATE_DISCOUNT",
    details: `Created ${percentage}% discount for ${months} months (code: ${discount.code})`,
  };
}
```

## Running the Demo

The repo includes a standalone server and demo script that simulates 5 Creem webhook events — a new sale, subscription activation, cancellation (triggers AI), payment failure, and a dispute:

```bash
git clone https://github.com/malakhov-dmitrii/creem-store-agent
cd creem-store-agent
npm install

# Terminal 1: Start the server
CREEM_WEBHOOK_SECRET=whsec_demo_secret npm run demo:server

# Terminal 2: Fire events
CREEM_WEBHOOK_SECRET=whsec_demo_secret npm run demo
```

You'll see each event processed, classified, and — for the cancellation — analyzed with either Claude (if you set `ANTHROPIC_API_KEY`) or the rule-based fallback.

Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to get real Telegram alerts with inline action buttons.

## Testing

103 tests across 7 modules. Every component is tested in isolation — webhook handler, event processor, rule engine, LLM analyzer (with mocked Claude responses), action executor, Telegram bot, and the helper functions:

```bash
npm test           # 103 tests, ~300ms
npm run typecheck  # TypeScript strict mode
```

The LLM analyzer tests cover edge cases: malformed JSON, missing fields, code blocks in responses, confidence clamping, and API failures falling back to rules.

## Why OpenClaw?

OpenClaw runs locally on your machine and connects to any messaging service. Building this as an OpenClaw skill means:

- **No server to deploy** — runs alongside your other agents
- **Messaging agnostic** — Telegram today, Slack tomorrow
- **Composable** — combine with other skills (e.g., a CRM updater or Slack notifier)
- **Privacy** — your API keys and customer data stay local

Install it: `clawhub install creem-store-agent`

## What's Next

- **Slack integration** — same alerts, different channel
- **Revenue dashboard** — daily/weekly MRR reports with trend analysis
- **Custom rules** — define your own retention playbook (e.g., always offer 50% to annual subscribers)
- **Multi-store** — monitor multiple Creem accounts from one agent

## Try It

The code is MIT licensed and on GitHub: [malakhov-dmitrii/creem-store-agent](https://github.com/malakhov-dmitrii/creem-store-agent)

If you're running a SaaS on Creem and losing sleep over churn, give it a spin. Open an issue if something breaks. Star the repo if it doesn't.

---

*Built for the [Creem Scoops](https://creem.io/scoops) bounty program with [OpenClaw](https://openclaw.dev), [Creem SDK](https://docs.creem.io), and [Claude Haiku](https://anthropic.com).*
