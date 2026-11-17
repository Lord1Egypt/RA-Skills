## Description:

Extracts YouTube video transcripts for video analysis, content ideas, and blog posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and developers use this skill to extract YouTube transcripts, review video metadata, identify key points, and turn video content into blog posts, FAQs, quotes, or keyword research inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a YouTube API key and send YouTube video identifiers or URLs to YouTube-related services.

Mitigation: Use only in environments where sharing those identifiers with YouTube-related services is acceptable, and store the API key in environment configuration rather than in prompts or shared files.

Risk: The optional Python workflow installs an unpinned package.

Mitigation: Prefer an isolated environment and pin package versions before using the optional package-based workflow.

Risk: The documented fallback commands default transcript extraction to German.

Mitigation: Specify the transcript language explicitly when German is not the intended language.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with transcript excerpts, video metadata, key points, and content ideas; may include shell commands for optional extraction workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube video ID or URL; the documented default transcript language is German.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
