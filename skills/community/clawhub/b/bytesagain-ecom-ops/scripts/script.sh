#!/usr/bin/env bash
set -euo pipefail
DATA_DIR="${HOME}/.local/share/bytesagain-ecom-ops"
mkdir -p "$DATA_DIR"
_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
_err() { echo "ERROR: $*" >&2; exit 1; }

cmd_attribution() {
    local channels="" revenue=0
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --channels) channels="$2"; shift 2 ;;
            --revenue)  revenue="$2";  shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$channels" || -z "$revenue" ]] && \
        _err "Usage: attribution --channels 'google:5000,meta:3000,email:500' --revenue 18000"

    python3 - "$channels" "$revenue" << 'PYEOF'
import sys
channels_str, revenue_s = sys.argv[1], sys.argv[2]
revenue = float(revenue_s)

channels = {}
for item in channels_str.split(","):
    parts = item.strip().split(":")
    if len(parts) == 2:
        channels[parts[0].strip()] = float(parts[1].strip())

total_spend = sum(channels.values())
total_roas = revenue / total_spend if total_spend > 0 else 0

print(f"\n{'═'*52}")
print(f"MARKETING ATTRIBUTION ANALYSIS")
print(f"{'═'*52}\n")
print(f"  Total Ad Spend: ${total_spend:,.0f}")
print(f"  Total Revenue:  ${revenue:,.0f}")
print(f"  Blended ROAS:   {total_roas:.2f}x")
print(f"  Blended CPA:    ${total_spend/max(revenue/50,1):,.2f}  (est. ~50 orders)\n")
print(f"  {'Channel':<15} {'Spend':>8} {'Share%':>7} {'Est.Revenue':>12} {'ROAS':>6}")
print(f"  {'─'*50}")

# Simple last-click attribution (proportional to spend)
for ch, spend in sorted(channels.items(), key=lambda x: -x[1]):
    share = spend / total_spend if total_spend > 0 else 0
    est_rev = revenue * share
    roas = est_rev / spend if spend > 0 else 0
    flag = " 🔴" if roas < 2 else " 🟡" if roas < 3 else " 🟢"
    print(f"  {ch:<15} ${spend:>7,.0f} {share*100:>6.0f}% ${est_rev:>10,.0f} {roas:>5.1f}x{flag}")

print(f"\n  ROAS GUIDE: 🔴 <2x (unprofitable) 🟡 2-3x (break-even) 🟢 >3x (profitable)")
print()
print("  RECOMMENDATIONS:")
underperforming = [ch for ch, spend in channels.items() if (revenue * spend/total_spend) / spend < 2]
if underperforming:
    print(f"  → Consider reducing budget: {', '.join(underperforming)}")
top_channel = max(channels.items(), key=lambda x: x[1])[0]
print(f"  → Test incrementality on {top_channel} (holdout test)")
print(f"  → Attribution model: Consider data-driven vs last-click")
print()
print("─"*52)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_roi() {
    local spend=0 revenue=0 cogs_pct=40 platform="shopify"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --spend)     spend="$2";    shift 2 ;;
            --revenue)   revenue="$2";  shift 2 ;;
            --cogs-pct)  cogs_pct="$2"; shift 2 ;;
            --platform)  platform="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$spend" || -z "$revenue" ]] && \
        _err "Usage: roi --spend 8000 --revenue 18000 --cogs-pct 40 --platform shopify"

    python3 - "$spend" "$revenue" "$cogs_pct" "$platform" << 'PYEOF'
import sys
spend, revenue, cogs_pct, platform = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]

# Platform fees
fees = {"shopify": 0.02, "amazon": 0.15, "woocommerce": 0.01, "tiktok": 0.02}
fee_pct = fees.get(platform.lower(), 0.02)

gross_margin = revenue * (1 - cogs_pct/100)
platform_fee = revenue * fee_pct
net_after_fees = gross_margin - platform_fee
contribution = net_after_fees - spend
roas = revenue / spend if spend > 0 else 0
mer = revenue / spend  # Marketing Efficiency Ratio
breakeven_roas = 1 / (1 - cogs_pct/100 - fee_pct)

