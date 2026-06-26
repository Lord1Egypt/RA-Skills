## Description: <br>
Amazon Fba Finder helps agents analyze Amazon FBA product opportunities, market competition, supplier options, and FBA profit estimates for seller product research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce operators use this skill to evaluate candidate FBA products, compare competition, estimate costs and margins, and receive supplier-related guidance. The artifact shows a prototype-style implementation, so outputs should support due diligence rather than replace independent business validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises live Amazon product discovery and supplier recommendations, but evidence.security says the provided code appears prototype-like and the live data integrations are mostly unfinished. <br>
Mitigation: Treat results as exploratory analysis only until the publisher provides working, verifiable data integrations and pinned dependencies. <br>
Risk: The skill asks users to configure Amazon and Alibaba API keys, and evidence.security warns against placing API keys in prompt-visible files. <br>
Mitigation: Store API keys in environment variables or a secrets manager and avoid putting credentials in prompt-visible project files. <br>
Risk: The skill may influence paid product sourcing and inventory decisions. <br>
Mitigation: Validate all product, supplier, fee, and sales estimates against authoritative marketplace and supplier data before making business commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/amazon-fba-finder-lvjunjie) <br>
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python dictionaries and human-readable analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include product opportunity scores, competition summaries, supplier recommendations, FBA profit calculations, and overall recommendation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
