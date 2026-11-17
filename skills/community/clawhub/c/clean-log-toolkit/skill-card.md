## Description:

Clean Log Toolkit helps agents inspect local log files by parsing common formats, aggregating errors, filtering by pattern, time, level, and context, following live logs, and producing structured reports without third-party dependencies or remote calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers, support engineers, and agents use this skill to inspect local log files, convert logs into structured outputs, find error clusters, filter incident windows by time, level, and pattern, and prepare reports for tickets or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output files can overwrite source logs or symlink aliases, which can cause data loss.

Mitigation: Use a separate output directory and confirm output paths are not the original log path or a symlink to it before running parse, grep, or error-report commands.

Risk: Generated reports can preserve sensitive raw log content.

Mitigation: Inspect and redact reports before sharing them in tickets, repositories, spreadsheets, or chat.

## Reference(s):

- [Clean Log Toolkit ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/skills/clean-log-toolkit)
- [Clean Log Toolkit ClawHub homepage](https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit)
- [Related Clean CSV Toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)
- [Related Clean Text Toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, TSV, JSONL, shell commands, guidance]

**Output Format:** [Plain text summaries, filtered log lines, Markdown reports, JSON reports, CSV/TSV tables, JSONL rows, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local stdout output or files at caller-provided paths; follow.py can stream matched lines as JSON envelopes.]

## Skill Version(s):

0.2.0 (source: release metadata and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
