## Description:

Selects a cost-effective capable model for agent tasks, handles provider and rate-limit failures, and supports health, cost, configuration, and provider-sync checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adroidian](https://clawhub.ai/user/adroidian)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to route delegated tasks to configured model providers by task complexity, cost, and provider availability. They can also inspect health and cost output, record failed models for cooldown, and review provider sync results before promoting newly discovered models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider sync script includes a hardcoded Telegram bot credential and fixed chat destination.

Mitigation: Remove or rotate the bundled token before installing, and require notification credentials and destinations to be supplied by the user.

Risk: Live provider sync can query external model-provider APIs and update local router configuration.

Mitigation: Run provider sync with --dry-run first, provide only intended provider API keys, and review sync-report.json and discovered models before promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adroidian/skills/chitin-core)
- [Publisher profile](https://clawhub.ai/user/adroidian)
- [Chitin agentic OS](https://chitin.xyz)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON command output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routing output includes tier, model, confidence, estimated cost, and signals; provider sync can update local configuration after a dry run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
