## Description:

Helps agents work through authorized CTF web exploitation, reverse engineering, and source audit tasks using focused workflows for HTTP vulnerabilities, Ghidra headless analysis, and semgrep review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security practitioners, and CTF competitors use this skill to triage web challenges, reverse binaries, and audit source code in authorized lab or competition environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes highly actionable exploitation and credential-access guidance.

Mitigation: Use it only in authorized CTF, lab, or owned environments with an explicit testing boundary.

Risk: Commands may involve network exploitation, cloud metadata probing, reverse shells, webshells, or remote tool installers.

Mitigation: Run work in a disposable VM or container, avoid mounted secrets, and inspect or pin downloaded tooling before execution.

Risk: The security review found insufficient authorization and containment boundaries in the artifact text.

Mitigation: Require human review of proposed actions before executing commands against any target.

## Reference(s):

- [CTF Web Exploitation](references/ctf-web/SKILL.md)
- [CTF Reverse Engineering](references/ctf-reverse/SKILL.md)
- [Security Arsenal](references/security-arsenal/SKILL.md)
- [SQL Injection Notes](references/ctf-web/sql-injection.md)
- [Server-Side Web Notes](references/ctf-web/server-side.md)
- [Client-Side Web Notes](references/ctf-web/client-side.md)
- [JWT and Auth Notes](references/ctf-web/auth-jwt.md)
- [Reverse Engineering Tools](references/ctf-reverse/tools.md)
- [Reverse Engineering Field Notes](references/ctf-reverse/field-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/yxy050208/skills/ctf-web-reverse-audit)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose security testing commands, payloads, and tool setup steps for authorized challenge environments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
