## Description: <br>
A minimal but concrete diagnostic skill used to verify whether ClawHub publish and install return the same SKILL.md content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miniade](https://clawhub.ai/user/miniade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to check whether a ClawHub install or update returns the same SKILL.md content that was published. It is a diagnostic fixture for investigating publish, cache, registry, or install consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a diagnostic fixture rather than a production workflow skill, so it may not be useful outside ClawHub publish and install consistency checks. <br>
Mitigation: Install and use it only when testing ClawHub registry behavior or inspecting whether installed SKILL.md content matches the published copy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miniade/clawhub-publish-debug-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown checklist and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, tool calls, or external service access are performed by the skill content.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
