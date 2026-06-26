## Description: <br>
Calculates an Amazon listing push score from CTR, CVR, 7-day growth, and account health, then classifies the traffic tier and suggests optimization priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon marketplace operators and ecommerce teams use this skill to evaluate listing traffic potential from four supplied metrics and receive traffic-tier classification with prioritized CTR, CVR, growth, and account-health improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Amazon-ranking trigger terms may invoke the skill when the user does not intend push-score or traffic-tier analysis. <br>
Mitigation: Confirm the user wants Amazon push-score analysis and has provided the four required metrics before relying on recommendations. <br>
Risk: The score and optimization plan depend on user-supplied metrics and benchmark heuristics rather than real-time Amazon platform data. <br>
Mitigation: Verify the input metrics from trusted operational sources and treat the generated strategy as planning guidance. <br>


## Reference(s): <br>
- [Amazon Push Score on ClawHub](https://clawhub.ai/wangm-a3/amazon-push-score) <br>
- [CloudTrip homepage](https://cloudtrip.ai) <br>
- [Amazon industry benchmarks](references/benchmarks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with calculations and score tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied CTR, CVR, 7-day growth, and account health inputs; does not connect to Amazon data sources.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
