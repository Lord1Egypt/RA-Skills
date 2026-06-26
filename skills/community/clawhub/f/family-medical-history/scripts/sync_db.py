#!/usr/bin/env python3
"""
Sync script: writes Markdown records from SQLite DB.
Run this after direct DB modifications to keep .md files in sync.
Or run periodically to regenerate .md files from DB.
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "medical_records.db")
RECORDS_DIR = os.path.join(os.path.dirname(__file__), "..", "medical_records")

def get_connection(db_path: str = None):
    if db_path is None:
        db_path = DB_PATH
    return sqlite3.connect(db_path)

def ensure_dirs(member_code: str) -> dict:
    """Ensure all subdirectories exist for a member, return base path."""
    base = os.path.join(RECORDS_DIR, member_code)
    for subdir in ["visits", "medications", "exams", "daily_vitals", "attachments"]:
        os.makedirs(os.path.join(base, subdir), exist_ok=True)
    os.makedirs(os.path.join(base, "attachments", "2026"), exist_ok=True)
    os.makedirs(os.path.join(base, "attachments", "2027"), exist_ok=True)
    return base

def sync_members(db_path: str = None) -> None:
    """Sync all members from DB to Markdown profiles."""
    conn = get_connection(db_path)
    members = conn.execute("SELECT * FROM members").fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM members WHERE 1=0").description]
    conn.close()
    
    os.makedirs(RECORDS_DIR, exist_ok=True)
    
    for row in members:
        r = dict(zip(cols, row))
        base = ensure_dirs(r["member_code"])
        profile_path = os.path.join(base, "profile.md")
        
        profile = f"""# {r['member_code']} - 个人核心健康主页

## 🚨 紧急医疗摘要
- 紧急联系人：{r.get('emergency_contact_name', '待填写')} / {r.get('emergency_contact_phone', '电话待填写')}
- 血型：{r.get('blood_type', '待确认')} / RH{r.get('rh_factor', '待确认')}
- 严重过敏：{r.get('severe_allergies', '待记录')}
- 当前重大疾病/植入物：{r.get('current_conditions', '待记录')}
- 当前长期用药：{r.get('current_medications', '待记录')}

---

## 基础信息
- 姓名/代号：{r.get('name', '待填写')}
- 关系：{r.get('relationship', '待填写')}
- 出生日期 (DOB)：{r.get('dob', '待填写')}
- 性别：{r.get('gender', '待填写')}

## 证件与医保
- 身份证号：{r.get('id_number', '待填写')}
- 医保卡号：{r.get('insurance_number', '待填写')}
- 主要就诊医院档案号：{r.get('hospital档案号', '待填写')}

## 生活习惯
- 吸烟史：{r.get('smoking_history', '待记录')}
- 饮酒史：{r.get('drinking_history', '待记录')}
- 饮食偏好：{r.get('diet_preference', '待观察')}
- 高风险职业暴露史：{r.get('occupation_risk', '无')}

## 过敏史（详细）
（见 allergies 表）

## 内科病史
（见 medical_history 表）

## 外科/手术史
（见 surgical_history 表）

## 家族病史
（见 family_history 表）

## 疫苗接种
（见 vaccinations 表）

---

## 就诊记录索引
（从数据库同步）

## 用药记录索引
（从数据库同步）

---

*档案最后同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(profile)
    
    print(f"[OK] Synced {len(members)} member profiles to Markdown")

