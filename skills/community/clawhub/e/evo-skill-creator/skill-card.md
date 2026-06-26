## Description: <br>
Creates self-learning, continuously evolving domain-expert agent skills and supports their learning, review, and upgrade workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyao721](https://clawhub.ai/user/wuyao721) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design new self-evolving agent skills, plan learning work, scan for agent-design trends, and review or upgrade existing skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation, modification, scheduling, and upgrade of other agent skills. <br>
Mitigation: Use narrow workspace permissions, review generated skill changes before enabling them, and keep upgrade workflows under explicit user approval. <br>
Risk: Loose natural-language triggers could start creation or upgrade workflows when the user intended only discussion. <br>
Mitigation: Restrict activation to explicit commands for high-impact workflows such as creating, reviewing, upgrading, or scheduling agents. <br>
Risk: Permission templates include a full-access option that could grant broad filesystem and shell access. <br>
Mitigation: Prefer the basic scoped permission template and manually review any generated .claude/settings.local.json or scheduler configuration before use. <br>
Risk: Stateful memory, reports, and logs may contain private user data or operational details. <br>
Mitigation: Exclude private memory and output logs from shared packages, and inspect generated files before publishing or distribution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuyao721/evo-skill-creator) <br>
- [Self-Evolving Agent Model](references/evo-agent-model.md) <br>
- [Model Capability Rules](references/model-capability.md) <br>
- [Local Settings Permission Template](references/settings.local.json.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, file edits, configuration snippets, reports, and logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create skill files, memory files, reports, logs, and permission templates when the host agent has workspace access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
