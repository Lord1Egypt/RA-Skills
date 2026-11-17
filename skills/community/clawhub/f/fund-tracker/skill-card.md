## Description:

Tracks fund purchase availability, daily purchase quotas, fees, and changes since the previous run with AKShare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alondotsh](https://clawhub.ai/user/alondotsh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether configured funds are open for purchase, limited by quota, paused, or changed since the previous check. The output is informational and is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted preset names can cause history-file reads or writes outside the intended runtime folder.

Mitigation: Use only simple preset names containing letters, numbers, hyphens, or underscores, and review preset names before running the checker.

Risk: The checker fetches public fund data through AKShare and Eastmoney, so network or upstream schema changes can affect results.

Mitigation: Run in a reviewed environment, treat JSON errors as data-source failures, and verify important fund information against an authoritative source before acting.

Risk: The skill writes local runtime history files for change tracking.

Mitigation: Keep runtime history local, avoid committing generated history, and run the skill in a virtual environment or container when possible.

## Reference(s):

- [Fund Tracker Skill Page](https://clawhub.ai/alondotsh/skills/fund-tracker)
- [README](artifact/README.md)
- [Chinese README](artifact/README.zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown table and short summary derived from JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads preset configuration and writes local runtime history files for change tracking.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
