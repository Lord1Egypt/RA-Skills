## Description:

daily.dev Agentic Learning - continuous self-improvement through daily.dev feeds. Use when setting up agent learning, running learning loops, sharing insights with owner, or managing the agent's knowledge base. Triggers on requests about agent learning, knowledge building, staying current, or "what have you learned".

This skill is ready for commercial/non-commercial use.

## Publisher:

[idoshamun](https://clawhub.ai/user/idoshamun)

### License/Terms of Use:


## Use Case:

Developers and agent owners use this skill to configure an autonomous daily.dev learning loop, maintain a personalized feed, write learning notes, and share relevant findings from new technical content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous recurring operation can create cron jobs, change daily.dev feeds, send alerts, write persistent memory, or change learning goals without meaningful approval.

Mitigation: Require explicit approval before enabling recurring jobs, feed changes, alerts, persistent memory writes, or learning-goal changes; provide clear disable and uninstall controls.

Risk: External article fetching and search can introduce untrusted content and may expose sensitive owner or project context.

Mitigation: Validate URLs and domains, treat fetched content as untrusted, limit sensitive context shared with the skill, and review memory writes before preserving sensitive information.

Risk: The daily.dev API token is required for operation and could be misused if sent to unintended services.

Mitigation: Keep the token in the DAILY_DEV_TOKEN environment variable and send it only to api.daily.dev.

## Reference(s):

- [Learning Loop](references/learning-loop.md)
- [Memory Format for Agentic Learning](references/memory-format.md)
- [daily.dev API](https://api.daily.dev/public/v1)
- [Daily Dev Agentic on ClawHub](https://clawhub.ai/idoshamun/skills/daily-dev-agentic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning notes, feed configuration, owner-facing updates, and weekly digests.]

## Skill Version(s):

0.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
