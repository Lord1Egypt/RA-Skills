#!/usr/bin/env python3
"""
Query the Family Medical Records SQLite database.
Provides helper functions for common queries.
"""

import sqlite3
import os
import sys
import json
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "medical_records.db")

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "medical_records.db"))

def get_connection(db_path: str = None):
    if db_path is None:
        db_path = get_db_path()
    return sqlite3.connect(db_path)

# ─── Member Queries ───────────────────────────────────────────────────────────


def require_db(db_path: str = None) -> str:
    """Ensure database exists and is initialized. Auto-initializes if missing."""
    import subprocess
    path = get_db_path() if db_path is None else db_path
    if not os.path.exists(path):
        print("[INFO] Database not found. Initializing...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ["python3", os.path.join(script_dir, "init_db.py")],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError("[ERROR] Auto-init failed: " + result.stderr.strip())
        print("[OK] Database auto-initialized.")
    return path

def list_members(db_path: str = None) -> list:
    """Return all family members."""
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT id, member_code, name, relationship, dob, gender 
        FROM members ORDER BY id
    """).fetchall()
    conn.close()
    return rows

def get_member(member_code: str, db_path: str = None) -> dict:
    """Return full profile for a member."""
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not row:
        conn.close()
        return None
    cols = [desc[0] for desc in conn.execute("SELECT * FROM members WHERE member_code = ?", (member_code,)).description]
    conn.close()
    return dict(zip(cols, row))

def get_member_allergies(member_code: str, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        return []
    rows = conn.execute("SELECT * FROM allergies WHERE member_id = ?", (member_row[0],)).fetchall()
    conn.close()
    return rows

def get_member_medical_history(member_code: str, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        return []
    rows = conn.execute("SELECT * FROM medical_history WHERE member_id = ?", (member_row[0],)).fetchall()
    conn.close()
    return rows

def get_member_current_medications(member_code: str, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        return []
    cols = [desc[0] for desc in conn.execute("SELECT * FROM medications WHERE 1=0").description]
    rows = conn.execute("""
        SELECT * FROM medications 
        WHERE member_id = ? AND status = 'Current'
        ORDER BY start_date DESC
    """, (member_row[0],)).fetchall()
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

# ─── Visit Queries ─────────────────────────────────────────────────────────────

def get_visits(member_code: str, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        conn.close()
        return []
    rows = conn.execute("""
        SELECT * FROM visits 
        WHERE member_id = ? ORDER BY visit_date DESC
    """, (member_row[0],)).fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM visits WHERE 1=0").description]
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

def get_visit(visit_id: str, db_path: str = None) -> dict:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM visits WHERE visit_id = ?", (visit_id,)).fetchone()
    conn.close()
    if not row:
        return None
    cols = [desc[0] for desc in conn.execute("SELECT * FROM visits WHERE 1=0").description]
    return dict(zip(cols, row))

def get_recent_visits(member_code: str, days: int = 30, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        conn.close()
        return []
    rows = conn.execute("""
        SELECT * FROM visits 
        WHERE member_id = ? AND visit_date >= date('now', ?)
        ORDER BY visit_date DESC
    """, (member_row[0], f"-{days} days")).fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM visits WHERE 1=0").description]
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

# ─── Medication Queries ───────────────────────────────────────────────────────

def get_medications(member_code: str = None, visit_id: str = None, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    if member_code:
        member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
        if not member_row:
            conn.close()
            return []
        rows = conn.execute("""
            SELECT * FROM medications 
            WHERE member_id = ? ORDER BY start_date DESC
        """, (member_row[0],)).fetchall()
    elif visit_id:
        rows = conn.execute("SELECT * FROM medications WHERE visit_id = ?", (visit_id,)).fetchall()
    else:
        conn.close()
        return []
    cols = [desc[0] for desc in conn.execute("SELECT * FROM medications WHERE 1=0").description]
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

def get_medication_tracking(medication_id: str, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT * FROM medication_tracking 
        WHERE medication_id = ? ORDER BY dose_number
    """, (medication_id,)).fetchall()
    conn.close()
    return rows

def get_next_dose(medication_id: str, db_path: str = None) -> dict:
    """Get the next pending dose for a medication."""
    conn = get_connection(db_path)
    row = conn.execute("""
        SELECT * FROM medication_tracking 
        WHERE medication_id = ? AND status = 'pending'
        ORDER BY dose_number LIMIT 1
    """, (medication_id,)).fetchone()
    conn.close()
    if not row:
        return None
    cols = [desc[0] for desc in conn.execute("SELECT * FROM medication_tracking WHERE 1=0").description]
    return dict(zip(cols, row))

