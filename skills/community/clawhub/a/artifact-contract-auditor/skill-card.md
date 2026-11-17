## Description:

Audit the workspace against the pipeline artifact contract by checking DONE unit outputs and pipeline target artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill at the end of a pipeline run or before sharing a workspace to verify that required outputs and target artifacts are present. It produces an audit report with PASS, OK, or FAIL status and concrete next actions for missing artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports under-disclosed writes: the skill may update output/QUALITY_GATE.md in addition to output/CONTRACT_REPORT.md.

Mitigation: Run it only in workspaces where updates to both reports are acceptable, and review those files after execution.

Risk: The security scan reports path handling that can reach outside the expected workspace or pipeline directory.

Mitigation: Use trusted, non-symlinked workspace directories and trusted PIPELINE.lock.md contents before running the audit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/artifact-contract-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report and CLI status code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/CONTRACT_REPORT.md and may update output/QUALITY_GATE.md when the audit reaches a terminal quality state.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
