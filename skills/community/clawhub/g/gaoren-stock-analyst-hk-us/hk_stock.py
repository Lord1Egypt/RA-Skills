import requests
import re

# 腾讯财经港股格式: hk + 股票代码(5位)
symbols = {
    'hk01826': '京东物流',
    'hk009618': '京东集团',
    'hk003690': '美团',
    'hk00700': '腾讯',
    'hk09988': '阿里巴巴'
}

print("="*60)
print("  港股实时行情")
print("="*60)

base_url = 'https://qt.gtimg.cn/q='

for code, name in symbols.items():
    url = base_url + code
    try:
        r = requests.get(url, timeout=8)
        text = r.text
        
        if 'none_match' in text:
            continue
            
        # 解析数据 v_hk00700="100~腾讯控股~00700~519.500~550.500~528.000~31526795.0~
        # 格式: 代码~名称~代码~今收~最高~最低~成交量~...
        
        match = re.search(r'"([^"]+)"', text)
        if match:
            parts = match.group(1).split('~')
            if len(parts) >= 10:
                current = parts[3]   # 当前价
                high = parts[4]      # 最高
                low = parts[5]       # 最低
                volume = parts[6]   # 成交量
                open_price = parts[9] if len(parts) > 9 else parts[3]  # 开盘
                
                # 计算涨跌
                try:
                    change = float(current) - float(open_price)
                    change_pct = (change / float(open_price)) * 100 if float(open_price) > 0 else 0
                except:
                    change = 0
                    change_pct = 0
                
                print(f"\n【{name}】{code.replace('hk', '')}")
                print(f"  当前价: HK${current}")
                print(f"  涨跌: {change:+.2f} ({change_pct:+.2f}%)")
                print(f"  开盘: {open_price} | 最高: {high} | 最低: {low}")
                print(f"  成交量: {volume}")
                
    except Exception as e:
        print(f"{name}: Error - {e}")

print("\n" + "="*60)
