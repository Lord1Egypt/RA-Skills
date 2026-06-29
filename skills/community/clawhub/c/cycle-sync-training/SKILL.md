---
name: cycle-sync-training
description: >
  OpenClaw skill สำหรับวางแผนออกกำลังกายตามรอบประจำเดือน 4 เฟส (Cycle Syncing) โดยอิงจากงานวิจัยล่าสุด เพื่อเพิ่มประสิทธิภาพการเทรน ลดความเสี่ยงบาดเจ็บ และให้คำแนะนำที่แม่นยำและเป็นส่วนตัวสำหรับผู้หญิง
  ใช้เมื่อ user พูดถึง: รอบเดือน, cycle syncing, ฮอร์โมน, เฟสออกกำลังกาย,
  วางแผน workout ผู้หญิง, ประจำเดือน, follicular, luteal, ovulatory, menstrual,
  ออกกำลังกายตามรอบ, hormone training, วันไหนควรเทรนหนัก,
  หรือ gym fitness สำหรับผู้หญิงที่ต้องการ personalized plan.
  Trigger นี้เมื่อ user ถามเรื่องแผนออกกำลังกายผู้หญิงแม้จะไม่ได้พูดถึง cycle โดยตรง.
---

# Cycle Sync Training Skill

ช่วย AI agent วางแผนออกกำลังกายสำหรับผู้หญิงตามรอบประจำเดือน 4 เฟส
ผ่าน FastMCP 2.x server บน OpenClaw platform

---

## วิธีใช้ Skill นี้

### เมื่อ user ต้องการ:
- บันทึกเฟสรอบเดือนและอาการ → เรียก `log_cycle_phase`
- ขอโปรแกรมออกกำลังกาย → เรียก `get_phase_workout`
- ปรับความเข้มข้นการเทรน → เรียก `adjust_intensity`
- หาวันที่พลังงานสูงสุด → เรียก `predict_energy_window`

---

## 4 เฟสและหลักการ

อ่านรายละเอียดเพิ่มเติม: `references/phase_guide.md`

| เฟส | วันที่ (เฉลี่ย) | ฮอร์โมนหลัก | การเทรนที่เหมาะ |
|-----|--------------|------------|----------------|
| Menstrual | 1–5 | ต่ำทุกตัว | เบา / yoga / เดิน |
| Follicular | 6–13 | Estrogen ↑ | Moderate → Heavy |
| Ovulatory | 14–17 | Peak Estrogen + LH | Max intensity / PR |
| Luteal | 18–28 | Progesterone ↑ | Moderate / ลด volume |

---

## Tools API

### 1. `log_cycle_phase`
บันทึกเฟสปัจจุบันและอาการประจำวัน

**Input:**
```json
{
  "user_id": "string",
  "phase": "menstrual | follicular | ovulatory | luteal",
  "cycle_day": 1,
  "symptoms": ["cramps", "bloating", "fatigue", "energetic"],
  "mood_score": 7,
  "energy_score": 6,
  "date": "2027-01-15"
}
```

**Output:**
```json
{
  "status": "logged",
  "phase": "follicular",
  "cycle_day": 8,
  "next_phase_in_days": 5,
  "recommendation": "ช่วงนี้เหมาะสำหรับเพิ่ม intensity ได้แล้ว"
}
```

---

### 2. `get_phase_workout`
แนะนำโปรแกรมออกกำลังกายตามเฟส

**Input:**
```json
{
  "user_id": "string",
  "phase": "follicular",
  "available_equipment": ["barbell", "dumbbell", "cable"],
  "session_duration_minutes": 60,
  "focus_area": "full_body | upper | lower | cardio"
}
```

**Output:**
```json
{
  "phase": "follicular",
  "intensity_level": "moderate-high",
  "workout": {
    "warmup": [...],
    "main_sets": [...],
    "cooldown": [...]
  },
  "phase_tips": "Estrogen เพิ่มขึ้น กล้ามเนื้อฟื้นตัวเร็ว เพิ่ม load ได้ 5-10%",
  "avoid": ["heavy singles ใน menstrual phase", "HIIT ตอน PMS peak"]
}
```

---

### 3. `adjust_intensity`
ปรับความเข้มข้นการเทรนตาม hormonal data และ symptoms

**Input:**
```json
{
  "user_id": "string",
  "planned_intensity": "heavy",
  "current_energy_score": 4,
  "current_symptoms": ["cramps", "fatigue"],
  "cycle_day": 2
}
```

**Output:**
```json
{
  "original_intensity": "heavy",
  "adjusted_intensity": "light",
  "adjustment_reason": "วันที่ 2 ของรอบ + อาการปวด → ลด intensity เพื่อฟื้นตัว",
  "alternative_workout": "Yin yoga 30 นาที + เดิน 20 นาที",
  "reschedule_heavy_to": "cycle_day_9"
}
```

---

### 4. `predict_energy_window`
คาดการณ์ช่วงที่พลังงานสูงสุดสำหรับ PR goals

**Input:**
```json
{
  "user_id": "string",
  "cycle_start_date": "2027-01-01",
  "cycle_length": 28,
  "goal": "1RM_test | HIIT_competition | race_day | photo_shoot"
}
```

**Output:**
```json
{
  "peak_window": {
    "start": "2027-01-14",
    "end": "2027-01-17",
    "phase": "ovulatory"
  },
  "secondary_window": {
    "start": "2027-01-09",
    "end": "2027-01-13",
    "phase": "late_follicular"
  },
  "avoid_window": {
    "start": "2027-01-25",
    "end": "2027-01-28",
    "reason": "PMS + progesterone peak → coordination และ strength ลดลง"
  },
  "goal_day_recommendation": "2027-01-15"
}
```

---

## Integration กับ OpenClaw

### Agent Orchestration Flow
```
User Input
    ↓
OpenClaw Orchestrator (Core-01)
    ↓
cycle-sync-training MCP Server (port 8420)
    ↓
Supabase (user data + cycle history)
    ↓
Response → LINE Notify / Facebook
```

### Environment Variables
```bash
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-anon-key>
MCP_PORT=8420
```

### OpenClaw Config
```json
{
  "skill": "cycle-sync-training",
  "mcp_endpoint": "http://localhost:8420/mcp",
  "agents": ["Core-01", "Admin-01"],
  "trigger_keywords": ["รอบเดือน", "cycle", "เฟส", "ฮอร์โมน", "ออกกำลังกายผู้หญิง"]
}
```

---

## การติดตั้ง

```bash
# 1. Install dependencies
pip install fastmcp supabase python-dateutil

# 2. Set environment variables
cp .env.example .env && nano .env

# 3. Run server
python server.py

# 4. Test
python -m pytest tests/ -v
```

---

## อ้างอิง
- `references/phase_guide.md` — รายละเอียดวิทยาศาสตร์ฮอร์โมนแต่ละเฟส + workout prescriptions (อัปเดต 2026)
- `references/research_findings_2026.md` — สรุปผลการวิจัยล่าสุด (2024-2026) เกี่ยวกับ Cycle Syncing และการออกกำลังกาย
- `tests/test_cases.json` — Test scenarios ครอบคลุมทุก tool
