## Description:

Controls Ezviz Open Platform PTZ cameras by listing devices, checking status and capabilities, and issuing PTZ, preset, and mirror commands through the Ezviz API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to query Ezviz devices and control PTZ-capable cameras, including movement, stopping movement, mirror flips, and preset management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has Ezviz device-control authority and can move or reconfigure PTZ-capable cameras.

Mitigation: Use a dedicated low-permission Ezviz application and test against intended devices before operational use.

Risk: Ezviz credentials and access tokens are sensitive, and the release security guidance warns against passing AppSecret on the command line.

Mitigation: Prefer environment-based secret handling where supported, avoid shell history exposure, and rotate credentials regularly.

Risk: The security evidence says tokens may be written to a shared temp cache even when caching is documented as disabled.

Mitigation: Avoid shared machines unless the cache behavior is fixed, or securely clean the token cache after use.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/ezviz-open/skills/ezviz-open-ptz-control)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ezviz-open)
- [Ezviz Open Platform](https://open.ys7.com/)
- [Ezviz Token API](https://openai.ys7.com/help/81)
- [Ezviz Device List API](https://openai.ys7.com/help/680)
- [Ezviz Device Status API](https://openai.ys7.com/help/681)
- [Ezviz Device Capacity API](https://openai.ys7.com/help/683)
- [Ezviz PTZ Start API](https://openai.ys7.com/help/690)
- [Ezviz PTZ Stop API](https://openai.ys7.com/help/691)
- [Ezviz Preset Add API](https://openai.ys7.com/help/692)
- [Ezviz Preset Clear API](https://openai.ys7.com/help/693)
- [Ezviz Preset Move API](https://openai.ys7.com/help/694)
- [Ezviz Mirror API](https://openai.ys7.com/help/695)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Console text with JSON API result details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EZVIZ_APP_KEY and EZVIZ_APP_SECRET credentials; may use a 0600 token cache in the system temp directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
