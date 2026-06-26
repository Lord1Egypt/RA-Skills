## Description: <br>
Persistent semantic memory for AI agents -- local, fast, free. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dannydvm](https://clawhub.ai/user/Dannydvm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Engram to give agents local searchable memory for prior decisions, facts, preferences, relationships, and conversation history across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent local memory, so stored secrets, credentials, regulated data, or confidential conversations may be recalled later or included in exports. <br>
Mitigation: Avoid storing sensitive data unless the deployment owner has approved retention and export behavior; review memory contents before export or reuse. <br>
Risk: The skill depends on the npm package engram-memory and the engram CLI being installed locally. <br>
Mitigation: Review and install the npm dependency from a trusted source before enabling the skill for agent workflows. <br>


## Reference(s): <br>
- [Engram on ClawHub](https://clawhub.ai/Dannydvm/engram-memory) <br>
- [Dannydvm publisher profile](https://clawhub.ai/user/Dannydvm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes the local engram CLI is installed and available on PATH.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
