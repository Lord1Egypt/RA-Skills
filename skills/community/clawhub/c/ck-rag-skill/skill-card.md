## Description: <br>
ck-rag-skill queries a RAGFlow knowledge base to answer technical, operations, and troubleshooting questions and return summarized guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenkun-nuaa](https://clawhub.ai/user/chenkun-nuaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to query a configured RAGFlow knowledge base for technical Q&A, Docker/container troubleshooting, system operations guidance, and suggested next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships reusable RAGFlow API credentials and a session cookie. <br>
Mitigation: Rotate or replace the credentials before installation and store secrets outside the skill artifact. <br>
Risk: The skill uses shared conversation state when querying the RAGFlow service. <br>
Mitigation: Use per-user or per-session conversation identifiers and clear sensitive context between sessions. <br>
Risk: Prompts and troubleshooting details are sent to the configured RAGFlow server. <br>
Mitigation: Avoid sensitive prompts until transport, access control, and retention behavior are understood. <br>
Risk: The skill may suggest system commands based on knowledge-base answers. <br>
Mitigation: Inspect suggested commands and require user approval before executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenkun-nuaa/ck-rag-skill) <br>
- [RAGFlow Skill Troubleshooting Guide](artifact/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and knowledge-base references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams responses from a configured RAGFlow API; responses may include cited knowledge-base documents and timing statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
