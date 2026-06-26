import akshare as ak
import pandas as pd

def main():
    print("🤖 AKShare 实际数据获取演示")
    try:
        print("正在获取 A股 实时行情...")
        df = ak.stock_zh_a_spot_em()
        if df.empty:
            print("⚠️ 获取数据为空！")
        else:
            print(f"✅ 成功获取 {len(df)} 条 A股 实时数据。")
            print(df[['代码', '名称', '最新价', '涨跌幅']].head())
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")

if __name__ == "__main__":
    main()
