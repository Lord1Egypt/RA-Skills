#!/usr/bin/env bash
# Compound — Compound Interest Calculator
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

DATA_DIR="$HOME/.compound"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"
VERSION="1.0.0"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" << 'EOF'
{"default_frequency": "monthly", "currency_symbol": "$", "decimal_places": 2}
EOF
fi

COMMAND="${1:-help}"

case "$COMMAND" in
  calculate)
    python3 << 'PYEOF'
import os, json, uuid, sys, math
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
rate = os.environ.get("RATE", "")
years = os.environ.get("YEARS", "")
frequency = os.environ.get("FREQUENCY", "monthly")
contribution = float(os.environ.get("CONTRIBUTION", "0"))
contrib_freq = os.environ.get("CONTRIB_FREQ", "monthly")

try:
    with open(config_file) as f:
        cfg = json.load(f)
    if "FREQUENCY" not in os.environ:
        frequency = cfg.get("default_frequency", "monthly")
    symbol = cfg.get("currency_symbol", "$")
    dp = cfg.get("decimal_places", 2)
except:
    symbol = "$"
    dp = 2

if not principal or not rate or not years:
    print("ERROR: PRINCIPAL, RATE, and YEARS environment variables are required")
    print("Usage: PRINCIPAL=10000 RATE=7.5 YEARS=20 bash scripts/script.sh calculate")
    sys.exit(1)

principal = float(principal)
rate = float(rate) / 100
years = float(years)

freq_map = {"daily": 365, "monthly": 12, "quarterly": 4, "annually": 1}
n = freq_map.get(frequency, 12)

contrib_freq_map = {"monthly": 12, "quarterly": 4, "annually": 1}
cn = contrib_freq_map.get(contrib_freq, 12)

# Compound interest: A = P(1 + r/n)^(nt)
total_periods = int(n * years)
rate_per_period = rate / n

if contribution > 0:
    # With regular contributions
    balance = principal
    total_contributions = principal
    contrib_period_ratio = n / cn  # how many compound periods per contribution
    for period in range(1, total_periods + 1):
        balance *= (1 + rate_per_period)
        if period % int(contrib_period_ratio) == 0:
            balance += contribution
            total_contributions += contribution
    final_amount = balance
else:
    final_amount = principal * (1 + rate_per_period) ** total_periods
    total_contributions = principal

interest_earned = final_amount - total_contributions
growth_pct = ((final_amount / principal) - 1) * 100

print(f"Compound Interest Calculation")
print(f"{'='*50}")
print(f"Principal:          {symbol}{principal:>14,.{dp}f}")
print(f"Annual Rate:        {rate*100:>14.2f}%")
print(f"Time Period:        {years:>14.1f} years")
print(f"Compounding:        {frequency:>14}")
if contribution > 0:
    print(f"Contribution:       {symbol}{contribution:>14,.{dp}f} ({contrib_freq})")
    print(f"Total Contributed:  {symbol}{total_contributions:>14,.{dp}f}")
print(f"{'='*50}")
print(f"Final Amount:       {symbol}{final_amount:>14,.{dp}f}")
print(f"Interest Earned:    {symbol}{interest_earned:>14,.{dp}f}")
print(f"Growth:             {growth_pct:>14.2f}%")

# Save to history
calc_id = uuid.uuid4().hex[:12]
record = {
    "id": calc_id,
    "timestamp": datetime.now().isoformat(),
    "type": "calculate",
    "params": {
        "principal": principal,
        "rate": rate * 100,
        "years": years,
        "frequency": frequency,
        "contribution": contribution,
        "contrib_freq": contrib_freq
    },
    "result": {
        "final_amount": round(final_amount, dp),
        "interest_earned": round(interest_earned, dp),
        "total_contributions": round(total_contributions, dp),
        "growth_pct": round(growth_pct, 2)
    }
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(f"\nCalculation ID: {calc_id}")
PYEOF
    ;;

  compare)
    python3 << 'PYEOF'
import os, json, uuid, sys
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
rates_str = os.environ.get("RATES", "")
years = os.environ.get("YEARS", "")
frequency = os.environ.get("FREQUENCY", "monthly")

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
    dp = cfg.get("decimal_places", 2)
except:
    symbol = "$"
    dp = 2

