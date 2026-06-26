## Description: <br>
Scan codebase for environment variables, generate .env.example, validate .env, and ensure .gitignore safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fratua](https://clawhub.ai/user/Fratua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit environment-variable usage, produce safe example configuration files, validate existing .env files, and check repository ignore rules before sharing or deploying a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Environment audits can expose secret names or accidentally include secret values in generated reports or files. <br>
Mitigation: Limit outputs to variable names, categories, and status; review generated .env.example or starter .env content before accepting it. <br>
Risk: Suggested .gitignore changes or git-history cleanup actions can affect repository workflow. <br>
Mitigation: Review ignore-file edits before applying them and treat git-history cleanup as a manual, coordinated maintenance task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fratua/env-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, environment-file snippets, validation tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose .env.example, starter .env, and .gitignore edits; outputs should list variable names and status, not secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