def sync_visits(member_code: str, db_path: str = None) -> None:
    """Sync visits for a specific member."""
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        print(f"[WARN] Member not found: {member_code}")
        conn.close()
        return
    
    visits = conn.execute("SELECT * FROM visits WHERE member_id = ? ORDER BY visit_date", (member_row[0],)).fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM visits WHERE 1=0").description]
    conn.close()
    
    base = ensure_dirs(member_code)
    visits_dir = os.path.join(base, "visits")
    
    for row in visits:
        v = dict(zip(cols, row))
        visit_path = os.path.join(visits_dir, f"{v['visit_id']}.md")
        content = f"""# {v['visit_id']} 就诊记录

## 基本信息
- **就诊日期**：{v['visit_date']}
- **就诊机构**：{v.get('institution', '待确认')}
- **就诊科室**：{v.get('department', '待确认')}
- **就诊医生**：{v.get('doctor', '待确认')}
- **就诊类型**：{v.get('visit_type', '门诊')}

## 主诉
{v.get('chief_complaint', '待记录')}

## 现病史
{v.get('present_illness', '待记录')}

## 诊断
| 诊断类型 | 诊断名称 |
|----------|----------|
| 主诊断 | {v.get('primary_diagnosis', '待明确')} |
| 次诊断 | {v.get('secondary_diagnosis', '待明确')} |

## 医嘱
{v.get('advice', '待记录')}

## 随访安排
- 复诊日期：{v.get('followup_date', '待确认')}

---

*最后同步：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        with open(visit_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print(f"[OK] Synced {len(visits)} visits for {member_code}")

def sync_medications(member_code: str, db_path: str = None) -> None:
    """Sync medications for a specific member."""
    conn = get_connection(db_path)
    member_row = conn.execute("SELECT id FROM members WHERE member_code = ?", (member_code,)).fetchone()
    if not member_row:
        conn.close()
        return
    
    meds = conn.execute("SELECT * FROM medications WHERE member_id = ? ORDER BY start_date", (member_row[0],)).fetchall()
    cols = [desc[0] for desc in conn.execute("SELECT * FROM medications WHERE 1=0").description]
    
    # Also get tracking data
    tracking = {}
    for med_id in conn.execute("SELECT DISTINCT medication_id FROM medications WHERE member_id = ?", (member_row[0],)):
        tracking_rows = conn.execute("SELECT * FROM medication_tracking WHERE medication_id = ? ORDER BY dose_number", (med_id[0],)).fetchall()
        tracking[med_id[0]] = tracking_rows
    
    conn.close()
    
    base = ensure_dirs(member_code)
    meds_dir = os.path.join(base, "medications")
    
    for row in meds:
        m = dict(zip(cols, row))
        med_path = os.path.join(meds_dir, f"{m['medication_id']}.md")
        
        # Build tracking table
        tracking_rows = tracking.get(m['medication_id'], [])
        tracking_md = "| 次数 | 计划日期 | 实际日期 | 状态 | 备注 |\n|------|----------|----------|------|------|\n"
        for tr in tracking_rows:
            tracking_md += f"| 第{tr[2]}次 | {tr[3]} | {tr[4] or ''} | {'✅' if tr[5]=='completed' else '⏳' if tr[5]=='pending' else '❌'} | {tr[6] or ''} |\n"
        
        content = f"""# 用药记录

- **用药记录ID**: {m['medication_id']}
- **关联就诊ID**: {m.get('visit_id', '待关联')}

---

## 药品信息
- **药品名称**: {m.get('drug_name', '待填写')}
- **通用名**: {m.get('generic_name', '待填写')}
- **规格/剂型**: {m.get('spec', '待填写')}
- **生产厂家**: {m.get('manufacturer', '待填写')}

## 用药方案
- **剂量**: {m.get('dosage', '待填写')}
- **用法**: {m.get('route', '待填写')}
- **频次**: {m.get('frequency', '待填写')}
- **疗程**: {m.get('duration', '待填写')}
- **开始日期**: {m.get('start_date', '待填写')}
- **结束日期**: {m.get('end_date', '待填写')} {'或 持续治疗中' if m.get('end_date') is None else ''}

---

## 用药记录（追踪表）
{tracking_md}

## 状态
- **Status**: {'☑ Current 治疗中' if m.get('status') == 'Current' else '☐ Discontinued 已停药'}

---

## 依从性记录
- **实际服用情况**: {m.get('compliance', '待记录')}
- **不良反应**: {'☐无 ☐有 → ' + m.get('adverse_reaction_desc', '') if m.get('adverse_reaction') == '有' else '☐无'}
- **停药原因**: {m.get('discontinuation_reason', '无')}

---

*最后同步：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        with open(med_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print(f"[OK] Synced {len(meds)} medications for {member_code}")

def sync_all(db_path: str = None) -> None:
    """Full sync: DB → Markdown for all members."""
    sync_members(db_path)
    conn = get_connection(db_path)
    members = conn.execute("SELECT member_code FROM members").fetchall()
    conn.close()
    for (mc,) in members:
        sync_visits(mc, db_path)
        sync_medications(mc, db_path)
    print("[OK] Full sync complete")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not os.path.exists(db_path or DB_PATH):
        print(f"[ERROR] Database not found")
        sys.exit(1)
    sync_all(db_path)
