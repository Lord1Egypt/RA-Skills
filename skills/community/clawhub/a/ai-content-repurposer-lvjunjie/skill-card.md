## Description:

Convert long-form content like videos, blogs, and podcasts into optimized short scripts, threads, posts, transcripts, and summaries for multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, podcasters, agencies, and developers use this skill to repurpose long-form source material into platform-ready social scripts, posts, transcripts, summaries, quotes, and batch-generated content assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processed content may be sent to OpenAI for transformation.

Mitigation: Do not process confidential or regulated content without approval, and use approved API keys and accounts.

Risk: Blog URL fetching can request private or internal URLs.

Mitigation: Fetch only trusted public URLs, or prefer an updated version that blocks private and internal URLs, validates redirects, and limits response size.

Risk: Batch configurations can write output outside the intended folder through job names.

Mitigation: Run only trusted batch configs, sanitize job names before use, or prefer an updated version that constrains writes to the selected output directory.

Risk: The security evidence flags review-worthy weaknesses and recommends dependency updates.

Mitigation: Review the skill before deployment and prefer a release that addresses the security guidance from the server scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/ai-content-repurposer-lvjunjie)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact quick start](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [JSON files or console text containing scripts, threads, posts, formatted transcripts, summaries, quotes, and social post ideas.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on supplied content, optional batch configuration, OpenAI API availability, and documented input truncation around 10,000 characters per transformation.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
