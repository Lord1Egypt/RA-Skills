## Description: <br>
A local Ebbinghaus forgetting-curve utility for memory decay calculations and simple spaced-repetition scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add configurable memory-decay scoring, review-interval calculation, and batch decay processing to local memory or retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation and roadmap claims do not fully agree with the implemented API surface. <br>
Mitigation: Verify the exact functions and constructor signatures in forgetting_curve.py before depending on documented power-law decay or complete SRS behavior. <br>
Risk: Memory decay scores can affect retrieval priority or review scheduling if integrated into another system. <br>
Mitigation: Review configured half-life, threshold, and interval parameters against the target workflow before using the scores for automated decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whoisme007/forgetting-curve) <br>
- [Publisher profile](https://clawhub.ai/user/whoisme007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and API usage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Python utility guidance; no external service calls are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
