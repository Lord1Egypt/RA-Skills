## Description: <br>
Selects a response path for incoming tasks, routing urgent or simple work faster and complex work toward deeper analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to classify a task by urgency, complexity, and context, then choose a fast, standard, guarded, or deep-analysis response path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Urgent-sounding requests can be routed toward reduced-confirmation handling. <br>
Mitigation: Keep normal confirmations for external, irreversible, privileged, sensitive, business, or financial actions. <br>
Risk: User task text may be retained in local .neuro route state. <br>
Mitigation: Inspect or clear the local .neuro state before sharing workspaces, and avoid entering sensitive task text when possible. <br>


## Reference(s): <br>
- [Apollo Neuro ClawHub release](https://clawhub.ai/nic-yuan/apollo-neuro) <br>
- [Publisher profile: nic-yuan](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance and shell route reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script may save task, route, circadian phase, and timestamp data to local .neuro route state JSON.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
