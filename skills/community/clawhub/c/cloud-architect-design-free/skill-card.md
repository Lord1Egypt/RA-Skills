## Description: <br>
Provides single-cloud architecture design, basic cost estimates, service selection, and best-practice guidance for individual developers and small teams planning AWS, Azure, or GCP applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and small teams use this skill to draft single-cloud architecture plans, estimate monthly cloud costs, choose services, and get baseline security and operations recommendations before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags the skill as suspicious because it requests shell execution even though it describes itself as LLM-only. <br>
Mitigation: Install only if shell execution is acceptable for the target environment, or remove exec permission before use. <br>
Risk: Architecture and cost recommendations may be incomplete or inaccurate for a specific cloud account, region, workload, or discount model. <br>
Mitigation: Have a cloud engineer validate the generated plan against current provider pricing, security requirements, and operational constraints before deployment. <br>
Risk: The artifact uses broad create, modify, delete, export, and save language that could be confused with taking real infrastructure or file actions. <br>
Mitigation: Treat those operations as advisory text generation unless a reviewed version explicitly narrows tool permissions and action scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-architect-design-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with architecture components, cost estimates, service recommendations, and advisory tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not directly call cloud provider APIs; cost estimates and architecture guidance should be reviewed before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
