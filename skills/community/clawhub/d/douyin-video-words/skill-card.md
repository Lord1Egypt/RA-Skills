## Description:

Extracts speech and useful copy from Douyin-style video links or local media, then uses a large language model to produce cleaned transcripts, summaries, rewrites, highlights, scene scripts, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, and agents use this skill to convert selected video or audio sources into reusable transcripts and content drafts. It is suited for short-video operations, meeting notes, course breakdowns, interview cleanup, highlights extraction, and prompt-directed rewrites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, video URLs, prompts, and task identifiers are sent to the GuaiKei service and its returned storage endpoint.

Mitigation: Install only if the provider is trusted; avoid confidential local videos, sensitive prompts, private URLs, and internal-network URLs unless the provider's retention and deletion promises are independently acceptable.

Risk: User-supplied URLs may be downloaded before upload, which can introduce untrusted remote media into the agent environment.

Mitigation: Restrict use to intended public media sources, review file size and source trust before execution, and avoid passing URLs that resolve to private infrastructure.

Risk: The security evidence marks the release as suspicious because network and download risks are under-disclosed.

Mitigation: Review the network behavior, token requirement, and provider terms before deployment; limit use to workflows where third-party media processing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-video-words)
- [Server-resolved source repository](https://github.com/why20261/douyin-video-words)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown returned on stdout, with progress and diagnostics on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts a media URL or local file path, a prior task ID, and an optional prompt; processes one media item per command.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
