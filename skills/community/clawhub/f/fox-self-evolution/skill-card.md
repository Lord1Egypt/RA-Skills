## Description: <br>
Documents an agent-facing self-evolution workflow for planning, validating, rolling back, and recording changes to skills, memory, reasoning behavior, and response formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators can use this skill as guidance for experimenting with agent self-improvement workflows, including proposed change planning, validation, rollback, and documentation. The artifact is marked as planned and not yet implemented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill tells an agent it may change its own skills, memory, and behavior without asking the user. <br>
Mitigation: Install only in an isolated test workspace and require explicit approval plus visible diffs before changes to skills, prompts, memory, reasoning behavior, response formats, scheduled agents, or logs. <br>
Risk: The security guidance says safety and formal-verification claims should be treated as unverified. <br>
Mitigation: Validate proposed changes with independent review and testing before relying on any claimed safety, rollback, or verification behavior. <br>
Risk: The artifact status says the skill is planned and not yet implemented. <br>
Mitigation: Treat the content as design guidance unless implementation evidence is supplied and validated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tihuaqin-commits/fox-self-evolution) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Implementation status](artifact/PLANNED.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file, skill, memory, and behavior changes that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
