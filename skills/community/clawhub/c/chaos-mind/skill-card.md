## Description: <br>
Chaos Mind is a hybrid local memory system for AI agents that supports manual search and storage, with optional opt-in transcript capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hargabyte](https://clawhub.ai/user/hargabyte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use Chaos Mind to search, store, and retrieve local project memories across decisions, facts, research findings, and session-derived context. Teams can optionally enable local auto-capture after configuring transcript paths and privacy controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation uses local shell scripts and release artifacts that can affect the user's machine. <br>
Mitigation: Review install.sh locally before installation, avoid curl-to-shell workflows, and verify release artifacts when possible. <br>
Risk: Optional auto-capture can read configured transcript paths and may process sensitive session content if paths are too broad. <br>
Mitigation: Keep auto-capture disabled until needed, configure only narrow transcript paths, exclude secrets or regulated data, and test with one-shot or dry-run workflows before running continuously. <br>
Risk: Captured memories are stored in a local database that users must protect and audit. <br>
Mitigation: Use appropriate filesystem permissions or disk encryption, review the local ~/.chaos database and logs, and understand how to stop nohup or systemd capture before enabling background operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hargabyte/chaos-mind) <br>
- [Project documentation](https://github.com/hargabyte/Chaos-mind#readme) <br>
- [Security policy](https://github.com/hargabyte/Chaos-mind/blob/main/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI workflows, local configuration paths, privacy guidance, and troubleshooting steps for agent memory operations.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
