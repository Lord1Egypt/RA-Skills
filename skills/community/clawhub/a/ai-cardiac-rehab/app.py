#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI心脏康复助手 — 病人安全增强版
==================================
基于 ACC/AHA 2023 心脏康复指南的安全管理 Web 应用。
安全特性：输入校验、绝对禁忌阻断、风险分层、症状预警。
数据全部存储在本地 SQLite，不上传云端。

合规声明：本工具不提供医疗诊断，康复方案须经心脏科医生审核。
"""

import hashlib
import os
import re
import secrets
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template_string, request, redirect, session, url_for, flash

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    print("=" * 60)
    print("安全错误：未设置 SECRET_KEY 环境变量。")
    print("设置：export SECRET_KEY=<随机字符串>")
    print("=" * 60)
    import sys
    sys.exit(1)
app.secret_key = secret_key
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
if os.getenv('HTTPS'): app.config['SESSION_COOKIE_SECURE'] = True

# ---------- 辅助函数 ----------
def hash_password(pwd, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt.encode(), 100000)
    return f"{salt}${dk.hex()}"


def validate_clinical_inputs(age, hr, bp_sys, bp_dia, ef, exercise_min):
    errors = []
    if age and (age < 18 or age > 120):
        errors.append("年龄需在18-120岁之间")
    if hr and (hr < 30 or hr > 220):
        errors.append("心率超出生理范围(30-220)")
    if bp_sys and (bp_sys < 40 or bp_sys > 250):
        errors.append("收缩压超出范围(40-250mmHg)")
    if bp_dia and (bp_dia < 20 or bp_dia > 150):
        errors.append("舒张压超出范围(20-150mmHg)")
    if ef and (ef < 10 or ef > 80):
        errors.append("射血分数EF应在10-80%之间")
    if exercise_min and (exercise_min < 0 or exercise_min > 300):
        errors.append("运动时长应在0-300分钟")
    return errors


def get_user_profile(user_id):
    conn = sqlite3.connect('cardio_rehab.db')
    c = conn.cursor()
    c.execute('SELECT * FROM profiles WHERE user_id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'age': row[1], 'gender': row[2], 'heart_disease': row[3],
            'ef': row[4], 'comorbid': row[5], 'resting_hr': row[6],
            'resting_bp_sys': row[7], 'resting_bp_dia': row[8], 'medications': row[9]
        }
    return None


def get_recent_logs(user_id, days=7):
    conn = sqlite3.connect('cardio_rehab.db')
    c = conn.cursor()
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    c.execute(
        '''SELECT log_date, symptoms, hr, bp_sys, bp_dia, exercise_min, notes
           FROM daily_logs WHERE user_id=? AND log_date>=? ORDER BY log_date DESC''',
        (user_id, start_date))
    logs = [{
        'date': r[0], 'symptoms': r[1], 'hr': r[2], 'bp_sys': r[3],
        'bp_dia': r[4], 'exercise_min': r[5], 'notes': r[6]
    } for r in c.fetchall()]
    conn.close()
    return logs


def check_symptom_alerts(logs):
    """基于症状的红色/橙色预警"""
    red_flags = []
    orange_flags = []
    for log in logs:
        sym = (log['symptoms'] or '').lower()
        if any(x in sym for x in ['胸痛', '胸闷压榨', '呼吸困难静息', '晕厥', '黑朦']):
            red_flags.append(log['date'])
        elif any(x in sym for x in ['心悸', '疲劳异常', '头晕活动时']):
            orange_flags.append(log['date'])
    return red_flags, orange_flags


# ---------- AI 安全决策引擎 ----------
def ai_safe_cardiac_rehab(user_id):
    profile = get_user_profile(user_id)
    if not profile:
        return {'error': '请先完善健康档案'}, None

    logs = get_recent_logs(user_id, 7)
    red_dates, orange_dates = check_symptom_alerts(logs)

    age = profile['age']
    ef = profile['ef'] or 55
    comorbid = (profile['comorbid'] or '').lower()
    heart_disease = (profile['heart_disease'] or '').lower()
    resting_hr = profile['resting_hr'] or 70
    resting_bp_sys = profile['resting_bp_sys'] or 120
    medications = (profile['medications'] or '').lower()

    # ----- 绝对禁忌与紧急处理 -----
    emergency = None
    contraindication = False

    if ef and ef < 30:
        emergency = "EF<30%，猝死风险高，禁止运动，立即心内科专科评估！"
        contraindication = True
    elif '不稳定心绞痛' in heart_disease or '急性心肌梗死1月内' in heart_disease:
        emergency = "不稳定心绞痛或急性心梗急性期，禁止运动，需住院治疗。"
        contraindication = True
    elif red_dates:
        emergency = f"近7天出现{len(red_dates)}次高危症状（胸痛/晕厥等），立即暂停运动并就医。"
        contraindication = True
    elif resting_bp_sys > 180 or resting_bp_sys < 90:
        emergency = f"静息收缩压{resting_bp_sys}mmHg，运动风险极高，需血压控制稳定后再评估。"
        contraindication = True

    if contraindication:
        return {
            'emergency': emergency,
            'exercise_advice': '严格执行医疗监护，暂停康复运动。'
        }, logs

    # ----- 风险分层 -----
    if ef < 40 or '心衰' in comorbid:
        risk = '高'
        intensity = '低强度 (RPE 9-11)'
        hr_target_range = '<100 次/分'
    elif ef < 50 or '糖尿病' in comorbid or '高血压' in comorbid:
        risk = '中'
        intensity = '中等强度 (RPE 12-14)'
        max_hr = 208 - 0.7 * age
        beta_blocker = any(x in medications for x in ['倍他乐克', '比索洛尔', '卡维地洛', '普萘洛尔'])
        if beta_blocker:
            max_hr = max_hr * 0.8
            hr_adjust_msg = "（因使用β阻滞剂，靶心率已下调20%）"
        else:
            hr_adjust_msg = ""
        target_low = int((max_hr - resting_hr) * 0.4 + resting_hr)
        target_high = int((max_hr - resting_hr) * 0.6 + resting_hr)
        hr_target_range = f'{target_low}-{target_high}次/分 {hr_adjust_msg}'
    else:
        risk = '低'
        intensity = '中等强度 (RPE 12-15)'
        max_hr = 208 - 0.7 * age
        target_low = int((max_hr - resting_hr) * 0.5 + resting_hr)
        target_high = int((max_hr - resting_hr) * 0.7 + resting_hr)
        hr_target_range = f'{target_low}-{target_high}次/分'

    # 运动处方生成
    if resting_bp_sys > 160:
        exercise_advice = '收缩压>160mmHg，暂缓运动，优先降压治疗。'
    else:
        exercise_advice = (
            f'建议每周5天，每次20-40分钟有氧运动（快走/骑车/游泳），'
            f'运动心率控制在{hr_target_range}，{intensity}。'
        )
    if orange_dates:
        exercise_advice += '注意：近周有活动时心悸/异常疲劳，请降低强度50%并观察症状。'

    # 药物依从性
    med_reminder = ''
    if '阿司匹林' not in medications and '氯吡格雷' not in medications:
        med_reminder = '未记录抗血小板药物，二级预防至关重要，请咨询医生。'
    if '他汀' not in medications:
        med_reminder += '他汀类药物可稳定斑块，建议评估使用。'

    call_doctor = ''
    if risk == '高' or orange_dates:
        call_doctor = '建议每周至少复诊一次，运动时需有人陪同。'

    return {
        'risk_level': risk,
        'intensity': intensity,
        'target_hr': hr_target_range,
        'exercise_advice': exercise_advice,
        'medication_reminder': med_reminder,
        'monitoring_tips': (
            f'晨起静息心率{resting_hr}，'
            f'如静息心率较平时增加>20次/分，当日运动减量。'
        ),
        'call_doctor': call_doctor,
        'has_emergency': False,
    }, logs


# ---------- 数据库初始化 ----------
def init_db():
    with sqlite3.connect('cardio_rehab.db') as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                age INTEGER,
                gender TEXT,
                heart_disease TEXT,
                ef INTEGER,
                comorbid TEXT,
                resting_hr INTEGER,
                resting_bp_sys INTEGER,
                resting_bp_dia INTEGER,
                medications TEXT,
                updated_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                log_date DATE,
                symptoms TEXT,
                hr INTEGER,
                bp_sys INTEGER,
                bp_dia INTEGER,
                exercise_min INTEGER,
                exercise_type TEXT,
                notes TEXT,
                UNIQUE(user_id, log_date),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')


init_db()


# ---------- HTML 模板 ----------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>安全AI心脏康复 | 患者安全优先</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-XrA6H6ViV4s0F2r6M6SH6GtRXk5I5U2C4Jf+0I0E5U5I5U5I5U5I5U5" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" integrity="sha384-vJhNT1P7F1Mh7lsKLEsG6D8lzOBH0t2mcnOZFK1kYfp7xtOeRSkE+IGlO3QlP0N" crossorigin="anonymous"></script>
<style>
body{background:#eef2f3; padding-top:20px;}
.card{border-radius:20px; margin-bottom:20px;}
</style>
</head>
<body>
<div class="container">
<div class="text-center mb-3"><h2>心脏康复AI <small class="text-muted">安全·个体化·循证</small></h2></div>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}{% for cat,msg in messages %}<div class="alert alert-{{ cat }} alert-dismissible">{{ msg }}</div>{% endfor %}{% endif %}
{% endwith %}

{% if session.user_id %}
<div class="d-flex justify-content-end"><a href="/logout" class="btn btn-outline-danger">退出</a></div>

<!-- 健康档案 -->
<div class="card shadow-sm">
<div class="card-header bg-primary text-white">患者档案（必须如实填写）</div>
<div class="card-body">
<form method="POST" action="/save_profile">
<div class="row g-2">
<div class="col-md-3"><label>年龄</label><input type="number" name="age" class="form-control" value="{{ profile.age if profile else '' }}" required></div>
<div class="col-md-2"><label>性别</label><select name="gender" class="form-control"><option>男</option><option>女</option></select></div>
<div class="col-md-4"><label>心脏病诊断</label><input name="heart_disease" class="form-control" value="{{ profile.heart_disease if profile else '心肌梗死后' }}" placeholder="心肌梗死后/心衰/不稳定心绞痛等"></div>
<div class="col-md-3"><label>左室射血分数EF(%)</label><input type="number" name="ef" class="form-control" value="{{ profile.ef if profile else 55 }}" step="1"></div>
</div>
<div class="row g-2 mt-2">
<div class="col-md-5"><label>合并症</label><input name="comorbid" class="form-control" value="{{ profile.comorbid if profile else '' }}" placeholder="高血压/糖尿病/心衰/慢阻肺"></div>
<div class="col-md-2"><label>静息心率</label><input type="number" name="resting_hr" class="form-control" value="{{ profile.resting_hr if profile else 70 }}"></div>
<div class="col-md-2"><label>静息收缩压</label><input type="number" name="resting_bp_sys" class="form-control" value="{{ profile.resting_bp_sys if profile else 120 }}"></div>
<div class="col-md-3"><label>药物（通用名）</label><input name="medications" class="form-control" value="{{ profile.medications if profile else '' }}" placeholder="阿司匹林 倍他乐克 他汀"></div>
</div>
<button type="submit" class="btn btn-primary mt-3">保存并获取安全建议</button>
</form>
</div></div>

<!-- AI 安全建议卡片 -->
<div class="card shadow-sm">
<div class="card-header bg-success text-white">AI安全决策引擎（基于ACC/AHA指南）</div>
<div class="card-body">
{% if ai_advice %}
{% if ai_advice.emergency %}
<div class="alert alert-danger"><strong>安全警告：{{ ai_advice.emergency }}</strong></div>
{% else %}
<div class="alert alert-{{ 'danger' if ai_advice.risk_level=='高' else 'warning' if ai_advice.risk_level=='中' else 'info' }}">
<strong>风险等级：{{ ai_advice.risk_level }}级</strong> | 推荐强度：{{ ai_advice.intensity }}<br>
运动处方：{{ ai_advice.exercise_advice }}<br>
靶心率：{{ ai_advice.target_hr }}<br>
{% if ai_advice.medication_reminder %}<span class="text-warning">{{ ai_advice.medication_reminder }}</span><br>{% endif %}
{{ ai_advice.monitoring_tips }}<br>
{% if ai_advice.call_doctor %}{{ ai_advice.call_doctor }}{% endif %}
</div>
{% endif %}
{% else %}<p class="text-muted">请先填写完整档案（尤其EF值和诊断）。</p>{% endif %}
</div></div>

<!-- 每日记录 -->
<div class="row">
<div class="col-md-6">
<div class="card">
<div class="card-header">今日安全记录</div>
<div class="card-body">
<form method="POST" action="/add_log" onsubmit="return validateLog()">
<input type="hidden" name="log_date" value="{{ today }}">
<label>症状（可多选，用逗号分隔）</label><input name="symptoms" class="form-control" placeholder="胸痛,呼吸困难,心悸,疲劳,头晕,无">
<label>心率（次/分）</label><input type="number" name="hr" class="form-control" required>
<label>血压（mmHg）</label>
<div class="row"><div class="col"><input name="bp_sys" placeholder="收缩压" required></div><div class="col"><input name="bp_dia" placeholder="舒张压" required></div></div>
<label>安全运动时长（分钟）</label><input type="number" name="exercise_min" class="form-control" value="0">
<label>运动类型</label><input name="exercise_type" class="form-control" placeholder="快走/骑车/抗阻">
<button type="submit" class="btn btn-secondary mt-2">保存今日记录</button>
</form>
</div></div></div>

<div class="col-md-6">
<div class="card">
<div class="card-header">心率趋势（近7天）</div>
<div class="card-body"><canvas id="hrChart"></canvas></div>
</div></div></div>

<div class="card mt-2">
<div class="card-header">患者安全须知</div>
<div class="card-body small text-muted">
本AI建议不能替代医生面对面诊疗。如有胸痛、呼吸困难、晕厥前兆，立即停止活动并拨打120。运动前后监测血压心率。
</div></div>

<script>
const hrData = {{ hr_chart_data | tojson | safe }};
if(hrData && hrData.labels.length){
  new Chart(document.getElementById('hrChart'), {
    type:'line',
    data:{ labels: hrData.labels, datasets:[{ label:'晨间心率', data: hrData.hr, borderColor:'#d9534f', fill:false }] }
  });
}
function validateLog(){
  let hr = document.querySelector('input[name="hr"]').value;
  let bp_sys = document.querySelector('input[name="bp_sys"]').value;
  if(hr<30 || hr>200) { alert('心率超出安全范围(30-200)'); return false; }
  if(bp_sys<60 || bp_sys>250) { alert('收缩压异常(60-250)'); return false; }
  return true;
}
</script>

{% else %}
<!-- 登录 -->
<div class="row justify-content-center">
<div class="col-md-5">
<div class="card">
<div class="card-body">
<h4>患者/医师登录</h4>
<form method="POST" action="/login">
<input type="text" name="username" class="form-control mb-2" placeholder="用户名" required>
<input type="password" name="password" class="form-control mb-2" placeholder="密码" required>
<button class="btn btn-primary w-100" type="submit">登录/自动注册（安全加密）</button>
</form>
</div></div></div></div>
{% endif %}

</div>
</body>
</html>
'''


# ---------- Web 路由 ----------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template_string(HTML_TEMPLATE, session=session)

    profile = get_user_profile(session['user_id'])
    if profile:
        ai_advice, logs = ai_safe_cardiac_rehab(session['user_id'])
        hr_chart = {
            'labels': [log['date'] for log in reversed(logs)],
            'hr': [log['hr'] for log in reversed(logs) if log['hr']]
        }
    else:
        ai_advice = None
        hr_chart = {'labels': [], 'hr': []}

    return render_template_string(
        HTML_TEMPLATE,
        session=session,
        profile=profile,
        ai_advice=ai_advice,
        today=datetime.now().strftime('%Y-%m-%d'),
        hr_chart_data=hr_chart
    )


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password']
    conn = sqlite3.connect('cardio_rehab.db')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username=?', (username,))
    user = c.fetchone()
    if user:
        stored = user[1]
        if '$' in stored:
            parts = stored.split('$')
            hashed_check = hash_password(password, parts[0])
            if hashed_check != stored:
                flash('密码错误', 'danger')
                return redirect(url_for('index'))
        user_id = user[0]
    else:
        hashed = hash_password(password)
        c.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, hashed))
        conn.commit()
        user_id = c.lastrowid
    conn.close()
    session['user_id'] = user_id
    flash('登录成功，请完善档案以保证安全评估', 'success')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/save_profile', methods=['POST'])
@login_required
def save_profile():
    try:
        age = int(request.form.get('age', 0))
        ef = int(request.form.get('ef', 55))
        resting_hr = int(request.form.get('resting_hr', 70))
        resting_bp_sys = int(request.form.get('resting_bp_sys', 120))
        errors = validate_clinical_inputs(age, resting_hr, resting_bp_sys, None, ef, None)
        if errors:
            for err in errors:
                flash(err, 'danger')
            return redirect(url_for('index'))
        conn = sqlite3.connect('cardio_rehab.db')
        c = conn.cursor()
        c.execute(
            '''INSERT OR REPLACE INTO profiles
               (user_id, age, gender, heart_disease, ef, comorbid, resting_hr, resting_bp_sys, resting_bp_dia, medications, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)''',
            (session['user_id'], age, request.form.get('gender'),
             request.form.get('heart_disease'), ef, request.form.get('comorbid'),
             resting_hr, resting_bp_sys, request.form.get('resting_bp_dia'),
             request.form.get('medications')))
        conn.commit()
        conn.close()
        flash('档案已更新，AI建议已基于最新安全规则重新生成', 'success')
    except Exception as e:
        flash(f'保存失败: {str(e)}', 'danger')
    return redirect(url_for('index'))


@app.route('/add_log', methods=['POST'])
@login_required
def add_log():
    log_date = request.form.get('log_date', datetime.now().strftime('%Y-%m-%d'))
    hr = request.form.get('hr', type=int)
    bp_sys = request.form.get('bp_sys', type=int)
    bp_dia = request.form.get('bp_dia', type=int)
    exercise_min = request.form.get('exercise_min', 0, type=int)
    errors = validate_clinical_inputs(None, hr, bp_sys, bp_dia, None, exercise_min)
    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('index'))
    conn = sqlite3.connect('cardio_rehab.db')
    c = conn.cursor()
    c.execute(
        '''INSERT OR REPLACE INTO daily_logs
           (user_id, log_date, symptoms, hr, bp_sys, bp_dia, exercise_min, exercise_type, notes)
           VALUES (?,?,?,?,?,?,?,?,?)''',
        (session['user_id'], log_date, request.form.get('symptoms'),
         hr, bp_sys, bp_dia, exercise_min, request.form.get('exercise_type'), ''))
    conn.commit()
    conn.close()
    flash('今日记录已保存，重新评估安全状态', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
