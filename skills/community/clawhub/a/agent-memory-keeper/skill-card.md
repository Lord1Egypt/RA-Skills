## Description: <br>
Agent Memory Keeper helps OpenClaw agents review conversations, record important user and project context into local long-term memory files, and search those notes in later sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-jin-xuan](https://clawhub.ai/user/li-jin-xuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, teams, and personal-assistant users use this skill to give OpenClaw agents a local memory workflow for capturing preferences, project decisions, feedback, and reusable knowledge across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to preserve personal and project details in long-term local memory without clear consent or sensitivity limits. <br>
Mitigation: Set explicit rules before use that prohibit storing secrets, credentials, health, financial, legal, or other sensitive personal information, and periodically inspect and delete MEMORY.md, USER.md, and memory directory entries. <br>


## Reference(s): <br>
- [Memory Rules](references/memory-rules.md) <br>
- [Review Template](references/review-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local note-taking and search workflows for MEMORY.md, USER.md, and the memory directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
