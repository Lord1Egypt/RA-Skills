## Description: <br>
Generates Ezviz camera live and playback streaming links for PC and mobile viewers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate live-view and playback URLs for Ezviz cameras when they need remote camera monitoring or quick preview links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Ezviz camera credentials and can generate camera stream access links. <br>
Mitigation: Use dedicated minimal-permission Ezviz credentials, avoid master account credentials, and rotate credentials if they are exposed. <br>
Risk: Secrets or access tokens may be exposed through command history, logs, copied terminal output, or generated preview URLs. <br>
Mitigation: Prefer environment variables over command-line arguments, avoid sharing run output, and treat generated URLs as sensitive. <br>
Risk: Token caching may persist access tokens in a shared temporary directory across skill runs. <br>
Mitigation: Disable caching with EZVIZ_TOKEN_CACHE=0 for sensitive cameras or run the skill in an isolated environment with controlled cache access. <br>
Risk: Fallback credential lookup may read OpenClaw configuration files that contain unrelated secrets. <br>
Mitigation: Set explicit Ezviz environment variables and keep Ezviz credentials in dedicated configuration files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ezviz-Open/ezviz-open-camera-video) <br>
- [Ezviz Agent API Reference](references/ezviz-agent-api.md) <br>
- [Ezviz Open Platform](https://open.ys7.com/) <br>
- [Ezviz API Documentation](https://openai.ys7.com/doc/) <br>
- [Token API Documentation](https://openai.ys7.com/help/81) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style terminal guidance with generated PC and mobile live/playback URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EZVIZ_APP_KEY and EZVIZ_APP_SECRET; EZVIZ_DEVICE_SERIAL and EZVIZ_CHANNEL_NO are optional inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
