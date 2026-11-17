## Description:

Guides agents in using AgentPMT's authenticated browser to complete tasks in user-authorized web accounts and websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents use this skill to automate authorized work in logged-in websites, such as posting content, updating CRM records, retrieving reports, and submitting forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation can post, submit forms, or change records in real logged-in accounts.

Mitigation: Limit connected accounts and permitted sites, and review requested actions before consequential submissions or changes.

Risk: Screenshots and recordings can persist sensitive account information.

Mitigation: Avoid capturing sensitive pages unless needed, and review stored artifacts before sharing them.

## Reference(s):

- [AstroBrowse setup and configuration](https://www.agentpmt.com/docs/tool-specific/astrobrowse)
- [AstroBrowse marketplace page](https://www.agentpmt.com/marketplace/astrobrowse-authenticated-agentic-browser)
- [AstroBrowse ClawHub release](https://clawhub.ai/agentpmt/skills/astrobrowse-authenticated-agentic-browser)
- [AstroBrowse action schema](schema.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Markdown instructions and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser actions can return extracted page content and references to downloaded files, screenshots, or recordings.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
