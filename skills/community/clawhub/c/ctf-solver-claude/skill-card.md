## Description: <br>
Helps solve capture-the-flag challenges when explicitly invoked by classifying web, pwn, reverse engineering, and misc tasks and producing analysis, commands, code, and exploit steps to recover the flag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hermes186](https://clawhub.ai/user/hermes186) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security learners use this skill for authorized CTF or lab challenges to identify the challenge category, follow the relevant solving workflow, and produce reproducible steps toward flag recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad exploit and credential-capture guidance that could be misused outside an authorized challenge or lab. <br>
Mitigation: Install and run it only for authorized CTF or lab work, and require explicit approval before exploit execution, remote connections, or webhook-based data capture. <br>
Risk: The workflows may install packages, run offensive tooling, execute generated code, or extract untrusted files. <br>
Mitigation: Use a disposable VM or container with no real credentials mounted, and require explicit approval before package installs, command execution, or extraction of untrusted files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hermes186/ctf-solver-claude) <br>
- [CTF Web Reference](references/web.md) <br>
- [CTF PWN Reference](references/pwn.md) <br>
- [CTF Reverse Engineering Reference](references/reverse.md) <br>
- [CTF Misc Reference](references/misc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exploit steps, package installation commands, remote connection commands, and flag recovery notes for authorized CTF or lab use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
