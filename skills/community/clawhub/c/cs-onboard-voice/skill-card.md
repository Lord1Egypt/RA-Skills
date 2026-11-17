## Description:

Turn a written customer-onboarding step list into one customer onboard voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Enablement and customer success teams use this skill to turn existing customer onboarding step lists into labeled voice clip packs. It plans 8 to 20 clips, optionally coordinates authorized voice cloning, submits text-to-speech work, and reports task, billing, and audio artifact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared Beatra device token with paid account capabilities beyond voice generation.

Mitigation: Review the requested account authority before installation and use Beatra account or device revocation controls when access should be removed.

Risk: The bundled client silently checks for and installs package updates by default.

Mitigation: Review the automatic update behavior and disable silent checks with the documented update --auto off command when manual update control is required.

Risk: Voice cloning and speech synthesis can consume Beatra credits.

Mitigation: Use the skill's separate confirmation cards, opaque request IDs, and task recovery guidance before submitting paid clone or speech work.

## Reference(s):

- [Customer onboard voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command snippets, JSON payload examples, and audio task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans a free labeled slot list first; paid clone and speech tasks require separate confirmation and return MP3 audio artifacts by default.]

## Skill Version(s):

0.1.2 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
