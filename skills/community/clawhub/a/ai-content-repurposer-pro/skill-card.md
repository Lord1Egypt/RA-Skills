## Description:

Automatically convert long-form videos, blogs, and podcasts into platform-optimized social media scripts, threads, summaries, and transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, agencies, and developers use this skill to turn transcripts, blog posts, and podcast text into reusable social content packages. It supports single-item and batch workflows for scripts, threads, LinkedIn posts, formatted transcripts, summaries, quotes, and related social copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary blog URLs, which may reach private networks or sensitive internal sites.

Mitigation: Review before installing in environments with private-network access and avoid processing untrusted URLs until URL validation is added.

Risk: Content sent for AI-powered transformations may be confidential, regulated, or proprietary.

Mitigation: Do not process sensitive content unless the user is comfortable sending it to OpenAI under the applicable account and data-handling terms.

Risk: Batch configuration and output paths are treated as trusted input.

Mitigation: Use trusted batch config files and restrict output directories until output-path containment is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/ai-content-repurposer-pro)
- [Artifact README](artifact/README.md)
- [Artifact Quickstart](artifact/QUICKSTART.md)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON content outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided content, file paths, or URLs; OpenAI-backed transformations use OPENAI_API_KEY and can fall back to demo/template output when unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
