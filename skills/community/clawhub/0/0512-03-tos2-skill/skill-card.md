## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run the summarize CLI for concise summaries of webpages, local documents and media, and YouTube links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected content may be sent to configured model providers or optional extraction services.

Mitigation: Use only approved provider keys and avoid confidential local files, private URLs, or sensitive media unless that data sharing is authorized.

Risk: The skill depends on an external summarization CLI and optional fallback services.

Mitigation: Install the CLI from the documented source, review enabled fallback services, and disable optional services that are not approved for the use case.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0512-03-tos2-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe CLI flags, provider API keys, optional extraction services, and generated summary output modes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
