from flask import Flask, render_template, request, jsonify, send_file, abort, Response
import sqlite3
import os
import zipfile
import shutil
import json
import time
import threading
import io
import csv
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
DB_PATH = 'emails.db'
BACKUP_DIR = 'backups'
CONFIG_PATH = 'config.json'

# 預設設定
DEFAULT_CONFIG = {
    "allowed_ips": ["127.0.0.1", "localhost", "::1"],
    "admin_password": "change_me_now",
    "backup_interval_days": 3,
    "backup_hour": 2,
    "max_backups": 5,
    "last_backup_date": ""
}

def load_config():
    # 修復 Bug：深拷貝預設值，避免記憶體污染導致 IP 刪除後不斷復活
    config = dict(DEFAULT_CONFIG)
    config['allowed_ips'] = list(DEFAULT_CONFIG['allowed_ips'])
    
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                for key, value in file_config.items():
                    config[key] = value
        except:
            pass
    return config

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_client_ip():
    return request.remote_addr

def is_localhost(ip):
    return ip in ["127.0.0.1", "localhost", "::1"]

# --- 安全驗證模組 ---

def check_auth(username, password):
    config = load_config()
    return username == 'admin' and password == config.get("admin_password", "change_me_now")

def authenticate():
    return Response(
        '此操作需要管理員權限。\n請輸入帳號 (admin) 與設定檔中的密碼。', 401,
        {'WWW-Authenticate': 'Basic realm="Admin Access"'})

def requires_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_localhost(get_client_ip()):
            abort(403, description="非本機 IP 禁止存取管理功能")
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- 備份與還原邏輯 ---