print(f"\n{'═'*50}")
print(f"AD CAMPAIGN ROI ANALYSIS ({platform.title()})")
print(f"{'═'*50}\n")
print(f"  Revenue:          ${revenue:>10,.2f}")
print(f"  COGS ({cogs_pct:.0f}%):       -${revenue*cogs_pct/100:>9,.2f}")
print(f"  Gross Margin:     ${gross_margin:>10,.2f}  ({100-cogs_pct:.0f}%)")
print(f"  Platform fees:    -${platform_fee:>9,.2f}  ({fee_pct*100:.1f}%)")
print(f"  Ad Spend:         -${spend:>9,.2f}")
print(f"  {'─'*40}")
print(f"  Net Contribution: ${contribution:>10,.2f}")
print()
print(f"  ROAS:             {roas:.2f}x")
print(f"  Breakeven ROAS:   {breakeven_roas:.2f}x")
print(f"  Status:           {'🟢 Profitable' if contribution > 0 else '🔴 Unprofitable'}")
print()
print("  BUDGET RECOMMENDATIONS:")
if roas > breakeven_roas * 1.5:
    print(f"  → Scale: ROAS {roas:.1f}x is well above breakeven ({breakeven_roas:.1f}x)")
    print(f"  → Consider increasing budget by 20–30%")
elif roas > breakeven_roas:
    print(f"  → Maintain: Marginally profitable, optimize creatives")
else:
    print(f"  → Pause or restructure: ROAS below breakeven")
print()
print("─"*50)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_inventory() {
    local product="" stock=0 daily_sales=0 lead_days=14 safety_days=7
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --product)     product="$2";     shift 2 ;;
            --current-stock) stock="$2";    shift 2 ;;
            --daily-sales) daily_sales="$2"; shift 2 ;;
            --lead-days)   lead_days="$2";   shift 2 ;;
            --safety-days) safety_days="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$stock" || -z "$daily_sales" ]] && \
        _err "Usage: inventory --product SKU-001 --current-stock 120 --daily-sales 15 --lead-days 14"

    python3 - "$product" "$stock" "$daily_sales" "$lead_days" "$safety_days" << 'PYEOF'
import sys
from datetime import datetime, timedelta
product, stock, daily, lead, safety = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

days_left = stock / daily if daily > 0 else 999
reorder_point = (daily * lead) + (daily * safety)
reorder_qty = daily * (lead + safety + 30)  # 30 days buffer
stockout_date = datetime.now() + timedelta(days=days_left)

print(f"\n{'═'*50}")
print(f"INVENTORY ANALYSIS: {product or 'Product'}")
print(f"{'═'*50}\n")
print(f"  Current Stock:    {stock:,} units")
print(f"  Daily Sales:      {daily:.1f} units/day")
print(f"  Days of Stock:    {days_left:.0f} days")
print(f"  Est. Stockout:    {stockout_date.strftime('%Y-%m-%d')}")
print()
print(f"  REORDER ANALYSIS:")
print(f"  Lead Time:        {lead} days")
print(f"  Safety Stock:     {daily * safety:.0f} units ({safety} days)")
print(f"  Reorder Point:    {reorder_point:.0f} units")
print(f"  Recommended Qty:  {reorder_qty:.0f} units")
print()
if stock <= reorder_point:
    print(f"  STATUS: 🔴 REORDER NOW — Below reorder point!")
elif stock <= reorder_point * 1.5:
    print(f"  STATUS: 🟡 ORDER SOON — Approaching reorder point")
else:
    print(f"  STATUS: 🟢 OK — Sufficient stock")
print()
print(f"  TURNOVER: {daily*365/stock:.1f}x per year" if stock > 0 else "")
print("─"*50)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_pricing() {
    local cost=0 current_price=0 competitor_price=0 margin_target=60
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --cost)             cost="$2";             shift 2 ;;
            --current-price)    current_price="$2";    shift 2 ;;
            --competitor-price) competitor_price="$2"; shift 2 ;;
            --margin-target)    margin_target="$2";    shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$cost" ]] && _err "Usage: pricing --cost 25 --current-price 79 --competitor-price 69 --margin-target 60"

    python3 - "$cost" "$current_price" "$competitor_price" "$margin_target" << 'PYEOF'
import sys
cost, current, comp, target_margin = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])

