# Tracking Plan for Medici Enterprises / DaVinci Software Labs

## Goal
Instrument all content and products with measurement so we can optimize conversion and attribution.

## Core Principles
1. **UTM everything**: Every external link gets UTM parameters
2. **Channel consistency**: Same naming conventions across all campaigns
3. **Event hierarchy**: Page view → Engagement → Conversion
4. **Privacy first**: No PII in tracking parameters, respect user privacy

---

## UTM Taxonomy

### Standard Parameters
- `utm_source`: Platform where link appears (facebook, google, newsletter, reddit, hn)
- `utm_medium`: Marketing medium (cpc, social, email, organic, referral)
- `utm_campaign`: Specific campaign name (launch_week_1, tax_optimizer_promo, linkedin_april)
- `utm_content`: Ad variant or content type (carousel_ad_1, text_post_2)
- `utm_term`: Keywords (optional, mainly for paid search)

### Naming Conventions
- Use lowercase, underscores for spaces
- Campaign names: `{product}_{initiative}_{timeframe}`
- Content IDs: `{format}_{variant}`

### Examples
```
Product launch:
https://example.com/product?utm_source=hn&utm_medium=social&utm_campaign=dsl_launch_mar2026&utm_content=show_hn_post

Email sequence:
https://example.com/download?utm_source=newsletter&utm_medium=email&utm_campaign=welcome_series&utm_content=email_3

Reddit post:
https://example.com/demo?utm_source=reddit&utm_medium=social&utm_campaign=fire_subreddit_promo&utm_content=text_post
```

---

## Conversion Events

### Critical Events to Track
1. **Page View**: User lands on product page
2. **Feature Exploration**: User interacts with demo or feature showcase
3. **Add to Cart**: User initiates purchase (Gumroad click)
4. **Purchase**: Successful transaction
5. **Module Activation**: User activates a paid module (post-purchase)
6. **Retention**: User returns within 7/30 days

### Event Properties
Each event should capture:
- Timestamp
- Source/Medium/Campaign (from UTM)
- Product/Module ID
- User type (new vs returning)
- Value (for purchase events)

---

## Pixel Implementation

### Facebook Pixel
```html
<!-- Facebook Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');
</script>
```

### Google Analytics 4
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Gumroad Integration
Gumroad provides built-in analytics. To track conversions back to source:
1. Pass UTM parameters through to Gumroad checkout URL
2. Gumroad webhook sends purchase event
3. Parse `referrer` field in webhook payload to attribute sale

---

## Attribution Model

### Last-Touch Attribution (default)
- Credit goes to the last touchpoint before conversion
- Lookback window: 30 days
- Simple, easy to explain, matches most platform reporting

### Future: Multi-Touch Attribution
- Track full customer journey
- Weight different touchpoints (first touch 40%, middle touches 20%, last touch 40%)
- Requires more sophisticated tracking infrastructure

---

## Data Collection Points

### Product Website
- Track: page views, time on page, feature clicks, CTA clicks, demo video plays
- Tools: GA4 + custom events

### Gumroad Store
- Track: product page views, checkout initiations, purchases
- Tools: Gumroad built-in analytics + webhooks

### Email Campaigns
- Track: open rate, click rate, UTM clicks to landing page
- Tools: ConvertKit/Mailchimp built-in + UTM parameters

### Social Posts
- Track: link clicks, engagement rate
- Tools: Platform native analytics + UTM parameters

### Product (Post-Purchase)
- Track: module activations, feature usage, retention
- Tools: Opt-in telemetry (privacy-first, anonymous)

---

## Reporting Structure

### Weekly Report
- Traffic by source/medium
- Top campaigns by conversion
- Conversion funnel: View → Click → Purchase
- Revenue by channel

### Monthly Report
- CAC (Customer Acquisition Cost) by channel
- LTV (Lifetime Value) projections
- Channel ROI
- Attribution model performance

### Tools
- Google Analytics 4 for web traffic
- Gumroad dashboard for sales
- Custom scripts in `scripts/analytics/` for attribution analysis

---

## Privacy & Compliance

### Principles
1. **No PII in UTMs**: Never pass email, name, or identifiable info in tracking parameters
2. **Opt-in telemetry**: Product usage tracking requires explicit user consent
3. **Local-first**: Core product stores no data externally
4. **Transparency**: Clear privacy policy explaining what we track and why

### Cookie Consent
Website requires cookie banner for GA4 and FB Pixel. Gumroad handles their own consent.

---

## Implementation Checklist

- [ ] Set up GA4 property and tracking code
- [ ] Set up Facebook Pixel (if running paid ads)
- [ ] Configure Gumroad webhook endpoint
- [ ] Build UTM link generator script (utm_builder.py) ✅
- [ ] Document pixel configs (pixel_configs.json) ✅
- [ ] Create attribution rules (attribution_config.json) ✅
- [ ] Add UTM parameters to all external links
- [ ] Test conversion tracking end-to-end
- [ ] Set up weekly reporting dashboard
- [ ] Privacy policy update with tracking disclosure

---

## Usage

### Generate UTM Link
```bash
python3 ~/.openclaw/workspace/skills/analytics-tracking/utm_builder.py \
  --url https://example.com/product \
  --source reddit \
  --medium social \
  --campaign fire_launch_mar2026 \
  --content text_post_1
```

### Track Custom Event (GA4)
```javascript
gtag('event', 'module_activated', {
  'module_name': 'einstein_research',
  'user_type': 'new',
  'activation_date': '2026-03-08'
});
```

### Analyze Attribution (future)
```bash
python3 scripts/analytics/attribution_report.py --lookback 30
```

---

## Notes
- Start simple: UTMs + GA4 + Gumroad analytics
- Iterate: Add more sophisticated attribution as we scale
- Privacy first: Always respect user data and be transparent
- Can't improve what we can't measure: Instrument everything

---

**Last Updated**: 2026-03-08  
**Owner**: Ogilvy (CMO) / DaVinci (CEO)  
**Status**: Foundation complete, implementation pending
