## Description:

Douyin NLP Search helps agents parse Chinese natural-language Douyin video search requests and return formatted text or JSON sample results with keywords, counts, sort order, and video metadata.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to interpret Douyin-related Chinese search requests and produce structured sample search results for local testing or research-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample videos and engagement metrics could be mistaken for live Douyin search results.

Mitigation: Treat returned videos and metrics as sample data unless a reviewed real API or browser integration is added.

Risk: Future real scraping or browser automation could introduce platform terms, rate-limit, network-access, credential, or session-handling concerns.

Mitigation: Review any expansion against Douyin platform terms, rate limits, and credential-handling requirements before deployment.

Risk: Natural-language parsing may extract broad or inaccurate keywords, counts, or sort preferences.

Mitigation: Confirm parsed query fields before relying on results in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-nlp-search)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, guidance]

**Output Format:** [Formatted text or JSON search-result data with optional Python and shell usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns built-in sample results unless extended with a real API or browser automation integration.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
