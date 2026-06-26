## Description: <br>
Complete OpenClaw Agent Security Hardening protects against data leaks, prompt injection, unsafe file permissions, sensitive data exposure, Git leaks, and unintended command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingquanagi](https://clawhub.ai/user/qingquanagi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw agent maintainers use this skill to harden agent workspaces, isolate secrets, add Git safeguards, and teach agents to distinguish quoted command text from explicit execution intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some shell snippets can change local files, permissions, Git history, cron configuration, or installed packages. <br>
Mitigation: Review each command before running it, execute commands one at a time, and skip cron, sudo, GPG, or Git history rewrite steps unless they are appropriate for the environment. <br>
Risk: Force-pushing rewritten Git history can disrupt collaborators and does not by itself revoke leaked credentials. <br>
Mitigation: Create backups, coordinate with collaborators, rotate exposed credentials, and verify repository state before using history rewrite commands. <br>
Risk: The security checks are defensive heuristics and may miss secrets, context-specific unsafe permissions, or prompt-injection patterns. <br>
Mitigation: Use the skill as part of a broader review process that includes manual inspection, credential rotation practices, and agent-specific execution controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingquanagi/agent-runtime-security) <br>
- [qingquanagi publisher profile](https://clawhub.ai/user/qingquanagi) <br>
- [OpenClaw security documentation](https://docs.openclaw.ai/security) <br>
- [GPG manual](https://www.gnupg.org/gph/en/manual.html) <br>
- [Semantic Versioning 2.0.0](https://semver.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checklists, command examples, security test cases, and incident response guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and CHANGELOG, released 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
