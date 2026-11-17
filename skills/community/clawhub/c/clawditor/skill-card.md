## Description:

Audit an OpenClaw agent workspace and generate standardized evaluation reports, scores, and patches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theylon](https://clawhub.ai/user/theylon)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Clawditor to audit OpenClaw workspaces for memory quality, retrieval efficiency, productive output, reliability, and goal alignment. It produces evidence-linked summaries, scorecards, JSON reports, and patch recommendations under an eval workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy sensitive memory or log snippets into report files.

Mitigation: Run it only on workspaces approved for audit, keep generated reports in a controlled eval directory, and inspect JSON and Markdown outputs before sharing or committing them.

Risk: The audit can be directed to write reports outside the intended workspace or overwrite prior reports.

Mitigation: Review output path and overwrite options before execution, and avoid broad log scanning or overwrite mode unless the target files are understood.

## Reference(s):

- [Clawditor Report Schema](artifact/references/report_schema.md)
- [Clawditor ClawHub Release](https://clawhub.ai/theylon/skills/clawditor)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance]

**Output Format:** [Markdown reports, structured JSON reports, and concrete patch recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be written under eval/ as exec_summary.md, scorecard.md, latest_report.json, and optional patch diffs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
