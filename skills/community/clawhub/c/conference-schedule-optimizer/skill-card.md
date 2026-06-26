## Description: <br>
Use when planning conference schedules, optimizing session selection at scientific meetings, managing time between presentations, or maximizing networking at academic conferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Conference attendees, researchers, clinicians, and professional teams use this skill to choose sessions, resolve schedule conflicts, plan networking, and prepare conference follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact documentation includes examples that reference scripts/schedule_optimizer.py, but the release contains scripts/main.py. <br>
Mitigation: Use the included scripts/main.py entry point, or confirm the publisher supplies the referenced schedule_optimizer.py module before execution. <br>
Risk: The CLI reads conference files supplied by the user and can write schedule outputs to a requested path. <br>
Mitigation: Run it only on conference files intended for scheduling and review proposed output paths before writing files. <br>
Risk: The schedule recommendations depend on the completeness and accuracy of user-provided session data and interests. <br>
Mitigation: Review the generated schedule against the official conference program before relying on it for attendance decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and Bash examples; the included CLI prints text and can write optimized schedule JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided conference schedule JSON files and optionally writes a selected output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and tile.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
