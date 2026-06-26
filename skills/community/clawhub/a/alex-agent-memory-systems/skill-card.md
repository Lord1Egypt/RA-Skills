## Description: <br>
This skill guides agents through memory architecture for intelligent agents, including short-term memory, long-term memory, and retrieval strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shendingyi](https://clawhub.ai/user/shendingyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design memory systems and choose memory types, vector stores, chunking, and retrieval strategies for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory-system guidance may be applied to private documents, vector stores, or credentials through separate connectors. <br>
Mitigation: Review any separate connector or memory-writing skill before granting access to private data stores or credentials. <br>
Risk: Poor chunking, filtering, or retrieval choices can cause agents to miss, surface stale, or surface conflicting memories. <br>
Mitigation: Test retrieval quality with representative data and use metadata filtering, temporal scoring, and conflict handling before production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or storage connector output; recommendations should be reviewed before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
