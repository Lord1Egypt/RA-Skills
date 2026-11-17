## Description:

Trigger a one-shot workflow that clones or pulls a Git repository, generates a structured wiki from it using the CodeWiki CLI, and optionally renders the result into static MkDocs or VitePress sites with an HTTP preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangsier-xyz](https://clawhub.ai/user/jiangsier-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent to document a target code repository by generating a Markdown wiki and, when requested, static documentation sites for local review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone or pull user-selected repositories and write generated output into local directories.

Mitigation: Confirm the repository URL and output directory before execution, and avoid running destructive overwrite options on important folders.

Risk: Rendering can install dependencies from external package registries and depends on the external CodeWiki CLI.

Mitigation: Install the skill only when the CodeWiki CLI and runtime package registries are trusted in the execution environment.

Risk: The optional preview mode starts foreground localhost servers.

Mitigation: Use preview serving only when a local HTTP process is expected and stop it when review is complete.

## Reference(s):

- [CodeWiki upstream project](https://github.com/FSoft-AI4Code/CodeWiki)
- [Code Wiki on ClawHub](https://clawhub.ai/jiangsier-xyz/skills/codewiki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command previews and generated repository documentation files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a Markdown wiki under the selected output directory and optional MkDocs or VitePress static site files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
