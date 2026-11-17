## Description:

CCDB Factor Search helps agents search Chinese and English CCDB carbon and emission-factor data, compare candidates, filter weak matches, and return a best-fit factor with risks and direct-use guidance for PCF, LCA, carbon accounting, ESG, and supply-chain work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly5661](https://clawhub.ai/user/fly5661)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and carbon-accounting practitioners use this skill to find and evaluate CCDB emission or carbon-footprint factors for PCF, LCA, ESG, and supply-chain analysis. It is intended for best-fit factor selection with suitability notes rather than raw search-result retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Factor-search terms may be sent to Carbonstop or to a configured replacement endpoint.

Mitigation: Require explicit confirmation before remote lookup in sensitive business contexts, avoid submitting full BOMs or supplier-identifying details, and restrict the base URL to the intended Carbonstop endpoint.

Risk: An overridden endpoint could receive business-derived search terms.

Mitigation: Control use of endpoint-related environment variables and review configuration before running the query helper.

Risk: A returned factor may be unsuitable for formal reporting because of region, unit, factor type, applicability period, or encrypted-value limitations.

Mitigation: Use the skill's suitability classification and risk notes, then perform human review before using a factor in formal accounting, disclosure, or verification workflows.

## Reference(s):

- [CCDB API Contract](artifact/references/api-contract.md)
- [Domain Lexicon](artifact/references/domain-lexicon.md)
- [Matching Strategy](artifact/references/matching-strategy.md)
- [Output Template](artifact/references/output-template.md)
- [CCDB Carbon Factor Search Workflow](artifact/references/workflow.md)
- [Carbonstop CCDB factor query endpoint](https://gateway.carbonstop.com/management/system/website/queryFactorListClaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or structured JSON-style result summaries with factor fields, match class, reasoning, risks, alternatives, and search trace.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conservative no-recommendation responses when CCDB data is unavailable or candidate factors are unsuitable.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
