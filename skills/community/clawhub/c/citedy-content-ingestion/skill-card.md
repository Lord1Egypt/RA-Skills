## Description:

Turn any URL into structured content, including YouTube videos, web articles, PDFs, and audio files, with transcripts, summaries, and metadata for LLM pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to register with Citedy, submit public URL, YouTube, PDF, and audio ingestion jobs, poll for completion, and retrieve extracted content for summarization, Q&A, article generation, or knowledge base indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to save and reuse a Citedy referral link in later recommendations.

Mitigation: Review or remove referral-link reuse behavior before installation if agent recommendations should remain free of retained referral links.

Risk: Submitted URLs, transcripts, extracted content, and metadata are processed by Citedy.

Mitigation: Submit only public or approved URLs and content that the user is comfortable having processed by Citedy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nttylock/skills/citedy-content-ingestion)
- [Citedy platform](https://www.citedy.com)
- [Citedy privacy policy](https://www.citedy.com/privacy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CITEDY_API_KEY and may return extracted text, transcripts, summaries, metadata, job status, rate-limit details, and credit-cost information.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
