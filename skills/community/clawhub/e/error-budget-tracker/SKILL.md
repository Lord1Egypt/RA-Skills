---
name: error-budget-tracker
description: Track SLO error budgets across services. Calculate remaining budget from SLI metrics, alert on budget burn rate, recommend development vs reliability investment, and generate error budget reports for stakeholder review.
---

# Error Budget Tracker

Make SLOs actionable. Track error budget consumption across services, calculate burn rates, predict when budgets will exhaust, and provide clear guidance on whether to ship features or invest in reliability — turning abstract availability targets into concrete engineering decisions.

Use when: "track error budget", "SLO status", "how much error budget is left", "should we freeze deploys", "reliability vs velocity", "SLI/SLO review", or during service review meetings.

## Commands

### 1. `track` — Calculate Current Error Budget

#### Step 1: Define SLOs

```yaml
# SLO definitions (store in repo as slo.yaml)
services:
  api-gateway:
    slos:
      - name: Availability
        target: 99.9%          # 43.8 min/month downtime budget
        sli: "1 - (sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m])))"
        window: 30d             # Rolling 30-day window
      - name: Latency P99
        target: 99%             # 99% of requests under 500ms
        sli: "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) < 0.5"
        window: 30d
  payment-service:
    slos:
      - name: Availability
        target: 99.95%         # 21.9 min/month downtime budget
        sli: "..."
```

#### Step 2: Query Current SLI Values

```bash
# Prometheus — current availability over rolling window
curl -s "$PROMETHEUS_URL/api/v1/query" --data-urlencode \
  "query=1 - (sum(increase(http_requests_total{service='api-gateway',status=~'5..'}[30d])) / sum(increase(http_requests_total{service='api-gateway'}[30d])))" | \
  python3 -c "
import json, sys
result = json.load(sys.stdin)
if result['data']['result']:
    sli = float(result['data']['result'][0]['value'][1])
    slo = 0.999
    budget_total = 1 - slo  # 0.001 = 0.1%
    budget_consumed = max(0, slo - sli) / budget_total * 100 if sli < slo else 0
    budget_remaining = max(0, 100 - budget_consumed)
    
    print(f'SLI (30d): {sli*100:.3f}%')
    print(f'SLO target: {slo*100:.1f}%')
    print(f'Error budget: {budget_remaining:.1f}% remaining')
    
    # Convert to minutes
    minutes_total = 30 * 24 * 60 * (1 - slo)  # 43.2 min for 99.9%
    minutes_used = minutes_total * (budget_consumed / 100)
    minutes_left = minutes_total - minutes_used
    print(f'Budget in minutes: {minutes_left:.1f} min remaining of {minutes_total:.1f} min')
    
    status = '🟢' if budget_remaining > 50 else '🟡' if budget_remaining > 20 else '🔴'
    print(f'Status: {status}')
"
```

#### Step 3: Calculate Burn Rate

```python
def calculate_burn_rate(budget_consumed_pct, days_elapsed, window_days=30):
    """How fast is the error budget being consumed?"""
    daily_burn = budget_consumed_pct / max(days_elapsed, 1)
    days_remaining = (100 - budget_consumed_pct) / daily_burn if daily_burn > 0 else float('inf')
    
    # Burn rate relative to expected (even burn = 1.0)
    expected_daily = 100 / window_days
    burn_rate = daily_burn / expected_daily
    
    return {
        'daily_burn_pct': daily_burn,
        'burn_rate': burn_rate,  # 1.0 = on track, >1 = burning fast
        'days_until_exhaustion': days_remaining,
        'alert': 'CRITICAL' if burn_rate > 10 else 'HIGH' if burn_rate > 5 else 'WARNING' if burn_rate > 2 else 'OK'
    }
```

#### Step 4: Generate Report

```markdown
# Error Budget Report — April 2026

## Executive Summary
- 3/5 services within budget ✅
- 1 service approaching exhaustion ⚠️
- 1 service budget exhausted 🔴 — deploy freeze recommended

## Service Status
| Service | SLO | SLI (30d) | Budget Left | Burn Rate | Action |
|---------|-----|-----------|-------------|-----------|--------|
| api-gateway | 99.9% | 99.92% | 78% 🟢 | 0.7× | Ship features |
| payment | 99.95% | 99.94% | 35% 🟡 | 1.3× | Caution |
| search | 99.5% | 99.48% | 12% 🔴 | 2.8× | Reliability sprint |
| auth | 99.99% | 99.995% | 95% 🟢 | 0.2× | Ship features |
| notifications | 99.9% | 99.85% | -50% 🔴 | 3.5× | Deploy freeze |

## Recommendations
### notifications (BUDGET EXHAUSTED)
- Freeze non-critical deploys until budget recovers
- Dedicate 1 engineer to reliability for 2 weeks
- Root cause: 3 incidents on Apr 12, 18, 23 consumed 150% of budget
- Projected recovery: 12 days if no further incidents

### search (LOW BUDGET)
- Defer risky refactors until next month
- Current burn rate exhausts budget in 4 days
- Root cause: elevated latency from new search index migration
```

### 2. `alert` — Set Up Budget Burn Alerts

Generate multi-window burn rate alerts (Google SRE book approach):
- 2% budget consumed in 1 hour → page (14.4× burn rate)
- 5% budget consumed in 6 hours → page (6× burn rate)
- 10% budget consumed in 3 days → ticket (1× burn rate)

### 3. `policy` — Generate Error Budget Policy

Create a formal error budget policy document:
- What happens at each budget threshold (100%, 75%, 50%, 25%, 0%)
- Who has authority to freeze deploys
- How to request budget exceptions
- How budget resets (rolling window vs calendar month)
- How to adjust SLOs based on historical data
