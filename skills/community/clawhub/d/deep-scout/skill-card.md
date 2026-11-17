## Description:

Multi-stage deep intelligence pipeline (Search → Filter → Fetch → Synthesize). Turns a query into a structured research report with full source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use Deep Scout to turn a research question into a cited Markdown report, comparison, bullet summary, or timeline assembled from searched, filtered, and fetched web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send research queries and fetched page content through search, fetch, browser, Firecrawl, and LLM tooling.

Mitigation: Use it only with approved network egress and avoid sensitive internal URLs or confidential research topics unless the runtime enforces appropriate controls.

Risk: The skill can fetch unrestricted URLs.

Mitigation: Review target queries and fetched URLs before use in restricted environments, and disable browser or Firecrawl fallback when those channels are not approved.

Risk: Sensitive query state may remain on disk after use.

Mitigation: Review and delete ~/.openclaw/state/deep-scout/state.json after use on shared machines, or set DEEP_SCOUT_STATE_DIR to a controlled location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanjing/skills/deep-scout)
- [ClawHub release homepage](https://clawhub.ai/jonathanjing/deep-scout)
- [Publisher profile](https://clawhub.ai/user/jonathanjing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research report, comparison table, bullet summary, or timeline with source citations; the CLI emits text action blocks for the agent loop.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports depth, freshness, country, language, search-count, min-score, style, dimensions, and optional output-file parameters.]

## Skill Version(s):

0.1.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
