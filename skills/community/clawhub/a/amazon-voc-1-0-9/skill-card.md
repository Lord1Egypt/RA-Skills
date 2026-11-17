## Description:

Amazon VOC (Buyer Voice) collects Amazon reviews and generates VOC insight reports covering negative-review pain points, purchase drivers, user personas, usage scenarios, Listing optimization suggestions, competitor comparison, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and operators use this skill to collect and analyze Amazon review data for VOC reports, competitor comparisons, trend analysis, and Listing or product improvement decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ARI credentials could be sent to an unintended API host if ARI_BASE_URL is set to an untrusted destination.

Mitigation: Avoid setting ARI_BASE_URL unless the destination is fully trusted; prefer a version that pins authenticated calls to https://ari.funewa.com or validates development overrides before using credentials.

Risk: Paid collection or analysis can consume ARI credits, and retrying after an interrupted paid operation may duplicate charges.

Mitigation: Run quote-only commands first, add --confirm only after explicit user approval, and check existing reports before retrying an interrupted paid action.

Risk: Small, partial, or failed review samples can produce misleading VOC conclusions.

Mitigation: Label small samples, use only successful API response parts, and separate direct API data from inference and strategic recommendations.

## Reference(s):

- [ARI CLI and API Reference](references/reference.md)
- [ARI API service](https://ari.funewa.com)
- [ClawHub release page](https://clawhub.ai/funewa/skills/amazon-voc-1-0-9)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include report IDs, credit usage, sample counts, time windows, account balance, and report URLs when returned by the ARI API.]

## Skill Version(s):

1.0.9 (source: artifact/_meta.json; ClawHub release version 1.0.0 from evidence.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
