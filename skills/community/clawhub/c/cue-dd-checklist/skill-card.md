## Description:

Given an A-share company, an as-of date, a lookback window, and a research purpose, produces a cited public-disclosure risk checklist and coverage ledger without investment or legal conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts conducting initial pre-investment, credit, or M&A screening use it to assemble an evidence-linked public-disclosure checklist for one A-share company and see which categories were searched or unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-routing or redirect concerns could expose CUE_API_KEY or sensitive research context to an unverified destination.

Mitigation: Review the credential destination and redirect behavior; avoid sending credentials or sensitive research context to destinations that have not been independently verified.

Risk: Reported installation risks and behavior mismatches with the declared company-risk research purpose need review.

Mitigation: Review the installation source and version and resolve the reported purpose mismatch before installing.

Risk: The security analysis was partial, so unexamined behavior is not covered by its findings.

Mitigation: Treat the scan as partial and do not use it as assurance that unexamined behavior is safe.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-dd-checklist)
- [Channel map](references/channel-map.md)
- [Coverage map template](references/coverage-map-template.md)
- [Cue data MCP setup](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, JSONL, JSON, Text]

**Output Format:** [Markdown report and coverage map, JSONL source index, JSON evidence snapshots, and a plain-text run log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company, as-of-date, and lookback-window scoped; report rows link to disclosure anchors and include a human-review placeholder.]

## Skill Version(s):

0.1.36 (source: frontmatter; server release 0.1.36)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
