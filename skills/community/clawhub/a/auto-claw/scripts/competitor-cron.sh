#!/bin/bash
# Competitor Monitoring Cron — Auto-Claw
# Runs daily at 8:05 UTC to check competitor sites and alert on changes
# Add to crontab: 5 8 * * * cd /path/to/auto-claw && bash scripts/competitor-cron.sh >> logs/competitor-cron.log 2>&1

SITE="http://linghangyuan1234.dpdns.org"
AUTO_CLAW_DIR="/root/.openclaw/workspace/auto-company/projects/auto-claw"
LOG_DIR="$AUTO_CLAW_DIR/logs"

mkdir -p "$LOG_DIR"

echo "[$(date -u '+%Y-%m-%d %H:%M UTC')] Running competitor monitoring..."
cd "$AUTO_CLAW_DIR" || exit 1

# Activate venv if exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

# Run competitor monitoring on Auto-Claw's actual competitors
python3 -c "
import sys
sys.path.insert(0, 'src')
from competitor_monitor import CompetitorMonitor

monitor = CompetitorMonitor(
    our_url='http://linghangyuan1234.dpdns.org',
    our_price='\$99-799/mo'
)

# Auto-Claw's real competitors in the WordPress AI operations space
competitors = [
    ('Shopify', 'https://www.shopify.com'),
    ('WooCommerce', 'https://woocommerce.com'),
    ('BigCommerce', 'https://www.bigcommerce.com'),
    ('ManageWP', 'https://managewp.com'),
]

print('Checking competitors...')
for name, url in competitors:
    try:
        monitor.add_competitor(name, url)
        data = monitor.fetch_competitor(name)
        # Check if site is accessible
        http_status = getattr(data, 'http_status', 0)
        title = getattr(data, 'title', '')[:50]
        print(f'  {name} [{http_status}]: {title}')
        if hasattr(data, 'has_pricing') and data.has_pricing:
            print(f'    💰 Pricing detected')
        if http_status == 200 and title:
            print(f'    ✅ Live')
        elif http_status > 0:
            print(f'    ⚠️  Status {http_status}')
        else:
            print(f'    ❌ Unreachable')
    except Exception as e:
        print(f'  {name}: ERROR - {e}')

print('Done.')
" 2>&1 | tee -a "$LOG_DIR/competitor-cron.log"

echo "[$(date -u '+%Y-%m-%d %H:%M UTC')] Competitor monitoring complete."
