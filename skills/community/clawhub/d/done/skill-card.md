## Description: <br>
Automatically extracts ZIP-packaged skills and installs them into WSL2 and Windows desktop skill folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aetik-yue](https://clawhub.ai/user/Aetik-yue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Done to install ZIP-packaged skills into a WSL2 OpenClaw workspace and copy a backup to a Windows desktop skills folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace existing OpenClaw skills during installation. <br>
Mitigation: Keep backups of installed skills and review the target skill name before allowing replacement. <br>
Risk: A ZIP package with an unsafe skill name may write outside the intended skill area. <br>
Mitigation: Inspect the archive's SKILL.md before installation and only install ZIP files from trusted sources. <br>
Risk: The Windows desktop backup path is hard-coded for a specific user path. <br>
Mitigation: Use only on systems where that path is appropriate or adjust the path before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Aetik-yue/done) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown-style progress messages with filesystem paths and status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs files into local WSL2 and Windows desktop skill directories and may overwrite existing skill folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
