#!/usr/bin/env python3
"""
Consolidated Calorie Tracker CLI for local calorie and weight tracking.
"""

import sqlite3
import sys
import argparse
import difflib
from datetime import datetime, date, timedelta
from pathlib import Path

# Default height is 180cm
HEIGHT_CM = 180.0
HEIGHT_M = HEIGHT_CM / 100.0

def get_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    conn = get_db(db_path)
    c = conn.cursor()
    
    # Food entries
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            food_name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            protein REAL,
            carbs REAL,
            fat REAL,
            meal_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Daily goals
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_goal (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            calorie_goal INTEGER NOT NULL,
            protein_goal REAL
        )
    ''')
    
    # Weight log (kg)
    c.execute('''
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            weight_kg REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Dynamic body measurements schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurement_types (
            key TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurement_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type_key TEXT NOT NULL REFERENCES measurement_types(key) ON DELETE CASCADE,
            value REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, type_key)
        )
    ''')

    # Migration from legacy body_measurements table
    c.execute("SELECT type FROM sqlite_master WHERE name = 'body_measurements'")
    res = c.fetchone()
    if res and res[0] == 'table':
        # Fetch existing legacy measurements
        c.execute("SELECT date, waist_cm, hips_cm, neck_cm, created_at FROM body_measurements")
        old_rows = c.fetchall()
        
        # Seed default measurement types
        c.execute("INSERT OR IGNORE INTO measurement_types (key, name, unit, description) VALUES ('waist', 'Waist', 'cm', 'Waist circumference')")
        c.execute("INSERT OR IGNORE INTO measurement_types (key, name, unit, description) VALUES ('hips', 'Hips', 'cm', 'Hips circumference')")
        c.execute("INSERT OR IGNORE INTO measurement_types (key, name, unit, description) VALUES ('neck', 'Neck', 'cm', 'Neck circumference')")
        
        for row in old_rows:
            date_val, waist_cm, hips_cm, neck_cm, created_at = row
            if waist_cm is not None:
                c.execute('''
                    INSERT OR IGNORE INTO measurement_log (date, type_key, value, created_at)
                    VALUES (?, 'waist', ?, ?)
                ''', (date_val, waist_cm, created_at))
            if hips_cm is not None:
                c.execute('''
                    INSERT OR IGNORE INTO measurement_log (date, type_key, value, created_at)
                    VALUES (?, 'hips', ?, ?)
                ''', (date_val, hips_cm, created_at))
            if neck_cm is not None:
                c.execute('''
                    INSERT OR IGNORE INTO measurement_log (date, type_key, value, created_at)
                    VALUES (?, 'neck', ?, ?)
                ''', (date_val, neck_cm, created_at))
        
        c.execute("DROP TABLE body_measurements")
        
    # Seed default types if not already seeded
    c.execute("SELECT COUNT(*) FROM measurement_types")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO measurement_types (key, name, unit, description) VALUES ('waist', 'Waist', 'cm', 'Waist circumference')")
        c.execute("INSERT INTO measurement_types (key, name, unit, description) VALUES ('hips', 'Hips', 'cm', 'Hips circumference')")
        c.execute("INSERT INTO measurement_types (key, name, unit, description) VALUES ('neck', 'Neck', 'cm', 'Neck circumference')")
    
    # Daily notes/annotations
    c.execute('''
        CREATE TABLE IF NOT EXISTS day_notes (
            date TEXT PRIMARY KEY,
            tracking_quality TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Dynamic meal types table
    c.execute('''
        CREATE TABLE IF NOT EXISTS meal_types (
            type TEXT PRIMARY KEY
        )
    ''')
    
    c.execute("PRAGMA table_info(day_notes)")
    columns = [row['name'] for row in c.fetchall()]
    if 'completed' not in columns:
        c.execute("ALTER TABLE day_notes ADD COLUMN completed INTEGER DEFAULT 0")
        
    # Migration: Check if measurement_log has 'notes' column
    c.execute("PRAGMA table_info(measurement_log)")
    log_columns = [row['name'] for row in c.fetchall()]
    if 'notes' not in log_columns:
        c.execute("ALTER TABLE measurement_log ADD COLUMN notes TEXT")
        
    # Migration: Check if daily_goal has 'height_cm' column
    c.execute("PRAGMA table_info(daily_goal)")
    goal_columns = [row['name'] for row in c.fetchall()]
    if 'height_cm' not in goal_columns:
        c.execute("ALTER TABLE daily_goal ADD COLUMN height_cm REAL DEFAULT 180.0")
        
    # Seed default meal types if table is empty
    c.execute("SELECT COUNT(*) FROM meal_types")
    if c.fetchone()[0] == 0:
        default_meals = [
            ('breakfast',), ('lunch',), ('dinner',), ('snack',),
            ('fika',), ('drink',), ('dessert',), ('evening',), ('other',)
        ]
        c.executemany("INSERT INTO meal_types (type) VALUES (?)", default_meals)
        
    # Define SQL Views for stats calculations
    c.execute("DROP VIEW IF EXISTS v_daily_summary")
    c.execute('''
        CREATE VIEW v_daily_summary AS
        SELECT 
            d.date,
            COALESCE(e.total_cal, 0) as total_cal,
            COALESCE(e.total_p, 0) as total_p,
            COALESCE(e.entry_count, 0) as entry_count,
            n.tracking_quality as completeness,
            COALESCE(n.completed, 0) as completed
        FROM (
            SELECT date FROM entries
            UNION
            SELECT date FROM day_notes
        ) d
        LEFT JOIN (
            SELECT 
                date,
                SUM(calories) as total_cal,
                SUM(protein) as total_p,
                COUNT(*) as entry_count
            FROM entries
            GROUP BY date
        ) e ON d.date = e.date
        LEFT JOIN day_notes n ON d.date = n.date
    ''')
    
    c.execute("DROP VIEW IF EXISTS v_daily_rolling_trends")
    c.execute('''
        CREATE VIEW v_daily_rolling_trends AS
        SELECT 
            date,
            total_cal,
            total_p,
            AVG(total_cal) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as rolling_7_cal,
            AVG(total_p) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as rolling_7_p,
            AVG(total_cal) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as rolling_30_cal,
            AVG(total_p) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as rolling_30_p,
            AVG(total_cal) OVER (ORDER BY date ROWS BETWEEN 89 PRECEDING AND CURRENT ROW) as rolling_90_cal,
            AVG(total_p) OVER (ORDER BY date ROWS BETWEEN 89 PRECEDING AND CURRENT ROW) as rolling_90_p
        FROM v_daily_summary
    ''')
    
    # BMI and WHtR resolved dynamically from the daily_goal table
    c.execute("DROP VIEW IF EXISTS v_weight_summary")
    c.execute('''
        CREATE VIEW v_weight_summary AS
        SELECT 
            date,
            weight_kg,
            ROUND(weight_kg / ( ( (SELECT COALESCE(height_cm, 180.0) FROM daily_goal WHERE id = 1) / 100.0 ) * ( (SELECT COALESCE(height_cm, 180.0) FROM daily_goal WHERE id = 1) / 100.0 ) ), 1) as bmi,
            ROUND(weight_kg - LAG(weight_kg) OVER (ORDER BY date), 1) as change_kg
        FROM weight_log
    ''')
    
    c.execute("DROP VIEW IF EXISTS body_measurements")
    c.execute('''
        CREATE VIEW body_measurements AS
        SELECT 
            MIN(id) as id,
            date,
            MAX(CASE WHEN type_key = 'waist' THEN value END) as waist_cm,
            MAX(CASE WHEN type_key = 'hips' THEN value END) as hips_cm,
            MAX(CASE WHEN type_key = 'neck' THEN value END) as neck_cm,
            MAX(created_at) as created_at
        FROM measurement_log
        GROUP BY date
    ''')

    c.execute("DROP VIEW IF EXISTS v_measurement_summary")
    c.execute('''
        CREATE VIEW v_measurement_summary AS
        SELECT 
            id,
            date,
            type_key,
            value,
            notes,
            ROUND(value - LAG(value) OVER (PARTITION BY type_key ORDER BY date), 2) as change_val,
            CASE 
                WHEN type_key = 'waist' THEN ROUND(value / (SELECT COALESCE(height_cm, 180.0) FROM daily_goal WHERE id = 1), 2)
                ELSE NULL
            END as whtr
        FROM measurement_log
    ''')

    c.execute("DROP VIEW IF EXISTS v_waist_summary")
    c.execute('''
        CREATE VIEW v_waist_summary AS
        SELECT 
            date,
            value as waist_cm,
            whtr,
            change_val as change_cm
        FROM v_measurement_summary
        WHERE type_key = 'waist' AND value IS NOT NULL
    ''')
    
    conn.commit()
    conn.close()

def get_valid_meal_types(db_path):
    conn = get_db(db_path)
    rows = conn.execute("SELECT type FROM meal_types").fetchall()
    conn.close()
    return {row['type'] for row in rows}

def validate_meal_type(db_path, meal_type):
    valid_types = get_valid_meal_types(db_path)
    if meal_type not in valid_types:
        print(f"Error: Invalid meal type '{meal_type}'. Valid types: {', '.join(sorted(valid_types))}")
        sys.exit(1)

def get_goal(db_path):
    conn = get_db(db_path)
    row = conn.execute("SELECT calorie_goal, protein_goal, height_cm FROM daily_goal WHERE id = 1").fetchone()
    conn.close()
    if row:
        return row['calorie_goal'], row['protein_goal'], row['height_cm']
    return None, None, 180.0

# ----------------- Configuration & Logging -----------------

def cmd_goal(args):
    conn = get_db(args.database)
    c = conn.cursor()
    
    # Keep existing height if not provided
    row = c.execute("SELECT height_cm FROM daily_goal WHERE id = 1").fetchone()
    existing_height = row['height_cm'] if row else 180.0
    height = args.height if args.height is not None else existing_height
    
    c.execute('''
        INSERT OR REPLACE INTO daily_goal (id, calorie_goal, protein_goal, height_cm)
        VALUES (1, ?, ?, ?)
    ''', (args.calories, args.protein, height))
    conn.commit()
    conn.close()
    
    p_str = f" | {args.protein}g protein" if args.protein is not None else ""
    print(f"Daily goal set: {args.calories} kcal{p_str} | Height: {height} cm")

def cmd_add(args):
    validate_meal_type(args.database, args.meal)
    entry_date = args.date or args.today or date.today().isoformat()
    
    conn = get_db(args.database)
    c = conn.cursor()
    c.execute('''
        INSERT INTO entries (date, food_name, calories, protein, carbs, fat, meal_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (entry_date, args.food_name, args.calories, args.protein, args.carbs, args.fat, args.meal))
    entry_id = c.lastrowid
    conn.commit()
    
    # Fetch today's totals from view
    totals = c.execute('SELECT total_cal FROM v_daily_summary WHERE date = ?', (entry_date,)).fetchone()
    conn.close()
    
    total_cal = totals['total_cal'] if totals else args.calories
    
    goal_cal, _, _ = get_goal(args.database)
    goal_str = f"/{goal_cal}" if goal_cal else ""
    
    # Print harmonized Added Entry output
    print(f"Added Entry {entry_id}: +{args.calories} ({total_cal}{goal_str})")

def cmd_list(args):
    entry_date = args.date or args.today or date.today().isoformat()
    conn = get_db(args.database)
    rows = conn.execute('''
        SELECT id, strftime('%H:%M', created_at) as t, meal_type, food_name, calories, protein
        FROM entries WHERE date = ? ORDER BY created_at
    ''', (entry_date,)).fetchall()
    conn.close()
    
    if not rows:
        print(f"No entries found for {entry_date}")
        return
        
    print(f"Entries for {entry_date}:")
    if getattr(args, 'no_group', False):
        for r in rows:
            time_str = r['t'] if r['t'] else "??:??"
            p_str = f" | {r['protein']:.1f}g P" if r['protein'] is not None else ""
            print(f"  [{r['id']}] {time_str} [{r['meal_type']}] {r['food_name']}: {r['calories']} kcal{p_str}")
    else:
        grouped = {}
        for r in rows:
            mt = r['meal_type']
            if mt not in grouped:
                grouped[mt] = {
                    'foods': [],
                    'calories': 0,
                    'proteins': [],
                    'has_protein': False
                }
            grouped[mt]['foods'].append(r['food_name'])
            grouped[mt]['calories'] += r['calories']
            if r['protein'] is not None:
                grouped[mt]['proteins'].append(r['protein'])
                grouped[mt]['has_protein'] = True
                
        for mt, data in grouped.items():
            foods_str = ", ".join(data['foods'])
            cal = data['calories']
            p_str = ""
            if data['has_protein']:
                p_val = sum(data['proteins'])
                p_str = f" | {p_val:.1f}g P"
            print(f"  • {mt}: {foods_str} — {cal} kcal{p_str}")

def cmd_update(args):
    conn = get_db(args.database)
    c = conn.cursor()
    
    row = c.execute("SELECT * FROM entries WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Error: Entry {args.id} not found.")
        conn.close()
        sys.exit(1)
        
    # Use existing values if flags not provided
    name = args.name if args.name is not None else row['food_name']
    calories = args.cal if args.cal is not None else row['calories']
    protein = args.p if args.p is not None else row['protein']
    carbs = args.c if args.c is not None else row['carbs']
    fat = args.f if args.f is not None else row['fat']
    meal_type = args.meal if args.meal is not None else row['meal_type']
    
    if args.meal is not None:
        validate_meal_type(args.database, meal_type)
        
    c.execute('''
        UPDATE entries
        SET food_name = ?, calories = ?, protein = ?, carbs = ?, fat = ?, meal_type = ?
        WHERE id = ?
    ''', (name, calories, protein, carbs, fat, meal_type, args.id))
    conn.commit()
    
    # Fetch date totals from view
    entry_date = row['date']
    totals = c.execute('SELECT total_cal FROM v_daily_summary WHERE date = ?', (entry_date,)).fetchone()
    conn.close()
    
    total_cal = totals['total_cal'] if totals else 0
    goal_cal, _, _ = get_goal(args.database)
    goal_str = f"/{goal_cal}" if goal_cal else ""
    
    # Print harmonized Changed Entry output
    print(f"Changed Entry {args.id}: {row['calories']}->{calories} ({total_cal}{goal_str})")

def cmd_delete(args):
    conn = get_db(args.database)
    c = conn.cursor()
    row = c.execute("SELECT date, calories FROM entries WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Error: Entry {args.id} not found.")
        conn.close()
        sys.exit(1)
        
    c.execute("DELETE FROM entries WHERE id = ?", (args.id,))
    conn.commit()
    
    # Fetch date totals from view
    entry_date = row['date']
    totals = c.execute('SELECT total_cal FROM v_daily_summary WHERE date = ?', (entry_date,)).fetchone()
    conn.close()
    
    total_cal = totals['total_cal'] if totals else 0
    goal_cal, _, _ = get_goal(args.database)
    goal_str = f"/{goal_cal}" if goal_cal else ""
    
    # Print harmonized Deleted Entry output
    print(f"Deleted Entry {args.id}: -{row['calories']} ({total_cal}{goal_str})")

def cmd_complete(args):
    conn = get_db(args.database)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO day_notes (date, tracking_quality, completed)
        VALUES (?, ?, 1)
    ''', (args.date, args.completeness))
    conn.commit()
    conn.close()
    print(f"Day {args.date} marked as completed (completeness: {args.completeness})")

def cmd_check_complete(args):
    target_date = args.date or args.today or date.today().isoformat()
    conn = get_db(args.database)
    row = conn.execute("SELECT completeness, completed FROM v_daily_summary WHERE date = ?", (target_date,)).fetchone()
    conn.close()
    
    if row and row['completeness'] == 'full' and row['completed'] == 1:
        print(f"Day {target_date} is fully complete.")
        sys.exit(0)
    else:
        q = row['completeness'] if row else "unlogged"
        print(f"Day {target_date} is NOT fully complete (status: {q}).")
        sys.exit(1)

def cmd_weight(args):
    target_date = args.date or args.today or date.today().isoformat()
    conn = get_db(args.database)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO weight_log (date, weight_kg)
        VALUES (?, ?)
    ''', (target_date, args.kg))
    conn.commit()
    conn.close()
    print(f"Weight logged: {args.kg} kg on {target_date}")

def format_value(val):
    if val is None:
        return ""
    if abs(val - round(val, 1)) < 1e-9:
        return f"{val:.1f}"
    return f"{val:.2f}"

def format_change(change, unit):
    if change is None:
        return ""
    val_str = format_value(abs(change))
    sign = "+" if change >= 0 else "-"
    return f" ({sign}{val_str} {unit})"

def cmd_waist(args):
    args.type = 'waist'
    args.value = args.cm
    cmd_measure(args)

def cmd_measure(args):
    target_date = args.date or args.today or date.today().isoformat()
    conn = get_db(args.database)
    c = conn.cursor()
    
    t_key = args.type.lower()
    row = c.execute("SELECT name, unit FROM measurement_types WHERE key = ?", (t_key,)).fetchone()
    if not row:
        print(f"Error: Measurement type '{t_key}' is not defined.")
        print(f"Define it first using: python scripts/tracker.py measure-type define {t_key} \"Name\" UNIT")
        conn.close()
        sys.exit(1)
        
    type_name = row['name']
    unit = row['unit']
    
    notes = args.notes if hasattr(args, 'notes') else None
    
    c.execute('''
        INSERT OR REPLACE INTO measurement_log (date, type_key, value, notes)
        VALUES (?, ?, ?, ?)
    ''', (target_date, t_key, args.value, notes))
    conn.commit()
    conn.close()
    notes_str = f" | notes: {notes}" if notes else ""
    print(f"{type_name} logged: {format_value(args.value)} {unit} on {target_date}{notes_str}")

def cmd_measure_type(args):
    conn = get_db(args.database)
    c = conn.cursor()
    
    if args.measure_type_command == "define":
        key = args.key.lower()
        if not key.replace('_', '').isalnum():
            print("Error: Key must contain only letters, numbers, and underscores.")
            conn.close()
            sys.exit(1)
            
        c.execute('''
            INSERT OR REPLACE INTO measurement_types (key, name, unit, description)
            VALUES (?, ?, ?, ?)
        ''', (key, args.name, args.unit, args.desc))
        conn.commit()
        print(f"Measurement type '{key}' defined: {args.name} ({args.unit})")
        if args.desc:
            print(f"  Description: {args.desc}")
            
    elif args.measure_type_command == "list":
        rows = c.execute("SELECT key, name, unit, description FROM measurement_types ORDER BY key").fetchall()
        if not rows:
            print("No measurement types defined.")
        else:
            print("-" * 80)
            print(f"{'Key':<15} | {'Name':<20} | {'Unit':<10} | Description")
            print("-" * 80)
            for r in rows:
                desc = r['description'] or ""
                print(f"{r['key']:<15} | {r['name']:<20} | {r['unit']:<10} | {desc}")
            print("-" * 80)
            
    elif args.measure_type_command == "delete":
        key = args.key.lower()
        row = c.execute("SELECT name FROM measurement_types WHERE key = ?", (key,)).fetchone()
        if not row:
            print(f"Error: Measurement type '{key}' does not exist.")
            conn.close()
            sys.exit(1)
            
        if key in ('waist', 'hips', 'neck'):
            print(f"Error: Cannot delete system default measurement type '{key}'.")
            conn.close()
            sys.exit(1)
            
        c.execute("DELETE FROM measurement_types WHERE key = ?", (key,))
        conn.commit()
        print(f"Measurement type '{key}' and all associated log entries deleted.")
        
    conn.close()

# ----------------- Statistics & Reports -----------------

def cmd_stats_day(args):
    today_str = args.today or date.today().isoformat()
    target_date = args.date or today_str
    conn = get_db(args.database)
    goal_cal, goal_p, _ = get_goal(args.database)
    
    entries = conn.execute('''
        SELECT id, strftime('%H:%M', created_at) as t, meal_type, food_name, calories, protein
        FROM entries WHERE date = ? ORDER BY created_at
    ''', (target_date,)).fetchall()
    
    # Query aggregated daily totals from view
    totals = conn.execute('''
        SELECT total_cal, total_p, completeness
        FROM v_daily_summary WHERE date = ?
    ''', (target_date,)).fetchone()
    
    note = conn.execute("SELECT notes FROM day_notes WHERE date = ?", (target_date,)).fetchone()
    conn.close()
    
    print("-" * 60)
    print(f"DAY BREAKDOWN: {target_date}")
    if totals and totals['completeness']:
        notes_str = f" | Note: {note['notes']}" if (note and note['notes']) else ""
        print(f"Status: {totals['completeness'].upper()}{notes_str}")
    print("-" * 60)
    
    if not entries:
        print("No entries logged for this day.")
        return
        
    if getattr(args, 'no_group', False):
        for e in entries:
            time_str = e['t'] if e['t'] else "??:??"
            p_str = f", {e['protein']:.0f}g P" if e['protein'] is not None else ""
            print(f"  [{e['id']}] {time_str} [{e['meal_type']}] {e['food_name']}: {e['calories']} kcal{p_str}")
    else:
        grouped = {}
        for e in entries:
            mt = e['meal_type']
            if mt not in grouped:
                grouped[mt] = {
                    'foods': [],
                    'calories': 0,
                    'proteins': [],
                    'has_protein': False
                }
            grouped[mt]['foods'].append(e['food_name'])
            grouped[mt]['calories'] += e['calories']
            if e['protein'] is not None:
                grouped[mt]['proteins'].append(e['protein'])
                grouped[mt]['has_protein'] = True
                
        for mt, data in grouped.items():
            foods_str = ", ".join(data['foods'])
            cal = data['calories']
            p_str = ""
            if data['has_protein']:
                p_val = sum(data['proteins'])
                p_str = f", {p_val:.0f}g P"
            print(f"  • {mt}: {foods_str} — {cal} kcal{p_str}")
        
    print("-" * 60)
    total_cal = totals['total_cal'] if totals else 0
    total_p = totals['total_p'] if totals else 0
    
    if goal_cal:
        diff = total_cal - goal_cal
        sign = "+" if diff >= 0 else ""
        print(f"Total: {total_cal} / {goal_cal} kcal ({sign}{diff} kcal) | {total_p:.1f}g Protein")
    else:
        print(f"Total: {total_cal} kcal | {total_p:.1f}g Protein")
    if goal_p:
        diff_p = total_p - goal_p
        sign_p = "+" if diff_p >= 0 else ""
        print(f"Protein: {total_p:.1f} / {goal_p} g ({sign_p}{diff_p:.1f} g)")
    print("-" * 60)

def cmd_stats_week(args):
    today_str = args.today or date.today().isoformat()
    today_date = date.fromisoformat(today_str)
    
    target_date_str = args.date or today_str
    target_date = date.fromisoformat(target_date_str)
    
    # Calculate Monday and Sunday of target week
    monday = target_date - timedelta(days=target_date.weekday())
    sunday = monday + timedelta(days=6)
    
    conn = get_db(args.database)
    goal_cal, goal_p, _ = get_goal(args.database)
    
    # Build list of weeks to display
    weeks_to_process = []
    for w_idx in range(args.weeks - 1, -1, -1):
        w_mon = monday - timedelta(weeks=w_idx)
        w_sun = w_mon + timedelta(days=6)
        weeks_to_process.append((w_mon, w_sun))
        
    for w_mon, w_sun in weeks_to_process:
        # Load daily summaries for the 7 days of the week in a single query from view
        summary_rows = conn.execute('''
            SELECT date, total_cal, total_p, completeness, completed, entry_count
            FROM v_daily_summary
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        ''', (w_mon.isoformat(), w_sun.isoformat())).fetchall()
        
        summary_map = {r['date']: r for r in summary_rows}
        
        days = []
        for i in range(7):
            d = w_mon + timedelta(days=i)
            d_str = d.isoformat()
            
            row = summary_map.get(d_str)
            if d > today_date:
                row = None
            
            kcal = row['total_cal'] if row else 0
            protein = row['total_p'] if row else 0
            entry_count = row['entry_count'] if row else 0
            completed_val = row['completed'] if row else 0
            
            status = "unlogged"
            if row and row['completeness']:
                status = row['completeness']
            elif entry_count > 0:
                status = "partial"
                
            days.append({
                "date": d,
                "date_str": d_str,
                "day_name": d.strftime("%A"),
                "kcal": kcal,
                "protein": protein,
                "completeness": status,
                "completed": completed_val,
                "has_data": entry_count > 0
            })
            
        # Calculate Averages
        completed_days = [d for d in days if d['completed'] == 1]
        completed_avg = sum(d['kcal'] for d in completed_days) / len(completed_days) if completed_days else 0
        
        mon_to_yesterday = [d for d in days if d['date'] < today_date]
        yesterday_avg = sum(d['kcal'] for d in mon_to_yesterday) / len(mon_to_yesterday) if mon_to_yesterday else 0
        
        mon_to_today = [d for d in days if d['date'] <= today_date]
        today_avg = sum(d['kcal'] for d in mon_to_today) / len(mon_to_today) if mon_to_today else 0
        
        # Budgets
        weekly_total = sum(d['kcal'] for d in days)
        weekly_target = goal_cal * 7 if goal_cal else 0
        
        # Calculate active elapsed days for average display
        if today_date > w_sun:
            elapsed_days = 7
        elif today_date < w_mon:
            elapsed_days = 0
        else:
            elapsed_days = (today_date - w_mon).days + 1
            
        avg_cal = weekly_total / elapsed_days if elapsed_days > 0 else 0
        
        # Determine include_today mode
        include_today_arg = getattr(args, 'include_today', 'auto')
        if include_today_arg == 'auto':
            if w_mon <= today_date <= w_sun:
                today_day_dict = next((d for d in days if d['date'] == today_date), None)
                today_is_completed = today_day_dict['completed'] == 1 if today_day_dict else False
                include_today = 'yes' if today_is_completed else 'no'
            elif today_date > w_sun:
                include_today = 'yes'
            else:
                include_today = 'no'
        else:
            include_today = include_today_arg

        # Calculate budgets and formatting
        rem_days_now = [d for d in days if d['date'] >= today_date]
        days_left_now = len(rem_days_now)
        
        rem_days_tomorrow = [d for d in days if d['date'] > today_date]
        days_left_tomorrow = len(rem_days_tomorrow)
        
        logged_before_today = sum(d['kcal'] for d in days if d['date'] < today_date)
        logged_today = sum(d['kcal'] for d in days if d['date'] == today_date)
        logged_up_to_today = logged_before_today + logged_today
        
        # Starting Today budget
        if goal_cal and days_left_now > 0:
            even_budget_starting_today = (weekly_target - logged_before_today) / days_left_now
            remaining_today = even_budget_starting_today - logged_today
            
            # Format remaining today string
            if w_mon <= today_date <= w_sun:
                today_day_dict = next((d for d in days if d['date'] == today_date), None)
                today_is_completed = today_day_dict['completed'] == 1 if today_day_dict else False
                if today_is_completed:
                    rem_today_str = "Today is complete"
                else:
                    if remaining_today >= 0:
                        rem_today_str = f"{remaining_today:.0f} kcal remaining today"
                    else:
                        rem_today_str = f"over by {-remaining_today:.0f} kcal today"
            else:
                rem_today_str = ""
                
            if rem_today_str:
                budg_starting_today_str = f"{even_budget_starting_today:.0f} kcal/d ({rem_today_str})"
            else:
                budg_starting_today_str = f"{even_budget_starting_today:.0f} kcal/d"
        else:
            budg_starting_today_str = "Week over" if today_date > w_sun else "0 kcal/d"
            if not goal_cal:
                budg_starting_today_str = "Goal not set"
            
        # Starting Tomorrow budget
        if goal_cal and days_left_tomorrow > 0:
            budget_tomorrow = (weekly_target - logged_up_to_today) / days_left_tomorrow
            budg_starting_tomorrow_str = f"{budget_tomorrow:.0f} kcal/d"
        else:
            budg_starting_tomorrow_str = "Week over"
            if not goal_cal:
                budg_starting_tomorrow_str = "Goal not set"
        
        # Display Stats
        if args.compact:
            if include_today == 'no':
                compact_total = logged_before_today
                compact_avg = yesterday_avg
            else:
                compact_total = weekly_total
                compact_avg = today_avg
                
            diff_cal = compact_total - weekly_target
            diff_sign = "+" if diff_cal >= 0 else ""
            
            if goal_cal:
                target_str = f"/{weekly_target}"
                diff_str = f" ({diff_sign}{diff_cal} kcal)"
                avg_str = f", daily average {compact_avg:.0f}/{goal_cal} kcal"
            else:
                target_str = ""
                diff_str = ""
                avg_str = f", daily average {compact_avg:.0f} kcal"
                
            print(f"Week {w_mon} to {w_sun}: Total {compact_total}{target_str} kcal{diff_str}{avg_str}")
        else:
            print("\n" + "=" * 70)
            print(f"WEEK SUMMARY: {w_mon} to {w_sun}")
            print("=" * 70)
            diff_cal = weekly_total - weekly_target
            diff_sign = "+" if diff_cal >= 0 else ""
            
            if goal_cal:
                print(f"Total: {weekly_total} / {weekly_target} kcal ({diff_sign}{diff_cal} kcal)")
            else:
                print(f"Total: {weekly_total} kcal")
                
            if today_date > w_sun:
                print("Averages:")
                print(f"  Average Mon-Sunday: {today_avg:.0f} kcal")
                print("Budgets:")
                print("  Budget: Week over")
            elif today_date < w_mon:
                print("Averages:")
                print("  Average: -")
                print("Budgets:")
                if goal_cal:
                    print(f"  Starting Monday: {goal_cal} kcal/d")
                else:
                    print("  Starting Monday: Goal not set")
            else:
                # Display Averages
                print("Averages:")
                if include_today == 'no':
                    if mon_to_yesterday:
                        print(f"  Average Mon-Yesterday: {yesterday_avg:.0f} kcal")
                    else:
                        print("  Average Mon-Yesterday: -")
                elif include_today == 'yes':
                    print(f"  Average Mon-Today: {today_avg:.0f} kcal")
                elif include_today == 'both':
                    if mon_to_yesterday:
                        print(f"  Average Mon-Yesterday: {yesterday_avg:.0f} kcal")
                    else:
                        print("  Average Mon-Yesterday: -")
                    print(f"  Average Mon-Today: {today_avg:.0f} kcal")
                    
                # Display Budgets
                print("Budgets:")
                if include_today == 'no':
                    print(f"  Starting Today: {budg_starting_today_str}")
                elif include_today == 'yes':
                    print(f"  Starting Tomorrow: {budg_starting_tomorrow_str}")
                elif include_today == 'both':
                    print(f"  Starting Today: {budg_starting_today_str}")
                    print(f"  Starting Tomorrow: {budg_starting_tomorrow_str}")
            
            # Print breakdown table
            print("-" * 70)
            print(f"{'Day':<10} | {'Date':<10} | {'Kcal':<6} | {'Protein':<8} | {'Target Diff':<11} | {'Completeness':<12}")
            print("-" * 70)
            for d in days:
                kcal_str = f"{d['kcal']}" if d['has_data'] or d['kcal'] > 0 else "-"
                p_str = f"{d['protein']:.0f}g" if (d['has_data'] or d['protein'] > 0) else "-"
                
                diff_str = "-"
                if goal_cal and (d['has_data'] or d['kcal'] > 0):
                    diff = d['kcal'] - goal_cal
                    diff_str = f"{'+' if diff >= 0 else ''}{diff}"
                    
                print(f"{d['day_name'][:10]:<10} | {d['date_str']:<10} | {kcal_str:<6} | {p_str:<8} | {diff_str:<11} | {d['completeness'].upper():<12}")
            print("=" * 70)
        
    conn.close()

def cmd_stats_trend(args):
    conn = get_db(args.database)
    today_str = args.today or date.today().isoformat()
    
    print("-" * 60)
    print("MACRONUTRIENT TRENDS (ROLLING AVERAGES)")
    print("-" * 60)
    
    # Query rolling averages directly from v_daily_rolling_trends up to today
    row = conn.execute('''
        SELECT rolling_7_cal, rolling_7_p, 
               rolling_30_cal, rolling_30_p, 
               rolling_90_cal, rolling_90_p
        FROM v_daily_rolling_trends
        WHERE date <= ?
        ORDER BY date DESC LIMIT 1
    ''', (today_str,)).fetchone()
    
    conn.close()
    
    if not row:
        print("No trend data available.")
        print("-" * 60)
        return
        
    for days, suffix in [(7, '7'), (30, '30'), (90, '90')]:
        cal = row[f'rolling_{suffix}_cal']
        p = row[f'rolling_{suffix}_p']
        
        cal_val = f"{cal:.0f} kcal" if cal is not None else "No data"
        p_val = f" | {p:.1f}g Protein" if p is not None else ""
        print(f"Last {days:2d} Days: {cal_val}{p_val}")
        
    print("-" * 60)

def cmd_stats_weight(args):
    conn = get_db(args.database)
    today_str = args.today or date.today().isoformat()
    
    entries = args.entries
    days = args.days
    
    if entries is None and days is None:
        entries = 5
        
    query = 'SELECT date, weight_kg, bmi, change_kg FROM v_weight_summary WHERE date <= ?'
    params = [today_str]
    
    if days is not None:
        query += ' AND date >= date(?, ?)'
        params.extend([today_str, f'-{days} days'])
        
    query += ' ORDER BY date DESC'
    
    if entries is not None and entries != 'all':
        query += ' LIMIT ?'
        params.append(entries)
        
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    print("-" * 60)
    if entries is not None and days is not None:
        header = f"WEIGHT TRENDS (LAST {entries} ENTRIES OVER LAST {days} DAYS)"
    elif entries is not None:
        header = f"WEIGHT TRENDS (LAST {entries} ENTRIES)" if entries != "all" else "WEIGHT TRENDS (ALL ENTRIES)"
    else:
        header = f"WEIGHT TRENDS (LAST {days} DAYS)"
    print(header)
    print("-" * 60)
    
    if not rows:
        print("No weight logs found.")
        return
        
    rows = list(rows)
    rows.reverse()
        
    for r in rows:
        ch_str = f" ({r['change_kg']:+.1f} kg)" if r['change_kg'] is not None else ""
        bmi_str = f"{r['bmi']:.1f}" if r['bmi'] is not None else "N/A"
        print(f"  {r['date']}: {r['weight_kg']:.1f} kg{ch_str} | BMI: {bmi_str}")
        
    if len(rows) >= 2:
        change = rows[-1]['weight_kg'] - rows[0]['weight_kg']
        print("-" * 60)
        print(f"Total Change: {change:+.1f} kg (from {rows[0]['weight_kg']:.1f} to {rows[-1]['weight_kg']:.1f})")
    print("-" * 60)

def cmd_stats_waist(args):
    args.type = 'waist'
    cmd_stats_measure(args)

def cmd_stats_measure(args):
    conn = get_db(args.database)
    today_str = args.today or date.today().isoformat()
    
    type_key = args.type.lower()
    t_row = conn.execute("SELECT name, unit FROM measurement_types WHERE key = ?", (type_key,)).fetchone()
    if not t_row:
        print(f"Error: Measurement type '{type_key}' is not defined.")
        conn.close()
        sys.exit(1)
        
    type_name = t_row['name']
    unit = t_row['unit']
    
    entries = args.entries
    days = args.days
    
    if entries is None and days is None:
        entries = 5
        
    query = 'SELECT date, value, notes, whtr, change_val FROM v_measurement_summary WHERE type_key = ? AND date <= ?'
    params = [type_key, today_str]
    
    if days is not None:
        query += ' AND date >= date(?, ?)'
        params.extend([today_str, f'-{days} days'])
        
    query += ' ORDER BY date DESC'
    
    if entries is not None and entries != 'all':
        query += ' LIMIT ?'
        params.append(entries)
        
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    print("-" * 60)
    header_name = type_name.upper()
    if entries is not None and days is not None:
        header = f"{header_name} TRENDS (LAST {entries} ENTRIES OVER LAST {days} DAYS)"
    elif entries is not None:
        header = f"{header_name} TRENDS (LAST {entries} ENTRIES)" if entries != "all" else f"{header_name} TRENDS (ALL ENTRIES)"
    else:
        header = f"{header_name} TRENDS (LAST {days} DAYS)"
    print(header)
    print("-" * 60)
    
    if not rows:
        print(f"No {type_key} logs found.")
        return
        
    rows = list(rows)
    rows.reverse()
    
    for r in rows:
        val = r['value']
        ch = r['change_val']
        whtr = r['whtr']
        notes = r['notes']
        
        val_str = format_value(val)
        ch_str = format_change(ch, unit)
        
        extra_str = ""
        if type_key == 'waist':
            whtr_str = f"{whtr:.2f}" if whtr is not None else "N/A"
            extra_str = f" | WHtR: {whtr_str}"
            
        notes_str = f" | notes: {notes}" if notes else ""
        print(f"  {r['date']}: {val_str} {unit}{ch_str}{extra_str}{notes_str}")
        
    if len(rows) >= 2:
        change = rows[-1]['value'] - rows[0]['value']
        val_start = format_value(rows[0]['value'])
        val_end = format_value(rows[-1]['value'])
        change_str = f"{change:+.1f}" if abs(change - round(change, 1)) < 1e-9 else f"{change:+.2f}"
        if change == 0.0:
            change_str = "+0.0"
        elif change > 0 and not change_str.startswith("+"):
            change_str = "+" + change_str
        print("-" * 60)
        print(f"Total Change: {change_str} {unit} (from {val_start} to {val_end})")
    print("-" * 60)

def cmd_search(args):
    conn = get_db(args.database)
    
    # 1. Get all unique food profiles from the database
    profiles = conn.execute('''
        SELECT food_name, calories, protein, carbs, fat, meal_type, COUNT(*) as count, MAX(date) as last_logged
        FROM entries
        GROUP BY food_name, calories, protein, carbs, fat, meal_type
    ''').fetchall()
    conn.close()
    
    if not profiles:
        print("Database is empty. No foods registered yet.")
        return

    # 2. Filter profiles using substring and fuzzy matching
    query_lower = args.query.lower()
    
    # Exact/substring matches (highest priority)
    substring_matches = []
    other_profiles = []
    for p in profiles:
        if query_lower in p['food_name'].lower():
            substring_matches.append(p)
        else:
            other_profiles.append(p)
            
    # Fuzzy matches for remaining names using word-based SequenceMatcher
    fuzzy_matches_with_ratio = []
    for p in other_profiles:
        words = p['food_name'].lower().split()
        if not words:
            continue
        max_ratio = max(difflib.SequenceMatcher(None, query_lower, w).ratio() for w in words)
        if max_ratio >= 0.6:
            fuzzy_matches_with_ratio.append((p, max_ratio))
            
    # Sort fuzzy matches by similarity ratio, then count, then last_logged
    fuzzy_matches_with_ratio = sorted(fuzzy_matches_with_ratio, key=lambda x: (x[1], x[0]['count'], x[0]['last_logged']), reverse=True)
    fuzzy_matches = [x[0] for x in fuzzy_matches_with_ratio]
    
    # Sort substring matches by frequency and recency
    substring_matches = sorted(substring_matches, key=lambda x: (x['count'], x['last_logged']), reverse=True)
    
    matches = (substring_matches + fuzzy_matches)[:args.limit]

    if not matches:
        print(f"No similar registered foods found for '{args.query}'")
        return

    print(f"Found {len(matches)} similar registered food(s):")
    for r in matches:
        p_str = f" {r['protein']:.1f}g P" if r['protein'] is not None else "no protein"
        c_str = f" | {r['carbs']:.1f}g C" if r['carbs'] is not None else ""
        f_str = f" | {r['fat']:.1f}g F" if r['fat'] is not None else ""
        macros = f"({p_str}{c_str}{f_str})"
        
        print(f"\n  * {r['food_name']} ({r['calories']} kcal) - {r['meal_type']}")
        print(f"    Macros: {macros}")
        print(f"    History: Logged {r['count']}x (last used: {r['last_logged']})")
        
        # Build helper copy-paste command
        cmd_macros = ""
        if r['protein'] is not None:
            cmd_macros += f" {r['protein']}"
            if r['carbs'] is not None:
                cmd_macros += f" {r['carbs']}"
                if r['fat'] is not None:
                    cmd_macros += f" {r['fat']}"
                    
        print(f"    Log command: python scripts/tracker.py add \"{r['food_name']}\" {r['calories']}{cmd_macros} --meal {r['meal_type']}")

def valid_date(s):
    try:
        return date.fromisoformat(s).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{s}'. Must be YYYY-MM-DD.")

def entries_type(s):
    if s.lower() == "all":
        return "all"
    try:
        val = int(s)
        if val <= 0:
            raise argparse.ArgumentTypeError(f"Invalid entries value: '{s}'. Must be a positive integer or 'all'.")
        return val
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid entries value: '{s}'. Must be a positive integer or 'all'.")

# ----------------- CLI Main parsing -----------------

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="Consolidated Calorie Tracker CLI")
    parser.add_argument("--database", default="./health_data.db", help="Path to SQLite database file")
    parser.add_argument("--today", type=valid_date, help="Simulate today's date as YYYY-MM-DD")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # goal command
    p_goal = subparsers.add_parser("goal", help="Set daily calorie & protein goals")
    p_goal.add_argument("calories", type=int, help="Calorie goal (kcal)")
    p_goal.add_argument("protein", type=float, nargs="?", default=None, help="Protein goal (grams, optional)")
    p_goal.add_argument("--height", type=float, default=None, help="Height in cm (optional, defaults to keeping current or 180.0)")
    
    # add command
    p_add = subparsers.add_parser("add", help="Add a food entry")
    p_add.add_argument("food_name", help="Description of food consumed")
    p_add.add_argument("calories", type=int, help="Calories in entry (kcal)")
    p_add.add_argument("protein", type=float, nargs="?", default=None, help="Protein in grams")
    p_add.add_argument("carbs", type=float, nargs="?", default=None, help="Carbohydrates in grams")
    p_add.add_argument("fat", type=float, nargs="?", default=None, help="Fat in grams")
    p_add.add_argument("--meal", required=True, help="Meal type (breakfast, lunch, dinner, etc.)")
    p_add.add_argument("--date", help="Date YYYY-MM-DD (defaults to today)")
    
    # list command
    p_list = subparsers.add_parser("list", help="List food entries for a date")
    p_list.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD (defaults to today)")
    p_list.add_argument("--no-group", action="store_true", help="Do not group entries by meal type (shows timestamps and entry IDs)")
    
    # update command
    p_upd = subparsers.add_parser("update", help="Update a food entry by ID")
    p_upd.add_argument("id", type=int, help="Entry ID to update")
    p_upd.add_argument("--name", help="New description")
    p_upd.add_argument("--cal", type=int, help="New calories")
    p_upd.add_argument("--p", type=float, help="New protein")
    p_upd.add_argument("--c", type=float, help="New carbs")
    p_upd.add_argument("--f", type=float, help="New fat")
    p_upd.add_argument("--meal", help="New meal type")
    
    # delete command
    p_del = subparsers.add_parser("delete", help="Delete a food entry by ID")
    p_del.add_argument("id", type=int, help="Entry ID to delete")
    
    # complete command
    p_comp = subparsers.add_parser("complete", help="Mark a day's tracking as completed")
    p_comp.add_argument("date", help="Date YYYY-MM-DD")
    p_comp.add_argument("--completeness", default="full", choices=["full", "partial", "minimal"], help="Completeness quality level")
    p_comp.add_argument("--notes", help="Optional daily notes")
    
    # check-complete command
    p_check = subparsers.add_parser("check-complete", help="Check day completeness status")
    p_check.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD")
    
    # weight command
    p_w = subparsers.add_parser("weight", help="Log body weight")
    p_w.add_argument("kg", type=float, help="Weight in kg")
    p_w.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD")
    
    # waist command
    p_wa = subparsers.add_parser("waist", help="Log waist circumference")
    p_wa.add_argument("cm", type=float, help="Waist circumference in cm")
    p_wa.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD")
    p_wa.add_argument("--notes", help="Optional notes/annotations for this waist entry")
    
    # measure command
    p_me = subparsers.add_parser("measure", help="Log a body measurement")
    p_me.add_argument("type", help="Measurement type (e.g. waist, hips, body_fat)")
    p_me.add_argument("value", type=float, help="Measurement value")
    p_me.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD (defaults to today)")
    p_me.add_argument("--notes", help="Optional notes/annotations for this measurement entry")
    
    # measure-type command group
    p_mt = subparsers.add_parser("measure-type", help="Manage measurement types")
    mt_sub = p_mt.add_subparsers(dest="measure_type_command", required=True)
    
    # measure-type define
    mt_def = mt_sub.add_parser("define", help="Define a custom measurement type")
    mt_def.add_argument("key", help="Unique key for the type (lowercase alphanumeric + underscores)")
    mt_def.add_argument("name", help="Display name (e.g. 'Hip (Upper)')")
    mt_def.add_argument("unit", help="Measurement unit (e.g. cm, in, %)")
    mt_def.add_argument("--desc", help="Optional description of measurement point")
    
    # measure-type list
    mt_list = mt_sub.add_parser("list", help="List all defined measurement types")
    
    # measure-type delete
    mt_del = mt_sub.add_parser("delete", help="Delete a measurement type")
    mt_del.add_argument("key", help="Key of the measurement type to delete")
    
    # stats command group
    p_stats = subparsers.add_parser("stats", help="Get statistics and reports")
    s_sub = p_stats.add_subparsers(dest="stats_command", required=True)
    
    # stats day
    s_day = s_sub.add_parser("day", help="Show daily breakdown")
    s_day.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD")
    s_day.add_argument("--no-group", action="store_true", help="Do not group entries by meal type (shows timestamps and entry IDs)")
    
    # stats week
    s_week = s_sub.add_parser("week", help="Show weekly averages and breakdown")
    s_week.add_argument("date", nargs="?", default=None, help="Date YYYY-MM-DD")
    s_week.add_argument("--weeks", type=int, default=1, help="Number of weeks to show (default: 1)")
    s_week.add_argument("--compact", action="store_true", help="Print a single-line compact summary for each week")
    s_week.add_argument("--include-today", choices=["auto", "yes", "no", "both"], default="auto", help="Include today's data in averages and budgets (default: auto)")
    
    # stats trend
    s_trend = s_sub.add_parser("trend", help="Show macronutrient rolling averages")
    s_trend.add_argument("--days", type=int, default=30, help="Number of days to look back")
    
    # stats weight
    s_w = s_sub.add_parser("weight", help="Show weight logs and changes")
    s_w.add_argument("-N", "--entries", type=entries_type, default=None, help="Number of entries to show (positive integer or 'all')")
    s_w.add_argument("--days", type=int, default=None, help="Number of days to look back")
    
    # stats waist
    s_wa = s_sub.add_parser("waist", help="Show waist logs and changes")
    s_wa.add_argument("-N", "--entries", type=entries_type, default=None, help="Number of entries to show (positive integer or 'all')")
    s_wa.add_argument("--days", type=int, default=None, help="Number of days to look back")
    
    # stats measure
    s_me = s_sub.add_parser("measure", help="Show logs and changes for a specific measurement type")
    s_me.add_argument("type", help="Measurement type key (e.g. waist, hips, body_fat)")
    s_me.add_argument("-N", "--entries", type=entries_type, default=None, help="Number of entries to show (positive integer or 'all')")
    s_me.add_argument("--days", type=int, default=None, help="Number of days to look back")
    
    # search command
    p_search = subparsers.add_parser("search", help="Search previously registered foods")
    p_search.add_argument("query", help="Food name query (supports fuzzy matching)")
    p_search.add_argument("--limit", type=int, default=5, help="Max number of results to display")
    
    args = parser.parse_args()
    
    # Ensure database folder exists and is initialized
    db_path = Path(args.database).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    init_db(db_path)
    
    if args.command == "goal":
        cmd_goal(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "complete":
        cmd_complete(args)
    elif args.command == "check-complete":
        cmd_check_complete(args)
    elif args.command == "weight":
        cmd_weight(args)
    elif args.command == "waist":
        cmd_waist(args)
    elif args.command == "measure":
        cmd_measure(args)
    elif args.command == "measure-type":
        cmd_measure_type(args)
    elif args.command == "stats":
        if args.stats_command == "day":
            cmd_stats_day(args)
        elif args.stats_command == "week":
            cmd_stats_week(args)
        elif args.stats_command == "trend":
            cmd_stats_trend(args)
        elif args.stats_command == "weight":
            cmd_stats_weight(args)
        elif args.stats_command == "waist":
            cmd_stats_waist(args)
        elif args.stats_command == "measure":
            cmd_stats_measure(args)
    elif args.command == "search":
        cmd_search(args)

if __name__ == "__main__":
    main()
