"""AI糖尿病康复助手-核心引擎"""
import os
from datetime import datetime, timedelta

GLUCOSE_CRITICAL_LOW = float(os.getenv("CRITICAL_LOW", "2.8"))
GLUCOSE_CRITICAL_HIGH = float(os.getenv("CRITICAL_HIGH", "20.0"))
GLUCOSE_HYPO = float(os.getenv("HYPO", "3.9"))
GLUCOSE_HYPER = float(os.getenv("HYPER", "13.9"))
MAX_BOLUS = float(os.getenv("MAX_BOLUS", "15.0"))

user_profiles = {}
user_records = {}

def safe_float(v, default=0.0, lo=None, hi=None):
    try:
        v = float(v)
        if lo is not None and v < lo: v = lo
        if hi is not None and v > hi: v = hi
        return v
    except: return default

def glucose_safety(g):
    if g <= 0: return (False, "critical", "无效血糖值")
    if g < GLUCOSE_CRITICAL_LOW: return (False, "critical", f"血糖{g}mmol/L极低！立即口服15g糖并就医")
    if g > GLUCOSE_CRITICAL_HIGH: return (False, "critical", f"血糖{g}mmol/L极高！立即就医")
    if g < GLUCOSE_HYPO: return (True, "warning", f"低血糖{g}，补充15g碳水")
    if g > GLUCOSE_HYPER: return (True, "warning", f"高血糖{g}，补水防酮症")
    return (True, "info", "血糖可控")

def get_profile(uid):
    if uid not in user_profiles:
        user_profiles[uid] = {"target": 6.0, "cf": 2.5, "ratio": 10, "meds": []}
    return user_profiles[uid]

class Coach:
    @staticmethod
    def emergency(g, msg):
        return {"glucose": g, "level": "critical", "action": "立即就医",
                "message": msg, "steps": "低血糖<2.8:口服糖；高血糖>20:查酮体",
                "disclaimer": "紧急情况，请立即采取行动"}

    @staticmethod
    def risk(uid):
        recs = user_records.get(uid, [])
        if len(recs) < 3: return {"risk": "insufficient", "msg": "记录少于3次"}
        recent = [r for r in recs if datetime.fromisoformat(r['ts']) >= datetime.now() - timedelta(days=7)]
        gs = [r['g'] for r in recent if r.get('g', 0) > 0]
        if not gs: return {"risk": "no_data", "msg": "无有效血糖"}
        hypo = sum(1 for g in gs if g < GLUCOSE_HYPO)
        hyper = sum(1 for g in gs if g > GLUCOSE_HYPER)
        cri_low = sum(1 for g in gs if g < GLUCOSE_CRITICAL_LOW)
        cri_high = sum(1 for g in gs if g > GLUCOSE_CRITICAL_HIGH)
        avg = sum(gs)/len(gs)
        if cri_low or cri_high: r, m = "critical", f"{cri_low}次极低/{cri_high}次极高"
        elif hypo >= 2: r, m = "high", f"周低血糖{hypo}次"
        elif hyper >= 3: r, m = "high", f"周高血糖{hyper}次"
        elif avg > 10: r, m = "medium", "平均血糖偏高"
        elif avg < 4.5: r, m = "medium", "平均血糖偏低"
        else: r, m = "low", "控制良好"
        return {"risk": r, "msg": m, "avg_7d": round(avg,1), "hypo": hypo, "hyper": hyper}

    @staticmethod
    def diet(g, meal="general"):
        if g <= 0: return {"carbs": "30-60g", "advice": "餐前未测按标准量"}
        _, lvl, msg = glucose_safety(g)
        if lvl == "critical": return {"carbs": "暂停进食", "advice": msg}
        if g < GLUCOSE_HYPO: return {"carbs": "立即15g快速碳水", "advice": "纠正后正餐"}
        if g > GLUCOSE_HYPER: return {"carbs": "15-30g低GI碳水", "advice": "多喝水"}
        r = {"breakfast":"30-45","lunch":"45-60","dinner":"45-60","general":"30-60"}
        t = {"breakfast":"搭蛋白","lunch":"先菜后饭","dinner":"餐后散步","general":"全谷物"}
        return {"carbs": r.get(meal, r["general"])+"g", "advice": t.get(meal, t["general"])}

    @staticmethod
    def exercise(g):
        if g < 5.0: return {"safety": "禁止", "advice": f"血糖{g}，补充至5.6以上"}
        if g > 13.9: return {"safety": "仅步行", "advice": "有酮体则休息"}
        if g < 7.0: return {"safety": "最佳", "advice": "30分钟有氧运动"}
        if g <= 10.0: return {"safety": "安全", "advice": "中等强度，注意补水"}
        return {"safety": "谨慎", "advice": "携带升糖食物"}

    @staticmethod
    def insulin(uid, curr_g, carbs, onboard=0):
        _, lvl, msg = glucose_safety(curr_g)
        if lvl == "critical": return {"total": 0, "warning": f"危急值：{msg}", "disclaimer": "医疗紧急"}
        p = get_profile(uid)
        corr = max(0, (curr_g - p["target"]) / p["cf"]) if curr_g > p["target"] else 0
        corr = min(corr, MAX_BOLUS)
        meal = min(carbs / p["ratio"], MAX_BOLUS) if carbs > 0 else 0
        total = max(0, corr + meal - onboard)
        if curr_g < GLUCOSE_HYPO: total *= 0.5
        elif curr_g < 5.0: total = max(0, total - 2)
        total = min(total, MAX_BOLUS)
        warns = []
        if curr_g < GLUCOSE_HYPO or curr_g < 5.0: warns.append("血糖偏低，剂量已减")
        if curr_g > 15 and total > 8: warns.append("伴大剂量，建议就医")
        if "sglt2" in p.get("meds", []) and curr_g > 13.9: warns.append("SGLT2查酮")
        return {"total": round(total,1), "meal": round(meal,1),
                "correction": round(corr,1), "warnings": warns,
                "disclaimer": "仅供参考"}
