## Description: <br>
Continuity Framework helps an agent reflect on recent sessions, extract structured memories, generate follow-up questions, and surface them when the user returns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Riley-Coyote](https://clawhub.ai/user/Riley-Coyote) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local continuity workflows to an agent: reflecting on prior sessions, maintaining memory and identity notes, and surfacing pending questions at the start of later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local long-term memory may retain sensitive or unwanted information from session transcripts. <br>
Mitigation: Avoid processing transcripts that contain secrets or sensitive information, and review the configured memory directory regularly. <br>
Risk: Generated questions, identity notes, or reflections may become inaccurate or no longer wanted. <br>
Mitigation: Delete or edit stored questions, identity notes, and reflections when they become inaccurate or unwanted. <br>


## Reference(s): <br>
- [Continuity Framework reference](references/framework.md) <br>
- [ClawHub release page](https://clawhub.ai/Riley-Coyote/continuity-framework) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Console text plus local Markdown and JSON memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CONTINUITY_MEMORY_DIR when set, otherwise writes under ~/clawd/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
