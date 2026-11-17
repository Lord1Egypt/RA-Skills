## Description:

Automates B2B sales follow-up scheduling, generates personalized email drafts from customer stage and contact history, and syncs follow-up records with OKKI CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operators and CRM automation developers use this skill to schedule outbound follow-ups, prepare reviewable email drafts, and record follow-up activity in OKKI CRM for B2B leads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled CRM automation can write customer follow-up records to OKKI using weak record-matching safeguards.

Mitigation: Keep the skill in dry-run mode until exact CRM identity matching is required and live sync behavior has been reviewed.

Risk: Draft-controlled internal fields and local file writes may affect which draft records are updated.

Mitigation: Reject draft-supplied internal fields such as filepath and constrain draft reads and writes to the expected drafts directory.

Risk: Customer email addresses and sales context can appear in logs or CRM follow-up content.

Mitigation: Mask customer emails in logs, define log retention, and verify that CRM record content meets internal privacy rules.

Risk: Automation may be mistaken for permitted sending, archiving, or notification behavior.

Mitigation: Document which actions are allowed, require human review before any email is sent, and verify cron jobs before enabling scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/follow-up-engine)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [follow-up-rules.json](artifact/config/follow-up-rules.json)
- [follow-up-strategies.json](artifact/config/follow-up-strategies.json)
- [stage-transitions.json](artifact/config/stage-transitions.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON draft files, shell commands, and CRM follow-up records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates draft JSON files and log entries locally; live CRM sync is controlled by command mode and configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact docs also state 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
