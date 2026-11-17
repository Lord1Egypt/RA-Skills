## Description:

Public API usage for the Clawdgle markdown-first search engine, including search, markdown fetch, URL ingest, and donation-link workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubybrewsday](https://clawhub.ai/user/rubybrewsday)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to call Clawdgle public endpoints for searching indexed markdown content, retrieving stored markdown for a URL, requesting indexing of public URLs, and opening the donation route.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, document fetches, ingest requests, and donation-link checks send requests to clawdgle.com.

Mitigation: Review outbound requests before use and avoid sending sensitive query strings, URLs, contact details, or reasons unless needed.

Risk: Ingest requests can submit URLs for indexing by the public service.

Mitigation: Use ingest only for public URLs intended for indexing and avoid repeated or spam-like submissions.

## Reference(s):

- [Clawdgle service](https://clawdgle.com)
- [Clawdgle Skill on ClawHub](https://clawhub.ai/rubybrewsday/skills/clawdgle)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown with inline HTTP endpoints and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents may produce URL-encoded request examples for public Clawdgle endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
