## Description:

Automatically converts long-form content such as videos, blog posts, and podcasts into platform-specific short-form scripts, social posts, transcripts, summaries, and quote assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, podcasters, and agencies use this skill to repurpose one source asset into channel-ready content for TikTok, YouTube Shorts, Instagram Reels, Twitter/X, LinkedIn, and podcast workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted blog URL fetching can expose internal services or retrieve untrusted content.

Mitigation: Use only trusted blog URLs, review the skill before installing it in environments with internal network access, and prefer a patched version that validates URLs.

Risk: Batch processing can write output files to unsafe or unintended paths.

Mitigation: Use only trusted batch config files, constrain output directories away from important project files, and prefer a patched version that constrains output paths.

Risk: Source content may be sent to an external AI service when OPENAI_API_KEY is configured.

Mitigation: Avoid confidential input unless OpenAI processing is approved for that data.

Risk: Flagged dependencies may increase maintenance or security exposure.

Mitigation: Review and update the flagged dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/ai-content-repurposer)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact Quick Start](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON or console text containing platform-specific scripts, social posts, transcripts, summaries, quote cards, and batch outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use OPENAI_API_KEY for AI-powered transformations; without an API key, artifact behavior returns demo/template output.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
