## Description: <br>
AgentTherapy helps agents handle uncertainty, repeated errors, correction, and ability limits by stopping bluffing, stating blockers, and offering concrete fallback options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macoloye](https://clawhub.ai/user/macoloye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and agent operators use this skill to help an agent recover when it is stuck, uncertain, corrected, blocked by missing context or tools, or at risk of hallucinating. It gives the agent a concise failure-handling pattern: pause, name the blocker, state what can and cannot be verified, and offer concrete next options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable working-style notes could capture sensitive information if an agent stores more than practical correction preferences. <br>
Mitigation: If note-taking is enabled, keep notes short and non-sensitive, and avoid storing secrets, logs, personal data, or psychological inferences. <br>
Risk: The therapy framing could be misunderstood as human mental-health support. <br>
Mitigation: Use the skill only as an agent failure-handling policy; the artifact explicitly states that it is not therapy for humans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macoloye/agenttherapy) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with response templates and compact preference-note examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code or hidden access requests were identified in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