current_margin = (current - cost) / current * 100 if current > 0 else 0
target_price = cost / (1 - target_margin/100)
comp_margin = (comp - cost) / comp * 100 if comp > 0 else 0

print(f"\n{'═'*50}")
print(f"PRICING ANALYSIS")
print(f"{'═'*50}\n")
print(f"  Cost:             ${cost:.2f}")
print(f"  Current Price:    ${current:.2f}  (margin: {current_margin:.1f}%)")
print(f"  Competitor Price: ${comp:.2f}  (their margin est: {comp_margin:.1f}%)")
print(f"  Target Margin:    {target_margin:.0f}%")
print()
print(f"  TARGET PRICE:     ${target_price:.2f}")
print()
print("  PRICING STRATEGY OPTIONS:")
if target_price > comp * 1.1:
    print(f"  → Premium pricing at ${target_price:.2f} (+{(target_price/comp-1)*100:.0f}% vs competitor)")
    print(f"    Requires strong differentiation (brand, reviews, features)")
elif target_price < comp * 0.95:
    print(f"  → Competitive pricing at ${target_price:.2f} (-{(1-target_price/comp)*100:.0f}% vs competitor)")
    print(f"    Good for volume; watch margin erosion")
else:
    print(f"  → Market-rate pricing at ${target_price:.2f} (≈ competitor)")
    print(f"    Compete on reviews, bundling, or conversion rate")
print()
print("  QUICK TESTS:")
print(f"  → A/B test: ${current:.2f} vs ${target_price:.2f} for 2 weeks")
print(f"  → Bundle: Add low-cost item to justify higher price point")
print("─"*50)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_cohort() {
    local new=0 m1=0 m3=0 avg_order=0
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --new-customers)    new="$2";       shift 2 ;;
            --month1-retained)  m1="$2";        shift 2 ;;
            --month3-retained)  m3="$2";        shift 2 ;;
            --avg-order)        avg_order="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$new" ]] && _err "Usage: cohort --new-customers 500 --month1-retained 210 --month3-retained 95 --avg-order 85"

    python3 - "$new" "$m1" "$m3" "$avg_order" << 'PYEOF'
import sys
new, m1, m3, aov = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])

r1 = m1/new*100 if new > 0 else 0
r3 = m3/new*100 if new > 0 else 0
ltv_12m = aov * (1 + r1/100 * 2 + r3/100 * 4)  # simplified LTV model

print(f"\n{'═'*50}")
print(f"COHORT RETENTION & LTV ANALYSIS")
print(f"{'═'*50}\n")
print(f"  New Customers:    {new:,}")
print(f"  Month 1 Retained: {m1:,} ({r1:.1f}%)")
print(f"  Month 3 Retained: {m3:,} ({r3:.1f}%)")
print(f"  Avg Order Value:  ${aov:.2f}")
print()
print(f"  Est. 12-Month LTV: ${ltv_12m:.2f}")
print()
print("  BENCHMARKS (e-commerce industry avg):")
print(f"  Month 1 retention: 25–35%  → {'🟢 Above' if r1 > 30 else '🔴 Below'} average ({r1:.1f}%)")
print(f"  Month 3 retention: 10–20%  → {'🟢 Above' if r3 > 15 else '🔴 Below'} average ({r3:.1f}%)")
print()
print("  IMPROVEMENT IDEAS:")
if r1 < 25:
    print("  → Post-purchase email flow (day 3, 7, 14)")
    print("  → First purchase discount for second order")
if r3 < 15:
    print("  → Loyalty program or subscription option")
    print("  → Win-back campaign at day 60–90")
print("─"*50)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_funnel() {
    local visits=0 pdp=0 atc=0 checkout=0 orders=0
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --visits)      visits="$2";   shift 2 ;;
            --pdp-views)   pdp="$2";      shift 2 ;;
            --add-to-cart) atc="$2";      shift 2 ;;
            --checkout)    checkout="$2"; shift 2 ;;
            --orders)      orders="$2";   shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$visits" ]] && _err "Usage: funnel --visits 10000 --pdp-views 3200 --add-to-cart 850 --checkout 320 --orders 280"

    python3 - "$visits" "$pdp" "$atc" "$checkout" "$orders" << 'PYEOF'
