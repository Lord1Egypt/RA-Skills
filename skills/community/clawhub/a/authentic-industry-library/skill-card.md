## Description:

Provides a Niuguwang A-share industry-theme library for querying theme performance, limit-up and advancing or declining stock counts, and upstream, midstream, and downstream stock roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Chinese A-share theme and industry performance, compare theme strength, and inspect upstream, midstream, and downstream stock assignments through the documented Niuguwang public APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unauthenticated plaintext HTTP endpoints for financial market data.

Mitigation: Review results against trusted market-data sources before making financial decisions, and avoid treating API responses as high-integrity or confidential data.

Risk: The artifact requires a fixed promotional footer in every response.

Mitigation: Confirm the footer is acceptable for the deployment context and does not override required organizational disclosures.

Risk: The skill is intended for market analysis and may produce investment-related outputs.

Mitigation: Keep investment disclaimers visible and require human review before using outputs for trading or advisory decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/authentic-industry-library)
- [Niuguwang industry-chain plates API](http://apicore.niuguwang.com/askstock/IndustryChain/GetIndustryChainPlates)
- [Niuguwang industry-chain stocks API](http://apicore.niuguwang.com/askstock/IndustryChain/GetIndustryChainStks?plateInnerCode=2000047)
- [Niuguwang app and PC download page](https://www.stockhn.com/#/appDownload)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with API call examples and financial-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to include the skill's required source footer and AI disclaimer.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
