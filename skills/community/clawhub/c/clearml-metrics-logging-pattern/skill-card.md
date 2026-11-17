## Description:

Standardized ClearML metrics logging patterns for PDEBench experiment scripts, including train loss, validation metrics, competition scores, PDE residuals, TensorBoardX integration, and dist/expflow compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill when adding or standardizing ClearML metric logging in PDEBench training and evaluation scripts so experiment runs can be compared consistently through expflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClearML experiment tracking can record metrics and related run details that may expose sensitive dataset information or secrets if logging is configured carelessly.

Mitigation: Review ClearML configuration before use, avoid logging secrets or sensitive dataset details, and prefer a self-hosted or governed ClearML server for private experiments.

Risk: Unpinned uvx or tool launches can reuse an installed tool environment and run an older or unexpected expflow release.

Mitigation: Pin expflow-pde versions in launch commands when reproducibility or supply-chain hygiene matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diamond2nv/skills/clearml-metrics-logging-pattern)
- [expflow Homepage](https://github.com/diamond2nv/expflow)
- [Publisher Profile](https://clawhub.ai/user/diamond2nv)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code templates, shell commands, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes metric naming conventions, installation options, ClearML telemetry guidance, and known pitfalls.]

## Skill Version(s):

0.7.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
