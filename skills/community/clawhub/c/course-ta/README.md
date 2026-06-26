# Course TA — OpenClaw Skill

An AI-powered virtual teaching assistant skill for [OpenClaw](https://github.com/nichochar/openclaw) that integrates with Canvas LMS and Discord to answer student questions using RAG over course materials.

## Features

- **Canvas LMS integration** — Auto-discovers courses, syncs all content (pages, assignments, announcements, discussions, quizzes, files, syllabus, enrollments)
- **Multi-course support** — Manages multiple courses/sections with full data isolation
- **Discord channel routing** — Maps channels to specific courses with security boundaries
- **RAG-powered Q&A** — Converts Canvas content and PPTX slides to markdown for retrieval-augmented answering
- **Rate limiting** — Per-user hourly/daily limits with privileged user tiers
- **Admin commands** — Inline content editing, Canvas sync triggers, submission tracking
- **Dashboard tools** — Deadlines, grades, engagement, roster, cross-section broadcast
- **Audit logging** — JSONL logs of all interactions
- **Write gating** — All Canvas write operations require explicit user confirmation; reads are unrestricted
- **Incremental sync** — SHA-256 change detection, only writes files that actually differ
- **Cron scheduling** — Periodic background sync (configurable interval)

## Directory Structure

```
course-ta/
├── SKILL.md                    # Agent behavior specification
├── .gitignore                  # Protects credentials, data, logs
├── README.md                   # This file
│
├── lib/                        # Python modules
│   ├── paths.py                # Central path resolver
│   ├── canvas_api.py           # Canvas REST API client
│   ├── canvas_content.py       # HTML → markdown converter
│   ├── canvas_courses.py       # Multi-course management CLI
│   ├── canvas_sync.py          # Content sync engine
│   ├── canvas_dashboard.py     # Admin dashboard tools
│   ├── extract_slides.py       # PPTX → markdown extractor
│   ├── rate_limit.py           # Per-user rate limiter
│   └── log_interaction.py      # Audit logger
│
├── config/                     # Runtime configs (created during setup)
│   ├── course-ta.json.template
│   ├── canvas-config.json.template
│   └── course-configs/         # Per-course configs
│
├── data/                       # All gitignored
│   ├── credentials/            # Canvas API token
│   ├── courses/                # Synced course content
│   ├── memory/                 # Generated RAG markdown files
│   └── logs/                   # Interaction audit logs
│
├── references/                 # Setup documentation
└── scripts/                    # Setup automation
```

## Quick Start

### Prerequisites

- [OpenClaw](https://github.com/nichochar/openclaw) installed and running
- Python 3.9+ with `requests` and `beautifulsoup4`:
  ```bash
  pip3 install requests beautifulsoup4
  ```
- A Canvas LMS API token (generate from Canvas → Account → Settings → New Access Token)

### 1. Install the skill

Copy this directory to `~/.openclaw/skills/course-ta/`.

### 2. Configure Canvas credentials

```bash
cp data/credentials/canvas.json.template data/credentials/canvas.json
# Edit with your Canvas base URL and API token
```

### 3. Initialize configs

```bash
cp config/course-ta.json.template config/course-ta.json
cp config/canvas-config.json.template config/canvas-config.json
# Edit course-ta.json with your Discord channel IDs, admin users, etc.
```

### 4. Discover and activate courses

```bash
cd ~/.openclaw/skills/course-ta/lib

# List available Canvas courses
python3 canvas_courses.py list

# Activate a course
python3 canvas_courses.py activate <canvas_course_id>

# Or map to an existing local directory
python3 canvas_courses.py map <canvas_course_id> <slug>
```

### 5. Sync course content

```bash
# Full initial sync
python3 canvas_sync.py full <canvas_course_id>

# Incremental sync (for periodic updates)
python3 canvas_sync.py all --incremental
```

### 6. Index memory for OpenClaw RAG

```bash
# Symlink skill memory to workspace (if not already done)
ln -sf ~/.openclaw/skills/course-ta/data/memory ~/.openclaw/workspace/memory

# Rebuild index
openclaw memory index --force
```

### 7. Verify

```bash
python3 canvas_api.py validate
python3 canvas_courses.py status
python3 canvas_dashboard.py deadlines
```

## Dashboard Commands

```bash
python3 canvas_dashboard.py deadlines [--days 7]
python3 canvas_dashboard.py submissions <course_id> <assignment_name>
python3 canvas_dashboard.py engagement <course_id>
python3 canvas_dashboard.py grades <course_id>
python3 canvas_dashboard.py roster <course_id>
python3 canvas_dashboard.py broadcast "<message>"
```

## Security Model

- **Read operations** (Canvas API GET, file reads): unrestricted
- **Write operations** (Canvas API POST/PUT, file edits): require explicit user confirmation
- **Channel isolation**: each Discord channel maps to exactly one course; the agent only reads memory files matching that course's slug
- **Enrollment privacy**: student rosters are stored as JSON but never indexed in RAG memory
- **Credentials**: stored in `data/credentials/` (gitignored)
- **Audit trail**: all interactions logged to `data/logs/` with timestamps, user IDs, and status codes

## License

MIT
