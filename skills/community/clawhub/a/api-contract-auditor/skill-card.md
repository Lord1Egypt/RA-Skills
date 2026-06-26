## Description: <br>
Reviews API documentation, examples, and field definitions for consistency and surfaces breaking-change risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API reviewers use this skill to audit API documentation, OpenAPI text, examples, or documentation folders before interface reviews, releases, or integration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script reads the user-provided input path and can write a report when an output path is supplied. <br>
Mitigation: Point it at a narrow API docs, OpenAPI, or examples folder and choose an intended report path. <br>
Risk: The generated report can influence API change decisions, but it is based on local input and review heuristics. <br>
Mitigation: Review the report against source contracts, examples, and release requirements before using it to guide API changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/api-contract-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Audit spec](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report or JSON payload, with optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local read-only audit helper; writes a report file only when the user supplies an output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
