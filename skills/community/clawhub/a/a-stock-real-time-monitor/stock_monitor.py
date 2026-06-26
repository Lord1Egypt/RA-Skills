import requests
import time
import threading
import json
from datetime import datetime
import pandas as pd
from colorama import init, Fore, Style

init(autoreset=True)  # 彩色输出初始化

# ==================== 配置区 ====================
STOCKS = [
    "sh600519",  # 贵州茅台
    "sz000001",  # 平安银行
    "sh600036",  # 招商银行
    # 添加你想盯的股票/指数，格式：sh/sz + 6位代码
]

# 异动阈值（可调）
PRICE_CHANGE_THRESHOLD = 5.0   # 涨跌幅 > 5% 提醒
VOLUME_SPIKE_THRESHOLD = 2.0   # 量比 > 2 提醒

# 推送配置（可选，填入后自动推送）
WECHAT_WEBHOOK = ""  # 企业微信Webhook URL（空则不推送）

# ===============================================

class AStockMonitorSkill:
    def __init__(self):
        self.last_data = {}      # 记录上一周期行情，用于计算异动
        self.session = requests.Session()
        self.session.headers.update({
            "Referer": "https://finance.sina.com.cn/",
            "User-Agent": "Mozilla/5.0"
        })
        print(Fore.CYAN + "🚀 A股实时盯盘Skill 已启动！监控股票：" + ", ".join(STOCKS))

    # 1. 实时行情（新浪API）
    def get_realtime_quotes(self):
        if not STOCKS:
            return {}
        codes = ",".join(STOCKS)
        url = f"http://hq.sinajs.cn/list={codes}"
        try:
            resp = self.session.get(url, timeout=5)
            lines = resp.text.split("\n")
            quotes = {}
            for line in lines:
                if not line.strip() or "=" not in line:
                    continue
                code, data_str = line.split("=", 1)
                code = code.replace("var hq_str_", "")
                items = data_str.strip('";').split(",")
                if len(items) < 10:
                    continue
                quotes[code] = {
                    "name": items[0],
                    "open": float(items[1]),
                    "prev_close": float(items[2]),
                    "current": float(items[3]),
                    "high": float(items[4]),
                    "low": float(items[5]),
                    "volume": int(float(items[8])),      # 手
                    "amount": float(items[9]),           # 金额
                    "change": round((float(items[3]) - float(items[2])) / float(items[2]) * 100, 2),
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
            return quotes
        except Exception as e:
            print(Fore.RED + f"行情获取失败: {e}")
            return {}

    # 2. 异动检测
    def check_abnormal(self, quotes):
        for code, data in quotes.items():
            prev = self.last_data.get(code)
            if not prev:
                continue
            # 价格异动
            if abs(data["change"]) >= PRICE_CHANGE_THRESHOLD:
                alert = f"⚠️【价格异动】{data['name']}({code}) 涨跌幅 {data['change']}%！当前价 {data['current']}"
                print(Fore.RED + alert)
                self.send_alert(alert)
            # 量比异动（当前量 / 上一周期量）
            if prev["volume"] > 0 and data["volume"] / prev["volume"] >= VOLUME_SPIKE_THRESHOLD:
                alert = f"⚠️【成交量异动】{data['name']}({code}) 量比 {data['volume']/prev['volume']:.1f}！成交量 {data['volume']}手"
                print(Fore.YELLOW + alert)
                self.send_alert(alert)
        self.last_data.update(quotes)

    # 3. 主力资金流向（东方财富API）
    def get_main_fund_flow(self):
        flows = {}
        for code in STOCKS:
            market = "1." if code.startswith("sh") else "0."
            secid = market + code[2:]
            url = f"https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&lmt=10&fields1=f1&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65&ut=bd1d9ddb0408974b0b2b9b6f6f4f4f4f"
            try:
                resp = self.session.get(url, timeout=5)
                data = resp.json().get("data", {})
                if data and "klines" in data and data["klines"]:
                    latest = data["klines"][-1].split(",")
                    # 最新主力资金（单位：万）
                    main_in = float(latest[1]) if len(latest) > 1 else 0
                    main_out = float(latest[2]) if len(latest) > 2 else 0
                    net = main_in - main_out
                    flows[code] = {
                        "name": data.get("name", code),
                        "main_net": round(net / 10000, 2),   # 亿
                        "timestamp": latest[0]
                    }
                    if net > 5000:   # 主力净流入>5000万
                        alert = f"💰【主力资金】{flows[code]['name']}({code}) 主力净流入 {flows[code]['main_net']}亿！"
                        print(Fore.GREEN + alert)
                        self.send_alert(alert)
            except:
                pass
        return flows

    # 4. 消息面实时监测（akshare + 东方财富热点）
    def monitor_news(self):
        try:
            import akshare as ak
            # 热门新闻/个股异动消息
            news_df = ak.stock_hot_rank_em()   # 东方财富实时热点
            if not news_df.empty:
                top_news = news_df.head(5)[["名称", "最新价", "涨跌幅"]]
                print(Fore.MAGENTA + "📢【消息面热点】" + str(top_news.to_string(index=False)))
                # 可进一步过滤与STOCKS相关的新闻
        except ImportError:
            # 无akshare时降级为简单新浪新闻标题拉取
            try:
                resp = self.session.get("https://finance.sina.com.cn/roll/2026-04-07/", timeout=5)
                if "异动" in resp.text or any(s in resp.text for s in [c[2:] for c in STOCKS]):
                    print(Fore.MAGENTA + "📢【消息面】检测到个股相关新闻（请打开东方财富APP查看详情）")
            except:
                pass

    # 推送（企业微信示例）
    def send_alert(self, message):
        if WECHAT_WEBHOOK:
            try:
                requests.post(WECHAT_WEBHOOK, json={"msgtype": "text", "text": {"content": message}})
            except:
                pass

    # 主循环
    def run(self):
        while True:
            now = datetime.now()
            # 仅交易时段高频刷新（9:30-11:30 & 13:00-15:00）
            if (9 <= now.hour < 11 and now.minute >= 30) or (13 <= now.hour < 15):
                quotes = self.get_realtime_quotes()
                if quotes:
                    self.check_abnormal(quotes)
                    print(Fore.WHITE + f"[{now.strftime('%H:%M:%S')}] 实时行情更新 → {len(quotes)}只股票")
                    for c, d in list(quotes.items())[:3]:   # 只打印前3只示例
                        print(f"   {d['name']}({c}) {d['current']} 涨跌{d['change']}% 量{d['volume']}手")

                # 主力资金（每30秒一次）
                if now.second % 30 == 0:
                    self.get_main_fund_flow()

                # 消息面（每5分钟一次）
                if now.minute % 5 == 0:
                    self.monitor_news()
            else:
                print(Fore.BLUE + f"[{now.strftime('%H:%M:%S')}] 非交易时段，暂停刷新...")

            time.sleep(5)   # 5秒轮询一次

# ==================== 启动 ====================
if __name__ == "__main__":
    skill = AStockMonitorSkill()
    try:
        skill.run()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n👋 盯盘Skill已停止。祝交易顺利！")