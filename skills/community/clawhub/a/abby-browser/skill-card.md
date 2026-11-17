## Description:

Abby Browser helps agents control an OpenClaw browser session to open pages, capture screenshots, click elements, type into fields, fill forms, extract page text, wait, and scroll.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earnabitmore365](https://clawhub.ai/user/earnabitmore365)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to ask an agent to perform routine browser actions in an OpenClaw-controlled Chrome or Chromium session without manually composing each browser CLI command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can act inside an active session, including authenticated pages.

Mitigation: Use only in browser sessions where the agent is permitted to open pages, click elements, type text, fill forms, and capture screenshots.

Risk: The security evidence flags under-scoped automation that can run injected page JavaScript through extraction behavior.

Mitigation: Avoid sensitive authenticated pages until selector handling in scripts/extract.py is fixed and raw evaluate use is clearly restricted or confirmed by the user.

## Reference(s):

- [OpenClaw Browser Docs](https://docs.openclaw.ai/cli/browser)
- [Abby Browser on ClawHub](https://clawhub.ai/earnabitmore365/skills/abby-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw browser tooling and a Chrome or Chromium browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
