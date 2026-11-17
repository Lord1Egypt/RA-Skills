## Description:

Generates new song lyrics and Suno-ready music outputs by analyzing a reference song or artist style, writing structurally similar lyrics for a new theme, and submitting them to KIE/Suno for audio generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-hou-pe](https://clawhub.ai/user/jason-hou-pe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to transform a reference song or artist plus a new theme into structured lyrics, Suno style tags, and generated audio links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically submit prompts and lyrics to KIE/Suno using the user's API key, which may expose creative content and incur API costs.

Mitigation: Use only after reviewing the generated prompt and lyrics, confirming consent to send content externally, and selecting an API key intended for this workflow.

Risk: Lyrics may be handled in a local plaintext temporary file during generation.

Mitigation: Avoid sensitive lyrics or update the workflow to use a private per-run temporary file or stdin before production use.

Risk: The callback URL behavior is underdisclosed.

Mitigation: Review, remove, or clearly disclose the callback destination before running the generator.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-hou-pe/skills/ai-songwriter-clone)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-style final response with generated song links, cleaned lyrics, a highlighted lyric line, and a style summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIE_API_KEY or SUNO_API_KEY and may handle lyrics through a local plaintext temporary file during generation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
