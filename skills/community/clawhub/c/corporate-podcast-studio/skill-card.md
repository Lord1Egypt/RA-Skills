## Description:

Turn executive talking points or company column copy into a serialized corporate podcast with one consistent host voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Communications and executive content teams use this skill to turn approved talking points or column copy into serialized corporate podcast episodes with a consistent host voice. Agents use it to plan episode ledgers, manage voice selection or consented cloning, synthesize episode audio through Beatra, and report task status, usage, and billing facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a broad shared Beatra account-level device token that can access more than podcast-specific tools and spend credits.

Mitigation: Install only when that shared authorization is acceptable, keep the token out of chat, logs, command arguments, and environment variables, and reconnect only when the user explicitly chooses to restore full Beatra authorization.

Risk: Remote Beatra tool calls can create billable clone or speech tasks.

Mitigation: Confirm voice choice, pronunciation table, and live estimates before paid submits; use one client_request_id per frozen payload and poll existing tasks instead of resubmitting uncertain work.

Risk: Silent self-updates are enabled by default and may change local package files.

Mitigation: Review update behavior before installation and disable silent checks with `python3 scripts/mcp_client.py update --auto off` when confirmation is required before package changes.

Risk: Voice cloning can misuse a speaker sample if consent is assumed from file access alone.

Mitigation: Require an explicit statement that the voice belongs to the user or that the speaker authorized this cloning use before uploading a sample or submitting a clone request.

Risk: Uninstall or disconnect can affect the shared Beatra device connection for other installed Beatra skills.

Mitigation: Use the bundled uninstall workflow and follow its decision output so the shared connection is removed only when this is the last Beatra skill on the device.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/corporate-podcast-studio)
- [Beatra skill homepage](https://beatra.ai/skills/corporate-podcast-studio)
- [Corporate podcast workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce and retrieve audio artifacts through Beatra text-to-speech tasks; reports actual duration, usage, and billing.net_charged_credits when returned.]

## Skill Version(s):

0.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
