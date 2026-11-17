## Description:

Ezviz Open Picture helps agents capture current images from one or more Ezviz devices, manage access tokens, and optionally download captured images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect live camera snapshots for monitoring archives, inspection reports, incident records, smart-home checks, or scheduled capture workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Ezviz camera credentials, access tokens, and signed camera-image URLs.

Mitigation: Use a dedicated least-privilege Ezviz app, rotate any exposed credentials, and avoid sending output that contains full pic_url values to shared logs.

Risk: Token caching can persist access tokens in a system temporary directory.

Mitigation: Disable token caching with EZVIZ_TOKEN_CACHE=0 in shared or high-security environments and clear the cache after use.

Risk: The skill may read Ezviz credentials from OpenClaw config files when environment variables are not set.

Mitigation: Set EZVIZ_APP_KEY and EZVIZ_APP_SECRET through environment variables and keep OpenClaw config files limited to dedicated Ezviz credentials.

Risk: Camera capture can involve privacy-sensitive images and local legal obligations.

Mitigation: Run the skill only for authorized devices and workflows that comply with applicable privacy and monitoring requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezviz-open/skills/ezviz-open-picture)
- [Ezviz Open Platform](https://open.ys7.com/)
- [Ezviz access token API](https://openai.ys7.com/help/81)
- [Ezviz device capture API](https://openai.ys7.com/help/687)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Console text with a JSON result object and optional local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Capture results include device, channel, pic_url or error details, and expire_hours when successful.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
