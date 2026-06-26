## Description: <br>
Lint, validate, and audit .dockerignore files for syntax issues, security risks, missing patterns, and optimization opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to lint .dockerignore files, audit whether sensitive files are excluded, suggest missing patterns, and analyze Docker build context contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Build context analysis can enumerate local project file names and sizes. <br>
Mitigation: Run context analysis only on the project directory intended for inspection and avoid sharing generated reports if file names are sensitive. <br>
Risk: Marketplace capability tags mention wallet credentials and sensitive credentials even though the scanner says this tool does not need them. <br>
Mitigation: Do not provide wallet credentials, API keys, or secrets when using this skill. <br>


## Reference(s): <br>
- [Dockerignore Linter on ClawHub](https://clawhub.ai/charlie-morrison/dockerignore-linter) <br>
- [charlie-morrison ClawHub profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 indicates no issues and exit code 1 indicates issues found.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
