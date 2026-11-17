## Description:

Generates a concise AGENTS.md project guide for coding agents, including project overview, quick start, architecture, coding standards, local validation, and documentation navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linuxcer](https://clawhub.ai/user/linuxcer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to create or update repository-facing AI guidance so an agent can understand the project, follow local standards, and verify changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently replace an existing CLAUDE.md file with a symlink.

Mitigation: Before running it, check whether CLAUDE.md already exists and require the agent to preserve it instead of using ln -sf or replacing it automatically.

Risk: The skill changes more files than its headline AGENTS.md output suggests.

Mitigation: Review the planned changes to AGENTS.md, docs/CODING_STYLE.md, docs/ARCHITECTURE.md, and CLAUDE.md before accepting generated edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linuxcer/skills/agentsmd-creator)
- [Community standards reference](references/community-standards.md)
- [Programming principles reference](references/principles.md)
- [Programming principles examples](references/examples.md)
- [AGENTS.md template](references/template.md)
- [Effective Go](https://go.dev/doc/effective_go)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [Alibaba Java Coding Guidelines](https://github.com/alibaba/p3c)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Microsoft .NET Naming Conventions](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with inline shell commands and documentation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets AGENTS.md at 200 lines or fewer and may also update docs/CODING_STYLE.md, docs/ARCHITECTURE.md, and CLAUDE.md compatibility.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
