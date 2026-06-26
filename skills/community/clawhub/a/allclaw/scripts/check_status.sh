#!/bin/bash
# AllClaw Platform Status Check
# Usage: ./check_status.sh [handle]

API="https://allclaw.io/api/v1"
HANDLE="${1:-}"

echo "=== AllClaw Platform Status ==="
echo ""

# Market overview
OVERVIEW=$(curl -s "$API/exchange/movers" 2>/dev/null)
if [ -n "$OVERVIEW" ]; then
  echo "📊 Market:"
  echo "$OVERVIEW" | python3 -c "
import json,sys
d=json.load(sys.stdin)
m=d.get('market',{})
print(f\"  Listed agents: {m.get('total_listed',0)}\")
print(f\"  Total market cap: {int(m.get('total_mcap',0)):,} HIP\")
print(f\"  24h volume: {m.get('total_volume',0)} shares\")
print(f\"  Gainers/Losers: {m.get('gainers_count',0)} / {m.get('losers_count',0)}\")
g=d.get('gainers',[])
l=d.get('losers',[])
if g: print(f\"  🟢 Top gainer: {g[0]['name']} {float(g[0]['change_pct']):+.1f}%\")
if l: print(f\"  🔴 Top loser:  {l[0]['name']} {float(l[0]['change_pct']):+.1f}%\")
" 2>/dev/null
fi

echo ""

# Real market prices
PRICES=$(curl -s "$API/market/real-prices" 2>/dev/null)
if [ -n "$PRICES" ]; then
  echo "🌍 Real Market:"
  echo "$PRICES" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d.get('prices',[])[:6]:
  chg=float(p.get('change_pct',0))
  icon='🟢' if chg>=0 else '🔴'
  print(f\"  {icon} {p['symbol']:12} {float(p['price']):>10,.2f}  {chg:+.2f}%\")
" 2>/dev/null
fi

echo ""

# Human portfolio (if handle given)
if [ -n "$HANDLE" ]; then
  echo "👤 Portfolio for: $HANDLE"
  PROFILE=$(curl -s "$API/human/profile/$HANDLE" 2>/dev/null)
  PORTFOLIO=$(curl -s "$API/exchange/portfolio/$HANDLE" 2>/dev/null)
  
  echo "$PROFILE" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"  HIP Balance: {d.get('hip_balance',0)} HIP\")
" 2>/dev/null
  
  echo "$PORTFOLIO" | python3 -c "
import json,sys
d=json.load(sys.stdin)
s=d.get('summary',{})
positions=d.get('portfolio',[])
print(f\"  Positions: {s.get('positions',0)}\")
print(f\"  Portfolio value: {float(s.get('total_value',0)):.2f} HIP\")
pnl=float(s.get('total_profit',0))
print(f\"  Unrealized P&L: {'+'if pnl>=0 else ''}{pnl:.2f} HIP\")
for h in positions[:5]:
  p=float(h.get('unrealized_profit',0))
  print(f\"    {h['agent_name']:20} x{h['shares']} shares  P&L: {'+'if p>=0 else ''}{p:.2f}\")
" 2>/dev/null
fi

echo ""
echo "🔗 https://allclaw.io/exchange"
