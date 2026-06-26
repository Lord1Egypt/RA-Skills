## Description: <br>
Safe configuration file editing workflow that helps agents back up, edit, diff, validate, and recover configuration files before changes can disrupt a system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucy6692](https://clawhub.ai/user/lucy6692) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill when changing system configuration files, credentials, startup settings, ports, or security-sensitive fields. It guides agents to scope the exact change, make a backup, edit precisely, review diffs, validate JSON, and recover from failed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration edits can expose or mishandle credentials, API keys, or other sensitive values. <br>
Mitigation: Confirm the exact file and values, review diffs carefully, and protect or remove backup files that may contain secrets. <br>
Risk: Startup-critical configuration changes can lock users out or prevent OpenClaw from starting. <br>
Mitigation: Create a dated snapshot for high-risk edits, validate JSON before restart, and restore from the latest backup if startup fails. <br>
Risk: Syntactically valid but semantically wrong configuration can make the system behave unexpectedly. <br>
Mitigation: Scope the intended file, key path, and before/after value before editing, then proceed only when the diff matches the intended change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucy6692/config-safe-edit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; users review diffs and validate configuration files before restart.] <br>

## Skill Version(s): <br>
2.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
