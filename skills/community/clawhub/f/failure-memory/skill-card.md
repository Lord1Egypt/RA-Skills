## Description: <br>
Stop making the same mistakes by turning failures into patterns that prevent recurrence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to detect repeated failures, record workspace-local observations, search prior mistakes, and promote recurring patterns into constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may record normal conversation or incorrect conclusions as failure memories. <br>
Mitigation: Install only when local failure notes are wanted, and periodically inspect or clear .learnings/ if lessons are incorrect. <br>
Risk: Workspace-local learning files may influence future agent behavior with stale or overly broad patterns. <br>
Mitigation: Review observations before promoting them into constraints, especially when recurrence and confirmation counts are low. <br>


## Reference(s): <br>
- [Failure Memory on ClawHub](https://clawhub.ai/leegitw/failure-memory) <br>
- [Publisher profile](https://clawhub.ai/user/leegitw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented text with workspace-local observation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read optional configuration from .openclaw/failure-memory.yaml or .claude/failure-memory.yaml and write learning notes under .learnings/.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