if not principal or not rates_str or not years:
    print("ERROR: PRINCIPAL, RATES, and YEARS are required")
    print("Usage: PRINCIPAL=10000 RATES='3,5,7,10' YEARS=20 bash scripts/script.sh compare")
    sys.exit(1)

principal = float(principal)
rates = [float(r.strip()) for r in rates_str.split(",")]
years = float(years)

freq_map = {"daily": 365, "monthly": 12, "quarterly": 4, "annually": 1}
n = freq_map.get(frequency, 12)

print(f"Rate Comparison — {symbol}{principal:,.{dp}f} over {years:.0f} years ({frequency} compounding)")
print(f"{'='*70}")
print(f"{'Rate':>8} {'Final Amount':>16} {'Interest':>16} {'Growth':>10}")
print(f"{'-'*70}")

results = []
for rate in rates:
    r = rate / 100
    final = principal * (1 + r / n) ** (n * years)
    interest = final - principal
    growth = ((final / principal) - 1) * 100
    print(f"{rate:>7.2f}% {symbol}{final:>15,.{dp}f} {symbol}{interest:>15,.{dp}f} {growth:>9.2f}%")
    results.append({"rate": rate, "final": round(final, dp), "interest": round(interest, dp), "growth": round(growth, 2)})

if len(rates) >= 2:
    diff = results[-1]["final"] - results[0]["final"]
    print(f"\nDifference between {rates[0]}% and {rates[-1]}%: {symbol}{diff:,.{dp}f}")

calc_id = uuid.uuid4().hex[:12]
record = {
    "id": calc_id,
    "timestamp": datetime.now().isoformat(),
    "type": "compare",
    "params": {"principal": principal, "rates": rates, "years": years, "frequency": frequency},
    "result": {"comparisons": results}
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
    ;;

  schedule)
    python3 << 'PYEOF'
import os, json, uuid, sys
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
rate = os.environ.get("RATE", "")
years = os.environ.get("YEARS", "")
frequency = os.environ.get("FREQUENCY", "monthly")
contribution = float(os.environ.get("CONTRIBUTION", "0"))

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
    dp = cfg.get("decimal_places", 2)
except:
    symbol = "$"
    dp = 2

if not principal or not rate or not years:
    print("ERROR: PRINCIPAL, RATE, and YEARS are required")
    sys.exit(1)

principal = float(principal)
rate = float(rate) / 100
years = float(years)

freq_map = {"daily": 365, "monthly": 12, "quarterly": 4, "annually": 1}
n = freq_map.get(frequency, 12)
total_periods = int(n * years)
rate_per_period = rate / n

period_names = {"daily": "Day", "monthly": "Month", "quarterly": "Quarter", "annually": "Year"}
pname = period_names.get(frequency, "Period")

# Limit display for daily
show_every = 1
if frequency == "daily" and total_periods > 100:
    show_every = 30
    print(f"(Showing every 30 days for readability)")

print(f"Growth Schedule — {symbol}{principal:,.{dp}f} at {rate*100:.2f}% ({frequency})")
if contribution > 0:
    print(f"Regular contribution: {symbol}{contribution:,.{dp}f}")
print(f"{'='*70}")
print(f"{'Period':>8} {'Balance':>16} {'Interest':>14} {'Cumul. Interest':>16}")
print(f"{'-'*70}")

balance = principal
cumulative_interest = 0
schedule_data = []

for period in range(1, total_periods + 1):
    interest = balance * rate_per_period
    balance += interest
    if contribution > 0:
        balance += contribution
    cumulative_interest += interest

    entry = {"period": period, "balance": round(balance, dp), "interest": round(interest, dp), "cumulative": round(cumulative_interest, dp)}
    schedule_data.append(entry)

    if period % show_every == 0 or period == total_periods:
        print(f"{period:>8} {symbol}{balance:>15,.{dp}f} {symbol}{interest:>13,.{dp}f} {symbol}{cumulative_interest:>15,.{dp}f}")

print(f"\nFinal balance: {symbol}{balance:,.{dp}f}")
print(f"Total interest earned: {symbol}{cumulative_interest:,.{dp}f}")

