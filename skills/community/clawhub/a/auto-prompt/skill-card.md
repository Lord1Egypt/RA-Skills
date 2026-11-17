## Description:

AUTO.Prompt is a strategy-first problem-solving protocol that guides an agent to create a concise strategy card, review it once against the user's request, execute the shortest supported path, and save only reusable factual conclusions to memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fore-auto](https://clawhub.ai/user/fore-auto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent plan before acting on open-ended tasks, solution requests, or strategy questions, with a fixed reuse order and a single adversarial review pass. It is intended to keep outputs concise, conclusion-first, and limited to the requested scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist project or cross-project memory that may influence future agent behavior.

Mitigation: Review `.workbuddy` memory files periodically and avoid using the skill on sensitive tasks unless the agent asks before persisting anything.

Risk: The skill intentionally shapes general problem-solving behavior across broad tasks.

Mitigation: Install it only when that planning posture is desired, and prefer specialized domain skills when they directly match the task.

## Reference(s):

- [T1 Source Routing Reference](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/fore-auto/skills/auto-prompt)
- [Publisher Site](https://fore.vip)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with concise strategy cards and conclusion-first responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write selected project or cross-project memory entries when the task is resolved and the skill's four memory criteria are met.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
