## Description: <br>
Keep your constraints healthy with lifecycle management and automatic staleness detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain constraint governance state, run periodic reviews, generate indexes, verify generated constraint artifacts, and manage schema migrations in an agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governance checks can update reports and workspace state during periodic maintenance or HEARTBEAT runs. <br>
Mitigation: Use the skill in trusted workspaces and review changes under output/governance/, output/constraints/, and agentic/INDEX.md before relying on them. <br>
Risk: The documented review cadence is advisory and does not itself enforce compliance decisions. <br>
Mitigation: Treat review output as decision support and require human approval before renewing, retiring, or migrating constraints. <br>
Risk: Full governance behavior depends on constraint-engine and failure-memory data being present and intended for the workspace. <br>
Mitigation: Install the documented governance stack and confirm .openclaw/governance.yaml or .claude/governance.yaml points to the expected workspace paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/agentic-governance) <br>
- [Publisher profile](https://clawhub.ai/user/leegitw) <br>
- [Packaged skill definition](artifact/SKILL.md) <br>
- [OpenClaw governance configuration](.openclaw/governance.yaml) <br>
- [Claude governance configuration](.claude/governance.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured workspace files for governance state, reviews, alerts, indexes, and verification results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes expected workspace outputs under output/governance/, output/constraints/, and agentic/INDEX.md when invoked.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
