## Description:

Turn a written census schedule into one census notice voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External office staff use this skill to turn an already-written census schedule into 8 to 20 labeled notice voice clips. It plans clip slots, confirms any paid clone or speech step, and retrieves generated audio task results through Beatra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Beatra authorization scope is broader than census voice generation and includes other media-generation, task, artifact, and wallet-spend capabilities.

Mitigation: Install only with a Beatra account where that broad authority is acceptable, keep the device token private, and review the requested authorization before use.

Risk: The bundled client silently checks for and installs package updates by default.

Mitigation: Use the documented `python3 scripts/mcp_client.py update --auto off` command when silent package updates are not acceptable for the installation.

Risk: Clone and speech operations consume Beatra credits, and retries can duplicate paid work if request identity is not preserved.

Mitigation: Confirm paid clone and speech cards before submission, use one opaque `client_request_id` per paid request, and retry uncertain submissions only with byte-identical arguments.

Risk: Voice cloning can misuse a staff voice if authorization and likeness rights are not confirmed.

Mitigation: Use cloned voices only after inspecting an authorized sample and confirming likeness and voice rights; otherwise use a catalog voice.

Risk: Generated census audio could imply results, penalties, records, or eligibility findings that were not in the source schedule.

Mitigation: Read only the supplied schedule, keep one schedule item per clip, and review names and content against the pronunciation table and written source before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/census-notice-voice)
- [Beatra skill homepage](https://beatra.ai/skills/census-notice-voice)
- [Census notice voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Beatra speech and optional voice-clone tasks that return MP3 audio artifacts through asynchronous task results.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
