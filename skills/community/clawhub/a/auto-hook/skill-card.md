## Description:

检查指定 SKILL 是否存在偷懒、跳步、简化执行等问题，并可为 Claude Code、OpenAI Codex CLI 和 OpenClaw 技能注入或撤销自审计钩子。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panhongwei](https://clawhub.ai/user/panhongwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to inspect agent skill instructions for skipped or simplified execution and to add or remove a persistent self-audit hook across supported agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally creates persistent self-audit hooks inside other skills, changing future agent behavior.

Mitigation: Use it only when that behavior is intended, keep backups of original SKILL.md files, and inspect generated diffs before replacing any original skill.

Risk: The documented rollback flow has broad triggers and deletion boundaries that can remove valid content after a detected hook marker.

Mitigation: Use rollback only on backed-up skills and review the cleaned SKILL.md before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panhongwei/skills/auto-hook)
- [hook.md](artifact/hook.md)
- [skill-audit-hook.txt](artifact/skill-audit-hook.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and file-edit instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent modifications to SKILL.md files; users should inspect diffs before replacing originals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
