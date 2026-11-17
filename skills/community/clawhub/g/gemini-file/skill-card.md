## Description:

Gemini CLI for one-shot Q&A, summaries, and generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenbaiyujason](https://clawhub.ai/user/chenbaiyujason)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to invoke the local Gemini CLI for one-shot Q&A, summarization, generation, and larger outputs that need to be saved as files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can write generated content to local files, including custom output directories.

Mitigation: Constrain output to a skill-owned directory where possible and review requested output paths before execution.

Risk: The --gemini-bin option can select an arbitrary executable instead of the expected Gemini CLI.

Mitigation: Treat executable selection as a developer-only option and use the default gemini binary unless the path is explicitly trusted.

Risk: Sensitive prompts or generated content may be persisted on disk by file-output mode.

Mitigation: Avoid sensitive inputs unless local storage is acceptable, and remove generated files according to the user's data-handling requirements.

## Reference(s):

- [Gemini API and developer documentation](https://ai.google.dev/)
- [ClawHub skill page](https://clawhub.ai/chenbaiyujason/skills/gemini-file)
- [ClawHub publisher profile](https://clawhub.ai/user/chenbaiyujason)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; file-output mode returns JSON containing an absolute file path and optional generated content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Gemini CLI installation and authentication. File-output mode writes generated content to disk.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
