## Description:

Configures ExDoc for Elixir projects including mix.exs setup, extras, groups, cheatsheets, and livebooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure ExDoc documentation generation for Elixir projects, including dependency setup, extras, module and document grouping, cheatsheets, Livebooks, and successful documentation builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ExDoc custom JavaScript, such as analytics or clipboard behavior, could conflict with a project's privacy or user-notice requirements.

Mitigation: Review custom head and body injections before installing or publishing the generated documentation.

Risk: Incorrect extras, asset paths, or dependency setup could make ExDoc builds fail or produce incomplete documentation.

Mitigation: Run mix deps.get, verify all referenced paths exist, and run mix docs before claiming the documentation configuration is complete.

## Reference(s):

- [Advanced Configuration](references/advanced-config.md)
- [Extras Formats](references/extras-formats.md)
- [Makeup syntax highlighting](https://hexdocs.pm/makeup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Elixir configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to verify dependency resolution, real extra paths, and generated documentation output before claiming success.]

## Skill Version(s):

1.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
