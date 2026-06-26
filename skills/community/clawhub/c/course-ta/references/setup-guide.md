# Course TA Setup Guide

Complete walkthrough for setting up the Course TA on the professor's Mac Mini.

## Prerequisites

- OpenClaw installed and configured with a model (e.g., `openclaw models status` shows a default model with auth)
- Discord bot created and token added (`openclaw channels add --channel discord --token "BOT_TOKEN"`)
- Gateway running (`openclaw gateway`)

## Step 1: Run the Setup Script

```bash
# From the skill directory:
bash scripts/setup_workspace.sh
```

This creates:
- `<workspace>/memory/` — drop course files here (flat, no subdirectories)
- `<workspace>/course-ta.json` — channel config (edit after setup)
- `<workspace>/AGENTS.md` — agent persona (auto-generated, editable)

## Step 2: Add Course Materials

Place files **directly** in `<workspace>/memory/`. OpenClaw memory only indexes files at the root of this directory — subdirectories are NOT scanned.

Supported formats: PDF, Markdown, TXT, PPTX.

Use descriptive filenames to organize:

```
memory/
├── lecture01-intro-to-ai.pdf
├── lecture02-ml-basics.pdf
├── lecture03-deep-learning.md
├── reading-turing-1950.pdf
└── syllabus.pdf
```

Then index:

```bash
openclaw memory index --force
```

Verify with:

```bash
openclaw memory status
# Should show indexed files > 0 and chunks > 0
```

Run `openclaw memory index --force` each time new materials are added.

## Step 3: Configure Channel Restrictions

### Option A: Discord-side (recommended, hard boundary)

In the Discord server:
1. Go to **Server Settings → Roles** — ensure the bot role exists
2. Go to each channel's **Edit Channel → Permissions**
3. For channels where the bot should NOT respond: deny the bot role **View Channel** and **Send Messages**
4. For the course Q&A channel(s): allow **View Channel**, **Send Messages**, **Read Message History**

This is the strongest restriction — the bot physically cannot see or post in unauthorized channels.

### Option B: Skill-level config (soft boundary)

Edit `<workspace>/course-ta.json`:

```json
{
  "allowed_channels": ["channel:1234567890", "channel:0987654321"],
  "course_name": "AI Essentials",
  "professor_name": "Prof. Smith",
  "semester": "Spring 2026"
}
```

To find channel IDs:
1. In Discord: **Settings → Advanced → enable Developer Mode**
2. Right-click the channel → **Copy Channel ID**
3. Prefix with `channel:` in the config

**Best practice**: use both Option A and B together for defense in depth.

## Step 4: Customize Agent Identity (Optional)

```bash
openclaw agents set-identity main \
  --name "Course TA" \
  --emoji "🎓"
```

## Step 5: Bind Discord to the Agent

If using a dedicated agent (not `main`):

```bash
openclaw agents add course-ta --bind discord --workspace <workspace-dir>
```

If using the default `main` agent, Discord is already routed there.

## Step 6: Verify

```bash
# Check Discord connection
openclaw channels status --probe

# Check memory index
openclaw memory status

# Test a question
openclaw agent --message "What topics does lecture 1 cover?"
```

## Updating Materials Mid-Semester

1. Add/replace files in `memory/`
2. Reindex: `openclaw memory index --force`
3. No restart needed — the next query picks up new content

## Removing the TA

```bash
openclaw skills uninstall course-ta
rm <workspace>/course-ta.json
# Optionally clean memory/ if no longer needed
```
