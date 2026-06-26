## Description: <br>
Provides multi-agent coordination protocols for handoffs, shared context, delegation, communication norms, and basic conflict resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edvisage](https://clawhub.ai/user/edvisage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to give agents structured protocols for coordinating multi-agent work, including task handoffs, shared context files, delegation, and conflict resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared handoff and context templates can expose secrets, regulated data, or unnecessary internal state if users paste too much context. <br>
Mitigation: Keep shared context files minimal and exclude secrets, credentials, regulated data, and unrelated agent memory from handoffs and logs. <br>
Risk: The free version provides coordination templates but does not enforce trust verification, automated routing, capability matching, or workload balancing. <br>
Mitigation: Use the templates only with trusted agents and manually verify receiving agents, routing decisions, task assignments, and returned outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edvisage/edvisage-agent-connect) <br>
- [Edvisage AI tools](https://edvisageglobal.com/ai-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown templates and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only coordination templates; no executable code or hidden automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
