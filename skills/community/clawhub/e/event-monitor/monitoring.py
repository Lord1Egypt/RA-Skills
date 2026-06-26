import sqlite3
import psutil
import datetime
import socket
import os
import argparse
import math
from math import ceil
from openpyxl import Workbook
from openpyxl.styles import Font

class DatabaseManager:
    def __init__(self, db_path="monitoring.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cpu_usage_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT,
                application_name TEXT,
                cpu_usage REAL,
                timestamp DATETIME,
                day INTEGER,
                week INTEGER,
                month INTEGER,
                working_day TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_usage_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT,
                application_name TEXT,
                memory_usage REAL,
                timestamp DATETIME,
                day INTEGER,
                week INTEGER,
                month INTEGER,
                working_day TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alert (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert TEXT,
                date TEXT,
                devicename TEXT,
                type TEXT,
                variant TEXT
            )
            """)
            conn.commit()

    def insert_cpu_metrics(self, metrics):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO cpu_usage_table
                (device_name, application_name, cpu_usage, timestamp, day, week, month, working_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, metrics)
            conn.commit()

    def insert_memory_metrics(self, metrics):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO memory_usage_table
                (device_name, application_name, memory_usage, timestamp, day, week, month, working_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, metrics)
            conn.commit()

def collect_metrics():
    device_name = socket.gethostname()
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    day = now.isoweekday()
    week = (now.day - 1) // 7 + 1
    month = now.month
    working_day = "Weekday" if day <= 5 else "Weekend"
    
    cpu_count = psutil.cpu_count(logical=True)
    psutil.cpu_percent(interval=0.1)  # Initial call to seed cpu_percent
    
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['pid'] == 0 or proc.info['name'].lower() in ['system idle process', 'idle']:
                continue
            cpu = proc.cpu_percent(interval=None)
            normalized_cpu = min(round(cpu / cpu_count, 3), 100.0)
            mem = round(proc.memory_percent(), 3)
            app_name = proc.info['name']
            process_list.append({
                'device_name': device_name,
                'app_name': app_name,
                'cpu_usage': normalized_cpu,
                'mem_usage': mem,
                'timestamp': timestamp,
                'day': day,
                'week': week,
                'month': month,
                'working_day': working_day
            })
        except Exception:
            continue
            
    top_cpu = sorted(process_list, key=lambda x: x['cpu_usage'], reverse=True)[:10]
    top_mem = sorted(process_list, key=lambda x: x['mem_usage'], reverse=True)[:10]
    
    return top_cpu, top_mem

def save_to_db(top_cpu, top_mem, db_manager):
    cpu_data = [
        (m['device_name'], m['app_name'], m['cpu_usage'], m['timestamp'], m['day'], m['week'], m['month'], m['working_day'])
        for m in top_cpu
    ]
    mem_data = [
        (m['device_name'], m['app_name'], m['mem_usage'], m['timestamp'], m['day'], m['week'], m['month'], m['working_day'])
        for m in top_mem
    ]
    
    db_manager.insert_cpu_metrics(cpu_data)
    db_manager.insert_memory_metrics(mem_data)
    print("Metrics saved to database.")

def predict_cpu_usage(db_manager):
    try:
        import pandas as pd
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
    except ImportError:
        print("Required libraries for prediction not found. Run: pip install pandas scikit-learn")
        return

    print("Starting predictive analysis...")
    conn = db_manager.get_connection()
    device_name = socket.gethostname()

    query = """
        SELECT 
            timestamp, 
            SUM(cpu_usage) as total_cpu, 
            working_day 
        FROM cpu_usage_table 
        GROUP BY timestamp, working_day
        ORDER BY timestamp ASC
    """
    df = pd.read_sql_query(query, conn)

    if len(df) < 10:
        print(f"Not enough data to train the prediction model. Found {len(df)} records, need at least 10.")
        return

    def get_status_label(cpu):
        if cpu >= 80:
            return 2
        elif cpu >= 70:
            return 1
        return 0

    df['avgPercent'] = df['total_cpu'].apply(get_status_label)
    df['datetime'] = pd.to_datetime(df['timestamp'])

    df['Day'] = df['datetime'].dt.weekday + 1 
    df['Week'] = df['datetime'].apply(lambda d: int(ceil((d.day + d.replace(day=1).weekday()) / 7.0)))
    df['Working'] = df['datetime'].dt.weekday.apply(lambda d: 0 if d in [5,6] else 1)
    df['Hour'] = df['datetime'].dt.hour
    df['Minute'] = df['datetime'].dt.minute

    X = df[['Day', 'Week', 'Working', 'Hour', 'Minute']]
    y = df['avgPercent']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    n_est = len(df)
    if n_est < 10:
        n_est = 10
    
    clf = RandomForestRegressor(n_estimators=n_est, max_features="sqrt", random_state=42)
    clf.fit(X_train, y_train)

    ntime = datetime.datetime.now()
    oneday = ntime + datetime.timedelta(hours=24)

    consecutive_amber_red_count = 0
    current_time = ntime.replace(minute=0, second=0, microsecond=0)

    print("Predicting potential CPU spikes for the next 24 hours...")
    
    while current_time < oneday:
        current_hour = current_time.hour
        current_minute = current_time.minute
        inserttime = current_time.strftime("%Y-%m-%d %H:%M:%S")

        day_pred = current_time.weekday() + 1
        work_pred = 0 if day_pred in [6, 7] else 1
        first_day = current_time.replace(day=1)
        adjusted_dom = current_time.day + first_day.weekday()
        week_pred = int(ceil(adjusted_dom / 7.0))

        features = pd.DataFrame([[day_pred, week_pred, work_pred, current_hour, current_minute]], 
                                columns=['Day', 'Week', 'Working', 'Hour', 'Minute'])
        pred_val = clf.predict(features)[0]

        if pred_val < 0.5:
            current_time_status = "Low"
            consecutive_amber_red_count = 0
        elif 0.5 <= pred_val <= 1.0:
            current_time_status = "Amber"
            consecutive_amber_red_count += 1
        else:
            current_time_status = "Red"
            consecutive_amber_red_count += 1

        if consecutive_amber_red_count >= 2:
            print(f"Prediction for {current_hour:02d}:00 - Status: {current_time_status}")
            if current_time_status != "Low":
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id FROM Alert 
                        WHERE alert = ? AND devicename = ? AND type = 'CPU' AND substr(date, 12, 2) = ?
                    """, (current_time_status, device_name, f"{current_hour:02d}"))
                    row = cursor.fetchone()

                    if row:
                        cursor.execute("UPDATE Alert SET alert = ?, date = ? WHERE id = ?", 
                            (current_time_status, inserttime, row[0]))
                    else:
                        cursor.execute("INSERT INTO Alert (alert, date, devicename, type, variant) VALUES (?, ?, ?, ?, ?)",
                            (current_time_status, inserttime, device_name, 'CPU', 'CPU'))
                consecutive_amber_red_count = 0
                current_time += datetime.timedelta(hours=1)
                current_time = current_time.replace(minute=0)
        else:
            current_time += datetime.timedelta(minutes=10)

    print("Predictive monitoring scan completed. Alerts saved to database if any.")

