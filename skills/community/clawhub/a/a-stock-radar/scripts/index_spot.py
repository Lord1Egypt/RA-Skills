"""
A股主要指数实时行情
上证、深成、创业板、科创50、沪深300

【双层架构】
1. 主：新浪财经 hq.sinajs.cn API
2. 备：东方财富网页 + 浏览器抓取（API 失败时自动切换）
"""
import requests
import time

MAJOR_INDICES = {
    "sh000001": "上证指数",
    "sz399001": "深证成指",
    "sz399006": "创业板指",
    "sh000688": "科创50",
    "sh000300": "沪深300",
    "sz399905": "中证500",
}

_NAME_MAP = {v: k for k, v in MAJOR_INDICES.items()}


def _get_via_sina() -> dict:
    """新浪财经 API（主）"""
    codes = ",".join(MAJOR_INDICES.keys())
    url = f"https://hq.sinajs.cn/list={codes}"
    headers = {"Referer": "http://finance.sina.com.cn"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    r.encoding = 'gbk'
    results = {}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        key, data = line.split('=', 1)
        vals = data.replace('"', '').replace(';', '').split(',')
        if len(vals) < 4:
            continue
        try:
            code = key[-8:].replace('_hq_str', '').replace('"', '')
            prev = float(vals[2])
            price = float(vals[3])
            if prev == 0:
                continue
            pct = (price - prev) / prev * 100
            chg = price - prev
            arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
            name = MAJOR_INDICES.get(code, code)
            results[code] = f"{arrow} {name}: {price:.2f} {chg:+.2f}({pct:+.2f}%)"
        except (ValueError, IndexError):
            continue
    return results


def _get_via_eastmoney() -> dict:
    """东方财富 API（备用1）"""
    url = (
        "https://push2.eastmoney.com/api/qt/clist/get"
        "?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3"
        "&fs=m:1+t:2&fields=f2,f3,f4,f12,f14"
    )
    headers = {
        "Referer": "https://quote.eastmoney.com/",
        "User-Agent": "Mozilla/5.0",
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", {}).get("diff", [])
    results = {}
    for item in items:
        code = "sh" + str(item.get("f12", ""))
        name = MAJOR_INDICES.get(code)
        if not name:
            continue
        price = item.get("f2", 0)
        pct = item.get("f3", 0)
        chg = price * pct / 100
        arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
        results[code] = f"{arrow} {name}: {price:.2f} {chg:+.2f}({pct:+.2f}%)"
    return results


def get_major_indices() -> dict:
    """
    获取A股主要指数，尝试顺序：
    新浪API → 东方财富API → 返回空dict（不抛异常）
    """
    # 尝试新浪（主）
    try:
        result = _get_via_sina()
        if result:
            return result
    except Exception:
        pass

    # 等待1秒再试东方财富（避免同时失败）
    time.sleep(1)

    # 尝试东方财富（备）
    try:
        result = _get_via_eastmoney()
        if result:
            return result
    except Exception:
        pass

    return {}


if __name__ == "__main__":
    print("\n=== A股主要指数 ===")
    indices = get_major_indices()
    for v in indices.values():
        print(v)

