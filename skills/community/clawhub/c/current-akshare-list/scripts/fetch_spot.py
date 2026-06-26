#!/usr/bin/env python3
"""
akshare 实时行情获取脚本
获取 A股、B股、科创板 实时行情数据并保存
"""
import akshare as ak
import json
import sys

def fetch_all_spot_data():
    """获取三个接口的实时行情数据"""
    results = {}
    
    # 1. A股实时行情
    print("=== 1. 获取 A股 实时行情 ===")
    sys.stdout.flush()
    try:
        df = ak.stock_zh_a_spot_em()
        codes = df[['代码', '名称']].to_dict('records')
        with open('/tmp/akshare_a_codes.json', 'w', encoding='utf-8') as f:
            json.dump(codes, f, ensure_ascii=False)
        results['a'] = len(codes)
        print(f"A股成功: {len(codes)} 条")
    except Exception as e:
        print(f"A股失败: {type(e).__name__}: {e}")
        raise ConnectionError(f"A股接口封禁: {e}")
    
    # 2. B股实时行情
    print("\n=== 2. 获取 B股 实时行情 ===")
    sys.stdout.flush()
    try:
        df = ak.stock_zh_b_spot_em()
        codes = df[['代码', '名称']].to_dict('records')
        with open('/tmp/akshare_b_codes.json', 'w', encoding='utf-8') as f:
            json.dump(codes, f, ensure_ascii=False)
        results['b'] = len(codes)
        print(f"B股成功: {len(codes)} 条")
    except Exception as e:
        print(f"B股失败: {e}")
        results['b'] = 0
    
    # 3. 科创板实时行情
    print("\n=== 3. 获取 科创板 实时行情 ===")
    sys.stdout.flush()
    try:
        df = ak.stock_zh_kcb_spot()
        codes = df[['代码', '名称']].to_dict('records')
        with open('/tmp/akshare_kcb_codes.json', 'w', encoding='utf-8') as f:
            json.dump(codes, f, ensure_ascii=False)
        results['kcb'] = len(codes)
        print(f"科创板成功: {len(codes)} 条")
    except Exception as e:
        print(f"科创板失败: {e}")
        results['kcb'] = 0
    
    print("\n=== 完成 ===")
    print(f"结果: {results}")
    return results

if __name__ == "__main__":
    try:
        fetch_all_spot_data()
    except ConnectionError as e:
        print(f"\n接口封禁，请开启VPN后重试")
        sys.exit(1)