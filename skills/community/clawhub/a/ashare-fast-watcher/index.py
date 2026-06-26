import sys
import json
import requests

def fetch_raw_data(code_str):
    url = f"http://qt.gtimg.cn/q={code_str}"
    try:
        resp = requests.get(url, timeout=0.5)
        if resp.status_code == 200:
            return resp.text.strip().split(';')
        return []
    except:
        return []

def parse_line(line):
    p = line.split('~')
    if len(p) < 40: return None
    return {
        "name": p[1], "code": p[2], "current": float(p[3]),
        "change_percent": float(p[32]), "volume_hands": p[36],
        "turnover_ten_thousand": round(float(p[37]), 2), "bid1": p[9], "ask1": p[19]
    }

def analyze_bond_linkage(stock_code, bond_code):
    """股债联动狙击逻辑"""
    data = fetch_raw_data(f"{stock_code},{bond_code}")
    if len(data) < 2: return {"action": "WAIT", "msg": "数据不全"}
    
    stock, bond = parse_line(data[0]), parse_line(data[1])
    if not stock or not bond: return {"action": "WAIT", "msg": "解析失败"}

    # 核心判断：正股涨停（涨幅>9.9%）且一字封单坚决，转债涨幅未达20%熔断线
    if stock['change_percent'] >= 9.9 and bond['change_percent'] < 19.5:
        return {
            "action": "TRIGGER_BOND_BUY",
            "target": bond['name'],
            "spread_left": round(20.0 - bond['change_percent'], 2),
            "msg": f"🔥 {stock['name']}已封板，{bond['name']} 存在 {round(20.0 - bond['change_percent'], 2)}% 熔断差价，建议出击！"
        }
    return {"action": "WAIT", "msg": "未达触发条件"}

def analyze_etf_premium(etf_code, iopv_code):
    """ETF 溢价率监控逻辑"""
    data = fetch_raw_data(f"{etf_code},{iopv_code}")
    if len(data) < 2: return {"action": "WAIT"}
    
    etf, iopv = parse_line(data[0]), parse_line(data[1])
    if not etf or not iopv: return {"action": "WAIT"}

    # 计算实时溢价率
    premium_rate = (etf['current'] - iopv['current']) / iopv['current'] * 100
    if premium_rate > 3.0:
        return {
            "action": "QUEUE_ETF_LIMIT_UP",
            "etf_name": etf['name'],
            "premium": round(premium_rate, 2),
            "msg": f"⚠️ {etf['name']} 溢价率飙升至 {round(premium_rate, 2)}%，可动用通道排单！"
        }
    return {"action": "WAIT", "premium": round(premium_rate, 2)}

if __name__ == "__main__":
    try:
        input_data = sys.argv[1] if len(sys.argv) > 1 else ""
        if input_data.startswith('{'):
            params = json.loads(input_data)
            mode = params.get("mode", "quote")
            stock = params.get("stock", "")
            bond_or_iopv = params.get("target2", "")
            
            if mode == "bond_linkage":
                print(json.dumps(analyze_bond_linkage(stock, bond_or_iopv), ensure_ascii=False))
            elif mode == "etf_premium":
                print(json.dumps(analyze_etf_premium(stock, bond_or_iopv), ensure_ascii=False))
            else:
                print(json.dumps({"error": "Unknown mode"}))
        else:
            print(json.dumps({"error": "Please provide JSON payload: {\"mode\": \"bond_linkage\", \"stock\": \"sz000651\", \"target2\": \"sz127053\"}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
