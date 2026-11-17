## Description:

Provides nine portable C99 driver templates, wiring notes, validation records, and peripheral initialization guidance for common embedded modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Embedded developers use the skill to find driver templates, wiring guidance, peripheral initialization requirements, and porting pitfalls for common sensors, displays, wireless modules, and motors. The templates are porting references and require adaptation to the target platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence classifies the release as suspicious and cites test-runner, tool-scope, and driver-documentation concerns; review is partial because two SKILL.md references could not be resolved.

Mitigation: Avoid installation until the maintainer explains or addresses the reported issues, and resolve and review the missing references before reassessing the package.

Risk: Hardware wiring and timing guidance may need adaptation to the specific component and board.

Mitigation: Check hardware-specific values against the component's official datasheet and adapt the port layer for the target platform.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liujycode/skills/embedded-driver-templates)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with C code blocks and wiring tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Porting reference; adapt the platform-specific port layer for the target hardware.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
