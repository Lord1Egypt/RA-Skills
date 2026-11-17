## Description:

Cogniexec routes cognitive, planning, coding, command execution, and utility-script tasks through a layered orchestration skill for analysis, automation, and code-related work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to plan, analyze, write code, generate shell commands, and orchestrate multi-step automation workflows with bundled utility scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automation can execute code, mutate files, databases, Git state, network services, or email.

Mitigation: Install and run only in a sandboxed workspace where those actions are acceptable, and review commands and outputs before execution.

Risk: The security summary reports unsafe helper-script behavior that can execute code, mutate data, or expose credentials.

Mitigation: Avoid untrusted datasets, codebases, archives, and credentials until the reported eval, dynamic import, TAR extraction, SMTP TLS, debug redaction, Git hook, and crypto documentation issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/cogniexec)
- [Command Reference](references/command_reference.md)
- [Security Review Checklist](references/security_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Natural language guidance, Markdown, inline shell commands, code snippets, and generated or modified files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform local file, network, database, Git, archive, image, QR, clipboard, and email actions when the host agent grants tools.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
