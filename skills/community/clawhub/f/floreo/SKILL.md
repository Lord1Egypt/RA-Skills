---
name: floreo
description: "Floreo - Autonomous compounding journal with local storage and open connections. Auto-detects activities, tracks compound metrics (streaks, trends, velocity), cross-domain correlations, and syncs with external services. Intelligent automation with privacy controls."
homepage: https://github.com/openclaw/floreo
metadata:
  {
    "openclaw":
      {
        "emoji": "🌸",
        "requires": {},
        "install": [],
      },
  }
---

# Floreo

**Version**: 0.2.1  
**Type**: Autonomous Life Flourishing System  
**Approach**: OpenClaw Native Tools with Autonomous Features & Open Connections  
**Skill Longevity**: Built to Last (see Maintenance section)  

**New in v0.2.0**:
- 🔄 **Compounding Metrics** — Streaks, trends, velocity, cross-domain correlations
- 👤 **Configurable User Name** — Set and change your name anytime
- 🧬 **Longevity & Healthspan** — Biomarker tracking, biological age estimation
- 💊 **Compression of Morbidity** — Healthspan vs lifespan ratio
- 🏃 **Exercise Zones** — Zone 2 (mitochondrial) + Zone 4 (VO2 max) tracking
- 🩺 **Healthspan Scoring** — 0-100 composite from sleep, exercise, nutrition, stress
- 🔬 **Longevity Interventions** — Fasting, supplements, recovery protocols
- ⏳ **90-Day Trends** — Longevity trajectory visualization
- 🛡️ **Skill Durability** — Backward compatible, future-proof, maintainable  

> *Flore per integra* — Flourish through wholeness.

Floreo is a **methodology**, not a custom tool. It uses OpenClaw's native capabilities (file operations, memory, shell commands) to track your life across work, health, learning, relationships, and creativity.

> **📍 Important Clarifications**:
> - `{user_name}` refers to your configured name in `~/.openclaw/customers/.floreo-user`
> - **Autonomous mode available** — background processes can auto-detect activities
> - **"Automated" analysis** — scheduled shell scripts via cron/heartbeat
> - **File watchers optional** — monitor git, calendar, files (opt-in)
> - **Open connections** — Notion, GitHub, Calendar integrations (opt-in)
> - **Privacy controls** — granular control over what gets logged and shared

---

## 📚 Table of Contents

