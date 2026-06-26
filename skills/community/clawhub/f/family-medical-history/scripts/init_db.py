#!/usr/bin/env python3
"""
Initialize SQLite database for Family Medical Records.
Creates all required tables if they don't exist.
"""

import sqlite3
import os
import sys
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "medical_records.db")

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "medical_records.db"))

def init_db(db_path: str = None) -> None:
    if db_path is None:
        db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_code TEXT UNIQUE NOT NULL,
            name TEXT,
            relationship TEXT,
            dob TEXT,
            gender TEXT,
            blood_type TEXT,
            rh_factor TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            severe_allergies TEXT,
            current_conditions TEXT,
            current_medications TEXT,
            id_number TEXT,
            insurance_number TEXT,
            hospital档案号 TEXT,
            smoking_history TEXT,
            drinking_history TEXT,
            diet_preference TEXT,
            occupation_risk TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Allergies table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS allergies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            allergy_type TEXT NOT NULL, -- drug, food, environmental
            allergen TEXT NOT NULL,
            reaction TEXT,
            severity TEXT, -- mild, moderate, severe, life_threatening
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Medical history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            condition_name TEXT NOT NULL,
            diagnosis_year TEXT,
            status TEXT NOT NULL, -- Active, Resolved, Chronic
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Surgical history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS surgical_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            surgery_name TEXT NOT NULL,
            surgery_year TEXT,
            hospital TEXT,
            organ_changes TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Family history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS family_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            condition TEXT NOT NULL,
            relation TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Vaccinations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            vaccine_name TEXT NOT NULL,
            vaccination_date TEXT,
            dose_number TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Visits table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_id TEXT UNIQUE NOT NULL,
            member_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            institution TEXT,
            department TEXT,
            doctor TEXT,
            visit_type TEXT, -- 门诊, 急诊, 住院, 在线问诊
            chief_complaint TEXT,
            present_illness TEXT,
            primary_diagnosis TEXT,
            secondary_diagnosis TEXT,
            icd_code TEXT,
            treatment TEXT,
            advice TEXT,
            followup_date TEXT,
            followup_institution TEXT,
            total_cost REAL,
            insurance_reimburse REAL,
            out_of_pocket REAL,
            notes TEXT,
            status TEXT DEFAULT 'open', -- open, closed, chronic
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Medications table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_id TEXT UNIQUE NOT NULL,
            visit_id TEXT,
            member_id INTEGER NOT NULL,
            drug_name TEXT NOT NULL,
            generic_name TEXT,
            manufacturer TEXT,
            spec TEXT, -- 规格/剂型
            dosage TEXT,
            route TEXT, -- 口服, 外用, 雾化, etc.
            frequency TEXT,
            duration TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'Current', -- Current, Discontinued
            compliance TEXT, -- 按计划执行, 漏用, 自行调整, 中途停药
            adverse_reaction TEXT,
            adverse_reaction_desc TEXT,
            discontinuation_reason TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (visit_id) REFERENCES visits(visit_id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Medication tracking table (for periodic treatments)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medication_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_id TEXT NOT NULL,
            dose_number INTEGER NOT NULL,
            planned_date TEXT,
            actual_date TEXT,
            status TEXT DEFAULT 'pending', -- pending, completed, missed
            notes TEXT,
            FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
        )
    """)

    # Exams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id TEXT UNIQUE NOT NULL,
            visit_id TEXT,
            member_id INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            exam_date TEXT,
            institution TEXT,
            key_findings TEXT,
            doctor_conclusion TEXT,
            abnormal_flags TEXT, -- JSON array of abnormal values
            attachment_path TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (visit_id) REFERENCES visits(visit_id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # Daily vitals table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            blood_pressure_sys INTEGER,
            blood_pressure_dia INTEGER,
            heart_rate INTEGER,
            temperature REAL,
            blood_glucose REAL,
            weight REAL,
            spo2 REAL,
            respiratory_rate INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (member_id) REFERENCES members(id),
            UNIQUE(member_id, record_date)
        )
    """)

    # Attachments table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            related_id TEXT NOT NULL, -- Visit_ID, Medication_ID, or Exam_ID
            related_type TEXT NOT NULL, -- visit, medication, exam
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT, -- Report, Scan, Photo, Prescription, etc.
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Create indexes for common queries
    cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_member ON visits(member_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_date ON visits(visit_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_medications_member ON medications(member_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_medications_status ON medications(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exams_member ON exams(member_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exams_visit ON exams(visit_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vitals_member_date ON daily_vitals(member_id, record_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_allergies_member ON allergies(member_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_medical_history_member ON medical_history(member_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_medication_tracking_med ON medication_tracking(medication_id)")

    conn.commit()
    conn.close()
    print(f"[OK] Database initialized at: {db_path}")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    init_db(db_path)
