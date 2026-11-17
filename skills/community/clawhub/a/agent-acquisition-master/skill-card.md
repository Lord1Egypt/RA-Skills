## Description:

Agent Acquisition Master helps an agent run client acquisition across cold email, LinkedIn outreach, organic content funnels, lead qualification, follow-up sequences, and closing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

External users and growth operators use this skill to plan and run client-acquisition workflows for B2B and B2C offerings. It supports prospecting, outreach copy, social content planning, qualification, follow-up, reporting, and closing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous outreach, posting, inbox reading, scraping, Telegram forwarding, and broad state writes can operate without enough user control.

Mitigation: Review and disable default crons before installation, scope account and file access, and require human approval before any email, social post, LinkedIn action, purchase, DNS change, or Telegram forwarding.

Risk: Secrets, lead data, inbox content, and outreach logs may contain sensitive personal or commercial data.

Mitigation: Store secrets and lead or inbox data in scoped, redacted storage with clear retention, unsubscribe, and access controls.

Risk: Automated acquisition messages can create compliance, reputation, or platform-policy risk if sent without review.

Mitigation: Review recipient targeting and message copy before sending, honor unsubscribe requests immediately, and keep volume limits conservative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/agent-acquisition-master)
- [Project homepage](https://github.com/wesley-agent/wesley-acquisition-master)
- [Gmail](https://gmail.com)
- [LinkedIn](https://linkedin.com)
- [X / Twitter](https://twitter.com)
- [Reddit](https://reddit.com)
- [Hunter.io](https://hunter.io)
- [Apollo.io](https://apollo.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce acquisition plans, outreach copy, schedules, lead data, logs, reports, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
