## Description:

Maintains cross-episode story, character, and visual consistency for AI manga or anime-drama production pipelines generated one episode at a time from uploaded TXT files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsinbupt](https://clawhub.ai/user/jsinbupt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production teams use this skill to convert prior episode summaries and current episode TXT files into compact continuity packs, visual anchors, and prompt notes for text, image, and video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Episode text and prior summaries may contain sensitive story or production details.

Mitigation: Provide only episode material you are comfortable sharing with the agent and review continuity summaries before reuse.

Risk: Missing prior episode summaries can reduce continuity quality for episode 2 and later.

Mitigation: Supply the previous episode inheritance summary when available; otherwise clearly mark the continuity risk in the generated context.

## Reference(s):

- [Episode Context Schema](references/episode-context-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Chinese Markdown templates and concise prompt-anchor notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese output; no executable code, credential use, persistence, or hidden data handling was found in security evidence.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
