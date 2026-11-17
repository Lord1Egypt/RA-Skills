## Description:

Multi-agent adversarial debate skill that coordinates Pro, Con, Judge, and Orchestrator roles with evidence refresh, five-part reasoning chains, and bilingual Markdown reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwxga](https://clawhub.ai/user/xwxga)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to run structured adversarial debates, red-team a topic, gather and refresh evidence, audit claims, and produce decision-oriented debate reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search the web or fetch pages while handling sensitive debate topics.

Mitigation: Use the skill only when external search is acceptable, and avoid confidential topics unless the runtime's web permissions are constrained.

Risk: The skill writes debate artifacts and audit logs into a workspace.

Mitigation: Run it in a dedicated, constrained workspace and review generated files before reusing them.

Risk: The skill can invoke local agent runtimes such as Claude or Codex through its orchestrator.

Mitigation: Confirm the available runtime, model settings, and execution permissions before running full debate orchestration.

Risk: The artifact describes optional recurring refresh behavior.

Mitigation: Approve persistence only when scheduled refresh is intended, and review or remove any cron configuration after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xwxga/skills/critical-debater)
- [Project Homepage](https://github.com/xwxga/critical-debater)
- [Data Contracts](artifact/references/data-contracts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON artifacts and Markdown reports with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates debate workspace files such as evidence stores, claim ledgers, round rulings, final_report.json, and debate_report.md when run.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
