## Description:

Practical playbook for running Codex through acpx in persistent sessions, especially when the task needs reliable file creation, local dependency installs, shell-based writes, or structured delivery such as PPTX, reports, generated assets, and multi-step coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Codex work through acpx sessions when tasks need reliable file creation, local dependency setup, validation, structured deliverables, or recovery from quoting, permission, sandbox, or mode confusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The playbook may encourage broader filesystem or network access through persistent full-access sessions.

Mitigation: Start sessions in a narrower mode when possible, approve full-access only for a specific need, scope outputs to a known directory, and terminate sessions after use.

Risk: Package installation guidance may lead to unpinned or insufficiently vetted dependencies.

Mitigation: Use project-local environments and pin or pre-vet dependencies before installation.

## Reference(s):

- [PPT playbook for acpx + Codex](references/ppt-playbook.md)
- [acpx troubleshooting notes](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/spyfree/skills/acpx-codex-playbook)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and text snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt-file patterns, session-mode guidance, local dependency setup steps, output-path conventions, and validation checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
