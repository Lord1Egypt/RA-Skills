# Family Partner - OpenClaw Skills Suite

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill%20Registry-blue)](https://clawhub.ai/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green)](https://github.com/openclaw/openclaw)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

> 🏠 **AI-Powered Family Intelligence Suite** - Making family management as simple as chatting

## 📖 Introduction

Family Partner is a complete home management solution designed for OpenClaw. With just one installation, you get:

### 🎯 Core Value Proposition

- **📅 Unified Calendar Management** - Create, view, delete family events; support for today/tomorrow/this week queries
- **✅ Smart Task Management** - To-do items, shopping lists, task assignment to family members
- **💭 Family Memory Network** - Record preferences, allergies, contraindications; AI proactive reminders
- **📊 Invisible Labor Tracking** - Visualize household contributions, promote family fairness
- **⏰ Family Time Recording** - Cherish every family activity, generate beautiful memories
- **🌅 Morning Briefing** - Daily automatic push of today's schedule, never forget important tasks
- **🎉 Anniversary Manager** - Birthday and wedding anniversary reminders, never miss important moments
- **🛒 Shopping Prediction** - Smart reminders based on consumption rate, continuous supply of essentials
- **🗳️ Voting & Decisions** - Democratic family decision-making, minority follows majority
- **🏆 Milestone Recording** - Witness every step of child growth, record family highlight moments
- **🎯 Family Challenges** - Gamified family activities, making persistence more interesting

## ✨ Features

### 🚀 Core Advantages

- **Cross-Platform Compatible** - Full support for Windows, macOS, Linux
- **Lightweight Implementation** - Uses SQLite database, no complex deployment needed
- **Privacy-First** - All data stored locally (`~/.openclaw/family-partner/`)

### 🛡️ Security Commitment

- ✅ No hardcoded credentials
- ✅ Minimal permission principle
- ✅ Transparent data access
- ✅ Open source code auditable
- ✅ Pure local storage, no cloud sync

## Function Modules (All included in SKILL.md)

### Core Functions

| Function | Description | Database Table |
|----------|-------------|----------------|
| **📅 Calendar Management** | Create, view, delete family events | events |
| **✅ Task Management** | To-do items, shopping lists, task assignments | tasks |
| **💭 Family Memory** | Record preferences, allergies, important info | memories |

### Important Functions

| Function | Description | Database Table |
|----------|-------------|----------------|
| **📊 Invisible Labor** | Record and track household contributions | labor |
| **⏰ Family Time** | Record family activities together | family_time |
| **🌅 Morning Briefing** | Daily automatic push of today's schedule | Multi-table query |
| **🎉 Anniversary** | Birthday and wedding anniversary reminders | anniversaries |
| **🛒 Shopping Prediction** | Smart suggestions based on history | tasks |

### Extended Functions

| Function | Description | Database Table |
|----------|-------------|----------------|
| **🗳️ Voting & Decisions** | Initiate and manage family votes | votes |
| **🏆 Milestone** | Witness important growth moments | milestones |
| **🎯 Family Challenge** | Create gamified challenge activities | challenges |

**Note**: All functions share the same database `~/.openclaw/family-partner/family.db`, data is fully interconnected.

## 🔧 Technical Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interaction Layer                   │
│  Telegram / WeChat Work / Feishu / CLI / Web                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 OpenClaw AI Agent                           │
│  • Natural Language Understanding                            │
│  • Read SKILL.md Instructions                                │
│  • Generate Unique ID (timestamp format)                     │
│  • Execute Shell Commands                                    │
│  • Parse Complex Data                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Family Partner - Single File Master Version        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SKILL.md (The Only Skill File)                       │   │
│  │  - Contains all 11 function modules                   │   │
│  │  - Unified entry point, intelligent routing           │   │
│  │  - Shared database and context                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Function Modules (Logical grouping, not physical)    │   │
│  ├──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ P0 Core (3)  │  │ P1 Key (5)   │  │ P2 Extended(3)│   │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ Calendar Mgt │  │ Invisible Lab│  │ Vote/Decision│   │
│  │ Task Mgt     │  │ Family Time  │  │ Milestone    │   │
│  │ Family Memory│  │ Morning Brief│  │ Family Chalg │   │
│  │              │  │ Anniversary  │  │              │   │
│  │              │  │ Shopping Pred│  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                Data Storage Layer (SQLite)                  │
│  ~/.openclaw/family-partner/family.db                       │
│                                                             │
│  • 9 Core Tables (events, tasks, labor, etc.)               │
│  • Flat design, reduced JOIN operations                     │
│  • Unified database, all functions shared                   │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

#### Core Tables

```sql
-- Events table
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    participants TEXT,  -- Comma-separated: "Dad, Mom, Ethan"
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT DEFAULT 'todo',  -- todo, shopping
    status TEXT DEFAULT 'pending',
    assignee TEXT,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invisible Labor table
CREATE TABLE labor (
    id TEXT PRIMARY KEY,
    member_name TEXT NOT NULL,
    type TEXT NOT NULL,  -- cooking, cleaning, childcare, etc.
    duration INTEGER NOT NULL,  -- minutes
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family Time table
CREATE TABLE family_time (
    id TEXT PRIMARY KEY,
    activity TEXT NOT NULL,
    participants TEXT,
    duration INTEGER,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Milestones table
CREATE TABLE milestones (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    category TEXT,  -- first, achievement, growth, skill, life, other
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anniversaries table
CREATE TABLE anniversaries (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,  -- MM-DD format
    year INTEGER,
    type TEXT DEFAULT 'birthday',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family Memories table
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    type TEXT NOT NULL,  -- preference, dislike, allergy
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Votes table (Simplified version)
CREATE TABLE votes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- Stores options and voting records
    status TEXT DEFAULT 'active',
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Challenges table (Simplified version)
CREATE TABLE challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- Stores participants and progress
    goal INTEGER,
    status TEXT DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Quick Start

### Prerequisites

- ✅ OpenClaw v0.8.0 or higher
- ✅ SQLite 3.x (pre-installed on most systems)
- ✅ Node.js 22+ (for OpenClaw)

### Installation

#### Install from ClawHub

**One-click installation of the entire Family Partner suite:**

```bash
openclaw skills install family-partner
```

### Verify Installation

```bash
# View all installed Family Partner skills
openclaw skills list | grep family

# Test morning briefing function
openclaw chat --message "Good morning"
```

### Initialize Database

If not automatically initialized during installation, manually execute:

```bash
# Create database directory
mkdir -p ~/.openclaw/family-partner

# Execute initialization script
sqlite3 ~/.openclaw/family-partner/family.db < init.sql
```

After initialization, the following tables will be created:
- events (Calendar)
- tasks (Tasks)
- labor (Labor records)
- family_time (Family time)
- milestones (Milestones)
- anniversaries (Anniversaries)
- memories (Family memories)
- votes (Votes)
- challenges (Challenges)

## 💡 Usage Examples

### Typical Usage Scenarios

#### Scenario 1: Morning Routine

```bash
# Automatically push every day at 8:00 AM
AI: 🌅 Good morning! Today is March 7, Saturday
    
    📅 Today's schedule:
    1. 10:00 - Parent-teacher meeting (Dad, Mom) @ School
    2. 18:00 - Family dinner @ Restaurant
    
    ✅ To-do tasks:
    1. Pay electricity bill (Due: Today)
    2. Buy milk
    
    🛒 Shopping list:
    □ Milk
    □ Eggs
    
    🎂 Upcoming anniversaries:
    • March 10: Grandma's birthday (in 3 days)
    
    Have a wonderful day! 🌟
```

#### Scenario 2: Recording Invisible Labor

```bash
# Record housework
User: Mom cooked for 1 hour today
AI: ✅ Recorded:
    👤 Mom
    🏠 Cooking
    ⏱️ 60 minutes

# Monthly statistics
User: Show housework statistics for this month
AI: 📊 Monthly housework contribution statistics (Total: 90 hours):
    👤 Mom: 45 hours (50%)
    👤 Dad: 30 hours (33%)
    👤 Ethan: 15 hours (17%)
    
    💡 Suggestion: Mom承担较多，建议重新分配部分家务哦～
```

#### Scenario 3: Family Decision Voting

```bash
# Initiate a vote
User: Create a vote, where to go this weekend
AI: ✅ Vote created:
    📋 Where to go this weekend?
    
    Options:
    1️⃣ Park picnic
    2️⃣ Amusement park
    3️⃣ Cinema
    
    Family members can start voting! Reply "I choose park" to vote.

# View results
User: What are the voting results?
AI: Current vote statistics:
    Park picnic: 2 votes (Dad, Mom)
    Amusement park: 1 vote (Ethan)
    
    🏆 Winning option: Park picnic
```

#### Scenario 4: Recording Growth Milestones

```bash
# Record milestone
User: Ethan walked independently for the first time today!
AI: ✅ Milestone recorded:
    👶 Ethan
    🎯 First independent walking
    📂 Category: First time
    📅 March 7, 2026
    
    This is an important moment in Ethan's growth! 🎉

# Review growth journey
User: What are Ethan's growth milestones?
AI: 🎯 Ethan's growth records:
    
    2026
    - March 7: First independent walking [First time]
    - February 15: Learned to call mom and dad [Skill]
    - January 10: First roll over [Growth]
```

#### Scenario 5: Family Challenge Activities

```bash
# Create challenge
User: Create a 30-day exercise challenge
AI: ✅ Challenge created:
    🏆 30-day exercise challenge
    🎯 Goal: 30 times
    📅 Start date: March 7
    
    Family members can start participating! Reply "I join" to participate.

# Record progress
User: I ran 5 kilometers today
AI: ✅ Progress updated!
    👤 You
    🏃 Running 5 km
    📊 Challenge progress: 6/30 times
    
    Keep it up! 24 more times to complete the challenge! 💪
```

### More Practical Tips

#### Quick Queries

```bash
# What's scheduled for today?
→ Query today's schedule

# Who does the most housework this week?
→ Show this week's labor statistics

# What is Ethan allergic to?
→ Query family memories

# When is the next family gathering?
→ Query future events

# What does our whole family like?
→ Show all family members' preferences
```

#### Smart Reminders

```bash
# Remember Ethan needs to bring medical report to school next week
→ AI will automatically add to calendar and set reminder

# Remind me to buy diapers tomorrow
→ AI will add to shopping list

# Wedding anniversary next Wednesday
→ AI will start reminding 3 days in advance
```

#### Data Analysis

```bash
# How much time did we spend together this month?
→ Statistics on total family time duration

# How many milestones were achieved this year?
→ Show annual milestone statistics

# Which week was the most fair for our family?
→ Analyze fairness of labor distribution
```

## 🔐 Security Notes

### Permission Declaration

Family Partner only requests the following minimal permissions:

- **File System**: Read/write access to `~/.openclaw/family-partner/` directory
- **Binary Tools**: `sqlite3` (for database operations)
- **No Network Access**: All data stored locally, zero cloud sync

### Environment Variables

This skills package does not require any environment variables. All configuration is done locally.

### Data Security

- ✅ All data stored locally (`~/.openclaw/family-partner/family.db`)
- ✅ No data uploaded to cloud
- ✅ No third-party tracking code
- ✅ Open source code, community auditable
- ✅ Standard SQLite encryption (optional)
- ✅ Regular automatic backups (configurable)

### Privacy Protection

- 🛡️ **Data Isolation**: Each family's data is completely isolated
- 🛡️ **Local First**: All computations done locally
- 🛡️ **Transparent Operations**: All SQL commands visible and verifiable
- 🛡️ **Minimal Permissions**: Only access necessary files and directories

## 🛠️ Development & Maintenance

### Update Skills Package

```bash
# Update the entire skills package
openclaw skills update family-partner

# Or manually update
cd ~/.openclaw/skills/family-partner
git pull origin main
```

### Backup & Recovery

#### Backup Database

```bash
# Manual backup
cp ~/.openclaw/family-partner/family.db ~/backups/family-backup-$(date +%Y%m%d).db

# Or use SQLite export
sqlite3 ~/.openclaw/family-partner/family.db ".backup '~/backups/family-backup.db'"
```

#### Restore Database

```bash
# Restore from backup
sqlite3 ~/.openclaw/family-partner/family.db < ~/backups/family-backup.db
```

### Troubleshooting

#### Issue: Skill fails to load

```bash
# Check if SQLite is installed
sqlite3 --version

# Check database file
ls -la ~/.openclaw/family-partner/family.db

# Reinitialize database
sqlite3 ~/.openclaw/family-partner/family.db < init.sql

# View OpenClaw logs
openclaw logs --tail 50
```

#### Issue: Query returns no results

```bash
# Check if data exists
sqlite3 ~/.openclaw/family-partner/family.db "SELECT * FROM events LIMIT 5"

# Check date format
sqlite3 ~/.openclaw/family-partner/family.db "SELECT date('now')"

# Verify table structure
sqlite3 ~/.openclaw/family-partner/family.db ".schema"
```

#### Issue: Morning briefing not pushing

```bash
# Check cron job configuration
crontab -l | grep openclaw

# Manual test
openclaw chat --message "Good morning"

# View detailed errors
openclaw chat --message "Good morning" --verbose
```

### Performance Optimization

```bash
# Regularly clean old data (optional)
sqlite3 ~/.openclaw/family-partner/family.db \
  "DELETE FROM labor WHERE date < date('now', '-1 year')"

# Optimize database performance
sqlite3 ~/.openclaw/family-partner/family.db "VACUUM"
sqlite3 ~/.openclaw/family-partner/family.db "ANALYZE"
```

## 📚 Documentation Resources

- [OpenClaw Official Docs](https://docs.openclaw.ai/tools/skills)
- [ClawHub Skill Format Spec](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Batch Upload Guide](批量上传指南.md) - Detailed publishing and upload instructions

## ❓ FAQ

### Q: Will data be synced to the cloud?
A: No. All data is stored locally, completely privacy-protected. If you need multi-device sync, you can configure cloud sync tools yourself (such as iCloud, Dropbox).

### Q: How to migrate to a new device?
A: Simply copy the `family.db` database file to the same location on the new device, then reinstall the skills package.

### Q: Does it support custom extensions?
A: Yes! You can add new tables and SQL commands based on the existing architecture. See developer documentation for details.

### Q: Can multiple families share one instance?
A: Technically yes, but not recommended. It's recommended that each family use an independent database instance to ensure data isolation.

### Q: How to report issues or suggestions?
A: Welcome to submit feedback via GitHub Issues, or contact the author directly.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file

## 👥 Team & Acknowledgments

### Main Author

- **AI-PlusPlus** - Initial design and implementation

### Special Thanks

- [OpenClaw Team](https://github.com/openclaw) - For providing the powerful AI Agent framework
- [ClawHub](https://clawhub.ai/) - Skills registry and distribution platform
- All contributors and early adopters

---

<div align="center">

**If this project helps you, please give us a ⭐️ Star!**

Made with ❤️ by AI-PlusPlus

**🏠 Family Partner - Making Love More Organized**

</div>
