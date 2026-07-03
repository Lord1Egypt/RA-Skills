# Geordi build loop

This is the sanitized public form of the former Geordi build-pipeline workflow.

## Loop

1. Load global agent context first from `~/.agents/AGENTS.md` or `GEORDI_AGENTS_FILE`.
2. Load project context before editing: repo instructions, PRD/story text, tests, current git status, and relevant files.
3. Create one bounded mission with a single acceptance command.
4. Run the mission through Codex or Droid.
5. Verify separately with the acceptance command.
6. If verification fails, preserve the log and create a smaller repair mission.
7. Commit only after the acceptance command passes and the diff is reviewed.
8. Update project context or notes with what changed and any follow-up risks.

## Retry rule

Retry a failed mission at most three times. Each retry should include the exact failure log and a narrower instruction. After three failures, mark it blocked and ask for operator input.

## Receipt rule

Every completed mission should leave:

- mission prompt
- agent output log
- verification log
- git status before and after
- concise summary of files changed
