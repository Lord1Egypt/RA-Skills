## Description: <br>
Archives older daily memory notes into month folders to keep active memory lean and reduce prompt token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x3r081](https://clawhub.ai/user/x3r081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to archive older local memory notes into month-based folders, reducing active memory clutter and prompt token overhead while keeping archived notes accessible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real run moves matching local memory notes out of the active memory directory. <br>
Mitigation: Run with --dry-run first and confirm the memory directory, cutoff month, and proposed moves before executing changes. <br>
Risk: An existing archived file with the same name can be replaced during archiving. <br>
Mitigation: Back up important notes or inspect the archive folder before a real run when filename collisions are possible. <br>


## Reference(s): <br>
- [Agent Memory Optimizer on ClawHub](https://clawhub.ai/x3r081/agent-memory-optimizer) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file operations only; dry-run preview available] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
