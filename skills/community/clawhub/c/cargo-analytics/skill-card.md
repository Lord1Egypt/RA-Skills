## Description: <br>
Download workflow run results, export segment data, and monitor run metrics using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Cargo workspace users use this skill to inspect workflow run metrics, monitor errors, download run or batch results, and export segment data from Cargo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cargo analytics and export commands can expose sensitive workspace data, credentials, downloaded files, and signed URLs. <br>
Mitigation: Install only for authorized Cargo users, verify the active Cargo session before use, and scope exports with workflow, date, status, model, and batch filters. <br>
Risk: The documented failed-record re-run flow can execute workflows and create real workspace side effects. <br>
Mitigation: Require explicit user approval before creating a new batch for failed records, and confirm that the underlying issue has been fixed before re-running records. <br>


## Reference(s): <br>
- [Cargo skills repository](https://github.com/getcargohq/cargo-skills) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Run analytics examples](references/examples/run-analytics.md) <br>
- [Data export examples](references/examples/exports.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with Cargo CLI command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of CSV or JSON exports and signed download URLs; exported workspace data should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
