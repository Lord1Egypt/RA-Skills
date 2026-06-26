# Background Agents And Bugbot - Cursor

Use this file when the user is considering remote execution or GitHub-connected review workflows.

## Background Agents

Treat Background Agents as remote execution, not as "Cursor but later."
Operationally they change several things at once:
- code can be cloned or fetched through GitHub-connected flows
- commands can run outside the local machine
- network access and remote compute become part of the trust boundary

Use them only when:
- the task is long-running enough to justify remote execution
- GitHub integration is acceptable
- the user agrees to the remote trust and review model

## Bugbot

Treat Bugbot as a review surface, not as automatic truth.
It is useful when:
- the unit of work is a pull request
- the goal is finding bugs or regressions before merge
- the user wants structured review comments instead of another implementation pass

Use repo guidance such as `.cursor/BUGBOT.md` only when it exists and is actually maintained.

## Review Discipline

- inspect Background Agent output before merging or applying follow-up changes locally
- inspect Bugbot findings before acting on them
- separate "helpful signal" from "approved change"
- if remote work touched the repo, compare the result against local expectations before continuing

## Red Flags

- enabling Background Agents just to avoid local setup work
- treating GitHub app access as a harmless toggle
- letting review comments trigger more remote work without clarifying ownership
- assuming privacy-sensitive repos are safe just because the feature is official
