---
name: family-partner
description: |
  Family Partner - AI-Powered Family Assistant Skills Suite
  A comprehensive collection of 11 family management skills including calendar, tasks, memory, labor tracking, milestones, anniversaries, voting, challenges, and more.
version: 1.0.0
author: AI-PlusPlus
license: MIT
emoji: 🏠
metadata:
  openclaw:
    requires:
      bins:
        - sqlite3
    primaryEnv: ""
---

# Family Partner Skills Suite

## Overview

Family Partner is a complete family management solution powered by AI. It includes 11 integrated skills that work together to help families organize their daily lives, track important information, and create lasting memories.

## Included Skills

### 1. Family Calendar (📅)
**Purpose:** Create, view, and manage family schedules and events.

**Key Features:**
- View today/tomorrow/this week's schedule
- Create new events with participants and location
- Delete or modify existing events
- Query events by participant

**When to use:**
- User asks about today's/tomorrow's schedule
- User wants to create or delete an event
- User wants to check someone's schedule

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "SELECT time(start_time), title, participants, location \
   FROM events \
   WHERE date(start_time) = date('now') \
   ORDER BY start_time"
```

---

### 2. Family Tasks (✅)
**Purpose:** Manage to-do lists and shopping lists for the family.

**Key Features:**
- Add, view, complete, and delete tasks
- Assign tasks to family members
- Support for todo and shopping list types
- Batch add shopping items

**When to use:**
- User wants to add a to-do item
- User wants to view task list
- User wants to complete/delete a task
- User wants to assign a task to someone

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO tasks (id, title, type, assignee) \
   VALUES ('t20260302150000', 'Doctor appointment', 'todo', 'Mom')"
```

---

### 3. Family Memory (💭)
**Purpose:** Record and query family member preferences, allergies, and important information.

**Key Features:**
- Store preferences, dislikes, allergies
- Record important information (medical, school, work)
- Track habits and goals
- Quick lookup by member or type

**When to use:**
- User wants to record family member preferences/allergies
- User asks about someone's preferences
- User says "remember..."

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO memories (id, member_name, type, content) \
   VALUES ('m20260302150000', 'Ethan', 'allergy', 'Allergic to peanuts')"
```

---

### 4. Family Labor (📊)
**Purpose:** Track invisible household labor and analyze fairness.

**Key Features:**
- Record household chores with duration
- View daily/weekly/monthly statistics
- Analyze labor distribution fairness
- Track various chore types (cooking, cleaning, childcare, etc.)

**When to use:**
- User wants to record housework
- User wants to view labor statistics
- User wants to analyze fairness

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO labor (id, member_name, type, duration, date) \
   VALUES ('l20260302150000', 'Mom', 'cooking', 60, date('now'))"
```

---

### 5. Family Time (⏰)
**Purpose:** Record and review family quality time activities.

**Key Features:**
- Log family activities (dinner, movies, outings)
- View activity history
- Statistics on quality time spent
- Annual review of family activities

**When to use:**
- User wants to record a family activity
- User wants to review family time
- User wants statistics on family bonding time

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO family_time (id, activity, participants, duration, date) \
   VALUES ('f20260302150000', 'Watch movie', 'Dad,Mom,Ethan', 120, date('now'))"
```

---

### 6. Family Morning (🌅)
**Purpose:** Daily morning briefing with all important family information.

**Key Features:**
- Today's schedule overview
- Pending tasks summary
- Shopping list
- Upcoming anniversaries reminder
- Weather tips (if API integrated)

**When to use:**
- User requests "morning briefing" or "good morning"
- Scheduled trigger (e.g., 8 AM daily)
- User wants quick overview of today's plan

**Example Output:**
```
☀️ Good morning! Today is March 2, 2026, Monday

📅 Today's Schedule:
09:00 - Take Ethan to school (Dad)
14:00 - Parent meeting (Mom)
19:00 - Family dinner

📋 To-do Items:
□ Doctor appointment (Mom)
□ Clean garage (Dad)

🛒 Shopping List:
□ Milk
□ Eggs

🎂 Upcoming Anniversaries:
March 5 - Ethan's Birthday 🎉

Have a wonderful day! 🌟
```

---

### 7. Family Anniversary (🎉)
**Purpose:** Manage important family anniversaries and birthdays.

**Key Features:**
- Record birthdays, wedding anniversaries, special dates
- View upcoming anniversaries (next 7 days)
- Calculate age from birth year
- Support multiple anniversary types

**When to use:**
- User wants to record an anniversary
- User asks about upcoming birthdays
- Need reminder for important dates

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO anniversaries (id, member_name, title, date, year, type) \
   VALUES ('a20260302150000', 'Ethan', 'Ethan Birthday', '03-05', 2018, 'birthday')"
```

---

### 8. Family Shopping (🛒)
**Purpose:** Shopping prediction based on purchase history.

**Key Features:**
- Add items to shopping list
- View shopping history
- Analyze purchase frequency
- Generate shopping suggestions

**When to use:**
- User wants to add shopping items
- User wants to view shopping history
- User needs shopping suggestions

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO tasks (id, title, type, status) \
   VALUES ('t20260302150000', 'Milk', 'shopping', 'pending')"
```

---

### 9. Family Vote (🗳️)
**Purpose:** Create and manage family decision voting.

**Key Features:**
- Create votes for family decisions
- Family members can vote
- View voting results
- Track active and closed votes

**When to use:**
- User wants to initiate a family vote
- Family needs to make a decision together
- User wants to see voting results

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO votes (id, title, description, status) \
   VALUES ('v20260302150000', 'Where to go this weekend?', 'Options: Park, Playground, Cinema', 'active')"
```

---

