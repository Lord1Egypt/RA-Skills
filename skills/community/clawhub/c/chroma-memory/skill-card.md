## Description: <br>
Stores and semantically retrieves per-turn customer conversation data with auto-tagging and customer isolation using ChromaDB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-facing sales and support agents use this skill to persist and retrieve conversation turns, quotes, commitments, objections, orders, sample requests, and CRM snapshots across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores sensitive customer conversations, identifiers, and CRM snapshots for later recall. <br>
Mitigation: Use it with real customer data only after confirming storage location, file access controls, consent requirements, retention limits, and deletion procedures. <br>
Risk: Automatic memory capture can retain more customer context than intended. <br>
Mitigation: Disable or limit automatic memory capture where appropriate, and review stored records before enabling the workflow for production customer interactions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ipythoning/chroma-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples; runtime commands print text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local per-customer memory records and CRM snapshot records for later recall.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
