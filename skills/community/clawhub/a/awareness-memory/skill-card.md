## Description: <br>
Persistent memory across sessions that automatically recalls past decisions, code, and tasks before each prompt, saves session checkpoints, and provides manual Bash tools for searching, recording, and querying memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwin-hao-ai](https://clawhub.ai/user/edwin-hao-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to recall prior decisions, code context, tasks, and knowledge across sessions, then record meaningful work back to memory. It supports automatic hooks plus manual Bash commands for search, lookup, import, setup, and recording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text, memory records, and prior memory or session snippets may be stored locally or sent to the Awareness API when cloud credentials are configured. <br>
Mitigation: Use the skill only in workspaces where that data flow is acceptable, and prefer an explicitly started local daemon for sensitive work. <br>
Risk: The skill persists API credentials and may write environment variables to a shell profile during setup. <br>
Mitigation: Review credential storage after setup and remove shell-profile or global OpenClaw credential writes if broad persistence is not desired. <br>
Risk: The skill automatically starts services, initiates cloud authentication, and can import past OpenClaw history. <br>
Mitigation: Review the artifact and security guidance before installation, especially in sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwin-hao-ai/awareness-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/edwin-hao-ai) <br>
- [Release Changelog](artifact/CHANGELOG.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Bash commands, XML recall blocks, and JSON-compatible memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and stores credentials in the user's Awareness configuration when cloud mode is configured.] <br>

## Skill Version(s): <br>
0.3.10 (source: server release metadata and changelog, released 2026-04-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
