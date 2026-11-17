## Description:

Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve CCTV News Broadcast highlights for a requested date and summarize the fetched titles and article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler follows links found in remote pages and may request destinations outside CCTV if those pages are manipulated.

Mitigation: Allowlist CCTV HTTPS domains and validate redirects before fetching detail pages.

Risk: The crawler sends a built-in cookie and performs outbound web requests without stated caps or timeouts.

Mitigation: Remove the hard-coded cookie, cap fetched links and response sizes, add request timeouts, and pin dependencies exactly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/cctv-news-fetcher-conflict)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [JSON from the crawler plus a Markdown summary for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a date in YYYYMMDD format; relative dates such as today or yesterday are resolved before execution.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
