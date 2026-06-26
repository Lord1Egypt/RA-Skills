## Description: <br>
Gestalt is a model-agnostic prompt-style collaboration skill that makes an agent more direct, substantive, explicit about uncertainty, and disciplined about memory use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwgoldie](https://clawhub.ai/user/dwgoldie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, coding-agent users, and chatbot users use Gestalt to steer language models toward terse, constructive collaboration: lead with answers, challenge weak assumptions, disclose uncertainty, and preserve durable decisions without saving secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes agent behavior and may make responses more direct or autonomous than users expect. <br>
Mitigation: Review the prompt text before deployment and keep explicit control over consequential actions such as commits, pushes, deletions, and privacy-sensitive steps. <br>
Risk: In coding-agent environments, durable memory files can accidentally capture sensitive or transient details. <br>
Mitigation: Use the skill only in trusted repositories, avoid saving secrets or sensitive information, and periodically review memory files created by the agent. <br>


## Reference(s): <br>
- [Gestalt ClawHub page](https://clawhub.ai/dwgoldie/gestalt) <br>
- [dwgoldie publisher profile](https://clawhub.ai/user/dwgoldie) <br>
- [README.md](README.md) <br>
- [AGENTS.md](AGENTS.md) <br>
- [CHATBOTS.md](CHATBOTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown prompt instructions and custom-instruction text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes variants for coding-agent files and chatbot custom-instruction fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
