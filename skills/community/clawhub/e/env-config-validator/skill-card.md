## Description: <br>
Validates .env files against schemas, compares environment files, detects common configuration mistakes, generates schemas, and reports results in text, JSON, or markdown with CI-friendly exit codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to audit environment configuration before deployment, enforce required variables and value types, compare environments, and generate reusable schema files for CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads explicitly selected .env files that may contain credentials or other sensitive values. <br>
Mitigation: Run it only against intended files and avoid sharing raw validation output from secret-bearing environments. <br>
Risk: Generated schemas and JSON diff reports can persist real example values from .env files. <br>
Mitigation: Review and redact generated schemas or reports before saving them to a repository, uploading them, or sending them to others. <br>


## Reference(s): <br>
- [Schema Format Reference](references/schema-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/env-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, markdown, and schema JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write validation reports or generated schemas to an output file; exits with 0 for no issues, 1 for warnings or environment differences, and 2 for errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
