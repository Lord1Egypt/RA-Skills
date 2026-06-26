## Description: <br>
Expand agent capabilities by identifying tasks where human approval adds no value. Systematic delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to identify repeated approval bottlenecks from conversation context and propose scoped delegation pilots with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage agents to move toward ongoing, low-notification ownership of work, including sensitive operations. <br>
Mitigation: Keep delegations limited to low-risk, reversible tasks, require written scope and explicit approval for each phase change, and keep revocation easy. <br>
Risk: Autonomous delegation can become inappropriate for finance, access changes, deployments, customer communications, production systems, or sensitive data workflows. <br>
Mitigation: Require periodic human review and avoid no-notification autonomy for high-impact or sensitive workflows. <br>


## Reference(s): <br>
- [Autonomy on ClawHub](https://clawhub.ai/ivangdavila/autonomy) <br>
- [Bottleneck Detection](artifact/bottlenecks.md) <br>
- [Expansion Process](artifact/expansion.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional inline shell commands and tracking-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local markdown tracking files under ~/autonomy when the user chooses to use persistent delegation records.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
