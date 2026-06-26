# Email Deliverability Guide

## Domain Setup (Required)

### SPF Record
Add to DNS TXT: `v=spf1 include:_spf.resend.com ~all`

### DKIM
Follow your provider's DKIM setup (Resend auto-generates DKIM records).

### DMARC
Add DNS TXT: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`

## Warmup Schedule

New domains MUST be warmed up:
- **Days 1-3**: 5 emails/day
- **Days 4-7**: 10 emails/day
- **Days 8-14**: 15 emails/day
- **Days 15-21**: 20 emails/day
- **Day 22+**: 25 emails/day (cruising speed)

## Inbox Placement Tips

- Keep emails under 150 words
- No images in cold emails (triggers spam filters)
- No links in first email (or max 1 link)
- Personalize subject and first line
- Avoid spam trigger words: "free", "guarantee", "act now", "limited time"
- Plain text outperforms HTML for cold outreach
- Reply-to should match from address
- Include 1-2 sentence footer with physical address

## Bounce Management

- **Hard bounce**: Remove immediately, never email again
- **Soft bounce**: Retry once after 48 hours, then remove
- **Bounce rate >2%**: Pause and clean your list

## Monitoring

- Track open rates (target: 40-60%)
- Track reply rates (target: 5-15%)
- Track bounce rates (target: <2%)
- If open rate drops below 20%, check deliverability
