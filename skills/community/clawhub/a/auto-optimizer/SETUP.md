# Auto-Optimizer Setup Guide

## For OpenClaw Users (Easiest)

Tell your agent:

```
"Install and set up auto-optimizer for cold outreach"
"Set up auto-optimizer on my prediction strategy file"
"Optimize my system prompt at ./prompts/assistant.md"
```

That's it. Your agent reads the SKILL.md, installs the skill, sets up the files, picks the right mode, and runs the loop. You get results in under 5 minutes.

---

## For Manual Setup (Human-Friendly)

### 1. Install

```bash
clawhub install auto-optimizer
```

Or clone directly:
```bash
git clone https://github.com/rmarji/autoresearch-openclaw.git
cp -r autoresearch-openclaw/skills/auto-optimizer ./skills/
```

### 2. Make sure you're in a git repo

The optimizer uses git to revert bad iterations. If you're not in a git repo:

```bash
cd your-project
git init && git add . && git commit -m "baseline"
```

### 3. Try a demo first

```bash
# Run the outreach demo (no files needed, creates everything)
./skills/auto-optimizer/auto-optimizer.sh --demo outreach --budget 5

# Or the prompt quality demo
./skills/auto-optimizer/auto-optimizer.sh --demo prompt --budget 5 --eval-mode binary
```

### 4. Run on your own file

**If you have a measurable metric (test score, accuracy, etc.):**
```bash
./skills/auto-optimizer/auto-optimizer.sh \
  --file ./your-file.md \
  --metric "bash ./your-metric.sh" \
  --budget 10
```

**If you want yes/no quality evaluation (copy, prompts, UX):**

First create an evals file:
```bash
cat > ./my-evals.md << 'EOF'
1. Is the hook under 15 words?
2. Is there exactly one call-to-action?
3. Does it mention a specific outcome or number?
4. Is the total under 150 words?
5. Does it address a specific pain point?
EOF
```

Then run:
```bash
./skills/auto-optimizer/auto-optimizer.sh \
  --eval-mode binary \
  --file ./your-file.md \
  --evals ./my-evals.md \
  --batch-size 10 \
  --budget 10
```

### 5. Not sure? Use the wizard

```bash
./skills/auto-optimizer/auto-optimizer.sh --wizard
```

---

## For AI Agents Setting This Up

Follow these exact steps. No ambiguity.

### Prerequisites check

```bash
# Check git
git --version || echo "MISSING: install git"

# Check claude CLI
claude --version || echo "MISSING: npm install -g @anthropic-ai/claude-code"

# Check bc and jq (used by the script)
bc --version && jq --version || echo "MISSING: apt-get install bc jq"
```

### Step 1: Install the skill

```bash
clawhub install auto-optimizer
# Installs to ./skills/auto-optimizer/
```

### Step 2: Ensure the target file is in a git repo

```bash
# Check if target dir is a git repo
git -C /path/to/target/dir rev-parse --show-toplevel 2>/dev/null || {
  cd /path/to/target/dir
  git init
  git add .
  git commit -m "baseline before auto-optimizer"
}
```

### Step 3: Determine the right mode

| Situation | Mode | Required flags |
|-----------|------|----------------|
| File with a test command | scalar | `--metric "your test cmd"` |
| Copy / prompt / UX quality | binary | `--eval-mode binary --evals ./evals.md` |
| Not sure | wizard | `--wizard` |

### Step 4: Run

**Scalar:**
```bash
./skills/auto-optimizer/auto-optimizer.sh \
  --file /path/to/target.md \
  --metric "bash /path/to/metric.sh" \
  --goal maximize \
  --budget 10 \
  --session "my-optimization-$(date +%Y%m%d)"
```

**Binary:**
```bash
# Create evals file first with numbered yes/no criteria
cat > /tmp/my-evals.md << 'EOF'
1. [Criterion 1 — yes/no question]
2. [Criterion 2 — yes/no question]
3. [Criterion 3 — yes/no question]
4. [Criterion 4 — yes/no question]
5. [Criterion 5 — yes/no question]
EOF

./skills/auto-optimizer/auto-optimizer.sh \
  --eval-mode binary \
  --file /path/to/target.md \
  --evals /tmp/my-evals.md \
  --batch-size 10 \
  --budget 10 \
  --session "my-optimization-$(date +%Y%m%d)"
```

### Step 5: Report results back

Results are saved to:
```
./skills/auto-optimizer/results/SESSION_NAME/
├── report.md          # Full summary
├── results.tsv        # Iteration-by-iteration log
├── best.md            # Best version of the file
└── hypothesis_log.jsonl  # What was tried and why
```

Read the report:
```bash
cat ./skills/auto-optimizer/results/SESSION_NAME/report.md
```

---

## Common Error Recovery

| Error | Fix |
|-------|-----|
| "Not a git repo" | `git init && git add . && git commit -m "baseline"` |
| "Metric command failed" | Test standalone: `bash ./metric.sh` — must output a float |
| "claude CLI not found" | `npm install -g @anthropic-ai/claude-code` |
| "--evals required" | Create a file with numbered yes/no criteria, pass via `--evals` |
| "program.md.template not found" | Reinstall: `clawhub install auto-optimizer` |
| "Budget too low" | Use minimum `--budget 5` |
