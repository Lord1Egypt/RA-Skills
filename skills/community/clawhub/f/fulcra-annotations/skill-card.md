## Description:

Create, list, record, and verify Fulcra annotation definitions and events through the Fulcra Life API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create Fulcra annotation definitions, record approved moment or metric annotations, and verify writes through readback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication depends on local Fulcra CLI execution and account credentials.

Mitigation: Install only with a trusted Fulcra account, API endpoint, and CLI supply chain; prefer a pinned reviewed CLI version or vetted local binary.

Risk: Broad FULCRA_CLI_COMMAND overrides could route authentication through an unintended executable.

Mitigation: Keep the default Fulcra CLI invocation when possible and avoid overrides unless the executable path has been reviewed.

Risk: Update, delete, bulk, or backfill workflows can change existing annotation state or create many records.

Mitigation: Require explicit user confirmation, use dry-run mode before writes, and use a reviewed admin or ledger-backed workflow for broad changes.

Risk: Fulcra records and tokens may contain private user data.

Mitigation: Do not print access tokens, credential files, capability URLs, or raw private records in chat or logs; share device authorization details only through the trusted user channel.

## Reference(s):

- [Fulcra Annotation API Notes](references/api-notes.md)
- [Fulcra API OpenAPI document](https://api.fulcradynamics.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/arc-claw-bot/skills/fulcra-annotations)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Fulcra authentication and readback verification for confirmed writes.]

## Skill Version(s):

1.0.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
