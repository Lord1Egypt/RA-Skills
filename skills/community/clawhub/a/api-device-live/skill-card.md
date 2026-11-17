## Description:

Closeli Device Live Query API obtains a web live playback link for a specified device so a user can view the device feed or integrate live streaming into a web or third-party system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[closeli-open](https://clawhub.ai/user/closeli-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request an H5 live player link for a Closeli device they are authorized to access. It is intended for remote live viewing and web or third-party live streaming integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a sensitive API key from a shared persistent configuration file.

Mitigation: Use a least-privilege API key and restrict ~/.openclaw/.env so it is readable only by the intended OpenClaw service user.

Risk: A configurable gateway or disabled TLS verification could expose the API key and device data.

Mitigation: Keep AI_GATEWAY_VERIFY_SSL enabled and confirm AI_GATEWAY_HOST points to the intended trusted Closeli gateway before use.

Risk: Unrelated skills running as the same user may be able to modify the shared configuration file.

Mitigation: Avoid deployment environments where unrelated skills can write to ~/.openclaw/.env or otherwise change the gateway configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/closeli-open/skills/api-device-live)
- [ClawHub publisher profile](https://clawhub.ai/user/closeli-open)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance]

**Output Format:** [JSON from the helper script, normally transformed by the agent into a concise Markdown link or error message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The live URL contains a short-lived token and should be shown as a Markdown link with the resolved device name when available.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