def export_to_json():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash, subject, sender, recipient, sent_time, body, file_path FROM emails")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def import_from_json(data_list):
    conn = get_db_connection()
    cursor = conn.cursor()
    new_count = 0
    for item in data_list:
        try:
            file_path = item.get('file_path', '')
            if '..' in file_path or (file_path and not file_path.lower().endswith('.eml')):
                file_path = "[SECURITY_RESTRICTED_INVALID_PATH]"

            cursor.execute('''
                INSERT OR IGNORE INTO emails (file_hash, subject, sender, recipient, sent_time, body, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item['file_hash'], item['subject'], item['sender'], item['recipient'], item['sent_time'], item['body'], file_path))
            if cursor.rowcount > 0:
                new_count += 1
        except Exception as e:
            continue
    conn.commit()
    conn.close()
    return new_count

def perform_backup(is_auto=False):
    config = load_config()
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    zip_filename = f"eml-indexer_{date_str}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_filename)
    
    json_data = export_to_json()
    temp_json_path = os.path.join(BACKUP_DIR, f"data_{date_str}.json")
    with open(temp_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_json_path, arcname='emails_data.json')
    
    os.remove(temp_json_path)
    
    if is_auto:
        config["last_backup_date"] = now.strftime('%Y-%m-%d')
        save_config(config)
    
    backups = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith('eml-indexer_') and f.endswith('.zip')]
    backups.sort(key=os.path.getmtime)
    while len(backups) > config["max_backups"]:
        os.remove(backups.pop(0))
    return zip_path

# --- 背景執行緒 ---

def auto_backup_thread():
    while True:
        try:
            config = load_config()
            now = datetime.now()
            if now.hour == config.get("backup_hour", 2):
                last_backup_str = config.get("last_backup_date", "")
                should_backup = not last_backup_str or (now - datetime.strptime(last_backup_str, '%Y-%m-%d')).days >= config.get("backup_interval_days", 3)
                if should_backup:
                    perform_backup(is_auto=True)
        except Exception as e:
            print(f"備份錯誤: {e}")
        time.sleep(60)

threading.Thread(target=auto_backup_thread, daemon=True).start()

# --- Flask 路由 ---

@app.before_request
def limit_remote_addr():
    client_ip = get_client_ip()
    config = load_config()
    if client_ip not in config["allowed_ips"]:
        abort(403, description="IP 不在允許清單中")

@app.route('/')
def index():
    client_ip = get_client_ip()
    show_admin = is_localhost(client_ip)
    config = load_config()
    return render_template('index.html', show_admin=show_admin, config=config)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    sender = request.args.get('sender', '').strip()
    recipient = request.args.get('recipient', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor()
    base_sql = " FROM emails WHERE 1=1"
    params = []
    
    if query:
        base_sql += " AND (LOWER(subject) LIKE LOWER(?) OR LOWER(body) LIKE LOWER(?))"
        params.extend([f'%{query}%', f'%{query}%'])
    if sender:
        base_sql += " AND LOWER(sender) LIKE LOWER(?)"
        params.append(f'%{sender}%')
    if recipient:
        base_sql += " AND LOWER(recipient) LIKE LOWER(?)"
        params.append(f'%{recipient}%')
    if start_date:
        base_sql += " AND sent_time >= ?"
        params.append(f'{start_date} 00:00:00')
    if end_date:
        base_sql += " AND sent_time <= ?"
        params.append(f'{end_date} 23:59:59')
        
    cursor.execute("SELECT COUNT(*)" + base_sql, params)
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT id, subject, sender, recipient, sent_time, file_path" + base_sql + " ORDER BY sent_time DESC LIMIT ? OFFSET ?", params + [per_page, offset])
    
    show_path = is_localhost(get_client_ip())
    results = []
    for row in cursor.fetchall():
        r = dict(row)
        if not show_path:
            r['file_path'] = '[為保護隱私，非本機查詢已隱藏路徑]'
        results.append(r)
        
    conn.close()
    
    return jsonify({'results': results, 'total_count': total_count, 'has_more': (offset + per_page) < total_count})

@app.route('/export_excel')
def export_excel():
    query = request.args.get('q', '').strip()
    sender = request.args.get('sender', '').strip()
    recipient = request.args.get('recipient', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    base_sql = " FROM emails WHERE 1=1"
    params = []
    
    if query:
        base_sql += " AND (LOWER(subject) LIKE LOWER(?) OR LOWER(body) LIKE LOWER(?))"
        params.extend([f'%{query}%', f'%{query}%'])
    if sender:
        base_sql += " AND LOWER(sender) LIKE LOWER(?)"
        params.append(f'%{sender}%')
    if recipient:
        base_sql += " AND LOWER(recipient) LIKE LOWER(?)"
        params.append(f'%{recipient}%')
    if start_date:
        base_sql += " AND sent_time >= ?"
        params.append(f'{start_date} 00:00:00')
    if end_date:
        base_sql += " AND sent_time <= ?"
        params.append(f'{end_date} 23:59:59')
        
    cursor.execute("SELECT subject, sender, recipient, sent_time, body, file_path" + base_sql + " ORDER BY sent_time DESC", params)
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    output.write('\ufeff') 
    writer = csv.writer(output)
    writer.writerow(['Subject', 'Sender', 'Recipient', 'Sent Time', 'Body Preview', 'File Path'])
    
    show_path = is_localhost(get_client_ip())
    for row in rows:
        body_preview = row['body'][:200].replace('\n', ' ') + '...' if row['body'] else ''
        file_path_display = row['file_path'] if show_path else '[為保護隱私，非本機匯出已隱藏路徑]'
        writer.writerow([row['subject'], row['sender'], row['recipient'], row['sent_time'], body_preview, file_path_display])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=eml_export.csv"}
    )

@app.route('/delete_email/<int:email_id>', methods=['DELETE'])
@requires_admin_auth
def delete_email(email_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM emails WHERE id = ?", (email_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        # 修復 Bug：統一回傳 success: False，讓前端 JS 不會報出 undefined
        return jsonify({'success': False, 'message': '找不到郵件'}), 404
    
    file_path = row['file_path']
    
    # 修復 Bug：無論檔案路徑是否合法，先無條件清除資料庫紀錄，確保 UI 乾淨
    cursor.execute("DELETE FROM emails WHERE id = ?", (email_id,))
    conn.commit()
    conn.close()
    
    # 防禦性刪除實體檔案 (不報錯中斷)
    if file_path and '..' not in file_path:
        abs_path = os.path.abspath(file_path)
        if abs_path.lower().endswith('.eml') and os.path.exists(abs_path) and os.path.isfile(abs_path):
            try:
                os.remove(abs_path)
            except Exception:
                pass
                
    return jsonify({'success': True, 'message': '已成功刪除'})

@app.route('/email/<int:email_id>')
def get_email(email_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails WHERE id = ?", (email_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return ("找不到郵件", 404)
        
    email_data = dict(row)
    if not is_localhost(get_client_ip()):
        email_data['file_path'] = '[為保護隱私，非本機檢視已隱藏路徑]'
        
    return render_template('detail.html', email=email_data)

# --- 管理員 API ---

@app.route('/api/config', methods=['GET', 'POST'])
@requires_admin_auth
def manage_config():
    config = load_config()
    if request.method == 'POST':
        data = request.json
        if 'allowed_ips' in data:
            # 修復 Bug：改用固定的陣列做合併，徹底斷絕跟 DEFAULT_CONFIG 的記憶體糾纏
            fixed_ips = ["127.0.0.1", "localhost", "::1"]
            config["allowed_ips"] = list(set(data['allowed_ips'] + fixed_ips))
        for field in ['backup_interval_days', 'backup_hour', 'max_backups', 'admin_password']:
            if field in data: config[field] = data[field]
        save_config(config)
        return jsonify({'message': '設定已儲存', 'config': config})
    return jsonify(config)

@app.route('/api/backup', methods=['GET'])
@requires_admin_auth
def backup_api():
    return send_file(perform_backup(is_auto=False), as_attachment=True)

@app.route('/api/restore', methods=['POST'])
@requires_admin_auth
def restore_api():
    file = request.files.get('file')
    if not file: return jsonify({'error': '無檔案'}), 400
    
    temp_zip = "temp_restore.zip"
    file.save(temp_zip)
    try:
        with zipfile.ZipFile(temp_zip, 'r') as zipf:
            with zipf.open('emails_data.json') as f:
                new_count = import_from_json(json.load(f))
        return jsonify({'message': f'還原成功，過濾並新增 {new_count} 封'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_zip): os.remove(temp_zip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)