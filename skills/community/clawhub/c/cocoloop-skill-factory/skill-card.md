## Description:

Guides agents through creating or upgrading multi-platform Agent Skills by turning rough ideas into stable specs, selecting platform templates, organizing atomic capabilities, planning scripts, and clarifying compatibility and release boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catrefuse](https://clawhub.ai/user/catrefuse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this meta skill to research, design, validate, and package new or upgraded Agent Skills across platforms such as Codex, Claude Code, OpenClaw, Copaw, Molili, and Hermes Agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local environment details as part of platform and tooling detection.

Mitigation: Run it only in workspaces where local platform, shell, browser, and tool availability may be shared with the agent.

Risk: The workflow may guide installation or execution of external CLIs, packages, browser extensions, or generated scripts.

Mitigation: Review commands before execution, pin dependency versions, and prefer isolated project environments over system-level installs.

Risk: Browser automation guidance may involve logged-in browser sessions.

Mitigation: Confirm account, permission, and session boundaries before using browser automation, and avoid high-risk or policy-restricted sites.

## Reference(s):

- [CocoLoop Skill Factory on ClawHub](https://clawhub.ai/catrefuse/skills/cocoloop-skill-factory)
- [Publisher profile: catrefuse](https://clawhub.ai/user/catrefuse)
- [Platform support matrix](artifact/ref/platform-support-matrix.md)
- [Factory Skill Builder](artifact/factory-skill-builder/README.md)
- [Browser access capability](artifact/atomic-capability/browser-access/index.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce skill specs, build plans, reference analyses, platform manifests, and packaged skill artifacts when the user authorizes the relevant steps.]

## Skill Version(s):

0.3.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
