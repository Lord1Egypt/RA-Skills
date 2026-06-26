## Description: <br>
Generate and manage test data fixtures using CLI templates. Use when creating seed data, mock records, or reproducible test datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, load, seed, validate, export, and reset reproducible local test fixture data for application tests and development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported fixture files are persisted locally under ~/.fixture/. <br>
Mitigation: Review input files before importing them and treat stored fixture data as persistent local development data. <br>
Risk: Import and export commands read from and write to user-provided paths. <br>
Mitigation: Check file paths before running load, import, dump, or export commands. <br>
Risk: The reset command can clear stored fixture records. <br>
Mitigation: Use reset --confirm only when intentionally clearing fixture data. <br>


## Reference(s): <br>
- [Fixture on ClawHub](https://clawhub.ai/xueyetianya/fixture) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell script writes fixture records and templates under ~/.fixture/ and can import or export JSON, JSONL, CSV, and SQL fixture data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