# ─── Exam Queries ─────────────────────────────────────────────────────────────

def get_exams(member_code: str = None, visit_id: str = None, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    if member_code:
        member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
        if not member_row:
            conn.close()
            return []
        rows = conn.execute("""
            SELECT * FROM exams 
            WHERE member_id = ? ORDER BY exam_date DESC
        """, (member_row[0],)).fetchall()
    elif visit_id:
        rows = conn.execute("SELECT * FROM exams WHERE visit_id = ?", (visit_id,)).fetchall()
    else:
        conn.close()
        return []
    cols = [desc[0] for desc in conn.execute("SELECT * FROM exams WHERE 1=0").description]
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

# ─── Daily Vitals Queries ─────────────────────────────────────────────────────

def get_vitals(member_code: str, year: int = None, db_path: str = None) -> list:
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        conn.close()
        return []
    if year:
        rows = conn.execute("""
            SELECT * FROM daily_vitals 
            WHERE member_id = ? AND record_date LIKE ?
            ORDER BY record_date DESC
        """, (member_row[0], f"{year}%")).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM daily_vitals 
            WHERE member_id = ? ORDER BY record_date DESC LIMIT 30
        """, (member_row[0],)).fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM daily_vitals WHERE 1=0").description]
    conn.close()
    return [dict(zip(cols, r)) for r in rows]

# ─── Dashboard / Summary ─────────────────────────────────────────────────────

def get_family_summary(db_path: str = None) -> dict:
    """Get a summary of all family members and key stats."""
    db_path = require_db(db_path)
    conn = get_connection(db_path)
    members = conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    visits = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    medications = conn.execute("SELECT COUNT(*) FROM medications").fetchone()[0]
    current_meds = conn.execute("SELECT COUNT(*) FROM medications WHERE status = 'Current'").fetchone()[0]
    exams = conn.execute("SELECT COUNT(*) FROM exams").fetchone()[0]
    conn.close()
    return {
        "total_members": members,
        "total_visits": visits,
        "total_medications": medications,
        "current_medications": current_meds,
        "total_exams": exams
    }

# ─── CLI Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = get_db_path()
    
    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found at {db_path}")
        print("Run init_db.py first to create the database.")
        sys.exit(1)
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    
    if cmd == "summary":
        s = get_family_summary(db_path)
        print("=== Family Medical Records Summary ===")
        print(f"  Members: {s['total_members']}")
        print(f"  Visits: {s['total_visits']}")
        print(f"  Medications (total): {s['total_medications']}")
        print(f"  Current medications: {s['current_medications']}")
        print(f"  Exams: {s['total_exams']}")
    
    elif cmd == "members":
        rows = list_members(db_path)
        print("=== Family Members ===")
        for r in rows:
            print(f"  [{r[0]}] {r[1]} - {r[2]} ({r[3]}) - DOB: {r[4]}")
    
    elif cmd == "visits" and len(sys.argv) > 2:
        rows = get_visits(sys.argv[2], db_path)
        print(f"=== Visits for {sys.argv[2]} ===")
        for r in rows:
            print(f"  {r['visit_id']} | {r['visit_date']} | {r['institution']} | {r['primary_diagnosis']}")
    
    elif cmd == "meds" and len(sys.argv) > 2:
        rows = get_medications(member_code=sys.argv[2], db_path=db_path)
        print(f"=== Medications for {sys.argv[2]} ===")
        for r in rows:
            print(f"  {r['medication_id']} | {r['drug_name']} | {r['status']} | {r['start_date']}")
    
    elif cmd == "current-meds" and len(sys.argv) > 2:
        rows = get_member_current_medications(sys.argv[2], db_path)
        print(f"=== Current Medications for {sys.argv[2]} ===")
        for r in rows:
            print(f"  {r['drug_name']} | {r['dosage']} | {r['frequency']} | Start: {r['start_date']}")
    
    elif cmd == "next-dose" and len(sys.argv) > 2:
        d = get_next_dose(sys.argv[2], db_path)
        if d:
            print(f"Next dose: #{d['dose_number']} planned for {d['planned_date']} [{d['status']}]")
        else:
            print("No pending doses found.")
    
    else:
        print("Usage:")
        print("  query_db.py summary")
        print("  query_db.py members")
        print("  query_db.py visits <member_code>")
        print("  query_db.py meds <member_code>")
        print("  query_db.py current-meds <member_code>")
        print("  query_db.py next-dose <medication_id>")
