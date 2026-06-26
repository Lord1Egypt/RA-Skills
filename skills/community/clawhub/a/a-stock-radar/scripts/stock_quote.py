"""
新浪财经个股实时行情
用法: python stock_quote.py sh600519
       python stock_quote.py sh600519 sz000001
"""
import requests
import sys

def fetch_stock_quotes(codes):
    if isinstance(codes, str):
        codes = [codes]
    url = f"https://hq.sinajs.cn/list={','.join(codes)}"
    headers = {"Referer": "http://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'gbk'
    results = []
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        name_part, data = line.split('=', 1)
        code = name_part.split('_')[-1].replace('"', '')
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 6:
            continue
        try:
            prev = float(vals[2])
            price = float(vals[3])
            if prev == 0:
                continue
            pct = (price - prev) / prev * 100
            chg = price - prev
            high = float(vals[4])
            low = float(vals[5])
            volume = float(vals[8]) / 1e8 if len(vals) > 8 and vals[8] else 0
            results.append({
                "code": code,
                "name": vals[0],
                "price": price,
                "chg": chg,
                "pct": pct,
                "high": high,
                "low": low,
                "volume": volume,
            })
        except (ValueError, IndexError):
            continue
    return results


def format_stock_quote(item):
    arrow = "🔴" if item["pct"] > 0 else "🟢" if item["pct"] < 0 else "⚪"
    return (
        f"{arrow} {item['name']:8s} {item['code']:8s} "
        f"现价:{item['price']:.2f} 涨跌:{item['chg']:+.2f}({item['pct']:+.2f}%) "
        f"高:{item['high']:.2f} 低:{item['low']:.2f} 量:{item['volume']:.2f}亿"
    )


def get_stock_quote(codes):
    results = fetch_stock_quotes(codes)
    for item in results:
        print(format_stock_quote(item))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python stock_quote.py sh600519 [sz000001 ...]")
        sys.exit(1)
    codes = sys.argv[1:]
    get_stock_quote(codes)
