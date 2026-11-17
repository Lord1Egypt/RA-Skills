# Coding Agent Handoffs

Reference for Gate 5 in `SKILL.md`: when the orchestrator stops and hands work to a
coding agent, and exactly what that handoff should contain. The orchestrator does not
modify files in a git repository under any circumstance — this file exists so that
boundary has a concrete procedure behind it instead of just a rule.

## When to hand off

Any fix that requires changing a file that lives in version control. In practice, for
this skill, that means:

- Ghost theme `.hbs` file modifications
- An edge function serving `/llms.txt` (or another agent-facing file) from a domain
  that isn't Ghost Pro itself
- `robots.txt` changes, since Ghost Pro doesn't expose this for editing
- Redirect logic implemented in application code in a deployed repository, as distinct
  from Ghost's own redirects UI (which is a browser-session task the orchestrator
  handles directly — see `ghost-deployment.md`)
- Anything else that ultimately requires a git commit and a pull request

If a fix can be done through the Ghost Admin API or a browser session against Ghost
itself, it is not a handoff — the orchestrator does it directly. Handoffs are
specifically for work outside what Ghost's own interfaces expose.

## Handoff template: Ghost theme modification

```
[AGENT_HANDOFF]
type: spec
target: <coding agent>

task: <one-line description of the theme change>
repo: <repo containing the Ghost theme>
branch: feature/<short-slug>
pr_title: "<title>"

---

CONTEXT
- Site: yourdomain.com (Ghost Pro)
- Theme file(s) affected: <e.g., partials/head.hbs>
- Why this can't be done via code injection or the Admin API: <reason>

CHANGE REQUIRED
<precise description of the template change — what to add/modify, and where>

CONSTRAINTS
- Must not break existing theme functionality on other pages/templates
- No proper names or credentials in committed code
- Follow existing theme code style

VERIFICATION
- <how the coding agent should confirm the change works before opening the PR>

Reply with a single [AGENT_HANDOFF] block. No prose outside the block.
[/AGENT_HANDOFF]
```

## Handoff template: edge function (e.g., serving llms.txt off-platform)

```
[AGENT_HANDOFF]
type: spec
target: <coding agent>

task: Serve /llms.txt from an edge function
repo: <deployment repo>
branch: feature/<short-slug>
pr_title: "<title>"

---

CONTEXT
- Domain: yourdomain.com, deployed via <platform, e.g., Vercel>
- Why this is needed instead of the Ghost page option: <reason>

CHANGE REQUIRED
- Add an edge function/route handler that returns the llms.txt content at /llms.txt
- Content-Type: text/plain
- Source content: <inline or pointer to approved copy>

CONSTRAINTS
- No proper names or credentials in committed code
- Must not affect routing for any other existing path

VERIFICATION
- curl -s https://yourdomain.com/llms.txt returns the expected content with a 200

Reply with a single [AGENT_HANDOFF] block. No prose outside the block.
[/AGENT_HANDOFF]
```

## Handoff template: robots.txt

```
[AGENT_HANDOFF]
type: spec
target: <coding agent>

task: Add/modify robots.txt
repo: <deployment repo>
branch: feature/<short-slug>
pr_title: "<title>"

---

CONTEXT
- Domain: yourdomain.com
- Why this must be handled here: robots.txt is not exposed for editing on Ghost Pro

CHANGE REQUIRED
- Serve the following content at /robots.txt:
  <exact robots.txt content>

CONSTRAINTS
- Must not conflict with Ghost Pro's own default crawler handling
- No proper names or credentials in committed code

VERIFICATION
- curl -s https://yourdomain.com/robots.txt returns the expected content with a 200

Reply with a single [AGENT_HANDOFF] block. No prose outside the block.
[/AGENT_HANDOFF]
```

## Review checklist for a returned PR

When the coding agent returns a PR, the orchestrator reviews before merge:

- Does the change match the handoff's stated scope exactly — no unrelated changes bundled in?
- No proper names, credentials, or secrets committed anywhere in the diff.
- No hardcoded site-specific values that should have come from config or environment instead.
- Does the PR include or describe how the change was verified?
- For theme changes: confirm the change doesn't affect templates outside the stated scope.
- For edge function / robots.txt changes: confirm the new route doesn't shadow an existing route.
- Does the PR description give enough context for a future reader without re-reading the original handoff?

Only after this checklist passes does the orchestrator move to Gate 4 (live verification).
