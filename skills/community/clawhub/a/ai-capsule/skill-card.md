## Description:

AI Capsule scores and ranks AI news articles against a user's role, interests, and purpose, then produces personalized daily digests or single-article evaluations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webpudge](https://clawhub.ai/user/webpudge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, product managers, founders, and other AI practitioners use this skill to prioritize AI news by personal relevance. It can score pasted article text, URLs, JSON batches, or a daily feed and return ranked recommendations with reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The X/Twitter source can read local Chrome x.com cookies and pass session-derived values to a twitter-cli subprocess.

Mitigation: Disable or remove X/Twitter sources unless browser-cookie access is acceptable, and run the skill from a browser profile and environment intended for this use.

Risk: The security summary says inherited environment secrets are handled too broadly during X/Twitter fetching.

Mitigation: Run setup and daily fetches with a minimal agent environment, avoid exposing unrelated API keys, and review source configuration before enabling X/Twitter collection.

Risk: Daily operation writes reports, history, and deduplication state to a local data directory.

Mitigation: Use a dedicated data directory, review retained reports for sensitive content, and clear history or dedup files when retention is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webpudge/skills/ai-capsule)
- [AI Capsule homepage](https://github.com/WebPudge/ai-capsule)
- [README](artifact/README.md)
- [Daily mode workflow](artifact/sections/daily-mode.md)
- [Scoring framework](artifact/sections/scoring.md)
- [Output format](artifact/sections/output-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest cards with a leading score_json block for scored articles and inline shell or YAML snippets for setup and configuration tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily mode writes reports, history, deduplication state, and temporary pending items to the configured local data directory.]

## Skill Version(s):

1.0.5 (source: server release metadata, skill frontmatter, and changelog released 2026-06-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
