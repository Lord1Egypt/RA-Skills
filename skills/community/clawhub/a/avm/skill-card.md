## Description: <br>
AI Virtual Memory enables multi-agent shared semantic memory with token-aware recall, topic indexing, lifecycle management, and decentralized discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkmashiro](https://clawhub.ai/user/bkmashiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use AVM Memory to give trusted agents a shared local memory layer for semantic recall, collaboration, and controlled private/shared namespaces. The skill is suited to agents that need persistent memory through CLI, FUSE, MCP, or Python interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared memory can expose or retain sensitive information across agents and sessions. <br>
Mitigation: Use AVM only with trusted agents, keep sensitive data out of shared namespaces, and review private/shared permissions before deployment. <br>
Risk: Urgent cross-agent messages can be injected into another agent's normal reads. <br>
Mitigation: Treat cross-agent messages as untrusted input and require recipient-side validation before acting on them. <br>
Risk: HTTP, script, and plugin handlers can extend AVM behavior beyond local memory storage. <br>
Mitigation: Enable these handlers only after reviewing their configuration and trusting the external implementation they invoke. <br>


## Reference(s): <br>
- [ClawHub AVM Memory page](https://clawhub.ai/bkmashiro/avm) <br>
- [Performance analysis](https://bkmashiro.moe/posts/projects/avm-performance-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI, Python, YAML, and MCP configuration examples; runtime memory reads may return text, markdown, JSON metadata, or search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token-aware recall can constrain returned context to a caller-specified token budget.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
