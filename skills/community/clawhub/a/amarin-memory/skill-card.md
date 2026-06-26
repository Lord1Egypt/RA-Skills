## Description: <br>
Amarin Memory gives agents persistent adaptive memory with temporal decay, semantic deduplication, surprise-based scoring, core memory blocks, and SQLite-backed semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flaggdavid-source](https://clawhub.ai/user/flaggdavid-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs durable memory across sessions, searchable user or task context, persistent identity blocks, and maintenance commands for revising, protecting, or forgetting stored memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-term memories in a local database, so secrets, credentials, regulated data, or sensitive personal details could be retained if an agent stores them. <br>
Mitigation: Only store information intended for long-term retention, and periodically review, revise, protect, or forget memories using the provided maintenance commands. <br>
Risk: Memory content may be sent to the configured embedding service when storing or searching memories. <br>
Mitigation: Keep OLLAMA_URL pointed at a trusted local or private embedding service when privacy matters. <br>
Risk: Passing untrusted memory text directly as shell arguments can create command-line quoting mistakes. <br>
Mitigation: Pipe untrusted content through stdin as shown in the skill instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flaggdavid-source/amarin-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Initializes and uses a local SQLite database at ~/.amarin/agent.db and an embedding service configured by OLLAMA_URL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
