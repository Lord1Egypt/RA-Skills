#!/bin/bash
# 加密货币价格查询脚本

case "$1" in
    price)
        COIN="$2"
        curl -s "https://api.coingecko.com/api/v3/simple/price?ids=${COIN}&vs_currencies=usd,cny&include_24hr_change=true&include_market_cap=true" | python3 -m json.tool
        ;;
    top)
        curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('='*70)
print('排名  币种           价格(USD)      24h涨跌      市值(USD)')
print('='*70)
for coin in data:
    rank = coin.get('market_cap_rank', '-')
    name = coin.get('symbol', '').upper()
    price = coin.get('current_price', 0)
    change = coin.get('price_change_percentage_24h', 0)
    cap = coin.get('market_cap', 0)
    change_str = '{:+.2f}%'.format(change) if change else 'N/A'
    cap_str = '\${:,.1f}B'.format(cap/1e9) if cap else 'N/A'
    print('{:5} {:15} \${:>12,.2f} {:>12} {:>15}'.format(rank, name, price, change_str, cap_str))
"
        ;;
    search)
        QUERY="$2"
        curl -s "https://api.coingecko.com/api/v3/search?query=${QUERY}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for coin in data.get('coins', [])[:5]:
    print(coin.get('symbol', '').upper() + ': ' + coin.get('name') + ' (ID: ' + coin.get('id') + ')')
"
        ;;
    *)
        echo "Usage: $0 {price|top|search} [args]"
        ;;
esac
