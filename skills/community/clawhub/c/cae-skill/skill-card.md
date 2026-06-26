## Description: <br>
Control local CAE applications on Windows including launching apps, opening files, checking status, closing apps, detecting active and running apps, detecting common executable paths, and saving user-provided executable paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doudou459](https://clawhub.ai/user/doudou459) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to control supported Windows CAE workstation applications, including Abaqus, Ansys, Ansa, and HyperWorks. It launches applications, opens supported engineering files, checks or closes running applications, detects active CAE tools, and manages saved executable paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The close_app action can force-close local engineering applications and may cause loss of unsaved work. <br>
Mitigation: Save work before closing applications and require explicit user confirmation before any forced close. <br>
Risk: Abaqus .py and .jnl files may execute scripts when opened. <br>
Mitigation: Open only trusted Abaqus script or journal files from known sources. <br>
Risk: Saved executable paths determine which local program is launched. <br>
Mitigation: Save only trusted executable paths and review configured paths before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doudou459/cae-skill) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON action results with local application side effects for launch, open, close, status, path detection, and path configuration actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on Windows for supported CAE applications and uses saved or predefined executable paths instead of broad filesystem or registry scanning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
