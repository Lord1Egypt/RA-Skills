## Description: <br>
Amazon PPC campaign builder and optimizer for sellers that builds new campaign structures, audits existing campaigns, calculates ACoS targets, recommends bid adjustments, and generates negative keyword lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce operators use this skill to build PPC launch campaign blueprints or optimize existing campaigns with ACoS calculations, keyword migration, bid adjustments, and negative keyword recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASINs, product descriptions, and keyword prefixes may be used for Amazon or web lookups during competitor and keyword research. <br>
Mitigation: Ask the agent to confirm before external research and avoid sharing confidential product strategy or regulated data unless the lookup behavior is approved. <br>
Risk: The bundled competitor fetch script performs public Amazon listing lookups, which may raise marketplace policy or scraping compliance concerns in some environments. <br>
Mitigation: Review the script and applicable marketplace terms before use, and disable or require approval for the script where scraping is not permitted. <br>
Risk: PPC recommendations are planning guidance and do not automatically apply changes in Seller Central. <br>
Mitigation: Manually verify campaign settings, bids, ACoS calculations, and negative keywords in Seller Central before implementing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/amazon-ppc-campaign) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with campaign setup tables, calculations, action plans, and optional shell command output from the competitor fetch script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces seller-facing PPC campaign blueprints, optimization plans, keyword groupings, bid recommendations, negative keyword lists, and follow-up questions for missing campaign inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
