## Description:

Turn a coworking or daytime office brief into one office background music playlist of 8 to 15 low-stimulation instrumentals. This coworking playlist studio writes a workday music and office BGM set for arrival, focus, light talk, and close. Use it for daytime instrumental beds and a low-stimulation playlist the floor can play through the day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace operators use this skill to turn a daytime coworking, office, or cafe brief into a reusable pack of quiet original instrumental beds. The agent plans the track list first, then uses Beatra music generation only after approval of the live cost and per-track request plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared broad Beatra device token with access beyond music generation, including upload, task, and wallet-spend capabilities.

Mitigation: Install only if that account authority is acceptable; keep the credential private, do not pass it through chat or command arguments, and revoke the device from Beatra when access is no longer needed.

Risk: Automatic updates are enabled by default and can replace package-owned code without a separate approval prompt.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` when reviewed code must remain fixed, and review new releases before re-enabling updates.

Risk: Generating each playlist slot is billable and retry mistakes could create duplicate paid work.

Mitigation: Require the live price and slot-count approval before generation, use one opaque `client_request_id` per slot, and retry uncertain submissions only with byte-identical arguments.

Risk: Uninstall and disconnect operations affect shared Beatra device state used by other Beatra skills.

Mitigation: Run the bundled uninstall script and follow its JSON decision; do not manually delete `~/.beatra` unless the documented flow says the shared connection has been retired.

## Reference(s):

- [Beatra package homepage](https://beatra.ai/skills/coworking-day-pack)
- [Daytime playlist workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and Beatra task or artifact results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an 8 to 15 track instrumental playlist plan and, after user approval, reports actual duration and billing fields returned by Beatra.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
