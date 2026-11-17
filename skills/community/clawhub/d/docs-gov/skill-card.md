## Description:

Audits and checks a project's documentation governance, and can install configuration, templates, and hooks to keep documentation aligned with the code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to diagnose missing governance practices, check whether documentation reflects project reality, and optionally install ongoing documentation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installed commit and Claude Code hooks persist and may block commits or file creation.

Mitigation: Review the planned changes before init --yes, and remove the installed hooks and settings entries when no longer needed.

Risk: Claude Code hooks may later execute an existing project-supplied governance script that has not been authenticated.

Mitigation: Before init --yes in a repository you do not fully control, inspect scripts/governance.py and confirm it matches the reviewed bundled copy.

## Reference(s):

- [docs-gov release on ClawHub](https://clawhub.ai/xiaoba-dev/skills/docs-gov)
- [Documentation governance framework](artifact/framework.md)
- [Incident list](artifact/incidents.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Plain-text audit and check reports; configuration, scripts, hooks, and Markdown templates when initialized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit and check are read-only; init previews changes unless explicitly confirmed with --yes.]

## Skill Version(s):

2.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
