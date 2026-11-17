## Description:

Fang audits skill scripts for environment-variable theft with a local static scanner and optional OpenAI-compatible LLM analysis, then reports risk ratings and recommended actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use Fang to audit installed or downloaded skill directories for suspicious environment-variable access, outbound network behavior, encoding, and execution patterns before running those skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM mode can upload source-code excerpts and file paths from the target directory to a configured remote provider.

Mitigation: Use the local static scan by default and enable LLM mode only for directories whose contents may be shared with the selected provider.

Risk: A custom OpenAI-compatible base URL receives the supplied bearer key when LLM analysis is enabled.

Mitigation: Use custom base URLs only for endpoints that are trusted to handle the API key and submitted source excerpts.

Risk: Broad or symlinked scan targets may include more files than intended during remote analysis.

Mitigation: Inspect target directories and symlinks before enabling LLM mode, and prefer scanning one skill directory at a time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/fang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown threat report with command examples and optional raw JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static scanning runs locally; optional LLM mode sends script excerpts and paths to the configured OpenAI-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
