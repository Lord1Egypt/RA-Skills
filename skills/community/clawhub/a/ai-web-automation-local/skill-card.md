## Description:

Automates web tasks such as form filling, data scraping, testing, scheduling, and monitoring with Selenium or Puppeteer-style browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-at](https://clawhub.ai/user/larry-at)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate authorized web workflows, including scraping public pages, filling forms, running tests, scheduling checks, and monitoring websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-supplied URLs from the agent environment without network safety boundaries.

Mitigation: Use it only on authorized public targets, and constrain runtime access with URL allowlists and network egress controls before allowing access to private networks or sensitive endpoints.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/larry-at/skills/ai-web-automation-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown reports and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated web scraping reports to an output directory during local execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
