## Description:

Amazon FBA Finder helps Amazon sellers evaluate product opportunities with product discovery, competition analysis, supplier recommendations, and FBA profit calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace sellers and ecommerce operators use this skill to screen product ideas, estimate competition and profitability, and prepare supplier due-diligence questions before committing inventory spend.

### Deployment Geography for Use:

Global, with artifact-declared marketplace support for US, UK, DE, JP, CA, and AU.

## Known Risks and Mitigations:

Risk: Marketplace API keys and product research queries may be shared with configured services.

Mitigation: Install only when those disclosures are acceptable, scope credentials to the minimum needed access, and rotate keys if exposure is suspected.

Risk: Profit, sales, supplier, and market outputs are estimates that can mislead inventory or purchasing decisions if treated as guarantees.

Mitigation: Validate inputs and outputs manually against current marketplace, supplier, fee, and policy data before spending or launching products.

Risk: Dependencies are specified as minimum versions rather than a reviewed lockfile.

Mitigation: Use pinned dependency versions or a reviewed lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/amazon-fba-finder-lvjunjie)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and Python-oriented analysis objects or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include estimated sales, supplier, fee, margin, ROI, and recommendation fields; financial results should be manually validated.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