calc_id = uuid.uuid4().hex[:12]
record = {
    "id": calc_id,
    "timestamp": datetime.now().isoformat(),
    "type": "schedule",
    "params": {"principal": principal * (100 / (rate * 100 + 100)), "rate": rate * 100, "years": years, "frequency": frequency, "contribution": contribution},
    "result": {"final_balance": round(balance, dp), "total_interest": round(cumulative_interest, dp), "periods": total_periods}
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
    ;;

  table)
    python3 << 'PYEOF'
import os, json, uuid, sys
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
rate = os.environ.get("RATE", "")
years = os.environ.get("YEARS", "")
contribution = float(os.environ.get("CONTRIBUTION", "0"))

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
    dp = cfg.get("decimal_places", 2)
except:
    symbol = "$"
    dp = 2

if not principal or not rate or not years:
    print("ERROR: PRINCIPAL, RATE, and YEARS are required")
    sys.exit(1)

principal = float(principal)
r = float(rate) / 100
years = int(float(years))

print(f"Year-by-Year Growth Table")
print(f"Principal: {symbol}{principal:,.{dp}f} | Rate: {float(rate):.2f}% | Contributions: {symbol}{contribution:,.{dp}f}/yr")
print(f"{'='*75}")
print(f"{'Year':>5} {'Start Balance':>16} {'Interest':>14} {'Contribution':>14} {'End Balance':>16}")
print(f"{'-'*75}")

balance = principal
total_interest = 0
total_contrib = 0

for year in range(1, years + 1):
    start = balance
    interest = balance * r
    balance += interest + contribution
    total_interest += interest
    total_contrib += contribution
    print(f"{year:>5} {symbol}{start:>15,.{dp}f} {symbol}{interest:>13,.{dp}f} {symbol}{contribution:>13,.{dp}f} {symbol}{balance:>15,.{dp}f}")

print(f"{'='*75}")
print(f"{'Total':>5} {'':>16} {symbol}{total_interest:>13,.{dp}f} {symbol}{total_contrib:>13,.{dp}f} {symbol}{balance:>15,.{dp}f}")
PYEOF
    ;;

  rate)
    python3 << 'PYEOF'
import os, json, uuid, sys, math
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
target = os.environ.get("TARGET", "")
years = os.environ.get("YEARS", "")
frequency = os.environ.get("FREQUENCY", "monthly")

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
except:
    symbol = "$"

if not principal or not target or not years:
    print("ERROR: PRINCIPAL, TARGET, and YEARS are required")
    sys.exit(1)

principal = float(principal)
target = float(target)
years = float(years)

freq_map = {"daily": 365, "monthly": 12, "quarterly": 4, "annually": 1}
n = freq_map.get(frequency, 12)

# r = n * ((target/principal)^(1/(n*t)) - 1)
required_rate = n * (math.pow(target / principal, 1 / (n * years)) - 1)
required_pct = required_rate * 100

print(f"Required Rate Calculation")
print(f"{'='*50}")
print(f"Starting amount:  {symbol}{principal:>14,.2f}")
print(f"Target amount:    {symbol}{target:>14,.2f}")
print(f"Time period:      {years:>14.1f} years")
print(f"Compounding:      {frequency:>14}")
print(f"{'='*50}")
print(f"Required rate:    {required_pct:>14.4f}%")
print(f"\nYou need an annual rate of {required_pct:.4f}% to grow")
print(f"{symbol}{principal:,.2f} to {symbol}{target:,.2f} in {years:.0f} years.")

calc_id = uuid.uuid4().hex[:12]
record = {
    "id": calc_id,
    "timestamp": datetime.now().isoformat(),
    "type": "rate",
    "params": {"principal": principal, "target": target, "years": years, "frequency": frequency},
    "result": {"required_rate": round(required_pct, 4)}
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
    ;;

  goal)
    python3 << 'PYEOF'
import os, json, uuid, sys, math
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
target = os.environ.get("TARGET", "")
rate = os.environ.get("RATE", "")
contribution = float(os.environ.get("CONTRIBUTION", "0"))

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
except:
    symbol = "$"

if not principal or not target or not rate:
    print("ERROR: PRINCIPAL, TARGET, and RATE are required")
    sys.exit(1)

principal = float(principal)
target = float(target)
rate = float(rate) / 100

if rate <= 0:
    print("ERROR: Rate must be positive")
    sys.exit(1)

