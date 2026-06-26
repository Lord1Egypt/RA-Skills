## Description: <br>
Agent Pool defines a global registry of business agents, including each agent's capabilities, tool dependencies, memory paths, workspace, and trigger conditions for on-demand workflow orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renxm78-creator](https://clawhub.ai/user/renxm78-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business automation teams use this skill to look up available business agents, understand their responsibilities and dependencies, and connect new systems to the right agents without pre-binding them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry can guide external research collection, outreach, posting, and email workflows without sufficient approval boundaries. <br>
Mitigation: Require human approval for external collection and outbound actions, and define explicit trigger contracts for each agent before operational use. <br>
Risk: Shared memory and knowledge-base workflows can write or expose data across systems if access boundaries are unclear. <br>
Mitigation: Restrict write paths and shared knowledge-base access, and set retention, deletion, and sensitive-data handling rules before deployment. <br>


## Reference(s): <br>
- [Agent detailed registry](references/agent-registry.md) <br>
- [System onboarding template](references/system-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with registry tables and onboarding steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
