## Description: <br>
Manage multiple OpenAI Codex accounts by capturing current login tokens, switching between saved accounts, and auto-selecting the best one based on quota budget scoring; it can also explicitly sync saved Codex tokens into OpenClaw agent auth stores on this machine and reads and writes local authentication files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to save, switch, compare, and auto-select local Codex account tokens, with optional explicit syncing to OpenClaw agent auth stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local Codex access and refresh tokens, including saved account snapshots. <br>
Mitigation: Review the script before installation and keep ~/.codex authentication files private with restrictive file permissions. <br>
Risk: Server security evidence notes that the tool may save active Codex credentials during normal account operations. <br>
Mitigation: Install only when credential snapshot behavior is acceptable and inspect saved accounts after use. <br>
Risk: OpenClaw token propagation can write saved Codex tokens into agent auth stores. <br>
Mitigation: Use explicit sync only when needed, prefer sync --dry-run first, and use --agent to limit which OpenClaw agents are updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/codex-account-switcher) <br>
- [Setup instructions](SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local Codex and OpenClaw authentication files when the user runs the provided script.] <br>

## Skill Version(s): <br>
1.4.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
