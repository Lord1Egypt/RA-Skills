## Description: <br>
Find and select the best-fit CCDB carbon or emission factor for PCF, LCA, carbon accounting, ESG, and supply-chain work using bilingual search, candidate comparison, and suitability guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly5661](https://clawhub.ai/user/fly5661) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sustainability analysts, and carbon-accounting practitioners use this skill to find, compare, and select CCDB emission or carbon-footprint factors for PCF, LCA, ESG, scope 3, BOM, and supply-chain calculations. It is intended to support factor selection decisions with matching rationale, alternatives, and review guidance rather than returning only raw search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Carbon-factor search terms may disclose confidential BOM, supplier, product, or process details to Carbonstop's CCDB service. <br>
Mitigation: Avoid entering confidential or proprietary details unless disclosure to the external service is acceptable. <br>
Risk: Returned factors may be unsuitable for formal reporting because of region, unit, lifecycle-stage, source, factor-type, or data-coverage mismatches. <br>
Mitigation: Treat results as decision support and review candidate fit, assumptions, and source fields before using them in formal PCF, LCA, ESG, or carbon-accounting reports. <br>


## Reference(s): <br>
- [CCDB Factor Search on ClawHub](https://clawhub.ai/fly5661/ccdb-factor-search) <br>
- [CCDB API Contract](references/api-contract.md) <br>
- [Matching Strategy](references/matching-strategy.md) <br>
- [Output Template](references/output-template.md) <br>
- [CCDB Carbon Factor Search Workflow](references/workflow.md) <br>
- [Domain Lexicon](references/domain-lexicon.md) <br>
- [Carbonstop CCDB query endpoint](https://gateway.carbonstop.com/management/system/website/queryFactorListClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON-style structured analysis with recommended factor, match class, risk notes, alternatives, search trace, and direct-use guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a Python helper or direct API request to query Carbonstop CCDB; returned factors should be reviewed before formal reporting.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
