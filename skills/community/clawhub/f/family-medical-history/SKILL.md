---
name: family-medical-history
description: Family Medical Records (家庭医疗档案) | SQLite DB as single source of truth, auto-initializes on first use. EN: (1) set up family health records; (2) log visits, meds, allergies, vaccinations; (3) query medical history; (4) track chronic/periodic treatments; (5) schedule follow-ups. Triggers: "medical record", "health record", "medication history", "visit log", "allergy", "vaccination", "chronic condition", "prescription renewal", "symptom log". ZH: 家庭成员健康档案创建与管理；就诊/用药/过敏/疫苗记录；医疗历史查询；慢性病与周期治疗追踪；随访复诊安排。触发词：医疗记录、健康档案、用药历史、就诊日志、过敏、疫苗接种、慢性病、处方续药、症状记录、家庭医疗。
---

# Family Medical History Skill

A complete family EHR system. **SQLite database is the single source of truth** for all records. Markdown files are optional human-readable exports.

## Database Setup (MANDATORY — First Time Only)

```bash
# Step 1: Initialize the database schema
python3 scripts/init_db.py

# Step 2: Verify
python3 scripts/query_db.py summary
# Expected: Members: 0 (empty database — ready for new records)
```

> **For NEW users**: Start here. The database is empty and ready. You will insert all records directly into the DB.
> **For existing Markdown users**: Run `python3 scripts/import_md.py ./medical_records` to migrate, then continue using the DB.

## Architecture

```
medical_records/
└── medical_records.db    # ← SINGLE SOURCE OF TRUTH (always use this)
    ├── members
    ├── allergies
    ├── medical_history
    ├── surgical_history
    ├── family_history
    ├── vaccinations
    ├── visits
    ├── medications
    ├── medication_tracking
    ├── exams
    ├── daily_vitals
    └── attachments
```

**Markdown layer has been removed.** The database is the only storage. Agents should query/write to SQLite, not to `.md` files.

## Scripts

| Script | When to Use |
|--------|-------------|
| `scripts/init_db.py` | **First time only** — create all tables |
| `scripts/query_db.py` | Any query (CLI or import as module) |
| `scripts/sync_db.py` | Export DB to Markdown (optional, for backup) |

## Database Schema Overview

```sql
-- Core tables
members           -- family member profiles
visits            -- every medical visit
medications       -- every prescription/treatment course
medication_tracking -- per-dose tracking for periodic treatments
exams             -- lab results, imaging reports
daily_vitals      -- BP, HR, temperature, glucose, etc.
allergies          -- allergy records
medical_history   -- past/ongoing conditions
vaccinations      -- vaccination records

-- Cross-reference tables
surgical_history  -- past surgeries
family_history   -- hereditary conditions
attachments      -- file references (scans, photos)
```

## Core Workflows

### Adding a New Family Member

```python
from scripts.query_db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    INSERT INTO members 
    (member_code, name, relationship, dob, gender, blood_type, rh_factor,
     emergency_contact_name, emergency_contact_phone, severe_allergies,
     current_conditions, current_medications)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bob",        # member_code (internal ID)
    "小明",            # name
    "女儿",             # relationship
    "2017-01-01",      # dob
    "女",               # gender
    "B",               # blood_type
    "阳性",            # rh_factor
    "父亲",            # emergency_contact_name
    "138-xxxx-xxxx",   # emergency_contact_phone (脱敏)
    "无",              # severe_allergies
    "无",              # current_conditions
    "无"               # current_medications
))

conn.commit()
conn.close()
```

### Logging a New Visit

```python
from scripts.query_db import get_connection

conn = get_connection()
cur = conn.cursor()

# Get member_id from member_code
member_row = cur.execute(
    "SELECT id FROM members WHERE member_code = ?", ("bob",)
).fetchone()
member_id = member_row[0]

cur.execute("""
    INSERT INTO visits
    (visit_id, member_id, visit_date, institution, department, doctor,
     visit_type, chief_complaint, present_illness, primary_diagnosis,
     secondary_diagnosis, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "V-20260402-01",
    member_id,
    "2026-04-02",
    "儿科医院",
    "儿科",
    "赵大夫",
    "门诊",
    "早起咳嗽持续一个月余",
    "患儿每日晨起咳嗽，有痰，无发热，无鼻塞",
    "待明确（过敏性咳嗽？）",
    "扁桃体炎后遗症？",
    "open"
))

conn.commit()
conn.close()
```

