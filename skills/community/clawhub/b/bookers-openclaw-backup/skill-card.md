## Description: <br>
Create, inspect, configure, and restore self-contained backup bundles for ~/.openclaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silronin](https://clawhub.ai/user/silronin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local full-state backups of ~/.openclaw, list existing backup bundles, adjust snapshot storage settings, and perform guarded restores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain agent configuration, installed skills, and local OpenClaw state. <br>
Mitigation: Treat generated backup archives as sensitive local files and store or share them only according to the user's data handling requirements. <br>
Risk: Restoring a bundle can replace local OpenClaw state at the selected target path. <br>
Mitigation: Confirm the restore target path before running restore commands and keep a separate recovery backup. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated local tar.gz backup bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local OpenClaw snapshot archives, manifests, checksums, and restore commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
