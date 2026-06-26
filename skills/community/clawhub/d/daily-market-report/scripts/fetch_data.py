import finnhub
import time

API_KEY = 'cra7aqpr01qhk4bpgnc0cra7aqpr01qhk4bpgncg'
client = finnhub.Client(api_key=API_KEY)

# Market indices
indices = {'QQQ': 'Nasdaq', 'DIA': 'Dow Jones', 'SPY': 'S&P 500'}
for sym, name in indices.items():
    try:
        q = client.quote(sym)
        change = q["dp"]
        current = q["c"]
        high = q["h"]
        low = q["l"]
        print(f"{name} ({sym}): ${current} ({change:+.2f}%) | H:${high} L:${low}")
    except Exception as e:
        print(f"{name} ({sym}): FAILED - {e}")
    time.sleep(1)

print()

# Holdings
for sym in ['BMI', 'PDD']:
    try:
        q = client.quote(sym)
        fin = client.company_basic_financials(sym, 'all')
        rec = client.recommendation_trends(sym)
        metric = fin.get('metric', {})

        print(f"=== {sym} ===")
        print(f"Price: ${q['c']} ({q['dp']:+.2f}%)")
        print(f"52W High: ${metric.get('52WeekHigh', 'N/A')} | 52W Low: ${metric.get('52WeekLow', 'N/A')}")
        print(f"Market Cap: ${metric.get('marketCapitalization', 'N/A')}M | PE: {metric.get('peTTM', 'N/A')}")
        print(f"Beta: {metric.get('beta', 'N/A')} | EPS: ${metric.get('epsExclExtraItemsTTM', 'N/A')}")
        if rec:
            r = rec[0]
            total_buy = r["strongBuy"] + r["buy"]
            total_sell = r["strongSell"] + r["sell"]
            print(f"Analyst: Buy={total_buy} Hold={r['hold']} Sell={total_sell}")
        print()
    except Exception as e:
        print(f"{sym}: FAILED - {e}")
    time.sleep(1.5)