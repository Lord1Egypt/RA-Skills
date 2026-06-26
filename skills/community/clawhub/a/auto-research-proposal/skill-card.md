## Description: <br>
Multi-agent research war room where personas debate research ideas and draft proposals through ideation and proposal-writing phases with persona persistence and drift detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankaging](https://clawhub.ai/user/frankaging) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and research teams use this skill to run structured persona-based debate, converge on a research idea, and draft a concise research proposal with logs, snapshots, and checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may launch a local terminal monitor and read project memory files in real time. <br>
Mitigation: Ask the agent to confirm before starting the monitor and verify that the monitor path resolves to this reviewed package. <br>
Risk: The skill persistently records detailed discussion logs, persona memos, checkpoints, and result copies that may contain sensitive unpublished research. <br>
Mitigation: Avoid putting secrets or sensitive unpublished material in the discussion, and delete memory/war-room, memory/.private, checkpoints, and results copies when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankaging/auto-research-proposal) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Persona configuration](artifact/personas/agents.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists discussion logs, private persona memos, checkpoints, idea snapshots, proposal drafts, and copied results in the active project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
