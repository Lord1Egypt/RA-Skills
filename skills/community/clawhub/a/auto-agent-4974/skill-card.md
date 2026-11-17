## Description:

Provides a step-by-step Bilibili-based learning helper for building personal AI agents, with references spanning beginner setup, agent workflows, and reusable skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to collect and apply tutorial references about creating personal AI agents from Bilibili learning material. It is suited for guided learning and knowledge-base capture around agent construction topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads code from an external local module path.

Mitigation: Install only where D:\\coze-local\\db and learn.py are trusted, reviewed, and protected from modification.

Risk: The skill can persist caller-supplied text into a local knowledge base.

Mitigation: Use explicit invocation or review before writes, and audit the knowledge base after use.

Risk: Automatic activation on the broad keyword "agent" could cause accidental knowledge writes.

Mitigation: Narrow activation rules or require user confirmation before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/auto-agent-4974)
- [Bilibili source video BV1jAVh6UEmZ](https://www.bilibili.com/video/BV1jAVh6UEmZ)
- [Caveman agent tutorial](https://www.bilibili.com/video/BV1hdV96rEiV)
- [Claude Code Auto Mode tutorial](https://www.bilibili.com/video/BV1Ky9yBzEBY)
- [Notion Custom Agent tutorial](https://www.bilibili.com/video/BV16eAGzbENv)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Boolean completion signal with console text and local knowledge-base entry behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist caller-supplied text into a local knowledge base when invoked.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
