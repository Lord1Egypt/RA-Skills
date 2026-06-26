## Description: <br>
Decision-making advisor using Tree of Thoughts for exploring options, analyzing trade-offs, and providing data-driven recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banxian87](https://clawhub.ai/user/banxian87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and decision-makers use this skill to compare options, weigh criteria, assess trade-offs, and generate structured recommendations for technical, business, or personal decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision details, criteria, context, and options may be sent to the configured LLM provider. <br>
Mitigation: Do not include confidential business plans, financial details, legal issues, personal data, or trade secrets unless the provider configuration and retention policy are acceptable. <br>
Risk: LLM-generated scoring and recommendations can be incomplete or misleading for high-impact decisions. <br>
Mitigation: Treat outputs as decision support, review the assumptions and weights, and require human approval before acting on consequential recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banxian87/decision-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/banxian87) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured recommendation objects and Markdown-style analysis tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a recommendation, weighted score, confidence level, reasoning, risks, alternatives, and full option ranking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
