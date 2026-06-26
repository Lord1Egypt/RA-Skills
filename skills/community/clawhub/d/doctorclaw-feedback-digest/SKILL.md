---
name: doctorclaw-feedback-digest
description: "Customer feedback digest — collect, categorize, and summarize reviews, survey responses, and support tickets. Weekly cron or on-demand."
version: 1.0.0
tags: [feedback, customer-success, reviews, support, automation]
metadata:
  clawdbot:
    emoji: "⭐"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Customer Feedback Digest

Listen to your customers without drowning in data. This skill collects feedback from reviews, surveys, support tickets, and social mentions — then categorizes it by sentiment, topic, and urgency so you know exactly what to fix, what to celebrate, and what to respond to.

Run it weekly for a full digest, or trigger on-demand after a product launch or campaign.

## What You Get

- All feedback categorized by sentiment (positive, neutral, negative, critical)
- Topics extracted and ranked by frequency (feature requests, bugs, praise, complaints)
- Urgent issues flagged for immediate response
- Suggested responses for negative reviews
- Trend analysis showing sentiment shifts over time
- Highlight reel of your best customer quotes

## Setup

### Required
- **Feedback source** — At least one: review platform data (CSV export), survey responses, support tickets, or social mentions your agent can access

### Optional (but recommended)
- **Multiple sources** — combine Google Reviews, app store reviews, support emails, survey tools
- **Response access** — ability to reply to reviews or tickets after your approval
- **Delivery channel** — Telegram/Discord for digest and urgent alerts
- **Feedback archive** — folder to store historical digests for trend tracking

### Configuration

Tell your agent:

1. **Feedback sources** — where to pull feedback from (file paths, URLs, integrations)
2. **Review schedule** — when to compile the digest (default: every Monday)
3. **Response style** — your tone for responding to reviews (grateful, professional, empathetic)
4. **Urgency triggers** — what counts as urgent (1-star reviews, keywords like "refund", "broken", "unsubscribe")
5. **Delivery** — where to send the digest
6. **Product/service context** — what you sell, so the agent understands the feedback properly

## How It Works

### Step 1: Collect Feedback
- Pull feedback from all configured sources
- For each piece: source, date, author (if available), content, rating (if applicable)
- Normalize ratings across sources (stars → sentiment score)

### Step 2: Analyze Sentiment
Categorize each piece of feedback:

**🟢 POSITIVE — Happy customers**
- 4-5 star reviews, compliments, thank-you messages
- Keywords: love, great, amazing, helpful, recommend, best

**🟡 NEUTRAL — Mixed or informational**
- 3-star reviews, feature requests without complaint, questions
- Neither strongly positive nor negative

**🔴 NEGATIVE — Unhappy customers**
- 1-2 star reviews, complaints, frustration
- Keywords: disappointed, frustrated, doesn't work, waste, overpriced

**⚫ CRITICAL — Needs immediate attention**
- Threats to churn, refund requests, public complaints, legal mentions
- Keywords: refund, cancel, lawyer, scam, report, BBB

### Step 3: Extract Topics
Group feedback by recurring themes:
- **Feature requests** — things customers want added
- **Bugs/issues** — things that are broken or confusing
- **Praise points** — what customers love most (keep doing this)
- **Pain points** — recurring frustrations
- **Competitive mentions** — when customers compare you to competitors

Rank by frequency — most-mentioned topics first.

### Step 4: Draft Responses
For NEGATIVE and CRITICAL feedback, draft responses:
- Acknowledge the issue specifically
- Apologize where appropriate
- Offer a solution or next step
- Match the configured response style
- Mark as DRAFT — never post without approval

### Step 5: Compile Digest

```
⭐ Feedback Digest — [Date Range]

📊 SENTIMENT OVERVIEW
Total feedback: [X] pieces
🟢 Positive: [X] ([X]%) | 🟡 Neutral: [X] ([X]%)
🔴 Negative: [X] ([X]%) | ⚫ Critical: [X]
Average rating: [X.X] / 5.0

⚫ CRITICAL — RESPOND NOW ([X])
1. [Source] — [Author]: "[excerpt]"
   📝 Suggested response: "[draft]"

🔴 NEGATIVE HIGHLIGHTS ([X])
2. [Source] — "[excerpt]"
   Topic: [bug/complaint/pricing]
   📝 Suggested response ready

🔥 TOP TOPICS THIS WEEK
1. [Topic] — mentioned [X] times ([sentiment breakdown])
2. [Topic] — mentioned [X] times
3. [Topic] — mentioned [X] times

💚 BEST QUOTES (use in marketing!)
• "[Great quote from happy customer]" — [Author]
• "[Another great quote]" — [Author]

📈 TRENDS
• Sentiment [up/down] [X]% vs last period
• New topic emerging: [topic]
• Recurring issue: [issue] — [X] mentions this month

💡 RECOMMENDATIONS
• [Fix X — 8 negative mentions this week]
• [Feature Y requested by 5 customers — consider adding]
• [Reply to critical reviews within 24 hours]
```

### Step 6: Deliver & Archive
- Send digest via configured channel
- Critical items get immediate alerts (don't wait for weekly digest)
- Save to `memory/feedback/YYYY-MM-DD.md`
- Track response status (drafted → approved → posted)

## Examples

**User:** "Show me this week's customer feedback"

**Agent compiles and responds with the full digest.**

**User:** "What are customers complaining about most?"

**Agent:**
> Top complaints this week:
> 1. **Onboarding confusion** — 6 mentions. Customers struggling with initial setup.
> 2. **Slow response times** — 4 mentions. Support taking 48+ hours.
> 3. **Pricing clarity** — 3 mentions. Confusion about what's included in each tier.
>
> Recommendation: Create an onboarding guide or video — this alone would address 40% of negative feedback.

**User:** "Send response to the critical review"

**Agent:** Posts the approved response to the review platform.

## Customization Ideas

- **NPS tracking** — run periodic NPS surveys and track scores over time
- **Review request automation** — after positive interactions, auto-send review requests to happy customers
- **Feedback-to-feature pipeline** — auto-create feature request tickets from customer suggestions
- **Competitor review monitoring** — track what customers say about competitors too
- **Testimonial collector** — auto-curate the best quotes for marketing use

## Want More?

This skill handles feedback collection and analysis. But if you want:

- **Custom integrations** — connect to Trustpilot, G2, Intercom, Zendesk, or your specific review platforms
- **Advanced automations** — auto-respond to reviews, trigger NPS surveys, feed insights into product roadmap
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
