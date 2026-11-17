## Description:

Privacy-first UX research ethnographer for OpenClaw with a personal-finance lens that observes consented usage, logs structured behavioral events, and produces sanitized pulse reports for participant review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dflam1](https://clawhub.ai/user/dflam1)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw participants and UX researchers use this skill to collect consent-based behavioral observations about personal-finance workflows, then review sanitized observed-behavior and interpretation reports before any sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records broad local OpenClaw usage metadata after consent, including non-finance activity when general usage logging is enabled.

Mitigation: Review the consent notice and settings before starting research mode, and disable or limit general usage logging when only finance-specific activity should be collected.

Risk: Finance-related observations may involve sensitive personal or financial context even when the skill is designed to abstract and sanitize values.

Mitigation: Keep participant review enabled, use the sanitizer subagent before storing or sharing reports, and approve exports or sends only after reviewing the sanitized package.

Risk: Stored event logs and pulse reports can accumulate local behavioral data over time.

Mitigation: Use the configured retention window, pause or stop research mode for unrelated work, and delete research data by date range when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dflam1/skills/finance-ethnographer2)
- [Publisher profile](https://clawhub.ai/user/dflam1)
- [Settings schema](artifact/settings.schema.json)
- [Example pulse output](artifact/example-output.md)
- [Test plan](artifact/test-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with JSONL event records, JSON manifests, and settings JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sanitized observed-behavior and interpretation reports, redaction manifests, local state files, and participant-facing review choices.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
