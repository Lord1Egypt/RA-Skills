# Web Monitor Examples

## Example 1: Track Product Price

```bash
# Monitor Mac Mini price on Apple Store
python scripts/monitor.py \
  --url "https://www.apple.com/shop/buy-mac/mac-mini" \
  --selector ".price" \
  --output mac-mini-current.json \
  --compare mac-mini-previous.json \
  --notify "telegram-send 'Mac Mini price changed!'"
```

## Example 2: Job Posting Monitor

```bash
# Check a job board daily
python scripts/monitor.py \
  --url "https://jobs.example.com/engineer" \
  --selector ".job-listing" \
  --output jobs.json \
  --compare jobs.json \
  --interval 86400 \
  --notify "echo 'New jobs posted!'"
```

## Example 3: Continuous Watch Mode

```bash
# Watch for product availability
python scripts/monitor.py \
  --url "https://store.example.com/product/123" \
  --selector ".availability" \
  --watch \
  --interval 300 \
  --notify "telegram-send 'Product is now available!'"
```

## Example 4: Price History Tracking

```bash
# Run as cron job (every 6 hours)
# 0 */6 * * * cd /path/to/web-monitor && python scripts/monitor.py --url X --selector .price --output /var/lib/price-history/$(date +\%Y\%m\%d-\%H\%M).json
```

## Selector Tips

- Use browser DevTools to find stable selectors
- Prefer class names, IDs, or data attributes
- Avoid deeply nested selectors
- Test selectors with: `python -c "from bs4 import BeautifulSoup; import requests; r=requests.get('URL'); print(BeautifulSoup(r.text).select_one('SELECTOR').get_text())"`

## Notification Commands

### Telegram (using telegram-send)
```bash
pip install telegram-send
telegram-send "Page changed!"
```

### Webhook
```bash
curl -X POST "https://hooks.slack.com/services/XXX" -d "{\"text\":\"Change detected\"}"
```

### Email (using msmtp)
```bash
echo "Change detected" | mail -s "Web Monitor Alert" user@example.com
```
