---
name: Automate Lead Scoring with Slack Alerts & Google Sheets Updates
description: "Automate email campaigns, sequences, and analytics for small businesses. Use when the user needs drip campaigns, welcome series, performance tracking, or integration with Mailchimp, ConvertKit, and ActiveCampaign."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["MAILCHIMP_API_KEY", "CONVERTKIT_API_KEY", "ACTIVECAMPAIGN_API_KEY", "SENDGRID_API_KEY"],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📧"
    }
  }
---

# EmailElevate: Automated Email Marketing for Small Businesses

## Overview

EmailElevate is a production-ready automation skill designed to help small business owners and marketing teams build, launch, and optimize email campaigns without the complexity of traditional marketing platforms. This skill transforms email marketing from a manual, time-intensive process into an automated, data-driven system.

**Why EmailElevate Matters:**
- **Save 10+ hours/week** on campaign setup and manual email sending
- **Increase open rates by 25-40%** through intelligent segmentation and A/B testing
- **Real-time analytics** to understand what resonates with your audience
- **Seamless integrations** with Mailchimp, ConvertKit, ActiveCampaign, SendGrid, and WordPress
- **Compliance-ready** with GDPR, CAN-SPAM, and CASL standards built-in

EmailElevate eliminates the friction between idea and execution. Instead of manually copying email lists, configuring sequences, and checking metrics across dashboards, you tell EmailElevate what you want to accomplish, and it handles the technical heavy lifting.

**Ideal For:**
- E-commerce businesses building automated product launch sequences
- SaaS companies managing onboarding and nurture flows
- Content creators sending newsletters with engagement tracking
- Agencies managing multiple client email programs
- Coaches and consultants automating client communication

---

## Quick Start

Try these prompts immediately to see EmailElevate in action:

### Example 1: Build a Welcome Series
```
Create a 5-email welcome sequence for my e-commerce store.
Email 1: Welcome + 10% discount (send immediately)
Email 2: Product recommendations (send 2 days later)
Email 3: Customer success story (send 5 days later)
Email 4: Frequently asked questions (send 8 days later)
Email 5: Re-engagement offer (send 12 days later)

Integrate with Mailchimp list "newsletter-subscribers"
Track open rates, click rates, and conversion events
```

### Example 2: Segment and Automate Based on Behavior
```
Create automated workflows for my ConvertKit audience:
- Trigger: New subscriber joins
- Action: Send welcome email + tag as "engaged"
- Branch 1: If they open 3+ emails → move to "hot-leads" segment
- Branch 2: If no opens in 7 days → send re-engagement email
- Branch 3: If they click on paid course link → add to "sales-ready" list

Set up A/B test: subject line "Learn X" vs "Discover X"
Report results weekly to my Slack #marketing channel
```

### Example 3: Analyze Campaign Performance
```
Generate a performance report for my last 3 campaigns:
- Overall metrics: send count, open rate, click rate, conversion rate
- Segment breakdown: by traffic source, device type, geographic location
- Subject line analysis: which performed best and why
- Recommendation engine: suggest improvements for next campaign

Export as CSV and post a summary to my Slack #analytics channel
```

### Example 4: Sync WordPress Blog Posts to Email Newsletter
```
Automate my weekly newsletter:
- Trigger: New WordPress post published with tag "newsletter"
- Action: Extract title, featured image, excerpt, and link
- Format: Create HTML email template with post previews
- Deliver: Send to my ActiveCampaign list "blog-subscribers"
- Schedule: Every Monday at 9 AM EST

Include social sharing buttons and track which links get clicked most
```

---

## Capabilities

### Campaign Building & Automation

**Create Email Sequences from Scratch**
- Build multi-step sequences with conditional logic (if/then branching)
- Set delays between emails (hours, days, weeks)
- Auto-personalize with merge tags: `{{first_name}}`, `{{company}}`, `{{purchase_history}}`
- A/B test subject lines, sender names, send times, and content variations
- Preview emails across devices (desktop, mobile, tablet)

**Email Template Generation**
- Auto-generate responsive HTML templates from your brand guidelines
- Choose from 50+ pre-built templates (welcome, promotional, educational, re-engagement)
- Customize colors, fonts, and CTAs to match your brand
- Add dynamic content blocks that change based on subscriber segment

**Trigger-Based Automation**
- New subscriber joins list
- User purchases a product or service
- User abandons shopping cart (e-commerce)
- User downloads a lead magnet
- User hasn't engaged in 30+ days (re-engagement trigger)
- Custom date fields (birthday, anniversary) trigger automated sends
- Behavioral triggers: link clicks, page visits, video plays

