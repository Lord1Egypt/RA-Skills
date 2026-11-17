## Description:

Agent Pool defines a global registry of business agents, including capabilities, tool dependencies, memory paths, workspaces, trigger conditions, and onboarding rules for on-demand orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renxm78-creator](https://clawhub.ai/user/renxm78-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business workflow owners use this skill to find registered agents, compose new workflows, and onboard new agents without pre-binding them to a system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support live marketing workflows that include customer research and outbound LinkedIn or email actions without clear approval boundaries.

Mitigation: Require explicit human approval before posts, comments, email sends, or customer research are executed.

Risk: The skill describes persistent shared knowledge storage in knowledge-base and MEMORY.md paths.

Mitigation: Define what data may be written to shared knowledge and memory files before deployment.

## Reference(s):

- [Agent Detailed Registry](references/agent-registry.md)
- [System Onboarding Template](references/system-template.md)
- [ClawHub Skill Page](https://clawhub.ai/renxm78-creator/skills/agent-pool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with registry tables and structured configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes agent capability, tool dependency, memory path, workspace, trigger condition, and system onboarding references.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
