import baostock as bs
import pandas as pd

def main():
    print("🤖 Baostock 实际数据获取演示")
    try:
        lg = bs.login()
        print(f"登录状态: error_code={lg.error_code}, error_msg={lg.error_msg}")

        print("正在获取 sh.600000 历史K线数据...")
        rs = bs.query_history_k_data_plus("sh.600000",
            "date,code,open,high,low,close,volume",
            start_date='2023-01-01', end_date='2023-01-10',
            frequency="d", adjustflag="3")
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        
        if result.empty:
            print("⚠️ 获取数据为空！")
        else:
            print(f"✅ 成功获取数据。")
            print(result.head())
        
        bs.logout()
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")

if __name__ == "__main__":
    main()
