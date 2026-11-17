## Description:

Turns selected AI conversation history into podcast-style Markdown drafts, asks for user review, and can publish approved content to a Halo blog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert selected OpenClaw chat sessions into polished podcast-style blog articles and publish them to Halo after review. It is intended for content-management workflows that require drafting, preview, optional image generation, and publication metadata updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad historical OpenClaw session logs while searching for conversation material.

Mitigation: Use it only on explicitly selected current-session or narrowly scoped conversation content, and avoid shared-agent environments.

Risk: The skill can publish AI-derived content to a public Halo blog.

Mitigation: Review the full preview, generated images, tags, visibility, and AI-generated-content annotations before approving publication.

Risk: Runtime Markdown conversion may use npm resolution for the converter.

Mitigation: Pin or preinstall the Markdown converter and Halo CLI before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-shen1121/skills/chat-to-podcast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles with optional shell commands and Halo publication metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate article body content, image prompts, Halo publish commands, visibility updates, AI-generated-content annotations, and a local podcast counter update.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