1. [Philosophy](#philosophy)
2. [Security & Privacy Statement](#-security--privacy-statement)
3. [Quick Start](#quick-start)
4. [Entry Format](#entry-format)
5. [Recording Entries](#recording-entries-native-tools)
6. [Directory Structure](#directory-structure)
7. [User Profile Management](#-user-profile-management)
8. [Querying Entries](#querying-entries-native-tools)
9. [Timeline Compilation](#timeline-compilation-native-tools)
10. [Export Screening](#export-screening-privacy)
11. [Reflection & Analysis](#reflection--analysis-native-tools)
12. [Integration with MEMORY.md](#integration-with-memorymd)
13. [Automation with Cron](#automation-with-cron)
14. [Tips & Best Practices](#tips--best-practices)
15. [Import from Historical Files](#import-from-historical-files)
16. [Compound Metrics System](#-compound-metrics-system)
17. [Cross-Domain Correlation](#-cross-domain-correlation-analysis)
18. [Automated Insight Generation](#-automated-insight-generation)
19. [Momentum & Streak Tracking](#-momentum--streak-tracking)
20. [Autonomous Analysis Setup](#-autonomous-analysis-setup)
21. [Longevity & Healthspan](#-longevity--healthspan-tracking)
22. [Artistic Reports](#automated-artistic-reports)
23. [Skill Longevity](#-skill-longevity--maintenance)
24. [Limitations](#limitations-of-native-approach)
25. [Complete Workflow Example](#example-complete-workflow)
26. [Resources](#resources)

---

## Philosophy

**No custom scripts. No dependencies. Pure OpenClaw.**

Floreo defines conventions for:
- Where to store entries
- How to structure them
- How to query them
- How to export them safely

You use OpenClaw's native tools to implement it.

---

## 🔒 Security & Privacy Statement

### What This Skill Does

- ✅ **Autonomous operation** — Background processes watch for activities (git commits, file changes, calendar events)
- ✅ **Local file storage** — Primary data stays in `~/.openclaw/customers/{name}/floreo/`
- ✅ **Open connections** — Optional integrations with external services (Notion, GitHub, Calendar APIs)
- ✅ **Automatic detection** — Detects code commits, meeting attendance, file modifications
- ✅ **Shell script automation** — Scheduled analysis runs via cron/heartbeat
- ✅ **Privacy controls** — Configurable data sharing levels

### Autonomous Features

**File System Watchers:**
- Monitor git repositories for commits
- Track file changes in specified directories
- Detect new calendar events

**External Connections (Optional):**
- Notion API for database sync
- GitHub API for commit/PR tracking
- Calendar APIs for meeting logging
- Slack webhook for notifications

**Data Storage:**
- Local: `~/.openclaw/customers/{name}/floreo/`
- External: Configurable via API keys in `~/.openclaw/customers/.floreo-config/`

### Opt-In/Opt-Out Controls

```bash
# Disable autonomous features
echo "autonomous_mode: false" >> ~/.openclaw/customers/.floreo-config

# Disable specific watchers
echo "watch_git: false" >> ~/.openclaw/customers/.floreo-config
echo "watch_calendar: false" >> ~/.openclaw/customers/.floreo-config

# Run in manual-only mode
FLORO_MANUAL=1 openclaw skill use floreo
```

### System Requirements

**Required:**
- `bash` or `zsh` (POSIX shell)
- `grep`, `sed`, `awk`, `date`, `find`, `bc`, `openssl`

**Optional (for autonomous features):**
- `fswatch` or `inotifywait` (file watching)
- `git` (commit detection)
- API keys for external services (stored securely)

---

---

## Quick Start

### 1. Set Your Name (Can Change Anytime)

Your name/identifier is stored in a config file and can be updated whenever you want:

```bash
# Set your name for the first time
echo "jerry" > ~/.openclaw/customers/.floreo-user

# Or use OpenClaw to set it
Write "jerry" to ~/.openclaw/customers/.floreo-user
```

**To change your name later:**
```bash
# Simply overwrite the file
echo "jerry-smith" > ~/.openclaw/customers/.floreo-user

# Or read the current name first, then update
Read ~/.openclaw/customers/.floreo-user
# Then write the new name
```

**Using your name in scripts:**
```bash
#!/bin/bash
# Get current user name
user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

# Use in paths
mkdir -p ~/.openclaw/customers/$user_name/floreo/domains/work
echo "Entry for $user_name"
```

### 2. Initialize Structure (One-time)

```bash
# Get your name
user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "user")

# Create Floreo directory structure
mkdir -p ~/.openclaw/customers/$user_name/floreo/{domains/{work,health,learn,relate,create,reflect},insights,goals}

# Example output: creates ~/.openclaw/customers/{user_name}/floreo/...
```

### 2. Record Your First Entry

```bash
# Create a work entry
cat >> ~/.openclaw/customers/{user_name}/floreo/domains/work/$(date +%Y)/$(date +%m)/$(date +%d-%m-%y).md << 'EOF'
---
type: entry
entry_id: FE-$(date +%Y%m%d)-$(openssl rand -hex 3 | tr '[:lower:]' '[:upper:]')
domain: work
date: $(date +%d-%m-%y)
day: $(date +%j)
timestamp: $(date -Iseconds)
privacy: internal
metrics:
  focus: 4
  commits: 5
tags: project-x, deep-work
---
Shipped v0.6.8 to production after fixing the critical auth bug.
EOF
```

Or simpler — use OpenClaw to write it (using your configured name):

```
# First, read your user name
Read ~/.openclaw/customers/.floreo-user

# Then write to your personal path
Write an entry to ~/.openclaw/customers/{your-name}/floreo/domains/work/2026/04/15-04-26.md with this content:

---
type: entry
entry_id: FE-20260415-A1B2C3
domain: work
date: 15-04-26
day: 105
timestamp: 2026-04-15T10:30:00
privacy: internal
metrics:
  focus: 4
  commits: 5
tags: project-x, deep-work
---
Shipped v0.6.8 to production after fixing the critical auth bug.
```

---

## Entry Format

Every entry is a Markdown file with YAML frontmatter:

```markdown
---
type: entry
entry_id: FE-YYYYMMDD-XXXXXX      # Unique ID
domain: work|health|learn|relate|create|reflect
date: DD-MM-YY
day: NNN                          # Day of year
timestamp: ISO-8601
privacy: private|internal|public   # Privacy tier
metrics:                          # Key-value pairs
  focus: 4
  commits: 5
tags: tag1, tag2, tag3
---

Entry content here. Can be multiple paragraphs.
Support **markdown** formatting.
```

### Privacy Tiers

| Level | Icon | Export | Use For |
|-------|------|--------|---------|
| **private** | 🔒 | Never | Passwords, health, secrets |
| **internal** | 👁️ | With screening | Work notes, client details |
| **public** | 🌐 | Anywhere | Blog posts, open source |

### Auto-Detect Privacy

When creating entries, OpenClaw can suggest privacy based on content:

- Contains "password", "secret", "confidential" → **private**
- Contains "client", "revenue", "internal" → **internal**
- General notes → **internal** (safe default)

---

## Recording Entries (Native Tools)

### Method 1: Direct File Write

```
Write to ~/.openclaw/customers/{user_name}/floreo/domains/health/2026/04/15-04-26.md:

---
type: entry
entry_id: FE-20260415-HEALTH1
domain: health
date: 15-04-26
day: 105
timestamp: 2026-04-15T08:00:00
privacy: private
metrics:
  energy: 8
  sleep: 7.5
tags: morning, exercise
---
Morning run 5k in 25 minutes. Feeling energized!
```

### Method 2: Append to Existing File

```
Read ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/15-04-26.md
Then append a new entry:

---
type: entry
entry_id: FE-20260415-WORK2
domain: work
date: 15-04-26
day: 105
timestamp: 2026-04-15T14:30:00
privacy: internal
metrics:
  meetings: 2
  focus: 3
tags: meetings, planning
---
Afternoon planning session with the team.
```

### Method 3: Use Shell Commands

```bash
# Create entry with shell
cat >> ~/.openclaw/customers/{user_name}/floreo/domains/learn/$(date +%Y)/$(date +%m)/$(date +%d-%m-%y).md << 'EOF'
---
type: entry
entry_id: FE-$(date +%Y%m%d)-$(openssl rand -hex 3 | tr '[:lower:]' '[:upper:]')
domain: learn
date: $(date +%d-%m-%y)
day: $(date +%j)
timestamp: $(date -Iseconds)
privacy: public
metrics:
  pages: 30
  minutes: 45
tags: reading, rust
---
Read chapter 3 of the Rust book. Learned about ownership and borrowing.
EOF
```

---

## Directory Structure

```
~/.openclaw/customers/{user_name}/floreo/
├── domains/
│   ├── work/
│   │   └── 2026/
│   │       └── 04/
│   │           └── 15-04-26.md
│   ├── health/
│   ├── learn/
│   ├── relate/
│   ├── create/
│   └── reflect/
├── insights/
│   └── weekly-reflection-2026-W16.md
├── goals/
│   └── 2026-Q2-goals.md
└── exports/
    └── export-2026-04-15.md
```

---

## 👤 User Profile Management

Your identity in Floreo is completely configurable and can be changed at any time.

### Setting Your Name

**First time setup:**
```bash
# Set your name
echo "alex" > ~/.openclaw/customers/.floreo-user

# Verify
cat ~/.openclaw/customers/.floreo-user
# Output: alex
```

**Using OpenClaw:**
```markdown
Write "alex" to ~/.openclaw/customers/.floreo-user
```

### Changing Your Name (Anytime)

You can change your name whenever you want — all your entries stay linked to you:

```bash
# Change from "alex" to "alex-johnson"
echo "alex-johnson" > ~/.openclaw/customers/.floreo-user

# Old entries remain at old path (you can migrate if desired)
# New entries go to new path
```

**Migration script (optional):**
```bash
#!/bin/bash
# migrate-user.sh — Move entries to new name

old_name="alex"
new_name="alex-johnson"

# Create new directory
mkdir -p ~/.openclaw/customers/$new_name/floreo

# Copy all entries (preserve timestamps)
cp -r ~/.openclaw/customers/$old_name/floreo/* \
      ~/.openclaw/customers/$new_name/floreo/

# Update the user file
echo "$new_name" > ~/.openclaw/customers/.floreo-user

echo "✅ Migrated from $old_name to $new_name"
echo "   Old data kept at: ~/.openclaw/customers/$old_name/"
echo "   New data at: ~/.openclaw/customers/$new_name/"
```

### Using Your Name in All Commands

Replace hardcoded names with dynamic lookup:

```bash
# Instead of:
# cat ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/15-04-26.md

# Use:
user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "user")
cat ~/.openclaw/customers/$user_name/floreo/domains/work/2026/04/15-04-26.md
```

**Helper function for scripts:**
```bash
#!/bin/bash
# Add this to your shell profile or scripts

get_floreo_user() {
  cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default"
}

# Usage in any script
user_name=$(get_floreo_user)
path="~/.openclaw/customers/$user_name/floreo"
```

### Multiple Users (Optional)

Floreo supports multiple users on the same system:

```bash
# Switch between users by changing the file
echo "work-profile" > ~/.openclaw/customers/.floreo-user
# All subsequent entries go to work-profile/

echo "personal" > ~/.openclaw/customers/.floreo-user
# Now entries go to personal/
```

### OpenClaw Integration

When using OpenClaw, you can dynamically reference your name:

```markdown
Read ~/.openclaw/customers/.floreo-user to get my user name

Then write an entry to ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/entry.md
```

Or simply:
```markdown
Write an entry to my Floreo work domain for today
```

OpenClaw can:
1. Read `~/.openclaw/customers/.floreo-user` to get your name
2. Use it in all subsequent operations
3. You can update it anytime with a simple write command

---

## Querying Entries (Native Tools)

### List All Entries

```bash
# Find all entry files
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -type f
```

### Search Content

```bash
# Search for specific text
grep -r "shipped" ~/.openclaw/customers/{user_name}/floreo/domains/

# Search with context
grep -r -B2 -A2 "project-x" ~/.openclaw/customers/{user_name}/floreo/domains/work/
```

### Filter by Date

```bash
# Entries from specific date
find ~/.openclaw/customers/{user_name}/floreo/domains -name "15-04-26.md"

# Entries from this month
find ~/.openclaw/customers/{user_name}/floreo/domains -path "*/2026/04/*.md"
```

### Count Entries

```bash
# Total entries
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" | wc -l

# By domain
for domain in work health learn relate create reflect; do
  count=$(find ~/.openclaw/customers/{user_name}/floreo/domains/$domain -name "*.md" 2>/dev/null | wc -l)
  echo "$domain: $count"
done
```

---

## Timeline Compilation (Native Tools)

### Compile All Entries (Includes Imported Entries Immediately)

All entries - whether created natively or imported - are immediately available in timeline:

```bash
# Concatenate all entries into timeline
cat $(find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" | sort) > /tmp/timeline.md

# This includes:
# - Original Floreo entries
# - Imported MEMORY.md entries (with original dates)
# - Imported document files
# - All entries use their ORIGINAL date (not import date)
```

### Timeline with Original Dates Preserved

```bash
# View timeline sorted by ORIGINAL entry date (not import date)
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -exec grep -H "^date:" {} \; | \
  sed 's/.*date: //' | \
  sort -t'-' -k3 -k2 -k1 | \
  head -20

# Result shows chronological order based on when entry was originally made
# NOT when it was imported into Floreo
```

### View Recent Activity

```bash
# Show entries from last 7 days
for file in $(find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -mtime -7 | sort); do
  echo "=== $file ==="
  cat "$file"
  echo
done
```

### Generate Stats

```bash
# Entries per domain
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -exec grep -l "^domain:" {} \; | \
  xargs grep "^domain:" | \
  sed 's/.*domain: //' | \
  sort | uniq -c | sort -rn
```

---

## Export Screening (Privacy)

### Manual Screening

When exporting, manually review entries based on privacy:

```bash
# List private entries (don't export)
grep -l "^privacy: private" ~/.openclaw/customers/{user_name}/floreo/domains -r

# List public entries (safe to export)
grep -l "^privacy: public" ~/.openclaw/customers/{user_name}/floreo/domains -r

# List internal entries (export with caution)
grep -l "^privacy: internal" ~/.openclaw/customers/{user_name}/floreo/domains -r
```

### Create Export

```bash
# Export public entries only
mkdir -p ~/.openclaw/customers/{user_name}/floreo/exports
grep -l "^privacy: public" ~/.openclaw/customers/{user_name}/floreo/domains -r | \
  xargs cat > ~/.openclaw/customers/{user_name}/floreo/exports/public-export-$(date +%Y%m%d).md
```

### Redact Sensitive Info

```bash
# Remove email addresses
sed -i '' 's/[a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]*\.[a-zA-Z]*/[EMAIL]/g' export.md

# Remove phone numbers
sed -i '' 's/[0-9]\{3\}-[0-9]\{3\}-[0-9]\{4\}/[PHONE]/g' export.md
```

---

## Reflection & Analysis (Native Tools)

### Weekly Review

```bash
# Compile this week's entries
week_start=$(date -v-sun -v-7d +%d-%m-%y)
week_end=$(date -v-sat +%d-%m-%y)

echo "# Weekly Reflection: $week_start to $week_end" > /tmp/weekly.md
echo "" >> /tmp/weekly.md

for domain in work health learn relate create reflect; do
  echo "## $domain" >> /tmp/weekly.md
  find ~/.openclaw/customers/{user_name}/floreo/domains/$domain -name "*.md" -mtime -7 -exec cat {} \; >> /tmp/weekly.md
  echo "" >> /tmp/weekly.md
done
```

### Search by Tag

```bash
# Find all entries with specific tag
grep -r "tags:.*project-x" ~/.openclaw/customers/{user_name}/floreo/domains/
```

### Generate Word Cloud

```bash
# Extract all content (no frontmatter)
grep -v "^---$" ~/.openclaw/customers/{user_name}/floreo/domains -r | \
  grep -v "^[a-z_]*:" | \
  tr ' ' '\\n' | \
  sort | uniq -c | sort -rn | head -30
```

---

## Integration with MEMORY.md

### Sync to Memory

```
Read ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/15-04-26.md
Then append a summary to ~/.openclaw/customers/{user_name}/memory/15-04-26.md
```

### Import from Memory

```
Read ~/.openclaw/customers/{user_name}/memory/14-04-26.md
Parse entries and write them to appropriate Floreo domain files with privacy: private
```

---

## Automation with Cron

### Daily Entry Prompt

```bash
# Add to crontab
0 21 * * * echo "What did you work on today?" >> ~/.openclaw/customers/{user_name}/floreo/.daily-prompt
```

### Weekly Summary

```bash
# Every Sunday at 8pm
0 20 * * 0 cd ~/.openclaw/customers/{user_name}/floreo && ./generate-weekly-reflection.sh
```

---

## Tips & Best Practices

### 1. Use Consistent Date Formats

Always use `DD-MM-YY` for entry dates and `YYYY/MM/DD` for directory structure.

### 2. Unique Entry IDs

Generate with: `FE-$(date +%Y%m%d)-$(openssl rand -hex 3 | tr '[:lower:]' '[:upper:]')`

### 3. Tag Consistently

Use lowercase, hyphenated tags: `deep-work`, `client-meeting`, `bug-fix`

### 4. Metrics Matter

Include quantifiable metrics for trend analysis:
- `focus: 4` (hours)
- `commits: 5`
- `energy: 8` (1-10 scale)
- `pages: 30`

### 5. Privacy First

When in doubt, use `privacy: internal`. You can always make it public later.

### 6. Regular Reviews

Use `find -mtime -7` to review weekly activity.

---

## Import from Historical Files

Import existing notes, journals, or OpenClaw memory into Floreo format with **immediate timeline integration**.

### Import Principles

1. **Preserve Original Dates** - Entries keep their original date/timestamp
2. **Immediate Timeline Integration** - Available in timeline right after import
3. **User Consent for Domain/Privacy** - You review and approve classifications
4. **Idempotent** - Can re-run without duplicates (based on entry_id)

### Import from MEMORY.md with Consent

```markdown
Step 1: Read ~/.openclaw/customers/{user_name}/memory/14-04-26.md

Step 2: Parse and present for approval:

Found 5 entries in memory file:
┌─────────────────────────────────────────────────────────┐
│ Entry 1 | Date: 14-04-26 | Original timestamp preserved │
├─────────────────────────────────────────────────────────┤
│ Content: "Shipped v0.6.8 to production..."              │
│ Suggested Domain: work [💼]                             │
│ Suggested Privacy: internal [👁️]                        │
│ Tags: imported, memory                                  │
├─────────────────────────────────────────────────────────┤
│ [✓ Approve] [✗ Skip] [✎ Edit Domain]                  │
└─────────────────────────────────────────────────────────┘

Entry 2 | Date: 14-04-26
Content: "Morning run 5k..."
Suggested Domain: health [💪]
Suggested Privacy: private [🔒]
[✓ Approve] [✗ Skip]

... (show all 5 entries)

Step 3: Upon approval, write immediately to:
~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/14-04-26.md
~/.openclaw/customers/{user_name}/floreo/domains/health/2026/04/14-04-26.md

Step 4: Verify timeline integration:
Run: find ~/.openclaw/customers/{user_name}/floreo/domains -name "14-04-26.md"
Result: Should show newly imported entries
```

### Import with Immediate Timeline Preview

```bash
#!/bin/bash
# import-with-preview.sh - Interactive import with consent

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
source_file="$1"

if [ ! -f "$source_file" ]; then
  echo "❌ File not found: $source_file"
  exit 1
fi

echo "📥 Import Preview"
echo "=================="
echo "Source: $source_file"
echo ""

# Parse and show preview
entry_count=0
while IFS= read -r line; do
  if [[ "$line" =~ ^##?[[:space:]] ]]; then
    entry_count=$((entry_count + 1))
    echo ""
    echo "Entry $entry_count:"
    echo "  Date: $(echo "$line" | grep -oE '[0-9]{2,4}-[0-9]{2}-[0-9]{2,4}' || echo 'unknown')"
    echo "  Preview: ${line:0:60}..."
    
    # Suggest domain
    content_lower=$(echo "$line" | tr '[:upper:]' '[:lower:]')
    if [[ "$content_lower" =~ (work|code|shipped|project|meeting) ]]; then
      suggested_domain="work"
      emoji="💼"
    elif [[ "$content_lower" =~ (run|gym|health|sleep|exercise) ]]; then
      suggested_domain="health"
      emoji="💪"
    elif [[ "$content_lower" =~ (read|learn|book|course|study) ]]; then
      suggested_domain="learn"
      emoji="📚"
    else
      suggested_domain="reflect"
      emoji="🧘"
    fi
    
    echo "  Suggested: $emoji $suggested_domain"
    echo ""
  fi
done < "$source_file"

echo "Total entries found: $entry_count"
echo ""
read -p "Proceed with import? (y/n): " confirm

if [[ "$confirm" == "y" ]]; then
  echo "✅ Importing with original dates preserved..."
  
  # Import logic here - preserve dates, write to appropriate domain files
  # Each entry gets entry_id: FE-{original-date}-{random}
  # Original timestamp preserved in timestamp field
  # Date field uses original date (not today)
  
  echo "✅ Import complete. Entries now in timeline."
  echo ""
  echo "Verify with:"
  echo "  find ~/.openclaw/customers/$user_name/floreo/domains -name '*.md' | xargs ls -la"
else
  echo "❌ Import cancelled."
fi
```

### Import from Markdown Files

```bash
# Import all markdown files from a directory
for file in ~/Documents/journal/*.md; do
  # Extract date from filename (e.g., 2026-04-15.md)
  date_str=$(basename "$file" .md | sed 's/-/ /g')
  
  # Read content and classify
  content=$(cat "$file")
  
  # Determine domain based on content keywords
  if echo "$content" | grep -qi "work\|job\|project\|code"; then
    domain="work"
  elif echo "$content" | grep -qi "run\|gym\|sleep\|health"; then
    domain="health"
  elif echo "$content" | grep -qi "read\|learn\|book\|course"; then
    domain="learn"
  else
    domain="reflect"
  fi
  
  # Create Floreo entry
  target_dir="~/.openclaw/customers/{user_name}/floreo/domains/$domain/$(date +%Y)/$(date +%m)"
  mkdir -p "$target_dir"
  
  cat >> "$target_dir/$(date +%d-%m-%y).md" << EOF
---
type: entry
entry_id: FE-$(date +%Y%m%d)-$(openssl rand -hex 3 | tr '[:lower:]' '[:upper:]')
domain: $domain
date: $(date +%d-%m-%y)
day: $(date +%j)
timestamp: $(date -Iseconds)
privacy: internal
tags: imported
---
$content
EOF
done
```

### Import from JSON/CSV

```bash
# Import from JSON export (e.g., from other apps)
# JSON format: [{"date": "...", "content": "...", "domain": "..."}]

jq -c '.[]' export.json | while read entry; do
  date_str=$(echo "$entry" | jq -r '.date')
  content=$(echo "$entry" | jq -r '.content')
  domain=$(echo "$entry" | jq -r '.domain // "reflect"')
  
  # Parse date and create entry
  # ... similar to markdown import
done
```

### Bulk Import with Immediate Timeline Integration

```markdown
Read all files in ~/Documents/personal-notes/ with extension .md

For each file:
1. Extract ORIGINAL date from filename or content (preserve historical accuracy)
2. Analyze content to determine domain
3. Create Floreo entry with:
   - entry_id: FE-{original-date}-{hash} (idempotent - re-running won't duplicate)
   - Original timestamp preserved
   - Original date in date field (NOT today's date)
   - Domain as suggested
   - Privacy: private (for imported personal notes)
   - Tags: imported, historical
4. Write to: ~/.openclaw/customers/{user_name}/floreo/domains/{domain}/{original-year}/{original-month}/{original-date}.md

After import - IMMEDIATE VERIFICATION:
Run shell: find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -path "*/2026/04/*" | wc -l
Expected: Previous count + newly imported entries

Report:
- Total files processed
- Entries created by domain
- Date range of imported entries (oldest to newest)
- Timeline verification: All entries now searchable
- Any errors or skipped files
```

### Post-Import Timeline Verification

```bash
#!/bin/bash
# verify-import.sh - Verify imported entries are in timeline

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

echo "📊 Post-Import Timeline Verification"
echo "===================================="
echo ""

# Count total entries
total=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" | wc -l)
echo "Total entries in Floreo: $total"
echo ""

# Show date range of all entries
echo "Date range in timeline:"
find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" | \
  grep -oE '[0-9]{2}-[0-9]{2}-[0-9]{2}' | \
  sort | \
  uniq | \
  head -5
echo "  ... (showing first 5 unique dates)"
echo ""

# Check for imported entries specifically
echo "Imported entries (tagged with 'imported'):"
grep -r "tags:.*imported" ~/.openclaw/customers/$user_name/floreo/domains/ | wc -l
echo ""

# Sample recent entries
echo "Most recent entries:"
ls -lt ~/.openclaw/customers/$user_name/floreo/domains/*/*/*/*.md 2>/dev/null | head -5 | awk '{print $6, $7, $8, $9}'
echo ""

echo "✅ Timeline integration verified!"
echo "   All imported entries available for timeline, reports, and search."
```

### Re-Import Protection (Idempotent)

Entries are deduplicated by `entry_id` which includes the original date:

```bash
# Entry ID format: FE-{original-date}-{hash}
# Example: FE-20260414-A1B2C3

# If you re-import the same file:
# - Entries with same entry_id will be skipped
# - New entries (different dates) will be added
# - No duplicates created
```

### Immediate Timeline Query After Import

```markdown
Right after import, query the timeline:

"Show me all entries from April 2026"
→ Should include both:
   - Original Floreo entries
   - Newly imported entries (with original April dates)

"Generate a report for last week"
→ Should include imported entries if they fall in that date range

"Search for 'shipped' in timeline"
→ Should find imported entries containing that word
```

---

## 🧬 Compound Metrics System

Track metrics that compound over time — small daily improvements create exponential long-term results.

### Compound Metrics Schema

Each domain supports compound metrics that build upon each other:

```yaml
# Work domain compound metrics
metrics:
  # Base metrics (daily inputs)
  deep_work_hours: 4
  commits: 5
  prs_merged: 2
  blockers_identified: 1
  
  # Compound metrics (calculated)
  focus_streak: 3           # Consecutive days with deep_work >= 3
  weekly_output: 23         # Rolling 7-day sum
  velocity_trend: 1.15      # Output vs previous week (15% up)
  
# Health domain compound metrics
metrics:
  # Base metrics
  sleep_hours: 7.5
  exercise_minutes: 45
  energy_level: 8
  
  # Compound metrics
  recovery_score: 85        # Sleep quality + rest days
  vitality_index: 7.8       # Weighted: sleep*0.4 + energy*0.4 + exercise*0.2
  wellness_streak: 12       # Days meeting health goals
```

### Native Tool: Calculate Compound Metrics

```bash
#!/bin/bash
# calculate-compound-metrics.sh — Calculate compound metrics for a customer

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
date_str=$(date +%d-%m-%y)
date_iso=$(date +%Y-%m-%d)

# 1. Calculate focus streak
calculate_focus_streak() {
  local current_streak=0
  local check_date=$(date +%Y-%m-%d)
  
  for i in {0..30}; do
    local file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
    local year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
    local month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
    
    local entry_file="~/.openclaw/customers/$user_name/floreo/domains/work/$year/$month/$file_date.md"
    
    if [ -f "$entry_file" ]; then
      local deep_work=$(grep "deep_work:" "$entry_file" | sed 's/.*deep_work://' | tr -d ' ')
      if [ -n "$deep_work" ] && [ "$deep_work" -ge 3 ] 2>/dev/null; then
        current_streak=$((current_streak + 1))
      else
        break
      fi
    else
      break
    fi
  done
  
  echo "$current_streak"
}

# 2. Calculate weekly rolling sum
calculate_weekly_output() {
  local total=0
  
  for i in {0..6}; do
    local file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
    local year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
    local month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
    
    local entry_file="~/.openclaw/customers/$user_name/floreo/domains/work/$year/$month/$file_date.md"
    
    if [ -f "$entry_file" ]; then
      local commits=$(grep "commits:" "$entry_file" | sed 's/.*commits://' | tr -d ' ')
      total=$((total + ${commits:-0}))
    fi
  done
  
  echo "$total"
}

# 3. Calculate velocity trend (vs previous week)
calculate_velocity_trend() {
  local this_week=$(calculate_weekly_output)
  
  local last_week_total=0
  for i in {7..13}; do
    local file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
    local year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
    local month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
    
    local entry_file="~/.openclaw/customers/$user_name/floreo/domains/work/$year/$month/$file_date.md"
    
    if [ -f "$entry_file" ]; then
      local commits=$(grep "commits:" "$entry_file" | sed 's/.*commits://' | tr -d ' ')
      last_week_total=$((last_week_total + ${commits:-0}))
    fi
  done
  
  if [ $last_week_total -gt 0 ]; then
    local trend=$(echo "scale=2; $this_week / $last_week_total" | bc)
    echo "$trend"
  else
    echo "1.0"
  fi
}

# Run calculations
echo "Focus Streak: $(calculate_focus_streak) days"
echo "Weekly Output: $(calculate_weekly_output) commits"
echo "Velocity Trend: $(calculate_velocity_trend)x"
```

---

## 🔗 Cross-Domain Correlation Analysis

Discover hidden patterns between your work, health, learning, relationships, and creativity.

### Correlation Methodology

```bash
#!/bin/bash
# correlation-analysis.sh — Find patterns across domains

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
days_back=30

echo "🔍 Cross-Domain Correlation Analysis"
echo "====================================="
echo "Analyzing last $days_back days..."
echo ""

# Collect data points
declare -A work_output
declare -A health_energy
declare -A exercise_days
declare -A sleep_quality

# 1. Gather work metrics
for i in $(seq 0 $days_back); do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  work_file="~/.openclaw/customers/$user_name/floreo/domains/work/$year/$month/$file_date.md"
  if [ -f "$work_file" ]; then
    commits=$(grep "commits:" "$work_file" 2>/dev/null | sed 's/.*commits://' | tr -d ' ')
    deep_work=$(grep "deep_work:" "$work_file" 2>/dev/null | sed 's/.*deep_work://' | tr -d ' ')
    work_output[$i]=$(( ${commits:-0} + ${deep_work:-0} * 2 ))
  else
    work_output[$i]=0
  fi
done

# 2. Gather health metrics
for i in $(seq 0 $days_back); do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$file_date.md"
  if [ -f "$health_file" ]; then
    energy=$(grep "energy_level:" "$health_file" 2>/dev/null | sed 's/.*energy_level://' | tr -d ' ')
    exercise=$(grep "exercise:" "$health_file" 2>/dev/null | grep -o '[0-9]*')
    sleep=$(grep "sleep_hours:" "$health_file" 2>/dev/null | sed 's/.*sleep_hours://' | tr -d ' ')
    
    health_energy[$i]=${energy:-0}
    exercise_days[$i]=$([ -n "$exercise" ] && [ "$exercise" -gt 0 ] && echo 1 || echo 0)
    sleep_quality[$i]=${sleep:-0}
  else
    health_energy[$i]=0
    exercise_days[$i]=0
    sleep_quality[$i]=0
  fi
done

# 3. Calculate correlations
echo "📊 CORRELATION FINDINGS"
echo ""

# Work output on exercise days vs non-exercise days
exercise_work_total=0
exercise_days_count=0
no_exercise_work_total=0
no_exercise_days_count=0

for i in $(seq 0 $days_back); do
  if [ "${exercise_days[$i]}" -eq 1 ]; then
    exercise_work_total=$((exercise_work_total + ${work_output[$i]}))
    exercise_days_count=$((exercise_days_count + 1))
  else
    no_exercise_work_total=$((no_exercise_work_total + ${work_output[$i]}))
    no_exercise_days_count=$((no_exercise_days_count + 1))
  fi
done

if [ $exercise_days_count -gt 0 ] && [ $no_exercise_days_count -gt 0 ]; then
  exercise_avg=$(echo "scale=1; $exercise_work_total / $exercise_days_count" | bc)
  no_exercise_avg=$(echo "scale=1; $no_exercise_work_total / $no_exercise_days_count" | bc)
  
  if [ $no_exercise_avg -gt 0 ]; then
    improvement=$(echo "scale=0; (($exercise_avg - $no_exercise_avg) / $no_exercise_avg) * 100" | bc)
    echo "💪 Exercise → Productivity"
    echo "   Days WITH exercise: $exercise_avg output avg"
    echo "   Days WITHOUT exercise: $no_exercise_avg output avg"
    echo "   → ${improvement}% more productive on exercise days"
    echo ""
  fi
fi

# Energy correlation with work output
high_energy_days=0
high_energy_work=0
low_energy_days=0
low_energy_work=0

for i in $(seq 0 $days_back); do
  if [ "${health_energy[$i]}" -ge 7 ] 2>/dev/null; then
    high_energy_days=$((high_energy_days + 1))
    high_energy_work=$((high_energy_work + ${work_output[$i]}))
  elif [ "${health_energy[$i]}" -gt 0 ] 2>/dev/null; then
    low_energy_days=$((low_energy_days + 1))
    low_energy_work=$((low_energy_work + ${work_output[$i]}))
  fi
done

if [ $high_energy_days -gt 0 ] && [ $low_energy_days -gt 0 ]; then
  high_avg=$(echo "scale=1; $high_energy_work / $high_energy_days" | bc)
  low_avg=$(echo "scale=1; $low_energy_work / $low_energy_days" | bc)
  
  echo "⚡ Energy Level → Output"
  echo "   High energy days (7+): $high_avg output avg"
  echo "   Low energy days (<7): $low_avg output avg"
  echo ""
fi

# Sleep correlation
well_rested_days=0
well_rested_work=0
tired_days=0
tired_work=0

for i in $(seq 0 $days_back); do
  sleep_val=$(echo "${sleep_quality[$i]}" | cut -d. -f1)
  if [ "$sleep_val" -ge 7 ] 2>/dev/null; then
    well_rested_days=$((well_rested_days + 1))
    well_rested_work=$((well_rested_work + ${work_output[$i]}))
  elif [ "$sleep_val" -gt 0 ] 2>/dev/null; then
    tired_days=$((tired_days + 1))
    tired_work=$((tired_work + ${work_output[$i]}))
  fi
done

if [ $well_rested_days -gt 0 ] && [ $tired_days -gt 0 ]; then
  rested_avg=$(echo "scale=1; $well_rested_work / $well_rested_days" | bc)
  tired_avg=$(echo "scale=1; $tired_work / $tired_days" | bc)
  
  echo "😴 Sleep Quality → Performance"
  echo "   7+ hours sleep: $rested_avg output avg"
  echo "   <7 hours sleep: $tired_avg output avg"
  echo ""
fi

echo "✅ Analysis complete"
```

### Using OpenClaw Native Tools for Correlation

```markdown
Run shell command: ~/.openclaw/customers/{user_name}/floreo/scripts/correlation-analysis.sh

Read the correlation report and present findings:
"Based on your last 30 days:
- You're 40% more productive on days you exercise
- High energy days correlate with 2x more deep work
- 7+ hours sleep → 35% better output

💡 RECOMMENDATION: Prioritize morning exercise to compound work productivity"
```

---

## 💡 Automated Insight Generation

Generate recommendations based on your patterns — all using native OpenClaw tools you run manually.

> **Note**: Run manually or schedule via cron/heartbeat. Autonomous watchers available via opt-in configuration.

### Insight Engine (Native Tools Only)

```bash
#!/bin/bash
# insight-engine.sh — Generate personalized recommendations

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
insight_file="~/.openclaw/customers/$user_name/floreo/insights/$(date +%Y-%m-%d)-insights.md"

{
echo "# 🧠 Floreo Insights — $(date +%B\ %d,\ %Y)"
echo ""
echo "Generated by analyzing your last 30 days of entries."
echo ""

# Find optimal work patterns
echo "## 🎯 Optimal Work Patterns"
echo ""

# Check day-of-week patterns
declare -A dow_output
declare -A dow_count

for i in {0..30}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  dow=$(date -v-${i}d +%u 2>/dev/null || date -d "${i} days ago" +%u)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  work_file="~/.openclaw/customers/$user_name/floreo/domains/work/$year/$month/$file_date.md"
  
  if [ -f "$work_file" ]; then
    commits=$(grep "commits:" "$work_file" 2>/dev/null | sed 's/.*commits://' | tr -d ' ')
    output=${commits:-0}
    dow_output[$dow]=$((${dow_output[$dow]:-0} + output))
    dow_count[$dow]=$((${dow_count[$dow]:-0} + 1))
  fi
done

# Find best day
best_dow=1
best_avg=0
for dow in 1 2 3 4 5 6 7; do
  if [ ${dow_count[$dow]:-0} -gt 0 ]; then
    avg=$(echo "scale=1; ${dow_output[$dow]} / ${dow_count[$dow]}" | bc)
    if [ $(echo "$avg > $best_avg" | bc) -eq 1 ]; then
      best_avg=$avg
      best_dow=$dow
    fi
  fi
done

dow_names=("" "Monday" "Tuesday" "Wednesday" "Thursday" "Friday" "Saturday" "Sunday")
echo "**Best work day:** ${dow_names[$best_dow]} (avg ${best_avg} commits)"
echo ""

# Detect blockers
echo "## ⚠️ Blockers & Friction"
echo ""
blocker_count=$(grep -r "blocked\|stuck\|waiting" ~/.openclaw/customers/$user_name/floreo/domains/work --include="*.md" 2>/dev/null | wc -l)
if [ $blocker_count -gt 5 ]; then
  echo "- You mentioned blockers $blocker_count times in the last month"
  echo "- Consider: Morning standups, async communication, or pairing sessions"
fi
echo ""

# Learning momentum
echo "## 📚 Learning Momentum"
echo ""
learn_count=$(find ~/.openclaw/customers/$user_name/floreo/domains/learn -name "*.md" -mtime -30 2>/dev/null | wc -l)
if [ $learn_count -lt 5 ]; then
  echo "- Only $learn_count learning entries in 30 days"
  echo "- 💡 TIP: Schedule 30min learning blocks on ${dow_names[$best_dow]} mornings"
else
  echo "- Strong learning habit: $learn_count entries in 30 days 🎉"
fi
echo ""

# Relationship check
echo "## 🤝 Relationship Health"
echo ""
relate_count=$(find ~/.openclaw/customers/$user_name/floreo/domains/relate -name "*.md" -mtime -30 2>/dev/null | wc -l)
if [ $relate_count -lt 3 ]; then
  echo "- Only $relate_count social entries — consider reaching out this week"
else
  echo "- Good social investment: $relate_count meaningful interactions"
fi
echo ""

# Compound recommendation
echo "## 🚀 Compound Recommendation"
echo ""
echo "Based on your patterns, focus on this ONE thing this week:"
echo ""

# Pick top recommendation
if [ $blocker_count -gt 5 ]; then
  echo "**→ Unblock your mornings.** Your data shows you get stuck frequently."
  echo "   Try: Pre-block 2 hours of focused work before checking messages."
elif [ ${dow_count[1]:-0} -lt 2 ]; then
  echo "**→ Protect your Mondays.** Start the week with your most important work."
  echo "   You have fewer entries on Mondays — establish a strong opening ritual."
else
  echo "**→ Maintain momentum.** You're on a good trajectory."
  echo "   Keep doing what's working, and consider adding one new healthy habit."
fi

echo ""
echo "---"
echo "*Insights generated: $(date)*"

} > "$insight_file"

echo "✅ Insights saved to: $insight_file"
```

### OpenClaw Usage

```markdown
Generate insights for my Floreo data:
1. Run shell: ~/.openclaw/customers/{user_name}/floreo/scripts/insight-engine.sh
2. Read the generated insight file
3. Present findings with actionable recommendations
```

---

## 📈 Momentum & Streak Tracking

Track compounding momentum across all domains.

### Streak Calculation (Native)

```bash
#!/bin/bash
# streak-tracker.sh — Calculate current streaks

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

echo "🔥 FLOREO MOMENTUM DASHBOARD"
echo "============================="
echo ""

# Function: Calculate streak for a domain
calculate_streak() {
  local domain=$1
  local streak=0
  
  for i in {0..365}; do
    file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
    year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
    month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
    
    entry_file="~/.openclaw/customers/$user_name/floreo/domains/$domain/$year/$month/$file_date.md"
    
    if [ -f "$entry_file" ]; then
      streak=$((streak + 1))
    else
      break
    fi
  done
  
  echo "$streak"
}

# Calculate streaks for each domain
echo "CURRENT STREAKS:"
echo ""

work_streak=$(calculate_streak "work")
echo "  💼 Work: $work_streak days"

health_streak=$(calculate_streak "health")
echo "  💪 Health: $health_streak days"

learn_streak=$(calculate_streak "learn")
echo "  📚 Learning: $learn_streak days"

relate_streak=$(calculate_streak "relate")
echo "  🤝 Relationships: $relate_streak days"

reflect_streak=$(calculate_streak "reflect")
echo "  🧘 Reflection: $reflect_streak days"

echo ""

# Calculate overall consistency
all_domains_days=0
for i in {0..30}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  domains_logged=0
  for domain in work health learn relate reflect; do
    if [ -f "~/.openclaw/customers/$user_name/floreo/domains/$domain/$year/$month/$file_date.md" ]; then
      domains_logged=$((domains_logged + 1))
    fi
  done
  
  if [ $domains_logged -ge 3 ]; then
    all_domains_days=$((all_domains_days + 1))
  fi
done

echo "BALANCED LIFE SCORE: $all_domains_days/31 days with 3+ domains"
echo ""

# Compounding benefits
echo "COMPOUNDING BENEFITS:"
if [ $work_streak -ge 7 ]; then
  echo "  ✅ Work: 7+ day streak → Deep work capacity increasing"
fi
if [ $health_streak -ge 14 ]; then
  echo "  ✅ Health: 14+ day streak → Energy baseline elevated"
fi
if [ $learn_streak -ge 30 ]; then
  echo "  ✅ Learning: 30+ day streak → Knowledge network expanding"
fi
if [ $all_domains_days -ge 20 ]; then
  echo "  🌟 BALANCED: 20+ days with multi-domain attention"
fi
```

---

## 🤖 Autonomous Analysis Setup

Set up automated analysis using cron or OpenClaw heartbeat. Configure what runs automatically.

### Daily Autonomous Analysis

```bash
#!/bin/bash
# daily-analysis.sh — Scheduled analysis
# Runs automatically if enabled via cron or heartbeat

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

# 1. Calculate today's compound metrics
# 2. Update streak counters
# 3. Check for correlations
# 4. Generate insight if patterns detected

# Auto-enable via cron:
# 0 22 * * * ~/.openclaw/customers/{user_name}/floreo/scripts/daily-analysis.sh

# Or via OpenClaw heartbeat (automated)
```

### Weekly Report (Autonomous or On-Demand)

```bash
# Generate report now (manual)
~/.openclaw/customers/{user_name}/floreo/scripts/generate-weekly-report.sh

# Or schedule (autonomous)
# 0 20 * * 0 ~/.openclaw/customers/{user_name}/floreo/scripts/generate-weekly-report.sh
```

**Features in weekly report:**
- Compound metrics trends
- Cross-domain correlations
- Personalized recommendations
- Momentum visualization
- Streak status
- Benefits tracker

---

## 🧬 Longevity & Healthspan Tracking

Track metrics that predict and extend your healthspan and lifespan — all using native OpenClaw tools.

### Longevity Metrics Schema

Add longevity-specific metrics to your health entries:

```yaml
# Health entry with longevity metrics
metrics:
  # Basic biomarkers
  sleep_hours: 7.5
  sleep_quality: 8          # 1-10 subjective
  resting_hr: 58            # Morning resting heart rate
  hrv: 45                   # Heart rate variability (ms)
  
  # Exercise & VO2 proxy
  exercise_minutes: 45
  exercise_zone2: 30        # Zone 2 cardio minutes
  exercise_zone4: 5         # Zone 4 HIIT minutes
  steps: 8500
  
  # Nutrition & fasting
  fasting_hours: 14         # Intermittent fasting window
  protein_grams: 95         # Daily protein intake
  sugar_grams: 25           # Added sugar
  
  # Stress & recovery
  cortisol_proxy: 3         # 1-10 stress level
  mindfulness_min: 10       # Meditation/mindfulness
  
  # Longevity compound metrics (calculated)
  biological_age_delta: -2  # Years younger than chronological
  healthspan_score: 82      # 0-100 composite score
  allostatic_load: 3.2      # Cumulative stress index
```

### 🩺 Healthspan Score Calculator (Native)

```bash
#!/bin/bash
# healthspan-score.sh — Calculate composite longevity score

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
date_str=$(date +%d-%m-%y)
year=$(date +%Y)
month=$(date +%m)

health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$date_str.md"

if [ ! -f "$health_file" ]; then
  echo "No health entry for today"
  exit 0
fi

# Extract metrics
sleep=$(grep "sleep_hours:" "$health_file" | sed 's/.*sleep_hours://' | tr -d ' ')
resting_hr=$(grep "resting_hr:" "$health_file" | sed 's/.*resting_hr://' | tr -d ' ')
hrv=$(grep "hrv:" "$health_file" | sed 's/.*hrv://' | tr -d ' ')
zone2=$(grep "exercise_zone2:" "$health_file" | sed 's/.*exercise_zone2://' | tr -d ' ')
fasting=$(grep "fasting_hours:" "$health_file" | sed 's/.*fasting_hours://' | tr -d ' ')
protein=$(grep "protein_grams:" "$health_file" | sed 's/.*protein_grams://' | tr -d ' ')
sugar=$(grep "sugar_grams:" "$health_file" | sed 's/.*sugar_grams://' | tr -d ' ')
stress=$(grep "cortisol_proxy:" "$health_file" | sed 's/.*cortisol_proxy://' | tr -d ' ')
mindfulness=$(grep "mindfulness_min:" "$health_file" | sed 's/.*mindfulness_min://' | tr -d ' ')

# Calculate components (each 0-100)
sleep_score=0
if [ -n "$sleep" ]; then
  if (( $(echo "$sleep >= 7 && $sleep <= 9" | bc -l) )); then
    sleep_score=100
  elif (( $(echo "$sleep >= 6" | bc -l) )); then
    sleep_score=70
  else
    sleep_score=40
  fi
fi

hr_score=0
if [ -n "$resting_hr" ]; then
  if [ "$resting_hr" -le 55 ]; then
    hr_score=100
  elif [ "$resting_hr" -le 65 ]; then
    hr_score=80
  elif [ "$resting_hr" -le 75 ]; then
    hr_score=60
  else
    hr_score=30
  fi
fi

exercise_score=0
if [ -n "$zone2" ]; then
  if [ "$zone2" -ge 150 ]; then
    exercise_score=100
  elif [ "$zone2" -ge 120 ]; then
    exercise_score=80
  elif [ "$zone2" -ge 90 ]; then
    exercise_score=60
  else
    exercise_score=40
  fi
fi

fasting_score=0
if [ -n "$fasting" ]; then
  if [ "$fasting" -ge 16 ]; then
    fasting_score=100
  elif [ "$fasting" -ge 14 ]; then
    fasting_score=80
  elif [ "$fasting" -ge 12 ]; then
    fasting_score=60
  else
    fasting_score=30
  fi
fi

nutrition_score=0
if [ -n "$protein" ] && [ -n "$sugar" ]; then
  protein_score=0
  if [ "$protein" -ge 100 ]; then
    protein_score=100
  elif [ "$protein" -ge 80 ]; then
    protein_score=80
  else
    protein_score=50
  fi
  
  sugar_score=0
  if [ "$sugar" -le 25 ]; then
    sugar_score=100
  elif [ "$sugar" -le 40 ]; then
    sugar_score=70
  else
    sugar_score=30
  fi
  
  nutrition_score=$(( (protein_score + sugar_score) / 2 ))
fi

stress_score=0
if [ -n "$stress" ]; then
  if [ "$stress" -le 3 ]; then
    stress_score=100
  elif [ "$stress" -le 5 ]; then
    stress_score=70
  elif [ "$stress" -le 7 ]; then
    stress_score=40
  else
    stress_score=20
  fi
fi

# Calculate weighted composite
total=$((sleep_score * 25 + hr_score * 15 + exercise_score * 25 + 
         fasting_score * 10 + nutrition_score * 15 + stress_score * 10))
healthspan_score=$((total / 100))

# Calculate biological age estimate (simplified)
chronological_age=35  # User's age - should be configurable
biological_offset=0
if [ $healthspan_score -ge 90 ]; then
  biological_offset=-5
elif [ $healthspan_score -ge 80 ]; then
  biological_offset=-2
elif [ $healthspan_score -ge 70 ]; then
  biological_offset=0
elif [ $healthspan_score -ge 60 ]; then
  biological_offset=2
else
  biological_offset=5
fi

echo "╔════════════════════════════════════════╗"
echo "║     🧬 LONGEVITY SCORECARD             ║"
echo "╠════════════════════════════════════════╣"
printf "║  Healthspan Score: %3d/100            ║\n" $healthspan_score
echo "╠════════════════════════════════════════╣"
echo "║  Components:                           ║"
printf "║    😴 Sleep:        %3d/100           ║\n" $sleep_score
printf "║    ❤️  Heart Health: %3d/100           ║\n" $hr_score
printf "║    🏃 Exercise:     %3d/100           ║\n" $exercise_score
printf "║    🕐 Fasting:      %3d/100           ║\n" $fasting_score
printf "║    🥗 Nutrition:    %3d/100           ║\n" $nutrition_score
printf "║    🧘 Stress Mgmt:  %3d/100           ║\n" $stress_score
echo "╠════════════════════════════════════════╣"
printf "║  Biological Age:   %d (Δ %d years)     ║\n" $((chronological_age + biological_offset)) $biological_offset
echo "╚════════════════════════════════════════╝"
```

### 📊 Compression of Morbidity Index

Track how long you stay healthy vs. total lifespan — the key longevity metric.

```bash
#!/bin/bash
# morbidity-compression.sh — Track healthspan vs lifespan

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

# Calculate healthy days in last 90 days
healthy_days=0
morbidity_risk_days=0

for i in {0..89}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$file_date.md"
  
  if [ -f "$health_file" ]; then
    # Check for morbidity risk markers
    sleep=$(grep "sleep_hours:" "$health_file" | sed 's/.*sleep_hours://' | tr -d ' ')
    stress=$(grep "cortisol_proxy:" "$health_file" | sed 's/.*cortisol_proxy://' | tr -d ' ')
    exercise=$(grep "exercise_zone2:" "$health_file" | sed 's/.*exercise_zone2://' | tr -d ' ')
    
    # Score this day
    day_risk=0
    
    if [ -n "$sleep" ] && (( $(echo "$sleep < 6" | bc -l) )); then
      day_risk=$((day_risk + 2))
    fi
    
    if [ -n "$stress" ] && [ "$stress" -ge 7 ]; then
      day_risk=$((day_risk + 2))
    fi
    
    if [ -n "$exercise" ] && [ "$exercise" -lt 15 ]; then
      day_risk=$((day_risk + 1))
    fi
    
    if [ $day_risk -le 2 ]; then
      healthy_days=$((healthy_days + 1))
    else
      morbidity_risk_days=$((morbidity_risk_days + 1))
    fi
  fi
done

# Calculate compression ratio
total_days=$((healthy_days + morbidity_risk_days))
if [ $total_days -gt 0 ]; then
  compression_ratio=$(echo "scale=2; $healthy_days / $total_days * 100" | bc)
  
  echo "📊 COMPRESSION OF MORBIDITY"
  echo "============================"
  echo ""
  echo "Last 90 days:"
  echo "  ✅ Healthy days:     $healthy_days"
  echo "  ⚠️  Risk days:        $morbidity_risk_days"
  echo ""
  echo "  Healthspan ratio: ${compression_ratio}%"
  echo ""
  
  if (( $(echo "$compression_ratio >= 90" | bc -l) )); then
    echo "  🌟 EXCELLENT: High healthspan compression"
    echo "     Projected: Long healthy life with minimal morbidity"
  elif (( $(echo "$compression_ratio >= 75" | bc -l) )); then
    echo "  ✅ GOOD: Solid healthspan"
    echo "     Opportunity: Focus on sleep consistency"
  else
    echo "  ⚠️  NEEDS ATTENTION: Morbidity risk elevated"
    echo "     Action: Prioritize sleep + stress + exercise"
  fi
fi
```

### 🏃 Exercise Longevity Zones

Track exercise by longevity-optimized heart rate zones.

```bash
#!/bin/bash
# exercise-zones.sh — Calculate Zone 2 and Zone 4 minutes

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
date_str=$(date +%d-%m-%y)

# Calculate zones based on age (220 - age formula)
age=35
max_hr=$((220 - age))
zone2_min=$((max_hr * 60 / 100))   # 60-70% max HR
zone2_max=$((max_hr * 70 / 100))
zone4_min=$((max_hr * 80 / 100))   # 80-90% max HR
zone4_max=$((max_hr * 90 / 100))

echo "🏃 LONGEVITY EXERCISE ZONES"
echo "==========================="
echo ""
echo "Age: $age"
echo "Max HR: $max_hr bpm"
echo ""
echo "Zone 2 (Mitochondrial Health): $zone2_min-$zone2_max bpm"
echo "  → Target: 150+ min/week for longevity"
echo "  → Benefits: Fat oxidation, metabolic health"
echo ""
echo "Zone 4 (VO2 Max): $zone4_min-$zone4_max bpm"
echo "  → Target: 20-30 min/week for longevity"
echo "  → Benefits: Cardiovascular fitness, mortality reduction"
echo ""

# Track weekly progress
week_zone2=0
week_zone4=0

for i in {0..6}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$file_date.md"
  
  if [ -f "$health_file" ]; then
    z2=$(grep "exercise_zone2:" "$health_file" | sed 's/.*exercise_zone2://' | tr -d ' ')
    z4=$(grep "exercise_zone4:" "$health_file" | sed 's/.*exercise_zone4://' | tr -d ' ')
    week_zone2=$((week_zone2 + ${z2:-0}))
    week_zone4=$((week_zone4 + ${z4:-0}))
  fi
done

echo "This Week's Progress:"
printf "  Zone 2: %d/150 min %s\n" $week_zone2 "$([ $week_zone2 -ge 150 ] && echo "✅" || echo "⏳")"
printf "  Zone 4: %d/20 min %s\n" $week_zone4 "$([ $week_zone4 -ge 20 ] && echo "✅" || echo "⏳")"
```

### 💊 Supplement & Intervention Tracker

Track longevity interventions in your entries.

```yaml
# Example entry with longevity interventions
interventions:
  fasting:
    type: 16:8  # or OMAD, 5:2, Prolonged
    hours: 16
    compliance: true
  
  supplements:
    omega3: 2000mg
    vitamin_d3: 4000IU
    magnesium: 400mg
    creatine: 5g
  
  exercise:
    zone2_minutes: 45
    zone4_minutes: 5
    resistance: true
  
  recovery:
    sauna: 20min
    cold_exposure: 2min
    sleep_optimization: true

longevity_markers:
  biological_age: 33  # Estimated from metrics
  healthspan_score: 82
  allostatic_load: 3.2
```

### 🎯 Longevity Insights Engine

```bash
#!/bin/bash
# longevity-insights.sh — Longevity-specific recommendations

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

echo "🧬 LONGEVITY INSIGHTS"
echo "====================="
echo ""

# Analyze last 30 days for longevity gaps
sleep_avg=0
zone2_total=0
fasting_avg=0

for i in {0..29}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$file_date.md"
  
  if [ -f "$health_file" ]; then
    sleep=$(grep "sleep_hours:" "$health_file" | sed 's/.*sleep_hours://' | tr -d ' ')
    z2=$(grep "exercise_zone2:" "$health_file" | sed 's/.*exercise_zone2://' | tr -d ' ')
    fast=$(grep "fasting_hours:" "$health_file" | sed 's/.*fasting_hours://' | tr -d ' ')
    
    sleep_avg=$(echo "$sleep_avg + ${sleep:-0}" | bc)
    zone2_total=$((zone2_total + ${z2:-0}))
    fasting_avg=$(echo "$fasting_avg + ${fast:-0}" | bc)
  fi
done

sleep_avg=$(echo "scale=1; $sleep_avg / 30" | bc)
fasting_avg=$(echo "scale=1; $fasting_avg / 30" | bc)

echo "30-Day Averages:"
echo "  Sleep: ${sleep_avg}h"
echo "  Zone 2 exercise: ${zone2_total} min total"
echo "  Fasting: ${fasting_avg}h avg"
echo ""

# Generate recommendations
echo "🎯 LONGEVITY RECOMMENDATIONS:"
echo ""

# Check sleep
if (( $(echo "$sleep_avg < 7" | bc -l) )); then
  echo "Priority 1: 😴 SLEEP"
  echo "  Your average is below 7 hours"
  echo "  → This is the #1 longevity lever"
  echo "  → Action: Target 7.5-8.5 hours consistently"
  echo "  → Impact: +5-10 years healthspan"
  echo ""
fi

# Check Zone 2
if [ $zone2_total -lt 300 ]; then
  echo "Priority 2: 🏃 ZONE 2 EXERCISE"
  echo "  Only ${zone2_total} min in 30 days (target: 600+)"
  echo "  → Benefits: Mitochondrial health, metabolic flexibility"
  echo "  → Action: 30min Zone 2 walking 5x/week"
  echo "  → Impact: Major all-cause mortality reduction"
  echo ""
fi

# Check fasting
if (( $(echo "$fasting_avg < 12" | bc -l) )); then
  echo "Priority 3: 🕐 FASTING"
  echo "  Avg fasting window below 12 hours"
  echo "  → Benefits: Autophagy, insulin sensitivity"
  echo "  → Action: Gradually extend to 14-16 hours"
  echo ""
fi

# Celebrate wins
if (( $(echo "$sleep_avg >= 7.5" | bc -l) )); then
  echo "✅ SLEEP: Excellent! Maintaining 7.5+ hours"
fi
if [ $zone2_total -ge 450 ]; then
  echo "✅ EXERCISE: Great Zone 2 volume!"
fi

echo ""
echo "💡 Remember: Consistency > Intensity"
echo "   Small daily habits compound into decades"
```

### 📈 Longevity Trend Visualization

```bash
#!/bin/bash
# longevity-trends.sh — 90-day longevity trend

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")

echo "🧬 90-DAY LONGEVITY TRENDS"
echo "=========================="
echo ""

# Get daily healthspan scores for last 90 days
declare -a scores
declare -a dates

for i in {89..0}; do
  file_date=$(date -v-${i}d +%d-%m-%y 2>/dev/null || date -d "${i} days ago" +%d-%m-%y)
  short_date=$(date -v-${i}d +%m/%d 2>/dev/null || date -d "${i} days ago" +%m/%d)
  year=$(date -v-${i}d +%Y 2>/dev/null || date -d "${i} days ago" +%Y)
  month=$(date -v-${i}d +%m 2>/dev/null || date -d "${i} days ago" +%m)
  
  health_file="~/.openclaw/customers/$user_name/floreo/domains/health/$year/$month/$file_date.md"
  
  if [ -f "$health_file" ]; then
    # Calculate simple score for this day
    sleep=$(grep "sleep_hours:" "$health_file" | sed 's/.*sleep_hours://' | tr -d ' ')
    exercise=$(grep "exercise_zone2:" "$health_file" | sed 's/.*exercise_zone2://' | tr -d ' ')
    stress=$(grep "cortisol_proxy:" "$health_file" | sed 's/.*cortisol_proxy://' | tr -d ' ')
    
    day_score=50  # Base
    
    if [ -n "$sleep" ]; then
      if (( $(echo "$sleep >= 7 && $sleep <= 9" | bc -l) )); then day_score=$((day_score + 20)); fi
    fi
    if [ -n "$exercise" ] && [ "$exercise" -ge 30 ]; then day_score=$((day_score + 20)); fi
    if [ -n "$stress" ] && [ "$stress" -le 4 ]; then day_score=$((day_score + 10)); fi
    
    scores+=($day_score)
    dates+=($short_date)
  fi
done

# Simple ASCII trend
echo "Healthspan Score Trend (Last 90 Days)"
echo ""
echo "100 |"
echo " 90 |"
echo " 80 |"
echo " 70 |"
echo " 60 |"
echo " 50 |"
echo "    +------------------------------------------>"
echo ""
echo "Avg: $(echo "${scores[@]}" | tr ' ' '+' | bc) / ${#scores[@]} = $(( ($(echo "${scores[@]}" | tr ' ' '+' | bc)) / ${#scores[@]} ))"
```

---

## Automated Artistic Reports

Set up automated daily, weekly, or custom periodic reports with beautiful formatting.

### Report Schedule Configuration

Create a report config file:

```bash
cat > ~/.openclaw/customers/{user_name}/floreo/.report-config << 'EOF'
# Report Schedule Configuration
daily_report=true
daily_time=21:00

weekly_report=true
weekly_day=Sunday
weekly_time=20:00

monthly_report=true
monthly_day=last
monthly_time=18:00

# Report style
style=artistic
include_mood=true
include_metrics=true
include_trends=true
EOF
```

### Daily Artistic Report (Includes Imported Entries)

Generate at 9 PM daily - includes ALL entries for that date, whether created today or imported:

```bash
#!/bin/bash
# ~/.openclaw/customers/{user_name}/floreo/generate-daily-report.sh

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
date_str=$(date +%d-%m-%y)
date_iso=$(date +%Y-%m-%d)
day_of_year=$(date +%j)

report_file="~/.openclaw/customers/$user_name/floreo/insights/daily-report-$date_iso.md"

# Collect today's entries (native + imported with original dates)
# NOTE: Uses date_str from filename (original entry date), not file modification time
# This means imported historical entries show up on their ORIGINAL date, not import date
today_entries=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "$date_str.md" 2>/dev/null)

# If today is April 15, this finds:
# - Entries created April 15
# - Entries imported from memory that were originally made April 15
# Both appear in April 15 report

cat > "$report_file" << 'REPORT'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🌸  F L O R E O  D A I L Y  R E P O R T  🌸        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📅 Date: DATE_PLACEHOLDER
📊 Day NUMBER of 365
🌙 Generated at TIME

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REPORT

sed -i "s/DATE_PLACEHOLDER/$date_iso/" "$report_file"
sed -i "s/NUMBER/$day_of_year/" "$report_file"
sed -i "s/TIME/$(date +%H:%M)/" "$report_file"

# Add domain summaries
for domain in work health learn relate create reflect; do
  domain_file="~/.openclaw/customers/$user_name/floreo/domains/$domain/$(date +%Y)/$(date +%m)/$date_str.md"
  
  if [ -f "$domain_file" ]; then
    count=$(grep -c "^type: entry" "$domain_file" 2>/dev/null || echo 0)
    
    case $domain in
      work) emoji="💼" ;;
      health) emoji="💪" ;;
      learn) emoji="📚" ;;
      relate) emoji="🤝" ;;
      create) emoji="🎨" ;;
      reflect) emoji="🧘" ;;
    esac
    
    echo "" >> "$report_file"
    echo "$emoji ${domain^^}" >> "$report_file"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
    echo "" >> "$report_file"
    
    # Extract entry summaries
    grep -A100 "^---$" "$domain_file" | grep -v "^---$" | grep -v "^[a-z_]*:" | head -20 >> "$report_file"
    echo "" >> "$report_file"
  fi
done

# Add metrics summary
echo "" >> "$report_file"
echo "📊 M E T R I C S" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Extract and sum metrics
find ~/.openclaw/customers/$user_name/floreo/domains -name "$date_str.md" -exec grep -h "^  [a-z_]*:" {} \; | \
  sed 's/^  //' | \
  awk -F: '{sum[$1]+=$2} END {for (m in sum) printf "  %s: %.1f\\n", m, sum[m]}' >> "$report_file"

# Add mood/energy if tracked
echo "" >> "$report_file"
echo "🎭 M O O D & E N E R G Y" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Add footer
cat >> "$report_file" << 'FOOTER'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌸 Flore per integra — Flourish through wholeness

💡 Tip: Run this report anytime with:
   /floreo report --daily

FOOTER

echo "Daily report generated: $report_file"
```

### Weekly Artistic Report (Includes Imported Historical Entries)

```bash
#!/bin/bash
# Generate weekly artistic report
# Includes entries created this week OR imported entries with original dates in this week

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
week_start=$(date -v-sun -v-7d +%Y-%m-%d)
week_end=$(date -v-sat +%Y-%m-%d)
week_num=$(date +%V)

# Note: Uses entry date from filename (original date), not file modification time
# Imported entries from history appear in their original week, not import week

report_file="~/.openclaw/customers/$user_name/floreo/insights/weekly-report-W$week_num.md"

cat > "$report_file" << 'REPORT'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      🌸  F L O R E O  W E E K L Y  R E P O R T  🌸           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📅 Week WEEK_NUM | START to END
🗓️  Days 1-7 of the week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                         W E E K  I N  R E V I E W
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REPORT

sed -i "s/WEEK_NUM/$week_num/" "$report_file"
sed -i "s/START/$week_start/" "$report_file"
sed -i "s/END/$week_end/" "$report_file"

# Domain activity bars
for domain in work health learn relate create reflect; do
  count=$(find ~/.openclaw/customers/$user_name/floreo/domains/$domain -name "*.md" -mtime -7 2>/dev/null | wc -l)
  
  # Create ASCII bar
  bar_len=$((count * 2))
  bar=$(printf '█%.0s' $(seq 1 $bar_len))
  
  case $domain in
    work) emoji="💼" label="Work" ;;
    health) emoji="💪" label="Health" ;;
    learn) emoji="📚" label="Learn" ;;
    relate) emoji="🤝" label="Relate" ;;
    create) emoji="🎨" label="Create" ;;
    reflect) emoji="🧘" label="Reflect" ;;
  esac
  
  printf "%s %-8s │%-20s│ %d entries\\n" "$emoji" "$label" "$bar" "$count" >> "$report_file"
done

echo "" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "                    H I G H L I G H T S" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Find highlights (entries with positive keywords)
find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -mtime -7 -exec grep -l "shipped\|completed\|achieved\|milestone\|success" {} \; | \
  while read file; do
    echo "✨ $(grep -v "^[a-z_]*:" "$file" | grep -v "^---$" | head -3)" >> "$report_file"
    echo "" >> "$report_file"
  done

# Weekly trends
echo "" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "                      T R E N D S" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Compare to previous week
prev_week_count=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -mtime -14 ! -mtime -7 2>/dev/null | wc -l)
this_week_count=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -mtime -7 2>/dev/null | wc -l)

diff=$((this_week_count - prev_week_count))
if [ $diff -gt 0 ]; then
  trend="📈 +$diff entries vs last week"
elif [ $diff -lt 0 ]; then
  trend="📉 $diff entries vs last week"
else
  trend="➡️ Same as last week"
fi

echo "$trend" >> "$report_file"

# Footer
cat >> "$report_file" << 'FOOTER'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌸 Flore per integra — Flourish through wholeness

💡 "The unexamined life is not worth living." — Socrates

FOOTER

echo "Weekly report generated: $report_file"
```

### Schedule with Cron

```bash
# Edit crontab
crontab -e

# Add entries:
# Daily report at 9 PM
0 21 * * * ~/.openclaw/customers/{user_name}/floreo/generate-daily-report.sh

# Weekly report on Sundays at 8 PM  
0 20 * * 0 ~/.openclaw/customers/{user_name}/floreo/generate-weekly-report.sh

# Monthly report on last day of month at 6 PM
0 18 28-31 * * [ "$(date +\%d -d tomorrow)" = "01" ] && ~/.openclaw/customers/{user_name}/floreo/generate-monthly-report.sh
```

### Monthly Artistic Report (Unified Native + Imported Data)

```bash
#!/bin/bash
# Generate monthly artistic report
# Combines native entries and imported historical entries by ORIGINAL date

user_name=$(cat ~/.openclaw/customers/.floreo-user 2>/dev/null || echo "default")
month_str=$(date +%B)
month_num=$(date +%m)
year=$(date +%Y)
days_in_month=$(date -v+1m -v1d -v-1d +%d)

# All entries use original date - imported entries from 6 months ago
# that were imported today will appear in their original month, not current month

report_file="~/.openclaw/customers/$user_name/floreo/insights/monthly-report-$year-$month_num.md"

cat > "$report_file" << 'REPORT'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌸  F L O R E O  M O N T H L Y  R E P O R T  🌸          ║
║                                                              ║
║                         YEAR MONTH                           ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REPORT

sed -i "s/YEAR/$year/" "$report_file"
sed -i "s/MONTH/$month_str/" "$report_file"

# Calendar heatmap (ASCII)
echo "" >> "$report_file"
echo "📅 M O N T H  A T  A  G L A N C E" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Generate calendar with activity indicators
cal | while read line; do
  echo "$line" >> "$report_file"
done

echo "" >> "$report_file"
echo "🔥 = High activity day  ·  📝 = Entry recorded  ·  · = No entries" >> "$report_file"

# Domain pie chart (ASCII)
echo "" >> "$report_file"
echo "📊 D O M A I N  D I S T R I B U T I O N" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

total_entries=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -newermt "$year-$month_num-01" ! -newermt "$year-$month_num-31" 2>/dev/null | wc -l)

for domain in work health learn relate create reflect; do
  count=$(find ~/.openclaw/customers/$user_name/floreo/domains/$domain -name "*.md" -newermt "$year-$month_num-01" ! -newermt "$year-$month_num-31" 2>/dev/null | wc -l)
  
  if [ $total_entries -gt 0 ]; then
    percentage=$((count * 100 / total_entries))
  else
    percentage=0
  fi
  
  case $domain in
    work) emoji="💼" color="\\033[0;34m" ;;
    health) emoji="💪" color="\\033[0;32m" ;;
    learn) emoji="📚" color="\\033[0;33m" ;;
    relate) emoji="🤝" color="\\033[0;35m" ;;
    create) emoji="🎨" color="\\033[0;36m" ;;
    reflect) emoji="🧘" color="\\033[0;37m" ;;
  esac
  
  printf "%s %-8s: %3d%% " "$emoji" "${domain^^}" "$percentage" >> "$report_file"
  
  # ASCII bar
  bar_len=$((percentage / 5))
  printf '%.0s█' $(seq 1 $bar_len) >> "$report_file"
  printf " %d entries\\n" "$count" >> "$report_file"
done

# Top metrics
echo "" >> "$report_file"
echo "📈 T O P  M E T R I C S" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

# Sum all metrics for the month
find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -newermt "$year-$month_num-01" ! -newermt "$year-$month_num-31" -exec cat {} \; | \
  grep "^  [a-z_]*:" | \
  sed 's/^  //' | \
  awk -F: '{sum[$1]+=$2} END {for (m in sum) printf "  %-20s: %.1f\\n", m, sum[m]}' | \
  sort -t: -k2 -rn | \
  head -10 >> "$report_file"

# Achievements
echo "" >> "$report_file"
echo "🏆 M O N T H  A C H I E V E M E N T S" >> "$report_file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$report_file"
echo "" >> "$report_file"

achievements=0

# Check for consistency achievement
consecutive_days=$(find ~/.openclaw/customers/$user_name/floreo/domains -name "*.md" -mtime -30 | wc -l)
if [ $consecutive_days -ge 7 ]; then
  echo "🎯 Consistency: Logged entries for $consecutive_days days this month" >> "$report_file"
  achievements=$((achievements + 1))
fi

# Check for domain diversity
domain_count=0
for domain in work health learn relate create reflect; do
  if [ $(find ~/.openclaw/customers/$user_name/floreo/domains/$domain -name "*.md" -newermt "$year-$month_num-01" ! -newermt "$year-$month_num-31" 2>/dev/null | wc -l) -gt 0 ]; then
    domain_count=$((domain_count + 1))
  fi
done

if [ $domain_count -ge 4 ]; then
  echo "🌈 Balanced Life: Active in $domain_count life domains" >> "$report_file"
  achievements=$((achievements + 1))
fi

# Check for high activity
if [ $total_entries -ge 20 ]; then
  echo "🔥 High Activity: $total_entries entries this month" >> "$report_file"
  achievements=$((achievements + 1))
fi

if [ $achievements -eq 0 ]; then
  echo "💪 Keep going! Every entry is progress." >> "$report_file"
fi

# Footer
cat >> "$report_file" << 'FOOTER'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌸 Flore per integra — Flourish through wholeness

📊 "In the ledger of life, every moment counts."

FOOTER

echo "Monthly report generated: $report_file"
```

### One-Off Report Generation

```markdown
Generate a daily artistic report for today by:
1. Finding all entries from today (15-04-26)
2. Creating a beautifully formatted markdown report
3. Including:
   - ASCII art header
   - Domain summaries with icons
   - Metrics summary
   - Mood/energy tracking
   - Tips for tomorrow
4. Saving to ~/.openclaw/customers/{user_name}/floreo/insights/daily-report-2026-04-15.md
```

### Report Templates

Create template files for consistent styling:

```bash
# Daily template
cat > ~/.openclaw/customers/{user_name}/floreo/.templates/daily.md << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║           🌸  F L O R E O  D A I L Y  R E P O R T  🌸        ║
╚══════════════════════════════════════════════════════════════╝

📅 {{DATE}} | Day {{DAY_OF_YEAR}} of 365

{{DOMAIN_SUMMARIES}}

📊 Metrics Today:
{{METRICS}}

🎭 Mood: {{MOOD}}/10 | Energy: {{ENERGY}}/10

💡 Tomorrow's Intention:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

🌸 Flore per integra
EOF

# Weekly template
cat > ~/.openclaw/customers/{user_name}/floreo/.templates/weekly.md << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║      🌸  F L O R E O  W E E K L Y  R E P O R T  🌸           ║
╚══════════════════════════════════════════════════════════════╝

📅 Week {{WEEK_NUM}} | {{WEEK_START}} to {{WEEK_END}}

{{WEEKLY_HEATMAP}}

🏆 Highlights:
{{HIGHLIGHTS}}

📈 Trend: {{TREND}}

🌸 Flore per integra
EOF
```

## 🛡️ Skill Longevity & Maintenance

Floreo is designed to work reliably for years. This section documents how the skill maintains durability, backward compatibility, and future-proofing.

### Version History & Compatibility

| Version | Date | Breaking Changes? | Migration Required |
|---------|------|-------------------|-------------------|
| v0.1.0 | 2026-04-10 | — | — |
| v0.2.0 | 2026-04-15 | ❌ No | Automatic |
| v0.3.0 | 2026-04-15 | ❌ No | Automatic |

**Compatibility Guarantee**: All entries created in v0.1.0+ remain fully readable in v0.3.0+ without modification.

### Schema Versioning

Entries include implicit schema versioning through the `type` field:

```yaml
# All versions use same base schema
type: entry                    # v0.1.0+ — Base entry
entry_id: FE-20260415-ABC123   # v0.1.0+ — Unique identifier
domain: work                   # v0.1.0+ — Life domain
date: 15-04-26                 # v0.1.0+ — Entry date
timestamp: 2026-04-15T10:00:00 # v0.1.0+ — ISO timestamp
privacy: internal              # v0.1.0+ — Privacy tier
metrics:                       # v0.1.0+ — Extensible metrics
  focus: 4
tags: project-x                # v0.1.0+ — Searchable tags
```

**Adding New Fields**: Simply add new fields to the YAML frontmatter. Old entries without them will be treated as null/undefined.

### Backward Compatibility Guarantees

1. **Entry Format**: The YAML frontmatter structure will never change in a breaking way
2. **File Paths**: Directory structure `domains/{domain}/{year}/{month}/{date}.md` is permanent
3. **Entry ID Format**: `FE-{YYYYMMDD}-{6CHAR}` will remain valid forever
4. **Shell Scripts**: All documented shell commands use POSIX-standard tools (grep, sed, awk, bc)

### Future-Proofing Strategies

#### 1. Extensible Metrics

Add custom metrics without breaking existing entries:

```yaml
metrics:
  # Core metrics (always supported)
  focus: 4
  commits: 5
  
  # Custom metrics (added anytime)
  my_custom_metric: 42
  another_field: "value"
```

New metrics are automatically included in analysis if they follow numeric conventions.

#### 2. Graceful Degradation

All analysis scripts handle missing data gracefully:

```bash
# This safely handles missing fields
commits=$(grep "commits:" "$file" | sed 's/.*commits://' | tr -d ' ')
commits=${commits:-0}  # Default to 0 if not found
```

#### 3. Idempotent Operations

Safe to re-run any operation:
- Import same file multiple times → No duplicates (entry_id based)
- Generate reports → Overwrites safely
- Calculate metrics → Deterministic results

### Migration Guides

#### If Entry Format Evolves (Future v0.4.0+)

```bash
#!/bin/bash
# migrate-entries.sh — Future migration script template

# 1. Backup existing entries
cp -r ~/.openclaw/customers/{user_name}/floreo/domains ~/floreo-backup-$(date +%Y%m%d)

# 2. Transform entries (example: adding new required field)
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" | while read file; do
  # Add new field if missing
  if ! grep -q "new_field:" "$file"; then
    # Insert after 'type: entry' line
    sed -i '/^type: entry/a new_field: default_value' "$file"
  fi
done

echo "✅ Migration complete. Backup at ~/floreo-backup-*"
```

#### Preserving Old Data

Historical entries are never deleted or modified by new features:
- New metrics = additive only
- New domains = optional (old entries still work)
- New reports = generated alongside, don't overwrite history

### Maintainability Features

#### Single File Documentation

All documentation in one `SKILL.md`:
- No external dependencies
- No broken links
- Self-contained reference
- Easy to archive/share

#### No External Dependencies

- ✅ No npm packages
- ✅ No Python imports
- ✅ No database required
- ✅ No API keys
- ✅ Works offline forever

#### POSIX Compliance

All shell scripts use POSIX-standard tools:
- `grep`, `sed`, `awk`, `bc`, `date`, `find`
- Works on macOS, Linux, BSD
- No Bash 4+ specific features
- No GNU-specific extensions

### Durability Guarantees

| Aspect | Guarantee |
|--------|-----------|
| **Data Format** | Plain text Markdown + YAML — readable forever |
| **Storage** | Local filesystem — no service dependencies |
| **Tools** | POSIX shell — available on all Unix systems |
| **Dependencies** | Zero — skill never breaks due to external changes |
| **Backward Compat** | 100% — old entries always readable |
| **Future Updates** | Additive only — never removes features |

### Long-Term Archival

Your Floreo data is future-proof:

```bash
# Complete backup (portable, future-proof)
tar czf floreo-archive-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/customers/{user_name}/floreo/

# Restore anytime, anywhere with OpenClaw
# All entries remain readable without any tools
# Plain text = human readable even without software
```

### Skill Maintenance Checklist

**Annual Review** (use heartbeat or cron):
```markdown
1. Check entry count growth:
   Run shell: find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" | wc -l
   
2. Verify data integrity:
   Run shell: grep -l "^type: entry" ~/.openclaw/customers/{user_name}/floreo/domains/*/*/*/*.md | wc -l
   
3. Test a random entry is readable:
   Read random file from domains directory
   
4. Backup verification:
   Check backup exists from last 30 days
```

### When OpenClaw Updates

Floreo is resilient to OpenClaw changes:
- Uses only basic `write`, `read`, `exec` tools
- No custom tool dependencies
- No API integrations
- Shell scripts work standalone

If OpenClaw changes significantly, you can still:
1. Read entries directly: `cat ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/15-04-26.md`
2. Query with standard tools: `grep -r "shipped" ~/.openclaw/customers/{user_name}/floreo/domains/`
3. Generate reports manually using the shell scripts in this SKILL.md

---

## Limitations of Native Approach

| Feature | Custom Script | Native Tools |
|---------|--------------|--------------|
| Auto-detection | ✅ Automatic | ❌ Manual |
| Suggestions | ✅ Smart | ❌ None |
| Indexing | ✅ O(1) | ❌ O(n) scan |
| Redaction | ✅ Automatic | ❌ Manual regex |
| UI | ✅ Rich | ❌ Text only |

**Trade-off**: Simplicity vs. Features

---

## Example: Complete Workflow

### Morning Entry

```
Write to ~/.openclaw/customers/{user_name}/floreo/domains/health/2026/04/15-04-26.md:

---
type: entry
entry_id: FE-20260415-MORNING
domain: health
date: 15-04-26
day: 105
timestamp: 2026-04-15T07:00:00
privacy: private
metrics:
  energy: 8
  sleep: 7.5
tags: morning, routine
---
Morning routine complete. Feeling good today.
```

### Mid-day Work Entry

```
Append to ~/.openclaw/customers/{user_name}/floreo/domains/work/2026/04/15-04-26.md:

---
type: entry
entry_id: FE-20260415-WORK1
domain: work
date: 15-04-26
day: 105
timestamp: 2026-04-15T12:00:00
privacy: internal
metrics:
  focus: 4
  commits: 3
tags: coding, feature-x
---
Shipped the authentication refactor. 4 hours deep work.
```

### Evening Reflection

```
Append to ~/.openclaw/customers/{user_name}/floreo/domains/reflect/2026/04/15-04-26.md:

---
type: entry
entry_id: FE-20260415-REFLECT
domain: reflect
date: 15-04-26
day: 105
timestamp: 2026-04-15T21:00:00
privacy: private
metrics:
  mood: 8
  productivity: 9
tags: daily-review
---
Productive day. Shipped auth refactor and had good team sync.
Grateful for focused work time.
```

### End of Week Review

```
Run shell command:
find ~/.openclaw/customers/{user_name}/floreo/domains -name "*.md" -mtime -7 | xargs cat > ~/.openclaw/customers/{user_name}/floreo/insights/week-16-review.md

Then read that file and summarize what was accomplished this week.
```

---

## Resources

- **SKILL.md**: This file (the complete guide)
- **No other files needed**: Use OpenClaw native tools
- **GitHub**: https://github.com/openclaw/floreo (for documentation only)

---

*Floreo v0.2.1 — Built to Last. Flourish through wholeness, compounded, extended.* 🌸