### 10. Family Milestone (🏆)
**Purpose:** Record important milestone events for family members.

**Key Features:**
- Record first times, achievements, growth milestones
- View milestone history by member
- Categorize milestones (first, achievement, growth, skill, life)
- Review growth journey

**When to use:**
- User wants to record an important milestone
- User wants to view someone's milestones
- Important event occurs (first steps, graduation, etc.)

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO milestones (id, member_name, title, category, date) \
   VALUES ('m20260302150000', 'Ethan', 'First independent steps', 'first', date('now'))"
```

---

### 11. Family Challenge (🎯)
**Purpose:** Create and manage family challenge activities.

**Key Features:**
- Create challenges (exercise, reading, habits)
- Track participant progress
- View leaderboards
- Goal setting and completion tracking

**When to use:**
- User wants to start a family challenge
- User wants to record challenge progress
- User wants to see rankings

**Example:**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO challenges (id, title, goal, description, status, start_date) \
   VALUES ('c20260302150000', 'Monthly Exercise Challenge', 30, 'Participant Progress:', 'active', date('now'))"
```

---

## Technical Specifications

### Database Path
All skills use: `~/.openclaw/family-partner/family.db`

### Cross-Platform Support
All skills use standard SQL commands, fully compatible with Windows, macOS, and Linux. OpenClaw automatically handles path conversions.

### ID Generation Pattern
Each skill generates unique IDs using timestamp format:
- **Calendar:** `e` + YYYYMMDDHHMMSS (e.g., `e20260302150000`)
- **Tasks:** `t` + YYYYMMDDHHMMSS (e.g., `t20260302150000`)
- **Memory:** `m` + YYYYMMDDHHMMSS (e.g., `m20260302150000`)
- **Labor:** `l` + YYYYMMDDHHMMSS (e.g., `l20260302150000`)
- **Family Time:** `f` + YYYYMMDDHHMMSS (e.g., `f20260302150000`)
- **Anniversary:** `a` + YYYYMMDDHHMMSS (e.g., `a20260302150000`)
- **Vote:** `v` + YYYYMMDDHHMMSS (e.g., `v20260302150000`)
- **Milestone:** `m` + YYYYMMDDHHMMSS (e.g., `m20260302150000`)
- **Challenge:** `c` + YYYYMMDDHHMMSS (e.g., `c20260302150000`)

### Edge Cases Handling
- Non-existent records: Return appropriate "not found" message
- Duplicate entries: Warn user and ask for confirmation
- Empty results: Return "no data available" message
- Invalid input: Ask user for clarification

## Example Interactions

### Morning Routine
**User:** Good morning
**AI:** ☀️ Good morning! Today is March 2, 2026, Monday
  
  📅 Today's Schedule:
  09:00 - Take Ethan to school (Dad)
  14:00 - Parent meeting (Mom) @ School
  19:00 - Family dinner
  
  📋 To-do Items:
  □ Doctor appointment (Mom)
  □ Clean garage (Dad)
  
  🛒 Shopping List:
  □ Milk
  □ Eggs
  
  🎂 Upcoming:
  March 5 - Ethan's Birthday 🎉
  
  Have a wonderful day! 🌟

### Task Management
**User:** Buy milk and eggs
**AI:** ✅ Added to shopping list:
    🛒 Milk
    🛒 Eggs

**User:** What's on the shopping list?
**AI:** 🛒 Shopping List:
    □ Milk
    □ Eggs
    □ Bread

**User:** Milk is bought
**AI:** ✅ Completed: Milk 🎉

### Recording Memories
**User:** Remember Ethan is allergic to peanuts
**AI:** ✅ Recorded: Ethan is allergic to peanuts ⚠️
    All future food suggestions will take this into account.

**User:** What does Mom like to eat?
**AI:** ❤️ Mom's Preferences:
    - Likes hot pot
    - Likes latte coffee
    - Likes purple

### Labor Tracking
**User:** Mom cooked for 1 hour today
**AI:** ✅ Recorded:
    👤 Mom
    🏠 Cooking
    ⏱️ 60 minutes

**User:** Show me this month's labor statistics
**AI:** 📊 This Month's Labor Contribution (Total: 90 hours):
    👤 Mom: 45 hours (50%)
    👤 Dad: 30 hours (33%)
    👤 Ethan: 15 hours (17%)
    
    💡 Suggestion: Dad could take on more housework～

### Creating Events
**User:** Remind Dad to take Ethan to dance class next Saturday at 3 PM
**AI:** ✅ Created event:
    📅 Time: March 8 (Saturday) 15:00
    📝 Event: Dance Class
    👥 Participants: Dad, Ethan

### Family Voting
**User:** Let's vote on where to go this weekend
**AI:** ✅ Created vote:
    📋 Where to go this weekend?
    
    Options:
    1️⃣ Park
    2️⃣ Playground
    3️⃣ Cinema
    
    Family members can start voting!

### Milestone Recording
**User:** Ethan walked independently for the first time today!
**AI:** ✅ Recorded milestone:
    👶 Ethan
    🎯 First independent steps
    📂 Category: First time
    📅 March 2, 2026
    
    This is an important moment in Ethan's growth! 🎉

### Family Challenge
**User:** Start a monthly exercise challenge
**AI:** ✅ Created challenge:
    🏆 Monthly Exercise Challenge
    🎯 Goal: 30 times
    📅 Start Date: March 2, 2026
    
    Family members can join now!

## Installation & Setup

### Prerequisites
- OpenClaw >= 0.8.0
- SQLite3 installed

### Database Initialization
The package includes `init.sql` for database setup. Run:
```bash
sqlite3 ~/.openclaw/family-partner/family.db < init.sql
```

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions, please visit the project repository.
