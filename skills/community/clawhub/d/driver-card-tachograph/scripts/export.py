#!/usr/bin/env python3
"""
Tachograph Data Export
Exports SQLite data as CSV for drivers/authorities.
"""

import sqlite3
import csv
import os
import sys
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tachograph.db')
EXPORT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'exports')
SUMMARIES_DIR = os.path.join(os.path.dirname(__file__), '..', 'summaries')
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'export.log')
SUMMARY_FILE = os.path.join(SUMMARIES_DIR, f'export-summary-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')

# Summaries directory erstellen
os.makedirs(SUMMARIES_DIR, exist_ok=True)

def log(level, msg):
    """Meaningful logging with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def log_error(msg):
    log("ERROR", msg)

def log_info(msg):
    log("INFO", msg)

def log_success(msg):
    log("SUCCESS", msg)

def ensure_export_dir():
    """Create export directory if it doesn't exist."""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
        log_info(f"Export directory created: {EXPORT_DIR}")

def export_table(table_name, columns, filename):
    """Exports a table to CSV with validation."""
    output_path = os.path.join(EXPORT_DIR, filename)
    export_details = {
        'table': table_name,
        'filename': filename,
        'status': 'pending',
        'rows_exported': 0,
        'file_size': 0,
        'error': None
    }
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not cursor.fetchone():
            export_details['status'] = 'failed'
            export_details['error'] = 'Table not found'
            log_error(f"Table not found: {table_name}")
            return False, export_details
        
        # Fetch data
        cursor.execute(f"SELECT {','.join(columns)} FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            log_warn(f"No data in table: {table_name}")
            export_details['status'] = 'empty'
            # Create empty file with header
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
            export_details['file_size'] = os.path.getsize(output_path)
            return True, export_details
        
        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)  # Header
            writer.writerows(rows)
        
        file_size = os.path.getsize(output_path)
        export_details['status'] = 'success'
        export_details['rows_exported'] = len(rows)
        export_details['file_size'] = file_size
        
        log_success(f"Exported: {table_name} → {filename} ({len(rows)} rows, {file_size:,} Bytes)")
        return True, export_details
        
    except sqlite3.Error as e:
        export_details['status'] = 'failed'
        export_details['error'] = str(e)
        log_error(f"SQLite error during export of {table_name}: {e}")
        return False, export_details
    except IOError as e:
        export_details['status'] = 'failed'
        export_details['error'] = str(e)
        log_error(f"IO error writing {filename}: {e}")
        return False, export_details
    except Exception as e:
        export_details['status'] = 'failed'
        export_details['error'] = str(e)
        log_error(f"Unexpected error during export of {table_name}: {e}")
        return False, export_details

def log_warn(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [WARN] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def main():
    """Main function: Export all relevant tables."""
    print("=" * 50)
    print("Tachograph Data Export")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Check DB file
    if not os.path.exists(DB_PATH):
        log_error(f"Database not found: {DB_PATH}")
        sys.exit(1)
    
    db_size = os.path.getsize(DB_PATH)
    log_info(f"Database found: {DB_PATH} ({db_size:,} Bytes)")
    
    # Check DB integrity
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]
        conn.close()
        if integrity != 'ok':
            log_warn(f"DB integrity check: {integrity}")
        else:
            log_info("DB integrity check: OK")
    except Exception as e:
        log_error(f"DB integrity check failed: {e}")
    
    ensure_export_dir()
    
    # Export configuration: (table, columns, filename)
    exports = [
        ('driver_cards', 
         ['id', 'card_number', 'issuing_member_state', 'issuing_authority', 
          'issue_date', 'validity_begin', 'expiry_date', 'driver_surname', 
          'driver_first_names', 'birth_date', 'preferred_language', 'imported_at'],
         'drivers.csv'),
        
        ('daily_activities',
         ['id', 'card_number', 'record_date', 'presence_counter', 'day_distance', 'imported_at'],
         'activities.csv'),
        
        ('vehicles_used',
         ['id', 'card_number', 'vehicle_registration_nation', 'vehicle_registration_number',
          'vu_approval_number', 'vu_serial_number', 'first_use', 'last_use', 'imported_at'],
         'vehicles.csv'),
        
        ('work_periods',
         ['id', 'card_number', 'entry_time', 'entry_type_daily_work_period',
          'daily_work_period_country', 'daily_work_period_region', 
          'vehicle_odometer_value', 'imported_at'],
         'work_periods.csv'),
    ]
    
    success_count = 0
    fail_count = 0
    export_details = []
    total_rows = 0
    total_bytes = 0
    
    for table, columns, filename in exports:
        success, details = export_table(table, columns, filename)
        export_details.append(details)
        if success:
            success_count += 1
            total_rows += details.get('rows_exported', 0)
            total_bytes += details.get('file_size', 0)
        else:
            fail_count += 1
    
    end_time = datetime.now()
    duration_ms = (end_time - start_time).total_seconds() * 1000
    
    # Summary JSON schreiben
    summary = {
        'timestamp': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_ms': int(duration_ms),
        'db_path': os.path.abspath(DB_PATH),
        'db_size': db_size,
        'db_integrity': integrity if 'integrity' in dir() else 'unknown',
        'exports': export_details,
        'summary': {
            'total_exports': len(exports),
            'successful': success_count,
            'failed': fail_count,
            'total_rows_exported': total_rows,
            'total_bytes_exported': total_bytes
        }
    }
    
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(summary, f, indent=2)
    log_info(f"Summary geschrieben: {SUMMARY_FILE}")
    
    print("=" * 50)
    log_info(f"Export completed: {success_count} successful, {fail_count} failed")
    log_info(f"Total: {total_rows} rows, {total_bytes:,} Bytes in {int(duration_ms)}ms")
    
    if fail_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()