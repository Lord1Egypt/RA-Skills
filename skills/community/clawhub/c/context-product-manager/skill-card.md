## Description: <br>
Turn rough product, feature, or repo-change requests into a PM-grade plan plus agent-ready execution context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhu-ai](https://clawhub.ai/user/openclawzhu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and agent operators use this skill to turn vague product or repo-change requests into scoped plans, canonical context blueprints, and agent-ready handoffs. It is especially useful when work needs product framing, MVP slicing, acceptance criteria, or separate Codex, Antigravity, or OpenClaw execution context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads relevant workspace files when preparing repo-aware plans, which can expose project context to the active agent session. <br>
Mitigation: Confirm the workspace files are appropriate for agent review before using the skill on sensitive repositories. <br>
Risk: Generated handoffs can guide another coding agent toward incorrect scope, assumptions, or acceptance criteria if not reviewed. <br>
Mitigation: Review generated plans and handoffs before delegating work or allowing another automated coding agent to act on them. <br>
Risk: The skill defaults to Chinese for conversational planning, which may be unexpected in some teams. <br>
Mitigation: Set the desired language explicitly when using the skill in teams that require another working language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhu-ai/context-product-manager) <br>
- [Intake Framework](references/intake-framework.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Rendering Rules](references/rendering-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown plans, context blueprints, and agent handoffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Chinese user-facing planning sections and English coding-agent handoffs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
