## Description: <br>
Runs coding, debugging, or research work in one long-lived ACPX session while a separate supervisor checks engineering evidence until the task is accepted or explicitly failed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[programcaicai](https://clawhub.ai/user/programcaicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run a single ACPX execution session with a low-frequency supervisor that reviews real progress evidence, sends corrections back to the same session, and closes with an accepted or failed outcome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A supervisor loop can continue without useful progress if the task brief lacks acceptance criteria, failure conditions, or evidence paths. <br>
Mitigation: Start only after defining a brief with acceptance criteria, failure conditions, evidence paths, and allowed correction behavior. <br>
Risk: Progress and review files may accidentally capture sensitive information. <br>
Mitigation: Avoid writing secrets into progress or review files, and review evidence paths before sharing reports. <br>
Risk: Supervisor corrections could be sent to the wrong ACPX session. <br>
Mitigation: Confirm the intended ACPX session before sending corrections, and keep all correction prompts directed to the same execution session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/programcaicai/acpx-supervised-execution) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with prompt templates, evidence paths, and review-report structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates one ACPX execution session and one supervisor loop; no hidden code, credentials, or destructive behavior were identified by the provided security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
