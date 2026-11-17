## Description:

ARC multi-agent collaboration for planning, execution, review, summarization, research, criticism, and iterative peer review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate complex work through role-based task decomposition, dependency-ordered execution, peer review, and synthesis into a structured report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unreviewed local Python module under D:\coze-local\db.

Mitigation: Install only after separately reviewing and controlling that local module.

Risk: Delegated capabilities may run automatically through broad triggers.

Mitigation: Require explicit user confirmation before running delegated capabilities.

Risk: SkillEvolver may persist behavior or storage changes.

Mitigation: Review and approve persistent evolution behavior before enabling it.

## Reference(s):

- [Agent tracing and observability learning reference](https://www.bilibili.com/video/BV1BwVd6xEd8)
- [Caveman agent efficiency learning reference](https://www.bilibili.com/video/BV1hdV96rEiV)
- [MUSE-Autoskill skill evolution learning reference](https://www.bilibili.com/video/BV1QPVf6QEF1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured reports after coordinating delegated agent roles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
