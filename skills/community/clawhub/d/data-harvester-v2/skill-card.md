## Description:

Batch web scraping for competitor analysis, price monitoring and market research.

This skill is for research and development only.

## Publisher:

[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto)

### License/Terms of Use:


## Use Case:

Developers, analysts, and researchers use this skill to run command-driven market research workflows for stock lookups, sector summaries, news keyword results, competitor comparisons, and batch URL-list handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch command can read and print local file contents from any path supplied by the caller.

Mitigation: Run the skill in a sandbox or wrapper that restricts batch inputs to a dedicated URL-list directory and avoids sensitive local files.

Risk: The security verdict is suspicious and calls for review before installation.

Mitigation: Review the artifact and security guidance before deploying the skill, then scan it in the target environment.

Risk: Finance, news, comparison, and export outputs may be mock or incomplete.

Mitigation: Do not rely on these outputs for business, financial, or operational decisions without verification from trusted data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windy-001-crypto/skills/data-harvester-v2)
- [ClawHub publisher profile](https://clawhub.ai/user/windy-001-crypto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text and Markdown-compatible command output with tables, status messages, and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some finance, news, comparison, and export outputs are mock or incomplete according to the security guidance and artifact behavior.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
