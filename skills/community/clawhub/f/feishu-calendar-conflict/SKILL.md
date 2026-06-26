---
name: feishu-calendar-conflict
description: |
  Feishu Calendar Conflict Detector - Detect scheduling conflicts before booking meetings.
  
  **Features**:
  - Check if attendees are available before creating meeting
  - Query multiple users' free/busy status
  - Suggest available time slots
  - Visualize calendar conflicts
  
  **Trigger**:
  - User mentions "check conflict", "时间冲突", "冲突检测", "有没有空"
  - User wants to book a meeting and check availability
---

# Feishu Calendar Conflict Detector

## ⚠️ Pre-requisites

- ✅ **Time format**: ISO 8601 / RFC 3339 (with timezone), e.g. `2026-03-31T14:00:00+08:00`
- ✅ **Batch query**: Can check up to 10 users at once
- ✅ **user_open_id needed**: Get from message context SenderId

---

## 📋 Quick Reference

| Intent | Tool | action | Required Params |
|--------|------|--------|-----------------|
| Check free/busy | feishu_calendar_freebusy | list | time_min, time_max, user_ids |
| Create meeting | feishu_calendar_event | create | summary, start_time, end_time |
| Query user ID | feishu_search_user | - | query |

---

## 🛠️ Usage

### 1. Check Single User Availability

```json
{
  "action": "list",
  "time_min": "2026-03-31T09:00:00+08:00",
  "time_max": "2026-03-31T18:00:00+08:00",
  "user_ids": ["ou_xxx"]
}
```

**Response format**:
```json
{
  "busy_slots": [
    {"start": "2026-03-31T10:00:00+08:00", "end": "2026-03-31T11:00:00+08:00"},
    {"start": "2026-03-31T14:00:00+08:00", "end": "2026-03-31T15:30:00+08:00"}
  ],
  "free_slots": [
    {"start": "2026-03-31T09:00:00+08:00", "end": "2026-03-31T10:00:00+08:00"},
    {"start": "2026-03-31T11:00:00+08:00", "end": "2026-03-31T14:00:00+08:00"},
    {"start": "2026-03-31T15:30:00+08:00", "end": "2026-03-31T18:00:00+08:00"}
  ]
}
```

### 2. Check Multiple Users Availability

```json
{
  "action": "list",
  "time_min": "2026-03-31T09:00:00+08:00",
  "time_max": "2026-03-31T18:00:00+08:00",
  "user_ids": ["ou_xxx", "ou_yyy", "ou_zzz"]
}
```

**Result**: Returns common free time slots when ALL users are free.

### 3. Find Available Meeting Slots

Algorithm:
1. Get busy slots for all attendees
2. Find gaps between busy slots
3. Filter by minimum meeting duration
4. Return available windows

**Example**: 2-hour meeting, 3 attendees
```json
{
  "action": "list",
  "time_min": "2026-03-31T09:00:00+08:00",
  "time_max": "2026-03-31T18:00:00+08:00",
  "user_ids": ["ou_xxx", "ou_yyy", "ou_zzz"]
}
```

**Suggested slots** (if busy 10-11, 14-15:30):
- 09:00-10:00 ✓
- 11:00-14:00 ✓
- 15:30-18:00 ✓

### 4. Conflict Warning

Before creating a meeting, warn user if conflicts exist:

```json
{
  "action": "list",
  "time_min": "2026-03-31T10:00:00+08:00",
  "time_max": "2026-03-31T11:00:00+08:00",
  "user_ids": ["ou_xxx", "ou_yyy"]
}
```

If response shows busy slots in this time range → **Conflict detected!**

---

## 💰 Pricing

| Version | Price | Features |
|---------|-------|----------|
| Free | ¥0 | Check 1-2 users |
| Pro | ¥12/month | Check up to 10 users, auto-suggest slots |
| Team | ¥35/month | Historical analysis, recurring meeting conflicts |

---

## 📝 Example

**User says**: "看一下明天上午10点张三和李四有没有空"

**Execute**:
1. Search for 张三 and 李四 to get open_ids
2. Query free/busy for tomorrow morning 09:00-12:00
3. Check if 10:00-11:00 is in free slot
4. Report availability

**Response**: "张三和李四在明天上午10点都OK，没有冲突 ✓"

---

## 🔧 Tips

- Query 30 minutes before/after desired time for buffer
- Consider user's working hours (default: 09:00-18:00)
- For international teams, account for timezone differences
- Use "tentative" status as "may be busy" warning
