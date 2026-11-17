## Description:

Lint, validate, and audit .dockerignore files for syntax issues, security risks, missing patterns, and optimization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to check .dockerignore files, audit whether sensitive files are excluded, generate project-specific ignore patterns, and inspect Docker build context size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The context analyzer can list file paths and sizes from a selected directory.

Mitigation: Run it only on repositories whose filenames can be shared, and avoid sharing context reports from sensitive workspaces.

Risk: Ignore-pattern recommendations can change which files are included in Docker build context.

Mitigation: Review generated .dockerignore changes before applying them to production builds.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance with optional JSON linter output and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report local file paths and file sizes when analyzing Docker build context.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
