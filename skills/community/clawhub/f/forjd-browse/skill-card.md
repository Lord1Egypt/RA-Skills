## Description:

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danjdewhurst](https://clawhub.ai/user/danjdewhurst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Browse to drive a real browser for navigation, form entry, clicks, screenshots, data extraction, web application testing, accessibility checks, performance checks, and other browser-based automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority to navigate, click, fill forms, execute browser automation, and interact with live websites.

Mitigation: Install only for agents that need browser automation, review proposed browser actions for sensitive workflows, and prefer trusted or test environments for high-impact tasks.

Risk: Browser sessions can persist cookies, localStorage, authentication tokens, and reusable auth-state files.

Mitigation: Use isolated sessions for separate accounts, run browse wipe after sensitive work, avoid shared or sensitive accounts unless necessary, and protect exported auth-state files like passwords.

Risk: The artifact documents saving authentication state to /tmp, which can be unsafe on shared systems.

Mitigation: Save authentication state only to access-controlled paths and remove saved state after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danjdewhurst/skills/forjd-browse)
- [Publisher profile](https://clawhub.ai/user/danjdewhurst)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown or plain text with inline shell commands and command-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, traces, videos, reports, JSON, CSV, and saved authentication state when the underlying browse command is used for those tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
