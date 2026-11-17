## Description:

AAR with folder-based lessons, auto-trigger for all tasks, US Army 4-question method for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run After Action Reviews after tasks, capture concrete lessons, and maintain persistent lesson files that can guide future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent workspace memory after tasks.

Mitigation: Use explicit invocation or review before logging lessons, and regularly inspect stored lesson files.

Risk: Lesson content could capture secrets, client data, or sensitive operational details.

Mitigation: Do not log credentials or sensitive client information; redact sensitive task details before writing lessons.

Risk: Automatically loading prior lessons can carry incorrect or outdated guidance into future sessions.

Mitigation: Avoid adding the LESSONS.md auto-load pointer unless the stored lessons are trusted and periodically reviewed.

Risk: Proposed durable fixes to skills or rule files could change future agent behavior.

Mitigation: Require user approval before applying fix plans to persistent instructions or skill files.

## Reference(s):

- [AAR Loop ClawHub page](https://clawhub.ai/akdira/skills/aar-loop)
- [Publisher profile](https://clawhub.ai/user/akdira)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated lesson files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates persistent workspace lesson files when the included logging script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence and CLAWHUB.md; artifact/SKILL.md declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