import sys
v, pdp, atc, co, orders = [int(x) for x in sys.argv[1:6]]

def pct(a, b): return f"{a/b*100:.1f}%" if b > 0 else "N/A"
def flag(rate, good, ok): return "🟢" if rate >= good else "🟡" if rate >= ok else "🔴"

r_pdp = pdp/v if v > 0 else 0
r_atc = atc/pdp if pdp > 0 else 0
r_co = co/atc if atc > 0 else 0
r_ord = orders/co if co > 0 else 0
cvr = orders/v if v > 0 else 0

print(f"\n{'═'*55}")
print(f"CONVERSION FUNNEL ANALYSIS")
print(f"{'═'*55}\n")
print(f"  Stage              Visitors    Conv Rate   Benchmark")
print(f"  {'─'*53}")
print(f"  Traffic            {v:>8,}    —           —")
print(f"  PDP Views          {pdp:>8,}    {pct(pdp,v):>8}    {flag(r_pdp,0.4,0.25)} (bench: 30–40%)")
print(f"  Add to Cart        {atc:>8,}    {pct(atc,pdp):>8}    {flag(r_atc,0.12,0.07)} (bench: 8–12%)")
print(f"  Checkout Started   {co:>8,}    {pct(co,atc):>8}    {flag(r_co,0.6,0.4)} (bench: 45–65%)")
print(f"  Orders             {orders:>8,}    {pct(orders,co):>8}    {flag(r_ord,0.8,0.6)} (bench: 70–85%)")
print(f"  {'─'*53}")
print(f"  Overall CVR        {'':>8}    {pct(orders,v):>8}    🎯 (bench: 2–4%)")
print()

# Find biggest drop-off
stages = [("Traffic→PDP", r_pdp, 0.3), ("PDP→Cart", r_atc, 0.08),
          ("Cart→Checkout", r_co, 0.5), ("Checkout→Order", r_ord, 0.75)]
worst = min(stages, key=lambda x: x[1]/x[2])
print(f"  BIGGEST OPPORTUNITY: {worst[0]}")
if "PDP" in worst[0]:
    print("  → Improve product images, title, description")
    print("  → Add social proof (reviews, UGC)")
elif "Cart" in worst[0]:
    print("  → Reduce friction: show trust badges, delivery info")
    print("  → Cart abandonment email within 1 hour")
elif "Checkout" in worst[0]:
    print("  → Simplify checkout: reduce fields, add express pay")
    print("  → Show security seals and free return policy")
print("─"*55)
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_help() {
    cat << 'EOF'
Ecom Ops — Optimize e-commerce operations with AI analysis
Powered by BytesAgain | bytesagain.com

Commands:
  attribution  Analyze marketing channel attribution and ROAS
  roi          Calculate ad campaign ROI and budget recommendations
  inventory    Generate reorder recommendations from sales velocity
  pricing      Analyze pricing strategy and suggest optimizations
  cohort       Analyze customer cohort retention and LTV
  funnel       Analyze conversion funnel drop-off points
  help         Show this help

Usage:
  bash scripts/script.sh attribution --channels "google:5000,meta:3000,email:500" --revenue 18000
  bash scripts/script.sh roi --spend 8000 --revenue 18000 --cogs-pct 40 --platform shopify
  bash scripts/script.sh inventory --product "SKU-001" --current-stock 120 --daily-sales 15 --lead-days 14
  bash scripts/script.sh pricing --cost 25 --current-price 79 --competitor-price 69 --margin-target 60
  bash scripts/script.sh cohort --new-customers 500 --month1-retained 210 --month3-retained 95 --avg-order 85
  bash scripts/script.sh funnel --visits 10000 --pdp-views 3200 --add-to-cart 850 --checkout 320 --orders 280

More: https://bytesagain.com/skills | Feedback: https://bytesagain.com/feedback/
EOF
}

case "${1:-help}" in
    attribution) shift; cmd_attribution "$@" ;;
    roi)         shift; cmd_roi "$@" ;;
    inventory)   shift; cmd_inventory "$@" ;;
    pricing)     shift; cmd_pricing "$@" ;;
    cohort)      shift; cmd_cohort "$@" ;;
    funnel)      shift; cmd_funnel "$@" ;;
    help|*)      cmd_help ;;
esac
