## Description: <br>
Search and install an OpenClaw configuration pack from ClawMart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rxdaozhang](https://clawhub.ai/user/rxdaozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to search ClawMart, review matching configuration packs, download a selected pack, back up conflicting files, and install the pack into the local OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw behavior by installing files from remote ClawMart packs. <br>
Mitigation: Install only packs from trusted publishers, review pack details before confirmation, inspect target paths and downloaded file names when possible, and keep the backup location for recovery. <br>
Risk: The local ClawMart configuration stores an API token. <br>
Mitigation: Treat ~/.openclaw/clawmart-config.json as sensitive and avoid sharing or committing it. <br>


## Reference(s): <br>
- [Clawmart Install on ClawHub](https://clawhub.ai/rxdaozhang/clawmart-install) <br>
- [ClawMart](https://clawmart-gray.vercel.app) <br>
- [ClawMart API Token Dashboard](https://clawmart-gray.vercel.app/dashboard/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with API request examples, JSON configuration snippets, and file installation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw configuration files, skill files, backups, and a local ClawMart API token configuration when the user proceeds.] <br>

## Skill Version(s): <br>
1.2.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
