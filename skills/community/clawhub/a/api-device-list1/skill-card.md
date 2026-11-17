## Description:

Closeli Device List Query API retrieves the device list under the current account and returns basic information such as device name, MAC address, and IMEI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[closeli-open](https://clawhub.ai/user/closeli-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list devices bound to a Closeli account and obtain device identifiers before calling other device APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the account API key and device data to a configurable gateway host.

Mitigation: Use a least-privilege API key and confirm AI_GATEWAY_HOST is the expected trusted Closeli gateway before running the skill.

Risk: TLS certificate verification can be disabled with AI_GATEWAY_VERIFY_SSL=false.

Mitigation: Keep TLS verification enabled when using real credentials; reserve disabled verification for isolated development environments only.

Risk: The shared ~/.openclaw/.env credential file may be readable by other skills running as the same user.

Mitigation: Restrict file permissions, for example with chmod 600, and limit access to the OpenClaw service user.

Risk: Passing the API key through --api-key may expose it through local command-line logging or process inspection.

Mitigation: Prefer the persistent OpenClaw configuration file for credentials and avoid command-line API key overrides with real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/closeli-open/skills/api-device-list1)
- [Closeli default gateway](https://ai-open.icloseli.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Text]

**Output Format:** [JSON from the script, then a Markdown table or concise status message for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For successful non-empty responses, the agent displays MAC Address and Device Name and removes the xxxxS_ prefix from device_id.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
