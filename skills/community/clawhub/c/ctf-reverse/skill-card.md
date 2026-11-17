## Description:

Provides reverse engineering techniques and tool workflows for CTF challenges involving binaries, obfuscation, custom VMs, anti-analysis, bytecode, mobile apps, firmware, and game clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill as a quick-reference for authorized CTF reverse engineering tasks, including static and dynamic binary analysis, deobfuscation, emulation, symbolic execution, and flag extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes bypass, patching, remote installation, and binary instrumentation workflows that can be misused outside a CTF or lab setting.

Mitigation: Use only in isolated lab or CTF environments and only against targets the user owns or is explicitly authorized to analyze.

Risk: Tool installation and setup examples can introduce supply-chain risk, especially when cloning or installing external tools.

Mitigation: Pin and verify tool installs, avoid curl-to-bash patterns, and do not run setup commands as root unless necessary.

Risk: Some workflows may involve uploading or processing binaries with third-party services or tools.

Mitigation: Do not upload proprietary, confidential, or sensitive binaries to external services without informed approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gandli/skills/ctf-reverse)
- [Static Analysis Tools](tools.md)
- [Dynamic Analysis Tools](tools-dynamic.md)
- [Advanced Tools](tools-advanced.md)
- [Anti-Analysis Techniques](anti-analysis.md)
- [Patterns and Techniques](patterns.md)
- [Competition Patterns Part 1](patterns-ctf.md)
- [Competition Patterns Part 2](patterns-ctf-2.md)
- [Competition Patterns Part 3](patterns-ctf-3.md)
- [Language-Specific Techniques](languages.md)
- [Platform and Framework Techniques](languages-platforms.md)
- [Compiled Language Reversing](languages-compiled.md)
- [Platform-Specific Reversing](platforms.md)
- [Hardware and Architecture Reversing](platforms-hardware.md)
- [pycdc](https://github.com/zrax/pycdc)
- [pwndbg](https://github.com/pwndbg/pwndbg)
- [Blutter](https://github.com/worawit/blutter)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash, Python, and tool-command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose tool installation, binary-analysis, patching, hooking, emulation, and symbolic-execution commands for authorized CTF or lab targets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
