## Description: <br>
Automatically extract key facts from conversation history and persist to local memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobu2020](https://clawhub.ai/user/xiaobu2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan recent conversation history, extract memorable facts, classify them, and persist them into local memory/profile files for future agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently retain private chat details in local memory and profile files. <br>
Mitigation: Use dry-run first, review extracted facts before enabling automatic hooks, and define deletion, backup, and sensitive-data handling rules before use on private conversations. <br>
Risk: Persisted conversation text may influence future agent behavior through memory or tool-instruction files. <br>
Mitigation: Disable or tightly review writes to TOOLS.md and other behavior-shaping files, and audit saved facts for accuracy before relying on them. <br>


## Reference(s): <br>
- [Conversation Saver ClawHub release](https://clawhub.ai/xiaobu2020/conversation-saver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode to preview extracted facts before writing local files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
