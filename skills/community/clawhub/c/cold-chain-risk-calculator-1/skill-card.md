## Description: <br>
Calculate temperature excursion risks for cold chain transport. Assesses route risk, packaging suitability, and monitoring requirements for biological samples and pharmaceuticals requiring controlled-temperature shipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA teams, and cold-chain operations staff use this skill to estimate temperature excursion risk for shipments from route, duration, and packaging inputs. It is suitable for lightweight planning and documentation support, not standalone regulated cold-chain decision making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented behavior overstates the script's actual scoring, validation, and output behavior. <br>
Mitigation: Review and correct the documented-versus-actual behavior before using the skill in QA, medical, pharmaceutical, or operational workflows. <br>
Risk: The risk model is simplified and does not account for route complexity, transit legs, or ambient temperature variability. <br>
Mitigation: Use the output as an illustrative planning aid and require domain review plus additional shipment data before making regulated or operational cold-chain decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/cold-chain-risk-calculator-1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe risk score, risk level, assumptions, caveats, and mitigation recommendations for cold-chain transport scenarios.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
