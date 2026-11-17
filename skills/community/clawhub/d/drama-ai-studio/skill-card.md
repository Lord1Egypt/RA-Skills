## Description:

DramaAIStudio（AI影视工场） helps short-drama creators manage projects, upload and analyze scripts, extract and generate visual assets, build storyboards, generate storyboard videos, and monitor final asset or video changes through authenticated iDrama APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hobinson](https://clawhub.ai/user/hobinson)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and production teams use this skill to coordinate AI short-drama creation workflows, including project setup, script ingestion, asset extraction, image generation, storyboard generation, video generation, comments, and review loops. Agents can also propose OpenClaw Cron monitoring jobs that report changes in final asset candidates and selected storyboard videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist operating rules in agent memory.

Mitigation: Review memory changes before installation and keep the rules scoped to DramaAIStudio workflows.

Risk: The skill can store or reuse an iDrama token through environment variables, a local .env file, or command-line arguments.

Mitigation: Prefer host-managed secrets, avoid echoing full tokens, and only persist tokens after explicit user approval.

Risk: The skill can create recurring authenticated monitoring jobs.

Mitigation: Inspect every OpenClaw Cron command, schedule, destination, and embedded token reference before approving it.

Risk: The skill includes write-back and delete operations for scripts, assets, comments, storyboard shots, and selected videos.

Mitigation: Confirm user intent before mutating or deleting project content and verify the target project, episode, asset, shot, or task identifier.

Risk: The skill supports an API base URL setting used by its snapshot scripts.

Mitigation: Use only the official iDrama base URL unless an administrator has explicitly approved another endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hobinson/skills/drama-ai-studio)
- [iDrama service](https://idrama.lingban.cn/)
- [iDrama API token page](https://idrama.lingban.cn/api-token)
- [Skill source overview](artifact/SKILL.md)
- [Token API reference](artifact/references/ref-2-2-idrama-token.md)
- [Project management API reference](artifact/references/ref-4-1-get-openapi-drama-list.md)
- [Script upload API reference](artifact/references/ref-5-2-post-openapi-drama-play-id-scripts-upload.md)
- [Script analysis API reference](artifact/references/ref-5-5-post-openapi-drama-play-id-scripts-analyze.md)
- [Asset list API reference](artifact/references/ref-6-1-get-openapi-drama-play-id-assets-list.md)
- [Asset prompt helper API reference](artifact/references/ref-6-5-post-openapi-drama-play-id-assets-prompt-helper-generate.md)
- [Asset image generation API reference](artifact/references/ref-6-6-post-openapi-drama-play-id-assets-asset-type-asset-id-generate-image.md)
- [Storyboard analysis API reference](artifact/references/ref-7-2-post-openapi-drama-play-id-storyboard-episode-no-analyze.md)
- [Storyboard prompt optimization API reference](artifact/references/ref-7-5-post-openapi-drama-play-id-storyboard-episode-no-shots-shot-id-optimize-prompt.md)
- [Storyboard video task API reference](artifact/references/ref-8-1-post-openapi-drama-play-id-storyboard-video-episodes-episode-no-shots-shot-id-tasks.md)
- [Storyboard selected videos API reference](artifact/references/ref-8-4-get-openapi-drama-play-id-storyboard-video-episodes-episode-no-selected-videos.md)
- [Storyboard video comments API reference](artifact/references/ref-8-5-get-openapi-drama-play-id-storyboard-video-video-comments.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP API instructions, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated API requests, OpenClaw Cron command proposals, and local JSON snapshot files when users approve those workflows.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
