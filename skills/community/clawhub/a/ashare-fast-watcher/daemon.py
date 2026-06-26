import requests
import time
import os
import datetime

# ================= 配置区 =================
POLL_INTERVAL = 3  # 轮询间隔（秒）
# 配置你要盯盘的组合 (正股, 转债) 或 (ETF, IOPV)
BOND_PAIRS = [("sz002085", "sz128047")]  # 万丰奥威, 万丰转债
ETF_PAIRS = [("sh513520", "sh513520")]   # 日经ETF (测试用)

# 冷却池：防止同一个信号每3秒疯狂弹窗，设定60秒内不重复报警
alert_cooldown = {}
# ==========================================

def notify_mac(title, msg):
    """调用 macOS 原生系统弹窗与提示音 (游资专属高能提醒)"""
    safe_msg = msg.replace('"', '\\"')
    cmd = f'''osascript -e 'display notification "{safe_msg}" with title "{title}" sound name "Glass"''''
    os.system(cmd)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🚨 触发报警: {msg}")

def fetch_data(codes):
    try:
        url = f"http://qt.gtimg.cn/q={codes}"
        resp = requests.get(url, timeout=1.0)
        lines = resp.text.strip().split(';')
        res = {}
        for line in lines:
            p = line.split('~')
            if len(p) >= 40:
                res[p[2]] = {"name": p[1], "price": float(p[3]), "change": float(p[32])}
        return res
    except Exception as e:
        print(f"网络异常: {e}")
        return {}

def run_monitor():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 幽灵哨兵已启动，每 {POLL_INTERVAL} 秒极速轮询中...")
    
    while True:
        now = datetime.datetime.now()
        # 游资审美：非交易时间自动静默，节约资源 (9:15-11:30, 13:00-15:00)
        # 注：周末或测试期间可以注释掉这部分
        is_trading_time = (
            (now.hour == 9 and now.minute >= 15) or 
            (now.hour == 10) or 
            (now.hour == 11 and now.minute <= 30) or 
            (13 <= now.hour < 15)
        )
        
        # 强行放开限制以便你现在周末测试（实盘请改回 if is_trading_time:）
        if True: 
            all_codes = [p[0] for p in BOND_PAIRS] + [p[1] for p in BOND_PAIRS] + \
                        [p[0] for p in ETF_PAIRS] + [p[1] for p in ETF_PAIRS]
            market_data = fetch_data(",".join(set(all_codes)))

            # 1. 监控股债联动
            for stock, bond in BOND_PAIRS:
                if stock in market_data and bond in market_data:
                    s_data, b_data = market_data[stock], market_data[bond]
                    if s_data['change'] >= 9.9 and b_data['change'] < 19.5:
                        msg = f"{s_data['name']}已封板，{b_data['name']}涨幅仅{b_data['change']}%，存在套利空间！"
                        if time.time() - alert_cooldown.get(bond, 0) > 60:
                            notify_mac("🔥 股债联动狙击", msg)
                            alert_cooldown[bond] = time.time()

            # 2. 监控ETF溢价 (逻辑演示，由于测试时ETF和IOPV代码传的一样，溢价率算出来是0)
            for etf, iopv in ETF_PAIRS:
                if etf in market_data and iopv in market_data:
                    e_data, i_data = market_data[etf], market_data[iopv]
                    if i_data['price'] > 0:
                        premium = (e_data['price'] - i_data['price']) / i_data['price'] * 100
                        if premium > 3.0:
                            msg = f"{e_data['name']} 溢价率达 {round(premium, 2)}%，可动用通道排单！"
                            if time.time() - alert_cooldown.get(etf, 0) > 60:
                                notify_mac("⚠️ ETF溢价飙升", msg)
                                alert_cooldown[etf] = time.time()

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run_monitor()
