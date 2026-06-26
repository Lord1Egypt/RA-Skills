## Description: <br>
Prioritize vulnerability remediation using KEV-style exploitation context plus asset criticality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security teams and vulnerability managers use this skill to rank CVEs by exploitation context, CVSS score, and affected asset criticality, then produce patch-priority and due-window guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads the local vulnerability JSON file selected by the user. <br>
Mitigation: Use only intended input files and avoid including unnecessary sensitive asset or vulnerability data. <br>
Risk: The helper writes a local report file and may overwrite an existing path chosen with --output. <br>
Mitigation: Write reports to a dedicated output directory and avoid pointing --output at important files. <br>
Risk: The --dry-run flag is recorded in output details but does not prevent report file creation. <br>
Mitigation: Do not rely on --dry-run as a safeguard against file writes; choose a disposable output path when testing. <br>


## Reference(s): <br>
- [KEV Triage Method](references/triage-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON, CSV] <br>
**Output Format:** [Markdown guidance with optional JSON, Markdown, or CSV report files from the bundled triage script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script accepts a local JSON vulnerability input file and writes a selected local report artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
