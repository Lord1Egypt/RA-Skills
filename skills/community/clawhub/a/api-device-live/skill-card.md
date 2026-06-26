## Description: <br>
Closeli Open Device Live Query obtains a short-lived web live playback link for a specified Closeli device after verifying device ownership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[closeli-open](https://clawhub.ai/user/closeli-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve a browser-ready live player link for an owned Closeli device, such as when viewing a device feed remotely or integrating live viewing into another interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive API key stored in ~/.openclaw/.env. <br>
Mitigation: Use a least-privilege API key and restrict ~/.openclaw/.env to the OpenClaw service user. <br>
Risk: A misconfigured gateway host could send requests and device metadata to an unexpected endpoint. <br>
Mitigation: Verify AI_GATEWAY_HOST is the expected Closeli endpoint before use. <br>
Risk: Disabling TLS verification can expose credentials and device data to interception. <br>
Mitigation: Keep TLS verification enabled except in controlled development environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/closeli-open/api-device-live) <br>
- [Publisher profile](https://clawhub.ai/user/closeli-open) <br>
- [Closeli AI Gateway host](https://ai-open.icloseli.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown link to the live player, with error messages summarized from JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a device_id and a configured AI_GATEWAY_API_KEY; successful live player links are short-lived.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
