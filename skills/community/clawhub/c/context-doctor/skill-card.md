## Description: <br>
Visualize and diagnose OpenClaw context window usage with a breakdown of workspace files, installed skills, and bootstrap token budget allocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzOcb](https://clawhub.ai/user/jzOcb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect OpenClaw context window health, diagnose token-budget pressure, and identify missing or oversized bootstrap files after workspace changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may reveal local workspace paths, installed skill names, and the presence or size of personal context files when shared. <br>
Mitigation: Review terminal, JSON, PNG, and SVG outputs before sharing them outside the local workspace. <br>
Risk: Generated PNG, SVG, or JSON files can persist diagnostic details on disk. <br>
Mitigation: Write exports to an intended location and remove them when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, PNG image, shell commands, guidance] <br>
**Output Format:** [Terminal report, concise text summary, structured JSON, or PNG image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local workspace paths, installed skill names, file statuses, character counts, token estimates, and context budget percentages.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
