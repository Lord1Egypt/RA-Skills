## Description:

Semiconductor supply chain intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lboquillon](https://clawhub.ai/user/lboquillon)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, policy teams, and developers use ChipChain to investigate semiconductor materials, equipment suppliers, dependencies, and chokepoints. It guides multilingual searches, filing and database checks, source registries, confidence grading, and explicit reporting of unverified gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional verifier scripts may install or execute unpinned dependencies.

Mitigation: Review the scripts before running them and execute them only in an isolated virtual environment.

Risk: Some documented API examples can expose credentials, including KIPRIS examples over plaintext HTTP.

Mitigation: Use least-privilege research API keys, avoid sending real keys over plaintext HTTP unless the transport risk is accepted, and rotate any key previously used that way.

Risk: Static supply-chain data can become stale or be mistaken for confirmed current relationships.

Mitigation: Treat bundled entity and chemistry files as leads, require fresh source access for current claims, and preserve confidence labels and unverified-gap sections in reports.

## Reference(s):

- [ChipChain ClawHub Skill Page](https://clawhub.ai/lboquillon/skills/chipchain)
- [Data Sources and API Reference](sources.md)
- [Evidence Types and Confidence Caps](evidence-guide.md)
- [Supplier Identification Workflow](queries/supplier-id.md)
- [Scenario Analysis Workflow](queries/scenario.md)
- [Chemistry Chain Workflow](queries/chemistry-chain.md)
- [Trade HS Codes](trade/hs-codes.md)
- [UN Comtrade API](https://comtradeapi.un.org/data/v1/get/C/A/HS)
- [OpenDART API](https://opendart.fss.or.kr/api/)
- [Lens Patent API](https://api.lens.org/patent/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with source registries, confidence grades, search logs, gaps, and occasional shell or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite accessed sources, distinguish confirmed findings from inferences, and state what could not be verified.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
