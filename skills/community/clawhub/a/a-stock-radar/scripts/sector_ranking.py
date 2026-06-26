"""
东方财富板块涨跌排行
行业板块: m:90+t:2
概念板块: m:90+t:3

【双层架构】
1. 主：东方财富 push2 API
2. 备：东方财富网页 HTML 解析（502/超时/网络错误时切换）
"""
import requests
import sys
import time
import io

def _get_via_api(market_type, top, retries):
    """东方财富 API（主）"""
    fs = "m:90+t:2" if market_type == "行业板块" else "m:90+t:3"
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": top, "po": 1, "np": 1,
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": fs,
        "fields": "f12,f14,f2,f3,f5,f6,f8,f10,f15,f16,f18"
    }
    headers = {"Referer": "https://quote.eastmoney.com/"}

    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            if r.status_code == 502:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                break
            r.raise_for_status()
            return r.json()["data"]["diff"]
        except Exception:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            raise
    return None  # API 层失败，返回 None 触发备用


def _get_via_html(market_type, top=30):
    """
    东方财富板块排行 HTML 解析（备用）
    通过 pandas.read_html 直接解析网页表格，无需浏览器
    """
    market_id = "2" if market_type == "行业板块" else "3"
    url = f"https://quote.eastmoney.com/center/boardlist.html#行业板块_{market_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://quote.eastmoney.com/",
    }
    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"
    r.raise_for_status()

    import pandas as pd

    # 东方财富板块页面含多个表格，找到正确的那个
    tables = pd.read_html(io.StringIO(r.text))
    for df in tables:
        cols = df.columns.tolist()
        # 找含"板块名称"或"涨跌幅"的列
        if any("板块" in str(c) for c in cols) or any("涨跌幅" in str(c) for c in cols):
            # 标准化列名
            df.columns = [str(c) for c in df.columns]
            # 找涨跌幅列
            pct_col = next((c for c in df.columns if "涨跌幅" in c or "涨跌" in c), None)
            name_col = next((c for c in df.columns if "板块" in c or "名称" in c), None)
            if pct_col and name_col:
                result = []
                for _, row in df.iterrows():
                    try:
                        pct = float(str(row[pct_col]).replace("%", "").replace("+", ""))
                        name = str(row[name_col])
                        if name and name != "nan":
                            result.append({"f14": name, "f3": pct, "f6": 0})
                    except ValueError:
                        continue
                return result[:top]
    return []


def get_sector_ranking(market_type="行业板块", top=20, retries=3):
    """
    获取板块涨跌排行。
    优先走 API，失败时自动切换 HTML 解析。
    """
    # 尝试 API（主）
    data = None
    try:
        data = _get_via_api(market_type, top, retries)
    except Exception:
        pass

    if data is not None:
        return data

    # API 失败，切换 HTML 备用（等1秒）
    time.sleep(1)
    try:
        return _get_via_html(market_type, top)
    except Exception:
        return []

def format_sector(s):
    pct = s["f3"]
    arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
    return f"{arrow} {s['f14']:12s}  {'+' if pct>=0 else ''}{pct}%  成交额:{s['f6']/1e8:.1f}亿"

if __name__ == "__main__":
    market = sys.argv[1] if len(sys.argv) > 1 else "行业板块"
    print(f"\n=== {market}涨跌榜 ===")
    data = get_sector_ranking(market, 30)
    if not data:
        print("（板块数据暂时不可用，请稍后重试）")
    else:
        print("\n【涨幅榜】")
        for s in sorted(data, key=lambda x: x["f3"], reverse=True)[:10]:
            print(format_sector(s))
        print("\n【跌幅榜】")
        for s in sorted(data, key=lambda x: x["f3"])[:10]:
            print(format_sector(s))
