## Description: <br>
Retrieve and track technicians' real-time GPS location, find the nearest technician, calculate distance and ETA, and create geofences for job monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[comphone](https://clawhub.ai/user/comphone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Dispatch and operations staff use this skill to query technician vehicle locations, choose a nearby technician for a job, and estimate travel distance and arrival time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive technician location access and evidence.security reports bundled credentials, weak transport claims, and limited authorization guidance. <br>
Mitigation: Install only with authorization to track technicians; rotate or remove bundled credentials, store secrets outside skill files, disable HTTP fallback URLs, and add access controls, consent or notice, audit logging, and limits on location precision and retention before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/comphone/aika-gps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-style command results and Python integration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return technician location, distance, ETA, geofence, or error information depending on the command and available GPS data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
