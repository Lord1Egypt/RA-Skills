## Description: <br>
Organizes mixed task artifacts by workflow stage rather than file type, helping agents plan or clean task directories while handling sensitive files through existing secrets conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-dust](https://clawhub.ai/user/big-dust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and writing or research agents use this skill to plan staged workspace layouts before a multi-step task, or to reorganize an existing task directory so inputs, processing artifacts, verification work, and deliverables remain easy to find. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moving or renaming files during workspace cleanup can break scripts, relative references, or task continuity. <br>
Mitigation: Ask the agent to show the planned directory tree and move or rename list before changes, then verify scripts and important references still resolve. <br>
Risk: Sensitive values could be mishandled if mixed with ordinary task artifacts or shared directories. <br>
Mitigation: Keep any secrets/ area private and excluded from sharing or version control, and leave only non-sensitive references in task directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/big-dust/artifact-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with directory trees, concise rationale, and proposed or executed file organization steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May identify files that should move to an existing private secrets/ area and may summarize items intentionally left unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
