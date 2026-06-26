---
name: archive-project
version: 1.2.4
homepage: https://github.com/KaigeGao1110/ArchiveProject
description: Organize completed projects into searchable archives with session transcript backup.
dependencies: []
configPaths:
  - path: ~/.openclaw/agents/main/sessions/
    description: Required for reading session transcript files prior to archiving.
permissions:
  - read: session transcripts from configured path
  - write: workspace/projects/ directory
  - exec: git commit commands
  - exec: python3 scripts/sanitize_transcript.py
dataPolicy:
  archivedData: internal workspace only
  neverExternal: true
---

## Installation

### Option 1: ClawhHub CLI (recommended)
```bash
openclaw skills install archive-project
# or
clawhub install archive-project
```

### Option 2: From GitHub
```bash
# Clone the repo
git clone https://github.com/KaigeGao1110/ArchiveProject.git ~/.openclaw/skills/archive-project

# Or download directly
curl -L https://github.com/KaigeGao1110/ArchiveProject/archive/refs/heads/main.zip -o /tmp/archive-project.zip
unzip /tmp/archive-project.zip -d ~/.openclaw/skills/
mv ~/.openclaw/skills/ArchiveProject-main ~/.openclaw/skills/archive-project
```

# Archive Project Skill

Organize a completed project into a complete, long-term searchable archive.

> **Data Privacy**: Archived data (session transcripts, project files) **never leaves the internal workspace** unless you explicitly approve a publish step. The sanitize script is applied automatically before any archival.

---

## Trigger Conditions

Archive is triggered only when **you say "archive this"** or **"can we archive this"**. This is the only trigger — you always decide when a project is done.

### Trigger 2: Slash command
Type `//archive ` followed by your project name to activate the Archive skill.
Example: "//archive cureforge-hr-assessment"

However, in these scenarios, I will **prompt but not execute**:
- A delivery action just happened (email sent, demo link generated, all subagents done, code committed)
- You start a new project or say "next task" / "different topic"

I will NOT prompt when:
- Project is still in active development
- Task is ongoing operations
- Waiting on external feedback (48h+ silence)

---

## Archive Flow

### Step 1: Create project archive directory

```
workspace/projects/<project-name>/
  ARCHIVE.md
  session_transcript.jsonl
  subagent_sessions/
  deliverables/
  decisions.md
```

### Step 2: Collect session transcripts

**Subagent sessions (important — must collect):**

```bash
# Directory containing session transcripts (configurable via SESSION_TRANSCRIPT_PATH)
# Default: ~/.openclaw/agents/main/sessions/ (standard for all users)
# Override: set SESSION_TRANSCRIPT_PATH to a custom path (e.g., EFS mount)
SESSION_DIR="${SESSION_TRANSCRIPT_PATH:-$HOME/.openclaw/agents/main/sessions/}"

# Find main session transcript using explicit session key (from session label or passed argument)
# Use the session key/label to match the exact transcript file
SESSION_KEY="${1:-}"  # Pass session key as argument or extract from context
if [ -n "$SESSION_KEY" ]; then
  MAIN_SESSION_PATH=$(grep -l "$SESSION_KEY" "${SESSION_DIR}"*.jsonl 2>/dev/null | head -1)
fi
# Fallback: if no key provided or not found, use most recent transcript
if [ -z "$MAIN_SESSION_PATH" ] || [ ! -f "$MAIN_SESSION_PATH" ]; then
  MAIN_SESSION_PATH=$(ls -t "${SESSION_DIR}"*.jsonl 2>/dev/null | head -1)
fi

# Create project archive directory
mkdir -p workspace/projects/<project-name>/subagent_sessions/

# Copy main session transcript
cp "$MAIN_SESSION_PATH" "workspace/projects/<project-name>/session_transcript.jsonl"
```

**Child subagent transcripts:**

```bash
# Child subagent session IDs are listed in the main session JSONL
# Look for "childSessions" array in the session metadata
# Copy each child session transcript to subagent_sessions/
# Pattern: {SESSION_DIR}/{child-id}.jsonl
```

### Step 3: Sanitize transcripts (CRITICAL — must do before archiving)

**Before archiving, remove:**
- API keys, tokens, and authentication credentials
- Personal contact information (emails, phone numbers)
- Internal infrastructure details (hostnames, IPs)
- Any sensitive environment variables

**Use the sanitization script:**

```bash
python3 scripts/sanitize_transcript.py \
  workspace/projects/<project-name>/session_transcript.jsonl \
  -o workspace/projects/<project-name>/session_transcript_sanitized.jsonl
```

The script redacts:
- API keys (GitHub tokens, OpenAI keys, AWS credentials, etc.)
- Email addresses
- Phone numbers
- IP addresses (IPv4 and IPv6)
- Internal hostnames and AWS EC2 DNS names
- Generic secrets and high-entropy tokens

**Verify before proceeding:**
```bash
# Run built-in tests to confirm redaction works
python3 scripts/sanitize_transcript.py --test

# Manual spot-check (look for any remaining sensitive data)
grep -iE '(token|key|password|email|phone|@|192\.168|10\.)' \
  workspace/projects/<project-name>/session_transcript_sanitized.jsonl || echo "No sensitive data found"
```

