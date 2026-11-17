## Description:

Automates company due-diligence collection across Qichacha, Tianyancha, Eastmoney, and China Judgments Online, then generates screenshot-backed Markdown and PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangningsun](https://clawhub.ai/user/guangningsun)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to gather public and authenticated company due-diligence data, capture source screenshots, and produce Markdown or PDF diligence reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled browser session and cookie files may expose authenticated accounts or reusable site access.

Mitigation: Remove all bundled session and cookie files before installation, rotate any exposed accounts, and require users to create fresh local sessions.

Risk: Unsafe command execution paths can allow unintended shell behavior when inputs are passed through command construction.

Mitigation: Replace shell-based command construction with argument-list subprocess calls and validate user-supplied company names, paths, and options.

Risk: Reports, screenshots, raw data, and browser sessions may contain sensitive due-diligence information.

Mitigation: Add clear controls for output directories, retention, access permissions, and cleanup of generated reports and browser state.

Risk: Unpinned dependencies can change behavior or security posture between installations.

Mitigation: Pin dependency versions and review updates before publishing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guangningsun/skills/company-due-diligence)
- [Publisher profile](https://clawhub.ai/user/guangningsun)
- [Data Sources](references/data_sources.md)
- [Due Diligence Framework](references/framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, optional PDF reports, screenshots, and raw JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser sessions for authenticated data sources and writes report artifacts to configured local report directories.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