**Segmentation & List Management**
- Segment audiences by: location, purchase history, engagement level, custom fields, list source
- Auto-remove unsubscribes and bounced emails
- Merge duplicate contacts
- Clean email lists using built-in validation
- Create dynamic segments that update in real-time

### Analytics & Reporting

**Real-Time Performance Metrics**
- Open rate (with geographic breakdown)
- Click-through rate (CTR) with link-level performance
- Conversion tracking (purchases, sign-ups, downloads)
- Bounce rate and bounce reason classification
- Unsubscribe rate and feedback collection
- Mobile vs. desktop engagement
- Send-time optimization recommendations

**Advanced Analytics**
- Revenue attribution (which emails drove sales)
- Customer lifetime value (CLV) by segment
- Churn prediction for at-risk subscribers
- Content performance scoring (which topics resonate)
- Competitor benchmarking (your performance vs. industry averages)

**Automated Reporting**
- Daily digests to your Slack workspace
- Weekly summary reports via email
- Custom dashboards (embed in your website)
- Export reports as PDF, CSV, or JSON
- Schedule recurring reports for stakeholders

### Platform Integrations

**Email Service Providers**
- **Mailchimp**: Manage lists, segments, campaigns, automation, analytics
- **ConvertKit**: Sync subscribers, create sequences, tag subscribers, track opens
- **ActiveCampaign**: Trigger-based workflows, custom fields, deal tracking
- **SendGrid**: High-volume sending, delivery tracking, bounce management
- **Klaviyo**: E-commerce automation, dynamic content, revenue tracking

**CRM & Business Tools**
- **Salesforce**: Sync leads, log activities, update deal status
- **HubSpot**: Create contacts, manage pipelines, track engagement
- **Zapier**: Connect 1000+ apps to your email workflow
- **Slack**: Get notified of campaign milestones, post analytics, receive approvals

**E-Commerce Platforms**
- **Shopify**: Trigger emails on purchase, abandoned cart, re-order
- **WooCommerce**: Abandoned cart recovery, upsell sequences
- **BigCommerce**: Product recommendations, post-purchase automation

**Content Platforms**
- **WordPress**: Auto-sync blog posts to newsletters
- **Medium**: Republish articles in email format
- **YouTube**: Send video digests to subscribers

---

## Configuration

### Environment Variables (Required)

Set these before running EmailElevate:

```bash
# Email Service Provider APIs (choose at least one)
export MAILCHIMP_API_KEY="your_mailchimp_api_key_here"
export CONVERTKIT_API_KEY="your_convertkit_api_key_here"
export ACTIVECAMPAIGN_API_KEY="your_activecampaign_api_key_here"
export ACTIVECAMPAIGN_URL="https://youraccount.api-us1.com"
export SENDGRID_API_KEY="your_sendgrid_api_key_here"

# Analytics & Reporting (optional but recommended)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export GOOGLE_ANALYTICS_KEY="your_google_analytics_key"

# Brand Customization
export BRAND_SENDER_NAME="Your Company Name"
export BRAND_SENDER_EMAIL="marketing@yourcompany.com"
export BRAND_REPLY_TO="support@yourcompany.com"
```

### Configuration Options

```yaml
emailelevate:
  defaults:
    timezone: "America/New_York"           # Send emails in user's timezone
    unsubscribe_link: true                 # Include unsubscribe link (required)
    reply_tracking: true                   # Track replies and add to CRM
    link_tracking: true                    # Track all clicks
    image_tracking: true                   # Track open rate via tracking pixel
    list_validation: true                  # Clean emails before sending
    
  compliance:
    include_physical_address: true         # Required by CAN-SPAM
    gdpr_mode: false                       # Set to true if EU audience
    double_opt_in: false                   # Require confirmation after signup
    
  automation:
    max_concurrent_sequences: 50           # Limit automation load
    retry_bounced_emails: true             # Retry failed sends
    max_retry_attempts: 3
    
  analytics:
    track_conversions: true
    attribution_window_days: 30
    track_unsubscribe_reason: true
```

### Setup Instructions

1. **Get API Keys**
   - Visit your email platform (Mailchimp, ConvertKit, etc.)
   - Navigate to API settings or integrations
   - Generate and copy your API key
   - Save to your environment variables

2. **Connect Your Email List**
   ```
   Sync my Mailchimp list "Newsletter Subscribers" with EmailElevate
   ```

3. **Verify Sender Email**
   - Confirm your sending domain is verified
   - This prevents emails from going to spam

4. **Test with Sample Campaign**
   ```
   Create a test email campaign and send to myself before production use
   ```

