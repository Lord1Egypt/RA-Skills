---
name: engagement-analytics-tracker
description: >
  Use this skill whenever the user needs help with behavioral analytics, engagement tracking,
  or data collection across any digital touchpoint. Trigger for: website behavioral analytics
  (scroll depth, form abandonment, session tracking, GTM setup, GA4 custom events), email
  engagement tracking (open/click/attribution via Klaviyo, Mailchimp, or custom platforms),
  social media engagement monitoring (owned and competitor), mobile app analytics (Firebase,
  Amplitude, Mixpanel, AppsFlyer), user-level engagement scoring, cohort analysis, conversion
  tracking, event schema design, data layer setup, attribution modeling, or any request like
  "track user behavior", "set up analytics", "measure engagement", "build an event schema",
  "track form abandonment", "email attribution", "app retention analysis", "what events should
  I track?", or "how do I measure X". Always use this skill — do not guess at tracking
  implementations from memory; patterns and APIs change.
---

# Engagement Analytics Tracker Skill

A comprehensive skill for designing, implementing, and interpreting behavioral analytics
across four touchpoint layers: website, email, social, and mobile app.

---

## Four Tracking Modules

| Module | Reference File | Use When |
|--------|----------------|----------|
| Website Behavioral Analytics | `references/website-analytics.md` | GTM, GA4, scroll/form/session tracking |
| Email Engagement Tracker | `references/email-analytics.md` | Klaviyo, Mailchimp, open/click/attribution |
| Social Media Engagement | `references/social-analytics.md` | Owned + competitor social tracking |
| Mobile App Analytics | `references/mobile-analytics.md` | Firebase, Amplitude, Mixpanel, AppsFlyer |

**Load strategy:** Load only the relevant module(s) based on the user's question. For full
analytics stack questions ("build me a complete analytics system"), load all four.

---

## Universal Data Principles

These apply across ALL four modules:

### Event Naming Convention (Use Everywhere)
```
object_action
# Examples:
page_viewed          button_clicked       form_abandoned
video_played         product_viewed       email_opened
session_started      feature_used         purchase_completed
```
- Always lowercase with underscores
- Object first, then action
- Be specific: `checkout_form_abandoned` not `form_event`
- Keep consistent across all platforms — the same action has the same name everywhere

### Data Layer Structure (Web)
```javascript
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  event: 'event_name',           // string — always required
  user_id: 'u_abc123',           // hashed or anonymized
  session_id: 'ses_xyz',
  timestamp: new Date().toISOString(),
  page_path: window.location.pathname,
  // event-specific properties below:
  element_id: 'hero_cta',
  element_text: 'Start Free Trial',
});
```

### Engagement Scoring Formula
A composite score usable across web, email, and app:

```
Engagement Score = 
  (Sessions × 1) +
  (Pages per session × 2) +
  (Scroll 75%+ events × 3) +
  (CTA clicks × 5) +
  (Email opens × 2) +
  (Email clicks × 5) +
  (App sessions × 3) +
  (Feature completions × 8) +
  (Conversions × 20)

Score tiers:
  0–20:   Cold (re-engagement candidate)
  21–50:  Warming (nurture sequence)
  51–100: Engaged (sales-ready consideration)
  100+:   High Value (priority outreach)
```

Adjust weights based on business model. Recalculate weekly per user.

### Privacy & Compliance Baseline
- Never collect raw PII in event properties — hash emails/IDs before sending to any platform
- Implement consent gating: fire tracking tags only after user consents (GDPR)
- Use server-side tagging (GTM Server-Side) for sensitive data flows
- Respect `Do Not Track` headers and browser privacy modes
- Apple ATT opt-in required for IDFA on iOS — design attribution without assuming access
- CCPA: provide opt-out mechanism; do not sell behavioral data without consent

---

## Quick Implementation Checklist

### New Analytics Setup
- [ ] Define tracking plan: events, properties, naming convention — before touching any tool
- [ ] Set up GTM container (web) or SDK (mobile)
- [ ] Implement dataLayer or SDK event calls
- [ ] Configure GA4 or destination analytics platform
- [ ] Validate all events in debug/preview mode before going live
- [ ] Set up consent management (CMP) gating
- [ ] Create dashboards for key metrics
- [ ] Schedule regular data quality audits

### Existing Analytics Audit
- [ ] Are events named consistently? (check for duplicates with different names)
- [ ] Is user_id passed and consistent across sessions and platforms?
- [ ] Are conversion events firing correctly? (test end-to-end)
- [ ] Is there data loss from consent mode, ad blockers, or iOS ATT?
- [ ] Are email UTM parameters correctly attributed in GA4?
- [ ] Are mobile sessions merging correctly with web sessions (cross-device)?

---

## Cross-Channel Attribution Model

When a user touches multiple channels before converting:

```
Journey: Paid Ad → Email Click → Direct Visit → Converted

Attribution options:
  Last-click:     Direct gets 100% credit (most common, least accurate)
  First-click:    Paid Ad gets 100% credit
  Linear:         All 3 channels get 33% each
  Time-decay:     Direct > Email > Paid Ad (recency-weighted)
  Data-driven:    ML model (GA4 DDA) — most accurate, needs volume
```

**Recommended:** Use GA4 Data-Driven Attribution (DDA) when you have 500+ conversions/month.
Below that volume, use Linear to avoid bias toward any single channel.

Track cross-channel with UTM parameters on all non-direct traffic:
```
?utm_source=klaviyo&utm_medium=email&utm_campaign=may_reengagement&utm_content=cta_button
```

---

## Output Templates

### Event Schema Definition
```
Event Name: [object_action]
Trigger: [when exactly does this fire?]
Properties:
  - property_name (type): description, example value
  - property_name (type): ...
Platform: [GTM / Firebase / Klaviyo / etc.]
Destination: [GA4 / BigQuery / Amplitude / etc.]
Privacy: [PII risk? How handled?]
```

### Analytics Health Report
```
DATE: [date]
COVERAGE: [% of key user actions being tracked]
DATA QUALITY: [issues found — missing events, duplicates, naming inconsistencies]
TOP INSIGHTS THIS PERIOD: [what the data shows]
ACTION ITEMS: [what to fix or investigate]
```
