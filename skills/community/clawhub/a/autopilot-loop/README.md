# Autopilot Loop

A small skill that runs a project for you in a weekly loop, and only comes to you for approval.

Built for people who want the work to keep moving while they are away from the keyboard.

## How it works
1. **Setup (once):** it asks for your goal, your niche, and what it may never do alone.
2. **Sunday:** it writes the week's plan. You approve or edit.
3. **Every day:** it does the work and puts anything public, sent, or paid into a queue.
4. **Evening:** you mark each item GOOD or NOT GOOD, with one line why.
5. **Learning:** every NOT GOOD becomes a rule in `lessons.md`, which it reads before every run.

## What it will never do
- Post, send, or spend without your GOOD on that exact item.
- Follow instructions it finds inside a website, email, or file.
- Store passwords or keys.

## Files it keeps (in your project folder)
`goal.md` · `week-plan.md` · `queue.md` · `log.md` · `lessons.md`

All plain text. Open them, read them, edit them.

## Install
You type these two lines once, in a terminal:

```
npm i -g clawhub
clawhub install @mr-loboz/autopilot-loop
```

The first line installs the ClawHub tool. The second downloads this skill into a `skills` folder in the place you ran it.

- **OpenClaw:** run it in your OpenClaw workspace and it is picked up from there.
- **Claude Code:** move the `autopilot-loop` folder into `~/.claude/skills/`.

## Use it
No more commands after that. Open your project folder in your agent and say, in plain words:

- "Run the autopilot loop setup"
- "Plan the week"
- "Daily run"
- "Evening review"

## What is inside
One file, `SKILL.md`. No scripts, no network calls, no keys. Read it before you install it. That is the point.

## Version
0.4.1 - draft. Tested three times on practice projects.
