## Description:

Analyzes weekly or monthly repository changes, generates code quality delivery reports, performs AI scoring and review, and synchronizes results to a code quality database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fightingdao](https://clawhub.ai/user/fightingdao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering managers use this skill to analyze repository commit history and diffs over weekly or monthly periods, produce code quality reports, review issues, and sync results into a code-quality tracking database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can replace database records for selected reporting periods during synchronization.

Mitigation: Confirm the reporting period before sync, use a dry run or backup first, and verify that only the intended period is overwritten.

Risk: The skill analyzes repository history and diffs that may contain confidential code.

Mitigation: Use it only in approved workspaces and keep confidential repository review local unless external model review is explicitly approved.

Risk: The skill may delegate code review to a provider-qualified child model without clear consent.

Mitigation: Require explicit user consent before model delegation and document which model or review environment will receive repository content.

Risk: The skill relies on environment-specific paths, localhost services, and team or project identifiers.

Mitigation: Review and replace local configuration before use, and confirm target team and project mappings before writing analysis data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fightingdao/skills/fightingdao-code-quality-analyzer)
- [FightingDao publisher profile](https://clawhub.ai/user/fightingdao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured analysis notes, shell commands, SQL/API sync guidance, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository diff analysis, database sync steps, issue tables, and notification guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
