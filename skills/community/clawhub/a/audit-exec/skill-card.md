## Description:

Audits OpenClaw exec commands across platforms, flags high-risk operations, applies whitelist filtering, and produces a risk-ranked execution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaodaabao](https://clawhub.ai/user/gaodaabao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit recent OpenClaw exec commands, classify risky operations, and produce a report for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whitelist matching can incorrectly hide dangerous commands.

Mitigation: Treat the OK or whitelisted section as advisory only and manually review transcript commands, especially compound commands.

Risk: The skill reads local OpenClaw command transcripts that may contain sensitive command history.

Mitigation: Run it only in trusted environments and avoid sharing generated reports without reviewing them for sensitive commands or paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaodaabao/skills/audit-exec)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain-text or Markdown-style audit report with command counts, risk labels, timestamps, and reasons.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews recent transcript entries and separates high-risk, medium-risk, low-risk, and whitelisted commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
