## Description: <br>
Automatically summarize daily discussions and update memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-11even](https://clawhub.ai/user/mr-11even) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to summarize daily conversation notes into memory files and trigger memory saves on a schedule or after idle periods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automation can edit memory files without an interactive review step. <br>
Mitigation: Review the scripts before installing, back up existing memory files, and enable cron jobs only when automatic edits to OpenClaw memory files are acceptable. <br>
Risk: The heartbeat event handlers can run local workspace scripts outside the reviewed package. <br>
Mitigation: Remove unneeded heartbeat event handlers or change the idle-save path to call the packaged daily-evolution.py script directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mr-11even/auto-memory-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory summaries, JSON reports, and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes OpenClaw workspace memory files when scheduled or idle-triggered.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
