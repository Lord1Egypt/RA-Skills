# Source Notes

This skill was derived from a WeChat article about using `agent-browser` CLI plus OpenClaw skills to build low-code / zero-token browser automation.

## Key extracted ideas

- Traditional browser automation hurts because of code complexity, selector fragility, and maintenance cost.
- OpenClaw skill + `agent-browser` CLI changes the unit of automation from code-heavy scripts to reusable markdown-guided workflows.
- The core interaction model is semantic page refs (`@e1`, `@e2`, etc.) obtained from snapshots.
- The main loop is:
  - OPEN
  - SNAPSHOT
  - INTERACT
  - VERIFY
  - REPEAT
  - CLOSE
- Once a flow is stabilized, execution can be near-zero-token because the CLI can run deterministically without repeated model reasoning.
- Session/auth state save-load is critical for repeated sign-in style workflows.

## Commands highlighted by the source article

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e<n>
agent-browser fill @e<n> "text"
agent-browser type @e<n> "text"
agent-browser screenshot debug.png
agent-browser get url
agent-browser get title
agent-browser wait --load networkidle
agent-browser state save auth.json
agent-browser state load auth.json
agent-browser close
```

## Reusable task archetypes

- auto sign-in
- repeated form submission
- repeated dashboard opening/checking
- click-through admin workflows
- stable browser routines that do not require reasoning every run

## Failure patterns worth remembering

- stale refs after navigation
- page re-render without re-snapshot
- expired auth state
- silent login failure
- no explicit wait before next step

## Implementation note

The article emphasized “0 Token” as a strategic positioning idea. In practice, this means minimizing model involvement during execution after the workflow has already been discovered and encoded.
