## Description: <br>
Audit an OpenClaw agent's behavior-layer rules and prompt sources to find drift, redundancy, conflict, loss of focus, and weak behavior guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gkso](https://clawhub.ai/user/gkso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to audit OpenClaw behavior-layer files, identify rule drift or conflict, and produce concrete restructuring recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit outputs may summarize private agent rules, memory, identity, or user-profile files. <br>
Mitigation: Use only in workspaces where this analysis is acceptable, and review results before sharing them outside the workspace. <br>
Risk: Restructuring recommendations could introduce incorrect or misleading behavior guidance if applied without review. <br>
Mitigation: Treat recommendations as proposals and review changes before updating live behavior-layer files. <br>


## Reference(s): <br>
- [OpenClaw behavior sources](references/openclaw-behavior-sources.md) <br>
- [Output template for agent-rule-audit](references/output-template.md) <br>
- [Problem types for agent-rule-audit](references/problem-types.md) <br>
- [ClawHub release page](https://clawhub.ai/gkso/agent-rule-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with prioritized findings and file-specific recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive summaries of private agent behavior-layer files; review before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
