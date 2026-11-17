## Description:

Daily Income Logger helps agents record daily income from multiple platforms, summarize daily earnings, analyze weekly or monthly trends, and export reports as CSV or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesiyoq965-sudo](https://clawhub.ai/user/mesiyoq965-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators can use this skill to keep local records of daily platform income, review short-term earnings trends, and generate exportable income reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Income records are stored locally as plaintext JSON files.

Mitigation: Use the skill only on trusted machines, restrict file and directory permissions to the owner, and avoid sharing or committing the generated data files.

Risk: The sample update command uses a fixed tmp.json path and does not include locking.

Mitigation: Harden the command before repeated or shared use by using a unique temporary file, atomic replacement, and a lock around updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mesiyoq965-sudo/skills/daily-income-logger)
- [Publisher profile](https://clawhub.ai/user/mesiyoq965-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local-file workflow guidance for income records stored under ~/.daily-income-logger.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/package.json, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
