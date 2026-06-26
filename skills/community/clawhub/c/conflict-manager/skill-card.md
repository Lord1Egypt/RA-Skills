## Description: <br>
Provides HTTP endpoints for scanning Git repository conflicts across multiple branches and applying AI-suggested resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brajesh9373](https://clawhub.ai/user/brajesh9373) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let a dashboard request repository conflict scans and apply proposed merge resolutions through HTTP endpoints while receiving WebSocket status events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests repository write authority and can perform real merges and pushes through HTTP endpoints. <br>
Mitigation: Grant repo:write only on repositories where automated conflict resolution is acceptable, and require explicit approval before merges or pushes. <br>
Risk: The release evidence notes insufficient scoping and safety detail around write operations. <br>
Mitigation: Review for authentication, default dry-run behavior, logging, and rollback guidance before installation. <br>


## Reference(s): <br>
- [Conflict Manager on ClawHub](https://clawhub.ai/brajesh9373/conflict-manager) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with endpoint descriptions, payload guidance, and implementation references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish WebSocket events for conflict scan results, resolution suggestions, and applied resolutions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
