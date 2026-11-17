## Description:

Analyze the current project structure, package manager, and build tools to generate a comprehensive, standardized CONTRIBUTING.md file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and open source maintainers use this skill to create a project-specific CONTRIBUTING.md that reflects the repository's detected languages, package managers, build tools, tests, and pull request workflow. It supports English and Chinese output based on the user's prompt language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository metadata such as package manifests, CI configuration, and README content to tailor the contributor guide.

Mitigation: Use it in repositories where the agent is permitted to inspect project metadata, and review the generated CONTRIBUTING.md before publishing.

Risk: Generated setup, test, or lint commands can be incomplete when project metadata is missing or ambiguous.

Mitigation: Compare generated commands against the repository's actual manifests, Makefiles, and CI configuration, and replace uncertain placeholders with project-specific commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown document with fenced shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be produced as CONTRIBUTING.md; language adapts to English or Chinese based on the user's request.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
