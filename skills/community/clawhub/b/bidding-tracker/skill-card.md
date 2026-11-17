## Description:

Manages military and government procurement bid opportunities, including project registration, document purchase tracking, sealing and opening milestones, results entry, statistics, and win-probability evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and agent operators use this skill to track military and government bid projects across registration, document purchase, bid sealing, opening results, team access, statistics, and tender-document evaluation. It is scoped to bid-opportunity management and does not cover contract fulfillment, invoicing, reimbursement, or non-bidding procurement consulting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document evaluation can read local files available to the skill process.

Mitigation: Run the skill only in trusted directories and restrict who can provide file paths or attachments for evaluation.

Risk: Local bid data, attachments, and role-scoped records may be exposed if the database or attachment directory is shared too broadly.

Mitigation: Restrict filesystem permissions for the SQLite database and attachment directories, and deploy in a trusted single-user or tightly controlled OpenClaw/WeCom environment.

Risk: CLI identity handling can create role-access risk if the command surface is exposed to untrusted users.

Mitigation: Do not expose the CLI to untrusted users; mediate access through a controlled agent environment with known user context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpengle/skills/bidding-tracker)
- [Publisher profile](https://clawhub.ai/user/zhangpengle)
- [README](artifact/README.md)
- [Skill usage guide](artifact/SKILL.md)
- [Evaluation prompt](artifact/bidding_tracker/prompts/evaluate_prompt.md)
- [Strategic entity profiles](artifact/bidding_tracker/prompts/profiles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command responses, Markdown analysis prompts, and concise CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evaluation output can include extracted tender text, the analysis prompt, profile context, status messages, and local project-tracking data.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
