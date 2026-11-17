## Description:

CTF-SOLVER helps agents handle authorized capture-the-flag challenges by selecting web, pwn, reverse engineering, or miscellaneous workflows and producing step-by-step solution guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hermes186](https://clawhub.ai/user/hermes186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security learners, and CTF participants use this skill in isolated, authorized CTF environments to analyze challenge artifacts or services and produce solution paths, commands, code snippets, and flag extraction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad exploit and data-exfiltration instructions.

Mitigation: Use it only for isolated, authorized CTF targets and require explicit approval before network access, payload delivery, or callback collection.

Risk: The artifact includes workflows that install tools, execute binaries, and run shell commands.

Mitigation: Run in a sandboxed environment with pinned tools and review commands before execution.

Risk: Some web workflows mention cloud metadata services, real sessions, and out-of-band callbacks.

Mitigation: Block use against real third-party targets, real cloud metadata endpoints, real user sessions, and shared hosts unless separately authorized.

## Reference(s):

- [CTF MISC reference](references/misc.md)
- [CTF PWN reference](references/pwn.md)
- [CTF REVERSE reference](references/reverse.md)
- [CTF WEB reference](references/web.md)
- [Ghidra release referenced by reverse workflow](https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip)
- [phpggc referenced by web workflow](https://github.com/ambionics/phpggc)
- [Vigenere cipher reference tool](https://www.dcode.fr/vigenere-cipher)
- [Hash lookup reference tool](https://crackstation.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable exploit steps, package installation commands, and network testing guidance; review before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
