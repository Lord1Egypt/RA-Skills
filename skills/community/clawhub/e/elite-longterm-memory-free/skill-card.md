## Description: <br>
精英长期记忆免费版 helps an AI agent maintain local long-term memory through SESSION-STATE.md, MEMORY.md, and daily memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a local, file-backed memory workflow for AI coding assistants and conversational agents that need to preserve active context, decisions, preferences, and daily notes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files can retain credentials, private personal data, or confidential material across sessions. <br>
Mitigation: Only install the skill when persistent local memory is intended, avoid saving sensitive material unless explicitly required, and periodically review SESSION-STATE.md, MEMORY.md, and the memory/ directory. <br>
Risk: Stale or unnecessary memory entries can continue influencing future agent behavior. <br>
Mitigation: Delete stale entries during periodic memory review and keep the active session state and long-term summary files focused on current, useful context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/elite-longterm-memory-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and local Markdown file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to read and write local memory files, including SESSION-STATE.md, MEMORY.md, and memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
