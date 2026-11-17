## Description:

Summarize Codex token usage from local Codex Desktop or CLI session JSONL logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helenalhq](https://clawhub.ai/user/helenalhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit Codex token usage over requested time windows and report totals, input, cached input, output, reasoning output, net usage, cache hit rate, daily averages, peak day, and busiest week.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Codex session logs, and its reports may expose sensitive usage volumes, dates, or activity patterns.

Mitigation: Run it only against intended local Codex log directories and avoid sharing report output when usage counts, dates, or volumes are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helenalhq/skills/codex-token-usage)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown table or JSON report, with concise explanatory text and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports token totals, calls, sessions, cache hit rate, daily average, peak day, and busiest week for a selected date range.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
