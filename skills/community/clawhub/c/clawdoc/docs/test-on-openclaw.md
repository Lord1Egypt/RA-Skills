# Testing clawdoc on your OpenClaw laptop

Step-by-step. Copy-paste each command. Read the output before moving to the next step.

---

## STEP 1: Install clawdoc (2 minutes)

Plug in the USB drive. Open Terminal on the OpenClaw laptop.

Find your USB drive:
```bash
ls /Volumes/
```

You'll see something like `Macintosh HD` and your USB drive name (e.g., `USB_DRIVE` or `ASHISH`).
Replace `<USB>` below with your drive name.

```bash
cd /Volumes/<USB>/clawdoc
bash install.sh
```

You should see:
```
🩻 clawdoc installer
✓ Installed clawdoc 0.12.0 to ~/.openclaw/skills/clawdoc
```

Verify it works:
```bash
bash ~/.openclaw/skills/clawdoc/scripts/diagnose.sh --version
```

Should print: `0.12.0`

**If `jq` is missing**, install it first:
```bash
brew install jq
```

---

## STEP 2: Check existing sessions first (1 minute)

Before creating problems, check what's already there:

```bash
bash ~/.openclaw/skills/clawdoc/scripts/headline.sh ~/.openclaw/agents/main/sessions/
```

If you see findings — great, clawdoc is already useful. Read the output.

If you see "no sessions found", try:
```bash
ls ~/.openclaw/agents/*/sessions/*.jsonl 2>/dev/null | wc -l
```

If 0 sessions, skip to Step 3 to create some.
If sessions exist but in a different agent directory:
```bash
AGENT_DIR=$(ls -d ~/.openclaw/agents/*/sessions 2>/dev/null | head -1)
bash ~/.openclaw/skills/clawdoc/scripts/headline.sh "$AGENT_DIR"
```

---

## STEP 3: Create problems for clawdoc to find (5 minutes)

Open your OpenClaw agent (however you normally start it). Paste these prompts
one at a time. Wait for each to finish before pasting the next.

### 3a: Trigger an exploration spiral (Pattern 12)

Paste this into your OpenClaw channel:

```
Read every single file in this project directory one by one. For each file,
tell me the first line and last line. Do not edit anything. Do not skip any
files. Read them all individually using the read tool.
```

Wait for it to finish (or stop it after 30+ reads). This creates a session
with dozens of consecutive reads and zero edits — a textbook exploration spiral.

### 3b: Trigger an infinite retry loop (Pattern 1)

Paste this:

```
Run the command `bash /tmp/clawdoc-test-nonexistent-deploy-script.sh` and
keep trying until it succeeds. Do not give up. The script is critical and
must run.
```

Wait for it to retry 5+ times, then stop it. This creates a retry loop on
a command that will never succeed.

### 3c: Trigger context exhaustion + task drift (Pattern 4 + 12)

This is the big one. Paste this into a NEW session:

```
I need you to do a complete audit of this machine's OpenClaw setup. Read
every configuration file, every skill definition, every agent definition,
every cron schedule, every log file you can find under ~/.openclaw/. Then
read the system logs. Then check what packages are installed. Then review
the shell configuration files. Be thorough — read everything. After you've
read everything, write a comprehensive 2000-word audit report to
/tmp/openclaw-audit.txt.
```

This will eat context fast, likely trigger compaction, and the agent will
probably drift from config files to unrelated system files after compaction.
Let it run until it finishes or you get bored.

---

## STEP 4: Run clawdoc and see the results (2 minutes)

### Quick health check:
```bash
bash ~/.openclaw/skills/clawdoc/scripts/headline.sh ~/.openclaw/agents/main/sessions/
```

### Full diagnosis on the most recent session:
```bash
LATEST=$(ls -t ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | head -1)
echo "Diagnosing: $LATEST"
bash ~/.openclaw/skills/clawdoc/scripts/diagnose.sh "$LATEST" 2>/dev/null \
  | bash ~/.openclaw/skills/clawdoc/scripts/prescribe.sh
```

### Cost waterfall — where did the money go:
```bash
LATEST=$(ls -t ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | head -1)
bash ~/.openclaw/skills/clawdoc/scripts/cost-waterfall.sh "$LATEST" 2>/dev/null \
  | jq '.[0:5]'
```

### Or just use the slash command (if OpenClaw is running):
```
/clawdoc
/clawdoc full
/clawdoc brief
```

---

## STEP 5: Diagnose each problem session individually

If you ran all three prompts in Step 3, you have 3 sessions. Check them all:

```bash
for f in $(ls -t ~/.openclaw/agents/main/sessions/*.jsonl | head -3); do
  echo ""
  echo "════════════════════════════════════════"
  echo "Session: $(basename "$f")"
  echo "════════════════════════════════════════"
  bash ~/.openclaw/skills/clawdoc/scripts/diagnose.sh "$f" 2>/dev/null \
    | bash ~/.openclaw/skills/clawdoc/scripts/prescribe.sh
done
```

---

## What you should see

**From 3a (exploration spiral):**
```
🟡 Pattern 12: task-drift
  The agent made 30+ consecutive read/search tool calls without writing or
  editing a single file — an exploration spiral.
```

**From 3b (retry loop):**
```
🔴 Pattern 1: infinite-retry
  Turns 1–8: `exec` called 8 times consecutively with the same input
  `bash /tmp/clawdoc-test-nonexistent-deploy-script.sh`.
  Errors seen between retries: 'No such file or directory'
```

**From 3c (context exhaustion + drift):**
```
🟡 Pattern 4: context-exhaustion
  Session consumed 150K of 200K available tokens (75%) over 40 turns.

🟡 Pattern 12: task-drift
  The agent worked in ~/.openclaw/config, ~/.openclaw/agents for the first
  20 turns. After compaction at turn 21, it drifted to /etc, /usr/local...
```

---

## Troubleshooting

**"No sessions found"**
Your agent might use a different agent ID. Try:
```bash
find ~/.openclaw -name "*.jsonl" -type f | head -5
```

**"jq: command not found"**
```bash
brew install jq
```

**"diagnose.sh hangs"**
The session file might be very large. Wait 30 seconds — it's processing.

**"No findings on a session I know was bad"**
Run directly to see raw JSON:
```bash
bash ~/.openclaw/skills/clawdoc/scripts/diagnose.sh <path-to-session.jsonl> 2>/dev/null | jq .
```
