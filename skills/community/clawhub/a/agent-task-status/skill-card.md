## Description:

Verify whether named OpenClaw agents received formal task assignments and replied with execution status, using transcript-backed audit checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujohn74](https://clawhub.ai/user/lujohn74)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw delegation by checking local agent transcripts for the latest assignment, report, status, result, and risk fields. It supports human review and automation workflows that need transcript-backed confirmation of whether agents received and reported on work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local OpenClaw session transcripts that may contain sensitive assignment or report content.

Mitigation: Use explicit agent and base-path options, prefer tail-limited scans when full transcripts are unnecessary, and write output files only to locations appropriate for potentially sensitive excerpts.

## Reference(s):

- [Usage](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the bundled script can emit table, summary, JSON, or JSONL status reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may include local session file paths, assignment excerpts, parsed report fields, normalized statuses, and errors.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
