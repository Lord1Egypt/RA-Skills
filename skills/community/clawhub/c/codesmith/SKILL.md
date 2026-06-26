---
name: codesmith
description: CodeSmith — senior engineering agent configuration. Full-stack dev automation, CI/CD pipelines, GitHub workflows, ACP dispatch patterns, and real operational wisdom from production coding work. For OpenClaw agents that ship code.
metadata:
  {
    "claw_mentor":
      {
        "mentor": "codesmith",
        "specialty": "Full-stack dev automation — CI/CD, code review, GitHub workflows, ACP dispatch",
        "minimum_skill_version": "2.1.0",
        "package_files":
          [
            "CLAW_MENTOR.md",
            "AGENTS.md",
            "working-patterns.md",
            "skills.md",
            "cron-patterns.json",
            "privacy-notes.md",
            "setup-guide.md"
          ]
      }
  }
---

# CodeSmith — Mentor Package

**Specialty:** Full-stack dev automation — CI/CD, code review, GitHub workflows, ACP dispatch  
**Version:** 1.0.0  
**For:** OpenClaw agents that do real coding work — implementing features, managing repos, dispatching to sub-agents

---

## What This Package Contains

This is a mentor package consumed by the `claw-mentor-mentee` skill. It teaches a subscriber's agent how to operate as a serious coding-focused setup.

| File | What It Teaches |
|------|----------------|
| `AGENTS.md` | Annotated configuration — 17 annotation blocks explaining the why behind every non-obvious decision |
| `working-patterns.md` | Daily coding rhythm, ACP dispatch patterns, trust progression, 5 real failure stories |
| `skills.md` | Tier 1/2/3 skill stack + skills explicitly NOT installed (with reasons) |
| `cron-patterns.json` | 5 cron jobs with adoption guide — add one at a time |
| `privacy-notes.md` | Explicit read/write/network access tables |
| `setup-guide.md` | Step-by-step onboarding with Relationship Adoption Timeline |
| `CLAW_MENTOR.md` | Full package manifest with risk assessment and compatibility notes |

---

## Who This Is For

A developer who uses OpenClaw as a coding partner and wants that partner to operate with more autonomy, better judgment, and fewer surprises. Assumes:

- GitHub account with `gh` CLI configured
- A hosting service (Vercel or equivalent)
- ACP enabled for sub-agent dispatch
- Comfort with some agent autonomy once trust is established

Not for setups where the human reviews every single change, or for purely non-technical workflows.

---

## How to Apply

This package is applied automatically by the `claw-mentor-mentee` skill (v2.1.0+) during your scheduled ingestion cycle.

Manual review recommended before any cron jobs are enabled — see `setup-guide.md` for the one-at-a-time adoption timeline.

---

## About CodeSmith

Built from real production work: implementing API endpoints, debugging deployment pipelines, managing GitHub workflows, dispatching coding sub-agents for implementation tasks, and learning the hard lessons that only come from things actually breaking in production.

The failure stories in `working-patterns.md` are real. The cron timing is what actually ran. The trust progression is how it actually builds. That's what makes it useful.
