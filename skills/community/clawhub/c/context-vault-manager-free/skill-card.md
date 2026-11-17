## Description: <br>
Context Vault Manager Free helps agents manage short-term, long-term, and important local memory with keyword search, manual summarization, automatic cleanup, and JSON persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to keep long-running conversations and task agents focused by storing memories in short-term, long-term, and important tiers, then retrieving or summarizing relevant context on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memory files may contain sensitive user, customer, or project information. <br>
Mitigation: Avoid storing passwords, secrets, regulated data, or unnecessary customer details; use private storage paths with appropriate file permissions. <br>
Risk: Persisted memories can outlive the session and be reused later in unintended contexts. <br>
Mitigation: Delete or rotate memory files when they are no longer needed, and review stored memories before using them in sensitive workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and JSON persistence parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes add, search, summarize, clear, list, load, and save actions for local memory management.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
