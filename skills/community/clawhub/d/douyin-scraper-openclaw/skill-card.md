## Description:

Douyin Scraper helps an agent search Douyin videos from natural-language requests using browser automation and return result details such as titles, authors, engagement metrics, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to issue natural-language Douyin search requests and have an agent open Douyin, submit the query, and summarize video search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language activation can trigger automated Douyin browser actions unexpectedly.

Mitigation: Use explicit Douyin-specific invocation phrases, review the planned browser action before execution, and keep the browser dependency pinned or locally controlled.

Risk: Saved browser state can expose a Douyin login session if douyin-auth.json is shared or stored carelessly.

Mitigation: Store authentication state locally only when needed, do not share the state file, and remove it when the workflow no longer requires a logged-in session.

Risk: Search terms are sent to Douyin and the workflow may encounter login, captcha, rate-limit, or platform-policy constraints.

Mitigation: Avoid sensitive searches, follow Douyin platform terms, and stop automation when Douyin presents access-control or anti-abuse challenges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-openclaw)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [Douyin search](https://www.douyin.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text search summaries with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation steps, extracted search result summaries, and local screenshot/state file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
