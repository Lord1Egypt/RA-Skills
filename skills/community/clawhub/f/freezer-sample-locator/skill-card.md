## Description: <br>
Track and retrieve sample locations in -80°C freezers using hierarchical storage coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab operations staff, researchers, and automation agents use this skill to record, search, update, delete, and export freezer sample inventory records by sample metadata and storage coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python script creates and modifies a local sample inventory database. <br>
Mitigation: Run it only in an intended workspace, keep backups of the data directory, and review changes before relying on inventory records. <br>
Risk: Export paths can write files to arbitrary writable locations. <br>
Mitigation: Use explicit export paths in approved directories and avoid overwriting existing files without review. <br>
Risk: Sample names, notes, and project fields may contain sensitive lab information. <br>
Mitigation: Store the data directory in a protected location and avoid adding sensitive notes unless access controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/freezer-sample-locator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local JSON inventory data and export CSV files when the bundled script is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
