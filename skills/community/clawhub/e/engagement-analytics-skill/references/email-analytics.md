# Email Engagement Tracker

## Core Email Metrics to Collect

### Per-Email (Campaign Level)
```
send_timestamp          recipient_email (hashed)     email_id
campaign_id             campaign_name                subject_line
opened (bool)           open_timestamp               open_device
open_location           clicked (bool)               click_timestamp
links_clicked []        bounced (bool)               bounce_type (hard/soft)
unsubscribed (bool)     complaint (bool)             time_to_open_seconds
time_to_click_seconds
```

### Per-User (Profile Level)
```
total_sends             total_opens                  total_clicks
open_rate               click_rate                   click_to_open_rate (CTOR)
unsubscribe_rate        complaint_rate
engagement_trend        (trending up / stable / declining)
preferred_send_time     preferred_device             preferred_content_type
last_open_date          last_click_date              days_since_last_engagement
engagement_score        engagement_tier              (hot/warm/cold/inactive)
```

### Benchmark Targets
| Metric | Good | Average | Needs Work |
|---|---|---|---|
| Open Rate | >35% | 20–35% | <20% |
| Click Rate | >3% | 1–3% | <1% |
| CTOR | >8% | 4–8% | <4% |
| Unsubscribe Rate | <0.1% | 0.1–0.3% | >0.3% |
| Bounce Rate (hard) | <0.5% | 0.5–1% | >1% |
| Complaint Rate | <0.08% | 0.08–0.1% | >0.1% |

---

## Platform-Specific Implementation

### Klaviyo

**Key tracking capabilities:**
- Opens, clicks, bounces, unsubscribes — tracked automatically
- Revenue attribution: 5-day window (campaigns), configurable for flows
- Anonymous visitor backfill: captures on-site behavior before email identification
- UTM parameters supported for GA4 cross-attribution

**JavaScript Identification (for website tracking)**
```javascript
// Run after email capture (signup form, etc.)
klaviyo.identify({
  email: '[email protected]',       // required for email attribution
  first_name: 'Priya',
  last_name: 'Sharma',
  $source: 'homepage_popup',
});

// Track custom events
klaviyo.track('Viewed Pricing Page', {
  plan_viewed: 'pro',
  time_on_page: 45,
});
```

**Webhooks API (account-level events)**
```python
import requests

# Create a webhook subscription for email events
payload = {
    "data": {
        "type": "webhook",
        "attributes": {
            "name": "Email Engagement Webhook",
            "endpoint_url": "https://your-server.com/klaviyo-events",
            "secret_key": "YOUR_SECRET",
        },
        "relationships": {
            "webhook-topics": {
                "data": [
                    {"type": "webhook-topic", "id": "event:klaviyo.email.opened"},
                    {"type": "webhook-topic", "id": "event:klaviyo.email.clicked"},
                    {"type": "webhook-topic", "id": "event:klaviyo.email.bounced"},
                    {"type": "webhook-topic", "id": "event:klaviyo.email.unsubscribed"},
                ]
            }
        }
    }
}

resp = requests.post(
    "https://a.klaviyo.com/api/webhooks/",
    headers={
        "Authorization": "Klaviyo-API-Key YOUR_PRIVATE_KEY",
        "Content-Type": "application/json",
        "revision": "2024-10-15",
    },
    json=payload
)
```

