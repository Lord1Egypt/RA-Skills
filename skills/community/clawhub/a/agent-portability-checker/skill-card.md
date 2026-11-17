## Description:

Audits agent skills for platform lock-in and cross-agent compatibility, including hardcoded platform paths, missing data-directory support, and platform-specific dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to audit agent skill directories for cross-agent portability issues and optionally apply automatic fixes for hardcoded paths, user-agent strings, and SKILL.md path references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-fix mode can rewrite skill files without strong containment, confirmation, backup, or diff support.

Mitigation: Use audit-only mode for untrusted skills; run --fix only on copied or version-controlled directories after reviewing the planned changes and avoiding directories with symlinks or important unrelated files.

## Reference(s):

- [Portability Checklist](artifact/references/checklist.md)
- [Channel Formatting](artifact/references/formatting.md)
- [ClawHub Skill Page](https://clawhub.ai/99rebels/skills/agent-portability-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown audit summaries, optional structured JSON, and file edits when auto-fix mode is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit-only mode reports findings; --fix can rewrite auto-fixable skill files.]

## Skill Version(s):

1.1.3 (source: server release metadata and audit.py VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
