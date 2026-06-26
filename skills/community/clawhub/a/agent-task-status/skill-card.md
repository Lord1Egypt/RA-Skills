## Description: <br>
Verify whether named OpenClaw agents actually received formal task assignments and replied with execution status, using transcript-backed audit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujohn74](https://clawhub.ai/user/lujohn74) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw agent delegation by checking transcript-backed assignments, replies, task status, results, and risks for selected agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Status output may include task details, report text, risk notes, and local transcript paths from agent sessions. <br>
Mitigation: Run it only in OpenClaw environments whose transcripts you intend to audit, prefer explicit agent lists, choose the transcript base carefully, and treat terminal or saved output as sensitive. <br>


## Reference(s): <br>
- [Usage](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output can be table, summary, JSON, or JSONL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session indexes and transcript files only when the user runs the bundled script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
