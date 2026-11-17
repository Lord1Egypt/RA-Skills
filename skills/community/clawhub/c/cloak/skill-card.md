## Description:

Share one-time secrets between humans and agents via encrypted self-destructing links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saba-ch](https://clawhub.ai/user/saba-ch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use Cloak to create, retrieve, and delete one-time secret links for API keys, passwords, tokens, and configuration values without displaying retrieved secret values in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets are sent to the third-party service at cloak.opsy.sh.

Mitigation: Use the skill only when that service is trusted for the secret being shared; prefer approved or self-hosted secret-sharing tools for production, administrative, cloud, or high-value credentials.

Risk: Reading or deleting a Cloak secret can permanently consume it.

Mitigation: Confirm create, retrieve, and delete actions explicitly before issuing the command, and write retrieved values directly to their destination instead of displaying them.

## Reference(s):

- [Cloak homepage](https://cloak.opsy.sh)
- [Cloak skill on ClawHub](https://clawhub.ai/saba-ch/skills/cloak)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; create, retrieve, and delete actions interact with https://cloak.opsy.sh.]

## Skill Version(s):

0.1.3 (source: server release evidence; artifact frontmatter says 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
