## Description: <br>
Structured decision-making patterns for common engineering choices, including library selection, architecture, build vs buy, prioritization, reversibility analysis, and ADRs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to compare tools, frameworks, and architecture options, prioritize work, and document significant technical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The alternate GitHub-based install command can point at a branch path that changes over time. <br>
Mitigation: Prefer `npx clawhub@latest install decision-frameworks`; if using the GitHub-based command, verify the repository and exact revision first. <br>
Risk: Manual global installation makes the skill available to the agent across projects. <br>
Mitigation: Use project-scoped installation when the decision guidance should only apply within a specific workspace. <br>


## Reference(s): <br>
- [Decision Frameworks Skill Page](https://clawhub.ai/wpank/decision-frameworks) <br>
- [Publisher Profile](https://clawhub.ai/user/wpank) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with tables, templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only decision aid; no API keys, MCP tools, or credential environment variables were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
