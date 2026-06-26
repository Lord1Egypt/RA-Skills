---
name: bilimclass
description: "Access BilimClass school platform (Kazakhstan) for schedule, homework, grades, and diary via API. Triggers on schedule/raspisanie/расписание, homework/domashka/домашка/домашнее задание, grades/ocenki/оценки, diary/dnevnik/дневник, какие уроки завтра/сегодня, четвертные оценки, годовые оценки, and any school-related queries for Kazakhstan students. NOT for general education or non-BilimClass platforms."
metadata:
  "openclaw":
    emoji: "📚"
    requires:
      file: "~/.openclaw/.env.json"
---

# BilimClass — School Schedule, Homework & Grades

Access BilimClass API for Kazakhstan school data. Supports schedule, homework, and **quarterly/yearly grades**.

## Setup

Two tokens required in `~/.openclaw/.env.json`:
- **`bilimclass.token`** — main JWT from `localStorage.token` (RS256, valid ~1 year). Used for schedule and subject names.
- **`bilimclass.journalToken`** — journal JWT from API headers on grades page (HS512, expires ~2 weeks). Used for grades only.

Both expire — `token` annually, `journalToken` biweekly. To refresh `journalToken`:
1. Open bilimclass.kz → grades section
2. F12 → Network → find request to `journal-service.bilimclass.kz/diary`
3. Copy the `Authorization: Bearer ...` header value

To refresh main `token`: browser console → `localStorage.token`

### Required config fields in `.env.json`:
```json
{
  "bilimclass": {
    "token": "<YOUR_TOKEN>",
    "journalToken": "<YOUR_JOURNAL_TOKEN>",
    "schoolId": "<YOUR_SCHOOL_ID>",
    "eduYear": "<EDUCATION_YEAR>",
    "userId": "<YOUR_USER_ID>",
    "studentSchoolUuid": "<YOUR_STUDENT_UUID>",
    "studentGroups": [
      {"uuid": "<UUID>", "name": "Group name"},
      {"uuid": "<UUID>", "name": "Group name"}
    ]
  }
}
```

> `studentGroups` — all student groups for the user. The first one should be the current group for grades.

## Quick Usage

```bash
python3 <skill_dir>/scripts/bilimclass.py schedule [DD.MM.YYYY]
python3 <skill_dir>/scripts/bilimclass.py diary [YYYY-MM-DD]
python3 <skill_dir>/scripts/bilimclass.py week [DD.MM.YYYY]      # Monday of that week
python3 <skill_dir>/scripts/bilimclass.py grades <YYYY-MM-DD> <YYYY-MM-DD>
python3 <skill_dir>/scripts/bilimclass.py quarter-report [Q3|Q4]
python3 <skill_dir>/scripts/bilimclass.py today
python3 <skill_dir>/scripts/bilimclass.py tomorrow
```

All output is JSON — format it nicely for the user.

## Schedule Format

Each day contains:
- `date_label` — display date (e.g. "06 АПРЕЛЯ")
- `schedule[]` — lessons with:
  - `subject.label` — subject name
  - `subject.subjectId` — integer ID (used for grade mapping)
  - `teacher` — teacher full name
  - `homework.body` — homework text
  - `time.label` — time range (e.g. "08:00 - 08:40")

## Diaries (Homework Detail)

Multiple student groups. The script iterates all `studentGroups` — it handles dedup automatically.

## Grades

Grades use a **separate service** (`journal-service.bilimclass.kz`) with the `journalToken`.

### API Endpoints
- **Schedule + subject names:** `https://api.bilimclass.kz/api/v4/os/clientoffice/schedule`
  - Auth: `Bearer {token}` (main JWT)
  - Headers: `X-School-Id`, `X-Localization: ru`
- **Grades:** `https://journal-service.bilimclass.kz/diary`
  - Auth: `Bearer {journalToken}` (journal JWT)
  - Headers: `X-School-Id`, `X-Localization: ru`, `external: 1`

### How grades work
1. Query `/diary` with `schoolId`, `eduYear`, `userId`, `studentGroupUuid`, `date` (ISO 8601)
2. Response is `{"data": {<scheduleUuid>: {formattedScore, sor, soch, ...}}}`
3. Each of `formattedScore`/`sor`/`soch` contains:
   - `mark` — the score (integer)
   - `markMax` — maximum (usually 10, sometimes 24 for СОЧ)
   - `subjectId` — **integer** ID for mapping to subject names
   - `date`, `markType`, `comment`
4. `scheduleUuid` (the key) is a UUID, not the same as `subjectId`
5. Subject names come from the schedule API — map via `subjectId` from lesson data

### Grading scale (4th quarter rules)
- **5**: ≥ 87%
- **4**: ≥ 65%
- **3**: ≥ 50%
- **2**: < 50%

### Quarter date ranges (approximate for 2025-2026)
- **Q3:** January 8 — March 22
- **Q4:** March 31 — current date

### Notes
- Some subjects may have no grades in a quarter if no assessments have been given yet
- Absent-due-to-illness marks use `markType: "sick"` — exclude from percentage calculations
- Always use the **first** `studentGroup` (index 0) for current grades
- journalToken expires ~every 2 weeks — check `401` responses and prompt user to refresh
- When reporting grades, sort alphabetically by subject name
- Always show: subject name, %, predicted grade, number of assessments

## Notes

- Both APIs use `Bearer <token>` style auth but with **different tokens**
- Schedule API uses main token; Grades API uses journalToken
- `SUBJECT_NAMES` dict is populated dynamically from schedule API — if subject name missing, show `Предмет #{id}` and note the gap
