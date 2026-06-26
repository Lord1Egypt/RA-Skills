## Description: <br>
Audit a game feature, live update, roadmap item, event, or content drop by how different player segments are likely to perceive it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game designers, product managers, and live-ops teams use this skill to evaluate how different player segments may perceive a feature, update, event, or content drop. It helps identify audience, access, visibility, messaging, and expectation risks before rollout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can analyze unreleased feature, roadmap, event, or monetization plans that may be confidential. <br>
Mitigation: Use only product information that the operator is comfortable having processed by the agent, consistent with the security guidance. <br>
Risk: Metadata tags include crypto and purchasing-related capabilities even though the security evidence found no purchase, wallet, payment, or hidden execution behavior. <br>
Mitigation: Do not grant purchasing, wallet, payment, or transaction authority based only on metadata tags. <br>
Risk: The output is a design perception aid and may produce incomplete or misleading recommendations if treated as a substitute for player research. <br>
Mitigation: Review recommendations with product, design, and research stakeholders before using them for rollout or messaging decisions. <br>


## Reference(s): <br>
- [Segment Layers](references/segment-layers.md) <br>
- [Perception Failures](references/perception-failures.md) <br>
- [Recommendation Patterns](references/recommendation-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stanestane/game-design-player-segment-perception-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/stanestane) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown structured into feature read, target segment read, cross-segment perception, access and visibility mismatch, risk diagnosis, and recommendation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only audit output; no code execution, credential use, purchases, or data exfiltration is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
