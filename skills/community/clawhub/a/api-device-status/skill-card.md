## Description: <br>
Queries Closeli device status through the Closeli Open gateway to determine whether specified devices are online, offline, or sleeping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[closeli-open](https://clawhub.ai/user/closeli-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check whether Closeli devices are available before live streaming or event queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an API key and device metadata. <br>
Mitigation: Keep ~/.openclaw/.env permission-restricted, use a least-privilege API key, and avoid passing keys on the command line. <br>
Risk: A misconfigured gateway host or disabled TLS verification could expose credentials or device data. <br>
Mitigation: Verify AI_GATEWAY_HOST before running the skill and leave TLS verification enabled outside development environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/closeli-open/api-device-status) <br>
- [Closeli Open gateway host](https://ai-open.icloseli.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON status data from the script, typically rendered by the agent as a Markdown table or concise text message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires device IDs and an AI_GATEWAY_API_KEY configured in ~/.openclaw/.env or supplied with --api-key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
