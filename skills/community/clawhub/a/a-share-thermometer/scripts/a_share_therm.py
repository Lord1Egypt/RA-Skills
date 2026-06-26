import argparse
import akshare as ak
import pandas as pd
import concurrent.futures
from datetime import date
from dateutil.relativedelta import relativedelta

INDEX_NAMES = [
    "上证50", "沪深300", "上证380", "创业板50",
    "中证500", "深证红利", "深证100", "中证1000",
]

def get_index_temperature(name: str) -> dict:
    try:
        ten_years_ago = date.today() - relativedelta(years=10)
        df = ak.stock_index_pe_lg(name)
        metric = "滚动市盈率"
        df["日期"] = pd.to_datetime(df["日期"])
        df = df[(df["日期"] >= pd.to_datetime(ten_years_ago)) & (df[metric] > 0)].sort_values("日期")
        if len(df) < 250:
            return {"name": name, "error": "数据不足"}
        latest_pe = df[metric].iloc[-1]
        pectile_pe = df[metric].rank(pct=True)[df[metric] == latest_pe]
        temperature = pectile_pe.mean() * 100
        return {"name": name, "pe": round(latest_pe, 2), "temp": round(temperature, 1)}
    except Exception as e:
        return {"name": name, "error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default=None, help="指数名称")
    args = parser.parse_args()

    if args.index:
        result = get_index_temperature(args.index)
        if "error" in result:
            print(f"指数：{result['name']}\n失败：{result['error']}")
        else:
            print(f"指数：{result['name']}\n当前PE(TTM)：{result['pe']:.2f}\n温度：{result['temp']:.1f}")
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(get_index_temperature, name): name for name in INDEX_NAMES}
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        for name in INDEX_NAMES:
            for r in results:
                if r["name"] == name:
                    if "error" in r:
                        print(f"指数：{r['name']}\n失败：{r['error']}\n")
                    else:
                        print(f"指数：{r['name']}\n当前PE(TTM)：{r['pe']:.2f}\n温度：{r['temp']:.1f}\n")
                    break

if __name__ == "__main__":
    main()
