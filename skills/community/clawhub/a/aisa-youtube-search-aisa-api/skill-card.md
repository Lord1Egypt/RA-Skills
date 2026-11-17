## Description:

Search YouTube videos, channels, and playlists through the AIsa YouTube relay with one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover YouTube videos, channels, and playlists through AIsa's relay API with query, locale, and pagination filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search terms and filters are sent to the external AIsa API.

Mitigation: Avoid sensitive search terms, private project names, and personal data in queries.

Risk: The skill requires an AISA_API_KEY for API calls.

Mitigation: Use a dedicated, rotatable API key and keep it out of prompts, logs, and shared files.

## Reference(s):

- [AIsa homepage](https://aisa.one)
- [AIsa YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search)
- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/aisa-youtube-search-aisa-api)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends YouTube search queries and filters to api.aisa.one.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
