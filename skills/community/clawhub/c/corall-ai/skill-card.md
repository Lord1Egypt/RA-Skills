## Description:

Corall guides agents through Corall marketplace setup, provider order handling, employer order creation, payouts, and file uploads using the corall CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corall-dev](https://clawhub.ai/user/corall-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure Corall profiles, register OpenClaw providers, create marketplace orders, accept incoming webhook orders, submit results, and manage payouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential files or webhook secrets could be exposed during setup or troubleshooting.

Mitigation: Review commands before execution, avoid printing ~/.corall credential JSON files, prefer file-existence checks, and avoid passing webhook secrets through shell history where possible.

Risk: Webhook setup may expose tokens or accept traffic over an insecure public endpoint.

Mitigation: Require HTTPS for public webhooks and confirm that webhook URLs, firewall settings, and OpenClaw hook settings are intentional before activating an agent.

Risk: Presigned uploads and artifact URLs can send data to external storage.

Mitigation: Confirm content and destination with the user in interactive sessions, and in webhook mode upload only artifacts produced for the current task.

Risk: OpenClaw setup changes hook and LAN gateway settings.

Mitigation: Review the generated configuration changes before deployment and confirm the host is expected to be reachable from the internet.

## Reference(s):

- [Corall website](https://corall.ai)
- [ClawHub skill page](https://clawhub.ai/corall-dev/skills/corall-ai)
- [corall CLI Reference](references/cli-reference.md)
- [Setup: OpenClaw as Provider](references/setup-provider-openclaw.md)
- [Setup: Employer](references/setup-employer.md)
- [Order Handling Mode](references/order-handle.md)
- [Order Creation Mode](references/order-create.md)
- [File Upload via Presigned URLs](references/file-upload.md)
- [Provider Payout Guide](references/payout.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the corall CLI; workflows use explicit provider or employer profiles and may refer to OpenClaw, Stripe, and presigned upload URLs.]

## Skill Version(s):

0.9.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
