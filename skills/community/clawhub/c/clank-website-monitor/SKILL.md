---
name: website-monitor
description: Monitor websites for changes, new content, and price alerts. Perfect for tracking competitors, job postings, or product prices.
metadata:
  openclaw:
    emoji: "👁️"
---

# Website Monitor Skill

Monitor websites for changes and get alerts when something happens.

## Features

- **Change Detection** – Track content changes on any website
- **Price Tracking** – Monitor product prices and get alerts
- **New Content** – Detect new articles, posts, or listings
- **Screenshot Comparison** – Visual diff of page changes
- **Cron Integration** – Automatic periodic checks

## Usage

### Add a website to monitor
```
website-monitor add "https://example.com/jobs" --name "Job Board" --selector ".job-listing"
```

### Check for changes
```
website-monitor check
```

### View change history
```
website-monitor history --last 7d
```

## Use Cases

### For Businesses
- Monitor competitor pricing changes
- Track industry news and blog posts
- Watch for new job postings
- Monitor customer review sites

### For Individuals
- Track product prices on e-commerce sites
- Monitor event ticket availability
- Watch for new apartment/car listings
- Track social media mentions

## Implementation

This skill uses `curl` + `diff` for simple monitoring:

```bash
#!/bin/bash
# Save current state
curl -s "$URL" | md5sum > "$STATE_FILE"

# Compare with previous
if ! diff "$STATE_FILE" "$STATE_FILE.prev" > /dev/null 2>&1; then
    echo "CHANGE DETECTED!"
    # Send alert via OpenClaw
fi
```

## Requirements

- curl
- md5sum
- OpenClaw (for notifications)

## License

MIT
