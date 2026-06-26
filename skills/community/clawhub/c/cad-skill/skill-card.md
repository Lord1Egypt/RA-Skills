## Description: <br>
Control local CAD applications on Windows including launching apps, opening files, checking status, closing apps, detecting active or running apps, detecting common executable paths, and saving user-provided executable paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doudou459](https://clawhub.ai/user/doudou459) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and workstation users use this skill to automate local Windows CAD application control for SolidWorks, CATIA, Creo, and Siemens NX. It supports launching and closing applications, opening supported CAD files, checking running or active CAD status, detecting executable paths from saved or predefined locations, and storing user-provided executable paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start and force-close local CAD applications, which may interrupt active work. <br>
Mitigation: Save work before using close_app and avoid force=true unless explicitly needed. <br>
Risk: Saved executable paths and alternate configuration files can affect which local programs the skill launches. <br>
Mitigation: Verify saved executable paths yourself and use only configuration files you created and reviewed. <br>


## Reference(s): <br>
- [ClawHub cad-skill page](https://clawhub.ai/doudou459/cad-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON command payloads and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only local workstation automation; commands may launch or close CAD processes and update saved executable path configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
