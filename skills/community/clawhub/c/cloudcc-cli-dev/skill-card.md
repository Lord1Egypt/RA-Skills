## Description:

CloudCC CRM development CLI assistant for requirements breakdown, solution selection, and CloudCC asset creation, pull, and publish workflows using cloudcc-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[androidxhm](https://clawhub.ai/user/androidxhm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate CloudCC CRM customization requests into delivery plans and to operate cloudcc-cli workflows for objects, fields, menus, applications, backend classes, schedulers, triggers, and Vue custom components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation of an unpinned global cloudcc-cli package, including sudo-based installation on macOS.

Mitigation: Avoid sudo npm installation where possible, pin and verify the cloudcc-cli package before use, and install only when CloudCC CRM development tooling is intentionally required.

Risk: The skill can guide pull and publish operations that affect CloudCC CRM assets using developer credentials.

Mitigation: Use least-privileged CloudCC credentials, work in a development or staging org first, and require a human diff and review before pull or publish commands.

Risk: CloudCC developer keys, safety marks, secret keys, open secret keys, or tokens could be exposed through generated configuration or committed files.

Mitigation: Do not include real secrets in output, code, or commits; keep local configuration private and ignore secret-bearing configuration files in source control.

Risk: Pull operations and snippet synchronization can overwrite local logic inside the publishable source regions.

Mitigation: Keep publishable backend logic only inside the documented source markers, remove local-only debug code before synchronization, and review diffs after pull operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/androidxhm/skills/cloudcc-cli-dev)
- [SKILL.md](artifact/SKILL.md)
- [REQUIREMENTS_BREAKDOWN.md](artifact/REQUIREMENTS_BREAKDOWN.md)
- [INSTALL_AND_BOOTSTRAP.md](artifact/INSTALL_AND_BOOTSTRAP.md)
- [OBJECTS_AND_FIELDS.md](artifact/OBJECTS_AND_FIELDS.md)
- [BACKEND_CODE.md](artifact/BACKEND_CODE.md)
- [VUE_CUSTOM_COMPONENT.md](artifact/VUE_CUSTOM_COMPONENT.md)
- [CLI_CHEATSHEET.md](artifact/CLI_CHEATSHEET.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, code snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include CloudCC asset plans, command sequences, generated code snippets, and review checklists.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
