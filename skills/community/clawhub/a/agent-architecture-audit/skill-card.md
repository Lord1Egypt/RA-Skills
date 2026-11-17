## Description:

Audit agent system architecture across 12 layers for wrapper regression, memory pollution, tool discipline failures, and hidden fix loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit agent architectures for structural regressions, memory pollution, tool discipline failures, transport issues, and hidden repair loops, then produce severity-ranked findings and a code-first fix plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture audit reports may summarize sensitive internal project details from local files, logs, configuration, or memory artifacts.

Mitigation: Review gathered evidence and redact reports before sharing them outside the intended review audience.

Risk: The workflow is written primarily in Chinese, which may make review harder for teams that do not read Chinese.

Mitigation: Have a Chinese-proficient reviewer validate the audit instructions and findings before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/agent-architecture-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown report with optional JSON report structure and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings, architecture diagnosis, ordered fix plan, evidence references, confidence scores, and recommended fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
