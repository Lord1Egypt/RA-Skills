## Description: <br>
Universal multi-agent workflow orchestration using Claude Code Agent Teams. Use when user asks to run a team workflow, create an agent team, or coordinate parallel work across multiple teammates - for any domain (software, content, data, strategy, research, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doanbactam](https://clawhub.ai/user/doanbactam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to set up, coordinate, and quality-gate Claude Code Agent Teams for multi-step work across software, content, data, strategy, and research domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected context may be shared with multiple spawned agents during team workflows. <br>
Mitigation: Avoid confidential inputs unless every teammate should see them, and scope each teammate prompt to only the context needed for its task. <br>
Risk: Delegated workflows may lead to irreversible, costly, published, deployed, or compliance-sensitive actions if not gated. <br>
Mitigation: Require explicit user approval before publishing, deploying, spending money, making irreversible changes, or performing legal or compliance-sensitive actions. <br>
Risk: The workflow relies on agent handoffs and synthesis, so incomplete context sharing can reduce output quality. <br>
Mitigation: Review the workflow scope before spawning teammates and validate each handoff against the agreed definition of done. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/doanbactam/claude-agent-team-workflows) <br>
- [Domain Presets](reference/domain-presets.md) <br>
- [Pipeline Patterns](reference/patterns.md) <br>
- [Prompt Templates](reference/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown with workflow specifications, role cards, task prompts, and handoff instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Agent Teams to be enabled before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
