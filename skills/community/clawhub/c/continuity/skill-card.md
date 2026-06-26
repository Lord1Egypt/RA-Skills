## Description: <br>
Continuity Framework supports asynchronous reflection and memory integration by extracting structured memories, generating follow-up questions, and surfacing them when the user returns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Riley-Coyote](https://clawhub.ai/user/Riley-Coyote) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add post-session reflection, local memory integration, and pending-question surfacing to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally stores reflection questions, identity notes, and conversation-derived continuity data on local disk. <br>
Mitigation: Review the configured memory directory, avoid running reflection on conversations that should not be retained, and enable heartbeat reflection only when background post-session processing is acceptable. <br>


## Reference(s): <br>
- [Continuity Framework Reference](references/framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with Markdown memory files and JSON reflection logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local continuity files under the configured CONTINUITY_MEMORY_DIR.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
