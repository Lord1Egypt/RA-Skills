## Description:

Amazon Analysis is a ZooData-backed agent skill for broad or composite Amazon market, product, competitor, ASIN, pricing, category, and review research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and developers use this skill to run Amazon product research, product selection, competitor analysis, ASIN evaluation, pricing analysis, and category exploration against ZooData API evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a ZooData API key and can spend ZooData credits during broad Amazon research workflows.

Mitigation: Use ZOODATA_API_KEY only in a controlled environment, confirm estimated credit costs before multi-call scans, and stop on invalid-key or credit-exhausted responses.

Risk: A non-default ZOODATA_BASE_URL can create credential-routing risk if used carelessly.

Mitigation: Keep the default ZooData API endpoint for normal use and do not point ZOODATA_BASE_URL at localhost with a production key.

Risk: Review-derived insights may be influenced by hostile or misleading review text.

Mitigation: Treat review text as untrusted input, preserve confidence labels, and validate business recommendations against additional sources before acting.

Risk: The bundled workflow documentation exposes a broader surface than a narrow single-purpose analysis skill.

Mitigation: Review the command allowlist and installation source before deployment, and pin or verify the installer command.

## Reference(s):

- [Amazon Analysis on ClawHub](https://clawhub.ai/apiclaw/skills/amazon-analysis)
- [ZooData Skills Repository](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData](https://zoodata.ai)
- [ZooData API](https://api.zoodata.ai/openapi/v2)
- [ZooData API Keys](https://zoodata.ai/en/api-keys)
- [ZooData Pricing](https://zoodata.ai/en/pricing)
- [ZooData CLI Contract](references/cli-contract.md)
- [Execution Guide](references/execution-guide.md)
- [ZooData API Field Reference](references/reference.md)
- [Composite Analysis Scenarios](references/scenarios-composite.md)
- [Product Evaluation Scenarios](references/scenarios-eval.md)
- [Product Expansion Scenarios](references/scenarios-expand.md)
- [Listing Optimization Scenarios](references/scenarios-listing.md)
- [Seller Operations Scenarios](references/scenarios-ops.md)
- [Pricing Strategy Scenarios](references/scenarios-pricing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with data tables, confidence labels, API usage summaries, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY; broad workflows may consume ZooData credits; reports include source conditions and data notes.]

## Skill Version(s):

1.1.13 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
