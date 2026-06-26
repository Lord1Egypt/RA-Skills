## Description: <br>
Anthropic Chat lets an agent send natural language tasks to Claude through the Anthropic Messages API using the user's Anthropic API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liutao0401-afk](https://clawhub.ai/user/liutao0401-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route task prompts to Claude through Anthropic's Messages API with their own API key. It is useful when an agent needs Claude-generated text or code responses without adding a separate authentication flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task text are sent to Anthropic's API. <br>
Mitigation: Avoid sending secrets or regulated data unless approved, and use a restricted API key with appropriate spending limits. <br>
Risk: The skill requires an Anthropic API key in the runtime environment. <br>
Mitigation: Store ANTHROPIC_API_KEY only in controlled environments, rotate it if exposed, and avoid embedding it in skill files or prompts. <br>
Risk: The helper appears to reference an undeclared TASK variable and may need runtime wiring. <br>
Mitigation: Test the skill in the target agent runtime and ensure task input is correctly provided before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liutao0401-afk/anthropic-chat) <br>
- [Publisher profile](https://clawhub.ai/user/liutao0401-afk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Anthropic Messages API JSON response containing generated text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ANTHROPIC_API_KEY environment variable, supports ANTHROPIC_MODEL, and sets max_tokens to 4096.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