**After verification, replace the original with the sanitized version:**
```bash
mv workspace/projects/<project-name>/session_transcript_sanitized.jsonl \
   workspace/projects/<project-name>/session_transcript.jsonl
```

### Step 4: Write ARCHIVE.md

Use the template below. **Fill in decision rationale** — this is the most valuable part for future retrospectives.

### Step 5: Update MEMORY.md

Add a one-line summary to MEMORY.md: project name + status + link.

### Step 6: Delete EFS session files (requires approval)

**Before deleting any session files from EFS, ask the user:**

> "Can I delete the EFS session files for this project? They are already backed up in the archive."

**Only proceed if the user explicitly approves.** Never auto-delete without asking.

If approved:
```bash
# Remove the main session transcript from EFS
rm -f "${SESSION_DIR}$(basename "$MAIN_SESSION_PATH")"

# Remove any child subagent session transcripts from EFS
for CHILD_ID in <child-session-ids>; do
  rm -f "${SESSION_DIR}${CHILD_ID}.jsonl"
done
```

If not approved, leave the EFS session files as-is.

### Step 7: Git commit (internal workspace only)

```bash
cd workspace
git add projects/<project-name>/
git commit -m "Archive: <project-name>"
```

**Keep project data private.** Archive data is for internal reference only.



---

## ARCHIVE.md Template

```markdown
# <Project Name> — Project Archive

_Created: <date> | Owner: <owner> | Status: <status>_

---

## One-Line Summary

<1-2 sentences: what this project does, who it's for, its core value>

---

## Project Background

### Client
<Name + contact info — after archiving, record only what is needed for future reference>

### Source Materials
| File | Content |
|------|---------|
| <file1> | <description> |
| <file2> | <description> |

---

## Deliverables

### Code / Product
| Path | Description |
|------|-------------|
| <path> | <description> |

### Reports / Docs
| File | Description |
|------|-------------|
| <file> | <description> |

### Demo / Links
| Link | Description |
|------|-------------|
| <URL> | <description> |

---

## Timeline

| Date | Event |
|------|-------|
| YYYY-MM-DD | <event> |
| YYYY-MM-DD | <delivery> |

---

## Key Decisions

### N. <Decision Title>
**Options:** A vs B (chose A)
**Rationale:** <why this choice>
**Outcome:** <what happened>

---

## Open Items

| Item | Description | Priority |
|------|-------------|----------|
| <item> | <description> | High/Med/Low |

---

## Lessons Learned

### N. <Lesson Title>
<What was learned, what to do differently next time>

---

## Git Commits (Internal)

| Stage | Commit | Description |
|-------|--------|-------------|
| Initial | <hash> | <description> |
| Delivery | <hash> | <description> |

---

## Reconstruction Guide

```bash
<reconstruction commands>
```
```

---

## decisions.md Template

```markdown
# Key Decisions — <project-name>

## Decision N
- Date:
- Problem:
- Options:
  - A: <description>
  - B: <description>
- Decision: <what was chosen>
- Rationale: <why>
```

---

## Sanitization Script Reference

The `scripts/sanitize_transcript.py` script provides deterministic, audited redaction of sensitive data from session transcripts.

### What it redacts

| Category | Examples | Replacement |
|----------|----------|-------------|
| GitHub tokens | `ghp_xxx`, `github_pat_xxx` | `[REDACTED-GITHUB-TOKEN]` |
| OpenAI keys | `sk-xxx`, `sk-proj-xxx` | `[REDACTED-OPENAI-KEY]` |
| Anthropic keys | `sk-ant-xxx` | `[REDACTED-ANTHROPIC-KEY]` |
| AWS credentials | `AKIAxxx`, `aws_access_key_id=xxx` | `[REDACTED]` |
| Email addresses | `user@example.com` | `[REDACTED-EMAIL]` |
| Phone numbers | `+1 555-123-4567` | `[REDACTED-PHONE]` |
| IPv4 addresses | `192.168.1.1`, `10.0.0.1` | `[REDACTED-IP]` |
| IPv6 addresses | `2001:db8::1` | `[REDACTED-IPV6]` |
| Internal hostnames | `ip-10-0-1-43.local` | `[REDACTED-HOSTNAME]` |
| AWS EC2 DNS | `ec2-xxx.amazonaws.com` | `[REDACTED-AWS-HOST]` |
| Generic secrets | High-entropy base64/hex strings | `[REDACTED-SECRET]` |

### Usage

```bash
# Basic usage — output to stdout
python3 scripts/sanitize_transcript.py input.jsonl > sanitized.jsonl

# Explicit output file
python3 scripts/sanitize_transcript.py input.jsonl -o sanitized.jsonl

# Read from stdin
cat input.jsonl | python3 scripts/sanitize_transcript.py > sanitized.jsonl

# Run built-in tests
python3 scripts/sanitize_transcript.py --test
```

### Properties

- **Deterministic**: Same input always produces identical output
- **Non-destructive**: Original file is never modified
- **Structure-preserving**: JSON/JSONL structure is maintained; only string values are redacted
- **Testable**: Built-in test mode verifies redaction patterns
