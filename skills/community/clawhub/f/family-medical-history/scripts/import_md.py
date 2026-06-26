#!/usr/bin/env python3
"""
Import existing Markdown medical records into SQLite database.
Scans the medical_records/ directory and imports all members and records.
"""

import sqlite3
import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "medical_records.db")

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "medical_records.db"))

def parse_profile(content: str) -> dict:
    """Parse a profile.md file and extract fields."""
    import re
    data = {}
    lines = content.split("\n")
    current_section = None
    
    # Extract key-value pairs with **key**：value or - key：value format
    for line in lines:
        line = line.strip()
        if line.startswith("## ") or line.startswith("# "):
            current_section = line.strip("# ").strip()
            continue
        # Match **key**：value or **key**： value
        m = re.search(r"\*\*([^：*]+)\*\*[：:]\s*(.+)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            data[key] = val
        elif ": " in line and current_section in ["基础信息", "证件与医保", "生活习惯", "🚨 紧急医疗摘要"]:
            key, val = line.split(": ", 1)
            data[key.strip("- 「」")] = val.strip()
    
    return data

def parse_visits(content: str) -> dict:
    """Parse a visit record file."""
    data = {}
    for line in content.split("\n"):
        line = line.strip()
        # Match patterns like: - **key**：value 或 - **key**：value
        # or: **key**：value
        import re
        # Pattern: **key**：（中文冒号）value
        m = re.search(r"\*\*([^：*]+)\*\*[：:](.+)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            data[key] = val
        elif ": " in line and not line.startswith("|"):
            key, val = line.split(": ", 1)
            data[key.strip("-*「」 ")] = val.strip()
    return data

def import_all(records_dir: str, db_path: str = None) -> None:
    if db_path is None:
        db_path = get_db_path()
    
    if not os.path.exists(records_dir):
        print(f"[ERROR] Records directory not found: {records_dir}")
        return
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    imported_members = 0
    imported_visits = 0
    imported_medications = 0
    imported_exams = 0
    
    for member_code in os.listdir(records_dir):
        member_dir = os.path.join(records_dir, member_code)
        if not os.path.isdir(member_dir) or member_code == "templates":
            continue
        
        profile_path = os.path.join(member_dir, "profile.md")
        if not os.path.exists(profile_path):
            continue
        
        with open(profile_path, "r", encoding="utf-8") as f:
            profile_content = f.read()
        
        # Parse basic member info
        member_data = parse_profile(profile_content)
        
        cur.execute("""
            INSERT OR REPLACE INTO members 
            (member_code, name, relationship, dob, gender, blood_type, rh_factor,
             emergency_contact_name, emergency_contact_phone, severe_allergies,
             current_conditions, current_medications, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member_code,
            member_data.get("姓名"),
            member_data.get("关系"),
            member_data.get("出生日期 (DOB)"),
            member_data.get("性别"),
            member_data.get("血型"),
            member_data.get("RH阴性"),
            member_data.get("紧急联系人", "").split("/")[0].strip() if "紧急联系人" in member_data else None,
            member_data.get("紧急联系人", "").split("/")[-1].strip() if "紧急联系人" in member_data else None,
            member_data.get("严重过敏"),
            member_data.get("当前重大疾病/植入物"),
            member_data.get("当前长期用药"),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        member_row = cur.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
        if not member_row:
            continue
        member_id = member_row[0]
        imported_members += 1
        
        # Import visits
        visits_dir = os.path.join(member_dir, "visits")
        if os.path.exists(visits_dir):
            for fname in os.listdir(visits_dir):
                if not fname.endswith(".md"):
                    continue
                with open(os.path.join(visits_dir, fname), "r", encoding="utf-8") as f:
                    visit_content = f.read()
                
                visit_data = parse_visits(visit_content)
                visit_id = fname.replace(".md", "")
                
                cur.execute("""
                    INSERT OR REPLACE INTO visits
                    (visit_id, member_id, visit_date, institution, department, doctor, visit_type,
                     chief_complaint, present_illness, primary_diagnosis, secondary_diagnosis,
                     status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    visit_id, member_id,
                    visit_data.get("就诊日期"),
                    visit_data.get("就诊机构"),
                    visit_data.get("就诊科室"),
                    visit_data.get("就诊医生"),
                    visit_data.get("就诊类型"),
                    visit_data.get("主诉"),
                    visit_data.get("现病史"),
                    visit_data.get("主诊断"),
                    visit_data.get("次诊断"),
                    "open",
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                imported_visits += 1
        
        # Import medications
        meds_dir = os.path.join(member_dir, "medications")
        if os.path.exists(meds_dir):
            for fname in os.listdir(meds_dir):
                if not fname.endswith(".md"):
                    continue
                with open(os.path.join(meds_dir, fname), "r", encoding="utf-8") as f:
                    med_content = f.read()
                
                med_data = parse_visits(med_content)
                med_id = fname.replace(".md", "")
                
                # Extract drug name from file or content
                drug_name = med_data.get("药品名称", med_id)
                visit_id_link = med_data.get("关联就诊ID")
                
                cur.execute("""
                    INSERT OR REPLACE INTO medications
                    (medication_id, visit_id, member_id, drug_name, generic_name, manufacturer,
                     spec, dosage, route, frequency, duration, start_date, end_date, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    med_id, visit_id_link, member_id,
                    drug_name,
                    med_data.get("通用名"),
                    med_data.get("生产厂家"),
                    med_data.get("规格/剂型"),
                    med_data.get("剂量"),
                    med_data.get("用法", "").replace("☐", "").strip(),
                    med_data.get("频次", "").replace("☐", "").strip(),
                    med_data.get("疗程"),
                    med_data.get("开始日期"),
                    med_data.get("结束日期"),
                    "Current" if "治疗中" in med_content else "Discontinued",
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                imported_medications += 1
        
        # Import exams
        exams_dir = os.path.join(member_dir, "exams")
        if os.path.exists(exams_dir):
            for fname in os.listdir(exams_dir):
                if not fname.endswith(".md"):
                    continue
                with open(os.path.join(exams_dir, fname), "r", encoding="utf-8") as f:
                    exam_content = f.read()
                
                exam_data = parse_visits(exam_content)
                exam_id = fname.replace(".md", "")
                visit_id_link = exam_data.get("关联就诊ID")
                
                cur.execute("""
                    INSERT OR REPLACE INTO exams
                    (exam_id, visit_id, member_id, exam_name, exam_date, institution,
                     doctor_conclusion, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    exam_id, visit_id_link, member_id,
                    exam_data.get("检查项目"),
                    exam_data.get("检查日期"),
                    exam_data.get("检查机构"),
                    exam_data.get("医生结论"),
                    datetime.now().isoformat()
                ))
                imported_exams += 1
    
    conn.commit()
    conn.close()
    
    print(f"[OK] Import complete:")
    print(f"  - Members: {imported_members}")
    print(f"  - Visits: {imported_visits}")
    print(f"  - Medications: {imported_medications}")
    print(f"  - Exams: {imported_exams}")

if __name__ == "__main__":
    records_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "medical_records")
    db_path = sys.argv[2] if len(sys.argv) > 2 else None
    import_all(records_dir, db_path)
