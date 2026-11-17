## Description:

Create price watch tasks and receive IM notifications when freight rates are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobofrivia](https://clawhub.ai/user/bobofrivia)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and logistics agents use this skill to create ocean-freight price watch tasks, register polling for watch results, and notify users when freight rates are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create an indefinite recurring OpenClaw cron task that runs shell execution.

Mitigation: Review installation before production use, document ownership of eyun-watch-poll, and define procedures to list, audit, expire, or remove the cron when no watches remain.

Risk: The skill polls an external Eyun endpoint and sends freight-rate notifications to an external channel.

Mitigation: Use only a trusted Eyun endpoint over HTTPS, validate EYUN_BASE_URL and EYUN_COMPANY_ID, and restrict notifications to an approved channel and recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobofrivia/skills/eyun-watch)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing replies and notifications are primarily in Chinese; operation requires EYUN_BASE_URL, EYUN_COMPANY_ID, curl, and an approved notification channel.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
