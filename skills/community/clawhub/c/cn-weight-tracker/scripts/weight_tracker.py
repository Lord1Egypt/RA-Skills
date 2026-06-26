#!/usr/bin/env python3
"""
cn-weight-tracker 体重追踪技能
"""
import json, os, sys, re
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.qclaw/skills/cn-weight-tracker/data")
DATA_FILE = os.path.join(DATA_DIR, "weights.json")

def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"height": None, "unit": "kg", "target": None, "records": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_weight(text):
    """从文本中提取体重值（kg）"""
    # 带kg/公斤/千克
    m = re.search(r'(\d+\.?\d*)\s*(?:kg|公斤|千克)', text, re.IGNORECASE)
    if m: return float(m.group(1))
    # 斤 -> kg
    m = re.search(r'(\d+\.?\d*)\s*斤', text)
    if m: return float(m.group(1)) / 2
    # 目标体重70（无单位）
    m = re.search(r'[\u76ee\u6807].*?(\d+\.?\d*)', text)
    if m: return float(m.group(1))
    # 记录体重74.8 / 体重74.8（无单位）
    m = re.search(r'(?:体重|称了|记录.*?)\s*(\d+\.?\d*)', text)
    if m: return float(m.group(1))
    # 纯数字开头
    m = re.search(r'^\s*(\d+\.?\d*)\s*$', text)
    if m: return float(m.group(1))
    return None

def get_height(text):
    """从文本中提取身高(cm)"""
    m = re.search(r'(\d+\.?\d*)\s*(?:cm|厘米)', text, re.IGNORECASE)
    if m: return float(m.group(1))
    m = re.search(r'(\d+)\s*[米m]\s*(\d+)', text, re.IGNORECASE)
    if m: return float(m.group(1)) * 100 + float(m.group(2))
    m = re.search(r'^(\d+\.?\d*)\s*m\b', text, re.IGNORECASE)
    if m: return float(m.group(1)) * 100
    m = re.search(r'身高\s*(\d+\.?\d*)', text, re.IGNORECASE)
    if m:
        v = float(m.group(1))
        return v if v > 3 else v * 100
    return None

def bmi_str(w, h):
    b = w / (h/100) ** 2
    c = "偏瘦" if b < 18.5 else "正常" if b < 24 else "超重" if b < 28 else "肥胖"
    e = "🟢" if b < 18.5 else "✅" if b < 24 else "🟡" if b < 28 else "🔴"
    return f"{b:.1f}（{c} {e}）"

def trend_bar(records):
    if len(records) < 2: return "需要至少2条记录"
    recs = records[-7:]
    ws = [r["weight"] for r in recs]
    lo, hi = min(ws), max(ws)
    rng = hi - lo if hi != lo else 0.5
    lines = []
    for r in recs:
        bar = "█" * max(1, min(20, int((r["weight"] - lo) / rng * 20)))
        lines.append(f"  {r['date'][5:]}  {r['weight']:5.1f} |{bar:<20}|")
    return "\n".join(lines)

def handle(text):
    data = load_data()
    t = text.strip()

    # 查询统计类
    if t in ("查体重", "体重记录", "我的体重", "查", "看") or re.match(r'^(查|看).*(体重|记录)', t):
        recs = data["records"]
        if not recs: return "暂无记录，请说「记录体重 75.5kg」"
        ws = [r["weight"] for r in recs[-7:]]
        cur, avg = ws[-1], sum(ws)/len(ws)
        chg = cur - ws[0]
        e = "📈" if chg > 0.1 else "📉" if chg < -0.1 else "➡️"
        bmi = f"\nBMI：{bmi_str(cur, data['height'])}" if data["height"] else ""
        return (f"📊 体重统计（最近{len(recs[-7:])}天）\n━━━━━━━━━━━━━━\n"
                f"当前：{cur:.1f}kg | 均：{avg:.1f}kg\n变化：{chg:+.1f}kg {e}{bmi}\n\n📈 趋势：\n{trend_bar(recs)}")

    if "趋势" in t:
        return handle("查体重")

    if "bmi" in t.lower() or "体质" in t:
        if not data["height"]: return "❓ 请先「身高175cm」"
        if not data["records"]: return "❓ 请先记录体重"
        w = data["records"][-1]["weight"]
        return f"📏 BMI\n━━━━━━━━\n身高：{data['height']:.0f}cm\n体重：{w:.1f}kg\nBMI：{bmi_str(w, data['height'])}"

    if "身高" in t:
        h = get_height(t)
        if h:
            data["height"] = h
            save_data(data)
            return f"✅ 身高 {h:.0f}cm（BMI就绪）"
        return "❓「身高175cm」或「身高1米75」"

    if "目标" in t:
        w = get_weight(t)
        if w:
            data["target"] = w
            save_data(data)
            if data["records"]:
                d = data["records"][-1]["weight"] - w
                s = f"还差{abs(d):.1f}kg" if d > 0 else "已达目标🎉"
            else:
                s = "（待记录体重后计算差距）"
            return f"🎯 目标 {w:.1f}kg（{s}）"
        return "❓「目标体重70」"

    w = get_weight(t)
    if w:
        today = datetime.now().strftime("%Y-%m-%d")
        recs = data["records"]
        if recs and recs[-1]["date"] == today:
            recs[-1]["weight"] = w
        else:
            recs.append({"date": today, "weight": w, "unit": "kg"})
        save_data(data)
        bmi_s = f"\nBMI：{bmi_str(w, data['height'])}" if data["height"] else ""
        tgt_s = ""
        if data["target"]:
            d = w - data["target"]
            tgt_s = f"\n距目标：{d:+.1f}kg"
        return f"✅ 记录 {w:.1f}kg{bmi_s}{tgt_s}"

    return ("⚖️ 体重追踪\n━━━━━━━━━━━━━━\n"
            "📝 记录：记录体重 75.5kg\n"
            "📊 查记录：查体重 / 体重记录\n"
            "📏 BMI：算BMI（需先设身高）\n"
            "🎯 目标：目标体重70\n"
            "📏 身高：身高175cm")

if __name__ == "__main__":
    print(handle(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""))
