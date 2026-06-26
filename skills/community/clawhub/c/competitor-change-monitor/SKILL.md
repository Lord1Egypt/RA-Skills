---
name: competitor-change-monitor
description: Monitor competitor websites for changes, analyze updates, generate competitive intelligence reports. Track pricing, content, features, and alert on significant changes.
---

# Competitor Change Monitor

Automatically monitor competitor websites, detect changes, and generate actionable intelligence reports. Perfect for sales teams, product managers, and competitive strategists.

## What This Skill Does

Monitor a list of competitor websites continuously. Detect and analyze:
- **Pricing changes** (price increases/decreases)
- **New product launches** (feature announcements)
- **Content updates** (blog posts, case studies, testimonials)
- **Website structure changes** (new pages, navigation)
- **Messaging shifts** (homepage copy, value proposition)
- **Customer evidence** (testimonials, case studies, logos)

Generate automated reports with:
- Change summary (what changed and when)
- Competitive implications (what it means for you)
- Recommended actions (how to respond)
- Sentiment shift (tone analysis of marketing copy)
- Feature comparison (your features vs. theirs)

## When to Use This Skill

Use this skill when you need to:

- **Stay ahead of competition** → Monitor 3-5 key competitors continuously
- **Identify market threats** → Detect when competitors launch new features or pricing
- **Validate product strategy** → See what competitors are prioritizing
- **Support sales team** → Provide recent competitive intel to deal teams
- **Track marketing changes** → Monitor messaging shifts and positioning
- **Generate reports** → Weekly/monthly competitive intelligence for leadership

## How It Works

### Setup Phase

1. **Define competitors to monitor** → List of competitor domain URLs
2. **Set monitoring frequency** → Daily, weekly, or custom schedule
3. **Configure alerts** → What types of changes matter to you (pricing, content, etc.)
4. **Choose report style** → Executive summary, detailed analysis, or raw data

### Monitoring Phase

The agent:
- Takes a snapshot of each competitor website (HTML + content extract)
- Compares to previous snapshot using semantic diff
- Identifies meaningful changes (ignores nav reorders, minor wording)
- Categorizes changes (pricing, product, marketing, etc.)
- Generates change report with implications

### Reporting Phase

Automatic reports delivered:
- **Daily alerts** (if significant changes detected)
- **Weekly digest** (summary of all changes)
- **Monthly strategic report** (trends and implications)
- **Custom trigger reports** (on-demand analysis)

## Example Usage

```
User: "Monitor Stripe, Square, and PayPal. Alert me if they change pricing or add features."

Agent:
✓ Setup monitoring for stripe.com, square.com, paypal.com
✓ Configure alerts: pricing changes, feature announcements
✓ Schedule daily snapshot + weekly report
✓ Start baseline snapshot (current state)

[Day 3, 3pm]
Alert: Stripe updated their pricing page
  - New tier: "Stripe Premium" at $299/month
  - Feature added: "Dedicated account manager"
  - Implication: Targeting mid-market customers directly
  - Action: Review pricing to ensure competitiveness

[Weekly Report]
Competitors tracked: 3
Changes detected: 7
Most significant: PayPal launched "Commerce Manager" (new product)
Recommended action: Benchmark your comparable features
```

## Features Included

### Monitoring Capabilities
- **Continuous snapshots** → Weekly baseline snapshots of competitor sites
- **Change detection** → Semantic diff (understand what changed, not just text)
- **Categorization** → Automatically categorize changes (product, pricing, marketing)
- **Historical tracking** → Keep history of all changes per competitor

### Analysis & Intelligence
- **Competitive implications** → What does this change mean for your position?
- **Sentiment analysis** → Tone/messaging shifts in their marketing
- **Feature mapping** → Track new features they launch vs. what you have
- **Pricing intelligence** → Price changes, new tiers, discounting patterns

### Reporting
- **Daily alerts** → Real-time notification of significant changes
- **Weekly digest** → Consolidated report of all changes
- **Custom reports** → On-demand competitive analysis
- **Timeline view** → See competitor evolution over time

## Configuration Options

### Competitors to Monitor
```
competitors: [
  { name: "Stripe", url: "https://stripe.com", category: "payment" },
  { name: "Square", url: "https://square.com", category: "payment" },
  { name: "PayPal", url: "https://paypal.com", category: "payment" }
]
```

### Alert Triggers
```
alerts:
  - pricing_change: true        # Alert on any pricing page update
  - new_product: true           # Alert on feature announcements
  - content_update: true        # Alert on blog/case study changes
  - messaging_shift: true       # Alert on homepage copy changes
  - minimum_change_score: 0.3   # Only alert if change is significant (0-1 scale)
```

### Report Schedule
```
reports:
  daily_alert: true             # Real-time alerts on changes
  weekly_digest: "Monday 9am"   # Weekly summary
  monthly_strategic: "1st of month" # Strategic implications report
  timezone: "America/New_York"
```

## Premium Features (Gumroad)

**Free features:**
- Monitor up to 3 competitors
- Weekly reports only
- Basic change detection
- Email delivery

**Premium ($19.99/month):**
- Monitor unlimited competitors
- Daily alerts + weekly + monthly reports
- Advanced change detection (semantic understanding)
- Slack integration (real-time alerts in your channel)
- Custom report scheduling
- Feature comparison matrix (auto-generated)
- Pricing intelligence dashboard
- 90-day change history

**Enterprise ($99+/month):**
- API access (integrate with your systems)
- Custom alert rules (regex, patterns)
- White-label reports
- Team collaboration (shared workspace)
- Custom integrations (Salesforce, HubSpot, etc.)
- Priority support

## Implementation Notes

This skill uses:
- **Web scraping** (fetch competitor website HTML)
- **Semantic diffing** (understand what changed)
- **LLM analysis** (extract meaning from changes)
- **Scheduled jobs** (continuous monitoring)
- **Email/Slack delivery** (reports)

For detailed API documentation and configuration, see `references/api-guide.md`.

## Tips for Best Results

1. **Start with 3-5 competitors** → Too many = alert fatigue
2. **Tune alert sensitivity** → Adjust minimum_change_score to reduce noise
3. **Review weekly** → Set aside time to review reports weekly
4. **Act on insights** → Change isn't intelligence without action
5. **Cross-reference** → Combine with sales intel and market research

## Related Skills

- `content-repurposer` → Turn competitor content into your content
- `market-researcher` → Deep dive market analysis
- `sales-battle-cards` → Auto-generate sales battlecards from comp intel

---

**Status:** Production ready | **Last updated:** May 2026 | **Maintained by:** ClawHub Community
