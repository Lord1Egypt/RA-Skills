## Description:

Turn a written class duty roster into one class duty voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and school staff use this skill to convert an existing class duty roster into a labeled set of spoken reminder clips. It helps plan, approve, generate, review, and recover roster-based voice-pack work without inventing missing roster details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad Beatra account permissions, including billable generation permissions, task access, artifacts access, and voice permissions.

Mitigation: Install only when the user trusts Beatra with those permissions, keep the device token private, and use the bundled disconnect or uninstall flow when access should be removed.

Risk: Clone and speech operations can spend account credits.

Mitigation: Show the live cost card before each paid stage, use one opaque request identity per paid request, and do not retry billable work unless the recovery rules allow the same unchanged request.

Risk: Voice cloning can misuse a staff likeness or voice sample if the sample is not authorized.

Mitigation: Proceed with cloning only after the user provides rights or consent for the sample, and treat file access as insufficient proof of consent.

Risk: The bundled client can silently replace package-owned executable files through automatic updates.

Mitigation: Review the package before installing, rely on the documented checksum and fixed-source update controls, and disable automatic updates when explicit control is required.

## Reference(s):

- [Class Duty Voice Pack on ClawHub](https://clawhub.ai/beatra-ai/skills/class-duty-voice)
- [Class Duty Voice Pack homepage](https://beatra.ai/skills/class-duty-voice)
- [Class duty voice workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [MCP connection](artifact/references/mcp-connection.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; Beatra task outputs can include MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans 8 to 20 labeled roster voice clips and may submit billable speech or clone tasks after explicit user approval.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
