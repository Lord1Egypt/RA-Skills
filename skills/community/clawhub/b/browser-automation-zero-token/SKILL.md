---
name: browser-automation-zero-token
description: >
  Build and run low-code browser automation workflows with agent-browser CLI and reusable
  skills, especially for repetitive web tasks like 登录、签到、表单填写、固定点击流程、状态保存、
  重复网页操作, or when the user says things like “做浏览器自动化”, “用 agent-browser 跑网页流程”,
  “0 token 浏览器自动化”, “把网页重复操作固化成 skill”, “做自动签到 skill”, or
  “用 CLI + Skill 搭建 AI 浏览器自动化框架”.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["agent-browser", "npm"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "agent-browser",
              "bins": ["agent-browser"],
              "label": "Install agent-browser CLI (npm)",
            },
          ],
      },
  }
---

# Browser Automation Zero Token

Use `agent-browser` plus OpenClaw skills to turn repeatable browser tasks into reusable, low-maintenance workflows.

## When To Use

Use this skill for repeatable browser workflows such as:

- daily site sign-in
- repeated login + click flows
- dashboard checks
- fixed form-filling routines
- internal admin flows

Prefer this pattern when Playwright/Puppeteer feels too heavy, selectors are brittle, or repeated screenshot/tool loops waste tokens.

## Core Workflow

Always think in this loop:

1. **OPEN** — open the target page
2. **SNAPSHOT** — inspect page structure and collect current `@refs`
3. **INTERACT** — click / fill / select using `@refs`
4. **VERIFY** — re-snapshot or check page state after each meaningful change
5. **REPEAT** — continue until the business task is done
6. **CLOSE** — close the browser session cleanly

Short form:

`OPEN → SNAPSHOT → INTERACT → VERIFY → REPEAT → CLOSE`

## Preconditions

Before using this skill, verify:

- `agent-browser` is installed
- browser runtime/dependencies are installed
- the target site allows normal browser interaction
- credentials are available if login is required
- the user is authorized to automate the target site

Install CLI:

```bash
npm install -g agent-browser
agent-browser install --with-deps
agent-browser --version
```

Optional ecosystem install:

```bash
clawhub install openclaw-skills-browserautomation-skill
```

## Base Command Set

Use this minimal loop:

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e<n>
agent-browser fill @e<n> "text"
agent-browser state save auth.json
agent-browser state load auth.json
agent-browser close
```

Important rule: `@refs` come from the latest snapshot. After navigation or major DOM changes, snapshot again. More command notes live in `references/source-notes.md`.

## Operating Rules

### 1. Snapshot before interacting

Do not guess refs. Always obtain fresh `@refs` from `agent-browser snapshot -i` before click/fill/select actions.

### 2. Re-snapshot after state changes

After login, route changes, modal opens, tab switches, or dynamic content loads, run snapshot again.

### 3. Prefer refs over brittle selectors

Use `@e<n>` from snapshots whenever possible. Fall back to complex selectors only when refs or semantic locators are insufficient.

### 4. Save auth state for recurring tasks

If the workflow requires login and will be reused:

```bash
agent-browser state save auth.json
agent-browser state load auth.json
```

This is often the difference between “semi-automated” and “truly one-command repeatable.”

### 5. Verify, don’t assume

After key actions, confirm progress using one or more of:

- another snapshot
- `agent-browser get url`
- `agent-browser get title`
- visible text checks
- screenshots for debugging

## Zero-Token Execution Pattern

Use zero-token mode when the workflow is already known and stable:

1. discover the workflow once
2. capture the working CLI sequence
3. store it in a skill or task markdown
4. rerun it directly without repeated AI reasoning

Example:

```bash
agent-browser open https://example.com/login
agent-browser snapshot -i
agent-browser fill @e3 "username"
agent-browser fill @e4 "password"
agent-browser click @e5
agent-browser snapshot -i
agent-browser click @e21
agent-browser close
```

## Build A Reusable Site Skill

When the user wants to turn one website flow into a reusable skill:

1. identify the business goal
2. map the page flow once
3. note where refs must be refreshed
4. decide whether auth state should be saved/loaded
5. write the repeatable steps into a concise skill
6. document failure points and re-snapshot requirements

A good site skill should capture:

- target site / task
- prerequisites
- ordered browser steps
- verification points
- state save/load strategy
- caveats about changing refs

## Example: Daily Sign-In Flow

```md
---
name: auto-signin-example
description: Automatically sign in to example.com using agent-browser CLI.
---

# Auto Sign-In Example

## Workflow
1. Open the login page.
2. Snapshot interactive elements.
3. Fill username and password using current refs.
4. Click the login button.
5. Re-snapshot after navigation.
6. Click the sign-in button.
7. Save state if reuse is needed.
8. Close the browser.
```

## Debugging

If the automation breaks, check in this order:

1. was a fresh snapshot taken?
2. did the page navigate or re-render?
3. did login fail silently?
4. did the saved state expire?
5. did a ref change?
6. does the flow need an explicit wait?

For command examples, see `references/source-notes.md`.

## When Not To Use This Pattern

Avoid overcommitting to zero-token browser automation when:

- the task requires heavy judgment each run
- the page changes unpredictably every time
- anti-bot controls block normal automation
- the target workflow includes sensitive steps that should not be automated without explicit approval
- direct API integration would be cleaner and more reliable

## References

If you need the distilled source rationale, read `references/source-notes.md`.

## Output Expectations

Depending on the request, this skill should help produce one of:

- a repeatable CLI command sequence
- a site-specific automation skill
- a debugging checklist for a broken browser flow
- a saved-state based recurring automation routine

## Common Failure Modes

Avoid these:

- using stale refs after navigation
- storing hardcoded assumptions without verification steps
- skipping auth-state management for recurring tasks
- claiming zero-token while still relying on repeated AI interpretation each run

## Fast Heuristic

If the workflow can be discovered once, re-run many times, and verified through snapshots/state checks, it is a strong candidate for this skill.
