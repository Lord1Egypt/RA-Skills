# AgentBrowse Boundaries

## What This Skill Owns

- Browser launch and browser attach.
- Visible-state navigation and interaction.
- Structured extraction from the current page.
- Screenshots, status checks, and browser recovery.

## What Changes The Flow

- If the next step needs approved protected values, protected personal data,
  or payment-card entry, switch to the protected-flow tool that owns that
  step.
- Keep AgentBrowse focused on page control and observation around that
  boundary.

## Reliable Operation

- Base decisions on the current page, not on cached assumptions.
- Re-run `observe` after redirects, reloads, or major DOM changes.
- Use `extract` when you need structured output, not as a substitute for
  understanding whether the page changed.

## Diagnostics

- Use `browser-status` and `screenshot` to inspect the current state.
- Use `doctor` after `init` when AI-assisted `observe` or `extract` still
  fails.
- Use `close` for teardown or recovery, not as a success signal.

## Ask The User When

- the next step is still ambiguous after a fresh observe pass;
- browser startup or attach is blocked by the environment;
- the task reaches a protected boundary that needs explicit approval or a
  different tool.
