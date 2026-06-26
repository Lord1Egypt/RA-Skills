## Description: <br>
Advanced Collab Protocol defines collaboration rules for OpenClaw multi-agent pipelines, including file handoffs, routing envelopes, precision mentions, acknowledgments, and loop-prevention behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libaie](https://clawhub.ai/user/libaie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate OpenClaw multi-agent pipeline work across private handoffs and group channels. It helps agents exchange shared-file references, route status messages, avoid generic mentions, and terminate collaboration flows clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct agents to retrieve upstream private chat history or thought process when context is insufficient. <br>
Mitigation: Disable sessions_history by default, or require explicit user or administrator approval with narrow session scope and logging before production use. <br>
Risk: Cross-agent messaging and shared handoff files can expose task content to unintended agents or channels. <br>
Mitigation: Use least-privilege tool grants, explicit agent-to-agent allowlists, a constrained shared directory, and audit logs for routed messages and handoff files. <br>
Risk: Reading OpenClaw routing configuration can expose identity mappings beyond the immediate handoff need. <br>
Mitigation: Permit configuration reads only for identity mapping, restrict access to the required route data, and log those reads. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with structured chat and handoff message patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce shared handoff file paths, routing envelopes, acknowledgments, errors, and finish messages.] <br>

## Skill Version(s): <br>
1.4.1 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
