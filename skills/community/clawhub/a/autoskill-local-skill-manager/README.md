# AutoSkill Local Skill Manager

AutoSkill Local Skill Manager is an installable Agent Skill for maintaining
personal local skill files. It helps an agent proactively notice reusable
workflow knowledge, personal preferences, project conventions, and team rules,
search for similar local skills, and propose whether to discard, improve, merge,
or create a skill.

The skill is intentionally storage-agnostic. It does not depend on the AutoSkill
project runtime, APIs, vector stores, databases, or repository layout. It works
with ordinary local skill folders that contain `SKILL.md` files.

The default audience is personal. A useful skill does not need to be broadly
applicable to other users; it only needs to be reusable for the intended user,
team, or workspace, with explicit confirmation before anything is written.

## Install

Install with the Skills CLI:

```bash
npx skills add ECNU-ICALK/autoskill-skill
```

Install a specific skill explicitly:

```bash
npx skills add ECNU-ICALK/autoskill-skill --skill autoskill
```

## What It Does

- Detects reusable personal, team, or public skill material proactively during or
  after meaningful sessions.
- Runs extraction checks at natural pauses, task boundaries, and session-end reviews.
- Labels each candidate's intended audience and portability limits before asking
  for approval.
- Offers candidate skill titles, lets the user choose none, or accepts a custom
  topic before full extraction when the direction is ambiguous.
- Rechecks the reusable-skill boundary and similar-skill search after a chosen
  title or custom topic, so topic selection does not bypass quality gates.
- Preserves language consistency: Chinese source interactions produce Chinese
  skill drafts, English source interactions produce English drafts, and updates
  keep the target skill's dominant language.
- Searches local skills first, then uses external sources such as `npx skills
  find <query>` and skills.sh when external discovery is requested or duplicate
  risk is high.
- Chooses between discard, improve, merge, and create.
- Fully drafts proposed skill contents or update diffs before asking for user
  approval.
- Requires user confirmation before creating, updating, deleting, importing,
  installing, enabling, or materially rewriting skills.
- Shows exact target paths and proposed diffs before updating existing skills.
- Keeps extraction and maintenance work in the background when possible so it does
  not block the user's main task.

## Skill Contents

```text
SKILL.md
agents/openai.yaml
```

## Links

- Source repository: https://github.com/ECNU-ICALK/autoskill-skill
- Original project: https://github.com/ECNU-ICALK/AutoSkill
