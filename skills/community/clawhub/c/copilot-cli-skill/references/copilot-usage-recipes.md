# Copilot CLI usage recipes in OpenClaw

## 1) Quick implementation

- Tool: `exec`
- Params:
  - `pty:true`
  - `workdir:/path/to/repo`
  - `command:"copilot -p \"Implement X and add tests\" --allow-all-tools"`

## 2) Code review pass

- Tool: `exec`
- Params:
  - `pty:true`
  - `workdir:/path/to/repo`
  - `command:"copilot -p \"Review current changes and list critical issues\" --allow-tool 'shell(git)'"`

## 3) Work on a GitHub issue

- Tool: `exec`
- Params:
  - `pty:true`
  - `workdir:/path/to/repo`
  - `command:"copilot -p \"Work on issue https://github.com/owner/repo/issues/123 in a new branch\" --allow-all-tools"`

## 4) Create a pull request

- Tool: `exec`
- Params:
  - `pty:true`
  - `workdir:/path/to/repo`
  - `command:"copilot -p \"Create a PR for the current branch with a descriptive title\" --allow-tool 'shell(git)' --allow-tool 'shell(gh)'"`

## 5) Long task with monitoring

- Start:
  - `exec(background:true, pty:true, workdir, command:"copilot -p \"...\" --allow-all-tools")`
- Monitor:
  - `process list`
  - `process poll <sessionId>`
  - `process log <sessionId>`
- Interact:
  - `process submit <sessionId> "yes"`
- Stop if needed:
  - `process kill <sessionId>`

## 6) Scoped safe execution

- Tool: `exec`
- Params:
  - `pty:true`
  - `workdir:/path/to/repo`
  - `command:"copilot -p \"Refactor the auth module\" --allow-all-tools --deny-tool 'shell(rm)' --deny-tool 'shell(git push)'"`

## Common failures

- `copilot: command not found`
  - Install: `npm install -g @github/copilot`
- auth/login errors
  - Re-run `copilot` and complete `/login` flow, or set `COPILOT_GITHUB_TOKEN`.
- wrong repo modified
  - Ensure `exec.workdir` points to intended project.
- tool approval blocking
  - Use `--allow-all-tools` or specific `--allow-tool` flags for programmatic use.