if contribution > 0:
    # Simulate month by month
    balance = principal
    months = 0
    while balance < target and months < 12000:
        balance += balance * (rate / 12)
        balance += contribution
        months += 1
    years = months / 12
else:
    # t = ln(target/principal) / (n * ln(1 + r/n))
    n = 12
    years = math.log(target / principal) / (n * math.log(1 + rate / n))

years_int = int(years)
months_remaining = int((years - years_int) * 12)

print(f"Goal Calculation")
print(f"{'='*50}")
print(f"Starting amount:  {symbol}{principal:>14,.2f}")
print(f"Goal amount:      {symbol}{target:>14,.2f}")
print(f"Annual rate:      {rate*100:>14.2f}%")
if contribution > 0:
    print(f"Monthly contrib:  {symbol}{contribution:>14,.2f}")
print(f"{'='*50}")
print(f"Time to goal:     {years_int} years, {months_remaining} months")
print(f"                  ({years:.2f} years total)")

calc_id = uuid.uuid4().hex[:12]
record = {
    "id": calc_id,
    "timestamp": datetime.now().isoformat(),
    "type": "goal",
    "params": {"principal": principal, "target": target, "rate": rate * 100, "contribution": contribution},
    "result": {"years": round(years, 2), "years_int": years_int, "months_remaining": months_remaining}
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
    ;;

  chart)
    python3 << 'PYEOF'
import os, json, sys

config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))

principal = os.environ.get("PRINCIPAL", "")
rate = os.environ.get("RATE", "")
years = os.environ.get("YEARS", "")
width = int(os.environ.get("WIDTH", "60"))
height = int(os.environ.get("HEIGHT", "20"))

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
except:
    symbol = "$"

if not principal or not rate or not years:
    print("ERROR: PRINCIPAL, RATE, and YEARS are required")
    sys.exit(1)

principal = float(principal)
r = float(rate) / 100
years = int(float(years))

# Calculate yearly values
values = [principal]
balance = principal
for y in range(1, years + 1):
    balance *= (1 + r)
    values.append(balance)

# Also track principal-only line
principal_line = [principal * (y + 1) / 1 for y in range(years + 1)]

max_val = max(values)
min_val = min(values)
val_range = max_val - min_val if max_val != min_val else 1

print(f"Investment Growth Chart — {symbol}{principal:,.0f} at {r*100:.1f}%")
print(f"{'='*width}")

# ASCII chart
for row in range(height - 1, -1, -1):
    threshold = min_val + (val_range * row / (height - 1))
    label = f"{symbol}{threshold:>12,.0f} |"
    line = ""
    for col in range(len(values)):
        x_pos = int(col * (width - 16) / max(len(values) - 1, 1))
        if len(line) <= x_pos:
            line += " " * (x_pos - len(line))
        if values[col] >= threshold:
            line += "█"
        else:
            line += " "
    # Pad line
    line = line.ljust(width - 16)
    print(f"{label}{line}")

# X-axis
x_axis = " " * 15 + "+" + "-" * (width - 16)
print(x_axis)
x_labels = " " * 15
step = max(1, years // 10)
for y in range(0, years + 1, step):
    pos = int(y * (width - 16) / max(years, 1))
    while len(x_labels) < 15 + pos:
        x_labels += " "
    x_labels += str(y)
print(x_labels + " years")

print(f"\nStart: {symbol}{principal:,.2f}  →  End: {symbol}{values[-1]:,.2f}")
print(f"Total growth: {((values[-1]/principal)-1)*100:.1f}%")
PYEOF
    ;;

  export)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
output = os.environ.get("OUTPUT", "")
fmt = os.environ.get("FORMAT", "json")
calc_id = os.environ.get("CALC_ID", "")

records = []
try:
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                if calc_id and rec.get("id") != calc_id:
                    continue
                records.append(rec)
except FileNotFoundError:
    pass

if not records:
    print("No records found to export")
    sys.exit(0)

if fmt == "json":
    result = json.dumps(records if not calc_id else records[0], indent=2)
elif fmt == "csv":
    lines = ["id,timestamp,type,principal,rate,years,final_amount,interest_earned"]
    for r in records:
        p = r.get("params", {})
        res = r.get("result", {})
        lines.append(f"{r.get('id','')},{r.get('timestamp','')},{r.get('type','')},{p.get('principal','')},{p.get('rate','')},{p.get('years','')},{res.get('final_amount','')},{res.get('interest_earned','')}")
    result = "\n".join(lines)
