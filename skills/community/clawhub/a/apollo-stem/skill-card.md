## Description: <br>
Apollo Stem helps an OpenClaw agent check whether its core skills and self-improvement records need renewal while preserving existing experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to review core skill freshness, self-improvement records, workflow status, and script implementation coverage before deciding whether to update or create skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language and an open-ended self-update workflow could lead an agent to change skills without a clear approval step. <br>
Mitigation: Run this skill manually for maintenance and require explicit human review before applying any proposed skill changes. <br>
Risk: The bundled status script reads hard-coded /root/.openclaw/workspace paths and writes .stem/state.json, exposing local workspace metadata to the maintenance flow. <br>
Mitigation: Execute it only in the intended OpenClaw workspace, review the paths before running, and treat the generated state file as local workspace metadata. <br>
Risk: Skill updates suggested by the maintenance workflow could introduce incorrect or misleading guidance. <br>
Mitigation: Review and scan changed skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/apollo-stem) <br>
- [Publisher profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance; optional shell-script status report and JSON state file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled status script reads OpenClaw workspace status files and writes .stem/state.json when run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
