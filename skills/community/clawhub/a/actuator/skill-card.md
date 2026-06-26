## Description: <br>
Actuator is advertised as an actuator selection and sizing calculator, but security review identifies the artifact as a local data manager for storing, searching, deleting, and exporting user-entered records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers can use this skill as a shell-based local record manager for adding, listing, searching, deleting, and exporting user-entered entries. The advertised actuator sizing purpose should be verified before relying on the skill for engineering calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as an actuator sizing calculator, but security evidence says the artifact behaves as a local data manager. <br>
Mitigation: Review the function before installing and do not rely on it for actuator sizing decisions without independent validation. <br>
Risk: User-entered records are stored locally in JSONL under ~/.actuator by default and can be exported to files. <br>
Mitigation: Avoid entering sensitive engineering, business, or operational data; set ACTUATOR_DIR to a controlled location when testing. <br>
Risk: Records can be deleted by line number. <br>
Mitigation: Back up data before using remove operations or test with disposable data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/actuator) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Structured stdout text, JSONL records, and optional JSON or CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data under ~/.actuator by default; ACTUATOR_DIR can override the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
