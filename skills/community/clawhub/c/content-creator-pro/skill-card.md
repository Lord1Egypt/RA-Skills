## Description:

Content Creator Pro helps agents draft platform-native posts, threads, newsletters, long-form articles, and short-form video scripts while maintaining brand voice, queuing content, and tracking performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external ClawHub users can use this skill when an agent needs to create, queue, and refine marketing or social content across Twitter/X, LinkedIn, Reddit, Substack, and short-form video. It is also intended to maintain local brand voice, calendar, hook, performance, learning, error, and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated posts may contain inaccurate, misleading, off-brand, or unsuitable marketing claims.

Mitigation: Review generated content before publication, especially before allowing a connected publishing skill to post publicly.

Risk: The skill writes voice, performance, hook, queue, library, learning, error, and audit records in the workspace.

Mitigation: Confirm the workspace paths are appropriate for the agent environment and define retention rules for generated content and logs.

Risk: Queued drafts may be published by another skill after handoff.

Mitigation: Keep a human or policy review step between queued content and any automated publishing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/content-creator-pro)
- [Publisher profile](https://clawhub.ai/user/georges91560)
- [README.md](artifact/README.md)
- [human_writing.md](artifact/human_writing.md)
- [voice.md](artifact/voice.md)
- [hooks.md](artifact/hooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, platform-native text drafts, JSON queue and performance records, and optional Python CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated content and tracking records to local workspace paths; no network access is indicated by the server security evidence.]

## Skill Version(s):

1.0.7 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
