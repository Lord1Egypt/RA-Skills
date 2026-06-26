## Description: <br>
EMP routes OpenClaw prompts to role-specific assistant personas and wraps responses in a Nonviolent Communication structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzj0402](https://clawhub.ai/user/zzj0402) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use EMP to route prompts to specialized work roles, including development, security, legal, HR, operations, customer success, data science, and communication coaching. The skill returns role-labeled guidance organized as observation, feeling, need, and request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts and caller-supplied headers may be sent to OpenRouter and downstream model providers. <br>
Mitigation: Avoid using the skill with secrets, regulated data, sensitive legal or HR matters, security incidents, or internal headers unless the deployment explicitly discloses and controls that data flow. <br>
Risk: The skill provides broad role-based guidance, including legal, HR, and security-oriented outputs. <br>
Mitigation: Treat responses as draft guidance and require qualified review before using them for sensitive decisions or operational changes. <br>


## Reference(s): <br>
- [ClawHub EMP release page](https://clawhub.ai/zzj0402/emp) <br>
- [OpenRouter](https://openrouter.ai/) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [SOUL protocol](SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Structured text with role, model, observation, feeling, need, and request fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an OPENROUTER_API_KEY; prompts are sent to OpenRouter and may be processed by downstream model providers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
