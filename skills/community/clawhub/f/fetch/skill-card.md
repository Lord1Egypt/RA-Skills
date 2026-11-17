## Description:

Fetch is a public web retrieval and clean extraction skill for fetching public URLs, extracting title, text, and links, saving raw and cleaned output locally, and keeping job history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve public web pages, extract readable text and links, save raw and cleaned results locally, and inspect prior fetch jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised public-only boundary is not fully enforced by URL validation, so a provided URL or redirect could cause the agent host to fetch localhost, private-network, or cloud metadata addresses.

Mitigation: Use only clearly public HTTP/HTTPS pages and require strict public-destination plus redirect validation before treating the skill as a low-risk fetch utility.

## Reference(s):

- [Fetch Philosophy](references/philosophy.md)
- [Fetch on ClawHub](https://clawhub.ai/agistack/skills/fetch)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text command output, local raw HTML and cleaned text files, JSON job metadata, and Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetched data is stored locally under the OpenClaw workspace memory path; no credentials, browser automation, cloud sync, or external uploads are described.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
