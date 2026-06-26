## Description: <br>
Lightweight collaboration layer for multi-agent systems that provides file-based protocols for audit findings, context packs, mission control, flight recording, and experience promotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhelunsun](https://clawhub.ai/user/zhelunsun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple agents in one workspace through shared plain-text findings, context packs, mission control summaries, and handoff records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mission control may read .workbuddy memory logs outside the documented .agent-os project folder. <br>
Mitigation: Review or patch mission_control.py before deployment if the environment must avoid home-directory paths or stay strictly inside .agent-os. <br>
Risk: The skill creates and updates local coordination files under .agent-os. <br>
Mitigation: Install only in workspaces where local project coordination files are acceptable and review generated files before sharing them. <br>


## Reference(s): <br>
- [Agent OS ClawHub release](https://clawhub.ai/zhelunsun/agent-os-zhelun) <br>
- [Interface Contract](docs/INTERFACES.md) <br>
- [Schemas](references/schemas.md) <br>
- [Workflows](references/workflows.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSONL, JSON examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local project coordination files under .agent-os; some workflow outputs are templates in this release.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
