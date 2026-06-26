# Install And Surfaces - Cursor

Use this file when the user needs to choose the right Cursor operating surface before solving the actual coding problem.

## Surface Map

### Editor
Use the editor when:
- the user is already inside Cursor
- the work benefits from direct codebase context, inline edits, and local iteration
- you need to inspect how rules and context actually apply inside the repo

### `cursor-agent`
Use the CLI when:
- the task needs repeatable terminal execution
- the user wants automation or non-interactive runs
- you need a clean, explicit repo and command boundary

### Background Agent
Use it when:
- the task is longer-running and GitHub-connected execution is acceptable
- remote command execution is worth the trust tradeoff
- the user wants work to continue outside the local editor session

### Bugbot
Use it when:
- the job is review-first and tied to pull requests
- the user wants a separate review surface instead of another implementation pass
- GitHub-connected review output is acceptable

## Choosing Quickly

Ask only the questions that change the answer:
- Does this need to stay local?
- Does it need unattended execution?
- Is the goal implementation or review?
- Is the repo already open in Cursor?

## Practical Rule

Prefer the smallest surface that can solve the problem:
1. editor for local interactive work
2. `cursor-agent` for bounded automation
3. Background Agent for explicitly approved remote execution
4. Bugbot for review-specific GitHub workflows
