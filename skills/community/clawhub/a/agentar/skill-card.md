## Description: <br>
Export and import AI agent avatar (aka agentar) instances as portable .claw packages for backup, sharing, and migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rwonly](https://clawhub.ai/user/rwonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to export, import, back up, share, and roll back AI agent workspaces and configuration as portable .claw packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported .claw packages can persistently change OpenClaw workspace, configuration, and installed skills. <br>
Mitigation: Use packages only from trusted sources, run the documented dry-run preview before import, inspect conflicts and bundled skills, and keep automatic backups enabled so rollback remains available. <br>
Risk: The submitted artifact describes credential stripping and backup behavior but does not include the implementation that performs those actions. <br>
Mitigation: Verify exports before sharing, prefer local package files over URLs, and review package contents and dry-run output before installing. <br>


## Reference(s): <br>
- [Agentar homepage](https://agentar.site) <br>
- [ClawHub skill page](https://clawhub.ai/rwonly/agentar) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agentar CLI; import and rollback workflows may modify OpenClaw state and should be previewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
