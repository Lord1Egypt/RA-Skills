## Description: <br>
Queries the Closeli Open device list API for the current account and returns device names and identifiers such as MAC address and IMEI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[closeli-open](https://clawhub.ai/user/closeli-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to list devices bound to a Closeli account and obtain device identifiers before calling other device APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shared ~/.openclaw/.env credential file may be readable by other skills running as the same user. <br>
Mitigation: Restrict file permissions, run under the intended OpenClaw service user, and use a least-privilege API key limited to device-list access. <br>
Risk: A misconfigured gateway host or disabled TLS verification could expose the API key and device data. <br>
Mitigation: Verify AI_GATEWAY_HOST before running and keep AI_GATEWAY_VERIFY_SSL enabled outside development environments. <br>
Risk: Device names and identifiers may reveal account inventory information. <br>
Mitigation: Share output only with authorized users and avoid reusing high-privilege credentials for this query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/closeli-open/api-device-list1) <br>
- [Closeli Open publisher profile](https://clawhub.ai/user/closeli-open) <br>
- [Default Closeli gateway host](https://ai-open.icloseli.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown summary of JSON device-list results, with tabular output for successful non-empty responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, httpx, a Closeli gateway API key, and ~/.openclaw/.env configuration; the script prints JSON for the agent to transform into user-facing text.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
