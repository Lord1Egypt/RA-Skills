## Description:

Configures Ezviz devices through the Ezviz Open API, including arming, defense plans, privacy shutter, all-day recording, and motion-detection sensitivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Ezviz cameras and devices remotely from an agent workflow when they have dedicated Ezviz API credentials and a target device serial.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Ezviz access tokens may persist in a system temp cache, including in cases where users expect caching to be disabled.

Mitigation: Use dedicated least-privilege Ezviz credentials, avoid shared or high-security hosts, isolate or clear the temp token cache after use, and rotate credentials as needed.

Risk: The skill can change security and privacy affecting device settings such as arming, privacy shutter, recording, and motion detection.

Mitigation: Test on non-critical devices first, verify device support and API permissions, and review requested configuration actions before execution.

Risk: If environment variables are absent, the skill may read Ezviz credentials from OpenClaw config files.

Mitigation: Set explicit Ezviz environment variables for intended credentials or isolate OpenClaw config files in shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ezviz-open/skills/ezviz-open-camera-config)
- [Publisher Profile](https://clawhub.ai/user/ezviz-open)
- [API Mapping Reference](references/api-mapping.md)
- [Ezviz Open API Token Documentation](https://openai.ys7.com/help/81)
- [Ezviz Device Defense Documentation](https://openai.ys7.com/help/701)
- [Ezviz Defense Plan Documentation](https://openai.ys7.com/help/702)
- [Ezviz Privacy Shutter Documentation](https://openai.ys7.com/help/707)
- [Ezviz All-Day Recording Documentation](https://openai.ys7.com/help/713)
- [Ezviz Motion Detection Configuration Documentation](https://openai.ys7.com/help/715)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Ezviz Open API requests that modify device configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
