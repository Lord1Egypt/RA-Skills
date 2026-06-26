## Description: <br>
Provides a Chief Risk Officer assistant skill for assessing market, credit, operational, and other enterprise risks and generating impact analysis and response guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wen-Si](https://clawhub.ai/user/Wen-Si) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Enterprise risk, compliance, audit, and investment-support teams can use this skill to perform lightweight risk assessments, summarize likely financial, reputational, and operational impacts, and receive response recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's simplified scoring and recommendation logic may be mistaken for professional financial, legal, compliance, or investment advice. <br>
Mitigation: Use outputs as decision support only and require qualified review before acting on business-critical recommendations. <br>
Risk: Release provenance is unavailable, which limits independent auditability of the skill's origin. <br>
Mitigation: Review the publisher profile, release metadata, and artifact source before deployment. <br>
Risk: Static risk levels may not reflect an organization's actual exposure, controls, thresholds, or regulatory obligations. <br>
Mitigation: Validate and adapt the risk model against organization-specific policies, data, and review procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wen-Si/croskill) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact ClawHub metadata](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, code] <br>
**Output Format:** [JSON object with risk status, risk type, assessment details, recommendations, and timestamp] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external dependencies; scoring is based on simple local heuristics keyed primarily by risk type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
