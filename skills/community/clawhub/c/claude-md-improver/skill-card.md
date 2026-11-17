## Description:

Audit and improve CLAUDE.md files in repositories by locating project memory files, evaluating them against quality criteria, reporting gaps, and applying targeted updates after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to audit and maintain CLAUDE.md project memory files so Claude Code has concise, current commands, architecture notes, and gotchas across repositories and monorepos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-documented commands may be run during assessment without separate command-specific approval.

Mitigation: Before using the skill on untrusted repositories, instruct the agent not to execute commands from CLAUDE.md or project documentation unless you approve each exact command.

## Reference(s):

- [CLAUDE.md Quality Criteria](references/quality-criteria.md)
- [CLAUDE.md Templates](references/templates.md)
- [CLAUDE.md Update Guidelines](references/update-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown quality reports, proposed diffs, and targeted CLAUDE.md edits after approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports file-by-file quality scores before proposing or applying updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