**Important Klaviyo limitation:** Flow webhooks cannot trigger on `email_opened` or `email_clicked`
(these aren't flow triggers). Use System Webhooks (Webhooks API) for engagement events.

**Revenue attribution in Klaviyo:**
- Automatically links purchases to emails within attribution window
- Revenue Per Recipient (RPR) = best cross-campaign comparison metric
- Check "Recipient Activity → Placed Order" in campaign reports for who bought

**Pull profile engagement data:**
```python
# Get profile metrics
resp = requests.get(
    "https://a.klaviyo.com/api/profiles/PROFILE_ID/",
    headers={"Authorization": "Klaviyo-API-Key YOUR_KEY", "revision": "2024-10-15"}
)
profile = resp.json()["data"]["attributes"]
```

### Mailchimp

Two separate APIs:
- **Marketing API** — campaign data, subscriber lists, engagement reports
- **Transactional API (Mandrill)** — transactional email tracking, webhooks

**Get campaign report:**
```python
import requests

api_key = "YOUR_MAILCHIMP_KEY"
server = "us1"  # from your API key suffix

resp = requests.get(
    f"https://{server}.api.mailchimp.com/3.0/reports/CAMPAIGN_ID",
    auth=("anystring", api_key)
)
report = resp.json()
print(f"Opens: {report['opens']['open_rate']}")
print(f"Clicks: {report['clicks']['click_rate']}")
```

**Webhook setup (Mailchimp):**
```python
# Subscribe to engagement events via API
payload = {
    "url": "https://your-server.com/mailchimp-webhook",
    "events": {
        "subscribe": True,
        "unsubscribe": True,
        "profile": True,
        "cleaned": True,      # bounces
        "campaign": True,     # sends
    },
    "sources": {
        "user": True,
        "admin": True,
        "api": True,
    }
}
requests.post(
    f"https://{server}.api.mailchimp.com/3.0/lists/LIST_ID/webhooks",
    auth=("anystring", api_key),
    json=payload
)
```

---

## Attribution: Email → Website → Conversion

### UTM Parameter Strategy
Always append UTMs to every link in every email:
```
https://yoursite.com/product?
  utm_source=klaviyo          (or mailchimp, sendgrid)
  &utm_medium=email
  &utm_campaign=april_promo
  &utm_content=hero_cta       (which link in the email)
  &utm_term=segment_name      (which audience segment, optional)
```

### GA4 Attribution Chain
```
Email sent (Klaviyo)
  → User clicks link with UTM
  → GA4 session starts with source=klaviyo, medium=email
  → User browses, converts
  → Conversion credited to email (or shared per attribution model)
```

**Check in GA4:**
`Reports → Acquisition → Traffic Acquisition` → filter by `Session medium = email`

### Cross-Platform Attribution (Email + Paid + Organic)
```python
# Build a unified attribution table
events = [
    # pull from GA4 BigQuery export
    {"user_id": "u123", "event": "session_start", "source": "email", "ts": "2025-04-01"},
    {"user_id": "u123", "event": "page_view", "source": "email", "ts": "2025-04-01"},
    {"user_id": "u123", "event": "purchase", "source": "direct", "ts": "2025-04-02"},
]
# Use Linear attribution: credit both email (assisted) and direct (last)
```

---

## Engagement Scoring by Email Behavior

```python
def compute_email_score(profile):
    score = 0
    
    # Recency (when did they last engage?)
    days_inactive = profile["days_since_last_engagement"]
    if days_inactive < 7:   score += 20
    elif days_inactive < 30: score += 10
    elif days_inactive < 90: score += 5
    else:                    score -= 10  # cold

    # Frequency (how often do they engage?)
    score += min(profile["open_rate"] * 30, 20)    # max 20 pts
    score += min(profile["click_rate"] * 100, 30)  # max 30 pts

    # Quality signals
    if profile["complaint_rate"] > 0.001: score -= 20  # spam complaints
    if profile["unsubscribe_risk"]:       score -= 10

    return max(score, 0)  # never negative

# Tiers
# 0–20:  Inactive — sunset flow candidate
# 21–40: Cold — re-engagement campaign
# 41–70: Warm — standard nurture
# 71+:   Hot — prioritize for offers, sales outreach
```

---

## Email Preference & Suppression Management

### Track email preferences per user
```
preferred_frequency:    daily / weekly / monthly / as-needed
preferred_content_type: product_updates / educational / offers / all
opted_out_categories:   list of content types suppressed
send_time_preference:   morning / afternoon / evening (derived from open times)
channel_preference:     email / sms / push / all
```

### Automated List Hygiene
- Hard bounce → immediately suppress (blocks deliverability)
- Soft bounce × 3 in 30 days → suppress temporarily
- No opens in 90 days → move to sunset flow
- No opens after sunset flow → suppress permanently
- Keep suppression list synchronized across all platforms (Klaviyo + Mailchimp if using both)
