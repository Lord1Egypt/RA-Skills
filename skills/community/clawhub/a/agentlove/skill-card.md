## Description: <br>
AgentLove is a conversation-based OpenClaw setup wizard for backup migration, robot configuration, and personality/evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdodh22](https://clawhub.ai/user/bdodh22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use AgentLove to collect OpenClaw agent setup choices through a guided conversation and produce a configuration summary plus manual next steps for agent creation, skill installation, and channel credential setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste platform tokens or secrets into chat while working through channel setup. <br>
Mitigation: Use an explicit trigger such as /agentlove and configure credentials through the OpenClaw console rather than sending secrets in chat. <br>
Risk: Configuration choices may remain in process memory until reset or process restart. <br>
Mitigation: Avoid entering sensitive values into the wizard and reset the session or restart the process after handling sensitive setup decisions. <br>


## Reference(s): <br>
- [AgentLove configuration overview](artifact/references/configs.md) <br>
- [Execution flow](artifact/references/execution.md) <br>
- [Base layer configuration](artifact/references/layer1-base.md) <br>
- [Channel layer configuration](artifact/references/layer2-channels.md) <br>
- [Skills recommendation flow](artifact/references/layer3-skills.md) <br>
- [Personality configuration](artifact/references/personality.md) <br>
- [Preset role library](artifact/references/presets.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown conversation with JSON configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes manual follow-up steps for creating agents, installing skills, and configuring channel credentials.] <br>

## Skill Version(s): <br>
2.9.6 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
