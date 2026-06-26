---
name: canvas-lms-student
description: Use when the user needs to interact with Canvas LMS as a student. Trigger phrases include "check my homework", "what's due", "download my lecture PDFs", "list my Canvas courses", "when is my assignment due", "get my course materials". Provides read-only access to courses, assignments, files, and deadlines. Supports AI-assisted academic workflows including assignment research, deadline tracking, and material gathering.
version: 0.1.1
metadata: {"openclaw":{"requires":{"env":["CANVAS_BASE_URL","CANVAS_API_TOKEN"],"anyBins":["python3","python"],"config":["~/.config/canvas-lms/config.json"]},"primaryEnv":"CANVAS_API_TOKEN","emoji":"🎓","homepage":"https://github.com/Efan404/canvas-lms-student-skill"}}
---

# Canvas LMS Student Skill

This skill enables read-only access to Canvas LMS for student workflows.

## When to Use

Invoke this skill when the user asks anything related to their Canvas courses, such as:
- "Check my homework" / "what's due this week"
- "List my Canvas courses" / "what classes am I taking"
- "Download my lecture PDFs" / "get course materials"
- "When is my assignment due" / "upcoming deadlines"
- "Show my grades" / "how am I doing in CS101"
- "Find the syllabus" / "search for project requirements"
- "Export deadlines to my calendar"
- "Help me write my essay" (will gather assignment requirements)

**Key indicators:** Canvas, course, assignment, homework, deadline, grade, syllabus, lecture notes, materials.

## Prerequisites

**Configuration (in order of precedence):**

1. **Environment Variables** (highest priority):
   - `CANVAS_BASE_URL` - Institution Canvas URL (e.g., `https://canvas.university.edu`)
   - `CANVAS_API_TOKEN` - Personal API token from Canvas Settings

2. **Config File** (fallback if env vars not set):
   - Location: `~/.config/canvas-lms/config.json`
   - Format: `{"base_url": "...", "api_token": "..."}`
   - Created automatically if you use the CLI tool (`canvas-lms config`)

**Setup Guide (if not configured):**
1. Guide user to: Canvas → Account → Settings → Approved Integrations
2. Click "+ New Access Token"
3. Configure using ONE of these methods:
   - **Environment variables:**
     ```bash
     export CANVAS_BASE_URL="https://your-school.instructure.com"
     export CANVAS_API_TOKEN="copied-token"
     ```
   - **CLI tool (easier for humans):**
     ```bash
     pip install canvas-lms-cli
     canvas-lms config  # Interactive setup
     ```
4. Test with: `python scripts/canvas_client.py --test`

## Available Tools

### 1. List Courses
**Script:** `python scripts/list_courses.py`

**Purpose:** Get course IDs and basic information for other operations.

**Key Options:**
- `--active-only` - Show only current enrollments
- `--with-grades` - Include current scores
- `--json` - Output structured JSON (recommended for AI parsing)
- `--resolve "Course Name"` - Find course by name instead of ID

**Output:** Course ID, name, code, grade (optional)

**When to Use:** 
- First step before any course-specific operation to get valid course IDs
- Or use `--resolve` to find course ID from name (e.g., `--resolve "CS101"`)

**AI Tip:** Use `--json` for reliable parsing, or `--resolve` to convert course names to IDs automatically.

---

### 2. Get Assignments
**Script:** `python scripts/get_assignments.py --course <ID>`

**Purpose:** List assignments with deadlines and submission status.

**Key Options:**
- `--course 12345` or `--course "CS101" --resolve-name` - Course ID or name
- `--upcoming` - Only future assignments
- `--overdue` - Only overdue assignments
- `--unsubmitted` - Only pending work
- `--with-description` - Include full descriptions
- `--json` - Output structured JSON
- `--assignment-name "Project"` - Find specific assignment by name

**When to Use:** Checking workload, finding deadlines, or getting assignment overview.

**AI Tip:** Use `--resolve-name` to avoid manual ID lookup, or `--assignment-name` to find specific assignments by name.

---

### 3. Get Assignment Detail (For AI Writing)
**Script:** `python scripts/get_assignment_detail.py --course <ID> --assignment <ID>`

**Purpose:** Retrieve complete assignment requirements for AI-assisted writing.

**Returns:**
- Full description/prompt (cleaned HTML)
- Points possible and rubric criteria
- Submission type requirements
- Due date and submission status
- Allowed file extensions

**When to Use:** Before AI-assisted essay/assignment writing to get full context and requirements.

---

### 4. Download Course Files
**Script:** `python scripts/download_files.py --course <ID> --output <DIR>`

**Purpose:** Download all course materials to local directory.