def generate_excel_report(top_cpu, top_mem, filename="system_report.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Resource Usage"
    
    headers = ["ID", "Device Name", "Application Name", "CPU Usage (%)", "Memory Usage (%)", "Timestamp", "Day", "Week", "Month", "Working Day"]
    ws.append(headers)
    
    header_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = header_font
        
    for i, m in enumerate(top_cpu, 1):
        ws.append([i, m['device_name'], m['app_name'], f"{m['cpu_usage']:.3f}", f"{m['mem_usage']:.3f}", m['timestamp'], m['day'], m['week'], m['month'], m['working_day']])
        
    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = max_length + 2
        
    wb.save(filename)
    print(f"Report saved to {filename}")

def run_skill(run_predict=False):
    db_manager = DatabaseManager()
    top_cpu, top_mem = collect_metrics()
    save_to_db(top_cpu, top_mem, db_manager)
    generate_excel_report(top_cpu, top_mem)
    if run_predict:
        predict_cpu_usage(db_manager)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predictive Monitoring Skill for OpenClaw")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--predict", action="store_true", help="Run ML prediction on CPU usage")
    args = parser.parse_args()
    
    if args.test:
        print("Running in test mode...")
        run_skill(run_predict=args.predict)
    else:
        run_skill(run_predict=args.predict)
