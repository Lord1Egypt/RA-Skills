## Description: <br>
Creates robust, production-grade agent skills from natural language requests, handling design, error management, and code scaffolding for immediate use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acrid-auto](https://clawhub.ai/user/acrid-auto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn natural-language requests into ready-to-use agent skills with documentation, validation rules, error handling, and optional helper code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite generated skill files in a workspace. <br>
Mitigation: Review the target path and the planned file changes before accepting generated output. <br>
Risk: Generated skills may include Bash steps, external API calls, credentials, dependencies, or helper scripts. <br>
Mitigation: Review generated steps and scan files before deployment, especially where secrets, network calls, dependencies, or executable scripts are involved. <br>
Risk: Generated skill instructions could contain incorrect or misleading operational guidance. <br>
Mitigation: Validate generated skills against the documented quality gates and test expected success and error paths before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/acrid-auto/acrid-skill-creator) <br>
- [Publisher profile](https://clawhub.ai/user/acrid-auto) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Stock checker example](examples/stock-checker/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill and README files, optional code or configuration files, and concise delivery guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files and suggested commands should be reviewed before use, especially when they involve external APIs, credentials, dependencies, or target-path writes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
