## Description: <br>
Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warm-wm](https://clawhub.ai/user/warm-wm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this agent skill to create or update reusable skills with focused instructions, optional scripts, reference material, and packaged outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to write files and package generated skill content. <br>
Mitigation: Run it in a trusted workspace, avoid elevated privileges, and keep output paths inside the intended project or user skill directory. <br>
Risk: Generated skill instructions or scripts may be incomplete, misleading, or unsuitable for release. <br>
Mitigation: Review generated SKILL.md files, scripts, and packaged contents before installing, sharing, or relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/warm-wm/creator) <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and generated skill package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify SKILL.md files, reference files, scripts, and distributable .skill packages when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
