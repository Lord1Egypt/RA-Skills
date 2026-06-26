# Troubleshooting

## Auth Not Working

Symptoms:
- Codex cannot start the run you expect
- login state is unclear

Checks:
1. run `codex login status`
2. decide whether this workflow should use existing login or explicit `OPENAI_API_KEY`
3. avoid guessing by scraping secrets from files

## Wrong Directory or Wrong Repo

Symptoms:
- file search looks wrong
- Codex edits or analyzes an unexpected project

Checks:
1. verify `pwd`
2. rerun with `-C /path/to/repo`
3. confirm `git status --short` before any further write-capable run

## Dirty Worktree Confusion

Symptoms:
- Codex output mixes user changes and agent changes
- review diff becomes noisy

Checks:
1. inspect `git status --short`
2. separate user-owned dirt from the agent task
3. avoid destructive cleanup unless the user explicitly asks

## Sandbox or Approval Dead End

Symptoms:
- commands stall at approval boundaries
- expected writes fail under read-only mode

Checks:
1. confirm the current sandbox and approval policy
2. widen privilege only as much as the task actually needs
3. if the run is non-interactive, make sure the environment truly matches the chosen trust level

## MCP Scope Creep

Symptoms:
- the run suddenly depends on external tools or data

Checks:
1. list MCP servers in play
2. remove any server not required for the current task
3. prefer the narrowest local workflow over broad remote access

## Cloud Apply Risk

Symptoms:
- a remote Codex task exists and the user wants to merge it locally fast

Checks:
1. inspect `codex cloud diff TASK_ID`
2. confirm the target repo and branch
3. apply only after the diff is understood and the local tree is ready
