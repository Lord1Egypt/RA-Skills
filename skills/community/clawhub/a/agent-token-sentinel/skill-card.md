## Description: <br>
Real-time cost and quota guardian for AI agents that monitors API usage and can stop recursive loops or excessive reasoning to protect budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to keep agent sessions within token or dollar budgets, detect repeated work, and receive quota warnings before usage overruns occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real implementation of the advertised cost-control behavior could terminate active agent work when a budget cap is reached. <br>
Mitigation: Review the cap before use and run it only where stopping active agent processes is acceptable for budget protection. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a per-session budget cap supplied by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