### Logging a Medication

```python
from scripts.query_db import get_connection

conn = get_connection()
cur = conn.cursor()

# Get member_id
member_row = cur.execute(
    "SELECT id FROM members WHERE member_code = ?", ("bob",)
).fetchone()
member_id = member_row[0]

cur.execute("""
    INSERT INTO medications
    (medication_id, visit_id, member_id, drug_name, generic_name,
     spec, dosage, route, frequency, duration, start_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "M-20260402-01",
    "V-20260402-01",   # link to visit
    member_id,
    "头孢克肟混悬剂",
    "Cefixime",
    "50mg/5ml",
    "见处方",
    "口服",
    "每日2次",
    "6天",
    "2026-04-02",
    "Current"
))

conn.commit()
conn.close()
```

### Periodic Treatment Tracking (e.g., Ketoconazole Weekly)

```python
from scripts.query_db import get_connection

conn = get_connection()
cur = conn.cursor()

# First, insert the medication record
cur.execute("""
    INSERT INTO medications
    (medication_id, member_id, drug_name, route, frequency, duration, start_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "M-20260219-01", 2, "康王酮康唑洗剂", "外用", "每周1次", "8次", "2026-02-19", "Current"
))

# Then populate the tracking plan
planned_dates = [
    (1, "2026-02-19"), (2, "2026-02-26"), (3, "2026-03-05"),
    (4, "2026-03-12"), (5, "2026-03-19"), (6, "2026-03-26"),
    (7, "2026-04-02"), (8, "2026-04-09")
]

for dose_num, planned_date in planned_dates:
    cur.execute("""
        INSERT INTO medication_tracking
        (medication_id, dose_number, planned_date, status)
        VALUES (?, ?, ?, ?)
    """, ("M-20260219-01", dose_num, planned_date, "pending"))

conn.commit()
conn.close()
```

### Checking if Periodic Treatment is Due Today

```python
from scripts.query_db import get_next_dose, get_connection
from datetime import date

next_dose = get_next_dose("M-20260219-01")
today = date.today().isoformat()

if next_dose and next_dose['planned_date'] == today:
    print(f"今日({today})应执行第{next_dose['dose_number']}次")
    # Mark as completed after user confirms
elif next_dose and next_dose['planned_date'] < today:
    print(f"计划日期{next_dose['planned_date']}已过期，需补执行第{next_dose['dose_number']}次")
else:
    print("本次周期已完成")
```

### Marking a Dose as Completed

```python
from scripts.query_db import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    UPDATE medication_tracking
    SET actual_date = ?, status = 'completed'
    WHERE medication_id = ? AND dose_number = ?
""", ("2026-04-02", "M-20260219-01", 7))
conn.commit()
conn.close()
```

### Answering Common Questions

**"女儿现在在吃什么药？"**
```python
from scripts.query_db import get_member_current_medications

meds = get_member_current_medications("bob")
for m in meds:
    print(f"{m['drug_name']} | {m['dosage']} | {m['frequency']} | Started: {m['start_date']}")
```

**"luna的酮康唑今天要用吗？"**
```python
from scripts.query_db import get_next_dose
from datetime import date

next_dose = get_next_dose("M-20260219-01")
if next_dose and next_dose['planned_date'] == date.today().isoformat():
    print("是，今天应使用第7次")
elif next_dose and next_dose['planned_date'] < date.today().isoformat():
    print(f"计划已过期（第{next_dose['dose_number']}次，{next_dose['planned_date']}）")
```

**"最近谁去过医院？"**
```python
from scripts.query_db import get_recent_visits

for member in ["bob", "luna"]:
    visits = get_recent_visits(member, days=30)
    for v in visits:
        print(f"{member} | {v['visit_date']} | {v['chief_complaint']}")
```

## Templates Reference

- Full SQL schema and table definitions: See `references/schema.md`
- Markdown export templates (optional): See `references/templates.md`

## Data Entry Rules

1. **Never fabricate**: unknown = "待确认" / "待填写"
2. **Always link**: every visit, medication, exam references its parent
3. **Use `status`**: visits=`open/closed/chronic`; medications=`Current/Discontinued`; tracking=`pending/completed/missed`
4. **Periodic tracking**: always use `medication_tracking` table for scheduled treatments
5. **Dual-write not needed**: DB is the only source; Markdown sync is export-only
