# Competitor Change Monitor - API & Configuration Guide

## Configuration File

Create a `competitors.json` file to configure which competitors to monitor:

```json
{
  "competitors": [
    {
      "name": "Stripe",
      "url": "https://stripe.com",
      "category": "payment"
    },
    {
      "name": "Square",
      "url": "https://square.com",
      "category": "payment"
    },
    {
      "name": "PayPal",
      "url": "https://paypal.com",
      "category": "payment"
    }
  ],
  "alerts": {
    "pricing_change": true,
    "new_product": true,
    "content_update": true,
    "messaging_shift": true,
    "minimum_change_score": 0.3
  },
  "reports": {
    "daily_alert": true,
    "weekly_digest": "Monday 9am",
    "monthly_strategic": "1st of month",
    "timezone": "America/New_York"
  }
}
```

## Running the Monitor

### One-time snapshot
```bash
node scripts/monitor.js monitor
```

Fetches all competitors, creates snapshots, detects any changes from last run.

### Generate latest report
```bash
node scripts/monitor.js report
```

Creates a report from the latest snapshots of all competitors.

### Continuous monitoring (cron)
```bash
# Add to crontab for daily monitoring
0 9 * * * cd /path/to/skill && node scripts/monitor.js monitor >> logs/monitor.log 2>&1

# Weekly report (every Monday at 9am)
0 9 * * 1 cd /path/to/skill && node scripts/monitor.js report >> logs/report.log 2>&1
```

## Output Files

### Snapshots
Saved to `snapshots/` directory:
```
snapshots/
├── stripe-1725401200000.json
├── square-1725401200000.json
└── paypal-1725401200000.json
```

Each snapshot contains:
- Website title
- Main headings detected
- Current pricing
- Content hash (for change detection)
- Timestamp

### Reports
Saved to `reports/` directory:
```
reports/
└── report-1725401200000.json
```

Report structure:
```json
{
  "timestamp": "2026-05-09T10:00:00Z",
  "competitors": [
    {
      "name": "Stripe",
      "url": "https://stripe.com",
      "lastSnapshot": "2026-05-09T10:00:00Z",
      "changes": [
        {
          "type": "pricing_change",
          "severity": "high",
          "description": "New tier added: Enterprise at $999/mo"
        }
      ],
      "currentPricing": ["$29", "$99", "$999"],
      "contentSize": 450000
    }
  ],
  "summary": ["Stripe: 1 change detected", "Square: 0 changes"]
}
```

## Integration Options

### Email alerts
```bash
# Send report via email
node scripts/monitor.js report | mail -s "Weekly Competitive Report" team@company.com
```

### Slack integration
```bash
# Send report to Slack channel
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d @report-latest.json
```

### Database storage
```bash
# Store reports in MongoDB
mongoimport --db competitors --collection reports reports/report-*.json
```

## Customization

### Change Detection Tuning

Adjust `minimum_change_score` to filter noise:
- `0.1` = Very sensitive (lots of alerts)
- `0.3` = Standard (recommended)
- `0.7` = Conservative (only major changes)

### Alert Types

Enable/disable specific alerts:
```json
{
  "alerts": {
    "pricing_change": true,      // Alert on any price updates
    "new_product": true,         // Alert on new features
    "content_update": true,      // Alert on page changes
    "messaging_shift": true      // Alert on copy changes
  }
}
```

### Custom Webhooks

Implement custom alert handlers:
```javascript
// hooks/on-pricing-change.js
module.exports = async (change, competitor) => {
  // Send to your service
  await fetch('https://your-api.com/alerts', {
    method: 'POST',
    body: JSON.stringify({ change, competitor })
  });
};
```

## Troubleshooting

### Website not fetching
- Check URL is correct
- Verify website is accessible
- Check firewall/proxy settings
- Some websites block automated requests (use proxy service)

### No changes detected
- Check `minimum_change_score` isn't too high
- Verify snapshots are being created
- Manual verification: visit website, check for changes

### Reports not sending
- Verify email/Slack credentials
- Check logs for errors
- Test integration separately

## Support

For issues, feature requests, or custom configurations:
- Visit GitHub: https://github.com/yourusername/competitor-change-monitor
- Email: support@clawhub.ai
- Discord: https://discord.gg/clawhub
