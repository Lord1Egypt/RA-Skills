## Description:

Searches public Douyin content, retrieves creator post lists, fetches video comments, and queries real-time trending topics for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to gather public Douyin search results, creator posts, comments, and hot-list data for internal content planning, marketing research, competitor analysis, and public-comment review. It is not intended for posting, editing, watermark removal, private data access, or non-Douyin platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict with review-worthy API-token handling and contradictory contact or promotional authentication behavior.

Mitigation: Review before installing and use a dedicated, revocable GUAIKEI_API_TOKEN for this skill.

Risk: Douyin queries and URLs are expected to be sent to www.guaikei.com.

Mitigation: Use only public or approved research inputs and avoid sending sensitive, private, or regulated information.

Risk: Result logs are expected to be saved locally and may contain queried URLs, public content data, or operational context.

Mitigation: Avoid shared machines or repositories for generated logs, protect log storage, and rotate the token if it may have appeared in URL logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/douyin-public-data-fetcher-guaikei)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [User Documentation](readme.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with stderr logs and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; successful CLI runs write JSON logs locally.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