**Key Options:**
- `--folder "Folder Name"` - Download specific folder only
- `--type pdf` - Filter by file extension
- `--dry-run` - Preview without downloading
- `--flat` - Flat structure (don't preserve Canvas folders)
- `--json` - Output file list as JSON
- `--no-id-prefix` - Don't add ID prefix to duplicate filenames

**When to Use:** Gathering reading materials, saving lecture notes, or collecting reference documents.

**File Organization:**
By default, preserves Canvas folder structure. Files with duplicate names get ID prefix (e.g., `12345_lecture.pdf`). Use `--flat` for flat structure.

---

### 5. Export Deadlines to Calendar
**Script:** `python scripts/export_calendar.py --course <IDs> --output <FILE>`

**Purpose:** Export assignment deadlines to iCalendar (.ics) format.

**Key Options:**
- `--courses 123,456,789` - Multiple courses (comma-separated)
- `--unsubmitted-only` - Only pending assignments

**When to Use:** Creating calendar reminders, syncing with Google/Apple Calendar.

---

### 6. Search Canvas Content
**Script:** `python scripts/search_canvas.py --query "<search>"`

**Purpose:** Find files, assignments, or announcements across courses.

**Key Options:**
- `--course <ID>` - Search specific course only
- `--type assignment|file|announcement` - Limit search type
- `--full-content` - Show content previews

**When to Use:** Finding specific resources, locating assignment requirements, checking announcements.

---

## Workflow Patterns

### Pattern 1: AI-Assisted Essay Writing
```
1. List courses → get course ID
2. Get assignments → find target assignment ID
3. Get assignment detail → retrieve full requirements and rubric
4. (Optional) Search for related materials
5. (Optional) Download reference files
6. AI generates essay based on gathered context
```

### Pattern 2: Deadline Management
```
1. List courses → get all course IDs
2. Export calendar → generate .ics with all deadlines
3. Import to calendar app for reminders
```

### Pattern 3: Course Material Collection
```
1. List courses → get course ID
2. Download files → get all course materials
3. Search for specific topics if needed
```

## Safety & Limitations

**Read-Only:** This skill only reads data. It cannot:
- Submit assignments
- Modify grades
- Post to discussions
- Upload files to Canvas

**Rate Limits:** Canvas API has rate limiting. For bulk operations:
- Use pagination (handled automatically)
- Add delays between requests if needed
- Handle 429 errors with exponential backoff

**Data Privacy:**
- API tokens are password-equivalent
- Never log or expose tokens
- All data stays local (downloads only)

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Guide user to regenerate token |
| 403 Forbidden | Insufficient permissions | Check enrollment status |
| 404 Not Found | Wrong course/assignment ID | Verify IDs from list commands |
| 429 Rate Limited | Too many requests | Add delay and retry |

## References

- [API Overview](references/api-overview.md) - Authentication and pagination
- [Courses](references/courses.md) - Course operations details
- [Assignments](references/assignments.md) - Assignment handling
- [Files](references/files.md) - File download details
- [Calendar Export](references/calendar-export.md) - ICS format details
- [Search](references/search.md) - Search techniques

---

## OpenClaw Integration

This repository can be installed from ClawHub/OpenClaw as a skill bundle.
OpenClaw discovers the skill from `SKILL.md`. The added `manifest.json` and
`wrapper.py` are supplemental helper files for wrapper-based environments; they
do not auto-register seven native OpenClaw tools by themselves. If you want
native tool exposure inside OpenClaw, package the wrapper as a plugin or MCP
server separately.

### Installation

```bash
# Preferred: install from ClawHub/OpenClaw
openclaw skills install canvas-lms-student

# Or install with clawhub
clawhub install canvas-lms-student

# Or clone the repository directly
git clone https://github.com/Efan404/canvas-lms-student-skill.git

# Run setup to install dependencies
cd canvas-lms-student-skill
./setup.sh

# Or manually install dependencies
pip3 install canvasapi requests
```

### Configuration

Set up Canvas API access:

```bash
# Method 1: Environment variables
export CANVAS_BASE_URL="https://your-school.instructure.com"
export CANVAS_API_TOKEN="your-api-token"

# Method 2: Config file
mkdir -p ~/.config/canvas-lms
echo '{"base_url": "https://...", "api_token": "..."}' > ~/.config/canvas-lms/config.json
```

Get API token: Canvas → Account → Settings → Approved Integrations → + New Access Token

### Available Tools

When used through the local wrapper, these commands are available:

| Tool | Description | Example |
|------|-------------|---------|
| `list_courses` | List all courses | `list_courses()` |
| `resolve_course` | Find course by name | `resolve_course(name="CS5293")` |
| `get_assignments` | Get course assignments | `get_assignments(course="CS5293")` |
| `get_assignment_detail` | Get assignment info | `get_assignment_detail(course=67488, assignment=319756)` |
| `search_canvas` | Search content | `search_canvas(query="project", type="assignment")` |
| `download_files` | Download course files | `download_files(course=67488, type="pdf")` |
| `export_calendar` | Export deadlines | `export_calendar(courses="67488,67524")` |

### Wrapper Usage

For programmatic access, use the wrapper:

```bash
python3 wrapper.py list_courses '{"active_only": true}'
python3 wrapper.py get_assignments '{"course": "CS5293", "upcoming": true}'
python3 wrapper.py search_canvas '{"query": "deadline", "type": "announcement"}'
```

### Manifest

See `manifest.json` for complete tool definitions and parameter schemas.
