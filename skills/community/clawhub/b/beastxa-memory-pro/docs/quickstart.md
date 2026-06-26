# Quick Start — 5 Minutes to Never Forget Again

## Step 1: Install

```bash
clawhub install beastxa-memory-pro
```

Or clone from GitHub:
```bash
git clone https://github.com/beastxa6-668/beastxa-memory-pro.git
cp -r beastxa-memory-pro ~/.openclaw/skills/
```

## Step 2: Run Setup

```bash
cd ~/.openclaw/skills/beastxa-memory-pro
bash scripts/install.sh
```

The installer will:
1. Create `memory/` directory structure
2. Generate session-notes template
3. Configure compaction enhancement
4. Set up daily + weekly maintenance crons

## Step 3: (Optional) Split Existing Memory

If you already have a large MEMORY.md:

```bash
python3 scripts/split_memory.py
```

This reads your MEMORY.md, splits it by topic into `memory/topics/`, and creates an index. Your original file stays untouched.

## Step 4: Verify

```bash
bash scripts/verify.sh
```

You should see all green checkmarks.

## That's It

From now on:
- Your agent auto-saves context before each compaction
- Daily cron organizes today's notes into topic files (23:30)
- Weekly cron deduplicates and trims (Sunday 23:00)
- You never have to think about memory management again
