## Description:

Use this skill when you need portable agent self-improvement tooling: capture session handoffs, measure reasoning style, scan guidance for contradictions, log predictions, optimize playbooks, run Socratic questioning, or analyze cross-session coherence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ergopitrez](https://clawhub.ai/user/ergopitrez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve session continuity, audit reasoning behavior, find contradictory guidance, log predictions, and improve agent playbooks across workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive behavioral memory or workspace notes.

Mitigation: Review before installing in workspaces with private notes, customer data, proprietary prompts, or broad secrets; prefer a dedicated test workspace.

Risk: The playbook optimizer can send local playbooks or test cases to Gemini using workspace credentials.

Mitigation: Avoid running the optimizer on confidential playbooks unless external Gemini processing is acceptable, and prefer explicit environment variables over workspace .secrets files.

Risk: The thinking-partner protocol can affect default assistant behavior if treated as a standing policy.

Mitigation: Use the thinking-partner protocol as opt-in guidance for suitable tasks rather than as a default behavior policy.

## Reference(s):

- [Evolution Toolkit on ClawHub](https://clawhub.ai/ergopitrez/skills/evolution-toolkit)
- [Session Continuity Protocol](protocols/session-continuity.md)
- [Thinking Partner Protocol](protocols/thinking-partner.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal text, JSON, and workspace files depending on the selected tool.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts write state under the configured workspace memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
