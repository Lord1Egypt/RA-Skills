"""
涨跌停池查询（需要 akshare）
pip install akshare
"""
try:
    import akshare as ak
except ImportError:
    print("需要安装akshare: pip install akshare")
    exit(1)

def get_zt_pool():
    print("\n=== 涨停池 ===")
    try:
        zt = ak.stock_zt_pool_previous_em()
        print(f"涨停家数: {len(zt)}")
        print("涨停股(代码/名称/涨幅):")
        for _, row in zt.head(15).iterrows():
            print(f"  🔴 {row.get('代码','?')} {row.get('名称','?')} {row.get('涨幅','?')}%")
    except Exception as e:
        print(f"涨停池获取失败: {e}")

    print("\n=== 跌停池 ===")
    try:
        dt = ak.stock_zt_pool_dtgc_em()
        print(f"跌停家数: {len(dt)}")
        print("跌停股(代码/名称/跌幅):")
        for _, row in dt.head(15).iterrows():
            print(f"  🟢 {row.get('代码','?')} {row.get('名称','?')} {row.get('跌幅','?')}%")
    except Exception as e:
        print(f"跌停池获取失败: {e}")

if __name__ == "__main__":
    get_zt_pool()
