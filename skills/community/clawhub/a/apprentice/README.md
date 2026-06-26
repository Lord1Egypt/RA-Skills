# 🎓 apprentice

> Watch me once. Do it forever.

![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![No External Calls](https://img.shields.io/badge/external%20calls-none-brightgreen)
![Stdlib Only](https://img.shields.io/badge/dependencies-stdlib%20only-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

The entire history of computing asks: *What do you want?*

Apprentice asks: *Can I watch?*

You do a task once. You narrate it naturally. Apprentice observes, understands your intent, and turns it into a permanent repeatable workflow your agent can run forever — with your exact sequence, your exact decisions, your exact variables.

**This is Programming by Demonstration. For the first time, it actually works.**

---

## Install

```bash
clawhub install apprentice
```

---

## How It Works

### Teach it (once)
```
You: "Watch me set up a new project"
[You do the task, narrate out loud]
You: "Done"
```

### Run it (forever)
```
You: "New project setup for analytics-redesign"
Agent: [runs all your steps automatically with PROJECT_NAME=analytics-redesign]
```

That's it. No code. No config. No forms. Just show it.

---

## Trigger Phrases

**Start observation:**
```
"Watch me"
"Apprentice mode"
"Learn this"
"Remember how I do this"
"I'll show you"
```

**Stop observation:**
```
"Done"
"Stop watching"
"Got it?"
"End lesson"
```

**Run a workflow:**
```
"Run [workflow-name]"
"[workflow-name] with PROJECT_NAME=my-app"
"Replay [workflow-name]"
"What have you learned?"
```

---

## Full Example

**Teaching:**
```
You: "Watch me — I'm going to show you how I set up a new project"

You: "First I create the directory called my-app"
     > mkdir projects/my-app

You: "Then I copy the starter template"
     > cp -r ~/templates/react-starter projects/my-app

You: "I update the README with the project name"
     > sed -i 's/TEMPLATE_NAME/my-app/g' README.md

You: "Git init and connect to GitHub"
     > git init && git remote add origin git@github.com:myorg/my-app.git

You: "Done"
```

**Apprentice responds:**
```
🎓 OBSERVATION COMPLETE — New Project Setup

Steps I learned:
  1. Create project directory with PROJECT_NAME
  2. Copy react-starter template
  3. Replace template placeholder with PROJECT_NAME in README
  4. Initialize git + connect remote for PROJECT_NAME

Variables detected:
  • PROJECT_NAME (example: my-app)
  • GIT_ORG (example: myorg)

Saved to: apprentice/workflows/new-project-setup/
Run with: "new project setup for [name]"
```

**Next time:**
```
You: "New project setup for client-dashboard"
Agent: [runs all 4 steps with PROJECT_NAME=client-dashboard]
```

---

## Your Workflow Library

After a few weeks of use, you have a personal operating system:

```
🎓 LEARNED WORKFLOWS (7):
  ✅ morning-routine          6 steps  learned: 2026-01-15
  ✅ new-project-setup        5 steps  learned: 2026-01-18
  ✅ weekly-report            8 steps  learned: 2026-01-22
  ✅ deploy-staging           4 steps  learned: 2026-02-01
  ✅ client-onboarding       12 steps  learned: 2026-02-05
  ✅ code-review-prep         3 steps  learned: 2026-02-10
  ✅ end-of-day-shutdown      5 steps  learned: 2026-02-14
```

No two users' libraries are the same. This is your agent, shaped by what only you do.

---

## What Makes a Good Observation

✅ **Talk out loud** — "Now I'm updating the config with the API key"
✅ **Explain why** — "I always do this before deploying"
✅ **Name variables** — "The PROJECT_NAME here would change each time"
✅ **Mark the end** — "And that's the whole thing, every time"

---

## Refining Workflows

After a run, you can correct or extend:

```
"That step was wrong — here's how it should be: ..."
"Add a step after step 3: ..."
"Watch me do new-project-setup again"
```

---

## CLI Usage

```bash
# Start observation
python3 skills/apprentice/scripts/observe.py start "new project setup"

# Stop and capture session
python3 skills/apprentice/scripts/observe.py stop

# Synthesize into workflow
python3 skills/apprentice/scripts/synthesize.py new-project-setup --preview

# List workflows
python3 skills/apprentice/scripts/run.py --list

# Preview a workflow
python3 skills/apprentice/scripts/run.py new-project-setup --preview

# Run it
python3 skills/apprentice/scripts/run.py new-project-setup PROJECT_NAME=my-app

# Dry run
python3 skills/apprentice/scripts/run.py new-project-setup --dry-run
```

---

## File Structure

```
apprentice/
├── SKILL.md                    ← OpenClaw skill instructions
├── README.md                   ← This file
├── scripts/
│   ├── observe.py              ← Observation session manager
│   ├── synthesize.py           ← Turns observations into workflow skills
│   └── run.py                  ← Executes and manages learned workflows
└── workflows/                  ← Your personal workflow library
    └── (grows as you teach it)
```

Each learned workflow generates:
```
workflows/your-workflow-name/
├── SKILL.md           ← Valid OpenClaw skill (publishable to ClawHub)
├── run.sh             ← Execution script
├── observation.json   ← Raw observation (editable)
└── run_log.json       ← Execution history
```

---

## Security

- **Zero external calls.** Everything is local.
- **No credentials accessed.** Apprentice only sees what you tell it.
- **You review before saving.** Every synthesis requires your approval.
- **Stdlib only.** Three Python files, no pip dependencies.

---

## Philosophy

When you describe what you want, you lose nuance — the order matters, the edge cases matter, the "I always do this first" matters. When Apprentice watches, it captures all of it, exactly as you actually do it.

Your agent doesn't get smarter by being trained on more data. It gets smarter by watching you.

---

## License

MIT — use freely, modify, share, contribute.
