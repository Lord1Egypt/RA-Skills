## Description: <br>
Install or customize this OpenClaw cyberpunk chat and dream theme. Use when the user wants this exact theme, wants to import it into another workspace, or wants to swap the bundled avatars and background images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasanuowa](https://clawhub.ai/user/kasanuowa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install a cyberpunk visual theme, re-apply it after OpenClaw UI updates, or replace the seven documented avatar and background slots with their own assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer modifies the local OpenClaw Control UI and may apply changes immediately. <br>
Mitigation: Install only when this visual change is intended, keep the generated backups until the theme is confirmed, and use --skip-apply to stage files before modifying the live UI. <br>


## Reference(s): <br>
- [Theme slots](references/theme-slots.md) <br>
- [Theme config example](references/theme-config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install theme files into an OpenClaw workspace and optionally apply them to the live Control UI.] <br>

## Skill Version(s): <br>
1.0.21 (source: server evidence and SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
