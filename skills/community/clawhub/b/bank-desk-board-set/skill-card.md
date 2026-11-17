## Description:

Turn user-supplied branch window names and board lines into a four-to-eight still bank desk board set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan, approve, generate, review, and recover branch desk board image packs from user-confirmed window names and board lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a persistent shared Beatra Device Token with broad media, wallet, artifact, and task permissions.

Mitigation: Review the skill before installation, keep the credential file private, and revoke or uninstall the Beatra connection when it is no longer needed.

Risk: The bundled client can silently install newer executable package files through automatic updates.

Mitigation: Disable automatic updates with the documented update command when reviewed code must remain unchanged, and review updated packages before use.

Risk: Image generation is paid work and can consume Beatra credits.

Mitigation: Check the live model card and approval prompt before paid generation, use one client request identity per still, and report returned net charged credits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/bank-desk-board-set)
- [Beatra skill homepage](https://beatra.ai/skills/bank-desk-board-set)
- [Bank desk board pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a labeled pack list, approval card, Beatra generation calls, task recovery guidance, and delivery notes for returned image artifacts.]

## Skill Version(s):

0.1.2 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
