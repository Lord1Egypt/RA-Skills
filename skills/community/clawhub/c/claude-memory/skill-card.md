## Description: <br>
Structured memory system for OpenClaw agents with a 4-type classification, layered memory files, write rules, and heartbeat maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiji-z](https://clawhub.ai/user/kaiji-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to set up and maintain a structured persistent memory system for OpenClaw agents. It provides templates, write rules, reference guidance, and a setup script for long-term memory, feedback, topic notes, and heartbeat maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain personal information, secrets, or sensitive third-party data longer than intended. <br>
Mitigation: Install only in a private workspace where persistent memory is desired, avoid saving secrets or sensitive third-party data, and review memory files regularly. <br>
Risk: Loading MEMORY.md in shared or group-chat contexts can expose private user context. <br>
Mitigation: Follow the skill guidance to load MEMORY.md only in direct sessions and keep shared contexts from reading private memory files. <br>
Risk: The setup script creates memory files in the provided workspace path, which could place persistent notes in an unintended location. <br>
Mitigation: Run the initializer only against the intended private workspace and review the generated files before relying on them. <br>


## Reference(s): <br>
- [AGENTS.md memory rules](references/agents-rules.md) <br>
- [Encoding notes](references/encoding-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes templates for MEMORY.md, memory/feedback.md, daily notes, and memory/topics/.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
