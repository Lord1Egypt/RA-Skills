## Description:

Diskmon helps agents record, search, summarize, and export local disk-related observations from a Bash command-line utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sysadmins, and operations teams can use this skill to log disk observations, maintenance notes, alerts, cleanup activity, backup notes, benchmark results, and searchable history. It should be treated as a local documentation aid, not as an automated disk monitor, alerting system, cleanup tool, backup tool, or restore tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marketed as real disk monitoring, but the reviewed behavior records plaintext notes and exports rather than performing automated monitoring or alerting.

Mitigation: Use it only for local note and history tracking; rely on dedicated monitoring, alerting, cleanup, backup, and restore tooling for operational protection.

Risk: Disk observations, infrastructure names, incident details, and maintenance notes may be stored in plaintext local logs and exported files.

Mitigation: Avoid entering secrets or sensitive infrastructure details unless plaintext local storage is acceptable for the deployment environment.

## Reference(s):

- [Diskmon ClawHub skill page](https://clawhub.ai/ckchzh/skills/diskmon)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON, CSV, TXT, and log file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext logs and exports under ~/.local/share/diskmon when its shell script is used.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
