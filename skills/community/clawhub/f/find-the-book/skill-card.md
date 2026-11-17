## Description:

Searches for books and returns Douban ratings, summaries, Douban links, and WeChat Reading links when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wintersun661](https://clawhub.ai/user/wintersun661)

### License/Terms of Use:


## Use Case:

Readers, researchers, and reading-focused agents use this skill to find books by title or topic and compare likely matches using Douban ratings, summaries, and available reading links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL checks are too loose and could allow fetching attacker-controlled or internal network URLs.

Mitigation: Run the skill in a restricted network sandbox and validate fetched URLs strictly against official book.douban.com and weread.qq.com hosts before requesting them.

Risk: Search and scraping behavior depends on external services and may return unavailable, stale, or incomplete links.

Mitigation: Treat returned ratings and reading links as best-effort results, handle request failures gracefully, and verify important links before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wintersun661/skills/find-the-book)
- [Douban Books](https://book.douban.com)
- [WeChat Reading](https://weread.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown book recommendations derived from structured search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to the requested count of book results with titles, ratings, summaries, Douban links, and optional WeChat Reading links.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
