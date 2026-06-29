## Description: <br>
Give a Node.js agent durable, local-first memory plus a queryable SPARQL knowledge graph backed by CortexDB through its gRPC sidecar and the cortexdb-client npm package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliang-cn](https://clawhub.ai/user/liliang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add durable local memory, semantic recall, knowledge storage, and SPARQL-backed graph querying to Node.js agents such as OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent store long-term local memory, which may persist sensitive or personal information across sessions. <br>
Mitigation: Avoid storing secrets or sensitive personal data, scope memories deliberately, and confirm you can inspect or delete the CortexDB database file. <br>
Risk: The CortexDB gRPC endpoint uses a bearer token and is described for localhost use. <br>
Mitigation: Use a real sidecar token, keep the endpoint local by default, and add transport security before any cross-machine deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liliang-cn/cortexdb-agent-memory) <br>
- [CortexDB client npm package](https://www.npmjs.com/package/cortexdb-client) <br>
- [CortexDB project documentation](https://github.com/liliang-cn/cortexdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reusable Node.js helper functions for memory, recall, knowledge search, relation storage, and SPARQL graph queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
