"""AI糖尿病康复助手-API服务"""
import os, sys, logging
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify
from core import (GLUCOSE_CRITICAL_HIGH, GLUCOSE_CRITICAL_LOW, GLUCOSE_HYPO, MAX_BOLUS,
                  glucose_safety, get_profile, user_records, safe_float, Coach)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("FATAL: API_KEY environment variable is required. Set a strong key before starting.")
    sys.exit(1)

app = Flask(__name__)
audit = logging.getLogger("audit")
coach = Coach()

def require_auth(f):
    @wraps(f)
    def dec(*a, **kw):
        if request.headers.get("X-API-Key") != API_KEY:
            return jsonify({"error": "unauthorized"}), 401
        return f(*a, **kw)
    return dec

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "active"})

@app.route('/profile', methods=['GET','POST'])
@require_auth
def profile():
    uid = request.args.get('user_id') or (request.json.get('user_id') if request.method=='POST' else None)
    if not uid: return jsonify({"error": "user_id required"}), 400
    if request.method == 'GET': return jsonify({"user_id": uid, **get_profile(uid)})
    data = request.get_json()
    p = get_profile(uid)
    if 'target' in data: p['target'] = safe_float(data['target'], 6.0, 4.0, 10.0)
    if 'cf' in data: p['cf'] = safe_float(data['cf'], 2.5, 1.0, 20.0)
    if 'ratio' in data: p['ratio'] = safe_float(data['ratio'], 10.0, 5.0, 30.0)
    if 'meds' in data and isinstance(data['meds'], list): p['meds'] = data['meds']
    audit.info(f"Profile updated {uid}")
    return jsonify({"status": "updated", **p})

@app.route('/record', methods=['POST'])
@require_auth
def record():
    data = request.get_json()
    uid = data.get('user_id', 'default')
    g = safe_float(data.get('glucose'), 0.0)
    _, lvl, _ = glucose_safety(g)
    if lvl == "critical": audit.warning(f"Critical glucose {g} for {uid}")
    rec = {"ts": data.get('timestamp', datetime.now().isoformat()), "g": g,
           "carbs": safe_float(data.get('meal_carbs'), 0, 0, 300),
           "exercise": safe_float(data.get('exercise_minutes'), 0, 0, 240),
           "insulin": safe_float(data.get('insulin_dose'), 0, 0, MAX_BOLUS)}
    user_records.setdefault(uid, []).append(rec)
    return jsonify({"status": "success", "id": len(user_records[uid])-1}), 201

@app.route('/advice', methods=['POST'])
@require_auth
def advice():
    data = request.get_json(); g = safe_float(data.get('glucose'), 0)
    if g <= 0: return jsonify({"error": "valid glucose required"}), 400
    _, lvl, msg = glucose_safety(g)
    if lvl == "critical": return jsonify(coach.emergency(g, msg))
    return jsonify({"glucose": g, "level": lvl, "message": msg,
                    "diet": coach.diet(g, data.get('meal_type', 'general')),
                    "exercise": coach.exercise(g),
                    "disclaimer": "基于临床指南，请结合医生意见"})

@app.route('/insulin', methods=['POST'])
@require_auth
def insulin():
    data = request.get_json(); uid = data.get('user_id')
    if not uid: return jsonify({"error": "user_id required"}), 400
    curr = safe_float(data.get('current_glucose'), 0)
    if curr <= 0: return jsonify({"error": "current_glucose required"}), 400
    return jsonify(coach.insulin(uid, curr, safe_float(data.get('carbs_grams'), 0),
                                 safe_float(data.get('on_board_insulin'), 0)))

@app.route('/risk/<uid>', methods=['GET'])
@require_auth
def risk(uid):
    return jsonify({"user_id": uid, **coach.risk(uid)})

@app.route('/summary/<uid>', methods=['GET'])
@require_auth
def summary(uid):
    recs = user_records.get(uid, [])
    if not recs: return jsonify({"tips": ["开始记录血糖"]})
    recent = recs[-5:]; avg = None; hypo_flag = False
    for r in recent:
        if r.get('g',0) > 0:
            avg = r['g'] if avg is None else (avg + r['g'])/2
            if r['g'] < GLUCOSE_HYPO: hypo_flag = True
    tips = []
    if hypo_flag: tips.append("近期低血糖，随身带糖")
    if avg and avg > 8.5: tips.append("血糖偏高，增加运动或复诊")
    if not tips: tips.append("保持平稳")
    return jsonify({"recent": recent, "avg_glucose": round(avg,1) if avg else None, "tips": tips})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("BIND_HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=False)
