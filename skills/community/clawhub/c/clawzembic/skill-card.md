## Description:

Clawzempic audits OpenClaw efficiency and scores context injection, cron health, session bloat, configuration, skill bloat, and transcript size while identifying token waste and model right-sizing opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anna-claudette](https://clawhub.ai/user/anna-claudette)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to audit local or trusted remote OpenClaw installations, interpret weighted efficiency findings, and review suggested remediation commands before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote audit mode executes the audit over SSH on the named host.

Mitigation: Use --remote only with hosts you administer and trust, and verify SSH key-based access before running the skill.

Risk: Default terminal output includes styled text that may be unsafe to render in less-trusted terminals or logs.

Mitigation: Prefer --json when auditing less-trusted data or when forwarding results into dashboards and other tools.

Risk: --fix mode prints remediation commands and configuration changes that could alter OpenClaw behavior if applied blindly.

Mitigation: Treat --fix output as manual suggestions to review before editing cron jobs, sessions, skills, or configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anna-claudette/skills/clawzembic)
- [Publisher profile](https://clawhub.ai/user/anna-claudette)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal report or JSON, with optional remediation suggestions as reviewable shell commands and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads OpenClaw metadata under the configured .openclaw directory and can run over SSH for trusted remote hosts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