else:
    result = "\n".join(json.dumps(r) for r in records)

if output:
    with open(output, "w") as f:
        f.write(result + "\n")
    print(f"Exported {len(records)} records to {output}")
else:
    print(result)
PYEOF
    ;;

  config)
    python3 << 'PYEOF'
import os, json, sys

config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))
key = os.environ.get("KEY", "")
value = os.environ.get("VALUE", "")

try:
    with open(config_file) as f:
        cfg = json.load(f)
except:
    cfg = {"default_frequency": "monthly", "currency_symbol": "$", "decimal_places": 2}

if key and value:
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    cfg[key] = value
    with open(config_file, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Set {key} = {value}")
elif key:
    print(f"{key} = {cfg.get(key, 'not set')}")
else:
    print("Current configuration:")
    print(json.dumps(cfg, indent=2))
PYEOF
    ;;

  history)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.compound/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.compound/config.json"))
limit = int(os.environ.get("LIMIT", "20"))
sort_by = os.environ.get("SORT", "date")

try:
    with open(config_file) as f:
        cfg = json.load(f)
    symbol = cfg.get("currency_symbol", "$")
except:
    symbol = "$"

records = []
try:
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except:
                    pass
except FileNotFoundError:
    pass

if not records:
    print("No calculation history found.")
    sys.exit(0)

if sort_by == "principal":
    records.sort(key=lambda x: x.get("params", {}).get("principal", 0), reverse=True)
elif sort_by == "rate":
    records.sort(key=lambda x: x.get("params", {}).get("rate", 0), reverse=True)
elif sort_by == "total":
    records.sort(key=lambda x: x.get("result", {}).get("final_amount", 0), reverse=True)
else:
    records.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

records = records[:limit]

print(f"{'ID':<14} {'Date':<20} {'Type':<10} {'Principal':>12} {'Rate':>7} {'Result':>14}")
print("-" * 80)
for r in records:
    ts = r.get("timestamp", "")[:19]
    typ = r.get("type", "?")
    p = r.get("params", {})
    res = r.get("result", {})
    principal_val = p.get("principal", 0)
    rate_val = p.get("rate", p.get("rates", "?"))
    final = res.get("final_amount", res.get("required_rate", res.get("years", "?")))
    rate_str = f"{rate_val:.1f}%" if isinstance(rate_val, (int, float)) else str(rate_val)[:6]
    final_str = f"{symbol}{final:,.0f}" if isinstance(final, (int, float)) and final > 100 else str(final)
    print(f"{r.get('id',''):<14} {ts:<20} {typ:<10} {symbol}{principal_val:>11,.0f} {rate_str:>7} {final_str:>14}")

print(f"\nShowing {len(records)} of total records")
PYEOF
    ;;

  help)
    cat << 'HELPEOF'
Compound — Compound Interest Calculator v1.0.0

Usage: bash scripts/script.sh <command>

Commands:
  calculate   Calculate compound interest
  compare     Compare multiple interest rates
  schedule    Generate detailed growth schedule
  table       Year-by-year summary table
  rate        Calculate required rate for a goal
  goal        Calculate time to reach a savings goal
  chart       ASCII chart of investment growth
  export      Export calculation history
  config      View/update configuration
  history     View past calculations
  help        Show this help message
  version     Show version

Environment Variables:
  PRINCIPAL     Initial investment amount
  RATE          Annual interest rate (%)
  YEARS         Number of years
  FREQUENCY     daily, monthly, quarterly, annually
  CONTRIBUTION  Regular contribution amount
  TARGET        Goal amount (for rate/goal commands)

Examples:
  PRINCIPAL=10000 RATE=7.5 YEARS=20 bash scripts/script.sh calculate
  PRINCIPAL=10000 RATES="3,5,7,10" YEARS=20 bash scripts/script.sh compare
  PRINCIPAL=5000 TARGET=100000 RATE=8 bash scripts/script.sh goal

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
    ;;

  version)
    echo "compound v${VERSION}"
    ;;

  *)
    echo "Unknown command: $COMMAND"
    echo "Run 'bash scripts/script.sh help' for usage information"
    exit 1
    ;;
esac
