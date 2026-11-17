## Description:

Summarize long-form content — articles, podcasts, research papers, PDFs, notes, and more — using the Dizest API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[s-annam](https://clawhub.ai/user/s-annam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize URLs, long-form documents, podcasts, PDFs, reports, notes, transcripts, or pasted text through the Dizest API. It supports optional focus instructions and output language selection for structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided content is sent to Dizest's external API for summarization.

Mitigation: Use the skill only for material approved for external processing, and avoid secrets, credentials, private keys, regulated personal data, and confidential documents unless the organization has approved that use.

Risk: The artifact README includes an HTTP API-key link.

Mitigation: Use the HTTPS API-key page, https://dizest.ai/api/keys, when obtaining or managing API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/s-annam/skills/dizest-summarize)
- [Dizest website](https://www.dizest.ai)
- [Dizest API keys](https://dizest.ai/api/keys)
- [Dizest App Store listing](https://apps.apple.com/app/id6752311120)
- [Dizest Google Play listing](https://play.google.com/store/apps/details?id=com.ideas116.dizest)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell configuration commands, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIZEST_API_KEY and sends user-provided content to Dizest's external API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
