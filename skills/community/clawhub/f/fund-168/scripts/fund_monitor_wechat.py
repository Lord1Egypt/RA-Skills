#!/usr/bin/env python3
"""
Fund-005 基金监控技能 - 多源API降级 · 独立任务模式 · 涨跌幅告警 · 持仓盈亏追踪
支持：自选基金管理、压力位/支撑位计算、多渠道推送（企业微信/钉钉/飞书/邮件）
"""
import sys
import os
import json
import re
import csv
import datetime
import urllib.request
import urllib.error
import traceback

VERSION = "v2.1.0"

# 数据目录
DATA_DIR = os.environ.get("LOOK_FUND_DATA_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))

WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
PUSH_FILE = os.path.join(DATA_DIR, "push_channels.json")
ALERT_FILE = os.path.join(DATA_DIR, "alert_config.json")
HOLDINGS_FILE = os.path.join(DATA_DIR, "holdings.json")
LOG_DIR = os.path.join(DATA_DIR, "logs")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

def log(msg):
    ensure_dirs()
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{today}.log")
    ts = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_watchlist():
    return load_json(WATCHLIST_FILE, [])

def save_watchlist(wl):
    save_json(WATCHLIST_FILE, wl)

def get_config():
    return load_json(CONFIG_FILE, {
        "monitor_times": ["14:30"],
        "webhook_url": "",
        "default_ma_period": 20,
        "tasks": {},
        "alert": {"default_threshold": 3, "mode": "close"},
        "backup": {"format": "csv", "path": "", "auto_backup": False}
    })

def save_config(cfg):
    save_json(CONFIG_FILE, cfg)

def get_push_channels():
    return load_json(PUSH_FILE, [])

def save_push_channels(channels):
    save_json(PUSH_FILE, channels)

def get_alert_config():
    return load_json(ALERT_FILE, {"default_threshold": 3, "mode": "close", "per_fund": {}})

def save_alert_config(ac):
    save_json(ALERT_FILE, ac)

def get_holdings():
    return load_json(HOLDINGS_FILE, {})

def save_holdings(h):
    save_json(HOLDINGS_FILE, h)

# ========== API 数据源 ==========

def _http_get(url, headers=None, timeout=15):
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")

def fetch_nav_eastmoney(code, count=60):
    try:
        url = (f"http://fund.eastmoney.com/f10/F10DataApi.aspx"
               f"?type=lsjz&code={code}&page=1&per={count}")
        text = _http_get(url, headers={"Referer": "https://fundf10.eastmoney.com/"})
        match = re.search(r'content:"(.*?)"', text, re.DOTALL)
        if not match:
            return []
        html = match.group(1)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
        nav_list = []
        for row in rows:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(tds) >= 3:
                date_str = tds[0].strip()
                nav_str = tds[1].strip()
                try:
                    nav = float(nav_str)
                    nav_list.append({"date": date_str, "nav": nav})
                except ValueError:
                    pass
        return nav_list
    except Exception as e:
        log(f"[eastmoney] failed for {code}: {e}")
        return []

def fetch_nav_doctorxiong(code, count=60):
    try:
        url = f"https://api.doctorxiong.club/v1/fund/netWorth?code={code}"
        text = _http_get(url)
        data = json.loads(text)
        items = data.get("data", [])
        nav_list = []
        for item in items[-count:]:
            nav = item.get("netWorth") or item.get("nav")
            date_str = item.get("date") or item.get("fundDate", "")
            if nav:
                nav_list.append({"date": date_str, "nav": float(nav)})
        return nav_list
    except Exception as e:
        log(f"[doctorxiong] failed for {code}: {e}")
        return []

def fetch_nav_eastmoney_backup(code, count=60):
    try:
        url = f"https://fund.eastmoney.com/pingzhongdata/{code}.js"
        text = _http_get(url, headers={"Referer": "https://fund.eastmoney.com/"})
        match = re.search(r'var Data_netWorthTrend\s*=\s*(\[.*?\]);', text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            nav_list = []
            for item in data[-count:]:
                nav = item.get("y", 0)
                date_ms = item.get("x", 0)
                if nav and date_ms:
                    date_str = datetime.datetime.fromtimestamp(
                        date_ms / 1000).strftime("%Y-%m-%d")
                    nav_list.append({"date": date_str, "nav": float(nav)})
            return nav_list
    except Exception as e:
        log(f"[eastmoney-backup] failed for {code}: {e}")
    return []

def fetch_nav(code, count=60):
    result = fetch_nav_eastmoney(code, count)
    if result:
        return result
    result = fetch_nav_eastmoney_backup(code, count)
    if result:
        return result
    result = fetch_nav_doctorxiong(code, count)
    return result

def fetch_realtime_estimation(code):
    try:
        url = f"http://fundgz.1234567.com.cn/js/{code}.js"
        text = _http_get(url)
        match = re.search(r'jsonpgz\((.*?)\);', text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            return {
                "name": data.get("fundname", ""),
                "code": data.get("fundcode", ""),
                "estimation": float(data.get("gsz", 0)),
                "change_pct": float(data.get("gszzl", 0)),
                "date": data.get("gztime", ""),
            }
    except Exception:
        pass
    return None

# ========== 技术分析 ==========

def calc_pressure_support(nav_list, ma_period=20):
    if not nav_list:
        return None
    current = nav_list[-1]["nav"]
    recent = nav_list[-min(ma_period, len(nav_list)):]
    ma = sum(x["nav"] for x in recent) / len(recent)

    ma_pressure = ma * 1.05
    if ma_pressure > current:
        pressure = round(ma_pressure, 4)
    else:
        pressure = round(current * 1.05, 4)

    ma_support = ma * 0.95
    if ma_support < current:
        support = round(ma_support, 4)
    else:
        support = round(current * 0.95, 4)

    return {
        "current": round(current, 4),
        "ma": round(ma, 4),
        "pressure": pressure,
        "support": support,
        "focus": round(support, 2),
    }

# ========== 多渠道推送 ==========

def send_feishu(webhook_url, text):
    payload = json.dumps({"msg_type": "text", "content": {"text": text}}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("code") == 0 or result.get("StatusCode") == 0
    except Exception as e:
        log(f"[feishu] send failed: {e}")
        return False

def send_dingtalk(webhook_url, text, secret=None):
    import hashlib, hmac as _hmac, base64, time as _time
    if secret:
        ts = str(int(_time.time() * 1000))
        sign_str = f"{ts}\n{secret}"
        hmac_code = _hmac.new(secret.encode(), sign_str.encode(), hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode()
        sep = "&" if "?" in webhook_url else "?"
        webhook_url = f"{webhook_url}{sep}timestamp={ts}&sign={sign}"
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("errcode") == 0
    except Exception as e:
        log(f"[dingtalk] send failed: {e}")
        return False

def send_wechat(webhook_url, text):
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("errcode") == 0
    except Exception as e:
        log(f"[wechat] send failed: {e}")
        return False

def send_email(config, text):
    try:
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = "基金监控报告"
        msg["From"] = config.get("from", "")
        msg["To"] = config.get("to", "")
        with smtplib.SMTP_SSL(config.get("smtp", ""), config.get("port", 465)) as server:
            server.login(config.get("from", ""), config.get("password", ""))
            server.sendmail(config.get("from", ""), [config.get("to", "")], msg.as_string())
        return True
    except Exception as e:
        log(f"[email] send failed: {e}")
        return False

def push_to_channels(text, cfg=None):
    if cfg is None:
        cfg = get_config()
    results = []

    feishu_url = cfg.get("feishu_webhook", "") or cfg.get("webhook_url", "")
    if feishu_url and "feishu" in feishu_url:
        ok = send_feishu(feishu_url, text)
        results.append(("飞书", ok))

    channels = get_push_channels()
    for ch in channels:
        ch_type = ch.get("type", "")
        ch_url = ch.get("url", "")
        ch_secret = ch.get("secret", "")
        if ch_type == "feishu":
            ok = send_feishu(ch_url, text)
            results.append(("飞书", ok))
        elif ch_type == "dingtalk":
            ok = send_dingtalk(ch_url, text, ch_secret)
            results.append(("钉钉", ok))
        elif ch_type in ("wechat", "qywechat"):
            ok = send_wechat(ch_url, text)
            results.append(("企业微信", ok))
        elif ch_type == "email":
            ok = send_email(ch, text)
            results.append(("邮件", ok))
    return results

# ========== 报告生成 ==========

def get_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

def gen_monitor_report_all():
    now = get_now()
    wl = get_watchlist()
    cfg = get_config()
    ma_period = cfg.get("default_ma_period", 20)
    per_fund_ma = cfg.get("per_fund_ma", {})

    if not wl:
        return "📊 基金监控报告\n自选基金列表为空，请先添加基金。"

    lines = [f"📊 基金监控报告 [{now.strftime('%Y-%m-%d %H:%M')}]", "─" * 52]
    for fund in wl:
        code = fund.get("code", "")
        name = fund.get("name", "")
        mp = per_fund_ma.get(code, ma_period)
        nav_list = fetch_nav(code)
        if not nav_list:
            lines.append(f"  【{name}】{code}")
            lines.append(f"    ❌ 数据获取失败")
            lines.append("  " + "┄" * 50)
            continue
        result = calc_pressure_support(nav_list, mp)
        if not result:
            lines.append(f"  【{name}】{code}")
            lines.append(f"    ❌ 数据不足")
            lines.append("  " + "┄" * 50)
            continue
        lines.append(f"  【{name}】{code}")
        lines.append(f"    最新净值：{result['current']}")
        lines.append(f"    压 力 位：{result['pressure']}")
        lines.append(f"    支 撑 位：{result['support']}")
        lines.append(f"    重点关注：{result['focus']}")
        holdings = get_holdings()
        if code in holdings:
            h = holdings[code]
            cost = h.get("cost", 0)
            shares = h.get("shares", 0)
            if cost > 0 and shares > 0:
                value = result["current"] * shares
                pnl = value - cost * shares
                pnl_pct = (result["current"] / cost - 1) * 100
                sign = "+" if pnl >= 0 else ""
                lines.append(f"    持仓盈亏：{sign}{pnl:.2f} ({sign}{pnl_pct:.2f}%)")
        lines.append("  " + "┄" * 50)
    lines.append("─" * 52)
    lines.append("end")
    return "\n".join(lines)

def gen_feishu_report():
    now = get_now()
    wl = get_watchlist()
    cfg = get_config()
    ma_period = cfg.get("default_ma_period", 20)
    per_fund_ma = cfg.get("per_fund_ma", {})

    if not wl:
        return "自选基金列表为空"

    header = f"[{now.strftime('%m-%d %H:%M')}]信息来源：三康智能体11bot"
    lines = [header, "📊 基金监控报告", ""]

    for fund in wl:
        code = fund.get("code", "")
        name = fund.get("name", "")
        mp = per_fund_ma.get(code, ma_period)
        nav_list = fetch_nav(code)
        if not nav_list:
            lines.append(f"{name}({code})")
            lines.append("数据获取失败")
            lines.append("")
            continue
        result = calc_pressure_support(nav_list, mp)
        if not result:
            lines.append(f"{name}({code})")
            lines.append("数据不足")
            lines.append("")
            continue
        lines.append(f"{name}({code})")
        lines.append(f"压力位：{result['pressure']}")
        lines.append(f"当前净值：{result['current']}")
        lines.append(f"支撑位：{result['support']}")
        lines.append(f"重点关注={result['focus']}")
        lines.append("")

    lines.append("---END---")
    return "\n".join(lines)

# ========== 命令处理 ==========

def cmd_add(args):
    if len(args) < 3:
        print("用法: add <代码> <名称> <类型>")
        return
    code, name, ftype = args[0], args[1], args[2]
    wl = get_watchlist()
    for f in wl:
        if f.get("code") == code:
            print(f"⚠️ {name}({code}) 已在自选列表中")
            return
    wl.append({"code": code, "name": name, "type": ftype})
    save_watchlist(wl)
    print(f"✅ 已添加 {name}({code}) [{ftype}]")

def cmd_remove(args):
    if not args:
        print("用法: remove <代码>")
        return
    wl = get_watchlist()
    new_wl = [f for f in wl if f.get("code") != args[0]]
    if len(new_wl) == len(wl):
        print(f"⚠️ 未找到代码 {args[0]}")
        return
    save_watchlist(new_wl)
    print(f"✅ 已删除 {args[0]}")

def cmd_list(args):
    wl = get_watchlist()
    if not wl:
        print("📋 自选基金列表为空")
        return
    print(f"📋 自选基金列表（共 {len(wl)} 只）")
    print("─" * 52)
    for f in wl:
        print(f"  {f.get('code', '')}  {f.get('name', '')}  [{f.get('type', '')}]")
    print("─" * 52)

def cmd_webhook(args):
    if not args:
        print("用法: webhook <URL>")
        return
    cfg = get_config()
    cfg["webhook_url"] = args[0]
    if "feishu" in args[0].lower():
        cfg["feishu_webhook"] = args[0]
    save_config(cfg)
    print("✅ Webhook 已设置")

def cmd_monitor(args):
    push = "--wechat" in args or "--feishu" in args or "--push" in args
    report = gen_monitor_report_all()
    print(report)
    if push:
        results = push_to_channels(report)
        for name, ok in results:
            print(f"{'✅' if ok else '❌'} {name}推送{'成功' if ok else '失败'}")

def cmd_monitor_single(args):
    if not args:
        print("用法: monitor-single <代码>")
        return
    code = args[0]
    wl = get_watchlist()
    fund = next((f for f in wl if f.get("code") == code), None)
    if not fund:
        print(f"⚠️ 未找到 {code}")
        return
    cfg = get_config()
    mp = cfg.get("per_fund_ma", {}).get(code, cfg.get("default_ma_period", 20))
    nav_list = fetch_nav(code)
    if not nav_list:
        print(f"📊 基金监控 [{get_now().strftime('%Y-%m-%d %H:%M')}]\n  ❌ 数据获取失败")
        return
    result = calc_pressure_support(nav_list, mp)
    if not result:
        print(f"📊 基金监控 [{get_now().strftime('%Y-%m-%d %H:%M')}]\n  ❌ 数据不足")
        return
    print(f"📊 基金监控 [{get_now().strftime('%Y-%m-%d %H:%M')}]")
    print("─" * 52)
    print(f"  【{fund.get('name','')}】{code}")
    print(f"    最新净值：{result['current']}")
    print(f"    压 力 位：{result['pressure']}")
    print(f"    支 撑 位：{result['support']}")
    print(f"    重点关注：{result['focus']}")
    print("─" * 52)
    print("end")

def cmd_feishu(args):
    report = gen_feishu_report()
    print(report)
    cfg = get_config()
    feishu_url = cfg.get("feishu_webhook", "")
    if feishu_url:
        ok = send_feishu(feishu_url, report)
        print(f"{'✅' if ok else '❌'} 飞书推送{'成功' if ok else '失败'}")
    else:
        print("⚠️ 未配置飞书webhook")

def cmd_doctor(args):
    print(f"🏥 系统自检报告 [{get_now().strftime('%Y-%m-%d %H:%M')}]")
    print("─" * 52)
    print(f"  ✅ Python版本：{sys.version.split()[0]}")
    wl = get_watchlist()
    print(f"  ✅ watchlist.json：{len(wl)}只基金")
    cfg = get_config()
    print(f"  ✅ config.json：{'格式正确' if cfg else '⚠️ 异常'}")
    try:
        _http_get("http://fund.eastmoney.com/js/000001.js", timeout=5)
        print("  ✅ 天天基金API：连通正常")
    except Exception:
        print("  ⚠️ 天天基金API：连接失败")
    print("─" * 52)

def cmd_alert_threshold(args):
    if not args:
        print("用法: alert threshold <%>")
        return
    ac = get_alert_config()
    ac["default_threshold"] = float(args[0])
    save_alert_config(ac)
    print(f"✅ 全局涨跌幅阈值设为 ±{args[0]}%")

def cmd_hold_add(args):
    if len(args) < 3:
        print("用法: hold add <代码> <成本价> <份额>")
        return
    code, cost, shares = args[0], float(args[1]), float(args[2])
    h = get_holdings()
    if code in h:
        old = h[code]
        total_shares = old.get("shares", 0) + shares
        avg_cost = (old.get("cost", 0) * old.get("shares", 0) + cost * shares) / total_shares
        h[code] = {"cost": round(avg_cost, 4), "shares": total_shares}
        print(f"✅ 均价更新：{avg_cost:.4f}，总份额：{total_shares}")
    else:
        h[code] = {"cost": cost, "shares": shares}
        print(f"✅ 已记录 {code} 成本 {cost} 份额 {shares}")
    save_holdings(h)

def cmd_hold_list(args):
    h = get_holdings()
    if not h:
        print("📋 持仓列表为空")
        return
    print("📋 持仓列表")
    print("─" * 52)
    for code, info in h.items():
        print(f"  {code}  成本：{info['cost']}  份额：{info['shares']}")
    print("─" * 52)

def cmd_ma_period(args):
    if not args:
        print("用法: ma period <天数>")
        return
    cfg = get_config()
    cfg["default_ma_period"] = int(args[0])
    save_config(cfg)
    print(f"✅ 全局均线周期设为 {args[0]}日")

def cmd_ma_set(args):
    if len(args) < 2:
        print("用法: ma set <代码> <天数>")
        return
    cfg = get_config()
    cfg.setdefault("per_fund_ma", {})[args[0]] = int(args[1])
    save_config(cfg)
    print(f"✅ {args[0]} 均线周期设为 {args[1]}日")

def cmd_version(args):
    print(f"fund-005 {VERSION}")
    print("基金监控技能 · 多源API降级 · 独立任务模式 · 涨跌幅告警 · 持仓盈亏追踪")

def main():
    ensure_dirs()
    if len(sys.argv) < 2:
        print("用法: python fund_monitor_wechat.py <命令> [参数...]")
        print("  常用命令: add, remove, list, monitor, feishu, webhook, doctor, --version")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "add": cmd_add,
        "remove": cmd_remove,
        "list": cmd_list,
        "webhook": cmd_webhook,
        "monitor": cmd_monitor,
        "monitor-single": cmd_monitor_single,
        "feishu": cmd_feishu,
        "doctor": cmd_doctor,
        "alert": lambda a: cmd_alert_threshold(a[1:]) if a and a[0] == "threshold" else print("用法: alert threshold <%>"),
        "hold": lambda a: cmd_hold_add(a[1:]) if a and a[0] == "add" else (cmd_hold_list(a) if a and a[0] == "list" else print("用法: hold add/list")),
        "ma": lambda a: cmd_ma_period(a[1:]) if a and a[0] == "period" else (cmd_ma_set(a[1:]) if a and a[0] == "set" else print("用法: ma period/set")),
        "--version": cmd_version,
        "-v": cmd_version,
    }

    if cmd in commands:
        try:
            commands[cmd](args)
        except Exception as e:
            print(f"❌ 执行出错: {e}")
            traceback.print_exc()
            log(f"Error in {cmd}: {e}\n{traceback.format_exc()}")
    else:
        print(f"❌ 未知命令: {cmd}")
        print("可用命令: add, remove, list, monitor, feishu, webhook, doctor, alert, hold, ma, --version")

if __name__ == "__main__":
    main()
