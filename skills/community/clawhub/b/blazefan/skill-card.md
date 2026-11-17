## Description:

通用 EC 风扇调速方法论，帮助代理排查 sysfs、EC 寄存器和 I/O 端口接口并生成风扇控制方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and advanced laptop users use this skill to diagnose available fan-control interfaces and prepare cautious fan tuning commands or service configuration. It is most relevant when vendor tools are unavailable or need to be compared with EC-level control paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged fan-control commands and EC writes can affect hardware behavior on unsupported or incorrectly identified machines.

Mitigation: Verify the exact model, control interface, fan count, and register behavior before writing values; prefer sysfs, vendor, or kernel-supported fan interfaces when available.

Risk: Persisting ec_sys write support or a systemd fan-control service can preserve unsafe settings across reboots.

Mitigation: Do not persist write support until the configuration is validated, and keep documented rollback steps to restore firmware or BIOS fan control.

Risk: Running multiple fan-control tools can create conflicting control loops.

Mitigation: Use one fan-control backend at a time and disable competing tools before deploying a persistent loop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/blazefan)
- [nbfc-linux documentation](https://github.com/nbfc-linux/nbfc-linux)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline bash, C snippets, shell scripts, and systemd configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged commands and hardware-specific values that require user verification before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
