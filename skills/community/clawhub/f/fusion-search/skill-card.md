## Description:

Fusion Search routes Chinese and English web queries across multiple search engines using Playwright, then deduplicates, scores, and optionally fetches full page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjingxuan-ai](https://clawhub.ai/user/lvjingxuan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to perform multilingual web research, choose an appropriate search engine chain, and return ranked results with snippets or optional fetched page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth browsing and anti-detection behavior may have policy or site-terms implications.

Mitigation: Review allowed use for target search engines and sites before deployment, and restrict or disable the behavior where policy requires it.

Risk: Full-content fetching can visit arbitrary result URLs and may expose sensitive or internal queries.

Mitigation: Run the skill in a contained environment with restricted outbound network access, block private networks and metadata endpoints, and avoid sending secrets or internal queries.

Risk: The browser is launched with unsafe Chromium settings while fetching web pages.

Mitigation: Use container or sandbox isolation with minimal privileges and do not share browser state with trusted browsing sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjingxuan-ai/skills/fusion-search)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON array of search results or plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include title, url, snippet, content, engine, and score; full-content fetching is optional and limited by the implementation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter, metadata.json, and changelog show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
