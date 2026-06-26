## Description: <br>
Codex Sessions Manager helps agents inspect, search, export, verify, clean up, delete, restore, and purge local Codex sessions stored under a Codex root such as ~/.codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1939869736luosi](https://clawhub.ai/user/1939869736luosi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage local Codex conversation history safely, including listing, filtering, exporting, deleting, trashing, restoring, purging, verifying, and diagnosing sessions. It is intended for local Codex roots and not for generic chat history or the current live conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and export local Codex session history, which may contain sensitive private conversation data. <br>
Mitigation: Treat displayed and exported sessions as sensitive data, avoid printing chat content in diagnostics, and share exports only with trusted recipients. <br>
Risk: Delete, restore, purge, and cleanup operations can modify or remove local Codex session storage. <br>
Mitigation: Use preview or diagnostic mode first, verify the selected root and session IDs, require explicit confirmation for write operations, and prefer recoverable trash over permanent deletion. <br>
Risk: Side conversations can be stored as separate child sessions, so parent-session actions may not cover all related transcripts. <br>
Mitigation: Identify parent and child session IDs before export, delete, trash, restore, purge, or verification, and preview the complete selected set before confirming writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1939869736luosi/codex-sessions-manager) <br>
- [README.md](README.md) <br>
- [Safety Guide](docs/SAFETY.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [npm package](https://www.npmjs.com/package/codex-sessions-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MCP tool calls or CLI commands; destructive operations require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
