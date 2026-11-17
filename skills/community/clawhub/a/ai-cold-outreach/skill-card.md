## Description:

Complete cold email outreach system for AI agents that supports Apollo lead generation, email enrichment, Saleshandy prospect import, warmup monitoring, campaign management, email templates, and deliverability guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and growth operators, founders, and developers use this skill to build and run cold email workflows that search for prospects, enrich contact data, import leads into Saleshandy sequences, monitor sender readiness, and draft campaign copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles prospect personal data and can prepare generated CSV files for outreach workflows.

Mitigation: Keep generated prospect files out of version control, limit retained data to the campaign need, and verify lead sourcing and enrichment practices against applicable privacy rules.

Risk: The skill uses Apollo and Saleshandy API credentials for live third-party services.

Mitigation: Use least-privileged API keys, avoid storing real keys in workspace config files or shell history, and rotate credentials if exposed.

Risk: The skill can import prospects into outreach systems and support campaign activation.

Mitigation: Require manual approval before importing prospects, activating sequences, or sending campaigns, and verify unsubscribe, personalization, and cold-email compliance requirements first.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Configuration Template](references/config-template.json)
- [Cold Email Templates](references/email-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/joeytbuilds/skills/ai-cold-outreach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, Python script usage, and CSV workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Apollo and Saleshandy API credentials and may produce prospect CSV files for import into outreach systems.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
