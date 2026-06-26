## Description: <br>
Dataset Intake Auditor checks fields, units, missing value rates, outliers, and usability before a new dataset is ingested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, analysts, and governance reviewers use this skill to review CSV or TSV datasets before intake. It produces a readable audit of dataset overview, field summaries, missing and outlier checks, unit risks, intake recommendations, and follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local dataset files and writes reports, which may include sensitive or regulated data from the input. <br>
Mitigation: Run it only on files you are allowed to analyze, choose output paths deliberately, and review or redact reports before sharing. <br>
Risk: Changing the bundled specification could broaden what the audit script inspects or reports. <br>
Mitigation: Treat spec changes as intentional configuration changes and review the generated report behavior after any modification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/dataset-intake-auditor) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report, with optional JSON output from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are review-oriented and may include dataset summaries, missingness and outlier observations, unit and definition risks, recommendations, follow-up actions, and explicit items requiring confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
