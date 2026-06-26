## Description: <br>
Captures snapshots from one or more Ezviz camera devices, manages access tokens, and can optionally download captured images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to capture current images from authorized Ezviz cameras for monitoring archives, incident records, periodic inspections, and remote status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation includes realistic-looking EZVIZ credentials and unsafe secret examples. <br>
Mitigation: Review or replace those examples before use and rotate any values that were ever real. <br>
Risk: Camera capture can expose private images or unauthorized devices. <br>
Mitigation: Run the skill only for cameras the operator is authorized to access, using dedicated minimal-permission EZVIZ credentials. <br>
Risk: Access tokens are cached in a system temp directory by default. <br>
Mitigation: Disable caching on shared machines with EZVIZ_TOKEN_CACHE=0 and clear the cache after sensitive use. <br>
Risk: Credentials may be read from OpenClaw config files when environment variables are absent. <br>
Mitigation: Prefer environment variables and review ~/.openclaw config files for dedicated Ezviz-only credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ezviz-Open/ezviz-open-picture) <br>
- [Ezviz Open Platform](https://open.ys7.com/) <br>
- [Ezviz access token API](https://openai.ys7.com/help/81) <br>
- [Ezviz device capture API](https://openai.ys7.com/help/687) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Console text with a JSON capture summary; optional downloaded JPEG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Capture entries include device, channel, pic_url or local_path, and error details when a request fails; returned image URLs are documented as expiring after 2 hours.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
