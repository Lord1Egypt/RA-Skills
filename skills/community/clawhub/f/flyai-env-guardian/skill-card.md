## Description: <br>
Protect sensitive environment variables from accidental exposure in commits, logs, and CI pipelines with automated scanning and pre-commit validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan repositories, staged changes, environment files, and CI/CD workflows for exposed secrets before code reaches version control or deployment pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may need to read source files, staged changes, environment files, and possibly git history to find exposed secrets. <br>
Mitigation: Use it only in repositories where that access is acceptable and review the scope of files or history before allowing broad scans. <br>
Risk: Scan results may reveal real secret values, secret names, or precise file locations. <br>
Mitigation: Treat findings as sensitive, avoid sharing raw output unnecessarily, and rotate any credential that may have been exposed. <br>
Risk: Suggested .gitignore edits, .env.example generation, pre-commit hooks, or CI/CD changes could affect repository workflows. <br>
Mitigation: Review proposed file and configuration changes before applying them, then test the affected commit or pipeline path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/flyai-env-guardian) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with findings, remediation guidance, and inline shell commands or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May identify file paths, line locations, environment variable names, and suggested .gitignore, .env.example, pre-commit, or CI/CD changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
