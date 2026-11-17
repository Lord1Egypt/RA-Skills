## Description:

Scan codebase for environment variables, generate .env.example, validate .env, and ensure .gitignore safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fratua](https://clawhub.ai/user/fratua)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit project environment variables, generate environment examples, validate current environment files, and check safeguards against accidentally committed secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect secret-bearing environment files and git history.

Mitigation: Require the agent to read only variable names, never print secret values, and avoid production .env files unless explicitly approved.

Risk: The skill may create or edit .env, .env.example, or .gitignore files.

Mitigation: Confirm proposed file changes before writing them and run the agent without elevated access.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and environment-file snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create .env.example, starter .env, and .gitignore changes when approved.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
