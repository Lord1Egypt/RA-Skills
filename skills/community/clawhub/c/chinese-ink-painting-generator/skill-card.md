## Description:

Generate traditional Chinese ink paintings and sumi-e brushwork art from text prompts via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese ink painting-style images from short text descriptions, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference image IDs, and the Neta API token are sent to the TalesOfAI/Neta service.

Mitigation: Use only non-sensitive prompts and reference IDs, and install only if the external service is acceptable for the intended use.

Risk: The token is supplied through a command-line flag, which can expose it through shell history, logs, or process monitoring.

Mitigation: Prefer expanding the token from a protected environment variable, avoid pasting real tokens into reusable commands, and rotate the token if exposure is suspected.

Risk: Install examples use mutable package sources.

Mitigation: Prefer a pinned or otherwise verified install source before using the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/chinese-ink-painting-generator)
- [Neta API access page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts prompt text, image size, and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
