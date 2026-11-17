## Description:

OpenClaw skill for source-backed web search, page reading, and evidence-aware claim checking that helps verify factual answers with live search results and explicit source handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run live web searches, read source pages, verify factual claims, and prepare citation-ready evidence summaries for answers that need current or source-backed support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned package version can change reviewed behavior over time.

Mitigation: Install in an isolated virtual environment as a non-privileged user and pin cross-validated-search==16.0.0 before use.

Risk: Search queries and page-fetch requests are sent to configured search providers during normal operation.

Mitigation: Avoid sensitive queries unless the provider path is approved, and consider a self-hosted SearXNG configuration for more control.

Risk: Claim verification is heuristic and may surface conflicting evidence without resolving it.

Mitigation: Review the cited source URLs and any conflicts before relying on or publishing conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wd041216-bit/skills/cross-validated-search)
- [Project Homepage](https://github.com/wd041216-bit/cross-validated-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text, Markdown, and JSON from command-line verification workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include support and conflict scores, page-aware verification status, source URLs, and recommended next steps.]

## Skill Version(s):

16.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
