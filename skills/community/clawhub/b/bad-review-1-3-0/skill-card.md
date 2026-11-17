## Description:

Analyzes 1-3 star Amazon reviews for a specified ASIN, groups negative-review causes such as quality issues, shipping damage, description mismatch, and user confusion by frequency, and produces improvement recommendations, charts, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, commerce operators, and support teams use this skill to collect and analyze Amazon review data for specified ASINs, identify negative-review root causes, compare competitors or categories, and generate VOC reports and listing or product improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can send the saved ARI API key to a service URL selected through environment configuration.

Mitigation: Use only trusted execution environments, leave ARI_BASE_URL unset unless it points to the legitimate ARI service, and rotate any ari_live_ key that may have been exposed in an untrusted environment.

Risk: Paid collection, analysis, leaderboard, and advice commands can spend ARI credits when run with explicit confirmation.

Mitigation: Review the quoted cost, balance, ASIN, site, and command before approving --confirm; after interruptions, check existing reports before retrying a paid command.

Risk: Exports and workbench actions can write local files or update review workflow state.

Mitigation: Review export destinations and workbench status updates before approving those actions.

## Reference(s):

- [ClawHub Listing](https://clawhub.ai/funewa/skills/bad-review-1-3-0)
- [Server-Resolved Source Repository Path](https://github.com/funewa/amazon-bad-review/tree/main/bad-review-1.3.0)
- [ARI CLI and API Reference](references/reference.md)
- [Skill README](README.md)
- [ARI Service](https://ari.funewa.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and structured JSON responses, with optional CSV, Markdown, or HTML export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ARI API key; paid collection, analysis, leaderboard, and advice actions require explicit confirmation.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata); artifact internal version 1.3.0 (source: SKILL.md frontmatter, _meta.json, scripts/ari.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
