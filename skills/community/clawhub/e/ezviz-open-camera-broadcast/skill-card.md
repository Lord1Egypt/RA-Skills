## Description:

Broadcasts local audio files or generated text-to-speech audio to Ezviz devices through the Ezviz Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send voice announcements, alerts, reminders, and broadcast messages to Ezviz devices that support audio playback or talk functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls audio broadcast-capable Ezviz devices and uses device-control credentials.

Mitigation: Install only for expected Ezviz broadcast use cases and use dedicated least-privilege Ezviz app credentials.

Risk: Access tokens are cached by default in a system temporary directory.

Mitigation: Set EZVIZ_TOKEN_CACHE=0 on shared or high-security machines unless the cache location is hardened.

Risk: Credentials may be read from OpenClaw config files if environment variables are not set.

Mitigation: Prefer EZVIZ_APP_KEY, EZVIZ_APP_SECRET, and EZVIZ_DEVICE_SERIAL environment variables, which take priority over config-file fallback.

Risk: Passing secrets as command-line arguments can expose them through shell history or process listings.

Mitigation: Provide credentials through environment variables or a managed secret mechanism instead of command-line arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezviz-open/skills/ezviz-open-camera-broadcast)
- [Ezviz Open API token documentation](https://open.ys7.com/help/81)
- [Ezviz voice upload documentation](https://open.ys7.com/help/1241)
- [Ezviz voice send documentation](https://open.ys7.com/help/1253)
- [Ezviz Open Platform](https://open.ys7.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console status text with JSON API responses and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and can execute device-control API calls when configured with Ezviz credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