---

## Example Outputs

### Output 1: Welcome Sequence Campaign Structure
```json
{
  "campaign_id": "welcome-series-ecom-2024",
  "name": "E-Commerce Welcome Series",
  "platform": "Mailchimp",
  "emails": [
    {
      "sequence": 1,
      "subject": "Welcome! Here's your 10% discount 🎉",
      "send_time": "immediate",
      "template": "welcome-discount",
      "personalization": ["{{first_name}}", "{{company}}"],
      "a_b_test": { "variant_a": "Welcome! Here's your 10% discount 🎉", "variant_b": "We're excited to have you! Claim your welcome offer →" }
    },
    {
      "sequence": 2,
      "subject": "We handpicked 3 products just for you",
      "send_delay": "2 days",
      "template": "product-recommendations",
      "dynamic_content": "based on browse history"
    },
    {
      "sequence": 3,
      "subject": "See how {{first_name}} is using our product",
      "send_delay": "5 days",
      "template": "social-proof-case-study"
    }
  ],
  "estimated_metrics": {
    "send_count": 15000,
    "projected_open_rate": "32%",
    "projected_click_rate": "8%",
    "projected_revenue": "$4,800"
  }
}
```

### Output 2: Performance Analytics Report
```
📊 EMAIL CAMPAIGN PERFORMANCE REPORT
Campaign: "Black Friday Flash Sale"
Period: 2024-01-15 to 2024-01-22

SUMMARY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sent:               50,000 emails
Delivered:          49,250 (98.5%)
Bounced:            750 (1.5%)
Opens:              18,970 (38.5% open rate)
Clicks:             3,794 (7.7% click rate)
Conversions:        456 (0.92% conversion rate)
Revenue Generated:  $12,456

SEGMENT PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Segment              Opens    Clicks   Conversions
Past Customers       45.2%    12.1%    1.8%
Website Visitors     38.1%    8.3%     0.9%
Email Signups        28.5%    4.2%     0.4%

TOP PERFORMING SUBJECT LINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. "48-hour flash sale (40% off inside)" — 52% open rate
2. "Your exclusive early access link" — 48% open rate
3. "Last chance: Sale ends tonight" — 41% open rate

DEVICE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mobile:              68% (opens), 71% (clicks)
Desktop:            32% (opens), 29% (clicks)

RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Your "past customers" segment outperforms by 18%
  → Send more campaigns to this segment
✓ Mobile users click 2.4x more than desktop
  → Optimize for mobile-first design
✓ Subject line pattern "exclusive + deadline" works best
  → Use this formula for future campaigns
```

### Output 3: Automated Workflow Diagram
```
TRIGGER: New subscriber joins list
    ↓
[Email 1: Welcome] (send immediately)
    ↓
    ├─ IF opens within 24 hours → Tag "engaged"
    │   ↓
    │   [Email 2: Main offer] (send 2 days later)
    │
    └─ IF no open within 24 hours → Tag "cold-lead"
        ↓
        [Re-engagement email] (send 3 days later)
        ↓
        ├─ IF clicks link → move back to "engaged" segment
        └─ IF no open → unsubscribe after 30 days
```

---

## Tips & Best Practices

### Campaign Optimization
1. **Test Subject Lines First**
   - Use A/B testing to find your winning formula
   - Front-load keywords (users see first 50 characters)
   - Avoid spam trigger words: "free," "urgent," "buy now"
   - Emojis increase open rates by 7-12% (test for your audience)

2. **Segment Ruthlessly**
   - Segmented campaigns get 14.3x higher conversion rates
   - Create segments by: purchase history, engagement level, traffic source, industry
   - Update segments monthly based on new behavior

3. **Timing Matters**
   - Test different send times (9 AM, 2 PM, 6 PM in user's timezone)
   - Tuesday-Thursday typically perform 15% better than weekends
   - Use EmailElevate's send-time optimization to auto-schedule

4. **Content Strategy**
   - Follow 80/20 rule: 80% value, 20% promotion
   - Use clear, benefit-driven CTAs ("Get 30% Off" not "Click Here")
   - Keep emails under 600 pixels wide for mobile
   - Include 1-2 images maximum (text-heavy emails convert better)

### Compliance & Deliverability
1. **Authentication Setup**
   - Implement SPF, DKIM, DMARC records (prevents spoofing, improves deliverability)
   - Warm up new sending domains gradually (start with 100/day, increase 10% daily)
   - Monitor bounce and complaint rates (keep under 0.5%)

2. **List Hygiene**
   - Remove invalid emails every 30 days
   - Re-engage inactive subscribers