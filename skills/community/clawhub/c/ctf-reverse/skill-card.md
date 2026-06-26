## Description: <br>
Provides reverse-engineering reference workflows and tool guidance for CTF challenges involving binaries, bytecode, mobile apps, firmware, custom VMs, anti-analysis, and game clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security practitioners, and CTF participants use this skill to choose reverse-engineering techniques, tools, and analysis workflows for authorized competition or lab binaries and related artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill includes under-scoped operational instructions for impersonation, bypasses, data retrieval, and cyber-physical actions. <br>
Mitigation: Use only for authorized CTFs or controlled lab reverse engineering, and do not apply vehicle/CAN, anti-cheat, iOS, Firebase, or C2 examples to real systems without explicit authorization. <br>
Risk: The security guidance flags unpinned tool installs as a supply-chain risk. <br>
Mitigation: Install and run tools in an isolated VM or container, pin and review dependencies where practical, and scan downloaded tooling before use. <br>
Risk: Reverse-engineering workflows may involve private, proprietary, or sensitive binaries. <br>
Mitigation: Avoid uploading private binaries to third-party services and keep analysis artifacts in controlled environments. <br>


## Reference(s): <br>
- [Ctf Reverse ClawHub Release](https://clawhub.ai/gandli/ctf-reverse) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [tools.md](artifact/tools.md) <br>
- [tools-dynamic.md](artifact/tools-dynamic.md) <br>
- [tools-advanced.md](artifact/tools-advanced.md) <br>
- [anti-analysis.md](artifact/anti-analysis.md) <br>
- [patterns.md](artifact/patterns.md) <br>
- [patterns-ctf.md](artifact/patterns-ctf.md) <br>
- [patterns-ctf-2.md](artifact/patterns-ctf-2.md) <br>
- [patterns-ctf-3.md](artifact/patterns-ctf-3.md) <br>
- [languages.md](artifact/languages.md) <br>
- [languages-platforms.md](artifact/languages-platforms.md) <br>
- [languages-compiled.md](artifact/languages-compiled.md) <br>
- [platforms.md](artifact/platforms.md) <br>
- [platforms-hardware.md](artifact/platforms-hardware.md) <br>
- [pycdc](https://github.com/zrax/pycdc) <br>
- [pwndbg](https://github.com/pwndbg/pwndbg) <br>
- [Blutter](https://github.com/worawit/blutter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reference guidance for an agent; it does not itself execute tools unless the supervising agent follows the suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
