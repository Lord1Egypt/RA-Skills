## Description: <br>
Artifact Analysis turns local documents and project knowledge into auditable scan plans, per-slice findings, and citation-backed synthesis reports on disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze local project documents, preserve path-anchored evidence, and produce structured reports without returning unsourced inline prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Findings and reports may retain verbatim excerpts from scanned local documents. <br>
Mitigation: Choose a clear output directory and avoid scanning private material that should not be persisted in analysis files. <br>
Risk: The skill reads local paths selected by the caller or auto-discovery. <br>
Mitigation: Review the generated plan.md and its resolved paths before relying on the final report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/artifact-analysis) <br>
- [Citation Schema](artifact/references/citation-schema.md) <br>
- [Companion Invocation Contract](artifact/references/companion-contract.md) <br>
- [Failure Modes](artifact/references/failure-modes.md) <br>
- [Synthesis Skeleton](artifact/references/report-template.md) <br>
- [Default Skip Patterns](artifact/references/skip-patterns.md) <br>
- [Subagent Brief Template](artifact/references/subagent-brief.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files written to disk, including plan.md, findings files, and report.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include path-anchored citations and record gaps, skipped paths, and verification failures.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
