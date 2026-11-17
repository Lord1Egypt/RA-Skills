## Description:

AI fullstack project scaffold turns a natural-language project request into a runnable project structure with code framework, Makefile, task tracking, and Docker deployment configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to initialize or extend fullstack projects from a short requirements description. It coordinates planning, code generation, Makefile generation, and Docker configuration for Node.js, Python, Go, and Java stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes many local project files, including source code, Makefile, Dockerfile, docker-compose.yml, and configuration files.

Mitigation: Run it in a new or clean directory when possible and review generated files before running commands or committing changes.

Risk: Generated source, build files, and Docker configuration may not match production security or business requirements.

Mitigation: Review generated code and deployment configuration, then adjust and scan them before production use.

Risk: Existing-project mode may create conflicts or overwrite expectations because conflict handling is not clearly documented.

Mitigation: Use version control or a backup before running against an existing project and inspect the resulting diff before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-fullstack-project-scaffold)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration]

**Output Format:** [Project files and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a project directory that may include source code, Makefile, Dockerfile, docker-compose.yml, .dockerignore, README.md, package or dependency files, and task planning documents.]

## Skill Version(s):

1.0.0 (source: frontmatter and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
