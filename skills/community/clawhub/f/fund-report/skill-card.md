## Description:

Fund Report provides real-time OTC fund net asset value estimates and estimated price changes, with support for querying multiple fund codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wndagg](https://clawhub.ai/user/wndagg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce concise fund holding reports for multiple OTC fund codes, including estimated net value movement and estimated gains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references scripts/fund_report.py, but that script is not bundled in the package.

Mitigation: Only run a local scripts/fund_report.py after confirming its source and reviewing its contents.

Risk: The skill documentation is in Chinese, which may make review harder for non-Chinese-speaking operators.

Mitigation: Have a reviewer who can read Chinese confirm the intended behavior before deployment.

## Reference(s):

- [Fund Report ClawHub page](https://clawhub.ai/wndagg/skills/fund-report)
- [Project homepage](https://github.com/wNDAGG/mimi-scripts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on a local scripts/fund_report.py file that is referenced by the skill but not included in the package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
