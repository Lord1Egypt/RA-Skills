## Description:

Search Bilibili videos by keyword, sorted by relevance, newest, or most played, and return titles, uploader details, engagement metrics, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find Bilibili reviews, tutorials, and other videos about a topic or product. The skill returns searchable video details and supports relevance, newest, and popularity sorting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx command runs an unpinned package, and the security scan was partial.

Mitigation: Review the command and install a specific dataxapi CLI version from a trusted source before use; treat the benign scan verdict as limited by the partial scan.

Risk: Search calls and additional result pages incur charges.

Mitigation: Use the per-call price cap and fetch only the pages needed; tell the user the total cost before making multiple calls.

## Reference(s):

- [Bilibili video search API documentation](https://dataxapi.com/apis/bilibili/videos/search/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [ClawHub skill page](https://clawhub.ai/data-x-api/skills/dataxapi-bilibili-video-search)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Markdown or plain text with video titles, uploader details, engagement metrics, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns one page of up to 20 results; additional pages incur additional per-call charges. Returned video content is third-party text.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
