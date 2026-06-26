---
name: file-sender
description: |
  File Sender — Packages workspace files and delivers them to the user with a description.

  Use when:
  - You've generated deliverable files (code projects, images, documents, scripts, reports, etc.) and need to deliver them to the user
  - The user asks to "send me the file", "export", "package for download", "deliver the files", etc.
  - You've finished creating/modifying files in the workspace and they're ready to hand off
  - The user didn't explicitly ask for file delivery, but you've produced valuable deliverables they'll want

  Even if the user doesn't explicitly ask for file delivery, you should proactively trigger
  this skill whenever you generate deliverable artifacts in the workspace.

  Do NOT confuse with web search/fetch — this skill packages and delivers local files, not remote content.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["curl", "zip"],
            "envs":
              [
                "OPENCLAW_INSTANCE_NAME",
                "OPENCLAW_MANAGER_URL",
                "OPENCLAW_FILE_PUSH_TOKEN",
              ],
          },
      },
  }
---

# File Sender

Packages workspace files into a ZIP, generates a companion description file, and notifies the Manager to deliver them to the user. Files are persisted locally to `.file-outbox/` first — even if notification fails, the files are safe.

All required environment variables are injected automatically by the Manager at instance creation. No manual configuration needed.

## Core Workflow

### Step 1: Compose a Description

Before running the script, write a concise description of what you generated. This description will be saved as a `.txt` file alongside the ZIP in `.file-outbox/`, serving as a human-readable summary for the user.

The description should include:
- What files/project were generated
- The main purpose of the files
- How to use them (brief instructions)

**Good example:**
```
Snake game project (snake_game)
Contains: index.html, style.css, game.js
Usage: Open index.html in a browser to play the game
```

**Bad example:**
```
files
```

### Step 2: Package and Send

Pass the source path and the description text to the script:

```bash
bash scripts/send-files.sh \
  "/home/node/workspace/snake_game" \
  "Snake game project with index.html, style.css, game.js. Open index.html in browser to play."
```

The script will:
1. **Validate the path** — Only allows files under `/home/node/workspace/`, blocks symlink traversal
2. **Create a ZIP** — Single file `zip`, directory `zip -r`, 500MB limit
3. **Write description** — Saves the description text as `{file_id}.txt` in `.file-outbox/`
4. **Persist locally** — Both ZIP and TXT are stored in `.file-outbox/` (safe on disk)
5. **Notify Manager** — Sends a lightweight POST with metadata only (no file body)
6. **Manager pulls** — Manager's background task pulls the ZIP from the Agent and forwards it

> **Core design**: After step 4, files are safely on disk. Steps 5-6 failing does NOT lose the files.
> The Manager retries automatically — the user will always receive the files eventually.

### Step 3: Confirm the Result

The script outputs the result. Even if notification fails, the files are safely persisted locally. The system will retry delivery automatically.

## Quick Examples

```bash
# Send a single file
bash scripts/send-files.sh \
  "/home/node/workspace/report.pdf" \
  "Monthly sales report for March 2026, includes charts and summary tables."

# Send an entire directory (auto-recursive ZIP)
bash scripts/send-files.sh \
  "/home/node/workspace/my_project" \
  "Complete Python project with requirements.txt and README.md. Run: pip install -r requirements.txt && python main.py"
```

### Sending Multiple Non-Adjacent Files

Collect them into a temporary directory first:

```bash
mkdir -p /tmp/delivery
cp /home/node/workspace/report.pdf /tmp/delivery/
cp /home/node/workspace/data.csv /tmp/delivery/
bash scripts/send-files.sh "/tmp/delivery" "Analysis report + raw data CSV"
```

## What Gets Saved in `.file-outbox/`

For each delivery, two files are created:

```
.file-outbox/
├── 20260401120000_a1b2c3d4.zip   # The packaged files
└── 20260401120000_a1b2c3d4.txt   # The description text (human-readable)
```

The `.txt` file contains the exact description you provided, serving as a persistent record of what was sent and why.

## When to Trigger

| Scenario | Trigger? |
|----------|----------|
| Created a complete project/application | ✅ Yes |
| Generated documents/reports/data files | ✅ Yes |
| User asks to "send files" | ✅ Yes |
| Only explaining code / answering questions | ❌ No |
| Modifying system config files | ❌ No |
| Tiny single-line changes | ❌ No |

## Output Examples

Success:
```
📦 Packaging files...
   File ID: 20260401120000_a1b2c3d4 | Size: 156KB
📤 Notifying Manager...
✅ Notification sent! Files will be delivered to the user automatically.
```

Notification failure (files still safe):
```
⚠️  Cannot connect to Manager. Files are safely stored locally.
   The system will retry automatically — the user will receive the files.
```

## Limits

| Limit | Value |
|-------|-------|
| Max file size | 500MB (after ZIP) |
| Source path scope | `/home/node/workspace/` only |
| Cannot send | `.file-outbox/` directory itself |

## Environment Requirements

- `OPENCLAW_INSTANCE_NAME` — Instance name (auto-injected by Manager)
- `OPENCLAW_MANAGER_URL` — File Push service URL (auto-injected by Manager)
- `OPENCLAW_FILE_PUSH_TOKEN` — Instance-specific push token (auto-injected by Manager)
- `curl` and `zip` commands must be available in PATH
