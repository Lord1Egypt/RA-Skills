## Description:

Memory-oriented browser automation skill for repeatable web workflows including login, extraction, bulk actions, form filling, screenshots, and checks across RoxyBrowser, Camoufox, and Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whjstc](https://clawhub.ai/user/whjstc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to drive repeatable browser workflows with BrowseCraft, including opening pages, taking snapshots, interacting with stable element references, filling forms, capturing screenshots, and reporting structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned globally installed npm CLI.

Mitigation: Install browsecraft-cli only from a trusted source, prefer a pinned version or isolated environment, and avoid elevated global installs where possible.

Risk: Browser automation can expose credentials or sensitive page data during web workflows.

Mitigation: Keep credentials in environment or config rather than command lines, avoid printing secrets, and use a dedicated browser profile for sensitive sites or bulk actions.

Risk: Automation may access network destinations outside the intended target workflow.

Mitigation: Ask for confirmation before using network access outside the target website, matching the skill's scope policy.

## Reference(s):

- [Browsecraft on ClawHub](https://clawhub.ai/whjstc/skills/browsecraft)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to return objective, steps, result, failure reason, and next action.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
