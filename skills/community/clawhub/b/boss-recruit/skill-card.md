## Description:

BOSS Recruit Assistant helps process a BOSS Zhipin recruiting inbox by reading candidate resumes, syncing candidate records and resume attachments to Feishu Base, and optionally drafting or sending resume-request messages under controlled pacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

HR users and recruiting operators use this skill to triage BOSS Zhipin new-greeting inbox items, copy candidate profile data into a Feishu talent table, download visible resume attachments, and request missing resumes only when explicitly run in live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill acts through a logged-in BOSS account and can perform browser automation that may trigger platform account restrictions.

Mitigation: Run small batches, keep the default dry-run mode for outward messages, review before using --live, and stop when platform risk signals or verification challenges appear.

Risk: The skill handles candidate resumes and personal data while syncing records to Feishu Base.

Mitigation: Use only accounts and candidate data the operator is authorized to process, restrict local file permissions, and configure a dedicated least-privilege Feishu token.

Risk: The artifact includes anti-detection browser automation guidance and cookie-reuse attachment download behavior.

Mitigation: Review whether those behaviors are acceptable for the deployment context and remove the anti-detection guidance or cookie-reuse adapter before operational use if they conflict with policy or platform terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/casperkwok/skills/boss-recruit)
- [README](README.md)
- [AGENTS](AGENTS.md)
- [Anti-Detection Reference](references/anti-detection.md)
- [OpenCLI](https://github.com/jackwener/opencli)
- [Claude Code](https://claude.com/claude-code)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script-generated structured progress output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runnable scripts can write local task memory, target configuration, downloaded resume PDFs, and Feishu Base records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
