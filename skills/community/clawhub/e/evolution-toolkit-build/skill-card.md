## Description:

Evolution Toolkit provides portable agent self-improvement tooling for session handoffs, reasoning-style measurement, guidance contradiction scanning, prediction logging, playbook optimization, Socratic questioning, and cross-session coherence analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ergopitrez](https://clawhub.ai/user/ergopitrez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add portable self-improvement workflows to agent workspaces, including session continuity, reasoning audits, guidance consistency checks, prediction calibration, playbook optimization, and structured thinking-partner behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit can read and persist sensitive workspace memory, identity or guidance files, task context, and personal reasoning notes.

Mitigation: Install it only in workspaces approved for that analysis, set EVOLUTION_TOOLKIT_WORKSPACE explicitly, review generated files under memory/, and avoid shared or synced directories for sensitive reports or imprints.

Risk: The playbook optimizer can send playbooks and test cases to Gemini.

Mitigation: Use the optimizer only when the selected playbooks, test cases, and configuration are safe to send to Google-hosted model services.

Risk: The README's unpinned npx install command can resolve to a changing package version.

Mitigation: Prefer a pinned installer version for reproducible installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ergopitrez/skills/evolution-toolkit-build)
- [Session Continuity Protocol](artifact/protocols/session-continuity.md)
- [Thinking Partner Protocol](artifact/protocols/thinking-partner.md)
- [Configuration Example](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown files, with optional JSON output from selected scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts write workspace memory files or reports under EVOLUTION_TOOLKIT_WORKSPACE.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
