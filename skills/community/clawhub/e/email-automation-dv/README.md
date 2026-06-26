# Email Automation

Programmatic email sequence deployment for digital product launches via ConvertKit and Mailchimp.

## Description

Email Automation provides tools for building, deploying, and monitoring email sequences for product launches, welcome flows, and nurture campaigns. It integrates with ConvertKit (primary) and Mailchimp (fallback) to create sequences programmatically, add subscribers, and track delivery/open/click rates. Designed for automated deployment of marketing campaigns without manual platform work.

## Key Features

- **Programmatic sequence creation** - Build email sequences via API (no manual platform work)
- **Multi-platform support** - ConvertKit (primary) and Mailchimp (fallback)
- **Template library** - Welcome sequences, launch sequences, nurture campaigns
- **Subscriber management** - Add/remove subscribers via API
- **Performance monitoring** - Track delivery, open, and click rates
- **Delay scheduling** - Configure time delays between emails (e.g., day 0, 3, 7)
- **Content integration** - Works with content pipeline for automated copy deployment

## Quick Start

```bash
# Set API credentials
export CONVERTKIT_API_SECRET="your_api_secret"
export MAILCHIMP_API_KEY="your_api_key"

# Create welcome sequence
bash scripts/create-sequence.sh \
  --type welcome \
  --product "AI Tax Optimizer" \
  --emails 3 \
  --delay-days "0,3,7"

# Deploy launch sequence
bash scripts/deploy-launch.sh \
  --product "Trading Signals" \
  --list "launch_subscribers" \
  --sequence-id 12345

# Monitor performance
python3 scripts/monitor_sequences.py \
  --sequence-id 12345 \
  --output metrics.json
```

**Sequence types:**
- **Welcome** - New subscriber onboarding (3-5 emails)
- **Launch** - Product release announcement (4-7 emails)
- **Nurture** - Lead warming and education (5-10 emails)

## API Integration

**ConvertKit (Primary):**
- Create sequences, add subscribers, get stats
- Rate limit: 120 req/min
- Authentication: API secret

**Mailchimp (Fallback):**
- Create automations, manage lists, campaign reports
- Rate limit: 10 req/sec
- Authentication: API key

## What It Does NOT Do

- Does NOT write email copy (provide content as input)
- Does NOT handle ESP account setup (requires existing ConvertKit/Mailchimp account)
- Does NOT manage contact hygiene or list cleaning
- Does NOT provide A/B testing or advanced segmentation
- Does NOT replace full marketing automation platforms (basic sequence deployment only)

## Requirements

- Python 3.8+
- requests library
- ConvertKit or Mailchimp account with API access
- API credentials set as environment variables

## License

MIT
