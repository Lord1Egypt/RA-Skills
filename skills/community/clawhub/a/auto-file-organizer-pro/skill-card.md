## Description:

自动整理专业版 helps agents organize files through duplicate-file review, content-aware classification, scheduled batch processing, real-time folder monitoring, shared rules, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and run file governance workflows: finding duplicate files, classifying documents by content-aware rules, scheduling batch organization, monitoring folders, exporting reports, and sharing team rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automated authority over user files can move, reorganize, or deduplicate files beyond the intended scope.

Mitigation: Start with narrow test folders, require dry-run plans before deduplication or moves, and confirm target paths and retention policies before execution.

Risk: Watch, schedule, and daemon modes can continue changing files in the background.

Mitigation: Avoid enabling background modes until rollback behavior is understood, and keep monitoring limited to explicit folders with a clear stop procedure.

Risk: Email, callback, notification, or team sync features may expose file-operation metadata outside the local machine.

Mitigation: Configure network notifications and team sync only when metadata sharing is acceptable, and keep credentials in environment variables.

## Reference(s):

- [Detailed reference](artifact/references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/auto-file-organizer-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and YAML/JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run plans, organization reports, status summaries, execution logs, and structured JSON-style result examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
