#!/usr/bin/env python3
"""
Tachograph Database Health Check
Checks database integrity and creates report.
"""

import sqlite3
import json
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tachograph.db')
REPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'summaries', 'health-report.json')


def check_integrity(conn):
    """PRAGMA integrity_check - Full check."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check")
    result = cursor.fetchone()[0]
    return result == 'ok', result


def check_quick_check(conn):
    """PRAGMA quick_check - Faster check."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA quick_check")
    result = cursor.fetchone()[0]
    return result == 'ok', result


def check_foreign_keys(conn):
    """PRAGMA foreign_key_check - Check foreign keys."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_key_check")
    violations = cursor.fetchall()
    return len(violations) == 0, violations


def get_table_stats(conn):
    """Statistics for all tables."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    stats = {}
    for table in tables:
        if table.startswith('sqlite_'):
            continue
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cursor.fetchone()[0]
    return stats


def get_db_info(conn):
    """Datenbank-Informationen."""
    cursor = conn.cursor()
    
    # Page size und page count
    cursor.execute("PRAGMA page_size")
    page_size = cursor.fetchone()[0]
    cursor.execute("PRAGMA page_count")
    page_count = cursor.fetchone()[0]
    
    # Freie Pages
    cursor.execute("PRAGMA freelist_count")
    freelist_count = cursor.fetchone()[0]
    
    # Incremental vacuum
    cursor.execute("PRAGMA auto_vacuum")
    auto_vacuum = cursor.fetchone()[0]
    
    return {
        'page_size': page_size,
        'page_count': page_count,
        'freelist_count': freelist_count,
        'auto_vacuum': auto_vacuum,
        'estimated_size': page_size * page_count,
        'used_size': page_size * (page_count - freelist_count)
    }


def main():
    """Hauptfunktion: Health Check durchführen."""
    print("=" * 50)
    print("Tachograph Database Health Check")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Prüfe DB-Datei
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Datenbank nicht gefunden: {DB_PATH}")
        sys.exit(1)
    
    db_size = os.path.getsize(DB_PATH)
    print(f"Datenbank: {DB_PATH} ({db_size:,} Bytes)")
    
    conn = sqlite3.connect(DB_PATH)
    
    report = {
        'timestamp': start_time.isoformat(),
        'db_path': os.path.abspath(DB_PATH),
        'db_size': db_size,
        'checks': {},
        'table_stats': {},
        'db_info': {},
        'overall_health': 'unknown'
    }
    
    all_ok = True
    
    # 1. Integrity Check
    print("\n[1/4] Integrity Check...")
    try:
        ok, result = check_integrity(conn)
        report['checks']['integrity'] = {
            'status': 'ok' if ok else 'failed',
            'result': result
        }
        print(f"  {'✓' if ok else '✗'} Integrity: {result}")
        if not ok:
            all_ok = False
    except Exception as e:
        report['checks']['integrity'] = {'status': 'error', 'error': str(e)}
        print(f"  ✗ Integrity check failed: {e}")
        all_ok = False
    
    # 2. Quick Check
    print("[2/4] Quick Check...")
    try:
        ok, result = check_quick_check(conn)
        report['checks']['quick_check'] = {
            'status': 'ok' if ok else 'failed',
            'result': result
        }
        print(f"  {'✓' if ok else '✗'} Quick Check: {result}")
        if not ok:
            all_ok = False
    except Exception as e:
        report['checks']['quick_check'] = {'status': 'error', 'error': str(e)}
        print(f"  ✗ Quick check failed: {e}")
        all_ok = False
    
    # 3. Foreign Key Check
    print("[3/4] Foreign Key Check...")
    try:
        ok, violations = check_foreign_keys(conn)
        report['checks']['foreign_keys'] = {
            'status': 'ok' if ok else 'violations_found',
            'violations': violations,
            'count': len(violations)
        }
        if ok:
            print(f"  ✓ Foreign Keys: No violations")
        else:
            print(f"  ✗ Foreign Keys: {len(violations)} violation(s)")
            for v in violations:
                print(f"    - {v}")
        if not ok:
            all_ok = False
    except Exception as e:
        report['checks']['foreign_keys'] = {'status': 'error', 'error': str(e)}
        print(f"  ✗ Foreign key check failed: {e}")
        all_ok = False
    
    # 4. Table Statistics
    print("[4/4] Table Statistics...")
    try:
        stats = get_table_stats(conn)
        report['table_stats'] = stats
        for table, count in sorted(stats.items()):
            print(f"  {table}: {count:,} rows")
    except Exception as e:
        report['table_stats'] = {'error': str(e)}
        print(f"  ✗ Failed to get table stats: {e}")
        all_ok = False
    
    # DB Info
    try:
        db_info = get_db_info(conn)
        report['db_info'] = db_info
        print(f"\nDB Info:")
        print(f"  Page Size: {db_info['page_size']:,} bytes")
        print(f"  Page Count: {db_info['page_count']:,}")
        print(f"  Free Pages: {db_info['freelist_count']:,}")
        print(f"  Estimated Size: {db_info['estimated_size']:,} bytes")
        print(f"  Used Size: {db_info['used_size']:,} bytes")
    except Exception as e:
        report['db_info'] = {'error': str(e)}
        print(f"  ✗ Failed to get DB info: {e}")
    
    conn.close()
    
    # Overall Health
    end_time = datetime.now()
    duration_ms = (end_time - start_time).total_seconds() * 1000
    
    report['overall_health'] = 'healthy' if all_ok else 'unhealthy'
    report['duration_ms'] = int(duration_ms)
    report['end_time'] = end_time.isoformat()
    
    # Report schreiben
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n{'=' * 50}")
    print(f"Overall Health: {'✓ HEALTHY' if all_ok else '✗ UNHEALTHY'}")
    print(f"Report: {REPORT_FILE}")
    print(f"Duration: {int(duration_ms)}ms")
    
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
