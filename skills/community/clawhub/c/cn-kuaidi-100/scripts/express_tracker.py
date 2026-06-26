#!/usr/bin/env python3
"""
cn-express-tracker 快递追踪技能
快递100免费接口查询，无需API Key
"""
import json
import os
import sys
import re
import requests

DATA_DIR = os.path.expanduser("~/.qclaw/skills/cn-express-tracker/data")
DATA_FILE = os.path.join(DATA_DIR, "express.json")

CARRIERS = {
    "顺丰": "shunfeng", "sf": "shunfeng", "shunfeng": "shunfeng",
    "中通": "zhongtong", "zhongtong": "zhongtong",
    "圆通": "yuantong", "yuantong": "yuantong",
    "韵达": "yunda", "yunda": "yunda",
    "申通": "shentong", "shentong": "shentong",
    "极兔": "jtexpress", "jtexpress": "jtexpress",
    "京东": "jd", "jd": "jd",
    "ems": "ems",
    "邮政": "youzheng",
    "德邦": "debangwuliu",
}

NUMBER_CARRIER = {
    "SF": "shunfeng", "ET": "jtexpress", "YT": "yuantong",
    "YD": "yunda", "ST": "shentong",
}


def load():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return {"tracking": []}


def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def extract_number(text):
    """从文本中提取快递单号"""
    # SF + 10+位数字
    m = re.search(r'SF(\d{10,18})', text, re.IGNORECASE)
    if m:
        return "SF" + m.group(1)
    # JD + 12+位数字
    m = re.search(r'JD(\d{12,20})', text, re.IGNORECASE)
    if m:
        return "JD" + m.group(1)
    # YT + 10+位数字
    m = re.search(r'YT(\d{10,20})', text, re.IGNORECASE)
    if m:
        return "YT" + m.group(1)
    # EA / RA 开头
    m = re.search(r'(EA\d{9,15}|RA\d{9,15})', text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # 纯数字 10-22位
    m = re.search(r'\b(\d{10,22})\b', text)
    if m:
        return m.group(1)
    return None


def detect(number):
    n = number.strip().upper()
    for prefix, c in NUMBER_CARRIER.items():
        if n.startswith(prefix):
            return c
    # 按位数猜
    if len(n) == 12 and n.startswith("SF"):
        return "shunfeng"
    if len(n) == 18 and n.startswith("SF"):
        return "shunfeng"
    if len(n) == 15:
        return "shunfeng"
    if len(n) == 13:
        return "yuantong"
    if len(n) == 15:
        return "jtexpress"
    return None


def extract_carrier(text):
    for kw, c in CARRIERS.items():
        if kw in text:
            return c
    return None


def query_kuaidi100(number, carrier):
    """查询快递100接口，使用SSL双层降级策略"""
    url = f"https://www.kuaidi100.com/query?type={carrier}&postid={number}&temp=0.1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.kuaidi100.com/",
    }
    
    # 第一层：标准SSL验证
    try:
        r = requests.get(url, headers=headers, timeout=10, verify=True)
        return r.json()
    except requests.exceptions.SSLError:
        # 第二层：SSL验证失败时回退（仅用于兼容老旧环境）
        try:
            r = requests.get(url, headers=headers, timeout=10, verify=True)
            return r.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"网络请求失败: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"网络请求失败: {str(e)}"}


def format_result(number, carrier, data):
    state_map = {
        "0": "🚚 在途", "1": "📦 已揽收", "2": "🛵 派送中",
        "3": "✅ 已签收", "4": "↩️ 退回中", "5": "⚠️ 问题件",
    }
    if data.get("status") != "200":
        return f"❌ 查询失败：{data.get('message', '未知')}\n📦 {number}（{carrier}）\n💡 确认单号正确"

    state = str(data.get("state", "0"))
    st = state_map.get(state, f"📍 状态{state}")
    items = data.get("data", [])
    latest = items[0] if items else {}
    lines = [f"{st} {number}（{carrier}）", "━━━━━━━━━━━━━━"]
    if latest:
        lines.append(f"📍 {latest.get('context', '')}")
        lines.append(f"🕐 {latest.get('ftime', latest.get('time', ''))}")
    if len(items) > 1:
        lines.append("\n📋 历史：")
        for i in items[1:5]:
            lines.append(f"  {i.get('ftime', i.get('time',''))} {i.get('context','')}")
    return "\n".join(lines)


def handle(text):
    data = load()
    t = text.strip()
    num = extract_number(t)

    # 查所有
    if t in ("查快递", "快递状态", "我的快递", "快递", "所有快递") or re.match(r'^(查|我的|看)\s*快递', t):
        if not data["tracking"]:
            return "📦 暂无追踪快递\n━━━━━━━━━━━━━━\n📝 添加：添加快递 SF1234567890\n🔍 查询：查 单号"
        lines = ["📦 快递追踪\n━━━━━━━━━━━━━━"]
        for item in data["tracking"]:
            n = item["number"]
            c = item["carrier"]
            s = item.get("last_status", "未知")
            tt = item.get("last_time", "")[:10]
            lines.append(f"🏢 {c} | {n}\n   📍 {s} {tt}\n")
        return "\n".join(lines).strip()

    # 添加
    if ("添加" in t or "新增" in t) and num:
        carrier = extract_carrier(t) or detect(num)
        if not carrier:
            return f"❓ 无法识别公司，请「添加快递 {num} 公司:顺丰」"
        result = query_kuaidi100(num, carrier)
        last_s = last_t = "未知"
        if "data" in result and result["data"]:
            last_s = result["data"][0].get("context", "未知")
            last_t = result["data"][0].get("ftime", "")
        existing = [i for i in data["tracking"] if i["number"] == num]
        if existing:
            existing[0].update({"carrier": carrier, "last_status": last_s, "last_time": last_t})
            save(data)
            return f"♻️ 更新 {num}（{carrier}）\n📍 {last_s}"
        data["tracking"].append({"number": num, "carrier": carrier, "last_status": last_s, "last_time": last_t})
        save(data)
        return f"✅ 已添加\n━━━━━━━━━━━━━━\n📦 {num}\n🏢 {carrier}\n📍 {last_s}"

    # 删除
    if any(k in t for k in ["删除", "取消追踪", "移除"]):
        if not num:
            return "❓ 请提供单号：删除快递 单号"
        before = len(data["tracking"])
        data["tracking"] = [i for i in data["tracking"] if i["number"] != num]
        save(data)
        return f"{'✅' if len(data['tracking']) < before else '❓ 未找到'} 已删除 {num}"

    # 清除
    if any(k in t for k in ["清除", "清空"]):
        n = len(data["tracking"])
        data["tracking"] = []
        save(data)
        return f"🗑️ 已清除 {n} 条"

    # 查询单号
    if num:
        carrier = extract_carrier(t) or detect(num)
        if not carrier:
            return f"❓ 无法识别公司，请「查快递 {num} 公司:顺丰」"
        result = query_kuaidi100(num, carrier)
        return format_result(num, carrier, result)

    return ("📦 快递追踪\n━━━━━━━━━━━━━━\n"
            "📝 添加：添加快递 SF1234567890\n"
            "🔍 查询：查快递 / 查 单号\n"
            "📋 列表：我的快递\n"
            "🗑️ 删除：删除快递 单号")


if __name__ == "__main__":
    print(handle(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""))
