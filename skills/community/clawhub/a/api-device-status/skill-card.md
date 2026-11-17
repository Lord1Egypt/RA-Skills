## Description:

Queries Closeli device status so agents can determine whether specified devices are online, offline, or sleeping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[closeli-open](https://clawhub.ai/user/closeli-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether specified Closeli devices are available before live streaming or event queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bearer API key is read from a shared configuration file.

Mitigation: Use a least-privilege, revocable API key and keep ~/.openclaw/.env owner-readable only.

Risk: The gateway host can be configured, and TLS verification can be disabled.

Mitigation: Confirm AI_GATEWAY_HOST is the intended Closeli gateway and do not set AI_GATEWAY_VERIFY_SSL=false outside isolated development.

Risk: The script fetches device-list metadata to map device IDs to display names.

Mitigation: Review whether exposing device names is appropriate before running the skill in shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/closeli-open/skills/api-device-status)
- [Closeli AI gateway](https://ai-open.icloseli.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [JSON from the script, normally summarized by the agent as Markdown or a table for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, httpx, device IDs, and an AI_GATEWAY_API_KEY configured in ~/.openclaw/.env or supplied with --api-key.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
