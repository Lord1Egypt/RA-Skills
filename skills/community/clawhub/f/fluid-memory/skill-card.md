## Description: <br>
Fluid Memory adds local OpenClaw memory with ChromaDB recall, decay-based forgetting, and archive controls tied to OpenClaw memory flush events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgaintA](https://clawhub.ai/user/AgaintA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to store, recall, reinforce, forget, and archive local conversation memories across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores conversation content in local plaintext memory files and vector storage. <br>
Mitigation: Enable it deliberately, avoid sending secrets while the hook is active, and protect or periodically clear ~/.openclaw/workspace/database/. <br>
Risk: Scheduled cleanup can eventually delete archived memories. <br>
Mitigation: Run the daemon only when automatic cleanup is intended and keep separate backups for memories that must be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AgaintA/fluid-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text responses, JSON-style tool call arguments, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local plaintext storage under the OpenClaw workspace and does not disclose cloud synchronization.] <br>

## Skill Version(s): <br>
1.0.9 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
