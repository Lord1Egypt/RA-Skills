## Description:

Provides binary exploitation reference guidance for CTF pwn challenges, including overflow, ROP, heap, format string, sandbox, Windows, and Linux kernel techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security practitioners, and CTF participants use this skill for authorized binary exploitation challenge analysis and exploit-development workflows in controlled lab environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational exploitation guidance could be misused against systems outside the intended CTF context.

Mitigation: Restrict use to authorized CTF targets or disposable lab systems and require explicit authorization before network or exploit execution.

Risk: Examples include reverse-shell, privilege-escalation, data-exfiltration, and system-file modification patterns.

Mitigation: Run only inside an isolated VM or container without personal files, production credentials, or access to production networks.

Risk: Package installation and shell-command snippets may alter the local environment.

Mitigation: Review all installs and commands before execution and prefer throwaway environments for tool setup.

## Reference(s):

- [ClawHub ctf-pwn skill page](https://clawhub.ai/gandli/skills/ctf-pwn)
- [overflow-basics.md](artifact/overflow-basics.md)
- [rop-and-shellcode.md](artifact/rop-and-shellcode.md)
- [rop-advanced.md](artifact/rop-advanced.md)
- [format-string.md](artifact/format-string.md)
- [heap-techniques.md](artifact/heap-techniques.md)
- [advanced.md](artifact/advanced.md)
- [advanced-exploits.md](artifact/advanced-exploits.md)
- [advanced-exploits-2.md](artifact/advanced-exploits-2.md)
- [advanced-exploits-3.md](artifact/advanced-exploits-3.md)
- [advanced-exploits-4.md](artifact/advanced-exploits-4.md)
- [sandbox-escape.md](artifact/sandbox-escape.md)
- [kernel.md](artifact/kernel.md)
- [kernel-techniques.md](artifact/kernel-techniques.md)
- [kernel-bypass.md](artifact/kernel-bypass.md)
- [pwndbg](https://github.com/pwndbg/pwndbg)
- [libc.blukat.me](https://libc.blukat.me/)
- [libc.rip](https://libc.rip/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference guidance and example commands for agent-assisted CTF exploitation workflows; agent execution should be gated by human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
