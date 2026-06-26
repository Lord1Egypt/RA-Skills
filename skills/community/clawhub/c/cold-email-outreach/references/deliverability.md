# Email Deliverability Guide

## Domain Setup (Do This First)

### 1. SPF Record
Add TXT record to your domain DNS:
```
v=spf1 include:resend.com ~all
```

### 2. DKIM
Resend provides DKIM keys during domain verification. Add the CNAME records they give you.

### 3. DMARC
Add TXT record:
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

### 4. Verify in Resend
```bash
curl -X POST https://api.resend.com/domains \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "yourdomain.com"}'
```

## Warm-Up Schedule
| Day | Emails/Day | Notes |
|-----|-----------|-------|
| 1-3 | 5 | Send to known contacts first |
| 4-6 | 10 | Mix of warm and cold |
| 7-9 | 15 | Monitor bounce rates |
| 10-12 | 20 | Check spam folder placement |
| 13+ | 25 | Full cold outreach rate |

## Spam Prevention
- Keep emails under 150 words
- No more than 1 link per email
- Avoid spam trigger words: "free", "guarantee", "no obligation", "act now"
- Use plain text (no HTML templates for cold outreach)
- Include a physical mailing address
- Personalize every email (no mass-blast feeling)
- Remove bounced emails immediately
- Track and honor unsubscribe requests

## Metrics to Watch
- **Bounce rate** > 5% → pause and clean list
- **Spam complaints** > 0.1% → rewrite templates
- **Open rate** < 20% → fix subject lines
- **Reply rate** < 2% → fix email body/CTA

## Multi-Domain Strategy
For scaling past 25 emails/day:
1. Register 3-5 sending domains ($10-15/each)
2. Set up SPF/DKIM/DMARC on each
3. Warm up each domain separately
4. Rotate across domains: 25/domain/day × 5 = 125 emails/day
5. Use different "from" names per domain for variety
