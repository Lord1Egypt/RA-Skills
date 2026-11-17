## Description:

Reviews agent skills for structure, YAML frontmatter, description quality, instruction completeness, examples, and publishability against Anthropic-style skill guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzxiaoshan](https://clawhub.ai/user/xzxiaoshan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review agent skill folders or SKILL.md content, score documentation and instruction quality, and produce issue reports with improvement recommendations before publication or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional install workflow uses an unpinned npx command that can execute mutable third-party code.

Mitigation: Provide a local skill folder when possible, or run package installation only in a disposable sandbox with a pinned, verified version.

Risk: The review workflow may prompt an agent to inspect target skill folders that contain private instructions or files.

Mitigation: Review only intended local skill directories and avoid exposing private skill content to untrusted tools or external contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xzxiaoshan/skills/agent-skill-reviewer)
- [Anthropic Skills Development Guide](references/anthropic-skills-development-guide.md)
- [Skill Review Checklist](references/checklist.md)
- [Official Guide Summary](references/official-guide-summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with checklist scores, findings, shell command examples, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt the agent to inspect local skill folders and, in one optional workflow, install a named skill before review.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
