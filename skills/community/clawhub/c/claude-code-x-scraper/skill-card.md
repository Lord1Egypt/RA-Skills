## Description:

Extracts and analyzes X/Twitter data by fetching user timelines, searching recent posts, retrieving tweet details, and supporting social media research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lamtest556-blip](https://clawhub.ai/user/lamtest556-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media researchers use this skill to collect public X/Twitter posts, user timeline data, and recent search results for monitoring, trend analysis, and downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill can request and automatically use sensitive X account credentials broader than necessary.

Mitigation: Prefer a limited X API bearer token, keep credentials outside root-owned browser profiles, and avoid providing a full browser cookie jar unless authenticated scraping is intentional.

Risk: Browser-based scraping may reuse authenticated cookies and blend skill activity with a normal logged-in session.

Mitigation: Run browser scraping in an isolated environment with dedicated credentials or cookies and review any cookie file before use.

Risk: X API access limits and account permissions can cause incomplete results, authorization failures, or rate-limit errors.

Mitigation: Use the minimum requested result count, confirm the account has the needed X API access level, and handle 401, 403, and 429 responses before relying on results.

## Reference(s):

- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [X API v2 Reference](references/x_api_limits.md)
- [ClawHub Skill Page](https://clawhub.ai/lamtest556-blip/skills/claude-code-x-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON tweet, user, search, and metadata payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include post text, account metadata, timestamps, public metrics, query metadata, error messages, and rate-limit or access-level guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
