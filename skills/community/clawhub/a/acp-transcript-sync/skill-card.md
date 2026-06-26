## Description: <br>
ACP Transcript Sync copies completed ACP child-session transcript content into a main OpenClaw session transcript so downstream collection can capture the full sub-agent work history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steflerjiang](https://clawhub.ai/user/steflerjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after spawning ACP sub-agents to merge child-session reasoning and replies into the main session transcript. It is intended for workflows where another platform reads the main transcript as the record of work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child-session transcripts may contain secrets, private data, or sensitive reasoning that becomes visible in the main session log after synchronization. <br>
Mitigation: Inspect the child transcript before write-back and use the skill only when that content is intended to be copied into systems that read the main transcript. <br>
Risk: Automatic main-session detection can append transcript content to the wrong session in multi-session environments. <br>
Mitigation: Prefer passing explicit main_session_id and main_agent values, then verify the main transcript after synchronization. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes JSONL transcript entries to a local OpenClaw session file when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
