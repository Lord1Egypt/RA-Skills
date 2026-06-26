## Description: <br>
List, inspect, and watch local OpenAI Codex sessions from the CLI or VS Code using the CodexMonitor Homebrew formula. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate CodexMonitor for browsing, inspecting, watching, and resuming local Codex session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Codex session logs may contain sensitive prompts, outputs, paths, or other private session content. <br>
Mitigation: Install only from a trusted Homebrew source, prefer specific session IDs or scoped CODEX_SESSIONS_DIR values, and avoid exposing displayed session content unnecessarily. <br>
Risk: The resume command can append new content to an existing Codex session. <br>
Mitigation: Use resume only when intentionally continuing that session and confirm the target session ID before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/codexmonitor) <br>
- [CodexMonitor homepage](https://github.com/Cocoanetics/CodexMonitor) <br>
- [Setup instructions](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; codexmonitor output can be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Homebrew, the codexmonitor binary, and readable local Codex session logs.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
