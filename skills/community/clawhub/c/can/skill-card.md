## Description: <br>
Agent and MCP integration for stamping tool outputs with a timestamp, content hash, and local name so agents can verify, recall, and log them locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xccx](https://clawhub.ai/user/xccx) <br>

### License/Terms of Use: <br>
Public Domain <br>


## Use Case: <br>
External developers and agent builders use this skill to add a local timestamp, SHA-256 content hash, and human-readable label to MCP or tool outputs so agents can verify and recall prior results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CAN logging can leave persistent local records or cached tool outputs on the user's machine, including sensitive MCP or API results if the agent logs them. <br>
Mitigation: Treat ~/.can as persistent local memory; avoid logging secrets, credentials, personal data, or sensitive tool results unless retention is intended and the directory can be protected or deleted later. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xccx/can) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell utilities sha256sum and date when applying the described CAN workflow.] <br>

## Skill Version(s): <br>
1.9.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
