## Description: <br>
Auto Responder helps agents react to messages in configured topics using keyword, exclusion, template, and cooldown rules to avoid duplicate or excessive replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure autonomous topic-specific replies for OpenClaw agents. It is intended for agents that need to respond to inbound messages with controlled frequency and reusable response templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post automatically in group topics when wired into message hooks or heartbeats. <br>
Mitigation: Enable it only in trusted topics, narrow keyword rules, and consider requiring mentions for higher-risk spaces. <br>
Risk: The actual auto-responder executable or source is not included in the artifact evidence. <br>
Mitigation: Obtain and review the executable or source before installation, and inspect the persistent cache at ~/.cache/auto-responder.json. <br>
Risk: Loose templates or cooldown settings can create excessive or unwanted replies. <br>
Mitigation: Use conservative cooldowns, max response limits, exclusion terms, and topic-specific templates before enabling autonomous posting. <br>


## Reference(s): <br>
- [Auto Responder skill page](https://clawhub.ai/lunaviva211-sketch/auto-responder) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces configurable response templates, topic rules, cooldown guidance, and installation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
