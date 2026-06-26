## Description: <br>
This skill guides an agent through a five-step communication loop of listening, thinking, saying, doing, and reviewing to make reasoning, execution, and lessons learned more transparent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to structure replies and collaborative work through listening, thinking, saying, doing, and reviewing. It is most useful when the user wants assumptions, chosen actions, command results, and reflections to be visible before the next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow encourages saving decisions, execution results, and reflections to memory or knowledge stores, which may capture sensitive work details. <br>
Mitigation: Confirm whether memory, Obsidian, ChromaDB, or web tools are enabled before use, and require redaction or explicit confirmation before saving secrets, credentials, confidential command output, regulated data, or sensitive business information. <br>
Risk: The skill can ask the agent to show commands and results, which may expose private paths, environment details, or confidential output. <br>
Mitigation: Review command output before preserving or sharing it, and redact sensitive values from logs, terminal output, and review notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markma84/five-steps-to-wisdom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured five-step sections and optional inline command/result blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include decision rationale, execution results, review notes, and wiki-style knowledge links when relevant.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
