## Description: <br>
Turn URLs, YouTube videos, web articles, PDFs, and audio files into structured content, transcripts, summaries, and metadata for LLM pipelines using Citedy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nttylock](https://clawhub.ai/user/nttylock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to register a Citedy-enabled agent and ingest supported public URLs into structured content for summarization, Q&A, article generation, or knowledge base indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citedy API keys can authorize ingestion requests if exposed. <br>
Mitigation: Store CITEDY_API_KEY in a secret manager or environment variable, avoid pasting it into chat, and revoke compromised keys from the Citedy dashboard. <br>
Risk: Target URLs and extracted content are sent to Citedy for processing. <br>
Mitigation: Use the skill only for content you are allowed to send to Citedy, and avoid private, tokenized, confidential, proprietary, login-gated, or paywalled links unless the privacy terms have been reviewed. <br>
Risk: Ingestion can consume Citedy credits and is subject to content-size and rate limits. <br>
Mitigation: Show expected credit cost before ingestion, prefer cache hits when available, and respect the documented batch size, duration, file-size, and rate limits. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nttylock/citedy-content-ingestion) <br>
- [Citedy platform](https://www.citedy.com) <br>
- [Citedy privacy policy](https://www.citedy.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with HTTP and curl examples plus JSON API request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CITEDY_API_KEY and sends target URLs and extracted content to Citedy API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
